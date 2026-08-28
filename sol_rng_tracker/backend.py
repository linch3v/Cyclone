"""Log monitoring and Discord delivery for Cyclone."""
import ctypes
import json
import os
import re
import threading
import time
from pathlib import Path
import sys

if getattr(sys, 'frozen', False):
    # Writable per-user settings folder; survives the exe being moved/redownloaded.
    BASE_DIR = Path(os.environ.get("APPDATA", Path.home())) / "Cyclone"
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    # Read-only defaults PyInstaller unpacked alongside the frozen app.
    BUNDLED_DIR = Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
else:
    BASE_DIR = Path(__file__).resolve().parent
    BUNDLED_DIR = BASE_DIR
_stop_event = threading.Event()
_backend_thread = None
_monitor_threads = []
_started_at = None
LOG_ID_SCAN_BYTES = 256 * 1024


def _load_json(filename, default):
    target_path = BASE_DIR / filename
    if not target_path.exists():
        bundled_path = BUNDLED_DIR / filename
        try:
            if bundled_path.is_file():
                target_path.write_bytes(bundled_path.read_bytes())
        except OSError:
            pass  # Fall through; the read below will just use `default`.
    try:
        with target_path.open("r", encoding="utf-8") as file:
            value = json.load(file)
        return value
    except (OSError, json.JSONDecodeError):
        return default


def _save_json(filename, value):
    temporary_path = BASE_DIR / f".{filename}.tmp"
    with temporary_path.open("w", encoding="utf-8") as file:
        json.dump(value, file, indent=2)
        file.write("\n")
    temporary_path.replace(BASE_DIR / filename)


def load_config():
    return _load_json("config.json", {"macro_name": "Cyclone", "version": "1.0.0", "instances": []})


def save_config(config):
    _save_json("config.json", config)


def load_accounts():
    return _load_json("accounts.json", [])


def save_accounts(accounts):
    _save_json("accounts.json", accounts)


def load_biomes():
    biomes = _load_json("biomes.json", [])
    for biome in biomes:
        biome.setdefault("send_message", True)
        if "ping_everyone" not in biome:
            biome["ping_everyone"] = biome.get("ping", False)
    return biomes


def find_roblox_log_files():
    """Return recent Roblox log files from the standard Windows locations."""
    roots = []
    for variable in ("LOCALAPPDATA", "TEMP"):
        value = os.environ.get(variable)
        if value:
            roots.append(Path(value) / "Roblox" / "logs")
    roots.append(Path.home() / "AppData" / "Local" / "Roblox" / "logs")
    files = set()
    for root in roots:
        if root.is_dir():
            files.update(path for path in root.glob("*.log") if path.is_file())
    return sorted(files, key=lambda path: path.stat().st_mtime, reverse=True)


def _account_user_id(account):
    value = account.get("roblox_user_id", account.get("user_id", "")) if account else ""
    value = str(value).strip()
    return value if value.isdigit() else ""


def find_log_user_ids(path):
    """Return Roblox user IDs found in a log's startup header or recent tail."""
    try:
        with path.open("rb") as file:
            header = file.read(LOG_ID_SCAN_BYTES)
            file.seek(0, os.SEEK_END)
            file.seek(max(0, file.tell() - LOG_ID_SCAN_BYTES))
            tail = file.read()
    except OSError:
        return set()
    text = (header + tail).decode("utf-8", errors="replace")
    return set(re.findall(r"\buserid\s*:\s*(\d+)", text, re.IGNORECASE))


def find_log_for_accounts(accounts, excluded_paths=None, current_path=None):
    """Find the newest log whose contents identify one configured account."""
    account_by_id = {
        user_id: account
        for account in accounts
        if (user_id := _account_user_id(account))
    }
    if not account_by_id:
        return None, None
    excluded_paths = excluded_paths or set()
    candidates = []
    for path in find_roblox_log_files():
        path_string = str(path)
        if path_string in excluded_paths:
            continue
        try:
            path.stat()
        except OSError:
            continue
        matched_ids = find_log_user_ids(path) & account_by_id.keys()
        if matched_ids:
            candidates.append((path, account_by_id[next(iter(matched_ids))]))
    return candidates[0] if candidates else (None, None)


def assign_latest_logs(config, accounts=None):
    """Fill auto-managed instances with the newest unused Roblox logs."""
    accounts = accounts or []
    used_paths = set()
    changed = False
    for instance in config.get("instances", []):
        current_path = instance.get("log_path", "")
        if current_path and Path(current_path).is_file():
            used_paths.add(current_path)

    for instance in config.get("instances", []):
        current_path = instance.get("log_path", "")
        if current_path and not instance.get("auto_log", False) and Path(current_path).is_file():
            continue
        account_indices = instance.get("account_indices")
        if account_indices is None:
            account_indices = [instance.get("account_index", 0)]
        instance_accounts = [
            accounts[index] for index in account_indices
            if isinstance(index, int) and 0 <= index < len(accounts)
        ]
        other_instance_paths = used_paths - {current_path}
        matched_path, _ = find_log_for_accounts(instance_accounts, other_instance_paths)
        if matched_path is None and not instance_accounts:
            candidates = [
                path for path in find_roblox_log_files()
                if str(path) not in used_paths
            ]
            matched_path = candidates[0] if candidates else None
        if matched_path:
            if str(matched_path) != current_path:
                changed = True
            instance["log_path"] = str(matched_path)
            instance["auto_log"] = True
            used_paths.add(str(matched_path))
    return changed


def _embed_color(color):
    if isinstance(color, str):
        value = color.strip().lstrip("#")
        if len(value) == 6:
            try:
                return int(value, 16)
            except ValueError:
                pass
    return 0x4AA3DF


def build_webhook_payload(
    biome,
    account,
    config,
    ping_everyone=False,
    event_type="started",
    started_at=None,
    ended_at=None,
    biome_color=None,
):
    username = account.get("username", "Unknown account") if account else "Unknown account"
    private_link = account.get("private_link", "") if account else ""
    description = f"**Account:** {username}"
    if private_link:
        description += f"\n**Server:** [Join server]({private_link})"
    if event_type == "started" and started_at is not None:
        description += f"\n**Started:** <t:{int(started_at)}:t> (<t:{int(started_at)}:R>)"
    elif event_type == "ended" and ended_at is not None:
        description += f"\n**Ended:** <t:{int(ended_at)}:t> (<t:{int(ended_at)}:R>)"
    payload = {
        "embeds": [{
            "title": f"{biome} biome {event_type}",
            "description": description,
            "color": _embed_color(biome_color),
            "footer": {"text": f"{config.get('macro_name', 'Cyclone')} \u2022 v{config.get('version', '1.0.0')}"},
        }]
    }
    if ping_everyone:
        payload["content"] = "@everyone"
        payload["allowed_mentions"] = {"parse": ["everyone"]}
    return payload


def send_webhook(webhook_url, payload):
    if not webhook_url:
        print("Webhook skipped: no Discord webhook destination is configured.")
        return False
    if not webhook_url.startswith(("https://discord.com/api/webhooks/", "https://discordapp.com/api/webhooks/")):
        print("Webhook skipped: destination is not a Discord webhook URL.")
        return False
    try:
        import requests
        response = requests.post(webhook_url, json=payload, timeout=5)
        response.raise_for_status()
        print(f"Webhook sent: {payload['embeds'][0]['title']}")
        return True
    except Exception as error:
        print(f"Webhook send failed ({type(error).__name__}): {error}")
        return False


def find_biome(line, biomes):
    """Return the first configured biome mentioned in a log line."""
    normalized_line = re.sub(r"[^a-z0-9]", "", line.casefold())
    for biome in biomes:
        name = biome.get("name", "")
        normalized_name = re.sub(r"[^a-z0-9]", "", name.casefold())
        if normalized_name and normalized_name in normalized_line:
            return biome
    return None


def trim_working_set():
    if os.name != "nt":
        return False
    try:
        process = ctypes.windll.kernel32.GetCurrentProcess()
        ctypes.windll.psapi.EmptyWorkingSet(process)
        return True
    except (AttributeError, OSError):
        return False


def stop_backend():
    _stop_event.set()


def is_backend_running():
    return _backend_thread is not None and _backend_thread.is_alive()


def get_backend_status():
    return {
        "running": is_backend_running(),
        "started_at": _started_at,
        "active_logs": sum(thread.is_alive() for thread in _monitor_threads),
        "active_log_names": [thread.name for thread in _monitor_threads if thread.is_alive()],
    }


def start_backend_async():
    global _backend_thread
    if is_backend_running():
        return False
    _backend_thread = threading.Thread(target=start_backend, name="CycloneBackend", daemon=True)
    _backend_thread.start()
    return True


def _monitor_instance(instance, config, biomes, accounts):
    account_indices = instance.get("account_indices")
    if account_indices is None:
        account_indices = [instance.get("account_index", 0)]
    selected_accounts = [
        accounts[index] for index in account_indices
        if isinstance(index, int) and 0 <= index < len(accounts)
    ]
    if not selected_accounts:
        selected_accounts = [None]
    current_path = None
    file = None
    matched_account = None
    try:
        last_biome_key = None
        active_biome = None
        biome_started_at = None
        while not _stop_event.is_set():
            if instance.get("auto_log", False):
                path, matched_account = find_log_for_accounts(
                    selected_accounts,
                    current_path=current_path,
                )
            else:
                path = Path(instance.get("log_path", ""))
                matched_account = None
            if path != current_path:
                if file is not None:
                    file.close()
                    file = None
                current_path = path
                if path is not None and path.is_file():
                    file = path.open("r", encoding="utf-8", errors="replace")
                    file.seek(0, os.SEEK_END)
                    last_biome_key = None
                    active_biome = None
                    biome_started_at = None
            if file is None:
                time.sleep(0.5)
                continue
            line = file.readline()
            if not line:
                time.sleep(0.5)
                continue
            biome = find_biome(line, biomes)
            if not biome:
                continue
            event_key = biome["name"].casefold()
            if event_key == last_biome_key:
                continue
            event_at = time.time()
            if active_biome is not None:
                if active_biome.get("send_message", True):
                    target_accounts = [matched_account] if matched_account else selected_accounts
                    for account in target_accounts:
                        payload = build_webhook_payload(
                            active_biome["name"],
                            account,
                            config,
                            active_biome.get("ping_everyone", active_biome.get("ping", False)),
                            event_type="ended",
                            started_at=biome_started_at,
                            ended_at=event_at,
                            biome_color=active_biome.get("color"),
                        )
                        webhook_url = (
                            instance.get("webhook_url")
                            or config.get("webhook_url", "")
                        )
                        send_webhook(webhook_url, payload)
                print(f"{instance.get('name', path.name)}: {active_biome['name']} ended")
            last_biome_key = event_key
            active_biome = biome if biome.get("track", biome.get("enabled", True)) else None
            biome_started_at = event_at if active_biome is not None else None
            if active_biome is not None and biome.get("send_message", True):
                target_accounts = [matched_account] if matched_account else selected_accounts
                for account in target_accounts:
                    payload = build_webhook_payload(
                        biome["name"],
                        account,
                        config,
                        biome.get("ping_everyone", biome.get("ping", False)),
                        event_type="started",
                        started_at=biome_started_at,
                        biome_color=biome.get("color"),
                    )
                    webhook_url = (
                        instance.get("webhook_url")
                        or config.get("webhook_url", "")
                    )
                    send_webhook(webhook_url, payload)
            elif active_biome is not None:
                print(f"{instance.get('name', path.name)}: {biome['name']} detected; Discord message disabled")
            if active_biome is not None:
                print(f"{instance.get('name', path.name)}: {biome['name']}")
    finally:
        if file is not None:
            file.close()


def start_backend():
    global _monitor_threads, _started_at
    config = load_config()
    accounts = load_accounts()
    if assign_latest_logs(config, accounts):
        save_config(config)
    biomes = load_biomes()
    _stop_event.clear()
    _started_at = time.time()
    print(f"{config.get('macro_name', 'Cyclone')} v{config.get('version', '1.0.0')} backend started.")
    threads = []
    for instance in config.get("instances", []):
        if not instance.get("webhook_url") and not config.get("webhook_url"):
            print(f"{instance.get('name', 'Instance')}: no Discord webhook destination configured")
        if not Path(instance.get("log_path", "")).is_file():
            print(f"{instance.get('name', 'Instance')}: Roblox log file not found")
        thread = threading.Thread(
            target=_monitor_instance,
            args=(instance, config, biomes, accounts),
            name=instance.get("name", "Roblox log"),
            daemon=True,
        )
        thread.start()
        threads.append(thread)
    _monitor_threads = threads
    try:
        trim_interval = max(10, int(config.get("trim_interval", 60)))
    except (TypeError, ValueError):
        trim_interval = 60
    while threads and not _stop_event.wait(trim_interval):
        if config.get("ram_trim_enabled", True):
            trim_working_set()
    _monitor_threads = []
    _started_at = None

"""Windows Roblox Anti-AFK worker for Cyclone."""
import ctypes
import os
import re
import threading
import time
from pathlib import Path

SW_RESTORE = 9
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
VK_SPACE = 0x20
_stop_event = threading.Event()
_worker_thread = None
_status = "Stopped"


class _MouseInput(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_long),
        ("y", ctypes.c_long),
        ("mouse_data", ctypes.c_ulong),
        ("flags", ctypes.c_ulong),
        ("timestamp", ctypes.c_ulong),
        ("extra_info", ctypes.c_void_p),
    ]


class _KeyInput(ctypes.Structure):
    _fields_ = [
        ("virtual_key", ctypes.c_ushort),
        ("scan_code", ctypes.c_ushort),
        ("flags", ctypes.c_ulong),
        ("timestamp", ctypes.c_ulong),
        ("extra_info", ctypes.c_void_p),
    ]


class _InputData(ctypes.Union):
    _fields_ = [("mouse", _MouseInput), ("keyboard", _KeyInput)]


class _Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("data", _InputData)]


def _roblox_windows():
    if os.name != "nt":
        return []
    user32 = ctypes.windll.user32
    windows = []
    callback_type = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p)

    @callback_type
    def callback(hwnd):
        if not user32.IsWindowVisible(hwnd):
            return True
        process_id = ctypes.c_ulong()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(process_id))
        try:
            import psutil
            process = psutil.Process(process_id.value)
            if process.name().lower() == "robloxplayerbeta.exe":
                windows.append((hwnd, process_id.value, process.create_time()))
        except Exception:
            pass
        return True

    user32.EnumWindows(callback, 0)
    return windows


def _log_time(path):
    if not path:
        return None
    match = re.search(r"_(\d{8}T\d{6})Z_Player_", Path(path).name)
    if not match:
        return None
    try:
        return time.mktime(time.strptime(match.group(1), "%Y%m%dT%H%M%S"))
    except ValueError:
        return None


def _window_for_log(path, windows, used_processes):
    available = [window for window in windows if window[1] not in used_processes]
    if not available:
        return None
    log_time = _log_time(path)
    if log_time is not None:
        return min(available, key=lambda window: abs(window[2] - log_time))
    return available[0]


def _press_space(hwnd, restore_window=None):
    user32 = ctypes.windll.user32
    if not user32.IsWindow(hwnd):
        return False
    previous_window = user32.GetForegroundWindow()
    current_thread = ctypes.windll.kernel32.GetCurrentThreadId()
    target_thread = user32.GetWindowThreadProcessId(hwnd, None)
    previous_thread = user32.GetWindowThreadProcessId(previous_window, None) if previous_window else 0
    attached_threads = []
    for thread_id in (previous_thread, target_thread):
        if thread_id and thread_id != current_thread and thread_id not in attached_threads:
            if user32.AttachThreadInput(current_thread, thread_id, True):
                attached_threads.append(thread_id)
    try:
        user32.ShowWindow(hwnd, SW_RESTORE)
        user32.BringWindowToTop(hwnd)
        activated = bool(user32.SetForegroundWindow(hwnd))
        if activated:
            user32.SetFocus(hwnd)
    finally:
        for thread_id in reversed(attached_threads):
            user32.AttachThreadInput(current_thread, thread_id, False)
    if not activated or user32.GetForegroundWindow() != hwnd:
        return False
    time.sleep(0.15)
    scan_code = user32.MapVirtualKeyW(VK_SPACE, 0)
    key_down = _Input(1, _InputData(keyboard=_KeyInput(0, scan_code, KEYEVENTF_SCANCODE, 0, None)))
    key_up = _Input(1, _InputData(keyboard=_KeyInput(0, scan_code, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0, None)))
    try:
        sent_down = user32.SendInput(1, ctypes.byref(key_down), ctypes.sizeof(_Input))
        time.sleep(0.25)
        sent_up = user32.SendInput(1, ctypes.byref(key_up), ctypes.sizeof(_Input))
        time.sleep(0.5)
        return sent_down == 1 and sent_up == 1
    finally:
        if restore_window is not None:
            previous_window = restore_window
        if previous_window and previous_window != hwnd and user32.IsWindow(previous_window):
            user32.SetForegroundWindow(previous_window)


def _worker(accounts, mode, interval, log_resolver):
    global _status
    next_at = 0
    while not _stop_event.wait(1):
        if time.time() < next_at:
            continue
        selected_accounts = accounts if mode == "multi" else accounts[:1]
        windows = _roblox_windows()
        original_window = ctypes.windll.user32.GetForegroundWindow()
        used_processes = set()
        used_paths = set()
        successful = 0
        failed = 0
        for account in selected_accounts:
            path, _ = log_resolver([account], excluded_paths=used_paths)
            window = _window_for_log(path, windows, used_processes)
            if window is None:
                failed += 1
                continue
            try:
                if _press_space(window[0], restore_window=None):
                    used_processes.add(window[1])
                    if path:
                        used_paths.add(str(path))
                    successful += 1
                else:
                    failed += 1
            except Exception:
                failed += 1
                continue
            time.sleep(0.75)
        if original_window and ctypes.windll.user32.IsWindow(original_window):
            ctypes.windll.user32.SetForegroundWindow(original_window)
        _status = f"Space delivered: {successful}/{len(selected_accounts)}; failed: {failed}" if selected_accounts else "No accounts configured"
        next_at = time.time() + interval
    _status = "Stopped"


def start(accounts, mode, interval, log_resolver):
    global _worker_thread, _status
    if _worker_thread is not None and _worker_thread.is_alive():
        return False
    _stop_event.clear()
    _status = "Starting"
    _worker_thread = threading.Thread(
        target=_worker,
        args=(accounts, mode, interval, log_resolver),
        name="CycloneAntiAFK",
        daemon=True,
    )
    _worker_thread.start()
    return True


def stop():
    global _status
    _stop_event.set()
    _status = "Stopped"


def is_running():
    return _worker_thread is not None and _worker_thread.is_alive()


def get_status():
    return {"running": is_running(), "status": _status}

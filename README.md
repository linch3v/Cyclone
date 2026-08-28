Cyclone watches multiple Roblox game-instance log files, detects configured Sol's RNG biomes, and optionally sends Discord embeds for each tracked biome.

Quick start

Create and activate a venv (Windows PowerShell):

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Run the app:
powershell
python -m sol_rng_tracker.main
Building the .exe

Cyclone ships as a single-file Windows executable built with PyInstaller. To build it yourself (Windows PowerShell):

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install pyinstaller
pyinstaller Cyclone.spec

The finished executable will be at dist\Cyclone.exe. It's fully self-contained — once built, you can copy just that one file anywhere (a different folder, a different PC) and run it without Python, pip, or any dependencies installed.

Default settings (config.json, accounts.json, biomes.json) are bundled inside the exe. On first launch, they're copied out to %APPDATA%\Cyclone\ and all further reads/writes happen there — your Roblox accounts, Discord webhooks, and biome settings persist per-user and survive the exe being moved or replaced with a newer build.

Configuration

Use the tabs in the application to configure:

Instances: Add one entry per Roblox session, select its account, and enable automatic log detection. Automatic detection matches the configured Roblox user ID in each log and follows newly created active logs in real time.
Accounts: Store the account username, Roblox user ID, and private-server link. These values are persisted to accounts.json (in sol_rng_tracker/ when run from source, or %APPDATA%\Cyclone\ when run as the compiled exe).
Instances: Each instance entry owns its Discord webhook and lets you select multiple accounts for that destination.
Biomes: Independently enable tracking, Discord messages, and @everyone mentions for every biome in biomes.json (same location rules as above).
Anti-AFK: Enable the toggle, choose Single instance or Multiple instances, and enter a custom interval in seconds. When tracking starts, Cyclone finds the matching Roblox process/window, brings it forward, and sends Space directly to it.
Settings: Set the macro name, version, fallback webhook, Windows RAM-trim interval, and whether periodic RAM trimming is enabled. You can also run Trim memory now manually. Settings and instances are persisted to config.json (same location rules as above).

The READMD was written by AI.

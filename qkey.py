import keyboard
import time
import json
import ctypes

SHORTCUTS_FILE = "shortcuts.json"

def load_shortcuts():
    try:
        with open(SHORTCUTS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_shortcuts(shortcuts):
    with open(SHORTCUTS_FILE, "w") as f:
        json.dump(shortcuts, f, indent=4)


def press_shortcut(keys):
    for key in keys:
        ctypes.windll.user32.keybd_event(keyboard.key_to_scan_codes(key)[0], 0, 0, 0)
    time.sleep(0.1)
    for key in keys:
        ctypes.windll.user32.keybd_event(keyboard.key_to_scan_codes(key)[0], 0, 2, 0)


def listen_for_shortcuts(shortcuts):
    key_hold_times = {}

    def on_key_event(event):
        key = event.name

        if key in shortcuts:
            if event.event_type == "down":
                key_hold_times[key] = time.time()
            elif event.event_type == "up":
                if key in key_hold_times:
                    hold_time = time.time() - key_hold_times[key]
                    if hold_time >= 1:  # 1 second hold
                        print(f"✅ Triggering shortcut for '{key}'")
                        press_shortcut(shortcuts[key])
                key_hold_times.pop(key, None)

    keyboard.hook(on_key_event)
    print("🚀 Qkey is running... Hold a key for 1 second to trigger its shortcut. Press ESC to exit.")
    keyboard.wait("esc")


def add_shortcut():
    shortcuts = load_shortcuts()
    key = input("🔑 Enter the key to bind (e.g., 'p'): ").lower()
    shortcut = input("🖥️ Enter the shortcut keys (comma-separated, e.g., 'ctrl,win,right'): ").lower().split(",")

    shortcuts[key] = shortcut
    save_shortcuts(shortcuts)
    print(f"✅ Added shortcut: Hold '{key}' → Triggers {' + '.join(shortcut)}")

# Main function
if __name__ == "__main__":
    print("🎉 Welcome to Qkey!")
    choice = input("1️⃣ Start Qkey\n2️⃣ Add a new shortcut\nChoose (1/2): ").strip()

    if choice == "1":
        shortcuts = load_shortcuts()
        if not shortcuts:
            print("⚠️ No shortcuts found! Add one first.")
        else:
            listen_for_shortcuts(shortcuts)
    elif choice == "2":
        add_shortcut()
    else:
        print("❌ Invalid option. Exiting.")

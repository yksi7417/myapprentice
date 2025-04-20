import subprocess
import psutil
import os
import sys

MAX_TERMINAL_INSTANCES = 3


def count_windows_terminal_instances():
    count = 0
    for proc in psutil.process_iter(attrs=['name']):
        if proc.info['name'] in ("WindowsTerminal.exe", "wt.exe"):
            count += 1
    return count


def launch_windows_terminal_with_limit(max_instances=MAX_TERMINAL_INSTANCES):
    if sys.platform != "win32":
        raise RuntimeError("This function only works on Windows.")

    current_count = count_windows_terminal_instances()
    print(f"Current terminal instances: {current_count}")

    if current_count >= max_instances:
        print(f"Limit reached: {current_count} ≥ {max_instances}. Not launching.")
        return

    wt_path = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe")
    if not os.path.isfile(wt_path):
        raise FileNotFoundError("wt.exe (Windows Terminal) not found.")

    subprocess.Popen([wt_path], creationflags=subprocess.CREATE_NO_WINDOW)
    print("Windows Terminal launched.")


if __name__ == "__main__":
    launch_windows_terminal_with_limit()

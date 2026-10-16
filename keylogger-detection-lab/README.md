# Lab: Keylogger Implementation and Detection Methodologies

This educational repository demonstrates how keystroke logging software functions, the limitations of static signature scanning, and how to implement proactive, real-time background process monitoring.

⚠️ **Disclaimer:** This project is created strictly for authorized educational purposes, security research, and malware analysis studies. 

---

## 🏗️ Architectural Overview & Explanation

This lab breaks down the "cat-and-mouse" nature of security engineering into three distinct phases:

### 1. The Target: `malicious_logger.py` (Script 1)
- **What it does:** Uses the `pynput` library to globally hook into the operating system's keyboard pipeline. 
- **The Mechanism:** Every time a key is pressed, it captures the raw input char or hardware layout name and appends it directly to a local text file called `captured_keystrokes.txt`. It functions across all active applications until `ESC` is pressed.

### 2. The Blueprint Reader: `static_signature_scanner.py` (Script 2)
- **What it does:** Performs **Static Code Analysis** using Python's built-in Abstract Syntax Tree (`ast`) module.
- **The Mechanism:** It treats your code file as a static text document. It reads `malicious_logger.py` without running it, parsing it into syntax tokens. It sweeps these tokens for hardcoded signature keywords like `"pynput"` or `"keyboard.Listener"`.
- **The Limitation:** It cannot tell if the keylogger is currently running. If an attacker changes the variable names or obfuscates the text strings, this script will completely miss it.

### 3. The Real-Time Guard: `live_process_monitor.py` (Script 3 - Enhanced Better Version)
- **What it does:** Performs **Dynamic Runtime Monitoring** using the `psutil` system library.
- **The Mechanism:** This script actively loops in the background of your OS memory loop. It looks at every running Process ID (PID) and inspects its runtime command line arguments. If it detects a background Python instance executing `malicious_logger.py`, it instantly flags it in real-time, displays its process details, and terminates it safely.

---

## 🚀 How to Install & Run the Lab

### Prerequisites
Ensure you have Python 3 installed. Open your terminal or command prompt inside this folder and install the required modules:

```bash
pip install -r requirements.txt
```

### Step 1: Test the Static Code Scanner (Script 2)
Run the signature scanner to see how it can identify malicious source code blueprints sitting on your drive before they ever execute.

```bash
python static_signature_scanner.py
```
* **Expected Output:** The console will list the suspicious lines, functions, and library imports found inside the raw `malicious_logger.py` script.

### Step 2: Start the Real-Time Process Monitor (Script 3)
Open a **new, separate terminal window** and start the active monitor guard loop:

```bash
python live_process_monitor.py
```
* **Expected Output:** The console will print `[🛡️] Proactive Guard Active... Scanning memory loops.` and wait.

### Step 3: Launch the Keylogger (Script 1)
Return to your first terminal window and launch the keylogger script:

```bash
python malicious_logger.py
```

### Step 4: Observe the Real-Time Catch
Watch your **Process Monitor (Script 3)** terminal window. Within seconds, it will detect the background keylogger process running, flag its exact System Process ID (PID), print an alert, and automatically kill the process to protect the system.

---

## 🛠️ The New Script Source Code: `live_process_monitor.py`

Below is the implementation for the proactive dynamic monitor script included in this lab bundle:

```python
import os
import time
import psutil

TARGET_MALWARE_FILE = "malicious_logger.py"

def scan_and_kill_keylogger():
    print(f"[🛡️] Proactive Guard Active... Scanning memory loops for '{TARGET_MALWARE_FILE}'")
    
    try:
        while True:
            # Iterate through all currently running OS background processes
            for process in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = process.info['cmdline']
                    if cmdline:
                        # Inspect the command arguments for our target keylogger script filename
                        if any(TARGET_MALWARE_FILE in argument for argument in cmdline):
                            pid = process.info['pid']
                            name = process.info['name']
                            
                            print(f"\n🚨 [ALERT] Active Keylogger Detected in Background Process Memory!")
                            print(f"   ↳ Process Name: {name}")
                            print(f"   ↳ System PID:   {pid}")
                            print(f"   ↳ Command Line: {' '.join(cmdline)}")
                            print(f"[💥] Attempting to terminate malicious process {pid} immediately...")
                            
                            # Terminate the background keylogger process safely
                            p = psutil.Process(pid)
                            p.terminate()
                            print(f"[✅] Keylogger successfully terminated. System secure.")
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            # Rest the CPU loop briefly before scanning memory tables again
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n[🛡️] Guard deactivated safely by user.")

if __name__ == "__main__":
    scan_and_kill_keylogger()
```

import os

LOG_FILE = "logs/session_log.txt"

def reset_log():
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "w") as f:
        f.write("=== TSLA Hedge Session Log ===\n")

def log_simulation(**kwargs):
    with open(LOG_FILE, "a") as f:
        f.write("\n--- Hedge Simulation ---\n")
        for k, v in kwargs.items():
            f.write(f"{k}: {v}\n")

def log_decision(**kwargs):
    with open(LOG_FILE, "a") as f:
        f.write("\n--- Decision Simulation ---\n")
        for k, v in kwargs.items():
            f.write(f"{k}: {v}\n")

import os
import shutil

def clean_up_logs_and_cache():
    try:
        os.remove("logs/hedge_logs.csv")
        print("✅ Deleted hedge_logs.csv")
    except FileNotFoundError:
        print("ℹ️ No hedge log found to delete.")

    try:
        os.remove("session/selected_exp.txt")
        print("✅ Deleted session expiration file")
    except FileNotFoundError:
        print("ℹ️ No session file found to delete.")

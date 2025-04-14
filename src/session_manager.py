import os

SESSION_FILE = os.path.join(os.path.dirname(__file__), '../session/selected_exp.txt')

def save_selected_expiration(exp_date):
    os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)
    with open(SESSION_FILE, 'w') as f:
        f.write(exp_date)

def get_selected_expiration():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as f:
            return f.read().strip()
    return None

def clear_session():
    try:
        os.remove(SESSION_FILE)
    except FileNotFoundError:
        pass
import os
import glob

def clear_cache_files():
    """Deletes cache files and session logs at the start of a session."""
    cache_patterns = ["puts_*.csv", "logs/*.txt"]

    for pattern in cache_patterns:
        for file in glob.glob(pattern):
            try:
                os.remove(file)
                print(f"🧹 Deleted: {file}")
            except Exception as e:
                print(f"⚠️ Could not delete {file}: {e}")

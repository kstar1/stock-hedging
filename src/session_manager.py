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

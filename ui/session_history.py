# ui/session_history.py
"""Session history tracker using JSON file storage."""
import json, os, datetime

_HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'solve_history.json')

def _load():
    try:
        with open(_HISTORY_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def _save(records):
    with open(_HISTORY_FILE, 'w') as f:
        json.dump(records, f, indent=2)

def add_record(cube_state, solution, move_count):
    """Add a solve record to history."""
    records = _load()
    records.append({
        'timestamp': datetime.datetime.now().isoformat(),
        'cube_state': cube_state,
        'solution': solution,
        'move_count': move_count
    })
    # Keep last 50 records
    if len(records) > 50:
        records = records[-50:]
    _save(records)

def get_history():
    """Return all solve records, newest first."""
    return list(reversed(_load()))

def clear_history():
    """Clear all records."""
    _save([])

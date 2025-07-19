# author: Alysa Jarrell
# A keylogger that tracks key press/release timing and saves session-level features only.

from pynput import keyboard
import time
import csv
import uuid
import os
import pandas as pd

# --- Session setup ---
session_id = str(uuid.uuid4())
char_count = 0
errors_count = 0
start_time = None
end_time = None
keystroke_data = []
last_release_time = None

def on_press(key):
    global last_release_time
    global errors_count
    global start_time

    press_time = time.time()
    if start_time is None:
        start_time = press_time

    try:
        key_char = key.char
    except AttributeError:
        key_char = str(key)

    flight_time = None
    if last_release_time != None:
        flight_time = press_time - last_release_time

    keystroke_data.append({
        'session_id': session_id,
        'press_time': press_time,
        'release_time': None,
        'dwell_time': None,
        'flight_time': flight_time,
        'error': errors_count, 
        'wpm': None
    })

def on_release(key):
    global last_release_time
    global errors_count
    global char_count
    global end_time

    char_count += 1
    release_time = time.time()

    try:
        key_char = key.char
    except AttributeError:
        key_char = str(key)

    for k in reversed(keystroke_data):
        if k['release_time'] is None:
            k['release_time'] = release_time
            k['dwell_time'] = release_time - k['press_time']
            last_release_time = release_time
            break

    #add to error counter if 'backspace' or 'delete' keys are used
    if key == keyboard.Key.backspace or key == keyboard.Key.delete:
        errors_count += 1
        char_count -= 1

    if key == keyboard.Key.esc:
        end_time = release_time
        return False

# --- Start session ---
print("Typing session started. Press ESC to stop.")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# --- WPM Calculation ---
words = char_count / 5
session_time_min = (end_time - start_time) / 60
wpm = words / session_time_min if session_time_min > 0 else 0

print(f"\nTyping session complete.")
print(f"Error count: {errors_count}; Words per minute (WPM): {wpm}")


# --- Store WPM  ---
if keystroke_data:
    # keystroke_data[-1]['error'] = errors_count
    keystroke_data[-1]['wpm'] = wpm


# --- Convert to DataFrame ---
df = pd.DataFrame(keystroke_data)

# Clean numeric fields
for col in ['dwell_time', 'flight_time', 'error', 'wpm']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna(subset=['dwell_time', 'flight_time'])

# --- Extract session-level features ---
features = {
    'dwell_time_mean': df['dwell_time'].mean(),
    'dwell_time_std': df['dwell_time'].std(),
    'flight_time_mean': df['flight_time'].mean(),
    'flight_time_std': df['flight_time'].std(),
    'error_count': df['error'].iloc[-1],
    'wpm_mean': df['wpm'].mean()
}

# --- Save features to file ---
output_dir = "session_features"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, f"session_{session_id}.csv")

pd.DataFrame([features]).to_csv(output_path, index=False)
print(f"Session features saved to: {output_path}")

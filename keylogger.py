# author: Alysa Jarrell
# A keylogger that tracks key presses and release, but does not record actual letters or keys (with the exception of 'backspace' and 'delete').


from pynput import keyboard
# from pynput.keyboard import Key, Listener
import time
import csv
import uuid
import tkinter as tk
from tkinter import StringVar, OptionMenu, Button

#generate a unique session ID so emotion can be attached appropriately
session_id = str(uuid.uuid4())

# counter to hold number of characters typed (use this to determine WPM)
char_count = 0
# counter to hold 'errors' (when 'backspace' or 'delete' keys are used)
errors_count = 0
# start and end time to calculate WPM
start_time = None
end_time = None
# data structure to hold the keystroke info
keystroke_data = []
last_release_time = None

def on_press(key):
    global last_release_time
    global errors_count
    global start_time

    press_time = time.time()
    if start_time == None:
        start_time = press_time
    try:
        key_char = key.char
    except AttributeError:
        key_char = str(key)

    #record flight time from previous key
    flight_time = None
    if last_release_time != None:
        flight_time = press_time - last_release_time
    
    #append all the data to keystroke_data
    keystroke_data.append({
        'session_id' : session_id,
        # 'key' : key_char,
        'press_time': press_time,
        'release_time': None,
        'dwell_time': None,
        'flight_time': flight_time,
        'emotion' : None, #placeholder for later
        'error' : errors_count,
        'wpm' : None #placeholder
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
        # if k ['key'] == key_char and k['release_time'] is None:
        if k['release_time'] is None:
            k['release_time'] = release_time
            k['dwell_time'] = release_time - k['press_time']
            last_release_time = release_time
            break

    #add to error counter if 'backspace' or 'delete' keys are used
    if key == keyboard.Key.backspace:
        errors_count += 1
        char_count -= 1 
    elif key == keyboard.Key.delete:
        errors_count += 1
        char_count -= 1

    #stop listener if ESC is pressed
    if key == keyboard.Key.esc:
        end_time = time.time()
        return False



#start session
print("Typing session started. Press ESC to stop.")
with keyboard.Listener(on_press= on_press, on_release= on_release) as listener:
    listener.join()

# calculate WPM
words = char_count/5
sess_time_min = (end_time - start_time)/60 # session time in minutes
wpm = words/sess_time_min

print( f"\nTyping session complete. This is the error count: {errors_count}, The WPM: {wpm}")


# GUI prompt for emotion label
def get_emotion_label():
    emotion_result = {"value": None}

    def submit():
        emotion_result["value"] = selected_emotion.get()
        root.quit #exits the mainloop
        # root.destroy #destroys the window

    root = tk.Tk()
    root.title("Select Your Emotion")
    root.geometry("350x200")

    selected_emotion = StringVar(root)
    selected_emotion.set("select...") # default
    options = ["Calm", "Stressed", "Frustrated", "Tired", "Other"]
    
    label = tk.Label(root, text= "How would you describe your current emotion?")
    label.pack(pady=10)

    dropdown = OptionMenu(root, selected_emotion, *options)
    dropdown.pack()


    submit_button = Button(root, text= "Submit", command=submit)
    submit_button.pack(pady=10)

    label2 = tk.Label(root, text= "Please select label, press 'Submit', then exit out of window.")
    label2.pack(pady=10)

    root.mainloop()
    return emotion_result["value"]

# add emotion label and wpm to all records
emotion_label = get_emotion_label()
for record in keystroke_data:
    record['emotion'] = emotion_label
    record['wpm'] = wpm

#save the collected data
filename = f'keystroke_session.csv'
with open(filename, 'a', newline='') as file:
    fieldnames = ['session_id', 'press_time', 'release_time', 'dwell_time', 'flight_time', 'emotion', 'error', 'wpm']
    writer = csv.DictWriter(file, fieldnames = fieldnames)
    writer.writeheader()
    for row in keystroke_data:
        writer.writerow(row)




print(f"Data has been saved to {filename}")
# Silent Signals 
## Purpose
The purpose of the “Silent Signals” project is to create a program that uses a person’s typing behavior and patterns to track their emotions. 
It will analyze the keystrokes of the user to detect different emotional states (ex: frustration, calmness, excitement, anger). 
By using data like typing speed, keypress durations and error rates (accuracy) rather than facial recognition or recording the words that are being typed, the user is able to retain more privacy.

## How to use 
First collect data, and train the learning model. 
Once you have a large data set and an accurate trained model exported, you only need to use [session_feature_log.py](session_feature_log.py) and the files listed after it.
More detail is provided throughout the [Files and What They Do](#files-and-what-they-do) section.<br>  

__*It is important to note__ the current data set will not be accurate for your own typing behaviors. 
You will want to create your own dataset (the more data the better) to get results that reflect your own emotions. 
This is due to the differing of typing behaviours for each person.

## Files and What They Do 
### keylogger.py
This file is the initial data collector. 
While running it tracks the key presses (and releases) of a user durring a 'session' without recording the actual key that is being pressed (with the exception of 'backspace' and 'delete').
To end the session press 'esc', it will then print out the error count and words per minute for the session. 
It triggers a pop-up window where you can record your emotion for the session using a dropdown list, (select the emotion, click submit and close the window).
Once an emotion is selected it is added to each line of data and saves the new session to a .csv file.
<br>
Data that is recorded:
- session_id
- press time
- release time
- dwell time
- flight time
- emotion (when given at end)
- error count
- wpm

### keystoke_session.csv
This is where the data from the keylogger is stored. 
Each line represents a character that was pressed in a typing session. 
The information is stored in the same order listed above in the [keylogger.py](keylogger.py) section.

### silentsignals.py
This file (originally created and run in GoogleColab) cleans and transforms the data from keystroke_session.csv to be used in a RandomForestClassifier training model.
(It currently only uses the "stressed" and "calm" emotions for the learning model for the highest accuracy due to a low number of 'frustrated' and 'tired' typing sessions).
Once it converts a session (according to the session_Id) into a single line (using mean and std), it trains a learning model.
At the end of the file it saves and exports the model and leabel encoder for later use.

### session_feature_log.py
This file is almost a copy and paste of the keylogger.py file. It collects all of the same data, but instead of getting the emotion from the user, the data is saved and used to predict the user's emotion.
This file also cleans and transforms the data it just collected into a single line (just like [silentsignals.py](silentsignals) does) and stores it as a .csv file in the "session_features" folder.

### session_features folder
This is a dedicated folder for 'current' typing sessions, they are named as "session_{session_ID}.csv". 
I have since edited some of these file names for ease of switching which file is referenced in [prediction.py](prediction.py) for demostration examples.

### prediction.py
Prediction.py takes a file, loads the trained model and label encoder from [silentsignals.py](silentsignals.py) and predicts the emotion for the given file.
Once the emotion is returned it calls a dashboard that has been created for the emotion. 
(The dashboard options are currently in this file for ease of connecting the emotion, but they are also in [dashboard.py](dashbaord.py).

### dashboard.py
Each emotion has its own dashboard pop-up window.
Calm uses a light green colored background and has a message of encouragement. 
Stressed uses a red background and gives some gentle advice. 
<br>

## What's next?
- Further develop dataset - increase emotions that can be recognized
- Add new dashboards for emotions
- Create a logging system to track your emotions over time. 
  This might also include a color coordinated journal, timestamps/days, various summary options (daily, weekly, monthly, by emotion etc.).
- Add a profile feature to allow multiple users; uses their own data/trained model to make their predictions (serving more people than just me).
- Adjust the 'current' session to be timed (rather than manually starting and stopping it) and update an interactive dashboard periodically.

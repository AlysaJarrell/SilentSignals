import pandas as pd
import pickle
import tkinter as tk
from tkinter import StringVar, OptionMenu, Button

print("starting")


def predict_from_csv(featured_session, model_path='emotion_classifier_rf.pkl', encoder_path='label_encoder.pkl'):
    # Load session data
    session_df = pd.read_csv(featured_session)


    # Load model and label encoder
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    with open(encoder_path, 'rb') as f:
        label_encoder = pickle.load(f)

    # Predict emotion from current session
    predicted_class = model.predict(session_df)[0]
    predicted_emotion = label_encoder.inverse_transform([predicted_class])[0]

    # Return result

    return predicted_emotion


# Calm Dashboard --------------------
def calm_dash():
    root = tk.Tk()
    root.title("Calm")
    root.geometry("350x200")
    root.configure(bg="#92B780")  # Light green background

    label = tk.Label(
        root, 
        text="You're feeling calm. \n\nKeep up the good work!", 
        bg="#92B780",        # Match the label background to the window
        fg="white",            # Text color
        font=("Arial", 14)     # nicer font
    )
    label.place(relx=0.5, rely=0.5, anchor="center")  # Center both axes
    root.mainloop() 


# Stressed Dashboard ---------------------
def stressed_dash():
    root = tk.Tk()
    root.title("Stressed")
    root.geometry("350x200")
    root.configure(bg="#CD4B4B")

    label = tk.Label(
        root, 
        text="It seems like you are stressed. \n\nYou could: \n -Take a 10 minute break. \n -Listen to your favorite song.", 
        bg="#CD4B4B",        # Match the label background to the window
        fg="white",            # Text color
        font=("Arial", 14)     # nicer font
    )
    label.place(relx=0.5, rely=0.5, anchor="center")  # Center both axes
    root.mainloop() 




# this file path can be switched to process a different session easily

featured_session =  "session_features/session_3.csv"
emotion = predict_from_csv(featured_session)
print("Predicted Emotion:", emotion)

# call the proper dashboard for the emotion
if (emotion == "Calm"):
    calm_dash()
elif (emotion == "Stressed"):
    stressed_dash()

import tkinter as tk
from tkinter import Frame, Label, Button, Text, messagebox
import cv2
from PIL import Image, ImageTk  
from keras.models import model_from_json
import numpy as np
import subprocess

# Load the face emotion recognition model
json_file = open("./Models/Faceemotiondetector.json", "r")
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
model.load_weights("./Models/Faceemotiondetector.h5")
haar_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(haar_file)
face_labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}

# Initialize main application window
root = tk.Tk()
root.title("Multi-Screen Tkinter Application")
root.geometry("800x600")
root.configure(bg='black')

# Global variables
cap = None  # Variable to store the video capture object
response_label = None
detected_facial_emotion = None

# Function to show the startup screen
def show_startup_screen():
    clear_window()

    # Frame for Startup Screen
    startup_frame = Frame(root, bg='black')
    startup_frame.pack(expand=True, fill='both')

    # Add a label and a button to the startup screen
    Label(startup_frame, text="Welcome to the Application!", font=("Arial", 24, 'bold'), fg='white', bg='black').pack(pady=60)
    Button(startup_frame, text="Next", font=("Arial", 18, 'bold'), bg='#4CAF50', fg='white', command=show_second_screen, padx=20, pady=10).pack(side='bottom', pady=40)

# Function to show the second screen
def show_second_screen():
    clear_window()

    # Frame for Second Screen
    second_frame = Frame(root, bg='black')
    second_frame.pack(expand=True, fill='both')

    # Add content to the second screen
    Label(second_frame, text="This is the second screen. Click continue to proceed.", font=("Arial", 18), fg='white', bg='black').pack(pady=60)
    Button(second_frame, text="Continue", font=("Arial", 18, 'bold'), bg='#4CAF50', fg='white', command=show_main_screen, padx=20, pady=10).pack(side='bottom', pady=40)

# Function to show the main screen with webcam feed for face emotion detection
def show_main_screen():
    clear_window()

    # Frame for Main Screen
    main_frame = Frame(root, bg='black')
    main_frame.pack(expand=True, fill='both')

    # Left frame for webcam
    left_frame = Frame(main_frame, bg='black')
    left_frame.pack(side='left', fill='both', expand=True)

    # Create a frame to contain the webcam feed
    webcam_frame = Frame(left_frame, bg='black', bd=2, relief='sunken')
    webcam_frame.pack(pady=20, padx=10)

    # Webcam feed display label inside the frame
    webcam_label = Label(webcam_frame, bg='black')
    webcam_label.pack()

    # Start video capture
    global cap
    cap = cv2.VideoCapture(0)  # Open the webcam
    if not cap.isOpened():
        print("Error: Could not open video.")

    # Start updating webcam feed with emotion recognition
    update_webcam_feed(webcam_label)

    # Submit button
    Button(main_frame, text="Submit", font=("Arial", 18, 'bold'), bg='#4CAF50', fg='white', command=show_facial_emotion_popup).pack(side='bottom', pady=20)

# Function to clear the current window content
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# Function to extract features for emotion recognition
def extract_features(image):
    feature = np.array(image)
    feature = feature.reshape(1, 48, 48, 1)
    return feature / 255.0

# Function to update the webcam feed with emotion detection
def update_webcam_feed(webcam_label):
    if cap is not None and cap.isOpened():
        ret, frame = cap.read()  # Read a frame from the webcam
        if ret:
            # Convert frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            # Loop over detected faces and predict emotion
            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face_resized = cv2.resize(face, (48, 48))
                img = extract_features(face_resized)
                pred = model.predict(img)
                global detected_facial_emotion
                detected_facial_emotion = face_labels[pred.argmax()]

                # Draw rectangle and label for each face
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, detected_facial_emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Convert frame to ImageTk format for displaying in Tkinter
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)

            # Update the webcam label with the new frame
            webcam_label.imgtk = imgtk
            webcam_label.configure(image=imgtk)
        
        # Call the update function again after 10 milliseconds
        webcam_label.after(10, update_webcam_feed, webcam_label)
    else:
        # Ensure the capture object is released
        if cap is not None:
            cap.release()

# Function to show the detected facial emotion in a pop-up box
def show_facial_emotion_popup():
    if detected_facial_emotion:
        # Stop the webcam feed when showing the pop-up
        if cap is not None:
            cap.release()
        
        messagebox.showinfo("Facial Emotion Detected", f"The detected emotion is: {detected_facial_emotion}")
        show_text_input_screen()
    else:
        messagebox.showerror("Error", "No face detected. Please try again.")

# Function to show the fourth screen with text input box in the middle
def show_text_input_screen():
    clear_window()

    print(detected_facial_emotion)

    # Frame for Text Input Screen
    text_input_frame = Frame(root, bg='black')
    text_input_frame.pack(expand=True, fill='both')

    # Text input area in the middle of the screen
    Label(text_input_frame, text="Enter your text:", font=("Arial", 18), fg='white', bg='black').pack(pady=20)
    text_area = Text(text_input_frame, height=5, width=50, font=("Arial", 14), bg='white', fg='black')
    text_area.pack(pady=20)

    # Submit button for text input
    Button(text_input_frame, text="Submit Text", font=("Arial", 18, 'bold'), bg='#4CAF50', fg='white', command=lambda: process_text_emotion(text_area.get("1.0", "end-1c").strip())).pack(pady=20)

# Function to process the text emotion and show the fifth screen
def process_text_emotion(text):
    if text:
        try:
            detected_text_emotion = subprocess.check_output(
                ["python", "hick.py", text],
                universal_newlines=True
            ).strip()  # Get detected emotion from hick.py

            show_response_screen(detected_text_emotion)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error detecting text emotion: {e}")
    else:
        messagebox.showwarning("Input Error", "Please enter some text.")

# Function to show the fifth screen with the combined response
def show_response_screen(text_emotion):
    clear_window()

    # Frame for Response Screen
    response_frame = Frame(root, bg='black')
    response_frame.pack(expand=True, fill='both')

    # Show both facial and text emotions
    Label(response_frame, text=f"Facial Emotion: {detected_facial_emotion}", font=("Arial", 18), fg='white', bg='black').pack(pady=20)
    Label(response_frame, text=f"Text Emotion: {text_emotion}", font=("Arial", 18), fg='white', bg='black').pack(pady=20)

    # Send both emotions to responses.py
    try:
        result = subprocess.check_output(
            ["python", "Finalresponses.py", text_emotion, detected_facial_emotion],
            universal_newlines=True
        ).strip()

        # Display the result
        Label(response_frame, text=f"Response: {result}", font=("Arial", 18), fg='white', bg='black', wraplength=600).pack(pady=20)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error getting response: {e}")

    # Exit button
    Button(response_frame, text="Exit", font=("Arial", 18, 'bold'), bg='#F44336', fg='white', command=root.quit).pack(side='bottom', pady=20)

# Start the application with the startup screen
show_startup_screen()

# Run the Tkinter event loop
root.mainloop()

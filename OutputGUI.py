import tkinter as tk
from tkinter import Frame, Label, Button, Text, messagebox,PhotoImage
import cv2
from PIL import Image, ImageTk  
from keras.models import model_from_json
import numpy as np
import subprocess

json_file = open("./Models/Faceemotiondetector.json", "r")
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
model.load_weights("./Models/Faceemotiondetector.h5")
haar_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(haar_file)
face_labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}

root = tk.Tk()
root.title("Online Therapist")
root.geometry("800x600")
root.configure(bg='black')

global canvas
cap = None  
response_label = None
detected_facial_emotion = None
bg_image=None

def on_enter(e):
    start_button['background'] = 'black'  
    start_button['foreground'] = 'white'

def on_leave(e):
    start_button['background'] = 'white'  
    start_button['foreground'] = 'black'

def show_startup_screen():
    clear_window()
    global bg_image

    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack(fill="both", expand=True)
    

    bg_image = PhotoImage(file="background.png")  
    canvas.create_image(0, 0, image=bg_image, anchor="nw")
    canvas.create_text(400, 150, text="Online Therapist", font=("Helvetica", 36, "bold"), fill="#edf1f7")
    canvas.create_text(400, 250, text="\"Step into a space of healing\"!!", font=("Helvetica", 18), fill="#4B0082")
    global start_button
    start_button = tk.Button(root, text="Get Started", font=("Helvetica", 16, "bold"),
                             bg='#ffffff', fg='black', activebackground='black', activeforeground='white',
                             relief="flat", borderwidth=0, padx=20, pady=10,command=show_second_screen)
    start_button.bind("<Enter>", on_enter)
    start_button.bind("<Leave>", on_leave)

    canvas.create_window(400, 350, anchor="center", window=start_button, width=200)

def show_second_screen():
    clear_window()
    global bg_image

    second_frame = Frame(root, bg='black')
    second_frame.pack(expand=True, fill='both')

    bg_image = PhotoImage(file="background.png") 
    bg_label = tk.Label(second_frame, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    scrollbar = tk.Scrollbar(second_frame)
    scrollbar.pack(side="right", fill="y")

    terms_text = tk.Text(second_frame, wrap="word", yscrollcommand=scrollbar.set, font=("Helvetica", 12), bg="white")
    terms_text.pack(pady=10, padx=10, fill="both", expand=True)

    scrollbar.config(command=terms_text.yview)

    terms_content = """
    Welcome to the Online Therapist platform. By using this application, you agree to the following terms and conditions:

    1. **Use of Webcam**: 
       - The Online Therapist application will access your device's webcam to detect facial expressions and predict emotional states using advanced facial recognition technology.
       - The webcam data is processed in real-time and is not stored unless explicit consent is provided by the user.

    2. **Personal Information**:
       - We collect personal information such as name, email, and emotional feedback to enhance the user experience.
       - This data is confidential and will only be used to provide personalized therapy recommendations.
       - Your data will not be shared with third parties without your consent, except as required by law.

    3. **Security**:
       - We take the security of your personal information seriously and implement various security measures to protect your data.

    4. **Consent**:
       - By using this application, you consent to the collection and use of your personal information and webcam data as described in this agreement.
       - You may revoke consent at any time by contacting support, but certain features may become unavailable.

    5. **Privacy Policy**:
       - For more information on how we handle your data, please refer to our Privacy Policy available on our website.

    Please read these terms carefully and click 'Agree' if you consent to the use of your personal data and webcam as described.
    """

    terms_text.insert(tk.END, terms_content)

    terms_text.config(state="disabled")
    Button(second_frame, text="Continue", font=("Arial", 18, 'bold'), bg='#ffffff', fg='black', command=show_main_screen, padx=20, pady=10).pack(side='bottom', pady=40)


def show_main_screen():
    clear_window()
    global bg_image
    main_frame = Frame(root, bg='black')
    main_frame.pack(expand=True, fill='both')

    bg_image = PhotoImage(file="background.png")  
    bg_label = tk.Label(main_frame, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    
    webcam_frame = Frame(main_frame, bg='black', bd=2, relief='sunken')
    webcam_frame.pack(pady=20, padx=10)
    Label(webcam_frame, text="Express your feelings in much more detailed way:", font=("Arial", 18), fg='white', bg='black').pack(pady=20)

    webcam_label = Label(webcam_frame, bg='black')
    webcam_label.pack()

    global cap
    cap = cv2.VideoCapture(0)  
    if not cap.isOpened():
        print("Error: Could not open video.")

    update_webcam_feed(webcam_label)

    Button(main_frame, text="Submit", font=("Arial", 18, 'bold'), bg='#ffffff', fg='black', command=show_facial_emotion_popup).pack(side='bottom', pady=20)

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def extract_features(image):
    feature = np.array(image)
    feature = feature.reshape(1, 48, 48, 1)
    return feature / 255.0

def update_webcam_feed(webcam_label):
    if cap is not None and cap.isOpened():
        ret, frame = cap.read()  
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face_resized = cv2.resize(face, (48, 48))
                img = extract_features(face_resized)
                pred = model.predict(img)
                global detected_facial_emotion
                detected_facial_emotion = face_labels[pred.argmax()]

                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, detected_facial_emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)

            webcam_label.imgtk = imgtk
            webcam_label.configure(image=imgtk)
        
        webcam_label.after(10, update_webcam_feed, webcam_label)
    else:
        if cap is not None:
            cap.release()

def show_facial_emotion_popup():
    if detected_facial_emotion:
        if cap is not None:
            cap.release()
        
        messagebox.showinfo("Facial Emotion Detected", f"The detected emotion is: {detected_facial_emotion}")
        show_text_input_screen()
    else:
        messagebox.showerror("Error", "No face detected. Please try again.")

def show_text_input_screen():
    clear_window()
    global bg_image
    print(detected_facial_emotion)

    text_input_frame = Frame(root, bg='black')
    text_input_frame.pack(expand=True, fill='both')

    bg_image = PhotoImage(file="background.png")  
    bg_label = tk.Label(text_input_frame, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    Label(text_input_frame, text="Express your feelings in much more detailed way:", font=("Arial", 18), fg='white', bg='black').pack(pady=20)
    text_area = Text(text_input_frame, height=5, width=50, font=("Arial", 14), bg='white', fg='black')
    text_area.pack(pady=20)

    Button(text_input_frame, text="Submit Text", font=("Arial", 18, 'bold'), bg='#ffffff', fg='black', command=lambda: process_text_emotion(text_area.get("1.0", "end-1c").strip())).pack(pady=20)

def process_text_emotion(text):
    if text:
        try:
            detected_text_emotion = subprocess.check_output(
                ["python", "hick.py", text],
                universal_newlines=True
            ).strip()  

            show_response_screen(detected_text_emotion)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error detecting text emotion: {e}")
    else:
        messagebox.showwarning("Input Error", "Please enter some text.")

def show_response_screen(text_emotion):
    clear_window()
    global bg_image
    response_frame = Frame(root, bg='black')
    response_frame.pack(expand=True, fill='both')

    bg_image = PhotoImage(file="background.png")  
    bg_label = tk.Label(response_frame, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    Label(response_frame, text=f"Facial Emotion: {detected_facial_emotion}", font=("Arial", 18), fg='white', bg='black').pack(pady=20)
    Label(response_frame, text=f"Text Emotion: {text_emotion}", font=("Arial", 18), fg='white', bg='black').pack(pady=20)

    try:
        result = subprocess.check_output(
            ["python", "Finalresponses.py", text_emotion, detected_facial_emotion],
            universal_newlines=True
        ).strip()

        Label(response_frame, text=f"Response: {result}", font=("Arial", 18), fg='white', bg='black', wraplength=600).pack(pady=20)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error getting response: {e}")

    Button(response_frame, text="Exit", font=("Arial", 18, 'bold'), bg='#ffffff', fg='black', command=root.quit).pack(side='bottom', pady=20)

show_startup_screen()



root.mainloop()
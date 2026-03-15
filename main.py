import cv2
import mediapipe as mp
import pyautogui
import math
import time
import pyttsx3
from twilio.rest import Client
from tkinter import *
from tkinter import font as tkFont


ACCOUNT_SID = ''          
AUTH_TOKEN = ''            
TWILIO_PHONE_NUMBER = '' 
TARGET_PHONE_NUMBER = '+91'      

BLINK_THRESHOLD = 0.28  
CLICK_DURATION_THRESHOLD = 0.15 
SENSITIVITY = 1.8


pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0 

screen_w, screen_h = pyautogui.size()

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1, 
    refine_landmarks=True,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

blink_start_time = 0
is_blinking = False
click_executed = False 

def trigger_alert(phrase):
    print(f"Action: {phrase}")
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 130) 
        engine.say(phrase)
        engine.runAndWait()
    except: pass

    if phrase == "I need help":
        
        try:
            client = Client(ACCOUNT_SID, AUTH_TOKEN)
            client.messages.create(
                body=f"🚨 EMERGENCY: {phrase}",
                from_=TWILIO_PHONE_NUMBER,
                to=TARGET_PHONE_NUMBER
            )
        except: print("SMS Error")

def calculate_ear(eye_landmarks, frame_w, frame_h):
    try:
        
        p2_p6 = math.hypot((eye_landmarks[1].x - eye_landmarks[5].x) * frame_w, (eye_landmarks[1].y - eye_landmarks[5].y) * frame_h)
        p3_p5 = math.hypot((eye_landmarks[2].x - eye_landmarks[4].x) * frame_w, (eye_landmarks[2].y - eye_landmarks[4].y) * frame_h)
        p1_p4 = math.hypot((eye_landmarks[0].x - eye_landmarks[3].x) * frame_w, (eye_landmarks[0].y - eye_landmarks[3].y) * frame_h)
        return (p2_p6 + p3_p5) / (2.0 * p1_p4)
    except: return 0.3

def eye_tracking_loop():
    global blink_start_time, is_blinking, click_executed
    ret, frame = cam.read()
    if not ret:
        root.after(1, eye_tracking_loop)
        return

    frame = cv2.flip(frame, 1)
    frame_h, frame_w, _ = frame.shape
    results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    status, ear_val = "Normal", "0.00"

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        
        
        iris = [landmarks[i] for i in [474, 475, 476, 477]]
        ix = sum(p.x for p in iris) / 4
        iy = sum(p.y for p in iris) / 4
        pyautogui.moveTo(int(ix * screen_w * SENSITIVITY), int(iy * screen_h * SENSITIVITY), _pause=False)

        
        eye = [landmarks[i] for i in [362, 385, 387, 263, 373, 380]]
        ear = calculate_ear(eye, frame_w, frame_h)
        ear_val = f"{ear:.2f}"

        curr_t = time.time()
        if ear < BLINK_THRESHOLD:
            if not is_blinking:
                is_blinking = True
                blink_start_time = curr_t
                click_executed = False 
            
            
            if not click_executed and (curr_t - blink_start_time) > CLICK_DURATION_THRESHOLD:
                pyautogui.click()
                click_executed = True
                status = "CLICKED! ✅"
            else:
                status = "BLINKING..."
        else:
            is_blinking = False
            status = "Ready"

    ear_value_label.config(text=f"EAR: {ear_val}")
    blink_status_label.config(text=f"Status: {status}")
    root.after(1, eye_tracking_loop) 


root = Tk()
root.title("Iris HCI Assistant Pro")
root.geometry("1200x900")
root.configure(bg="#1a1a2e")

title_f = tkFont.Font(family="Helvetica", size=24, weight="bold")
btn_f = tkFont.Font(family="Helvetica", size=13, weight="bold")

Label(root, text="👁️ Iris HCI Communication Board", font=title_f, bg="#16213e", fg="white", pady=20).pack(fill="x")

stat_f = Frame(root, bg="#0f3460")
stat_f.pack(pady=5, fill="x")
ear_value_label = Label(stat_f, text="EAR Value: 0.00", font=("Helvetica", 15, "bold"), bg="#0f3460", fg="yellow")
ear_value_label.pack(side="left", padx=60, pady=10)
blink_status_label = Label(stat_f, text="Status: Ready", font=("Helvetica", 15, "bold"), bg="#0f3460", fg="lightgreen")
blink_status_label.pack(side="right", padx=60, pady=10)

text_area = Text(root, height=5, font=("Helvetica", 22), bg="#e8f6ef", fg="#1a1a2e", relief="flat", borderwidth=15)
text_area.pack(pady=15, padx=40, fill="x")

comm_frame = Frame(root, bg="#1a1a2e")
comm_frame.pack(pady=10)
phrases = ["Hello", "Thank You", "Yes", "No", "I need help", "I'm hungry", "I'm thirsty", "Bathroom"]

for i, p in enumerate(phrases):
    btn = Button(comm_frame, text=p, bg="#533483", fg="white", font=btn_f, width=18, height=2,
                 relief="flat", command=lambda x=p: [text_area.insert("end", x + ". "), trigger_alert(x)])
    btn.grid(row=i//4, column=i%4, padx=10, pady=10)

kb_frame = Frame(root, bg="#1a1a2e")
kb_frame.pack()

def kb_act(k):
    if k == "<-": text_area.delete("end-2c", "end-1c")
    elif k == "Space": text_area.insert("end", " ")
    elif k == "CLEAR ALL": text_area.delete("1.0", "end")
    else: text_area.insert("end", k)

rows = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'], 
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'], 
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Space', '<-'],
        ['CLEAR ALL']]

for r in rows:
    f = Frame(kb_frame, bg="#1a1a2e")
    f.pack()
    for k in r:
        color = "#e94560" 
        width = 5
        if k == "Space": width = 15
        if k == "CLEAR ALL": 
            width = 25
            color = "#f0932b" 
        Button(f, text=k, bg=color, fg="white", font=btn_f, width=width, height=2,
               relief="flat", command=lambda x=k: kb_act(x)).pack(side="left", padx=4, pady=4)

cam = cv2.VideoCapture(0)
if cam.isOpened(): eye_tracking_loop()
root.mainloop()
cam.release()
cv2.destroyAllWindows()
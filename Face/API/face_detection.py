import cv2
import numpy as np
import os, shutil
import time
import pyscreenshot as ImageGrab
from datetime import datetime
from face_api import facerec
import requests
from controller import *

def clearFolder():
    folder = 'C:\\Users\\vtcst\\Desktop\\Client_Server\\Face\\API\\Entrance'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def start():
    count = 0
    clearFolder()
    # cap = cv2.VideoCapture(1)
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret,frame = cap.read()

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            # startTime = 0
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 5)
            if w * h < 100000:
                cv2.putText(frame, "Please move closer", (x, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 200), 2)
                # print(w * h)
            elif w * h > 100000:
                image_name = f"screenshot_{str(count)}"
                filepath = f"C:\\Users\\vtcst\\Desktop\\Client_Server\\Face\\API\\Entrance\\{image_name}.png"
                cv2.imwrite(filepath, frame)
                name = facerec(filepath)
                if name != "":
                    name, id = facerec(filepath).split("_")
                    print("Valid")
                    cv2.putText(frame, "Welcome " + name + " " + id, (x, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 200, 0), 2)
                    # send msg to SERVER
                    data = {'status': True}
                    res = requests.post('http://127.0.0.1:3000/gatestate', json=data)
                    returned_data = res.json()
                    print(returned_data)
                    door(returned_data['result'])
                    time.sleep(1)
                else:
                    print("Invalid")
                    cv2.putText(frame, "Please try again ", (x, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 200), 2)
                    data = {'status': False}
                    res = requests.post('http://127.0.0.1:3000/gatestate', json=data)
                    returned_data = res.json()
                    print(returned_data)
                    door(returned_data['result'])
                    time.sleep(1)
                count += 1

        
        cv2.imshow('Face Detection', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cap.destroyAllWindows()

start()
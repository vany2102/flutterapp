import requests

import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
from mediapipe.framework.formats import landmark_pb2
from surya_namaskar import evaluate_surya_namaskar_pose


def get_landmark_coordinates(image_path):
    # Initialize a list to store x and y coordinates
    landmark_coordinates = []

    cap = cv2.VideoCapture(image_path)
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        landmarks = results.pose_landmarks.landmark

        # Extract x and y coordinates from the landmark subset
        for landmark in landmarks:
            x, y, z = landmark.x, landmark.y, landmark.z
            landmark_coordinates.append((x, y))

    return landmark_coordinates


data_to_send = get_landmark_coordinates('./vajra.jpg')
print(data_to_send)
print(mp_pose.PoseLandmark.LEFT_SHOULDER.value)
a = data_to_send[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
b = type(a)
print(b)

asana_to_evaluate = "surya_namaskar" 


if asana_to_evaluate == "surya_namaskar":
    suggestions = evaluate_surya_namaskar_pose(data_to_send)


for suggestion in suggestions:
    print(suggestion)

response = requests.post('http://localhost:5000/get_array', json=suggestions)

if response.status_code == 200:
    print('Data sent successfully.')
else:
    print('Failed to send data.')

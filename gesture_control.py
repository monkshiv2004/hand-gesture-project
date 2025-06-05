import cv2
import mediapipe as mp
import pyautogui
import time
import webbrowser
import numpy as np
from collections import deque

THUMB_TIP, INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP, WRIST = 4, 8, 12, 16, 20, 0
INDEX_PIP, MIDDLE_PIP, RING_PIP, PINKY_PIP = 6, 10, 14, 18

KEY_MAP = {
    "fullscreen": 'f',
    "pause": 'k',
    "volume_up": 'up',
    "volume_down": 'down',
    "forward": 'l',
    "rewind": 'j',
    "mute": 'm',
    "next_video": ['shift', 'n'],
    "prev_video": ['shift', 'p'],
    "speed_up": ['shift', '.'],
    "speed_down": ['shift', ',']
}

CONTINUOUS_GESTURES = {"volume_up", "volume_down", "speed_up", "speed_down"}


def fingers_up(landmarks, handedness):
    fingers = []
    if handedness == "Right":
        fingers.append(landmarks[THUMB_TIP].x > landmarks[THUMB_TIP - 1].x)
    else:
        fingers.append(landmarks[THUMB_TIP].x < landmarks[THUMB_TIP - 1].x)

    fingers.append(landmarks[INDEX_TIP].y < landmarks[INDEX_PIP].y)
    fingers.append(landmarks[MIDDLE_TIP].y < landmarks[MIDDLE_PIP].y)
    fingers.append(landmarks[RING_TIP].y < landmarks[RING_PIP].y)
    fingers.append(landmarks[PINKY_TIP].y < landmarks[PINKY_PIP].y)

    return fingers


def classify_gesture(landmarks, handedness):
    fingers = fingers_up(landmarks, handedness)
    thumb, index, middle, ring, pinky = fingers
    
    if index and not any([thumb, middle, ring, pinky]):
        return "pause"
    if all(fingers):
        return "fullscreen"
    if index and middle and not any([ring, pinky, thumb]):
        return "volume_down"
    if thumb and not any([index, middle, ring, pinky]):
        return "volume_up"
    if pinky and not any([index, middle, ring, thumb]):
        return "mute"
    if index and middle and ring and not any([thumb, pinky]):
        return "rewind"
    if thumb and index and not any([middle, ring, pinky]):
        return "next_video"
    if thumb and pinky and not any([index, middle, ring]):
        return "prev_video"
    if index and ring and not any([thumb, middle, pinky]):
        return "speed_up"
    if middle and pinky and not any([thumb, index, ring]):
        return "speed_down"
    
    if index and middle and ring and pinky and not thumb:
        return "forward"
    return None


def execute_action(gesture):
    try:
        if gesture in KEY_MAP:
            key = KEY_MAP[gesture]
            if isinstance(key, list):
                pyautogui.hotkey(*key)
            else:
                pyautogui.press(key)
    except Exception as e:
        print(f"Error executing action for gesture '{gesture}': {e}")


def main():
    webbrowser.open("https://www.youtube.com")
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access webcam.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    current_gesture = None
    gesture_start_time = None
    repeat_interval = 0.4

    try:
        while True:
            success, frame = cap.read()
            if not success:
                print("Error: Failed to read frame.")
                break

            frame = cv2.resize(frame, (480, 360))
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)
            gesture = None

            if results.multi_hand_landmarks and results.multi_handedness:
                for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    landmarks = hand_landmarks.landmark
                    handedness_label = hand_handedness.classification[0].label
                    gesture = classify_gesture(landmarks, handedness_label)
            else:
                if current_gesture not in CONTINUOUS_GESTURES:
                    current_gesture = None
                    gesture_start_time = None
                cv2.putText(frame, 'No hand detected', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            if gesture:
                if gesture == current_gesture:
                    if gesture in CONTINUOUS_GESTURES:
                        if time.time() - gesture_start_time > 0.2:
                            execute_action(gesture)
                            gesture_start_time = time.time()
                else:
                    current_gesture = gesture
                    gesture_start_time = time.time()
                    execute_action(gesture)

                cv2.putText(frame, f'Gesture: {str(gesture)}', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow("Gesture Control", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        hands.close()


if __name__ == "__main__":
    main()

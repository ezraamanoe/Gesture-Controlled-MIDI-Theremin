import cv2
import mediapipe as mp
import numpy as np

def get_finger_states(hand_landmarks):
    fingers = []
    tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky tips
    mcp = [2, 5, 9, 13, 17]  # MCP joints for comparison
    
    threshold = 0.02  # Adjusted sensitivity threshold
    for i in range(1, 5):  # Index to Pinky
        fingers.append(hand_landmarks.landmark[tips[i]].y < hand_landmarks.landmark[mcp[i]].y - threshold)
    
    # Improved thumb detection
    thumb_tip = hand_landmarks.landmark[tips[0]]
    thumb_mcp = hand_landmarks.landmark[mcp[0]]
    wrist = hand_landmarks.landmark[0]
    
    # Thumb is considered extended if it's farther from the palm center (wrist) in X direction
    fingers.insert(0, abs(thumb_tip.x - wrist.x) > abs(thumb_mcp.x - wrist.x) + threshold)
    
    return fingers

def recognize_gesture(fingers):
    if fingers == [0, 0, 0, 0, 0]:
        return "Fist"
    elif fingers == [1, 1, 1, 1, 1]:
        return "Open Palm"
    elif fingers == [0, 1, 0, 0, 0]:
        return "Point"
    elif fingers == [0, 1, 1, 0, 0]:
        return "Peace"
    elif fingers == [0, 1, 0, 0, 1]:
        return "Rock"
    else:
        return "Unknown"

def main():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.6)  # Lowered sensitivity
    mp_draw = mp.solutions.drawing_utils
    
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)
        
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                fingers = get_finger_states(hand_landmarks)
                gesture = recognize_gesture(fingers)

                landmark_spec = mp_draw.DrawingSpec(color=(255, 0, 0))
                connection_spec = mp_draw.DrawingSpec(color=(0, 0, 0))
                
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS, landmark_spec, connection_spec)
                cv2.putText(frame, gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        
        cv2.imshow("Hand Gesture Recognition", frame)
        if cv2.waitKey(1) & 0x00 == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()



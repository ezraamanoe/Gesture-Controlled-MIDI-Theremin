import cv2
import mediapipe as mp
from generate_midi import GenerateMidi

class HandTracker:
    def __init__(self, min_detection_conf=0.7, min_tracking_conf=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=min_detection_conf,
            min_tracking_confidence=min_tracking_conf
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.midi = GenerateMidi()
        self.current_gesture = None  # Track the current gesture

    def get_finger_states(self, hand_landmarks):
        """Determine which fingers are extended."""
        fingers = []
        tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky tips
        mcp = [2, 5, 9, 13, 17]  # MCP joints for comparison
        threshold = 0.02  

        # Check for each finger (excluding thumb)
        for i in range(1, 5):  
            fingers.append(hand_landmarks.landmark[tips[i]].y < hand_landmarks.landmark[mcp[i]].y - threshold)

        # Thumb detection logic
        thumb_tip = hand_landmarks.landmark[tips[0]]
        thumb_mcp = hand_landmarks.landmark[mcp[0]]
        wrist = hand_landmarks.landmark[0]

        # Thumb is extended if its x-position is significantly away from MCP & wrist
        fingers.insert(0, (thumb_tip.x > thumb_mcp.x) if wrist.x < thumb_mcp.x else (thumb_tip.x < thumb_mcp.x))

        return fingers

    def recognize_gesture(self, fingers):
        """Recognize hand gesture based on extended fingers."""
        gesture = "Unknown"
        if fingers == [0, 0, 0, 0, 0]:
            gesture = "Fist"
        elif fingers == [1, 1, 1, 1, 1]:
            gesture = "Open Palm"
        elif fingers == [0, 1, 0, 0, 0]:
            gesture = "Point"
        elif fingers == [0, 1, 1, 0, 0]:
            gesture = "Peace"
        elif fingers == [0, 1, 0, 0, 1]:
            gesture = "Rock"

        # Only trigger effects on gesture changes
        if gesture != self.current_gesture:
            # Stop the current effect if any
            if self.midi.active_effect:
                self.midi.start_effect("stop_current_effect")

            # Start the new effect based on the gesture
            if gesture == "Open Palm":
                self.midi.start_effect("reverb")
            elif gesture == "Point":
                self.midi.start_effect("volume")
            elif gesture == "Peace":
                self.midi.start_effect("delay")
            elif gesture == "Rock":
                # Reset all effects for Rock gesture
                self.midi.start_effect("stop_current_effect")
            
            self.current_gesture = gesture

        return gesture

    def process_frame(self, frame):
        """Process frame and detect hand landmarks."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            hand_landmarks = result.multi_hand_landmarks[0]  # Take only the first detected hand

            # Get bounding box coordinates
            h, w, _ = frame.shape
            x_min, y_min = w, h
            x_max, y_max = 0, 0

            for landmark in hand_landmarks.landmark:
                x, y = int(landmark.x * w), int(landmark.y * h)
                x_min, y_min = min(x_min, x), min(y_min, y)
                x_max, y_max = max(x_max, x), max(y_max, y)

            # Expand the box slightly for better visibility
            padding = 20
            x_min = max(0, x_min - padding)
            y_min = max(0, y_min - padding)
            x_max = min(w, x_max + padding)
            y_max = min(h, y_max + padding)

            # Draw a single bounding box
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)

            # Place text above the box
            fingers = self.get_finger_states(hand_landmarks)
            gesture = self.recognize_gesture(fingers)
            cv2.putText(frame, gesture, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)

        return frame

    def run(self):
        """Main loop to capture video and process frames."""
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            processed_frame = self.process_frame(frame)

            cv2.imshow("Hand Gesture Recognition", processed_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

# Run the hand tracker
if __name__ == "__main__":
    tracker = HandTracker()
    tracker.run()
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
            gesture = "Stop"
            self.midi.start_effect("Stop")  # Reset to 0 semitones
        elif fingers == [1, 1, 1, 1, 1]:
            gesture = "Major Fifth"
            self.midi.start_effect("Major Fifth") # +7 semitones (major fifth)
        elif fingers == [0, 1, 1, 1, 0]:
            gesture = "Major Third"
            self.midi.start_effect("Major Third")  # +4 semitones (major third)
        elif fingers == [0, 1, 1, 0, 0]:
            gesture = "Minor Third"
            self.midi.start_effect("Minor Third")  # +3 semitones (minor third)
        elif fingers == [0, 1, 0, 0, 0]:
            gesture = "Octave"
            self.midi.start_effect("Octave") # +12 semitones (octave)
        elif fingers == [0, 1, 0, 0, 1]:
            gesture = "Tritone"
            self.midi.start_effect("Tritone") # +6 semitones (tritone)

        return gesture

    def process_frame(self, frame):
        """Process frame and detect hand landmarks."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Get the bounding box coordinates for the hand (based on landmarks)
                x_min = min([hand_landmarks.landmark[i].x for i in range(21)])
                x_max = max([hand_landmarks.landmark[i].x for i in range(21)])
                y_min = min([hand_landmarks.landmark[i].y for i in range(21)])
                y_max = max([hand_landmarks.landmark[i].y for i in range(21)])

                # Convert normalized coordinates to pixel values (assuming frame is in BGR)
                h, w, _ = frame.shape
                x_min, x_max = int(x_min * w), int(x_max * w)
                y_min, y_max = int(y_min * h), int(y_max * h)

                # Draw a square/rectangle around the hand
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)

                # Get the finger states and recognize the gesture
                fingers = self.get_finger_states(hand_landmarks)
                gesture = self.recognize_gesture(fingers)

                # Display the gesture text on top of the square
                cv2.putText(frame, gesture, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

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
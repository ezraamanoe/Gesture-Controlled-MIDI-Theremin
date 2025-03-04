from hand_tracking import HandTracker
from generate_midi import GenerateMidi

def main():
    tracker = HandTracker()
    midi = GenerateMidi()

    try:
        while True:
            tracker.recognize_gesture()
            midi.play_midi()
            
    except KeyboardInterrupt:
        print("Exiting...")
        tracker.release()
        midi.close()

if __name__ == "__main__":
    main()
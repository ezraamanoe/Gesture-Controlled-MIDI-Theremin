import time
import rtmidi

class GenerateMidi:
    def __init__(self):
        self.midiout = rtmidi.MidiOut()
        self.available_ports = self.midiout.get_ports()
        
        if self.available_ports:
            print("Available MIDI ports:")
            for i, port in enumerate(self.available_ports):
                print(f"{i}: {port}")
            
            # Open the first available port
            self.midiout.open_port(0)
            print(f"Connected to MIDI port: {self.available_ports[0]}")
        else:
            print("No MIDI ports found. Creating a virtual MIDI port.")
            self.midiout.open_virtual_port("Virtual MIDI")
            print("Virtual MIDI port created.")

    def send_midi_message(self, channel, cc, value):
        """Send a MIDI control change message."""
        try:
            self.midiout.send_message([0xB0 + channel, cc, value])
            print(f"Sent MIDI: Channel {channel}, CC {cc}, Value {value}")
        except Exception as e:
            print(f"MIDI Error: {e}")

# Example usage for MIDI Learn
if __name__ == "__main__":
    midi = GenerateMidi()
    midi.send_midi_message(1, 20, 64)  # Send CC 20 with value 64
    time.sleep(1)  # Keep the script running for a moment
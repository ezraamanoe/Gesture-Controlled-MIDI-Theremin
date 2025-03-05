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

        self.active_effect = None  # Track the currently active effect

    def send_midi_message(self, channel, cc, value):
        """Send a MIDI control change message."""
        try:
            self.midiout.send_message([0xB0 + channel, cc, value]) # Offset channel by 0xB0
            print(f"Sent MIDI: Channel {channel}, CC {cc}, Value {value}")
        except Exception as e:
            print(f"MIDI Error: {e}")

    def set_semitones(self, semitones):
        """Set the semitones value in Logic Pro's Pitch Shifter."""
        cc_value = int((semitones + 12) * (127 / 24))  # Map -12 to +12 semitones to 0-127
        self.send_midi_message(1, 20, cc_value)  # Use CC 20

    def start_effect(self, effect_name):

        effect_map = {
            "Major Third": 4,
            "Major Fifth": 7,
            "Minor Third": 3,
            "Tritone": 6,
            "Octave": 12,
            "Stop": 0
        }

        if effect_name in effect_map:
            self.active_effect = effect_name
            self.set_semitones(effect_map[effect_name])
import time
import rtmidi
import threading

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

        # Threading and state management
        self.effect_lock = threading.Lock()
        self.active_effect = None  # Track the currently active effect
        self.effect_event = threading.Event()  # Signal to stop effects
        self.effect_thread = None  # Thread for the active effect

    def send_midi_message(self, channel, cc, value):
        """Send a MIDI control change message."""
        try:
            self.midiout.send_message([0xB0 + channel, cc, value])
            print(f"Sent MIDI: Channel {channel}, CC {cc}, Value {value}")
        except Exception as e:
            print(f"MIDI Error: {e}")

    def set_semitones(self, semitones):
        """Set the semitones value in Logic Pro's Pitch Shifter."""
        # Map semitones to MIDI CC value (0-127)
        # Logic Pro's Pitch Shifter typically uses a range of -24 to +24 semitones
        cc_value = int((semitones + 12) * (127 / 24))  # Map -24 to +24 semitones to 0-127
        cc_value = max(0, min(127, cc_value))  # Clamp to valid MIDI range
        self.send_midi_message(1, 20, cc_value)  # Use CC 20 (or the one you mapped)

    def stop_current_effect(self):
        """Stop the currently running effect and reset it to zero."""
        with self.effect_lock:
            if self.active_effect:
                print(f"Stopping current effect: {self.active_effect}")
                self.effect_event.set()  # Signal the effect thread to stop
                if self.effect_thread and self.effect_thread.is_alive():
                    self.effect_thread.join(timeout=0.1)  # Wait briefly for the thread to finish
                self.effect_thread = None
                self.active_effect = None
                self.effect_event.clear()  # Reset the event for future use

    def start_effect(self, effect_name):
        """Start a new effect, stopping the current one if necessary."""
        self.stop_current_effect()  # Stop any running effect

        if effect_name == "Third":
            self.active_effect = "Third"
            self.set_semitones(4)  # Set pitch shift to +4 semitones (major third)
        elif effect_name == "Fifth":
            self.active_effect = "Fifth"
            self.set_semitones(7)  # Set pitch shift to +7 semitones (major fifth)
        elif effect_name == "Tritone":
            self.active_effect = "Tritone"
            self.set_semitones(6)  # Set pitch shift to +6 semitones (tritone)
        elif effect_name == "Octave":
            self.active_effect = "Octave"
            self.set_semitones(12) # Set pitch shift to +12 semitones (octave)
        elif effect_name == "reset_pitch":
            self.set_semitones(0)  # Reset pitch shift to 0 semitones
            return
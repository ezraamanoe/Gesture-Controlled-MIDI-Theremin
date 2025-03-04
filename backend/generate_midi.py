import time
import rtmidi
import threading

class GenerateMidi:
    def __init__(self):
        self.midiout = rtmidi.MidiOut()
        self.available_ports = self.midiout.get_ports()
        
        if self.available_ports:
            self.midiout.open_port(0)
        else:
            self.midiout.open_virtual_port("Virtual MIDI")
        
        # Threading and state management for all effects
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

    def reset_effect(self, cc):
        """Reset a specific effect to zero."""
        self.send_midi_message(1, cc, 0)

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

    def reverb(self):
        """Gradually increase reverb effect."""
        try:
            for i in range(1, 127, 5):
                if self.effect_event.is_set():  # Check if the event is set to stop
                    print("Reverb stopped by event.")
                    break
                self.send_midi_message(1, 91, i)
                print(f"Reverb: {i}")
                time.sleep(0.1)  # Reduced sleep time for faster response
        finally:
            self.reset_effect(91)  # Reset reverb to zero
            print("Reverb reset to 0.")

    def volume(self):
        """Gradually increase volume effect."""
        try:
            for i in range(1, 127, 5):
                if self.effect_event.is_set():  # Check if the event is set to stop
                    print("Volume stopped by event.")
                    break
                self.send_midi_message(1, 7, i)
                print(f"Volume: {i}")
                time.sleep(0.1)  # Reduced sleep time for faster response
        finally:
            self.reset_effect(7)  # Reset volume to zero
            print("Volume reset to 0.")

    def delay(self):
        """Gradually increase delay effect."""
        try:
            for i in range(1, 127, 5):
                if self.effect_event.is_set():  # Check if the event is set to stop
                    print("Delay stopped by event.")
                    break
                self.send_midi_message(1, 95, i)
                print(f"Delay: {i}")
                time.sleep(0.1)  # Reduced sleep time for faster response
        finally:
            self.reset_effect(95)  # Reset delay to zero
            print("Delay reset to 0.")

    def start_effect(self, effect_name):
        """Start a new effect, stopping the current one if necessary."""
        self.stop_current_effect()  # Stop any running effect

        if effect_name == "reverb":
            self.active_effect = "reverb"
            self.effect_thread = threading.Thread(target=self.reverb)
        elif effect_name == "volume":
            self.active_effect = "volume"
            self.effect_thread = threading.Thread(target=self.volume)
        elif effect_name == "delay":
            self.active_effect = "delay"
            self.effect_thread = threading.Thread(target=self.delay)
        elif effect_name == "stop_reverb":
            self.reset_effect(91)  # Reset reverb to zero
            return

        if self.effect_thread:
            self.effect_thread.start()
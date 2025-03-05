# Gesture-Controlled-MIDI-Theremin

<html>
  <p>
This project is a real-time gesture-controlled MIDI system designed to emulate the behavior of a theremin using computer vision and MIDI control messages. The system utilizes a webcam to track hand movements and interpret them as musical notes and pitch shifts. It sends MIDI messages to control Logic Pro's pitch shifter plugin and VSTs in a DAW (Digital Audio Workstation), allowing for expressive, touchless music performance. The system uses MediaPipe Hands, a machine learning-based hand tracking solution, to detect and interpret hand gestures from a live video feed (OpenCV). These gestures are mapped to MIDI Control Change (CC) messages using rtmidi. Inspired by the theremin, <i>@julip.mp3</i>, and <i>Imogen Heap</i>.
  </p>

  <img src="https://i0.wp.com/www.nationalreview.com/wp-content/uploads/2024/05/leon-theremin.jpg?w=1054&ssl=1">
</html>

## Features
<html>
  <dl>
    <dt>Gesture Detection:</dt>
    <dd>- Utilizes MediaPipe Hands for real-time hand tracking and gesture recognition.</dd>
    <dd>- Detects 21 hand landmarks per hand, enabling precise tracking of finger positions and gestures.</dd>
    <dd>- Classifies gestures based on the state of extended fingers.</dd>
    <dt>MIDI Communication:</dt>
    <dd>- Implements rtmidi, a cross-platform MIDI library, to send MIDI CC messages to a DAW.</dd>
    <dd>- Maps detected gestures to specific MIDI CC values, which control the semitone shift parameter in the Pitch Shifter plugin.</dd>
    <dt>Real-time Video Processing:</dt>
    <dd>- Uses OpenCV to capture and process live video from a webcam.</dd>
    <dd>- Displays hand landmarks, gesture labels, and a bounding box around the detected hand for visual feedback.</dd>
    <dt>Pitch Shifting Logic:</dt>
    <dd>- Converts gesture-based inputs into semitone values (e.g., -12 to +12 semitones).</dd>
    <dd>- Maps semitone values to MIDI CC values using a linear scaling formula.</dd>
  </dl>
</html>

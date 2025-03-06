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
    <dd>- Utilizes MediaPipe Hands for real-time hand tracking and gesture recognition.
      <br />
    - Detects 21 hand landmarks per hand, enabling precise tracking of finger positions and gestures.
      <br />
    - Classifies gestures based on the state of extended fingers.</dd>
    <dt>MIDI Communication:</dt>
    <dd>
      - Implements rtmidi, a cross-platform MIDI library, to send MIDI CC messages to a DAW.
    <br />
      - Maps detected gestures to specific MIDI CC values, which control the semitone shift parameter in the Pitch Shifter plugin.
    </dd>
    <dt>Real-time Video Processing:</dt>
    <dd>
      - Uses OpenCV to capture and process live video from a webcam.
      <br />
    - Displays hand landmarks, gesture labels, and a bounding box around the detected hand for visual feedback.</dd>
    <dt>Pitch Shifting Logic:</dt>
    <dd>- Converts gesture-based inputs into semitone values (e.g., -12 to +12 semitones).
      <br />
    - Maps semitone values to MIDI CC values using a linear scaling formula.</dd>
  </dl>

## Gestures and Mappings
|Gestures|Interval|MIDI Effect|
|---|---|---|
|Fist|Stop|0 semitones (Reset)|
|Thumb|Major 2nd|+2 semitones|
|Thumb and Index|Minor 3rd|+3 semitones|
|Thumb, Index, and Middle|Major 3rd|+4 semitones|
|Thumb, Index, Middle, Ring|Perfect 4th|+5 semitones|
|Index and Pinky|Tritone|+6 semitones|
|Open Palm|Perfect 5th|+7 semitones|
|Index|Major 6th|+9 semitones|
|Index and Middle|Major 7th|+11 semitones|
|Index, Middle, and Ring|Octave|+12 semitones|

|Gesture|Action|
|---|---|
|Thumb and Pinky|Play Middle C|
|Thumb, Index, and Pinky|Stop playing Middle C|




## Run the app
<dl>
  <dt>Prerequisites:</dt>
    <dd>
      - <a href="https://www.python.org">Python 3.9+</a>
      <br />
      - MediaPipe Hands
      <br />
      - OpenCV
      <br />
      - rtmidi
    </dd>
</dl>
</html>

Clone the git repository by running:
```
$ git clone https://github.com/ezraamanoe/Gesture-Controlled-MIDI-Theremin.git
$ cd Gesture-Controlled-MIDI-Theremin
```

Set up a virtual environment and install the requirements:
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
#### Setting up virtual ports in MacOS

For MacOS, open Audio MIDI Setup > Window > Show MIDI Studio.
<br/>
<br/>
Double click on IAC Driver and select 'Device is online'.
<br/>
<br/>
Add ports as needed using the + button.
<br />
<br />

Run the app by running:
```
$ python3 hand_tracking.py
```

#### Setting up in Logic Pro, after running hand_tracking.py
Open Logic Pro > Settings > MIDI > Input.
<br />
<br />
Make sure your IAC Driver bus(es) are selected.
<br />
<br />
Create a software instrument track, load a VST and Pitch Shifter. In the demo attached below, I used the Tape Orchestra Synth by Spitfire LABS.
<br />
<br/>
Open the Pitch Shifter plugin click on the *semitones* parameter and press 
<kbd>cmd</kbd> + <kbd>L</kbd> to open learn mode.
<br />
<br/>
Make *gestures* with your left hand and Logic Pro should automatically learn the MIDI CC messages.

https://github.com/user-attachments/assets/c57af271-6a51-46af-ba1f-fce7b056275d


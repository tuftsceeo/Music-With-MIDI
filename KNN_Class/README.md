# 🎼 KNN Sensor-to-MIDI Classifier with Musical Staff Visualization

This PyScript web app allows users to **train a K-Nearest Neighbor (KNN) classifier** using physical sensor inputs (e.g. LEGO sensors), classify new input in real time, and **visualize the output as musical notes** on a digital staff. The predicted notes are also **played via MIDI**, turning physical interactions into interactive musical expression.

---

## 📌 Project Goals

- Teach core concepts of **machine learning** through music and hands-on coding.
- Engage students in **sensor-based instrument design** using real data.
- Connect **engineering and music education** through visualization and MIDI output.
- Provide a browser-native, no-install environment using **PyScript and Web Channels**.

---

## ⚙️ Features

### 🎹 KNN-Based MIDI Classifier

- Collect and train on sensor input using a KNN algorithm.
- Classify unknown input and return the most likely MIDI note.
- Tuneable number of neighbors (`k=3` by default).

### 🎵 Real-Time Visualization

- Convert MIDI values to musical note names (e.g. C4, G#5).
- Dynamically choose **bass** or **treble** staff based on note pitch.
- Plot notes on virtual staves for visual musical feedback.
- Display current prediction in a live status area.

### 📡 Channel Communication

- Listens for training and classification data from `/jerahwright/on` and `/jerahwright/newon`.
- Posts classified note data back to `/jerahwright/play` for MIDI playback.

### 📋 Data Table Display

- Every training or classification event is recorded in an HTML table.
- Displays pitch, sensor readings, instrument, and chosen staff.

### 🗑️ Data Management

- "Clear Data" button resets all training examples, visual notes, and prediction state.

---

## 🧠 How It Works

1. **Training Mode**
    - Sensor values (`sensor_reading1` and `sensor_reading2`) are sent with a known MIDI note.
    - The note is stored as a labeled training sample.

2. **Prediction Mode**
    - New sensor input is classified using the KNN algorithm.
    - The most probable note is selected and visualized.
    - MIDI output is sent via channel for playback.

3. **Visualization**
    - Notes are plotted on either a bass or treble staff depending on their pitch.
    - Each classified note appears as a new graphical dot.

---

## 🧪 Tech Stack

- **PyScript**: Python-in-the-browser execution environment.
- **Channel API (CEEO_Channel)**: Enables two-way communication between web pages and remote sensors.
- **JavaScript DOM Access via PyScript**: Used to control visual elements and real-time feedback.
- **Custom CSS for Staves and Notes**: Stylized musical note rendering.

---

## 📂 File Structure Overview

- `main.py`: Core classifier logic, visualization, and channel communication.
- `#knn-body`: Table element for displaying recorded training data.
- `#note-plot-treble` and `#note-plot-bass`: Containers for note visualization.
- `#clearData`: Button for clearing training data and visuals.
- `#live-prediction`: Displays most recent predicted note.

---

## 🚀 Usage

1. Load the web page (requires PyScript-enabled browser).
2. Begin sending sensor values using a companion page or sensor device connected to `/jerahwright/on`.
3. Train the model by sending known MIDI notes with sensor readings.
4. Send new (unlabeled) sensor values to `/jerahwright/newon` to receive real-time classification.
5. View the prediction on the virtual staff and hear the output via MIDI.

---

## 📖 Example Output

🎓 Learned: 450, 290 → G4
🤖 Predicted: 455, 288 → G4
✅ Channel connected: /jerahwright/on


---

## 🧹 Resetting

Click the **"Clear Data"** button to reset all:
- Stored KNN examples
- Plotted notes
- Display tables and prediction areas

---

## 💡 Educational Use Cases

- STEM + Music integrated curriculum
- Exploratory machine learning projects for beginners
- Tactile learning for sensor data interpretation
- Interactive digital instrument workshops

---

## 📜 License & Attribution

Created by @jcw372 using [PyScript](https://pyscript.net/) and CEEO channel tools.  
Developed for educational and research purposes at Tufts University.

---

Let students explore **code as music** and **music as logic**.  
🎧 Feel the sound of sensor data — live in your browser!

# 🎼 Sensor-to-MIDI Trainer with PyScript

This interactive PyScript app enables students and educators to **collect sensor input**, **train a classifier**, and **map physical data to MIDI notes** — all in the browser using Python. It leverages **channel communication**, **file I/O**, and **real-time sliders** to configure instruments and train the system to respond musically to sensor input.

---

## 📌 Project Goals

- Introduce students to **coding through music** by leveraging MIDI synthesis.
- Use **real-world sensor data** to create interactive digital instruments.
- Promote **algorithmic thinking** by letting users train their own K-Nearest Neighbor (KNN) models.
- Bridge **engineering concepts and musical creativity** using browser-native tools.

---

## 🧩 Features

### ✅ Core Functionalities

- **Sensor Data Collection**  
  Receives live sensor input (via CEEO channel) and displays it on the page.
  
- **MIDI Note Configuration**  
  Users can configure:
  - MIDI note pitch

- **Instrument Training**  
  Pressing **Train** captures the current sensor readings and associates them with the selected MIDI note and instrument.

- **Training Completion**  
  Pressing **Stop Training** signals the system to stop collecting data and store the session results.

- **UI Controls**  
  Dynamic controls for:
  - Adding/removing second sensor input
  - Adjusting note parameters via sliders
  - Displaying connection and training status

---

## 🧠 Technologies Used

- **PyScript**: Python-in-the-browser execution
- **Pyodide**: Brings Python to WebAssembly
- **MIDI**: Musical Instrument Digital Interface output
- **CEEO Channel**: Used for messaging and data transfer between pages
- **LEGO Hub or Compatible Sensor Inputs**
- **File Handling via PyScript.js `files` module**

---

## 🔧 How It Works

1. **Start the App**  
   Open the page in a browser with PyScript support. The app will connect to a channel named `/jerahwright/on`.

2. **Configure MIDI Note Settings**  
   Use slider to adjust:
   - `NoteRange` → MIDI pitch  

3. **Collect Sensor Data**  
   Activate one or two sensors (configurable via the "+" button). Sensor data will update live.

4. **Train Your Instrument**  
   Click **Train** to store the current sensor values along with the selected note/instrument into the KNN model.

5. **End the Training Session**  
   Click **Stop Training** to signal the model to finalize and save training data.


---

## 📂 File Structure (UI Elements)


- `#NoteRange`: Slider to control MIDI note parameters  
- `#train`, `#stopTrain`: Training control buttons  
- `#status`: Dynamic status message box  
- `#plus`, `#minus`: Show/hide additional sensor input rows

---

## 🚨 Requirements

- A browser that supports **PyScript (2025.7.3 or later)**
- A connected sensor environment using the **LEGO Hub** or other **hub.py-compatible inputs**
- MIDI-compatible output configured via browser or device

---

## 🧪 Educational Applications

- Coding + music workshops  
- STEAM curriculum development  
- Demonstrations of machine learning with physical interfaces  
- Hands-on exploration of data-driven instrument design

---

## 📃 License & Attribution

Created by @jcw372  
Channels hosted via CEEO at Tufts University  
Open-source and educational use encouraged — please credit where appropriate.

---

🎧 Ready to turn your movements into music? Train your custom instrument now!

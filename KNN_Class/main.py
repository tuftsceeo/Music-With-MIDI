from pyscript import document
import asyncio
import channel

from datetime import datetime
import json
from pyscript import window, when
import struct
import plot
from hub import hubs
from pyscript.web import page
from pyscript.js_modules import files

note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

knn_training_data = []  # list of tuples: (sensor1, sensor2)
knn_labels = []         # corresponding MIDI values

def add_knn_training_point(sensor_reading1, sensor_reading2, midi_val):
    knn_training_data.append([sensor_reading1, sensor_reading2])
    knn_labels.append(midi_val)

def classify_knn_point(sensor_reading1, sensor_reading2, k=3):
    if not knn_training_data:
        return None

    input_point = [sensor_reading1, sensor_reading2]
    distances = []

    for i, point in enumerate(knn_training_data):
        dist = sum((a - b) ** 2 for a, b in zip(point, input_point)) ** 0.5
        distances.append((dist, knn_labels[i]))

    distances.sort(key=lambda x: x[0])
    top_k = distances[:k]

    votes = {}
    for _, midi_val in top_k:
        votes[midi_val] = votes.get(midi_val, 0) + 1

    max_votes = max(votes.values())
    candidates = [m for m in votes if votes[m] == max_votes]

    if len(candidates) == 1:
        return candidates[0]
    else:
        avg_dists = {m: sum(d for d, mv in top_k if mv == m) / votes[m] for m in candidates}
        return min(avg_dists, key=avg_dists.get)

def midi_to_note(midi_value):
    note = note_names[midi_value % 12]
    octave = (midi_value // 12) - 1
    return f"{note}{octave}"

treble_positions = {
    "C4": 70, "D4": 65, "E4": 60, "F4": 55, "G4": 50,
    "A4": 45, "B4": 40, "C5": 35, "D5": 30, "E5": 25,
    "F5": 20, "G5": 15, "A5": 10, "B5": 5, "C6": 0
}

bass_positions = {
    "E2": 75, "F2": 70, "G2": 65, "A2": 60, "B2": 55,
    "C3": 50, "D3": 45, "E3": 40, "F3": 35, "G3": 30,
    "A3": 25, "B3": 20, "C4": 15, "D4": 10, "E4": 5
}

def choose_staff(pitch):
    try:
        octave = int(pitch[-1])
        return "bass" if octave < 4 else "treble"
    except:
        return "treble"

def add_knn_row(pitch, sensor_reading1, sensor_reading2, staff, instrument):
    table = document.querySelector("#knn-body")
    row = document.createElement("tr")
    row.innerHTML = f"""
        <td>{pitch}</td>
        <td>{sensor_reading1}</td>
        <td>{sensor_reading2}</td>
        <td>{instrument}</td>
        <td>{staff}</td>
    """
    table.appendChild(row)

def plot_note(pitch, staff):
    positions = treble_positions if staff == "treble" else bass_positions
    print(positions)
    y = positions.get(pitch, 40)

    plot_id = f"note-plot-{staff}"
    plot = document.querySelector(f"#{plot_id}")

    if plot:
        note = document.createElement("div")
        note.classList.add("note", "note-new")
        note.style.top = f"{y}px"
        note.style.left = f"{20 + 30 * len(list(plot.children))}px"
        note.title = f"Note: {pitch}"
        plot.appendChild(note)

def show_live_prediction(pitch):
    status_div = document.querySelector("#live-prediction")
    if status_div:
        status_div.innerHTML = f"🎵 Predicted Note: <strong>{pitch}</strong>"
        status_div.className = "status predicted"

def update_channel_status(connected=True, message=""):
    status_div = document.querySelector("#all_things_channels")
    if connected:
        status_div.innerHTML = f'''
            <span class="status-indicator status-connected"></span>
            ✅ Channel connected: /jerahwright/on {message}
        '''
    else:
        status_div.innerHTML = f'''
            <span class="status-indicator status-disconnected"></span>
            ❌ Channel disconnected - {message}
        '''

async def fred(message):
    update_channel_status(True, "- Receiving data")
    
    try:
        output_data ={}
        topic, value = myChannel.check('/jerahwright', message)

        if topic and topic.startswith('/jerahwright/newon'):
            sensor_reading1 = int(value["sensor_reading1"])
            sensor_reading2 = int(value["sensor_reading2"])
            predicted_midi = classify_knn_point(sensor_reading1, sensor_reading2, k=3)
            
            if predicted_midi is not None:
                midi_val = predicted_midi
                pitch = midi_to_note(midi_val)
                instrument = 0

                staff = choose_staff(pitch)
    
            output_data = {
                "midi_val" : predicted_midi,
                'instrument': instrument,
                'length': 1000,
                'volume': 127,
                'pitch': pitch,
                'staff': staff,
                'Sensor 1': sensor_reading1,
                'Sensor 2': sensor_reading2
            }
            print("Output",output_data)
            await myChannel.post('/jerahwright/play', output_data)
                
        if topic and topic.startswith('/jerahwright/on'):
            midi_val = int(value.get("midi_val", -1))
            sensor_reading1 = int(value["sensor_reading1"])
            sensor_reading2 = int(value["sensor_reading2"])
            instrument = int(value["instrument"])

            if midi_val >= 0:
                add_knn_training_point(sensor_reading1, sensor_reading2, midi_val)
                pitch = midi_to_note(midi_val)
                print(f"🎓 Learned: {sensor_reading1}, {sensor_reading2} → {pitch}")
            else:
                predicted_midi = classify_knn_point(sensor_reading1, sensor_reading2, k=3)
                if predicted_midi is not None:
                    midi_val = predicted_midi
                    pitch = midi_to_note(midi_val)
                    print(f"🤖 Predicted: {sensor_reading1}, {sensor_reading2} → {pitch}")
                    show_live_prediction(pitch)
                else:
                    print("⚠️ No training data")
                    return

            staff = choose_staff(pitch)
            add_knn_row(pitch, sensor_reading1, sensor_reading2, instrument, staff)
            plot_note(pitch, staff)

            output_data = {
                'instrument': instrument,
                'length': 1000,
                'volume': 127,
                'pitch': pitch,
                'staff': staff,
                'Sensor 1': sensor_reading1,
                'Sensor 2': sensor_reading2
            }
            await myChannel.post('/jerahwright/play', output_data)

    except Exception as e:
        print("❌ Error in fred:", e)
        update_channel_status(False, f"Error: {e}")

myChannel = channel.CEEO_Channel(
    "hackathon", "@chrisrogers", "talking-on-a-channel",
    divName='all_things_channels', suffix='_test'
)

print('📡 Channel reply status:', myChannel.reply)

myChannel.callback = fred

@when("click", "#clearData")
def clear_training_data(event):
    global knn_training_data, knn_labels
    knn_training_data.clear()
    knn_labels.clear()
    print("🗑️ Training data cleared.")

    table = document.querySelector("#knn-body")
    if table:
        table.innerHTML = ""

    for staff_id in ["note-plot-treble", "note-plot-bass"]:
        plot = document.querySelector(f"#{staff_id}")
        if plot:
            while plot.firstChild:
                plot.removeChild(plot.firstChild)

    status_div = document.querySelector("#status")
    if status_div:
        status_div.textContent = "Training data cleared."
        status_div.className = "status cleared"

    live_div = document.querySelector("#live-prediction")
    if live_div:
        live_div.innerHTML = ""
        live_div.className = "status"

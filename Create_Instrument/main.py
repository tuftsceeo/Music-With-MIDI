from pyscript import document
import asyncio
import channel
from datetime import datetime
import json
from pyscript import document, window, when
import struct
import plot
from hub import hubs
from pyscript.web import page
from pyscript.js_modules import files



myChannel = channel.CEEO_Channel(
    "hackathon", "@chrisrogers", "talking-on-a-channel",
    divName='all_things_channels', suffix='_test'
)

'''# Map MIDI to note name
note_names = ["C", "C#", "D", "D#", "E", "F",
              "F#", "G", "G#", "A", "A#", "B"]

def midi_to_note(midi_value):
    note = note_names[midi_value % 12]
    octave = (midi_value // 12) - 1
    return f"{note}{octave}"

# Map note name to Y position on staff
staff_positions = {
    # Bass clef
    "E2": 250, "F2": 245, "G2": 240, "A2": 235, "B2": 230,
    "C3": 225, "D3": 220, "E3": 215, "F3": 210, "G3": 205,
    "A3": 200, "B3": 195,

    # Treble clef
    "C4": 150, "D4": 145, "E4": 140, "F4": 135, "G4": 130,
    "A4": 125, "B4": 120, "C5": 115, "D5": 110, "E5": 105,
    "F5": 100, "G5": 95, "A5": 90, "B5": 85, "C6": 80
}

def choose_staff(pitch_name):
    try:
        octave = int(pitch_name[-1])
        return "bass" if octave < 4 else "treble"
    except:
        return "treble"

def add_knn_row(pitch, time, staff):
    table = document.querySelector("#knn-body")
    row = document.createElement("tr")
    row.innerHTML = f"<td>{pitch}</td><td>{time}</td><td>{staff}</td>"
    table.appendChild(row)

def plot_note(pitch, staff):
    y = staff_positions.get(pitch, 150)
    plot = document.querySelector("#note-plot")
    note = document.createElement("div")
    note.classList.add("note")
    note.style.top = f"{y}px"
    note.style.left = f"{10 + 20 * len(plot.children)}px"
    plot.appendChild(note)


async def fred(message):
    try:
        topic, value = myChannel.check('/jerahwright',message)
        if topic:
            if topic.startswith('/jerahwright/on'):
                midi_value = data.get("midi", 62)
                time_val = value[1]
                print(midi_val, time_val)
                pitch = midi_to_note(midi_val)
                staff = choose_staff(pitch)

                add_knn_row(pitch, time_val, staff)
                plot_note(pitch, staff)
                print(value)
                #await playsound(value)
                #await asyncio.sleep(1)   
            if topic.startswith('/midi/off'):
                midi.stopNote(value)
                
    except Exception as e:
        print('Error in MIDI: ',e)

print('reply = ',myChannel.reply)
myChannel.callback = fred


# Handle incoming messages from the channel
async def handle_input(data):
    midi_val = data.get("midi", 62)  # default to C4
    time_val = data.get("time", "00:00")

    pitch = midi_to_note(midi_val)
    staff = choose_staff(pitch)

    add_knn_row(pitch, time_val, staff)
    plot_note(pitch, staff)

# ✅ Start watching the channel and await properly
await myChannel.watch(handle_input)
async def send_test_note():
    """Send a test note to the channel"""
    try:
        test_data = {
            "midi": 64,  # E4
            "time": datetime.now().strftime("%H:%M:%S")
        }
        
        # Send to /jerahwright channel
        await myChannel.post("/jerahwright", test_data)
        print(f"Sent test note to /jerahwright: {test_data}")
        
    except Exception as e:
        print(f"Error sending test note: {e}")
'''
'''
def clear_staff():
    """Clear all notes from the staff and table"""
    # Clear visual notes
    notes = document.querySelectorAll(".note")
    for note in notes:
        note.remove()
    
    # Clear table
    tbody = document.querySelector("#knn-body")
    tbody.innerHTML = ""
    
    print("Cleared staff and table")
'''

# Update status
try:
    status_div = document.querySelector("#status")
    status_div.textContent = "Connected to CEEO channel - Listening for /jerahwright data"
    status_div.className = "status connected"
    print("KNN Music Staff initialized and listening for /jerahwright/on data")
except Exception as e:
    print(f"Error updating status: {e}")


fileName1 = document.getElementById('fileRead_collect')
files1 = files.newFile()
python_area1 = document.getElementById('PC_code_collect')

# Output file input
fileName2 = document.getElementById('fileRead_output')
files2 = files.newFile()
python_area2 = document.getElementById('PC_code_output')

# Handle reading collect file
@when("change", "#fileRead_collect")
async def on_local_read_collect(event): 
    fred1 = await files1.read('fileRead_collect')
    if fred1 and isinstance(fred1, str):
        python_area1.code = fred1
    else:
        window.console.error("Invalid file content for collect")

# Handle saving collect file
@when("click", "#local_collect")
async def on_save_collect(event): 
    filename = fileName1.value
    name = filename.split('\\')[-1] if filename else 'collect_code.py'
    await files1.save(python_area1.code, name)

# Handle reading output file
@when("change", "#fileRead_output")
async def on_local_read_output(event): 
    fred2 = await files2.read('fileRead_output')
    if fred2 and isinstance(fred2, str):
        python_area2.code = fred2
    else:
        window.console.error("Invalid file content for output")

# Handle saving output file
@when("click", "#local_output")
async def on_save_output(event): 
    filename = fileName2.value
    name = filename.split('\\')[-1] if filename else 'output_code.py'
    await files2.save(python_area2.code, name)

@when("click", "#plus")
def show_sensor2_row(event):
    row = document.getElementById("sensor2_row")
    row.style.display = "table-row"
    button = document.getElementById("plus")
    button.style.display = "none"
    label_cell = document.getElementById("value2_label_cell")
    data_cell = document.getElementById("value2_data_cell")

    if label_cell and data_cell:
        label_cell.style.display = "table-cell"
        data_cell.style.display = "table-cell"
@when("click", "#minus")
def hide_sensor2_row(event):
    row2 = document.getElementById("sensor2_row")
    row2.style.display = "none"
    button = document.getElementById("plus")
    button.style.display = "table-cell"
    label_cell3 = document.getElementById("value2_label_cell")
    if label_cell3:
        label_cell3.style.display = "none"
    label_cell4 = document.getElementById("value3_label_cell")
    if label_cell4:
        label_cell4.style

# Sensor objects (no plot passed)
...

# Sensor objects (no plot passed)
w = hubs(1)
x = hubs(2)

# 👇 Define the callback function before assigning it
async def main(message):
    try:
        payload = json.loads(message['payload'])
        topic = payload.get('topic', '')
        value = payload.get('value', {})
        window.console.log(f"Sensor data received: topic={topic}, value={value}")
    except Exception as e:
        window.console.error(f"Sensor handler error: {e}")

# 👇 Now it's safe to assign
myChannel.callback = main

@when("change", "#fileRead")
async def on_local_read(event): 
    path = fileName.value
    window.console.log(path)
    fred = await files.read('fileRead')
    window.console.log(fred)
    python_area.code = fred

@when("click", "#local")
async def on_save(event): 
    filename = fileName.value
    name = filename.split('\\')[-1] if filename else 'test.py'
    await files.save(python_area.code, name)

midi_note = 62
note_length = 50
note_volume = 50

@when ("input", "#NoteRange")
def handle_slider1(event):
    global midi_note
    slider = page.find("#NoteRange")[0]
    label = page.find("#NoteRangeLabel")[0]
    label.innerHTML = slider.value
    midi_note = int(slider.value)
@when ("input", "#NoteLength")
def handle_slider2(event):
    global note_length
    slider = page.find("#NoteLength")[0]
    label = page.find("#NoteLengthLabel")[0]
    label.innerHTML = slider.value
    note_length = int(slider.value)
@when ("input", "#NoteVolume")
def handle_slider3(event):
    global note_volume
    slider = page.find("#NoteVolume")[0]
    label = page.find("#NoteVolumeLabel")[0]
    label.innerHTML = slider.value
    note_volume = int(slider.value)

@when("change", "#fileRead")
async def on_local_read(event): 
    path = fileName.value
    window.console.log(path)
    fred = await files.read('fileRead')
    window.console.log(fred)
    python_area.code = fred

@when("click", "#local")
async def on_save(event): 
    filename = fileName.value
    name = filename.split('\\')[-1] if filename else 'test.py'
    await files.save(python_area.code, name)

@when("click", "#train")
def handle_train(event):
    slider = page.find("#NoteRange")[0]
    midi = int(slider.value)
    # get the instrument
    instrument = int(page.find("#instrument")[0].value)
    sensor_reading = int(page.find("#value1")[0].innerHTML)
    sensor_reading1 = int(page.find("#value2")[0].innerHTML)
    #set the note length
    slider = page.find("#NoteLength")[0]
    length = int(slider.value)
    #set the note volume
    slider = page.find("#NoteVolume")[0]
    volume = int(slider.value)
    # send it to Jake. ;-)
    data = {
        "midi_val": midi ,
        #"length": length,
        #"volume": volume,
        "instrument": instrument,  
        "sensor_reading1": sensor_reading,
        "sensor_reading2": sensor_reading1
    }
    if myChannel.is_connected:
        await myChannel.post('/jerahwright/on',data)
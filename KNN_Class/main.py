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
import channel
import asyncio

# MIDI to Note conversion
note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def midi_to_note(midi_value):
    note = note_names[midi_value % 12]
    octave = (midi_value // 12) - 1
    return f"{note}{octave}"

# Staff positioning for realistic placement
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

def add_knn_row(pitch, sensor1_val, sensor2_val, instrument, staff):
    table = document.querySelector("#knn-body")
    row = document.createElement("tr")
    row.innerHTML = f"""
        <td>{pitch}</td>
        <td>{sensor1_val}</td>
        <td>{sensor2_val}</td>
        <td>{instrument}</td>
        <td>{staff}</td>
    """
    table.appendChild(row)

def plot_note(pitch, staff):
    positions = treble_positions if staff == "treble" else bass_positions
    y = positions.get(pitch, 40)
    
    plot_id = f"note-plot-{staff}"
    plot = document.querySelector(f"#{plot_id}")
    
    if plot:
        note = document.createElement("div")
        note.classList.add("note", "note-new")
        note.style.top = f"{y}px"
        print(list(plot.children))
        note.style.left = f"{20 + 30 * len(list(plot.children))}px"
        note.title = f"Note: {pitch}"
        plot.appendChild(note)

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

# YOUR EXACT fred() FUNCTION
async def fred(message):
    print("📨 Message received:", message)
    update_channel_status(True, "- Receiving data")
    
    try:
        topic, value = myChannel.check('/jerahwright', message)
        if topic:
            print("✅ Valid topic:", topic)
            
            if topic.startswith('/jerahwright/on'):
                print("I got data")
                # Fix the variable name from your code (data -> value)
                midi_val = int(value["midi_val"])#.get("midi", 62)  # Fixed: was data.get("midi", 62)
                sensor1_val = int(value['sensor_reading1'])
                sensor2_val = int(value['sensor_reading2'])
                instrument = int(value['instrument'])
                '''data = {
                "midi_val": midi ,
                "length": length,
                "volume": volume,
                "instrument": instrument,  
                "sensor_reading1": sensor_reading,
                "sensor_reading2": sensor_reading1
            }'''
                print("🎵 MIDI Info:", type(midi_val), type(sensor1_val), type(sensor2_val), type(instrument))
                
                pitch = midi_to_note(midi_val)
                staff = choose_staff(pitch)

                add_knn_row(pitch, sensor1_val, sensor2_val, staff, instrument)
                plot_note(pitch, staff)
                print("📊 Processed value:", value)
                # Send to the MIDI player on /jerahwright/play


            
            #if topic.startswith('/midi/off'):
            #    print("🔇 Stopping MIDI note:", value)
            #    # midi.stopNote(value)  # Uncomment if you have midi module
                output_data = {
                    'midi_val': midi_val,
                    'instrument': instrument,
                    'length': 1000,  # 1 second duration
                    'volume': 127,   # Max volume
                    'pitch': pitch,  # Note name for reference
                    'staff': staff   # Treble or bass
                }
                window.console.log(output_data)
                print("🎼 Sending to MIDI player:", output_data)
                await myChannel.post('/jerahwright/play', output_data) 
                
    except Exception as e:
        print('❌ Error in MIDI handler:', e)
        update_channel_status(False, f"Error: {e}")
    except Exception as e:
        print('❌ Error in MIDI handler:', e)
        update_channel_status(False, f"Error: {e}")

# Create channel with your exact setup
myChannel = channel.CEEO_Channel(
    "hackathon", "@chrisrogers", "talking-on-a-channel",
    divName='all_things_channels', suffix='_test'
)

print('📡 Channel reply status:', myChannel.reply)

# Set your callback
myChannel.callback = fred
'''
# Update initial status
if hasattr(myChannel, 'reply') and myChannel.reply:
    update_channel_status(True, "- Ready for MIDI data")
    print("✅ Channel initialized successfully!")
else:
    update_channel_status(False, "- Check connection")
    print("⚠️ Channel may not be connected")

print("🎼 Musical staves KNN classifier loaded!")
'''
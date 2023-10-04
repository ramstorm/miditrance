#########################################
# IMPORT
# MODULES
#########################################

import time
import rtmidi
from rtmidi.midiutil import open_midiinput, open_midioutput
from pynput.keyboard import Key, Controller
import config

#########################################
# MIDI CALLBACK
#
#########################################

keyboard = Controller()
modifier = False
enable_keymap = False
key_reference = next(iter(config.keymap))
midi_in = None
midi_out = None
mod_1_pressed = False
mod_2_pressed = False
transpose = 0

class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        global modifier
        global enable_keymap
        global key_reference
        global midi_out
        global mod_1_pressed
        global mod_2_pressed
        global transpose
        message, deltatime = event
        self._wallclock += deltatime
        messagetype = message[0] >> 4
        channel = (message[0] & 15) + 1
        note = message[1] if len(message) > 1 else None
        velocity = message[2] if len(message) > 2 else None

        if enable_keymap and messagetype == 9 and note in config.keymap: # Note on
            keyboard.press(config.keymap[note])
        elif enable_keymap and messagetype == 8 and note in config.keymap: # Note off
            keyboard.release(config.keymap[note])
        else:
            if messagetype == 9: # Note on
                if note == config.mod_key_1:
                    mod_1_pressed = True
                elif note == config.mod_key_2:
                    mod_2_pressed = True
                elif mod_1_pressed and mod_2_pressed and note == config.mod_oct_up:
                    transpose += 12 if transpose < config.transpose_max else 0
                elif mod_1_pressed and mod_2_pressed and note == config.mod_oct_dn:
                    transpose -= 12 if transpose > config.transpose_min else 0
                elif mod_1_pressed and mod_2_pressed and note == config.mod_start:
                    keyboard.press('x')
                elif mod_1_pressed and mod_2_pressed and note == config.mod_toggle:
                    enable_keymap = not enable_keymap
            elif messagetype == 8: # Note off
                if note == config.mod_key_1:
                    mod_1_pressed = False
                elif note == config.mod_key_2:
                    mod_2_pressed = False
            if note is not None:
                message[1] = note + transpose
            midi_out.send_message(message)


#########################################
# MIDI DEVICES DETECTION
# MAIN LOOP
#########################################

for port in rtmidi.MidiOut().get_ports():
    if config.midi['out_device'] in port:
        midi_out, port_name = open_midioutput(port)
        print('Opened MIDI output: ' + port_name)
        break
for port in rtmidi.MidiIn().get_ports():
    if config.midi['in_device'] in port:
        midi_in, port_name = open_midiinput(port)
        midi_in.set_callback(MidiInputHandler(port_name))
        print('Opened MIDI input: ' + port_name)
        break
if midi_in is None or midi_out is None:
    print("MIDI device not found.")
    exit()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midi_in.close_port()
    del midi_in


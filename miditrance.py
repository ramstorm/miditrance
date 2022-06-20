#########################################
# IMPORT
# MODULES
#########################################

import time
import rtmidi
from rtmidi.midiutil import open_midiinput
from pynput.keyboard import Key, Controller
import config

#########################################
# MIDI CALLBACK
#
#########################################

keyboard = Controller()
modifier = False
enable_keymap = True
key_reference = next(iter(config.keymap))

class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        global modifier
        global enable_keymap
        global key_reference
        message, deltatime = event
        self._wallclock += deltatime
        print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        messagetype = message[0] >> 4
        channel = (message[0] & 15) + 1
        note = message[1] if len(message) > 1 else None
        midinote = note
        velocity = message[2] if len(message) > 2 else None
        print('MIDI messagetype: ' + str(messagetype) + ' note: '  + str(note) + ' channel: ' + str(channel))
        if enable_keymap and messagetype == 9 and note in config.keymap: # Note on
            keyboard.press(config.keymap[note])
        elif enable_keymap and messagetype == 8 and note in config.keymap: # Note off
            keyboard.release(config.keymap[note])
        elif modifier and messagetype == 9: # Note on with modifier
            transpose = note - key_reference
            config.keymap = { k + transpose: v for k, v in config.keymap.items() }
            key_reference = note
            enable_keymap = True
            modifier = False
        elif messagetype == 12: # Program change - set modifier and toggle keymap
            if modifier:
                enable_keymap = not enable_keymap
                modifier = False
            else:
                modifier = True


#########################################
# MIDI DEVICES DETECTION
# MAIN LOOP
#########################################

midi_in = None
midi_out = None
for port in rtmidi.MidiIn().get_ports():
    if config.midi['in_device'] in port:
        midi_in, port_name = open_midiinput(port)
        midi_in.set_callback(MidiInputHandler(port_name))
        print('Opened MIDI input: ' + port_name)
        break
if midi_in is None:
    print("MIDI input not found.")
    exit()

try:
    # Just wait for keyboard interrupt,
    # everything else is handled via the input callback.
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midi_in.close_port()
    del midi_in


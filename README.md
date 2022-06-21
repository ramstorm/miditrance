# miditrance
Translates MIDI notes to keyboard input.

Setup MIDI input and output ports (use `aconnect -l` to list) and note-to-key mappings as desired in `config.py`. Refer to the pynput documentation for available keys.

Program change (PC) acts as a modifier key.
* Send a PC and then a midi note to transpose all note-to-key mappings relative to that midi note.
* Send a PC and then another PC to toggle note-to-key mappings on and off.
* NOTE: The value of the PC does not matter. Use any value. The idea behind this is to make use of the PC up/down buttons that some MIDI devices have.

## Installation

Make sure you have python3 installed. The program was developed and tested using python 3.9.2.

Install dependencies:

```
sudo apt-get install python3-rtmidi
sudo apt-get install python3-pip
sudo pip3 install pynput
```

Run the program:

`python3 miditrance.py`

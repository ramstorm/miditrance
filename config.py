from pynput.keyboard import Key, Controller

midi = dict(
        in_device = 'Midi Through',
        out_device = 'M8',
)
keymap = {
        45:Key.left,
        47:'a',
        48:Key.down,
        50:Key.up,
        52:Key.right,
        53:'z',
        55:'s',
        56:'x',
}
mod_key_1 = 57
mod_key_2 = 59
mod_oct_up = 62
mod_oct_dn = 60
mod_toggle = 64
mod_start = 65
transpose_max = 36
transpose_min = -36


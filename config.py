from pynput.keyboard import Key, Controller

midi = dict(
        in_device = 'Midi Through',
        out_device = 'M8',
)
keymap = {
        45:Key.left,
        47:'z',
        48:Key.down,
        50:Key.up,
        52:Key.right,
        53:'a',
        55:'x',
        56:'s',
}
mod_key_1 = 57
mod_key_2 = 59
mod_oct_up = 62
mod_oct_dn = 60
mod_toggle = 67
mod_start = 65
transpose_max = 36
transpose_min = -36


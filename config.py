from pynput.keyboard import Key, Controller

midi = dict(
        in_device = 'iRig Keys',
        out_device = 'M8',
)
keymap = {
        48:'z',
        49:'a',
        50:'x',
        51:'s',
        52:Key.left,
        53:Key.down,
        54:Key.up,
        55:Key.right,
}


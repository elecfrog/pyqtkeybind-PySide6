# -*- coding: utf-8 -*-

import ctypes
from ctypes import windll
from qtpy.QtGui import QKeySequence
from qtpy.QtCore import Qt

from .keycodes import KeyTbl, ModsTbl


def extract_keys(keysequence: QKeySequence):
    # Extract the integer representation
    # print(f'Registered: {keysequence}')

    ks_comb = keysequence[0]
    # print(f'ks_comb: {ks_comb}')

    ks_modifiers = ks_comb.keyboardModifiers()
    # print(f'ks_modifiers: {ks_modifiers}')

    ks_key = ks_comb.key()
    # print(f'ks_key: {ks_key}')

    print(f'COMBS: {ks_comb} MOD: {ks_modifiers} KEYS: {ks_key}')

    # Calculate the modifiers
    mods = 0
    if ks_modifiers & Qt.ShiftModifier:
        mods |= ModsTbl.index(Qt.ShiftModifier)
    if ks_modifiers & Qt.AltModifier:
        mods |= ModsTbl.index(Qt.AltModifier)
    if ks_modifiers & Qt.ControlModifier:
        mods |= ModsTbl.index(Qt.ControlModifier)
    # print(f'mods = {mods}')

    # Calculate the keys, Use ks_key directly
    keys = 0
    try:
        keys = KeyTbl[ks_key]
        if keys == 0:
            keys = _get_virtual_key(ks_key)
    except ValueError:
        keys = _get_virtual_key(ks_key)
    except IndexError:
        keys = KeyTbl.index(ks_key)
        if keys == 0:
            keys = _get_virtual_key(ks_key)
    # print(f'keys = {keys}')

    print(f'mods = {mods}, keys = {keys}')

    return mods, keys


def _get_virtual_key(qtkeys):
    """Use the system keyboard layout to retrieve the virtual key.

    Fallback when we're unable to find a keycode in the mappings table.
    """
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    thread_id = 0

    # Key table doesn't have an entry for this keycode
    # Attempt to retrieve the VK code from system
    keyboard_layout = user32.GetKeyboardLayout(thread_id)
    virtual_key = windll.user32.VkKeyScanExW(qtkeys, keyboard_layout)
    if virtual_key == -1:
        keyboard_layout = user32.GetKeyboardLayout(0x409)
        virtual_key = windll.user32.VkKeyScanExW(qtkeys, keyboard_layout)
    # Key code is the low order byte
    keys = virtual_key & 0xff

    return keys

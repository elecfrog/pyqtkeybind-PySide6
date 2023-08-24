# -*- coding: utf-8 -*-

import sys

keybinder = None
if sys.platform.startswith("win"):
    from .win import WinKeyBinder

    keybinder = WinKeyBinder()
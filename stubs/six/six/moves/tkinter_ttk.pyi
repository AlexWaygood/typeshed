"""Ttk wrapper.

This module provides classes to allow using Tk themed widget set.

Ttk is based on a revised and enhanced version of
TIP #48 (http://tip.tcl.tk/48) specified style engine.

Its basic idea is to separate, to the extent possible, the code
implementing a widget's behavior from the code implementing its
appearance. Widget class bindings are primarily responsible for
maintaining the widget state and invoking callbacks, all aspects
of the widgets appearance lies at Themes.
"""

from tkinter.ttk import *

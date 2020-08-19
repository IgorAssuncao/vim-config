# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, MODify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

from typing import List  # noqa: F401

GROUPS = "12345678"
MOD = "mod4"
TERMINAL = "kitty"
BROWSER = "firefox-developer-edition"
FILEMANAGER = "pcmanfm"

keys = [
    # Switch between windows in current stack pane
    Key([MOD], "k", lazy.layout.down()),
    Key([MOD], "j", lazy.layout.up()),

    # Move windows up or down in current stack
    Key([MOD, "control"], "k", lazy.layout.shuffle_down()),
    Key([MOD, "control"], "j", lazy.layout.shuffle_up()),

    # Switch window focus to other pane(s) of stack
    Key([MOD], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([MOD, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([MOD, "shift"], "Return", lazy.layout.toggle_split()),

    # Spawn terminal
    Key([MOD], "Return", lazy.spawn(TERMINAL)),

    # Toggle between different layouts as defined below
    Key([MOD], "Tab", lazy.next_layout()),
    Key([MOD], "w", lazy.window.kill()),

    Key([MOD, "control"], "r", lazy.restart()),
    Key([MOD, "control"], "q", lazy.shutdown()),
    Key([MOD], "r", lazy.spawncmd()),

    # Spawn bmenu
    Key([MOD, "control"], "b", lazy.spawn(f"{TERMINAL} -e bmenu")),

    # Spawn dmenu_run
    Key([MOD], "c", lazy.spawn("dmenu_run")),

    # Spawn morce_menu
    Key([MOD], "z", lazy.spawn("morc_menu")),

    # Spawn browser
    Key([MOD], "b", lazy.spawn(BROWSER)),

    # Spawn File Manager
    Key([MOD], "F3", lazy.spawn(FILEMANAGER)),

    # Spawn pavucontrol
    Key([MOD, "control", "shift"], "m", lazy.spawn("pavucontrol")),

    # Spawn blurlock (Lock screen)
    Key([MOD], "9", lazy.spawn("blurlock"))
]

groups = [Group(i) for i in GROUPS]

for i in groups:
    keys.extend([
        # MOD + letter of group = switch to group
        Key([MOD], i.name, lazy.group[i.name].toscreen()),

        # MOD + shift + letter of group = switch to & move focused window to group
        Key([MOD, "control"], i.name, lazy.window.togroup(i.name)),

        # MOD + shift + letter of group = switch to & move focused window to group
        Key([MOD, "shift"], i.name, lazy.window.togroup(i.name), lazy.group[i.name].toscreen()),
    ])

# Layout theme that will be applied to all layouts specified below
LAYOUT_THEME = {
    "margin": 5,
    "border_width": 2,
    "border_focus": "00ffff",
    "border_normal": "969896",
}

layouts = [
    layout.MonadTall(**LAYOUT_THEME),
    layout.Stack(num_stacks = 4)
]

widget_defaults = {
    "font": "monospace",
    "fontsize": 12,
    "padding": 3
}
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Systray(),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p')
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([MOD], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([MOD], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([MOD], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup
def autostart():
    scriptLocation = '~/system-config/.config/qtile/autostart.sh'
    script = os.path.expanduser(scriptLocation)
    subprocess.call([script])

import math

import components.audio_plug as audio_plug
import components.usb_hub as usb_hub
import components.keyboard as keyboard
import components.screen_pillars as screen_pillars

## Standard things (TODO move to separate file)

# M3 threaded insert sizes
ti_radius = 2.35
ti_depth = 6.25

# M3 hex nut dimensions
m3_hn_diam = 6.2
m3_hn_hole = 3
m3_hn_thickness = 2.5

# Dimensions for countersunk M4 screws
m4_top = 9
m4_bottom = 4

## Keyboard dimensions
keyboard.kbd_height = 95.5
keyboard.kbd_width = 305
keyboard.kbd_back_thickness = 19
keyboard.kbd_front_thickness = 12
# Pythagoras
keyboard.kbd_actual_height = (
    keyboard.kbd_height**2
    - (keyboard.kbd_back_thickness - keyboard.kbd_front_thickness) ** 2
) ** 0.5
keyboard.kbd_angle = (
    math.acos(keyboard.kbd_actual_height / keyboard.kbd_height) * 180 / math.pi
)
keyboard.kbd_pillar_positions = [
    (19, 16),
    (142.5, 25.5),
    (keyboard.kbd_width - 20, 16),
    (23.5, 79.5),
    (145.5, 82.5),
    (keyboard.kbd_width - 19, 79.5),
]
keyboard.kbd_pillar_offset_1 = 5.5
keyboard.kbd_pillar_radius_1 = 5
keyboard.kbd_pillar_offset_2 = 2.5
keyboard.kbd_pillar_radius_2 = 2.4
keyboard.kbd_screw_radius = 1.1
keyboard.init()

## Screen dimensions
# Whole screen size
scr_w = 231
scr_h = 65
scr_thickness = 5.5
# Visible screen size
vis_w = 219
vis_h = 55


## Dimensions for the base of the computer

# Thickness of the outer material
shell_t = 3

# Size of the base
width = keyboard.kbd_width + 2 * shell_t
height = 159
base_thickness = 30 + shell_t  # 30 inside


# These are placed where convenient, and are used to join the top and bottom
# parts of the case.
# Measured from back-left corner OUTSIDE
mounting_pillar_positions = [
    (6, 6),
    (6, 43),
    (120, 6),
    (170, 6),
    (width - 6, 6),
    (width - 6, 43),
    (120, 48),
    (170, 48),
]

# Offset for the USB port from back-left corner
# of the case to left side of the hub
usb_offset_x = width - audio_plug.item_w - usb_hub.item_w

# CPU holder position from back-left corner of the case
cpu_offset_x = 177
cpu_offset_y = 2

# Battery holder position from back-left corner of the case
battery_offset_x = 15
battery_offset_y = 3

# HDMI out hole from back-left corner of the case
hdmi_out_offset_x = 138

## Dimensions for the Tandy lid

# Size of the whole object
tl_height = 66
tl_height_bottom = 59
tl_full_thickness = 48  # Will be shorter after construction
# Screen angle
tl_scr_angle = 20


## Dimensions for the hinged lid

# This is a constant used to control how far back the hinges go
# when open. It's arbitrary and can be adjusted experimentally
# printing small samples
hl_hinge_slant = shell_t + 2

hl_bezel_width = m3_hn_diam + 2
hl_bezel_height = 1
hl_bezel_thickness = 2

hl_hinge_radius = 5.5
hl_screw_radius = 1.5  # M3
hl_ring_radius = 5  # M3
hl_hinge_offset = max(p[1] for p in mounting_pillar_positions) + 6
hl_hinge_width = 25
# Base + this lid
hl_full_thickness = 43


## Dimensions for the simple lid
sl_lip_thickness = 1.5
sl_height = (
    max([y for _, y in mounting_pillar_positions]) + 6 + shell_t + sl_lip_thickness
)
sl_thickness = shell_t
sl_front_lip = 8

## Dimensions for pillars that connect base and lids
screen_pillars.pillar_width = 12
screen_pillars.pillar_height = 12
screen_pillars.screw_head_radius = 3
screen_pillars.screw_radius = 1.8
screen_pillars.screw_head_depth = (
    base_thickness - 13
)  # (screw thread length - threaded insert depth)

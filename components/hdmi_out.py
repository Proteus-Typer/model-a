# Hole to expose a USB audio card (YMMV)

import cadquery as cq

from utils import punch_hole

# The hole is for a random USB sound card.
# Consumers should set proper offsets for the hole

holes = [
    # Hole for HDMI female adapter
    {
        "x": 0,
        "y": 7,
        "shape": cq.Sketch().trapezoid(22, 12.5, 90, mode="a").vertices().fillet(2),
    },
]


def add(
    *,
    model,
    width,
    height,
    thickness,
    offset_x,
    offset_y,
    bottom_face,
    back_face,
    shell_t
):
    # Holes
    if back_face:
        for hole in holes:
            model = punch_hole(
                model=model,
                face=back_face,
                w=width,
                h=thickness,
                x_offset=width - offset_x,
                y_offset=shell_t,
                hole=hole,
                depth=shell_t,
            )

    return model

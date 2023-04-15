# Hole to expose a USB audio card (YMMV)

import cadquery as cq

from utils import extrude_shape, punch_hole

# The hole is for a random USB sound card.
# Consumers should set proper offsets for the hole

item_w = 49
item_h = 20.5

hole_w = 17
hole_h = 5

holes = [
    # 2-jack plug
    {
        "x": -item_h / 2,
        "y": 4,
        "shape": cq.Sketch()
        .trapezoid(hole_w, hole_h, 90, mode="a")
        .vertices()
        .fillet(2),
    },
]

elements = [
    # Outline
    {
        "x": item_w / 2,
        "y": item_h / 2,
        "shape": (
            cq.Sketch()
            .trapezoid(item_w, item_h, 90, mode="a")
            .trapezoid(item_w - 2, item_h - 2, 90, mode="s")
        ),
        "height": 0.2,
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
    # Extrusions
    if bottom_face:
        for element in elements:
            model = extrude_shape(
                model=model,
                face=bottom_face,
                w=width,
                h=height,
                x_offset=offset_x,
                y_offset=offset_y,
                element=element,
                height=-(element["height"] + shell_t),
            )

    # Holes
    if back_face:
        for hole in holes:
            model = punch_hole(
                model=model,
                face=back_face,
                # FIXME: This is weird because it's the RIGHT side,
                # So it's height instead of w, offset_y instead of x
                # need to work on making these coherent
                w=height,
                h=thickness,
                x_offset=height - offset_y,
                y_offset=shell_t,
                hole=hole,
                depth=shell_t,
            )

    return model

import cadquery as cq

from utils import punch_hole, extrude_shape

# Measurements for my USB hub, YMMV

# The hole is for a USB-A plug, y is measured in the hub
# (from the bottom face to middle of the hole)
# Consumers should set proper offsets for the hole

item_w = 17
item_h = 93

holes = [
    # USB-A port
    {
        "x": -item_w / 2,
        "y": 4,
        "shape": cq.Sketch().trapezoid(13, 5, 90, mode="a").vertices().fillet(1),
    },
]

elements = [
    # Thing to grab the hub
    {
        "x": item_w / 2,
        "y": 5,
        "shape": (
            cq.Sketch().trapezoid(22, 10, 90, mode="a").trapezoid(17, 10, 90, mode="s")
        ),
        "height": 8,
    },
    {
        "x": item_w / 2 + 5.5,
        "y": item_h - 3,
        "shape": (cq.Sketch().circle(2.5, mode="a")),
        "height": 8,
    },
    {
        "x": item_w / 2 - 5.5,
        "y": item_h - 3,
        "shape": (cq.Sketch().circle(2.5, mode="a")),
        "height": 8,
    },
    # Outline
    {
        "x": item_w / 2,
        "y": item_h / 2,
        "shape": (
            cq.Sketch()
            .trapezoid(item_w, item_h, 90, mode="a")
            .trapezoid(item_w - 2, item_h - 2, 90, mode="s")
            .vertices()
            .fillet(3)
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
    # USB Hub extrusions
    if bottom_face:
        for element in elements:
            model = extrude_shape(
                model=model,
                face=bottom_face,
                w=width,
                h=height,
                x_offset=offset_x,
                y_offset=shell_t + offset_y,
                element=element,
                height=-(element["height"] + shell_t),
            )

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

import cadquery as cq

from utils import extrude_shape, punch_hole, hex_vents

width = 65
height = 30
pillar_height = 7

stand_positions = [(3.5, 3.5), (3.5, 26.5), (61.5, 26.5), (61.5, 3.5)]

stands = (
    cq.Sketch().push(stand_positions).circle(3, mode="a").circle(2.65 / 2, mode="s")
)


elements = [
    # CPU holder stands
    {
        "x": 0,
        "y": 0,
        "shape": stands,
        "height": pillar_height,
    },
    {
        "x": 0,
        "y": 0,
        "shape": cq.Sketch().push(stand_positions).circle(5),
        "height": 0,
    },
    # Perimeter
    {
        "x": width / 2,
        "y": height / 2,
        "shape": (
            cq.Sketch()
            .trapezoid(width, height, 90, mode="a")
            .trapezoid(width - 2, height - 2, 90, mode="s")
            .vertices()
            .fillet(3)
        ),
        "height": 0.2,
    },
]

vents = hex_vents(size=3, width=width, height=height)

holes = [
    # One hole for everything TODO: improve
    {
        "x": -width / 2,
        "y": 1 + pillar_height,
        "shape": cq.Sketch().trapezoid(50, 6, 90, mode="a").vertices().fillet(1),
    }
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
    if bottom_face:
        # Vents
        for vent in vents:
            model = punch_hole(
                model=model,
                face=bottom_face,
                w=width,
                h=height,
                x_offset=offset_x + vent["x"],
                y_offset=shell_t + offset_y + vent["y"],
                hole=vent,
                depth=shell_t,
            )

        # CPU holder extrusions
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

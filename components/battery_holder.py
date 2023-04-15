import cadquery as cq

from utils import extrude_shape, punch_hole, hex_vents

stand_positions = [(3.5, 3.5), (61.5, 3.5), (61.5, 52.5), (3.5, 52.5)]
stands = (
    cq.Sketch().push(stand_positions).circle(3, mode="a").circle(2.65 / 2, mode="s")
)
pillar_height = 7
width = 85
height = 56

# This is a holder for DuPont cables so they connect to this
# things' pogo pins which are used to power the CPU
pin_positions = [(3.5, 0), (4 * 2.54 + 3.5, 0)]
pin_holder_width = 25
pin_holder_height = 15
pin_holder = (
    cq.Sketch()
    .polygon(
        [
            (0.5, 0),
            (pin_holder_width, 0),
            (pin_holder_width, pin_holder_height),
            (0, pin_holder_height),
            (0.5, 0),
        ],
        mode="a",
    )
    .push(pin_positions)
    .polygon(
        [(0, 0), (2.6, 0), (2.6, pin_holder_height), (0, pin_holder_height), (0, 0)],
        mode="s",
    )
)

elements = [
    # Battery holder stands
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
    # Pogo pin connector channels
    {
        "x": 3.5,
        "y": 43.5,
        "shape": pin_holder,
        "height": 3,
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


# Hole distances are relative to the rightmost pillar
# seen from the back of the case, that's why they are negative
# Heights are relative to base of pillars
# All distances are measured to the CENTER of the hole
holes = [
    # Power inlet
    {
        "x": -18.5,
        "y": -1 + pillar_height,
        "shape": cq.Sketch().trapezoid(12, 6.5, 90, mode="a").vertices().fillet(1),
    },
    # Power button
    {
        "x": -70,
        "y": 5.5 + pillar_height,
        "shape": cq.Sketch().trapezoid(7, 7, 90, mode="a").vertices().fillet(1),
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

        # Battery holder stands and pogo pin holder
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

    if back_face:
        # Holes
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

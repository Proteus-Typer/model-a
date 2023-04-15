from utils import extrude_shape, punch_hole
import cadquery as cq

elements = None
bottom_holes = None

# These are set from dimensions.py
pillar_width = 0
pillar_height = 0
screw_head_radius = 0
screw_head_depth = 0
screw_radius = 0


def init(positions, thickness):
    """Because these need to match in multiple models, we create the
    elemments dynamically"""
    global elements, bottom_holes
    elements = [
        {
            "x": 0,
            "y": 0,
            "shape": cq.Sketch()
            .push(positions)
            .trapezoid(pillar_width, pillar_height, 90, mode="a"),
            "height": thickness,
        }
    ]

    bottom_holes = [
        {
            "x": 0,
            "y": 0,
            "shape": cq.Sketch().push(positions).circle(screw_head_radius, mode="a"),
            "depth": screw_head_depth,
        },
        {
            "x": 0,
            "y": 0,
            "shape": cq.Sketch().push(positions).circle(screw_radius, mode="a"),
            "depth": 100,
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
        # Mounting pillars
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
        # Screw holes
        for hole in bottom_holes:
            model = punch_hole(
                model=model,
                face=bottom_face,
                w=width,
                h=height,
                x_offset=offset_x,
                y_offset=shell_t + offset_y,
                hole=hole,
                depth=hole["depth"],
            )

    return model

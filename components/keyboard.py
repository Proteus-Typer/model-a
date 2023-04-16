import cadquery as cq

# These should be set from dimensions.py
elements = None
kbd_pillar_positions = []
kbd_height = 0
kbd_width = 0
kbd_back_thickness = 0
kbd_front_thickness = 0
kbd_actual_height = 0
kbd_angle = 0
kbd_pillar_offset_1 = 0
kbd_pillar_radius_1 = 0
kbd_pillar_offset_2 = 0
kbd_pillar_radius_2 = 0
kbd_screw_radius = 0


def init():
    global elements

    elements = [
        # Shorter pillars
        {
            "x": 0,
            "y": 0,
            "z": kbd_pillar_offset_1,
            "shape": cq.Sketch()
            .push(kbd_pillar_positions)
            .circle(kbd_pillar_radius_1, mode="a"),
        },
        # Taller pillars with holes for self-tapping screws
        {
            "x": 0,
            "y": 0,
            "z": kbd_pillar_offset_2,
            "shape": (
                cq.Sketch()
                .push(kbd_pillar_positions)
                .circle(kbd_pillar_radius_2, mode="a")
                .circle(kbd_screw_radius, mode="s")
            ),
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
    # This one is special, it creates angled things and cuts off the
    # case, so ... it's going to do weird stuff

    if bottom_face:
        model = (
            model.faces(bottom_face)
            .workplane(centerOption="CenterOfBoundBox", offset=-kbd_front_thickness)
            .center(
                -width / 2,
                height / 2,
            )
            .transformed(rotate=cq.Vector(kbd_angle, 0, 0))
            .tag("kbd_sloped")
        )
        for element in elements:
            model = (
                model.workplaneFromTagged("kbd_sloped")
                .center(offset_x + element["x"], -offset_y - element["y"])
                .workplane(offset=element["z"])
                .placeSketch(element["shape"])
                .extrude(100)
            )

        model = (
            model.workplaneFromTagged("mid_height")
            .transformed(offset=cq.Vector(0, 0, -thickness / 2))
            .split(keepTop=True)
            .faces(">X")
            .workplane(centerOption="CenterOfBoundBox")
            .center(-height / 2, -thickness / 2)
            .placeSketch(
                cq.Sketch().polygon(
                    [
                        [0, kbd_front_thickness],
                        [shell_t, kbd_front_thickness],
                        [kbd_actual_height + shell_t, kbd_back_thickness],
                        [kbd_actual_height + shell_t, 1000],
                        [0, 1000],
                        [0, kbd_front_thickness],
                    ]
                )
            )
            .cutBlind(-1000)
        )
    return model

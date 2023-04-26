import cadquery as cq

import dimensions as dim
from utils import export
from components import screen_pillars

viewport_cutout = (
    cq.Sketch().trapezoid(dim.vis_w, dim.vis_h, 90, mode="a").vertices().fillet(2)
)
screen_cutout = cq.Sketch().trapezoid(dim.scr_w, dim.scr_h, 90, mode="a")

# Circuit board and cable hole.
# This is in the back of the screen, and is a bit shorter in height than the
# screen. It's wider so it removes enough material to make the shape simpler.
board_cutout = cq.Sketch().trapezoid(
    dim.scr_w + 5,
    dim.scr_h - 10,
    90,
    mode="a",
)

kbd_cable_hole = cq.Sketch().trapezoid(20, 9, 90, mode="a").vertices().fillet(1)

# y needs to be inverted because this is the top side, and there's 2 pillars we don't use
mounting_pillar_positions = [(x, -y) for x, y in dim.mounting_pillar_positions[:-2]]

mounting_pillars = (
    cq.Sketch()
    .push(mounting_pillar_positions)
    .trapezoid(screen_pillars.pillar_width, screen_pillars.pillar_height, 90, mode="a")
    .circle(dim.ti_radius, mode="s")
    .clean()
)


def model():
    return (
        cq.Workplane("XY")
        .workplane()
        .tag("mid_height")
        .box(dim.width, dim.tl_height, dim.tl_full_thickness)
        # The screen goes rotated
        .faces(">Z")
        .transformed(rotate=(dim.tl_scr_angle, 0, 0))
        # Move the screen "lower" so it doesn't interfere
        # so much with the back
        .center(0, -2)
        .tag("slanted")
        # Arbitrary huge trapezoid to cut off the material *in front*
        # of the inclined screen
        .placeSketch(cq.Sketch().trapezoid(1000, 1000, 90, mode="a"))
        .cutBlind(1000)
        # Trim the top
        .workplaneFromTagged("mid_height")
        .workplane(offset=21)
        .placeSketch(cq.Sketch().trapezoid(1000, 1000, 90, mode="a"))
        .cutBlind(100)
        # Make bottom smaller to fit with base
        .faces(">X")
        .workplane(centerOption="CenterOfBoundBox")
        .center(-dim.tl_height / 2, -dim.tl_full_thickness / 2)
        .placeSketch(
            cq.Sketch()
            .polygon(
                [
                    (dim.tl_height_bottom, 0),
                    (dim.tl_height_bottom, dim.tl_full_thickness / 3),
                    (dim.tl_height, dim.tl_full_thickness - 21),
                    (dim.tl_height, dim.tl_full_thickness),
                    (dim.tl_height + 5, dim.tl_full_thickness + 5),
                    (dim.tl_height + 5, 0),
                    (dim.tl_height_bottom, 0),
                ]
            )
            .vertices()
            .fillet(3)
        )
        .cutBlind(-1000)
        # Fillet top of the object
        .edges("|X and >Z")
        .fillet(3)
        # Cut off viewport hole so we can see the screen
        .workplaneFromTagged("slanted")
        .placeSketch(viewport_cutout)
        .cutBlind(-dim.shell_t)
        # Make hole for screen assembly so the whole screen fits
        .workplaneFromTagged("slanted")
        .workplane(offset=-dim.shell_t, centerOption="CenterOfBoundBox")
        # Left bezel is wider than right one, so this hole is displaced to the left
        .center(-3, 0)
        .placeSketch(screen_cutout)
        .cutBlind(-dim.scr_thickness)
        # Make it hollow
        .faces("<Z")
        # Can't be exactly shell_t because cq fails
        .shell(-dim.shell_t + 0.01)
        # Cut hole for the screen board and cables
        .workplaneFromTagged("slanted")
        .workplane(offset=-dim.scr_thickness, centerOption="CenterOfBoundBox")
        .placeSketch(board_cutout)
        .cutBlind(-6)
        .workplaneFromTagged("mid_height")
        .workplane(offset=-dim.tl_full_thickness / 2, centerOption="CenterOfBoundBox")
        .center(-dim.width / 2, dim.tl_height_bottom - dim.tl_height / 2 - dim.shell_t)
        .placeSketch(mounting_pillars)
        .extrude(10)
        # Fillet the front edge of the screen case so it looks softer
        .edges(">(0, -10, 5)")
        .fillet(2)
    )


if __name__ == "__main__":
    model = model()
    export(model, "tandy_lid.stl")

    offset_width = -dim.width / 2

    right_side = (
        model.faces(">X")
        .workplane(centerOption="CenterOfBoundBox", offset=offset_width)
        .split(keepTop=True)
    )

    export(right_side, "tandy_lid_right.stl")

    left_side = (
        model.faces(">X")
        .workplane(centerOption="CenterOfBoundBox", offset=offset_width)
        .split(keepBottom=True)
    )

    export(left_side, "tandy_lid_left.stl")

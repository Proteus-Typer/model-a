import cadquery as cq

import dimensions as dim
import components.keyboard as keyboard
import components.screen_pillars as screen_pillars
from utils import export

mounting_pillar_positions = [(x, -y) for x, y in dim.mounting_pillar_positions]
mounting_pillars = (
    cq.Sketch()
    .push(mounting_pillar_positions)
    .trapezoid(screen_pillars.pillar_height, screen_pillars.pillar_width, 90, mode="a")
    .circle(dim.ti_radius, mode="s")
    .clean()
)


def model():
    # Create a 2-part hinged lid

    model = (
        cq.Workplane("XY")
        # Hollow box
        .workplane(offset=-dim.hl_full_thickness / 2)
        .box(dim.width, dim.height, dim.hl_full_thickness)
        .tag("base")
        .edges("|X and >Z and <Y")
        .fillet(10)
        .edges("|X and >Z and >Y")
        .fillet(5)
        .edges("|Z")
        .fillet(2)
        .faces("<Z")
        .shell(-dim.shell_t)
        .faces(">X")
        .workplane()
        .center(
            dim.height / 2 - dim.hl_hinge_offset,
            dim.hl_full_thickness / 2 - dim.hl_hinge_radius,
        )
        .tag("rightSide")
        # Outer surface of the hinge
        .workplaneFromTagged("rightSide")
        .placeSketch(cq.Sketch().circle(dim.hl_hinge_radius))
        .extrude(-dim.hl_hinge_width)
        .workplaneFromTagged("rightSide")
        .workplane(offset=-dim.width + dim.hl_hinge_width)
        .placeSketch(cq.Sketch().circle(dim.hl_hinge_radius))
        .extrude(-dim.hl_hinge_width)
        # Cut middle section between the hinges
        .workplaneFromTagged("rightSide")
        .workplane(offset=-dim.hl_hinge_width)
        .placeSketch(
            cq.Sketch().polygon(
                [
                    (-dim.hl_hinge_radius, -dim.hl_hinge_radius),
                    (-dim.hl_hinge_radius, 0),
                    (-dim.hl_hinge_radius - dim.hl_hinge_slant, dim.hl_hinge_radius),
                    (-dim.hl_hinge_slant, dim.hl_hinge_radius),
                    (-dim.hl_hinge_slant, dim.hl_hinge_radius - dim.hl_hinge_slant),
                    (dim.hl_hinge_radius, dim.hl_hinge_radius - dim.hl_hinge_slant),
                    (dim.hl_hinge_radius, -dim.hl_hinge_radius),
                    (-dim.hl_hinge_radius, -dim.hl_hinge_radius),
                ]
            )
        )
        .cutBlind(-dim.width + 2 * dim.hl_hinge_width - 1)
        # Pillars to attach to base
        .workplaneFromTagged("base")
        .workplane(
            centerOption="CenterOfBoundBox",
            offset=dim.base_thickness - dim.hl_full_thickness / 2,
        )
        .workplaneFromTagged("base")
        .workplane(offset=dim.hl_full_thickness / 2 - dim.shell_t)
        .center(-dim.width / 2, dim.height / 2 - dim.shell_t)
        .placeSketch(mounting_pillars)
        .extrude(-10)
        # Hole for screws
        .workplaneFromTagged("rightSide")
        .placeSketch(cq.Sketch().circle(dim.hl_screw_radius))
        .cutBlind(-dim.hl_hinge_width)
        .workplaneFromTagged("rightSide")
        .workplane(offset=-dim.width + dim.hl_hinge_width)
        .placeSketch(cq.Sketch().circle(dim.hl_screw_radius))
        .cutBlind(-dim.hl_hinge_width)
        # Holes for rings & screw heads
        .workplaneFromTagged("rightSide")
        .placeSketch(cq.Sketch().circle(dim.hl_ring_radius))
        .cutBlind(-5)
        .workplaneFromTagged("rightSide")
        .workplane(offset=-dim.width + 4)
        .placeSketch(cq.Sketch().circle(dim.hl_ring_radius))
        .cutBlind(-5)
        # Split hinge halves
        .faces(">X")
        .workplaneFromTagged("rightSide")
        .workplane(offset=-dim.hl_hinge_width / 2)
        .placeSketch(
            cq.Sketch().trapezoid(
                dim.hl_hinge_radius * 2 + 1, dim.hl_hinge_radius * 2, 90
            )
        )
        .cutBlind(-1)
        .workplaneFromTagged("rightSide")
        .workplane(offset=-dim.hl_hinge_width)
        .placeSketch(
            cq.Sketch().trapezoid(
                dim.hl_hinge_radius * 2 + 1, dim.hl_hinge_radius * 2, 90
            )
        )
        .cutBlind(-1)
        .workplaneFromTagged("rightSide")
        .workplane(offset=-dim.width + dim.hl_hinge_width / 2)
        .placeSketch(
            cq.Sketch().trapezoid(
                dim.hl_hinge_radius * 2 + 1, dim.hl_hinge_radius * 2, 90
            )
        )
        .cutBlind(-1)
        .workplaneFromTagged("rightSide")
        .workplane(offset=-dim.width + dim.hl_hinge_width)
        .placeSketch(
            cq.Sketch().trapezoid(
                dim.hl_hinge_radius * 2 + 1, dim.hl_hinge_radius * 2, 90
            )
        )
        .cutBlind(-1)
        # Threaded inserts
        .workplaneFromTagged("rightSide")
        .workplane(offset=-dim.hl_hinge_width / 2)
        .placeSketch(cq.Sketch().circle(dim.ti_radius))
        .cutBlind(-dim.ti_depth)
        .workplaneFromTagged("rightSide")
        .workplane(offset=-dim.width + dim.hl_hinge_width / 2)
        .placeSketch(cq.Sketch().circle(dim.ti_radius))
        .cutBlind(dim.ti_depth)
        # Split two halves
        # First cut for the right hinge
        .workplaneFromTagged("rightSide")
        .placeSketch(
            cq.Sketch()
            .polygon(
                [
                    (0, 0),
                    (-dim.hl_hinge_radius - 0.2, 0),
                    (-dim.hl_hinge_radius - dim.hl_hinge_slant, dim.hl_hinge_radius),
                    (0, dim.hl_hinge_radius),
                    (0, 0),
                ]
            )
            .polygon(
                [
                    (-dim.hl_hinge_radius - 0.2, 0),
                    (-dim.hl_hinge_radius - 0.2, -1000),
                    (-dim.hl_hinge_radius, -1000),
                    (-dim.hl_hinge_radius, 0),
                    (-dim.hl_hinge_radius - 0.2, 0),
                ]
            )
            .circle(dim.hl_hinge_radius, mode="s")
        )
        .cutBlind(-dim.hl_hinge_width / 2 - 1)
        # Second cut for the right hinge
        .workplaneFromTagged("rightSide")
        .workplane(offset=-dim.hl_hinge_width / 2)
        .placeSketch(
            cq.Sketch()
            .polygon(
                [
                    (0, 0),
                    (dim.hl_hinge_radius + 0.2, 0),
                    (
                        dim.hl_hinge_radius + 0.2 + dim.hl_hinge_slant,
                        dim.hl_hinge_radius,
                    ),
                    (0, dim.hl_hinge_radius),
                    (0, 0),
                ]
            )
            .circle(dim.hl_hinge_radius, mode="s")
        )
        .cutBlind(-dim.hl_hinge_width / 2 - 1)
        # First cut for the left hinge
        .workplaneFromTagged("rightSide")
        .workplane(offset=-dim.width + dim.hl_hinge_width)
        .placeSketch(
            cq.Sketch()
            .polygon(
                [
                    (0, 0),
                    (dim.hl_hinge_radius + 0.2, 0),
                    (
                        dim.hl_hinge_radius + 0.2 + dim.hl_hinge_slant,
                        dim.hl_hinge_radius,
                    ),
                    (0, dim.hl_hinge_radius),
                    (0, 0),
                ]
            )
            .circle(dim.hl_hinge_radius, mode="s")
        )
        .cutBlind(-dim.hl_hinge_width / 2 - 1)
        # Second cut for the left hinge
        .workplaneFromTagged("rightSide")
        .workplane(offset=-dim.width + dim.hl_hinge_width / 2)
        .placeSketch(
            cq.Sketch()
            .polygon(
                [
                    (0, 0),
                    (-dim.hl_hinge_radius - 0.2, 0),
                    (-dim.hl_hinge_radius - dim.hl_hinge_slant, dim.hl_hinge_radius),
                    (0, dim.hl_hinge_radius),
                    (0, 0),
                ]
            )
            .polygon(
                [
                    (-dim.hl_hinge_radius - 0.2, 0),
                    (-dim.hl_hinge_radius - 0.2, -1000),
                    (-dim.hl_hinge_radius, -1000),
                    (-dim.hl_hinge_radius, 0),
                    (-dim.hl_hinge_radius - 0.2, 0),
                ]
            )
            .circle(dim.hl_hinge_radius, mode="s")
        )
        .cutBlind(-dim.hl_hinge_width / 2 - 1)
    )

    # Screen mount
    model = (
        # 1st layer
        model.workplaneFromTagged("base")
        .center(0, -32)
        .workplane(offset=dim.hl_full_thickness / 2 - dim.shell_t)
        .tag("screen_plane")
        .placeSketch(
            cq.Sketch()
            .trapezoid(
                dim.scr_w + 2 * dim.hl_bezel_width,
                dim.scr_h + 2 * dim.hl_bezel_height,
                90,
            )
            .vertices()
            .fillet(2)
        )
        .extrude(-2 - dim.scr_thickness)
        # Hole for screws
        .workplaneFromTagged("screen_plane")
        .workplane(offset=1)
        .rect(
            dim.scr_w + 2 * dim.hl_bezel_width - dim.m3_hn_diam - 1,
            dim.scr_h + 2 * dim.hl_bezel_height - dim.m3_hn_diam - 1,
            forConstruction=True,
        )
        .vertices()
        .hole(dim.m3_hn_hole, depth=10)
        # Holes for captured nuts
        .workplaneFromTagged("screen_plane")
        .workplane(offset=1)
        .rect(
            dim.scr_w + 2 * dim.hl_bezel_width - dim.m3_hn_diam - 1,
            dim.scr_h + 2 * dim.hl_bezel_height - dim.m3_hn_diam - 1,
            forConstruction=True,
        )
        .vertices()
        .hole(dim.m3_hn_diam, depth=dim.m3_hn_thickness + 0.5)
        # Remove middle of the screen holder
        .workplaneFromTagged("screen_plane")
        .placeSketch(
            cq.Sketch().trapezoid(
                dim.scr_w - 40,
                dim.scr_h + 2 * dim.hl_bezel_height,
                90,
            )
        )
        .cutBlind(-100)
        # Hole to place screen
        .workplaneFromTagged("screen_plane")
        .workplane(offset=-dim.scr_thickness - 2)
        .placeSketch(cq.Sketch().trapezoid(dim.scr_w, dim.scr_h, 90))
        .cutBlind(dim.scr_thickness)
    )

    # Cut off shape of the base
    model = (
        model.workplaneFromTagged("rightSide")
        .center(
            -dim.height + dim.hl_hinge_offset,
            -dim.hl_full_thickness + dim.hl_hinge_radius,
        )
        .placeSketch(
            cq.Sketch().polygon(
                [
                    (0, 0),
                    (0, keyboard.kbd_front_thickness),
                    (dim.shell_t, keyboard.kbd_front_thickness),
                    (keyboard.kbd_actual_height + dim.shell_t, keyboard.kbd_back_thickness),
                    (keyboard.kbd_actual_height + dim.shell_t, dim.base_thickness),
                    (dim.height, dim.base_thickness),
                    (dim.height, 0),
                    (0, 0),
                ]
            )
        )
        .cutBlind(-1000)
    )

    return model


def front_bezel():
    model = (
        cq.Workplane("XY")
        # Hollow box
        .tag("base")
        .placeSketch(
            cq.Sketch()
            .trapezoid(
                dim.scr_w + 2 * dim.hl_bezel_width + 2 * dim.hl_bezel_thickness,
                dim.scr_h + 2 * dim.hl_bezel_height + 2 * dim.hl_bezel_thickness,
                90,
            )
            .vertices()
            .fillet(2)
        )
        .extrude(-2 - dim.scr_thickness - dim.hl_bezel_thickness)
        .workplaneFromTagged("base")
        .workplane(offset=-dim.hl_bezel_thickness)
        .placeSketch(
            cq.Sketch()
            .trapezoid(
                dim.scr_w + 2 * dim.hl_bezel_width,
                dim.scr_h + 2 * dim.hl_bezel_height,
                90,
            )
            .vertices()
            .fillet(2)
        )
        .cutBlind(-100)
        # Holes for screws
        .workplaneFromTagged("base")
        .rect(
            dim.scr_w + 2 * dim.hl_bezel_width - dim.m3_hn_diam - 1,
            dim.scr_h + 2 * dim.hl_bezel_height - dim.m3_hn_diam - 1,
            forConstruction=True,
        )
        .vertices()
        .hole(dim.m3_hn_hole, depth=10)
        # Viewport hole
        .workplaneFromTagged("base")
        .placeSketch(
            cq.Sketch()
            .trapezoid(
                dim.vis_w,
                dim.vis_h,
                90,
            )
            .vertices()
            .fillet(2)
        )
        .cutBlind("last")
        # Cable gap
        .workplaneFromTagged("base")
        .workplane(offset=-dim.scr_thickness - dim.hl_bezel_thickness)
        .center(0, 10)
        .placeSketch(
            cq.Sketch()
            .trapezoid(
                dim.vis_w,
                dim.vis_h,
                90,
            )
            .vertices()
            .fillet(2)
        )
        .cutBlind(-10)
    )
    return model


if __name__ == "__main__":
    model = model()

    export(model, "hinged_lid.stl")

    export(front_bezel(), "hinged_lid_bezel.stl")

    export(
        model,
        "hinged_lid.svg",
        opt={
            "projectionDir": (0, 0, -1),
            "strokeWidth": 0.3,
        },
    )

    offset_width = -dim.width / 2

    right_side = (
        model.faces(">X")
        .workplane(centerOption="CenterOfBoundBox", offset=offset_width)
        .split(keepTop=True)
    )

    export(right_side, "hinged_lid_right.stl")

    left_side = (
        model.faces(">X")
        .workplane(centerOption="CenterOfBoundBox", offset=offset_width)
        .split(keepBottom=True)
    )

    export(left_side, "hinged_lid_left.stl")

import cadquery as cq

import dimensions as dim
from utils import extrude_shape2, hex_vents, punch_hole, export


def model():
    # Create the basic shape of the case lid
    model = (
        cq.Workplane("XY")
        # Hollow box
        .box(dim.width, dim.sl_height, dim.sl_thickness)
        .edges("|Z and >Y")
        .fillet(2)
        .faces("<Z")
        .tag("bottom")
    )

    # Make many holes
    vent = hex_vents(size=6, width=dim.width * 0.9, height=dim.sl_height * 0.9)[0]
    model = punch_hole(
        model=model,
        face=">Z",
        w=dim.width,
        h=dim.sl_height,
        x_offset=0.05 * dim.width,
        y_offset=0.05 * dim.sl_height,
        hole=vent,
        depth=dim.sl_thickness,
    )

    # Add screw holes
    for position in dim.mounting_pillar_positions:
        model = (
            model.faces(">Z")
            .workplane(centerOption="CenterOfBoundBox")
            .center(
                -dim.width / 2 + position[0],
                dim.sl_height / 2 - position[1] - dim.shell_t,
            )
            .placeSketch(cq.Sketch().circle(dim.m4_top / 2 + 1.5))
            .extrude(-dim.sl_thickness)
            .faces(">Z")
            .workplane(centerOption="CenterOfBoundBox")
            .center(
                -dim.width / 2 + position[0],
                dim.sl_height / 2 - position[1] - dim.shell_t,
            )
            .cskHole(dim.m4_bottom, dim.m4_top, 82, depth=None)
        )
    model.mounting_holes = [
        x for x in model.faces("<Z").edges("%CIRCLE").vals() if x.radius() == 2
    ]

    # Add front lip

    model = (
        model.faces(">Z")
        .workplane(centerOption="CenterOfBoundBox")
        .center(0, -dim.sl_height / 2 + dim.sl_lip_thickness / 2)
        .placeSketch(
            cq.Sketch().trapezoid(dim.width - 2 * dim.shell_t, dim.sl_lip_thickness, 90)
        )
        .extrude(-dim.sl_front_lip - dim.sl_thickness)
    )

    return model


def decorative_cover():
    # A decorative thingie to cover the ugly seam in the middle
    model = cq.Workplane("XY").box(10, dim.sl_height, 1).edges("|Z").fillet(1)
    vent = hex_vents(
        size=6, width=dim.width * 0.9, height=dim.sl_height * 0.9, density=0.775
    )[0]

    model = extrude_shape2(
        model=model,
        face=">Z",
        w=dim.width,
        h=dim.sl_height,
        x_offset=0.05 * dim.width,
        y_offset=0.05 * dim.sl_height,
        hole=vent,
        depth=3,
    )
    return model


if __name__ == "__main__":
    model = model()
    export(model, "simple_lid.stl")

    cover = decorative_cover()
    export(cover, "simple_lid_cover.stl")

    export(
        model,
        "simple_lid.svg",
        opt={
            "projectionDir": (0, 0, 1),
        },
    )

    export(
        model.faces(">X").workplane(offset=-dim.width / 2).split(keepTop=True),
        "simple_lid_right.stl",
    )
    export(
        model.faces(">X").workplane(offset=-dim.width / 2).split(keepBottom=True),
        "simple_lid_left.stl",
    )

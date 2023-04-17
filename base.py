import cadquery as cq

# from cq_warehouse.drafting import Draft

import components.audio_plug as audio_plug
import components.battery_holder as battery_holder
import components.hdmi_out as hdmi_out
import components.keyboard as keyboard
import components.screen_pillars as screen_pillars
import components.usb_hub as usb_hub
import components.zero_holder as cpu_holder
import dimensions as dim

from utils import export

# Base for the notebook. Basically a kbd base that extends back
# as much as possible

screen_pillars.init(dim.mounting_pillar_positions, dim.base_thickness - dim.shell_t)


def model():
    # Create the basic shape of the case bottom.
    model = (
        cq.Workplane("XY")
        .workplane(offset=dim.base_thickness / 2)
        .tag("mid_height")
        # Hollow box
        .box(dim.width, dim.height, dim.base_thickness)
        .edges("|Z")
        .fillet(2)
        .faces(">Z")
        .shell(-dim.shell_t)
    )

    # Now the basic box shape is in place, start adding things
    # and cutting holes.

    model = usb_hub.add(
        model=model,
        width=dim.width,
        height=dim.height,
        thickness=dim.base_thickness,
        bottom_face="<Z",
        back_face=">Y",
        offset_x=dim.usb_offset_x,
        offset_y=0,
        shell_t=dim.shell_t,
    )

    # Hole for audio in right side
    model = audio_plug.add(
        model=model,
        width=dim.width,
        height=dim.height,
        thickness=dim.base_thickness,
        offset_x=dim.width - audio_plug.item_w,
        offset_y=19,
        bottom_face="<Z",
        back_face=">X",
        shell_t=dim.shell_t,
    )

    # Hole for HDMI out in the back
    model = hdmi_out.add(
        model=model,
        width=dim.width,
        height=dim.height,
        thickness=dim.base_thickness,
        offset_x=dim.hdmi_out_offset_x,
        offset_y=0,
        bottom_face=None,
        back_face=">Y",
        shell_t=dim.shell_t,
    )

    model = cpu_holder.add(
        model=model,
        width=dim.width,
        height=dim.height,
        thickness=dim.base_thickness,
        offset_x=dim.cpu_offset_x,
        offset_y=dim.cpu_offset_y,
        bottom_face="<Z",
        back_face=None,  # Not exposing the holes
        shell_t=dim.shell_t,
    )

    # This adds all the holes and extrusions for the battery system
    model = battery_holder.add(
        model=model,
        width=dim.width,
        height=dim.height,
        thickness=dim.base_thickness,
        offset_x=dim.battery_offset_x,
        offset_y=dim.battery_offset_y,
        bottom_face="<Z",
        back_face=">Y",
        shell_t=dim.shell_t,
    )

    model = screen_pillars.add(
        model=model,
        width=dim.width,
        height=dim.height,
        thickness=dim.base_thickness,
        offset_x=0,
        offset_y=0,
        bottom_face="<Z",
        back_face=None,
        shell_t=dim.shell_t,
    )
    model.mounting_holes = [x for x in model.faces(">Z").edges("%CIRCLE").vals() if x.radius()==1.8]

    model = keyboard.add(
        model=model,
        width=dim.width,
        height=dim.height,
        thickness=dim.base_thickness,
        bottom_face="<Z",
        back_face=None,
        offset_x=dim.shell_t,
        offset_y=keyboard.kbd_height + dim.shell_t,
        shell_t=dim.shell_t,
    )

    return model


if __name__ == "__main__":
    model = model()

    left_cutout = cq.Sketch().polygon(
        [
            (0, 0),
            (dim.width / 2, 0),
            (dim.width / 2, -dim.height),
            (0, -dim.height),
            (0, 0),
        ],
        mode="a",
    )

    right_side = (
        model.faces("<Z")
        .workplaneFromTagged("mid_height")
        .transformed(offset=cq.Vector(0, 0, -dim.base_thickness / 2))
        .center(-dim.width / 2, dim.height / 2)
        .placeSketch(left_cutout)
        .cutBlind(100)
    )

    export(right_side, "base_right.stl")

    right_cutout = cq.Sketch().polygon(
        [
            (dim.width / 2, 0),
            (dim.width, 0),
            (dim.width, -dim.height),
            (dim.width / 2, -dim.height),
            (dim.width / 2, 0),
        ],
        mode="a",
    )

    left_side = (
        model.faces("<Z")
        .workplaneFromTagged("mid_height")
        .transformed(offset=cq.Vector(0, 0, -dim.base_thickness / 2))
        .center(-dim.width / 2, dim.height / 2)
        .placeSketch(right_cutout)
        .cutBlind(100)
    )
    export(left_side, "base_left.stl")

    # draft = Draft(decimal_precision=1)
    # dimensions = []
    # dimensions.append(
    #     draft.extension_line(
    #         object_edge=[
    #             cq.Vertex.makeVertex(-width / 2, -height / 2, 0),
    #             cq.Vertex.makeVertex(width / 2, -height / 2, 0),
    #         ],
    #         offset=10.0,
    #     )
    # )
    # dimensions.append(
    #     draft.extension_line(
    #         object_edge=[
    #             cq.Vertex.makeVertex(width / 2, -height / 2, 0),
    #             cq.Vertex.makeVertex(width / 2, height / 2, 0),
    #         ],
    #         offset=10.0,
    #     )
    # )

    export(model, "base.stl")

    # for d in dimensions[1:]:
    #     dimensions[0].add(d.toCompound())
    # dimensions[0].add(model)

    export(
        # model[0].toCompound(),
        model,
        "base.svg",
        opt={
            "projectionDir": (0, 0, 1),
            "strokeWidth": 0.3,
        },
    )

import shutil
import tempfile
from math import floor

import cadquery as cq
from cadquery import exporters


def extrude_shape(*, model, face, w, h, x_offset, y_offset, element, height):
    return (
        model.faces(face)
        .workplane(centerOption="CenterOfBoundBox")
        .center(-w / 2 + x_offset + element["x"], -h / 2 + y_offset + element["y"])
        .placeSketch(element["shape"])
        .extrude(height)
    )


def punch_hole(*, model, face, w, h, x_offset, y_offset, hole, depth):
    return (
        model.faces(face)
        .workplane(centerOption="CenterOfBoundBox")
        .center(-w / 2 + x_offset + hole["x"], -h / 2 + y_offset + hole["y"])
        .placeSketch(hole["shape"])
        .cutBlind(-depth)
    )


def extrude_shape2(*, model, face, w, h, x_offset, y_offset, hole, depth):
    return (
        model.faces(face)
        .workplane(centerOption="CenterOfBoundBox")
        .center(-w / 2 + x_offset + hole["x"], -h / 2 + y_offset + hole["y"])
        .placeSketch(hole["shape"])
        .extrude(-depth)
    )


def hex_vents(*, size, width, height, density=0.85):
    # size is radius of the hexagon
    # Information about how this works:
    # https://www.redblobgames.com/grids/hexagons/

    x_step = size * (3**0.5)
    y_step = size * 3 / 2

    x_count = floor(width / x_step) - 1

    if height > 4 * size:
        y_count = floor((height - 2 * size) / (1.5 * size))
    else:
        y_count = 1

    x_size = (x_count + 0.5) * x_step  # Assumes at least 2 rows
    y_size = 2 * size + 1.5 * size * (y_count - 1)

    x_offset = (width - x_size) / 2 + 0.5 * x_step
    y_offset = (height - y_size) / 2 + size

    vent_positions = []
    for x in range(0, x_count):
        for y in range(0, y_count):
            vent_positions.append(
                (
                    (x + (y % 2) / 2) * x_step + x_offset,
                    y * y_step + y_offset,
                )
            )
    vents = [
        {
            "x": 0,
            "y": 0,
            "shape": cq.Sketch().push(vent_positions).regularPolygon(size * density, 6),
        }
    ]

    return vents


def export(model, fname, **kwarg):
    tmpfile = tempfile.mktemp(suffix="." + fname.split(".")[-1])
    exporters.export(model, tmpfile, **kwarg)
    shutil.move(tmpfile, fname)

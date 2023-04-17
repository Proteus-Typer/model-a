import cadquery as cq

import base
import simple_lid

base = base.model()
lid = simple_lid.model()
# kbd =

compu = (
    cq.Assembly()
    .add(base, name="base", color=cq.Color("red"))
    .add(lid, name="lid", color=cq.Color("green"))
)

compu.constrain("base@faces@<X", "lid@faces@<X", "Plane", param=0)
# compu.constrain("base@faces@>Y", "lid@faces@>Y", "Plane", param=0)
# compu.constrain("base@faces@>X", "lid@faces@>X", "Plane", param=0)
compu.constrain("base@faces@>Z", "lid?bottom", "Plane")


# def pk(p):
#     c = p.Center()
#     return (c.x, c.y, c.z)


# lid_holes = sorted(
#     [x for x in lid.faces("|Z").edges("%CIRCLE").vals() if x.radius() == 2 and x.Closed()], key=pk
# )
# base_holes = sorted(
#     [x for x in base.faces(">Z").edges("%CIRCLE").vals() if x.radius() == 1.8], key=pk
# )
# print(len(lid_holes), len(base_holes))
# # Holes of diam 2 on the top lid and 1.8 in the base
# for a, b in list(zip(lid_holes, base_holes)):
#     compu.constrain("lid", a, "base", b, "Point")


compu.solve(5)
compu.save("compu.step")

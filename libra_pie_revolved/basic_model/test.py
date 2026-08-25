import openmc
from libra_pie_revolved import build_libra_pie_revolved
import numpy as np

# Salt Material
# lif-licl - natural - pure
cllif_nat = openmc.Material(name='ClLiF')
cllif_nat.add_element('F', .5*.305, 'ao')
cllif_nat.add_element('Li', .5*.305 + .5*.695, 'ao')
cllif_nat.add_element('Cl', .5*.695, 'ao')
cllif_nat.set_density('g/cm3', 1.54)

# Multiplier Material
beryllium = openmc.Material(name="Beryllium")
# Estimate Be temperature to be around 100 C
# Be.temperature = 100 + 273
beryllium.add_element('Be', 1.0, 'ao')
beryllium.set_density('g/cm3', 1.848)

# Reflector Material
# Graphite (reactor-grade) from PNNL Materials Compendium (PNNL-15870 Rev2)
graphite = openmc.Material(name='Graphite')
graphite.set_density('g/cm3', 1.7)
graphite.add_element('B', 0.000001, 'wo')
graphite.add_element('C', 0.999999, 'wo')

translation_vector = [50, 0, 0]

libra_region, libra_system_cell, libra_materials, src = build_libra_pie_revolved(salt_material=cllif_nat,
                                                                            multiplier_material=beryllium,
                                                                            multiplier_thickness=5,
                                                                            reflector_material=graphite,
                                                                            reflector_thickness=1,
                                                                            translation_vector=translation_vector,
                                                                            lead_thickness=2,
                                                                            insulation_thickness=5)

outer_sphere = openmc.Sphere(r=500, 
                             x0=translation_vector[0],
                             y0=translation_vector[1],
                             z0=translation_vector[2],
                             boundary_type='vacuum')
void_reg = -outer_sphere & ~libra_region

print(libra_region)
print(libra_region.bounding_box)
print(void_reg.bounding_box)
print(src.space.xyz)

void_cell = openmc.Cell(region=void_reg, fill=None)

universe = openmc.Universe(cells=[libra_system_cell, void_cell])
geometry = openmc.Geometry(universe)
geometry.remove_redundant_surfaces()

settings = openmc.Settings()
settings.run_mode = 'fixed source'
settings.source = src
settings.batches = 100
settings.inactive = 0
settings.particles = int(1e6)

plot = openmc.Plot.from_geometry(geometry)
plot.pixels = (2000, 2000)
plot.width = [200, 200]
plot.origin = translation_vector
plot.color_by = 'cell'

plot.to_ipython_image()

plot2 = openmc.Plot.from_geometry(geometry)
plot2.pixels = (2000, 4000)
plot2.width = [200, 400]
plot2.basis = 'xz'
plot2.origin = np.array(translation_vector) + np.array([0, 2, 0]) 
plot2.color_by = 'cell'

plot2.to_ipython_image()

model = openmc.Model(geometry=geometry,
                     materials=libra_materials,
                     settings=settings)
model.run()

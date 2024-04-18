import openmc
import vault
import numpy as np

point = openmc.stats.Point((1800, 400, 100))
src = openmc.IndependentSource(space=point)
src.energy = openmc.stats.Discrete([14.1E6], [1.0])
src.strength = 1.0

settings = openmc.Settings()
settings.run_mode = 'fixed source'
settings.source = src
settings.batches = 100
settings.inactive = 0
settings.particles = int(1e5)

water = openmc.Material(name='water')
water.add_element('O', 1/3)
water.add_element('H', 2/3)
water.set_density('g/cc', 1.0)

water_sphere = openmc.Sphere(r=10, 
                             x0=src.space.xyz[0]+100,
                             y0=src.space.xyz[1],
                             z0=src.space.xyz[2])
water_cell = openmc.Cell(region=-water_sphere, fill=water)
overall_exclusion_region = -water_sphere

tally = openmc.Tally()
tally.filters = [openmc.CellFilter(water_cell)]
tally.scores = ['flux']
tallies = openmc.Tallies([tally])

model = vault.build_vault_model(settings=settings,
                                tallies=tallies,
                                added_cells=[water_cell],
                                added_materials=[water],
                                overall_exclusion_region=overall_exclusion_region)
model.run()

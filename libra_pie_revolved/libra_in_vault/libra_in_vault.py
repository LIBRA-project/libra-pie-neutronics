import openmc
import sys
import numpy as np

sys.path.append('../basic_model')
from libra_pie_revolved import build_libra_pie_revolved

sys.path.append('../../vault')
from vault import build_vault_model

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

translation_vector = [1800, 200, 100]

#### Build LIBRA model
libra_region, libra_system_cell, libra_materials, src = build_libra_pie_revolved(salt_material=cllif_nat,
                                                                            multiplier_material=beryllium,
                                                                            multiplier_thickness=5,
                                                                            reflector_material=graphite,
                                                                            reflector_thickness=30,
                                                                            translation_vector=translation_vector)

### Translate LIBRA to appropriate place in Vault
translation_vector = [1800, 200, 100]

####### Add LIBRA to Vault Model

## Settings
settings = openmc.Settings()
settings.run_mode = 'fixed source'
settings.source = src
settings.batches = 100
settings.inactive = 0
settings.particles = int(1e6)

## Tallies
material_filter = openmc.MaterialFilter(cllif_nat)
t_tally = openmc.Tally(name='tritium_tally')
t_tally.filters = [material_filter]
t_tally.scores = ['(n,Xt)']

tallies = openmc.Tallies([t_tally])

test_sphere = openmc.Sphere(x0=1800, y0=300, z0=100, r=10)
test_cell = openmc.Cell(fill=cllif_nat, region=-test_sphere, name='test cell')
exclusion_region = -test_sphere

vault_model = build_vault_model(settings=settings, 
                                tallies=tallies,
                                added_cells=[libra_system_cell],
                                added_materials=libra_materials,
                                overall_exclusion_region=libra_region)

# vault_model = build_vault_model(settings=settings,
#                                 tallies=tallies,
#                                 added_cells=[test_cell],
#                                 added_materials=[cllif_nat],
#                                 overall_exclusion_region=exclusion_region)
vault_model.export_to_model_xml()

vault_model.run(threads=16)







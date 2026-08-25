import openmc

# lif-licl - natural - pure
cllif_nat = openmc.Material(name='ClLiF natural')
cllif_nat.add_element('F', .5*.305, 'ao')
cllif_nat.add_element('Li', .5*.305 + .5*.695, 'ao')
cllif_nat.add_element('Cl', .5*.695, 'ao')
cllif_nat.set_density('g/cm3', 2.242)

li6 = openmc.Material()
li6.add_nuclide('Li6', 1.0, 'wo')
li6.set_density('g/cm3', 2.242*0.5*0.07)

li7 = openmc.Material()
li7.add_nuclide('Li7', 1.0, 'wo')
li7.set_density('g/cm3', 2.242*0.5*0.93)

materials = openmc.Materials([cllif_nat, li6, li7])
materials.export_to_xml()

sphere = openmc.Sphere(r=20, boundary_type='vacuum')
cell = openmc.Cell(region=-sphere, fill=cllif_nat)
universe = openmc.Universe(cells=[cell])
geometry = openmc.Geometry(universe)
geometry.export_to_xml()

point = openmc.stats.Point((0.0, 0.0, 0.0))
src = openmc.IndependentSource(space=point)
src.energy = openmc.stats.Discrete([14.1E6], [1.0])
src.strength = 1.0

settings = openmc.Settings()
settings.run_mode = 'fixed source'
settings.source = src
settings.batches = 100
settings.inactive = 0
settings.particles = int(5e5)
# settings.photon_transport = True
settings.photon_transport = False
settings.export_to_xml()

cllif_mat_filter = openmc.MaterialFilter(cllif_nat)
li6_filter = openmc.MaterialFilter(li6)
li7_filter = openmc.MaterialFilter(li7)

tally_cllif = openmc.Tally()
tally_cllif.filters.append(cllif_mat_filter)
tally_cllif.nuclides = ['Li6', 'Li7']
tally_cllif.scores = ['(n,Xt)']

tally_li6 = openmc.Tally()
tally_li6.filters.append(li6_filter)
tally_li6.scores = ['(n,Xt)']

tally_li7 = openmc.Tally()
tally_li7.filters.append(li7_filter)
tally_li7.scores = ['(n,Xt)']

tallies = openmc.Tallies([tally_cllif, tally_li6, tally_li7])
tallies.export_to_xml()

openmc.run()

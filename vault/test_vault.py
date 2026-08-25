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
water_cell = openmc.Cell(region=-water_sphere, fill=water, name='Water sphere')
overall_exclusion_region = -water_sphere

### Tallies
mesh = openmc.RegularMesh()
mesh.dimension = (120, 80, 37)
mesh.lower_left = (0, -500, 0)
mesh.upper_right = (2400, 1100, 740)
mesh_vol = np.prod(mesh.width)
mesh_filter = openmc.MeshFilter(mesh)

dose_n_energies, dose_n_coeffs = openmc.data.dose_coefficients('neutron')
# Get rid of coefficients for energies above 15 MeV
n_mask = dose_n_energies<1.6e7
dose_n_energies = dose_n_energies[n_mask]
dose_n_coeffs = dose_n_coeffs[n_mask]
tally_n_energies = [0] + list(dose_n_energies)
energy_n_filter = openmc.EnergyFilter(tally_n_energies)

dose_p_energies, dose_p_coeffs = openmc.data.dose_coefficients('photon')
# Get rid of coefficients for energies above 20 MeV
p_mask = dose_p_energies <= 2.0e7
dose_p_energies = dose_p_energies[p_mask]
dose_p_coeffs = dose_p_coeffs[p_mask]
# print(dose_p_energies)
tally_p_energies = [0] + list(dose_p_energies)
energy_p_filter = openmc.EnergyFilter(tally_p_energies)

neutron_filter = openmc.ParticleFilter('neutron')
photon_filter = openmc.ParticleFilter('photon')

neutron_tally = openmc.Tally(tally_id=1)
neutron_tally.filters.append(mesh_filter)
neutron_tally.filters.append(energy_n_filter)
# neutron_tally.filters.append(energy_n_easy_filter)
neutron_tally.filters.append(neutron_filter)
neutron_tally.scores = ['flux']

photon_tally = openmc.Tally(tally_id=2)
photon_tally.filters.append(mesh_filter)
photon_tally.filters.append(energy_p_filter)
photon_tally.filters.append(photon_filter)
photon_tally.scores = ['flux']


tally = openmc.Tally()
tally.filters = [openmc.CellFilter(water_cell)]
tally.scores = ['flux']
tallies = openmc.Tallies([neutron_tally, photon_tally])


plots = openmc.Plots()
model = vault.build_vault_model(settings=settings,
                                tallies=tallies,
                                added_cells=[water_cell],
                                added_materials=[water],
                                overall_exclusion_region=overall_exclusion_region,
                                plots=plots)

model.export_to_model_xml()
model.run(geometry_debug=False, threads=12)

import openmc
import numpy as np
from matplotlib import pyplot as plt

# model_directory = 'libra_pie_2'
# salts = ['Flibe_nat', 'ClLiF natural']
salts = ['ClLiF natural']
reflectors = ['Graphite', 'Beryllium', 'Lead', 'HDPE',
                'Stainless Steel 304', 'SteelLowC', 'Tungsten']
reflector_thicknesses = [0.0, 2.0, 4.0, 6.0, 8.0]
tbrs = {}

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[12, 8])
for salt in salts:
    tbrs[salt] = {}
    for reflector in reflectors:
        tbrs[salt][reflector] = np.zeros((len(reflector_thicknesses),2))
        for i,thickness in enumerate(reflector_thicknesses):
                directory = '{}/{}_{}cm'.format(salt, reflector, thickness)
                settings = openmc.Settings.from_xml('{}/settings.xml'.format(directory))
                source_strength = settings.source[0].strength
                sp = openmc.StatePoint('{}/statepoint.100.h5'.format(directory))
                t_tally = sp.get_tally(name='tritium tally')
                tbrs[salt][reflector][i,0] = t_tally.get_reshaped_data(value='mean').squeeze()/source_strength
                tbrs[salt][reflector][i,1] = t_tally.get_reshaped_data(value='std_dev').squeeze()/source_strength
        ax.errorbar(reflector_thicknesses, tbrs[salt][reflector][:,0], tbrs[salt][reflector][:,1],
            fmt='.-', label='Salt:{} Refl:{}'.format(salt, reflector))
ax.set_xlabel('Back Reflector Thickness')
ax.set_ylabel('TBR')
ax.legend()

plt.show()
fig.savefig('libra_pie_back_refl_scan.png', dpi=200)



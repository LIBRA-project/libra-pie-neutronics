import openmc
import numpy as np
from matplotlib import pyplot as plt

# model_directory = 'libra_pie_2'
# salts = ['Flibe_nat', 'ClLiF natural']
salts = ['ClLiF natural']
reflectors = ['Graphite', 'Beryllium', 'Lead', 'Firebrick', 'HDPE',
                'Stainless Steel 304', 'SteelLowC', 'Zirconia', 'Tungsten']
reflector_thicknesses = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
tbrs = {}

colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red',
        'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
        'tab:olive', 'tab:cyan']

fig_tot, ax_tot = plt.subplots(nrows=1, ncols=1, figsize=[12, 8])
fig_li6, ax_li6 = plt.subplots(nrows=1, ncols=1, figsize=[12, 8])
fig_li7, ax_li7 = plt.subplots(nrows=1, ncols=1, figsize=[12, 8])
max_tbr = 0.0
for salt in salts:
    tbrs[salt] = {}
    for j,reflector in enumerate(reflectors):
        tbrs[salt][reflector] = {}
        tbrs[salt][reflector]['total'] = np.zeros((len(reflector_thicknesses),2))
        tbrs[salt][reflector]['Li6'] = np.zeros((len(reflector_thicknesses),2))
        tbrs[salt][reflector]['Li7'] = np.zeros((len(reflector_thicknesses),2))
        for i,thickness in enumerate(reflector_thicknesses):
                directory = '{}/{}_{}cm'.format(salt, reflector, thickness)
                settings = openmc.Settings.from_xml('{}/settings.xml'.format(directory))
                source_strength = settings.source[0].strength
                sp = openmc.StatePoint('{}/statepoint.100.h5'.format(directory))
                t_tally = sp.get_tally(name='tritium tally')
                tbrs[salt][reflector]['total'][i,0] = t_tally.get_reshaped_data(value='mean').squeeze()/source_strength
                tbrs[salt][reflector]['total'][i,1] = t_tally.get_reshaped_data(value='std_dev').squeeze()/source_strength
                if tbrs[salt][reflector]['total'][i,0] > max_tbr:
                    max_tbr = tbrs[salt][reflector]['total'][i,0]
                t_li_tally = sp.get_tally(name='tritium lithium tally')
                t_li_mean = t_li_tally.get_reshaped_data(value='mean').squeeze()/source_strength
                # print(t_li_mean)
                t_li_err = t_li_tally.get_reshaped_data(value='std_dev').squeeze()/source_strength
                tbrs[salt][reflector]['Li6'][i,0] = t_li_mean[0]
                tbrs[salt][reflector]['Li6'][i,1] = t_li_err[0]
                tbrs[salt][reflector]['Li7'][i,0] = t_li_mean[1]
                tbrs[salt][reflector]['Li7'][i,1] = t_li_err[1]
        ax_tot.errorbar(reflector_thicknesses, tbrs[salt][reflector]['total'][:,0], tbrs[salt][reflector]['total'][:,1],
            fmt='.-', color=colors[j], label='Refl:{}'.format(reflector))
        ax_li6.errorbar(reflector_thicknesses, tbrs[salt][reflector]['Li6'][:,0], tbrs[salt][reflector]['Li6'][:,1],
            fmt='.-', color=colors[j], label='Refl:{}'.format(reflector))
        ax_li7.errorbar(reflector_thicknesses, tbrs[salt][reflector]['Li7'][:,0], tbrs[salt][reflector]['Li7'][:,1],
            fmt='.-', color=colors[j], label='Refl:{}'.format(reflector))
ax_tot.set_xlabel('Reflector Thickness')
ax_tot.set_ylabel('TBR')
ax_tot.set_title('Total Tritium Production')
ax_tot.set_ylim(0.005, max_tbr*1.05)
ax_tot.legend()
fig_tot.savefig('libra_pie_reflector_scan_total.png', dpi=200)

ax_li6.set_xlabel('Reflector Thickness')
ax_li6.set_ylabel('TBR')
ax_li6.set_title('Li-6 Tritium Production')
ax_li6.legend()
ax_li6.set_ylim(0.005, max_tbr*1.05)
fig_li6.savefig('libra_pie_reflector_scan_li6.png', dpi=200)

ax_li7.set_xlabel('Reflector Thickness')
ax_li7.set_ylabel('TBR')
ax_li7.set_title('Li-7 Tritium Production')
ax_li7.legend()
ax_li7.set_ylim(0.005, max_tbr*1.05)
fig_li7.savefig('libra_pie_reflector_scan_li7.png', dpi=200)

plt.show()




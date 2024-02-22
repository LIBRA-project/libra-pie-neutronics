import openmc
import numpy as np
from matplotlib import pyplot as plt
from libra_pie_27sep2023 import *
import pandas as pd
import matplotx

salts = ['Flibe_nat', 'ClLiF natural']
multipliers = ['Beryllium', 'Lead']
multiplier_thicknesses = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
tbrs = {}
currents = {}

colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red',
        'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
        'tab:olive', 'tab:cyan']


fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[12, 8])
fig2, ax2 = plt.subplots(nrows=1, ncols=1, figsize=[12, 8])
for j,salt in enumerate(salts):
    tbrs[salt] = {}
    currents[salt] = {}
    for k,multiplier in enumerate(multipliers):
        tbrs[salt][multiplier] = np.zeros((len(multiplier_thicknesses),2))
        currents[salt][multiplier] = np.zeros((len(multiplier_thicknesses),2))
        for i,thickness in enumerate(multiplier_thicknesses):
                directory = '{}/{}_{}cm'.format(salt, multiplier, thickness)
                sp = openmc.StatePoint('{}/statepoint.100.h5'.format(directory))
                t_tally = sp.get_tally(name='tritium tally')
                tbrs[salt][multiplier][i,0] = t_tally.get_reshaped_data(value='mean').squeeze()/src.strength
                tbrs[salt][multiplier][i,1] = t_tally.get_reshaped_data(value='std_dev').squeeze()/src.strength

                curr_tally = sp.get_tally(name='current tally')
                curr = curr_tally.get_pandas_dataframe()
                # Get incoming current towards the quarter sector (0, pi/2)
                # print(curr)
                currents[salt][multiplier][i,0] = curr['mean'].loc[1]
                # Get incoming current away from the quarter sector (pi/2, 2pi)
                currents[salt][multiplier][i,1] = curr['mean'].loc[13]
        ax.errorbar(multiplier_thicknesses, tbrs[salt][multiplier][:,0], tbrs[salt][multiplier][:,1],
            fmt='.-', label='Salt:{} Mult:{}'.format(salt, multiplier))
        ax2.plot(multiplier_thicknesses, currents[salt][multiplier][:,0] / (np.pi/2), 
            '.-', color=colors[len(multipliers)*j + k], label='{} {} [0,90]'.format(salt, multiplier))
        ax2.plot(multiplier_thicknesses, currents[salt][multiplier][:,1] / (3*np.pi/2), 
            '^--', color=colors[len(multipliers)*j + k], label='{} {} [90,360]'.format(salt,multiplier))
ax.set_xlabel('Multiplier Thickness [cm]')
ax.set_ylabel('TBR')
ax.legend()
fig.savefig('libra_pie_multiplier_scan.png', dpi=200)

ax2.set_xlabel('Multiplier Thickness [cm]')
ax2.set_ylabel('Current per Radian [n/s]')
# ax2.legend()
matplotx.line_labels(ax=ax2)
ax2.spines.right.set_visible(False)
ax2.spines.top.set_visible(False)
fig2.tight_layout()
fig2.savefig('libra_pie_mult_curr_scan.png', dpi=200)

plt.show()
fig.savefig('libra_pie_multiplier_scan.png', dpi=200)



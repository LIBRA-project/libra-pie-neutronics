import openmc
from matplotlib import pyplot as plt
import numpy as np
import os
from glob import glob

salt_directory = 'Flibe_nat'


directories = glob('{}/*/'.format(salt_directory), recursive=True)

data = {}
for directory in directories:
    reflector_dir = directory.split('/')[1]
    dir_split = reflector_dir.split('_')
    # print(dir_split)

    thickness = float(dir_split[-1][:-2])
    label = " ".join(dir_split[:-1])

    sp = openmc.StatePoint('{}statepoint.100.h5'.format(directory))
    t_tally = sp.get_tally(name='tritium tally')
    tbr = np.sum(t_tally.get_reshaped_data(value='mean').squeeze())

    if label in data.keys():
        data[label] += [[thickness, tbr]]
    else:
        data[label] = [[thickness, tbr]]

fig, ax = plt.subplots()
for label in data.keys():
    data[label] = np.array(data[label])
    sort_ind = data[label][:,0].argsort()
    data[label] = data[label][sort_ind,:]
    print(data[label])
    ax.plot(data[label][:,0], data[label][:,1], '.-', label=label)
ax.set_xlabel('Reflector Thickness [cm]')
ax.set_ylabel('TBR')
ax.set_title(salt_directory)
ax.legend()

fig.tight_layout()
fig.savefig('{}_reflector_scan.png'.format(salt_directory))

plt.show()


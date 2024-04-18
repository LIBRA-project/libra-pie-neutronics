#Vault Model

## vault.py
Module with one function, build_vault_model(), which creates an OpenMC model of the NW13 Vault at MIT and its surroundings
including the control room, the maze, storage areas, the outside soil, and the floor and ceiling of the floor above the Vault lab. Some port and ventilation holes are missing in this model. This function also allows one to add geometry into
the vault room easily.

## test_vault.py
A very basic example of the utilization of the build_vault_model() function with a water sphere placed inside the Vault room.


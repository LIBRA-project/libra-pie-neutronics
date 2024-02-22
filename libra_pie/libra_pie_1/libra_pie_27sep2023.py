import numpy as np
import openmc
import os

multiplier_thicknesses = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
# multiplier_thicknesses = [0.0]
###### Materials ############################

# Source: PNNL Materials Compendium April 2021
# PNNL-15870, Rev. 2
inconel625 = openmc.Material(name='Inconel 625')
inconel625.set_density('g/cm3', 8.44)
inconel625.add_element('C',  0.000990, 'wo')
inconel625.add_element('Al', 0.003960, 'wo')
inconel625.add_element('Si', 0.004950, 'wo')
inconel625.add_element('P',  0.000148, 'wo')
inconel625.add_element('S',  0.000148, 'wo')
inconel625.add_element('Ti', 0.003960, 'wo')
inconel625.add_element('Cr', 0.215000, 'wo')
inconel625.add_element('Mn', 0.004950, 'wo')
inconel625.add_element('Fe', 0.049495, 'wo')
inconel625.add_element('Co', 0.009899, 'wo')
inconel625.add_element('Ni', 0.580000, 'wo')
inconel625.add_element('Nb', 0.036500, 'wo')
inconel625.add_element('Mo', 0.090000, 'wo')

# Using 2:1 atom ratio of LiF to BeF2, similar to values in 
# Seifried, Jeffrey E., et al. ‘A General Approach for Determination of 
# Acceptable FLiBe Impurity Concentrations in Fluoride-Salt Cooled High 
# Temperature Reactors (FHRs)’. Nuclear Engineering and Design, vol. 343, 2019, 
# pp. 85–95, https://doi.org10.1016/j.nucengdes.2018.09.038.
# Also using natural lithium enrichment (~7.5 a% Li6)
flibe_nat = openmc.Material(name='Flibe_nat')
# Flibe_nat.temperature = 700 + 273
flibe_nat.add_element('Be', 0.142857, 'ao')
flibe_nat.add_nuclide('Li6', 0.021685, 'ao')
flibe_nat.add_nuclide('Li7', 0.264029, 'ao')
flibe_nat.add_element('F', 0.571429, 'ao')
flibe_nat.set_density("g/cm3", 1.94)

# lif-licl - natural - pure
cllif_nat = openmc.Material(name='ClLiF natural')
cllif_nat.add_element('F', .5*.305, 'ao')
cllif_nat.add_element('Li', .5*.305 + .5*.695, 'ao')
cllif_nat.add_element('Cl', .5*.695, 'ao')
cllif_nat.set_density('g/cm3', 2.242)

air = openmc.Material(name="Air")
air.add_element("C", 0.00012399 , 'wo')
air.add_element('N', 0.75527, 'wo')
air.add_element('O', 0.23178, 'wo')
air.add_element('Ar', 0.012827, 'wo')
air.set_density('g/cm3', 0.0012)

beryllium = openmc.Material(name="Beryllium")
# Estimate Be temperature to be around 100 C
# Be.temperature = 100 + 273
beryllium.add_element('Be', 1.0, 'ao')
beryllium.set_density('g/cm3', 1.848)

lead = openmc.Material(name="Lead")
lead.add_element('Pb', 1.0,"ao")
lead.set_density("g/cm3", 11.34)

salt_materials = [flibe_nat, cllif_nat]
multiplier_materials = [lead, beryllium]

materials = openmc.Materials([
                            inconel625,
                            flibe_nat,
                            cllif_nat,
                            air,
                            beryllium,
                            lead
                            ])

############### Geometry ###################################
wall_thickness = 0.3175 # 1/8 inch
gap_thickness = 0.635 # 1/4 inch
salt_headspace = 7.28*2.54
multiplier_height = 10.0

######## Surfaces #################

# Tank double wall surfaces
inner_cyl_1 = openmc.ZCylinder(r=13.34)
inner_cyl_2 = openmc.ZCylinder(r=13.97)
inner_cyl_3 = openmc.ZCylinder(r=14.61)
inner_cyl_4 = openmc.ZCylinder(r=15.24)

x_plane_1 = openmc.XPlane(0.0)
x_plane_2 = openmc.XPlane(wall_thickness)
x_plane_3 = openmc.XPlane(wall_thickness + gap_thickness)
x_plane_4 = openmc.XPlane(2*wall_thickness + gap_thickness)

y_plane_1 = openmc.YPlane(0.0)
y_plane_2 = openmc.YPlane(wall_thickness)
y_plane_3 = openmc.YPlane(wall_thickness + gap_thickness)
y_plane_4 = openmc.YPlane(2*wall_thickness + gap_thickness)

outer_cyl_1 = openmc.ZCylinder(r=43.50)
outer_cyl_2 = openmc.ZCylinder(r=43.82)
outer_cyl_3 = openmc.ZCylinder(r=44.45)
outer_cyl_4 = openmc.ZCylinder(r=44.77)

z_plane_1 = openmc.ZPlane(0.0)
z_plane_2 = openmc.ZPlane(wall_thickness)
z_plane_3 = openmc.ZPlane(wall_thickness + gap_thickness)
z_plane_4 = openmc.ZPlane(2*wall_thickness + gap_thickness)

double_wall_top_plane_1 = openmc.ZPlane(117.89)
double_wall_top_plane_2 = openmc.ZPlane(117.89 + 0.89)


## Tank top cover surfaces
tank_top_cover_plane_1 = openmc.ZPlane(112.71 + z_plane_4.z0)
tank_top_cover_plane_2 = openmc.ZPlane(tank_top_cover_plane_1.z0 + wall_thickness*2)



### Heater reentrant tube surfaces

# theta measured going counterclockwise from y=0 plane
# heater_reentrant_1 center: theta = 20 degrees
# heater_reentrant_2 center: theta = 45 degrees
# heater_reentrant_3 center: theta = 70 degrees

heater_reentrant_1_in_cyl = openmc.ZCylinder(r=2.34, 
                                            x0=30.73, 
                                            y0=np.sqrt(32.70**2 - 30.73**2))
heater_reentrant_1_out_cyl = openmc.ZCylinder(r=2.54,
                                            x0=heater_reentrant_1_in_cyl.x0,
                                            y0=heater_reentrant_1_in_cyl.y0)

heater_reentrant_2_in_cyl = openmc.ZCylinder(r=2.34, 
                                            x0=23.12, 
                                            y0=np.sqrt(32.70**2 - 23.12**2))
heater_reentrant_2_out_cyl = openmc.ZCylinder(r=2.54,
                                            x0=heater_reentrant_2_in_cyl.x0,
                                            y0=heater_reentrant_2_in_cyl.y0)

heater_reentrant_3_in_cyl = openmc.ZCylinder(r=2.34, 
                                            x0=np.sqrt(32.70**2 - 30.73**2), 
                                            y0=30.73)
heater_reentrant_3_out_cyl = openmc.ZCylinder(r=2.54,
                                            x0=heater_reentrant_3_in_cyl.x0,
                                            y0=heater_reentrant_3_in_cyl.y0)
heater_reentrant_bot_plane_1 = openmc.ZPlane(25.60)
heater_reentrant_bot_plane_2 = openmc.ZPlane(25.80)

heater_reentrant_top_plane = openmc.ZPlane(tank_top_cover_plane_1.z0 + \
                                            6.72)

## Fill Tube
fill_tube_cyl_1 = openmc.ZCylinder(r=2.34, 
                                   x0=np.sqrt(20.32**2 - 14.37**2),
                                   y0=14.37)
fill_tube_cyl_2 = openmc.ZCylinder(r=2.54,
                                   x0=np.sqrt(20.32**2 - 14.37**2),
                                   y0=14.37)
fill_tube_top_plane = openmc.ZPlane(tank_top_cover_plane_1.z0 + 10.16)

## Gas tubes entering the inner tank (for salt tritium removal)

# Gas Tube 1: theta = 20 degrees
salt_gas_tube_1_cyl_1 = openmc.ZCylinder(r=1.06,
                                         x0=np.sqrt(23.18**2 - 7.93),
                                         y0=7.93)
salt_gas_tube_1_cyl_2 = openmc.ZCylinder(r=1.27,
                                         x0=np.sqrt(23.18**2 - 7.93),
                                         y0=7.93)
# Gas Tube 2: theta = 70 degrees
salt_gas_tube_2_cyl_1 = openmc.ZCylinder(r=1.06,
                                         x0=7.93,
                                         y0=np.sqrt(23.18**2 - 7.93))
salt_gas_tube_2_cyl_2 = openmc.ZCylinder(r=1.27,
                                         x0=7.93,
                                         y0=np.sqrt(23.18**2 - 7.93))

salt_gas_tube_top_plane = openmc.ZPlane(tank_top_cover_plane_1.z0 + 25.40)

## Thermocouple tubes
# thermocouple tube 3: theta = 70 degrees
thermocouple_tube_3_cyl_1 = openmc.ZCylinder(r=0.31,
                                            x0=13.68,
                                            y0=37.59)
thermocouple_tube_3_cyl_2 = openmc.ZCylinder(r=0.48,
                                            x0=13.68,
                                            y0=37.59)

# thermocouple tube 2: theta = 45 degrees
thermocouple_tube_2_cyl_1 = openmc.ZCylinder(r=0.31,
                                            x0=28.29,
                                            y0=28.29)
thermocouple_tube_2_cyl_2 = openmc.ZCylinder(r=0.48,
                                            x0=28.29,
                                            y0=28.29)

# thermocouple tube 1: theta = 70 degrees
thermocouple_tube_1_cyl_1 = openmc.ZCylinder(r=0.31,
                                            x0=37.59,
                                            y0=13.68)
thermocouple_tube_1_cyl_2 = openmc.ZCylinder(r=0.48,
                                            x0=37.59,
                                            y0=13.68)

thermocouple_tube_top_plane = openmc.ZPlane(tank_top_cover_plane_1.z0 + 12.70)

## salt surface:
salt_top_plane = openmc.ZPlane(tank_top_cover_plane_1.z0 - salt_headspace)

# multiplier surfaces
source_z_point = (z_plane_4.z0 + salt_top_plane.z0) / 2

multiplier_bot_plane = openmc.ZPlane(source_z_point - multiplier_height/2)
multiplier_top_plane = openmc.ZPlane(source_z_point + multiplier_height/2)

# print(multiplier_cyl)
# print(inner_cyl_1)
## Void surfaces:

void_bot_plane = openmc.ZPlane(-50.0, boundary_type='vacuum')
void_top_plane = openmc.ZPlane(salt_gas_tube_top_plane.z0 + 50.0, boundary_type='vacuum')
void_cyl = openmc.ZCylinder(r=outer_cyl_4.r+50, boundary_type='vacuum')

####### Regions and Cells ###############

## Outer tank wall
# Inner region
out_wall_reg_1 = +inner_cyl_1 & -inner_cyl_2 \
                & +y_plane_2 & +x_plane_2 \
                & +z_plane_1 & -double_wall_top_plane_1
# horizontal region
out_wall_reg_hor = +y_plane_1 & -y_plane_2 \
                & +inner_cyl_1 & -outer_cyl_4 & +x_plane_1 \
                & +z_plane_1 & -double_wall_top_plane_1
# vertical region
out_wall_reg_ver = +x_plane_1 & -x_plane_2 \
                & +inner_cyl_1 & -outer_cyl_4 & +y_plane_1 \
                & +z_plane_1 & -double_wall_top_plane_1
# outer region
out_wall_reg_2 = +outer_cyl_3 & -outer_cyl_4 \
                & +y_plane_2 & +x_plane_2 \
                & +z_plane_1 & -double_wall_top_plane_1
# bottom region
out_wall_reg_bot = +z_plane_1 & -z_plane_2 \
                    & +inner_cyl_2 & -outer_cyl_3 \
                    & +y_plane_2 & +x_plane_2
# overall region
out_wall_reg = out_wall_reg_1 | out_wall_reg_hor | out_wall_reg_ver \
                | out_wall_reg_2 | out_wall_reg_bot

out_wall_cell = openmc.Cell(region=out_wall_reg, fill=inconel625, name='tank outer wall')

## Tank wall gap 
# Inner region
wall_gap_reg_1 = +inner_cyl_2 & -inner_cyl_3 \
                & +y_plane_3 & +x_plane_3 \
                & +z_plane_2 & -double_wall_top_plane_1
# horizontal region
wall_gap_reg_hor = +y_plane_2 & -y_plane_3 \
                & +inner_cyl_2 & -outer_cyl_3 & +x_plane_1 \
                & +z_plane_2 & -double_wall_top_plane_1
# vertical region
wall_gap_reg_ver = +x_plane_2 & -x_plane_3 \
                & +inner_cyl_2 & -outer_cyl_3 & +y_plane_1 \
                & +z_plane_2 & -double_wall_top_plane_1
# outer region
wall_gap_reg_2 = +outer_cyl_2 & -outer_cyl_3 \
                & +y_plane_3 & +x_plane_3 \
                & +z_plane_2 & -double_wall_top_plane_1
# bottom region
wall_gap_reg_bot = +z_plane_2 & -z_plane_3 \
                    & +inner_cyl_3 & -outer_cyl_2 \
                    & +y_plane_2 & +x_plane_2
# overall region
wall_gap_reg = wall_gap_reg_1 | wall_gap_reg_hor | wall_gap_reg_ver \
                | wall_gap_reg_2 | wall_gap_reg_bot
wall_gap_cell = openmc.Cell(region=wall_gap_reg, fill=air, name='tank wall gap')

## Inner tank wall 
# Inner region
inner_wall_reg_1 = +inner_cyl_3 & -inner_cyl_4 \
                & +y_plane_4 & +x_plane_4 \
                & +z_plane_3 & -double_wall_top_plane_1
# horizontal region
inner_wall_reg_hor = +y_plane_3 & -y_plane_4 \
                & +inner_cyl_3 & -outer_cyl_2 & +x_plane_1 \
                & +z_plane_3 & -double_wall_top_plane_1
# vertical region
inner_wall_reg_ver = +x_plane_3 & -x_plane_4 \
                & +inner_cyl_3 & -outer_cyl_2 & +y_plane_1 \
                & +z_plane_3 & -double_wall_top_plane_1
# outer region
inner_wall_reg_2 = +outer_cyl_1 & -outer_cyl_2 \
                & +y_plane_3 & +x_plane_3 \
                & +z_plane_3 & -double_wall_top_plane_1
# bottom region
inner_wall_reg_bot = +z_plane_3 & -z_plane_4 \
                    & +inner_cyl_4 & -outer_cyl_1 \
                    & +y_plane_2 & +x_plane_2
# overall region
inner_wall_reg = inner_wall_reg_1 | inner_wall_reg_hor \
                | inner_wall_reg_ver | inner_wall_reg_2 | inner_wall_reg_bot
inner_wall_cell = openmc.Cell(region=inner_wall_reg, fill=inconel625, name='tank inner wall')


## heater reentrant tubes
heater_reentrant_1_reg = (+heater_reentrant_1_in_cyl & -heater_reentrant_1_out_cyl \
                        & -heater_reentrant_top_plane & +heater_reentrant_bot_plane_2) \
                        | (-heater_reentrant_1_out_cyl \
                            & +heater_reentrant_bot_plane_1 & -heater_reentrant_bot_plane_2)
heater_reentrant_1_cell = openmc.Cell(region=heater_reentrant_1_reg, fill=inconel625,
                                        name='Heater Reentrant Tube 1')
heater_fill_1_reg = -heater_reentrant_1_in_cyl & -heater_reentrant_top_plane & +heater_reentrant_bot_plane_2
heater_fill_1_cell = openmc.Cell(region=heater_fill_1_reg, fill=air, name='Heater 1') 

heater_overall_1_reg = -heater_reentrant_1_out_cyl & +heater_reentrant_bot_plane_1 & -heater_reentrant_top_plane

heater_reentrant_2_reg = (+heater_reentrant_2_in_cyl & -heater_reentrant_2_out_cyl \
                        & -heater_reentrant_top_plane & +heater_reentrant_bot_plane_2) \
                        | (-heater_reentrant_2_out_cyl \
                            & +heater_reentrant_bot_plane_1 & -heater_reentrant_bot_plane_2)
heater_reentrant_2_cell = openmc.Cell(region=heater_reentrant_2_reg, fill=inconel625,
                                        name='Heater Reentrant Tube 2')
heater_fill_2_reg = -heater_reentrant_2_in_cyl & -heater_reentrant_top_plane & +heater_reentrant_bot_plane_2
heater_fill_2_cell = openmc.Cell(region=heater_fill_2_reg, fill=air, name='Heater 2')

heater_overall_2_reg = -heater_reentrant_2_out_cyl & +heater_reentrant_bot_plane_1 & -heater_reentrant_top_plane

heater_reentrant_3_reg = (+heater_reentrant_3_in_cyl & -heater_reentrant_3_out_cyl \
                        & -heater_reentrant_top_plane & +heater_reentrant_bot_plane_2) \
                        | (-heater_reentrant_3_out_cyl \
                            & +heater_reentrant_bot_plane_1 & -heater_reentrant_bot_plane_2)
heater_reentrant_3_cell = openmc.Cell(region=heater_reentrant_3_reg, fill=inconel625,
                                        name='Heater Reentrant Tube 3')
heater_fill_3_reg = -heater_reentrant_3_in_cyl & -heater_reentrant_top_plane & +heater_reentrant_bot_plane_2
heater_fill_3_cell = openmc.Cell(region=heater_fill_3_reg, fill=air, name='Heater 3') 

heater_overall_3_reg = -heater_reentrant_3_out_cyl & +heater_reentrant_bot_plane_1 & -heater_reentrant_top_plane
heater_overall_3_vol = np.pi * heater_reentrant_3_out_cyl.r**2 * (heater_reentrant_top_plane.z0 - heater_reentrant_bot_plane_1.z0)

## fill tube
fill_tube_reg = +fill_tube_cyl_1 & -fill_tube_cyl_2 \
                & +tank_top_cover_plane_1 & -fill_tube_top_plane
fill_tube_cell = openmc.Cell(region=fill_tube_reg, fill=inconel625,
                            name='fill tube')

## Salt Gas Tubes
salt_gas_tube_1_reg = +salt_gas_tube_1_cyl_1 & -salt_gas_tube_1_cyl_2 \
                    & +tank_top_cover_plane_1 & -salt_gas_tube_top_plane
salt_gas_tube_1_cell = openmc.Cell(region=salt_gas_tube_1_reg, fill=inconel625,
                                    name='Salt Gas Tube 1')

salt_gas_tube_2_reg = +salt_gas_tube_2_cyl_1 & -salt_gas_tube_2_cyl_2 \
                    & +tank_top_cover_plane_1 & -salt_gas_tube_top_plane
salt_gas_tube_2_cell = openmc.Cell(region=salt_gas_tube_2_reg, fill=inconel625,
                                    name='Salt Gas Tube 2')

## thermocouple tubes
thermocouple_tube_1_reg = +thermocouple_tube_1_cyl_1 & -thermocouple_tube_1_cyl_2 \
                        & +tank_top_cover_plane_1 & -thermocouple_tube_top_plane
thermocouple_tube_1_cell = openmc.Cell(region=thermocouple_tube_1_reg, fill=inconel625,
                                    name='Thermcouple Tube 1')

thermocouple_tube_2_reg = +thermocouple_tube_2_cyl_1 & -thermocouple_tube_2_cyl_2 \
                        & +tank_top_cover_plane_1 & -thermocouple_tube_top_plane
thermocouple_tube_2_cell = openmc.Cell(region=thermocouple_tube_2_reg, fill=inconel625,
                                    name='Thermcouple Tube 2')

thermocouple_tube_3_reg = +thermocouple_tube_3_cyl_1 & -thermocouple_tube_3_cyl_2 \
                        & +tank_top_cover_plane_1 & -thermocouple_tube_top_plane
thermocouple_tube_3_cell = openmc.Cell(region=thermocouple_tube_3_reg, fill=inconel625,
                                    name='Thermcouple Tube 3')

## Inner tank top cover
inner_tank_cover_reg = +tank_top_cover_plane_1 & -tank_top_cover_plane_2 \
                        & +x_plane_4 & +y_plane_4 & +inner_cyl_4 & -outer_cyl_1 \
                        & +heater_reentrant_1_out_cyl & +heater_reentrant_2_out_cyl \
                        & +heater_reentrant_3_out_cyl \
                        & +fill_tube_cyl_2 \
                        & +salt_gas_tube_1_cyl_2 & +salt_gas_tube_2_cyl_2 \
                        & +thermocouple_tube_1_cyl_2 & +thermocouple_tube_2_cyl_2 \
                        & +thermocouple_tube_3_cyl_2
inner_tank_cover_cell = openmc.Cell(region=inner_tank_cover_reg, fill=inconel625,
                                    name='Inner Tank Top Cover')

## Outer tank top cover
# Inner region
outer_tank_cover_reg_1 = +inner_cyl_1 & -inner_cyl_4 \
                & +y_plane_4 & +x_plane_4 \
                & +double_wall_top_plane_1 & -double_wall_top_plane_2
# horizontal region
outer_tank_cover_reg_hor = +y_plane_1 & -y_plane_4 \
                & +inner_cyl_1 & -outer_cyl_4 & +x_plane_1 \
                & +double_wall_top_plane_1 & -double_wall_top_plane_2
# vertical region
outer_tank_cover_reg_ver = +x_plane_1 & -x_plane_4 \
                & +inner_cyl_1 & -outer_cyl_4 & +y_plane_1 \
                & +double_wall_top_plane_1 & -double_wall_top_plane_2
# outer region
outer_tank_cover_reg_2 = +outer_cyl_1 & -outer_cyl_4 \
                & +y_plane_4 & +x_plane_4 \
                & +double_wall_top_plane_1 & -double_wall_top_plane_2

outer_tank_cover_reg = outer_tank_cover_reg_1 | outer_tank_cover_reg_hor \
                    | outer_tank_cover_reg_ver | outer_tank_cover_reg_2
outer_tank_cover_cell = openmc.Cell(region=outer_tank_cover_reg, fill=inconel625,
                                    name='Outer Tank Top Cover')

salt_height = salt_top_plane.z0 - z_plane_4.z0
salt_vol = np.pi / 4 * salt_height * (outer_cyl_1.r**2 - inner_cyl_4.r**2) \
            - 3 * heater_overall_3_vol
print(salt_vol)
for salt_material in salt_materials:
    ## Salt region and cell
    salt_reg = +inner_cyl_4 & -outer_cyl_1 & +x_plane_4 & +y_plane_4 \
                & +z_plane_4 & -salt_top_plane \
                & ~heater_overall_1_reg & ~heater_overall_2_reg \
                & ~heater_overall_3_reg
    salt_cell = openmc.Cell(region=salt_reg, fill=salt_material, name='Salt')

    ## Inner tank air
    inner_tank_air_reg = +inner_cyl_4 & -outer_cyl_1 & +x_plane_4 & +y_plane_4 \
                & +salt_top_plane & -tank_top_cover_plane_1 \
                & ~heater_overall_1_reg & ~heater_overall_2_reg \
                & ~heater_overall_3_reg
    inner_tank_air_cell = openmc.Cell(region=inner_tank_air_reg, fill=air, name='Inner Tank Headspace')

    for multiplier_material in multiplier_materials:
        for multiplier_thickness in multiplier_thicknesses:
            ## Multiplier
            multiplier_inner_cyl = openmc.ZCylinder(r=2*2.54)
            multiplier_outer_cyl = openmc.ZCylinder(r=multiplier_inner_cyl.r +multiplier_thickness)
            multiplier_reg = +multiplier_inner_cyl & -multiplier_outer_cyl & +multiplier_bot_plane & -multiplier_top_plane \
                            & +x_plane_1 & +y_plane_1
            multiplier_cell = openmc.Cell(region=multiplier_reg, fill=multiplier_material, name='Multiplier')

            outside_air_reg = -outer_cyl_4 & +z_plane_1 & -salt_gas_tube_top_plane & +x_plane_1 & +y_plane_1 \
                            & ~out_wall_reg & ~wall_gap_reg & ~inner_wall_reg \
                            & ~salt_reg & ~inner_tank_air_reg \
                            & ~outer_tank_cover_reg \
                            & ~inner_tank_cover_reg & ~fill_tube_reg \
                            & ~heater_overall_1_reg & ~heater_overall_2_reg \
                            & ~heater_overall_3_reg \
                            & ~salt_gas_tube_1_reg & ~salt_gas_tube_2_reg \
                            & ~thermocouple_tube_1_reg & ~thermocouple_tube_2_reg \
                            & ~thermocouple_tube_3_reg \
                            & ~multiplier_reg
            outside_air_cell = openmc.Cell(region=outside_air_reg, fill=air, name='Outside Air')
                # void region
            libra_quarter_1_reg = -outer_cyl_4 & +z_plane_1 & -salt_gas_tube_top_plane & +x_plane_1 & +y_plane_1

            void_reg = -void_cyl & +void_bot_plane & -void_top_plane \
                         & ~libra_quarter_1_reg

            void_cell = openmc.Cell(fill=air, region=void_reg, name='Void Cell')


            cells = [out_wall_cell, wall_gap_cell, inner_wall_cell,
                    heater_reentrant_1_cell, heater_reentrant_2_cell, heater_reentrant_3_cell,
                    heater_fill_1_cell, heater_fill_2_cell, heater_fill_3_cell,
                    fill_tube_cell, salt_gas_tube_1_cell, salt_gas_tube_2_cell,
                    thermocouple_tube_1_cell, thermocouple_tube_2_cell, thermocouple_tube_3_cell,
                    inner_tank_cover_cell, outer_tank_cover_cell,
                    salt_cell, inner_tank_air_cell,
                    multiplier_cell, outside_air_cell,
                    void_cell]
            # print(heater_reentrant_3_reg.get_surfaces())

            universe = openmc.Universe(cells=cells)
            geometry = openmc.Geometry(universe)

            ### Source

            point = openmc.stats.Point((0.0, 0.0, source_z_point))
            src = openmc.IndependentSource(space=point)
            src.energy = openmc.stats.Discrete([14.1E6], [1.0])
            src.strength = 1.5E8

            vol = openmc.VolumeCalculation(domains=cells, samples=int(1e10))
            settings = openmc.Settings()
            settings.run_mode = 'fixed source'
            settings.source = src
            settings.batches = 100
            settings.inactive = 0
            settings.particles = int(5e5)
            settings.volume_calculations = [vol]
            # settings.photon_transport = True
            settings.photon_transport = False

            t_tally = openmc.Tally(name='tritium tally')
            salt_filter = openmc.CellFilter([salt_cell])
            t_tally.filters.append(salt_filter)
            t_tally.scores = ['(n,Xt)']

            multiplier_n2n_tally = openmc.Tally(name='multiplier tally')
            multiplier_filter = openmc.CellFilter(multiplier_cell)
            multiplier_n2n_tally.filters.append(multiplier_filter)
            multiplier_n2n_tally.scores = ['(n,2n)']

            r_grid = [inner_cyl_1.r - 0.1, inner_cyl_1.r]
            z_grid = [void_bot_plane.z0, void_top_plane.z0]
            phi_grid = [0, np.pi/2, 2*np.pi]
            cyl_mesh = openmc.CylindricalMesh(r_grid=r_grid, z_grid=z_grid,
                                            phi_grid=phi_grid)
            # cyl_mesh.r_grid = [0, inner_cyl_1.r]
            # cyl_mesh.z_grid = [void_bot_plane.z0, void_top_plane.z0]
            # cyl_mesh.phi_grid = [0, np.pi/2, 2*np.pi]

            current_tally = openmc.Tally(name='current tally')
            # surface_filter = openmc.SurfaceFilter(inner_cyl_1)
            # cell_filter = openmc.CellFilter([outside_air_cell, void_cell])
            # current_tally.filters.append(surface_filter)
            # current_tally.filters.append(cell_filter)
            surf_mesh_filter = openmc.MeshSurfaceFilter(cyl_mesh)
            current_tally.filters.append(surf_mesh_filter)
            current_tally.scores = ['current']

            tallies = openmc.Tallies([t_tally, multiplier_n2n_tally, current_tally])

            if __name__ == '__main__':
                salt_directory = salt_material.name
                multiplier_directory = '{}_{}cm'.format(multiplier_material.name, multiplier_thickness)
                if not os.path.isdir(salt_directory):
                    os.mkdir(salt_directory)
                directory = salt_directory + '/' + multiplier_directory
                if not os.path.isdir(directory):
                    os.mkdir(directory)
                os.chdir(directory)
                print(directory)
                model = openmc.Model(geometry=geometry, materials=materials,
                                    settings=settings, tallies=tallies)
                model.export_to_xml()

                openmc.calculate_volumes()
                vol_calc = openmc.VolumeCalculation.from_hdf5('volume_1.h5')
                print(vol_calc.volumes)

                break

                # openmc.run(threads=16)
                os.chdir('..')
                os.chdir('..')
            break
        break
    break


                    







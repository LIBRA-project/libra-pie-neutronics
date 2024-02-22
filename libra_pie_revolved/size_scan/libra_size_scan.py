import numpy as np
import openmc
import os
from matplotlib import pyplot as plt

multiplier_thickness = 5
# starting_radius_1 = 10.0

# salt_heights = [80, 85, 90, 95, 100, 105, 110, 120]
salt_heights = [80, 90, 100, 110]
# salt_thicknesses = [30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50]
salt_thicknesses = [36, 38, 40, 44, 48]

reflector_thicknesses = [20]


salt_height = 94
# reflector_thicknesses = [1.0]
# multiplier_thicknesses = [1.0]


def circle_strip_area(x, r):
    """ Calculates area (integral) of quarter circle in first quadrant 
        from 0 to x with radius r"""

    area = 1/2 * (x*np.sqrt(r**2 - x**2) + r**2 * np.arctan(x/np.sqrt(r**2 - x**2)))
    return area


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


# FLiBe at an approximate density at its melting point, from 
# Vidrio, J. Chem. Eng. Data 2022, 67, 12, 3517–3531

flibe_cold = openmc.Material(name='Flibe_460C')
# Flibe_nat.temperature = 700 + 273
flibe_cold.add_element('Be', 0.142857, 'ao')
flibe_cold.add_nuclide('Li6', 0.021685, 'ao')
flibe_cold.add_nuclide('Li7', 0.264029, 'ao')
flibe_cold.add_element('F', 0.571429, 'ao')
flibe_cold.set_density("g/cm3", 2.06)


# lif-licl - natural - pure
cllif_nat = openmc.Material(name='ClLiF')
cllif_nat.add_element('F', .5*.305, 'ao')
cllif_nat.add_element('Li', .5*.305 + .5*.695, 'ao')
cllif_nat.add_element('Cl', .5*.695, 'ao')
cllif_nat.set_density('g/cm3', 1.54)

# lif-licl - natural - pure - at room temperature
cllif_cold = openmc.Material(name='ClLiF_25C')
cllif_cold.add_element('F', .5*.305, 'ao')
cllif_cold.add_element('Li', .5*.305 + .5*.695, 'ao')
cllif_cold.add_element('Cl', .5*.695, 'ao')
cllif_cold.set_density('g/cm3', 2.17)

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

# Stainless Steel 304 from PNNL Materials Compendium (PNNL-15870 Rev2)
SS304 = openmc.Material(name="SS304")
# SS304.temperature = 700 + 273
SS304.add_element('C',  0.000800, "wo")
SS304.add_element('Mn', 0.020000, "wo")
SS304.add_element('P',  0.000450 , "wo")
SS304.add_element('S',  0.000300, "wo")
SS304.add_element('Si', 0.010000, "wo")
SS304.add_element('Cr', 0.190000, "wo")
SS304.add_element('Ni', 0.095000, "wo")
SS304.add_element('Fe', 0.683450, "wo")
SS304.set_density("g/cm3", 8.00)

# Graphite (reactor-grade) from PNNL Materials Compendium (PNNL-15870 Rev2)
graphite = openmc.Material(name='Graphite')
graphite.set_density('g/cm3', 1.7)
graphite.add_element('B', 0.000001, 'wo')
graphite.add_element('C', 0.999999, 'wo')

# Using Microtherm with 1 a% Al2O3, 27 a% ZrO2, and 72 a% SiO2
# https://www.foundryservice.com/product/microporous-silica-insulating-boards-mintherm-microtherm-1925of-grades/
firebrick = openmc.Material(name="Firebrick")
# Estimate average temperature of Firebrick to be around 300 C
# Firebrick.temperature = 273 + 300
firebrick.add_element('Al', 0.004, 'ao')
firebrick.add_element('O', 0.666, 'ao')
firebrick.add_element('Si', 0.240, 'ao')
firebrick.add_element('Zr', 0.090, 'ao')
firebrick.set_density('g/cm3', 0.30)

# High Density Polyethylene
# Reference:  PNNL Report 15870 (Rev. 1)
HDPE = openmc.Material(name='HDPE')
HDPE.set_density('g/cm3', 0.95)
HDPE.add_element('H', 0.143724, 'wo')
HDPE.add_element('C', 0.856276, 'wo')

#Reference: PNNL Report 15870 (Rev. 1) Low Carbon Steel
steel_lowC = openmc.Material(name='SteelLowC')
steel_lowC.add_element('C',  0.0010, 'wo')
steel_lowC.add_element('Mn', 0.0050, 'wo')
steel_lowC.add_element('P',  0.0004, 'wo')
steel_lowC.add_element('S',  0.0005, 'wo')
steel_lowC.add_element('Fe', 0.9931, 'wo')
steel_lowC.set_density('g/cm3', 7.872)

# Zirconia with the density of Zircar FBD referenced below:
zirconia = openmc.Material(name='Zirconia')
zirconia.set_density('g/cm3', 1.4)
zirconia.add_element('Zr', 1/3, 'ao')
zirconia.add_element('O', 2/3, 'ao')

# # Zircar FBD zirconia (90% ZrO2, Y2O) insulation with a density of 1.4 g/cm3
# # Source: https://www.zircarzirconia.com/images/datasheets/ZZ-5000_Rev02_-_ZYFB-3_ZYFB-6___FBD.pdf?type=file
# # Website: https://www.zircarzirconia.com/products/rigid-materials
# zircar_fbd = openmc.Material(name='Zircar_FBD')
# zircar_fbd.set_density('g/cm3', 1.4)
# zircar_fbd.add_element('')

# tungsten
tungsten = openmc.Material(name='Tungsten')
tungsten.set_density("g/cm3", 19.28)
tungsten.add_element('W', 1.00, 'ao')

# Name: Portland concrete
# Density: 2.3 g/cm3
# Reference: PNNL Report 15870 (Rev. 1)
# Describes: facility foundation, floors, walls
Concrete = openmc.Material(name='Concrete') 
Concrete.set_density('g/cm3', 2.3) 
Concrete.add_nuclide('H1', 0.168759, 'ao') 
Concrete.add_element('C', 0.001416, 'ao') 
Concrete.add_nuclide('O16', 0.562524, 'ao') 
Concrete.add_nuclide('Na23', 0.011838, 'ao') 
Concrete.add_element('Mg', 0.0014, 'ao') 
Concrete.add_nuclide('Al27', 0.021354, 'ao') 
Concrete.add_element('Si', 0.204115, 'ao') 
Concrete.add_element('K', 0.005656, 'ao') 
Concrete.add_element('Ca', 0.018674, 'ao') 
Concrete.add_element('Fe', 0.004264, 'ao') 

# Name: Borated Polyethylene (5% B in via B4C additive)
# Density: 0.95 g/cm3
# Reference: PNNL Report 15870 (Rev. 1) but revised to make it 5 wt.% B
# Describes: General purpose neutron shielding
BPE = openmc.Material(name='BPE') 
BPE.set_density('g/cm3', 0.95) 
BPE.add_nuclide('H1', 0.1345, 'wo') 
BPE.add_element('B', 0.0500, 'wo') 
BPE.add_element('C', 0.8155, 'wo')

water = openmc.Material(name='water')
water.set_density('g/cm3', 0.998)
water.add_element('H', 2/3, 'ao')
water.add_element('O', 1/3, 'ao')

gen_mat_1 = openmc.Material()
gen_mat_1.set_density('g/cm3', 0.05000000000000001)
gen_mat_1.add_nuclide('S32', 0.219, 'wo')
gen_mat_1.add_nuclide('F19', 0.781, 'wo')
#
gen_aluminum = openmc.Material(name='Aluminum')
gen_aluminum.set_density('g/cm3', 2.7)
gen_aluminum.add_nuclide('Al27', 1.0, 'wo')
#
gen_air = openmc.Material(name='Air')
gen_air.set_density('g/cm3', 0.0012000000000000001)
gen_air.add_nuclide('C12', 0.00012251284879063982, 'wo')
gen_air.add_nuclide('C13', 1.4871512093601811e-06, 'wo')
gen_air.add_nuclide('N14', 0.755268, 'wo')
gen_air.add_nuclide('O16', 0.231781, 'wo')
gen_air.add_nuclide('Ar40', 0.012780805392164559, 'wo')
gen_air.add_nuclide('Ar38', 7.667262798148065e-06, 'wo')
gen_air.add_nuclide('Ar36', 3.852734503729188e-05, 'wo')
#
gen_copper = openmc.Material(name='Copper')
gen_copper.set_density('g/cm3', 8.939999999999998)
gen_copper.add_nuclide('Cu63', 0.692, 'wo')
gen_copper.add_nuclide('Cu65', 0.308, 'wo')
#
gen_mat_5 = openmc.Material()
gen_mat_5.set_density('g/cm3', 8.35)
gen_mat_5.add_nuclide('Co59', 0.769136, 'wo')
gen_mat_5.add_nuclide('Sm149', 0.066489, 'wo')
gen_mat_5.add_nuclide('Sm150', 0.102735, 'wo')
gen_mat_5.add_nuclide('Sm152', 0.06164, 'wo')
#
gen_mat_6 = openmc.Material()
gen_mat_6.set_density('g/cm3', 2.230000000000001)
gen_mat_6.add_nuclide('B10', 0.000801, 'wo')
gen_mat_6.add_nuclide('B11', 0.032051, 'wo')
gen_mat_6.add_nuclide('O16', 0.539562, 'wo')
gen_mat_6.add_nuclide('Al27', 0.011644, 'wo')
gen_mat_6.add_nuclide('Si29', 0.018226328454672452, 'wo')
gen_mat_6.add_nuclide('Si28', 0.3465652818947457, 'wo')
gen_mat_6.add_nuclide('Si30', 0.01242838965058185, 'wo')
gen_mat_6.add_nuclide('K39', 0.003086439846097162, 'wo')
gen_mat_6.add_nuclide('K41', 0.0002341629936459004, 'wo')
gen_mat_6.add_nuclide('K40', 3.9716025693846255e-07, 'wo')
#
gen_mat_7 = openmc.Material()
gen_mat_7.set_density('g/cm3', 7.999999999999999)
gen_mat_7.add_nuclide('C12', 0.000395202738034322, 'wo')
gen_mat_7.add_nuclide('C13', 4.797261965678004e-06, 'wo')
gen_mat_7.add_nuclide('Si29', 0.0002415875146422837, 'wo')
gen_mat_7.add_nuclide('Si28', 0.004593675864147523, 'wo')
gen_mat_7.add_nuclide('Si30', 0.00016473662121019365, 'wo')
gen_mat_7.add_nuclide('P31', 0.00023, 'wo')
gen_mat_7.add_nuclide('S33', 1.154822906641789e-06, 'wo')
gen_mat_7.add_nuclide('S32', 0.0001421529162123894, 'wo')
gen_mat_7.add_nuclide('S34', 6.667728601323577e-06, 'wo')
gen_mat_7.add_nuclide('S36', 2.453227964521797e-08, 'wo')
gen_mat_7.add_nuclide('Cr52', 0.1590287884699489, 'wo')
gen_mat_7.add_nuclide('Cr50', 0.007930004419221556, 'wo')
gen_mat_7.add_nuclide('Cr53', 0.01837981508548118, 'wo')
gen_mat_7.add_nuclide('Cr54', 0.004661392025348396, 'wo')
gen_mat_7.add_nuclide('Mn55', 0.01, 'wo')
gen_mat_7.add_nuclide('Fe57', 0.015159954698765962, 'wo')
gen_mat_7.add_nuclide('Fe54', 0.039616575742117216, 'wo')
gen_mat_7.add_nuclide('Fe56', 0.6449005978502143, 'wo')
gen_mat_7.add_nuclide('Fe58', 0.0020528717089025846, 'wo')
gen_mat_7.add_nuclide('Ni62', 0.003547210629714033, 'wo')
gen_mat_7.add_nuclide('Ni60', 0.02476776568001649, 'wo')
gen_mat_7.add_nuclide('Ni58', 0.06215787740265687, 'wo')
gen_mat_7.add_nuclide('Ni64', 0.0009325391338474599, 'wo')
gen_mat_7.add_nuclide('Ni61', 0.0010946071537651504, 'wo')
#
gen_mat_8 = openmc.Material()
gen_mat_8.set_density('g/cm3', 7.75)
gen_mat_8.add_nuclide('C12', 0.001185608214102966, 'wo')
gen_mat_8.add_nuclide('C13', 1.439178589703401e-05, 'wo')
gen_mat_8.add_nuclide('Si29', 0.0004831750292845674, 'wo')
gen_mat_8.add_nuclide('Si28', 0.009187351728295046, 'wo')
gen_mat_8.add_nuclide('Si30', 0.0003294732424203873, 'wo')
gen_mat_8.add_nuclide('P31', 0.0004, 'wo')
gen_mat_8.add_nuclide('S33', 2.309645813283578e-06, 'wo')
gen_mat_8.add_nuclide('S32', 0.0002843058324247788, 'wo')
gen_mat_8.add_nuclide('S34', 1.3335457202647154e-05, 'wo')
gen_mat_8.add_nuclide('S36', 4.906455929043594e-08, 'wo')
gen_mat_8.add_nuclide('Cr52', 0.15065885223468842, 'wo')
gen_mat_8.add_nuclide('Cr50', 0.007512635765578316, 'wo')
gen_mat_8.add_nuclide('Cr53', 0.017412456396771643, 'wo')
gen_mat_8.add_nuclide('Cr54', 0.004416055602961638, 'wo')
gen_mat_8.add_nuclide('Mn55', 0.01, 'wo')
gen_mat_8.add_nuclide('Fe57', 0.01724190193533854, 'wo')
gen_mat_8.add_nuclide('Fe54', 0.045057200204898964, 'wo')
gen_mat_8.add_nuclide('Fe56', 0.733466101127579, 'wo')
gen_mat_8.add_nuclide('Fe58', 0.002334796732183536, 'wo')
#
gen_dt_fuel1 = openmc.Material(name='DT_fuel_1')
gen_dt_fuel1.set_density('g/cm3', 3.4999999999999993e-10)
gen_dt_fuel1.add_nuclide('H2', 0.4, 'wo')
gen_dt_fuel1.add_nuclide('H3', 0.6, 'wo')
#
gen_mat_11 = openmc.Material()
gen_mat_11.set_density('g/cm3', 2.2000000000000006)
gen_mat_11.add_nuclide('C12', 0.23729948405270865, 'wo')
gen_mat_11.add_nuclide('C13', 0.002880515947291357, 'wo')
gen_mat_11.add_nuclide('F19', 0.75982, 'wo')
#
gen_mat_12 = openmc.Material()
gen_mat_12.set_density('g/cm3', 8.000000000000002)
gen_mat_12.add_nuclide('C12', 0.00040508280648518004, 'wo')
gen_mat_12.add_nuclide('C13', 4.917193514819953e-06, 'wo')
gen_mat_12.add_nuclide('Si29', 0.00024496973984727567, 'wo')
gen_mat_12.add_nuclide('Si28', 0.004657987326245588, 'wo')
gen_mat_12.add_nuclide('Si30', 0.00016704293390713636, 'wo')
gen_mat_12.add_nuclide('P31', 0.00023, 'wo')
gen_mat_12.add_nuclide('S33', 1.154822906641789e-06, 'wo')
gen_mat_12.add_nuclide('S32', 0.0001421529162123894, 'wo')
gen_mat_12.add_nuclide('S34', 6.667728601323577e-06, 'wo')
gen_mat_12.add_nuclide('S36', 2.453227964521797e-08, 'wo')
gen_mat_12.add_nuclide('Cr52', 0.14228891599942797, 'wo')
gen_mat_12.add_nuclide('Cr50', 0.007095267111935077, 'wo')
gen_mat_12.add_nuclide('Cr53', 0.016445097708062108, 'wo')
gen_mat_12.add_nuclide('Cr54', 0.004170719180574881, 'wo')
gen_mat_12.add_nuclide('Mn55', 0.01014, 'wo')
gen_mat_12.add_nuclide('Fe57', 0.014452866050296309, 'wo')
gen_mat_12.add_nuclide('Fe54', 0.037768784534616476, 'wo')
gen_mat_12.add_nuclide('Fe56', 0.6148212274832106, 'wo')
gen_mat_12.add_nuclide('Fe58', 0.001957121931876689, 'wo')
gen_mat_12.add_nuclide('Ni62', 0.004601786762872259, 'wo')
gen_mat_12.add_nuclide('Ni60', 0.032131155476778146, 'wo')
gen_mat_12.add_nuclide('Ni58', 0.08063724636020352, 'wo')
gen_mat_12.add_nuclide('Ni64', 0.0012097804979642724, 'wo')
gen_mat_12.add_nuclide('Ni61', 0.0014200309021818167, 'wo')
gen_mat_12.add_nuclide('Mo98', 0.006196843088917898, 'wo')
gen_mat_12.add_nuclide('Mo92', 0.0035079728451151634, 'wo')
gen_mat_12.add_nuclide('Mo94', 0.0022478295952628046, 'wo')
gen_mat_12.add_nuclide('Mo95', 0.003925116097438845, 'wo')
gen_mat_12.add_nuclide('Mo97', 0.0024193988768413575, 'wo')
gen_mat_12.add_nuclide('Mo96', 0.004166334087942884, 'wo')
gen_mat_12.add_nuclide('Mo100', 0.0025365054084810477, 'wo')
#
gen_dt_fuel2 = openmc.Material(name='DT_fuel_2')
gen_dt_fuel2.set_density('g/cm3', 3.4000000000000007e-10)
gen_dt_fuel2.add_nuclide('H2', 0.4, 'wo')
gen_dt_fuel2.add_nuclide('H3', 0.6, 'wo')


salt_materials = [flibe_nat]
# salt_materials = [cllif_nat, flibe_nat, cllif_cold, flibe_cold]
# salt_materials = [flibe_nat, flibe_cold]
# salt_material = cllif_nat

# reflector_materials = [graphite, lead, beryllium, HDPE, SS304, steel_lowC, tungsten, Concrete, water]
# reflector_materials = [graphite]
reflector_material = graphite


# multiplier_material = beryllium
multiplier_material = lead

tbrs = np.zeros((len(salt_materials), len(reflector_thicknesses), len(salt_heights), len(salt_thicknesses)))
salt_volumes = np.zeros((len(salt_materials), len(reflector_thicknesses), len(salt_heights), len(salt_thicknesses)))

materials = openmc.Materials([
                            inconel625,
                            flibe_nat,
                            cllif_nat,
                            air,
                            beryllium,
                            lead,
                            graphite,
                            firebrick,
                            HDPE,
                            SS304,
                            steel_lowC,
                            zirconia,
                            tungsten,
                            Concrete,
                            BPE,
                            cllif_cold,
                            flibe_cold,
                            water,
                            gen_mat_1, gen_aluminum,
                            gen_copper, gen_mat_5,
                            gen_mat_6, gen_mat_7,
                            gen_mat_8, gen_dt_fuel1, 
                            gen_mat_11, gen_mat_12, 
                            gen_dt_fuel2, gen_air
                            ])

######## LIBRA Surfaces #################

libra_wall_th = 0.3175 # 1/8 inch
gap_thickness = 0.635 # 1/4 inch
salt_headspace = 7.28*2.54
multiplier_height = 28
# shield_thickness = 6*2.54
support_plate_thickness = 2.54
# lead_thickness = 2.54
lead_thickness = 0
reflector_thickness = 10

reference_salt_height = 112.71 - salt_headspace
reference_thickness = 52.39 - 2*libra_wall_th - gap_thickness - 15.24

# Tank double wall surfaces

# GEOMETRY

# surfaces
surf_302 = openmc.ZPlane(surface_id=302, z0=0.4)
gen_bot_plane = openmc.ZPlane(surface_id=300, z0=0.0)
surf_420 = openmc.ZCylinder(surface_id=420, x0=0.0, y0=0.0, r=4.28)
surf_303 = openmc.ZPlane(surface_id=303, z0=1.8)
gen_out_cyl = openmc.ZCylinder(surface_id=435, x0=0.0, y0=0.0, r=5.08)
surf_304 = openmc.ZPlane(surface_id=304, z0=2.6)
surf_305 = openmc.ZPlane(surface_id=305, z0=3.656)
surf_414 = openmc.ZCylinder(surface_id=414, x0=0.0, y0=0.0, r=2.743)
surf_307 = openmc.ZPlane(surface_id=307, z0=4.478)
surf_412 = openmc.ZCylinder(surface_id=412, x0=0.0, y0=0.0, r=2.21)
surf_311 = openmc.ZPlane(surface_id=311, z0=3.512)
surf_309 = openmc.ZPlane(surface_id=309, z0=6.04)
surf_413 = openmc.ZCylinder(surface_id=413, x0=0.0, y0=0.0, r=2.51)
surf_308 = openmc.ZPlane(surface_id=308, z0=5.634)
surf_306 = openmc.ZPlane(surface_id=306, z0=4.462)
surf_403 = openmc.ZCylinder(surface_id=403, x0=0.0, y0=0.0, r=0.7)
surf_351 = openmc.ZPlane(surface_id=351, z0=8.129)
surf_352 = openmc.ZPlane(surface_id=352, z0=9.5)
surf_1036 = openmc.ZCone(surface_id=1036, x0=0.0, y0=0.0,
                         z0=11.6404387755, r2=0.5109486)
surf_1037 = openmc.ZPlane(surface_id=1037, z0=11.6404387755)
surf_1034 = openmc.ZCone(surface_id=1034, x0=0.0,
                         y0=0.0, z0=11.220744898, r2=0.5109486)
surf_1035 = openmc.ZPlane(surface_id=1035, z0=11.220744898)
surf_315 = openmc.ZPlane(surface_id=315, z0=14.745)
surf_410 = openmc.ZCylinder(surface_id=410, x0=0.0, y0=0.0, r=1.53)
surf_406 = openmc.ZCylinder(surface_id=406, x0=0.0, y0=0.0, r=1.23)
surf_1038 = openmc.ZCone(surface_id=1038, x0=0.0, y0=0.0,
                         z0=6.796859375, r2=0.034329966)
surf_1039 = openmc.ZPlane(surface_id=1039, z0=6.796859375)
surf_501 = openmc.Sphere(surface_id=501, x0=0.0, y0=0.0, z0=9.526, r=1.14)
surf_310 = openmc.ZPlane(surface_id=310, z0=12.561)
surf_405 = openmc.ZCylinder(surface_id=405, x0=0.0, y0=0.0, r=1.139)
surf_407 = openmc.ZCylinder(surface_id=407, x0=0.0, y0=0.0, r=1.18)
surf_320 = openmc.ZPlane(surface_id=320, z0=30.112)
surf_316 = openmc.ZPlane(surface_id=316, z0=15.507)
surf_400 = openmc.ZCylinder(surface_id=400, x0=0.0, y0=0.0, r=1.575)
surf_415 = openmc.ZCylinder(surface_id=415, x0=0.0, y0=0.0, r=2.286)
surf_401 = openmc.ZCylinder(surface_id=401, x0=0.0, y0=0.0, r=1.905)
surf_317 = openmc.ZPlane(surface_id=317, z0=16.421)
surf_417 = openmc.ZCylinder(surface_id=417, x0=0.0, y0=0.0, r=3.416)
surf_353 = openmc.ZPlane(surface_id=353, z0=9.589)
surf_418 = openmc.ZCylinder(surface_id=418, x0=0.0, y0=0.0, r=2.68)
surf_318 = openmc.ZPlane(surface_id=318, z0=17.183)
surf_325 = openmc.ZPlane(surface_id=325, z0=64.29)
surf_425 = openmc.ZCylinder(surface_id=425, x0=0.0, y0=0.0, r=4.445)
surf_430 = openmc.ZCylinder(surface_id=430, x0=0.0, y0=0.0, r=4.869)
gen_top_plane = openmc.ZPlane(surface_id=330, z0=66.04)
surf_961 = openmc.XPlane(surface_id=961, x0=200.0)
surf_960 = openmc.XPlane(surface_id=960, x0=-200.0)
surf_963 = openmc.YPlane(surface_id=963, y0=200.0)
surf_962 = openmc.YPlane(surface_id=962, y0=-200.0)
surf_965 = openmc.ZPlane(surface_id=965, z0=-110.0)
surf_964 = openmc.ZPlane(surface_id=964, z0=-140.0)
surf_505 = openmc.Sphere(surface_id=505, x0=0.0, y0=0.0, z0=12.561, r=60.0)
surf_955 = openmc.XPlane(surface_id=955, x0=310.0, boundary_type='vacuum')
surf_954 = openmc.XPlane(surface_id=954, x0=-310.0, boundary_type='vacuum')
surf_957 = openmc.YPlane(surface_id=957, y0=310.0, boundary_type='vacuum')
surf_956 = openmc.YPlane(surface_id=956, y0=-310.0, boundary_type='vacuum')
surf_959 = openmc.ZPlane(surface_id=959, z0=310.0, boundary_type='vacuum')
surf_958 = openmc.ZPlane(surface_id=958, z0=-310.0, boundary_type='vacuum')

# regions
region_101 = (-surf_302 & +gen_bot_plane & -surf_420)
region_102 = (-surf_303 & +gen_bot_plane & -gen_out_cyl & +surf_420)
region_103 = (-surf_304 & +surf_302 & -surf_420)
region_104 = (-surf_305 & +surf_304 & -surf_420 & +surf_414)
region_105 = (-surf_307 & +surf_304 & -surf_414 & +surf_412)
region_106 = (-surf_311 & +surf_304 & -surf_412)
region_107 = (-surf_309 & +surf_307 & -surf_413 & +surf_412)
region_108 = (-surf_309 & +surf_308 & -surf_412)
region_109 = (-surf_306 & +surf_311 & -surf_403)
region_110 = ((-surf_412 & +surf_403 & +surf_311 & -surf_308)
              | (+surf_306 & -surf_308 & -surf_403))
region_111 = ((-surf_420 & +surf_414 & -surf_309 & +surf_305) |
              (-surf_414 & +surf_413 & -surf_309 & +surf_307))
region_112 = (-surf_351 & +surf_309 & -surf_413 & +surf_412)
region_113 = (-surf_352 & +surf_351 & -surf_1036 & -surf_1037 &
              ((+surf_1034 & -surf_1035) | +surf_1035))
region_114 = (-surf_315 & +surf_352 & -surf_410 & +surf_406)
region_115 = (-surf_351 & +surf_309 & -surf_412)
region_116 = ((-surf_352 & +surf_351 & -surf_1038 & +surf_1039) | (-surf_352 & +surf_351 & +
              surf_501 & ((+surf_1038 & +surf_1039) | -surf_1039) & -surf_1034 & -surf_1035))
region_117 = ((-surf_310 & +surf_352 & -surf_1038 & +surf_1039) | (-surf_315 & +
              surf_352 & -surf_406 & +surf_405 & ~(-surf_315 & +surf_310 & -surf_407)))
region_118 = (-surf_315 & +surf_310 & -surf_407)
region_119 = (-surf_501 & ((+surf_1038 & +surf_1039) | -surf_1039) & -surf_352)
region_120 = (-surf_405 & ((+surf_1038 & +surf_1039)
              | -surf_1039) & +surf_352 & -surf_310)
region_121 = (-surf_320 & +surf_316 & -surf_400)
region_122 = (-surf_316 & +surf_315 & -surf_415)
region_123 = (-surf_320 & +surf_316 & -surf_401 & +surf_400)
region_124 = (-surf_317 & +surf_316 & -surf_417 & +surf_401)
region_125 = (-surf_316 & +surf_353 & -surf_417 & +surf_418)
region_126 = (-surf_318 & +surf_317 & -surf_420 & +surf_401)
region_127 = (-surf_351 & +surf_309 & -surf_420 & +surf_413)
region_128 = (-surf_352 & +surf_351 & -surf_420 &
              ((+surf_1036 & -surf_1037) | +surf_1037))
region_129 = (-surf_315 & +surf_352 & -surf_420 & +surf_410 & ~
              (-surf_316 & +surf_353 & -surf_417 & +surf_418))
region_130 = (-surf_317 & +surf_315 & -surf_420 & +surf_415 & ~(-surf_317 & +
              surf_316 & -surf_417 & +surf_401) & ~(-surf_316 & +surf_353 & -surf_417 & +surf_418))
region_131 = (-surf_320 & +surf_318 & -surf_420 & +surf_401)
region_132 = (-surf_325 & +surf_320 & -surf_420)
region_133 = (-surf_325 & +surf_303 & -surf_425 & +surf_420)
region_134 = (-surf_325 & +surf_303 & -surf_430 & +surf_425)
region_135 = (-surf_325 & +surf_303 & -gen_out_cyl & +surf_430)
region_136 = (-gen_top_plane & +surf_325 & -gen_out_cyl)
region_138 = ((-gen_bot_plane | +gen_out_cyl | +gen_top_plane) & -surf_505)
region_139 = (-surf_955 & +surf_954 & -surf_957 & +surf_956 & -surf_959 & +surf_958  & +surf_505)
region_150 = (+surf_955 | -surf_954 | +surf_957 | -
              surf_956 | +surf_959 | -surf_958)

# cells
cell_101 = openmc.Cell(cell_id=101, region=region_101, fill=gen_mat_7)
cell_102 = openmc.Cell(cell_id=102, region=region_102, fill=gen_mat_7)
cell_103 = openmc.Cell(cell_id=103, region=region_103, fill=gen_mat_1)
cell_104 = openmc.Cell(cell_id=104, region=region_104, fill=gen_mat_7)
cell_105 = openmc.Cell(cell_id=105, region=region_105, fill=gen_mat_8)
cell_106 = openmc.Cell(cell_id=106, region=region_106, fill=gen_mat_8)
cell_107 = openmc.Cell(cell_id=107, region=region_107, fill=gen_mat_8)
cell_108 = openmc.Cell(cell_id=108, region=region_108, fill=gen_mat_8)
cell_109 = openmc.Cell(cell_id=109, region=region_109, fill=gen_mat_5)
cell_110 = openmc.Cell(cell_id=110, region=region_110, fill=gen_mat_1)
cell_111 = openmc.Cell(cell_id=111, region=region_111, fill=gen_mat_1)
cell_112 = openmc.Cell(cell_id=112, region=region_112, fill=gen_mat_6)
cell_113 = openmc.Cell(cell_id=113, region=region_113, fill=gen_mat_6)
cell_114 = openmc.Cell(cell_id=114, region=region_114, fill=gen_mat_6)
cell_115 = openmc.Cell(cell_id=115, region=region_115, fill=gen_dt_fuel1)
cell_116 = openmc.Cell(cell_id=116, region=region_116, fill=gen_dt_fuel1)
cell_117 = openmc.Cell(cell_id=117, region=region_117, fill=gen_dt_fuel2)
cell_118 = openmc.Cell(cell_id=118, region=region_118, fill=gen_copper)
cell_119 = openmc.Cell(cell_id=119, region=region_119, fill=gen_mat_12)
cell_120 = openmc.Cell(cell_id=120, region=region_120, fill=gen_mat_12)
cell_121 = openmc.Cell(cell_id=121, region=region_121, fill=gen_mat_1)
cell_122 = openmc.Cell(cell_id=122, region=region_122, fill=gen_aluminum)
cell_123 = openmc.Cell(cell_id=123, region=region_123, fill=gen_aluminum)
cell_124 = openmc.Cell(cell_id=124, region=region_124, fill=gen_aluminum)
cell_125 = openmc.Cell(cell_id=125, region=region_125, fill=gen_aluminum)
cell_126 = openmc.Cell(cell_id=126, region=region_126, fill=gen_mat_11)
cell_127 = openmc.Cell(cell_id=127, region=region_127, fill=gen_mat_1)
cell_128 = openmc.Cell(cell_id=128, region=region_128, fill=gen_mat_1)
cell_129 = openmc.Cell(cell_id=129, region=region_129, fill=gen_mat_1)
cell_130 = openmc.Cell(cell_id=130, region=region_130, fill=gen_mat_1)
cell_131 = openmc.Cell(cell_id=131, region=region_131, fill=gen_mat_1)
cell_132 = openmc.Cell(cell_id=132, region=region_132, fill=gen_mat_1)
cell_133 = openmc.Cell(cell_id=133, region=region_133, fill=gen_mat_7)
cell_134 = openmc.Cell(cell_id=134, region=region_134, fill=gen_mat_1)
cell_135 = openmc.Cell(cell_id=135, region=region_135, fill=gen_mat_7)
cell_136 = openmc.Cell(cell_id=136, region=region_136, fill=gen_mat_7)
cell_138 = openmc.Cell(cell_id=138, region=region_138, fill=gen_air)
cell_139 = openmc.Cell(cell_id=139, region=region_139, fill=gen_air)
cell_150 = openmc.Cell(cell_id=150, region=region_150, fill=None)

# create root universe
gen_universe = openmc.Universe(cells=[cell_101, cell_102, cell_103, cell_104, 
                                  cell_105, cell_106, cell_107, cell_108, 
                                  cell_109, cell_110, cell_111, cell_112, 
                                  cell_113, cell_114, cell_115, cell_116, 
                                  cell_117, cell_118, cell_119, cell_120, 
                                  cell_121, cell_122, cell_123, cell_124, 
                                  cell_125, cell_126, cell_127, cell_128, 
                                  cell_129, cell_130, cell_131, cell_132, 
                                  cell_133, cell_134, cell_135, cell_136, 
                                  cell_138, cell_139, cell_150])

generator_region = -gen_top_plane & +gen_bot_plane & -gen_out_cyl


for i,salt_material in enumerate(salt_materials):
    for r,reflector_thickness in enumerate(reflector_thicknesses):
        for j,salt_height in enumerate(salt_heights):
            for k,salt_thickness in enumerate(salt_thicknesses):
                # inner_cyl_1 = openmc.ZCylinder(r=starting_radius_1+multiplier_thickness)
                # inner_cyl_2 = openmc.ZCylinder(r=inner_cyl_1.r+2*libra_wall_th)
                # inner_cyl_3 = openmc.ZCylinder(r=inner_cyl_2.r+gap_thickness)
                # inner_cyl_4 = openmc.ZCylinder(r=inner_cyl_3.r+2*libra_wall_th)
                inner_cyl_1 = openmc.ZCylinder(r=13.34)
                inner_cyl_2 = openmc.ZCylinder(r=13.97)
                inner_cyl_3 = openmc.ZCylinder(r=14.61)
                inner_cyl_4 = openmc.ZCylinder(r=15.24)

                x_plane_1 = openmc.XPlane(0.0)
                x_plane_2 = openmc.XPlane(libra_wall_th)
                x_plane_3 = openmc.XPlane(libra_wall_th + gap_thickness)
                x_plane_4 = openmc.XPlane(2*libra_wall_th + gap_thickness)

                y_plane_1 = openmc.YPlane(0.0)
                y_plane_2 = openmc.YPlane(libra_wall_th)
                y_plane_3 = openmc.YPlane(libra_wall_th + gap_thickness)
                y_plane_4 = openmc.YPlane(2*libra_wall_th + gap_thickness)

                z_plane_1 = openmc.ZPlane(0.0)
                z_plane_2 = openmc.ZPlane(libra_wall_th)
                z_plane_3 = openmc.ZPlane(libra_wall_th + gap_thickness)
                z_plane_4 = openmc.ZPlane(2*libra_wall_th + gap_thickness)

                double_wall_top_plane_1 = openmc.ZPlane(117.89)
                double_wall_top_plane_2 = openmc.ZPlane(117.89 + 0.89)


                ## Tank top cover surfaces
                tank_top_cover_plane_1 = openmc.ZPlane(salt_height + salt_headspace + z_plane_4.z0)
                # tank_top_cover_plane_1 = openmc.ZPlane(salt_height + z_plane_4.z0 + salt_headspace)
                tank_top_cover_plane_2 = openmc.ZPlane(tank_top_cover_plane_1.z0 + libra_wall_th*2)

                double_wall_top_plane_1 = openmc.ZPlane(tank_top_cover_plane_1.z0 + 3.91)
                double_wall_top_plane_2 = openmc.ZPlane(double_wall_top_plane_1.z0 + 0.89)

                center_tank_top_plane_1 = openmc.ZPlane(tank_top_cover_plane_1.z0)
                center_tank_top_plane_2 = openmc.ZPlane(center_tank_top_plane_1.z0 + libra_wall_th*2)

                center_tank_salt_top_plane = openmc.ZPlane(center_tank_top_plane_1.z0 - salt_headspace)

                ## salt surface:
                salt_top_plane = openmc.ZPlane(tank_top_cover_plane_1.z0 - salt_headspace)



                # outer_cyl_4 = openmc.ZCylinder(r=52.39)
                # outer_cyl_3 = openmc.ZCylinder(r=outer_cyl_4.r-libra_wall_th)
                # outer_cyl_2 = openmc.ZCylinder(r=outer_cyl_3.r-gap_thickness)
                # outer_cyl_1 = openmc.ZCylinder(r=outer_cyl_2.r-libra_wall_th)


                new_salt_outer_radius = inner_cyl_4.r + salt_thickness

                outer_cyl_1 = openmc.ZCylinder(r=new_salt_outer_radius)
                outer_cyl_2 = openmc.ZCylinder(r=outer_cyl_1.r+libra_wall_th)
                outer_cyl_3 = openmc.ZCylinder(r=outer_cyl_2.r+gap_thickness)
                outer_cyl_4 = openmc.ZCylinder(r=outer_cyl_3.r+libra_wall_th)

                # multiplier surfaces
                source_z_point = np.mean([z_plane_4.z0,salt_top_plane.z0])

                # print(source_z_point)

                if multiplier_thickness < 8:
                    multiplier_top_th = multiplier_thickness
                else:
                    multiplier_top_th = 8
                multiplier_top_plane_2 = openmc.ZPlane(source_z_point + 14 + multiplier_thickness)
                multiplier_top_plane_1 = openmc.ZPlane(source_z_point + 14)
                dt_gen_top_plane = openmc.ZPlane(source_z_point + 12)
                multiplier_bot_plane = openmc.ZPlane(source_z_point - 15)

                center_tank_bot_plane_1 = openmc.ZPlane(multiplier_top_plane_2.z0)
                center_tank_bot_plane_2 = openmc.ZPlane(center_tank_bot_plane_1.z0 + libra_wall_th)
                center_tank_bot_plane_3 = openmc.ZPlane(center_tank_bot_plane_2.z0 + gap_thickness)
                center_tank_bot_plane_4 = openmc.ZPlane(center_tank_bot_plane_3.z0 + libra_wall_th)

                center_tank_cyl_4 = openmc.ZCylinder(r=inner_cyl_1.r - 0.2)
                center_tank_cyl_3 = openmc.ZCylinder(r=center_tank_cyl_4.r - libra_wall_th)
                center_tank_cyl_2 = openmc.ZCylinder(r=center_tank_cyl_3.r - gap_thickness)
                center_tank_cyl_1 = openmc.ZCylinder(r=center_tank_cyl_2.r - libra_wall_th)


                salt_gas_tube_top_plane = openmc.ZPlane(130)
                lead_shield_in_cyl = openmc.ZCylinder(r=outer_cyl_4.r+5)
                lead_shield_top_plane_1 = openmc.ZPlane(salt_gas_tube_top_plane.z0)
                lead_shield_top_plane_2 = openmc.ZPlane(lead_shield_top_plane_1.z0 + lead_thickness)

                support_plate_bot_plane = openmc.ZPlane(z_plane_1.z0 - support_plate_thickness)


                shield_bot_plane_2 = openmc.ZPlane(support_plate_bot_plane.z0 - 10)
                shield_bot_plane_1 = openmc.ZPlane(shield_bot_plane_2.z0 - reflector_thickness)

                shield_in_cyl = openmc.ZCylinder(r=lead_shield_in_cyl.r+lead_thickness)
                shield_out_cyl = openmc.ZCylinder(r=shield_in_cyl.r+reflector_thickness)
                shield_top_plane_1 = openmc.ZPlane(lead_shield_top_plane_2.z0)
                shield_top_plane_2 = openmc.ZPlane(shield_top_plane_1.z0 + reflector_thickness)

                floor_rpp = openmc.model.RectangularParallelepiped(-300, 300, -300, 300, -150, -100)
                floor_rpp.xmin.boundary_type='vacuum'
                floor_rpp.xmax.boundary_type='vacuum'
                floor_rpp.ymin.boundary_type='vacuum'
                floor_rpp.ymax.boundary_type='vacuum'
                floor_rpp.zmin.boundary_type='vacuum'
                boundary_top_plane = openmc.ZPlane(200, boundary_type='vacuum')

                # print(multiplier_cyl)
                # print(inner_cyl_1)
                ## Void surfaces:

                # void_bot_plane = openmc.ZPlane(-50.0, boundary_type='vacuum')
                # void_top_plane = openmc.ZPlane(salt_gas_tube_top_plane.z0 + 50.0, boundary_type='vacuum')
                # void_cyl = openmc.ZCylinder(r=outer_cyl_4.r+50, boundary_type='vacuum')

                libra_bot_plane = shield_bot_plane_1
                libra_top_plane = shield_top_plane_2
                libra_out_cyl = shield_out_cyl


                ## Calculate Salt Volume
                # Calculate area of quarter ring
                ring_area = np.pi/4 * (outer_cyl_1.r**2 - inner_cyl_4.r**2)
                # Calculate area of x cutoff strip
                x_cutoff_area = circle_strip_area(x_plane_4.x0, outer_cyl_1.r) \
                              - circle_strip_area(x_plane_4.x0, inner_cyl_4.r)
                # Calculate area of y cutoff strip
                y_cutoff_area = circle_strip_area(y_plane_4.y0, outer_cyl_1.r) \
                              - circle_strip_area(y_plane_4.y0, inner_cyl_4.r)
                # Calculate circular quadrant cross sectional area
                quadrant_xs_area = ring_area - x_cutoff_area - y_cutoff_area

                # Calculate total salt volume without reentrant tubes
                quadrant_salt_volume = quadrant_xs_area * salt_height
                center_tank_salt_volume = center_tank_cyl_1.r**2 * np.pi \
                                        * (center_tank_salt_top_plane.z0 - center_tank_bot_plane_4.z0)
                salt_volume = quadrant_salt_volume * 4 + center_tank_salt_volume

                # if salt_height==95 and salt_thickness==36:
                #     print('Ring Area = {}'.format(ring_area))
                #     print('x_cutoff_area = {}'.format(x_cutoff_area))
                #     print('y_cutoff_area = {}'.format(y_cutoff_area))
                #     print('quadrant_xs_area = {}'.format(quadrant_xs_area))
                #     print('quadrant_salt_volume = {}'.format(quadrant_salt_volume))
                #     print('center tank salt height = {}'.format(center_tank_salt_top_plane.z0 - center_tank_bot_plane_4.z0))
                #     print('center_tank_salt_volume = {}'.format(center_tank_salt_volume))
                #     print('center tank inner radius = {}'.format(center_tank_cyl_1.r))
                ####### Regions and Cells ###############

                gen_1_region = generator_region.rotate((0,180,0))
                gen_1_region = gen_1_region.translate((0, 0, source_z_point + 12))

                gen_1_cell = openmc.Cell(region=gen_1_region, fill=gen_universe, name='DT Generator 1')
                gen_1_cell.rotation = (0, 180, 0)
                gen_1_cell.translation = (0, 0, source_z_point + 12 )

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
                                    & +y_plane_3 & +x_plane_3
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
                                & +y_plane_4 & +x_plane_4 \
                                & +z_plane_3 & -double_wall_top_plane_1
                # bottom region
                inner_wall_reg_bot = +z_plane_3 & -z_plane_4 \
                                    & +inner_cyl_4 & -outer_cyl_1 \
                                    & +y_plane_4 & +x_plane_4
                # overall region
                inner_wall_reg = inner_wall_reg_1 | inner_wall_reg_hor \
                                | inner_wall_reg_ver | inner_wall_reg_2 | inner_wall_reg_bot
                inner_wall_cell = openmc.Cell(region=inner_wall_reg, fill=inconel625, name='tank inner wall')



                ## Inner tank top cover
                inner_tank_cover_reg = +tank_top_cover_plane_1 & -tank_top_cover_plane_2 \
                                        & +x_plane_4 & +y_plane_4 & +inner_cyl_4 & -outer_cyl_1

                inner_tank_cover_cell = openmc.Cell(region=inner_tank_cover_reg, fill=inconel625,
                                                    name='Inner Tank Top Cover')
                top_air_1_reg = +tank_top_cover_plane_2 & -salt_gas_tube_top_plane\
                              & +x_plane_4 & +y_plane_4 & +inner_cyl_4 & -outer_cyl_1 

                ## Outer tank top cover
                # Inner region
                outer_tank_cover_reg_1 = +inner_cyl_1 & -inner_cyl_4 \
                                & +y_plane_4 & +x_plane_4 \
                                & +double_wall_top_plane_1 & -double_wall_top_plane_2
                top_air_2_reg_1 = +inner_cyl_1 & -inner_cyl_4 \
                                & +y_plane_4 & +x_plane_4 \
                                & +double_wall_top_plane_2 & -salt_gas_tube_top_plane
                # horizontal region
                outer_tank_cover_reg_hor = +y_plane_1 & -y_plane_4 \
                                & +inner_cyl_1 & -outer_cyl_4 & +x_plane_1 \
                                & +double_wall_top_plane_1 & -double_wall_top_plane_2
                top_air_2_reg_hor = +y_plane_1 & -y_plane_4 \
                                & +inner_cyl_1 & -outer_cyl_4 & +x_plane_1 \
                                & +double_wall_top_plane_2 & -salt_gas_tube_top_plane
                # vertical region
                outer_tank_cover_reg_ver = +x_plane_1 & -x_plane_4 \
                                & +inner_cyl_1 & -outer_cyl_4 & +y_plane_1 \
                                & +double_wall_top_plane_1 & -double_wall_top_plane_2
                top_air_2_reg_ver = +x_plane_1 & -x_plane_4 \
                                & +inner_cyl_1 & -outer_cyl_4 & +y_plane_1 \
                                & +double_wall_top_plane_2 & -salt_gas_tube_top_plane
                # outer region
                outer_tank_cover_reg_2 = +outer_cyl_1 & -outer_cyl_4 \
                                & +y_plane_4 & +x_plane_4 \
                                & +double_wall_top_plane_1 & -double_wall_top_plane_2
                top_air_2_reg_2 = +outer_cyl_1 & -outer_cyl_4 \
                                & +y_plane_4 & +x_plane_4 \
                                & +double_wall_top_plane_2 & -salt_gas_tube_top_plane
                top_air_3_reg = -outer_cyl_1 & +center_tank_top_plane_2 & -salt_gas_tube_top_plane

                top_air_reg = top_air_1_reg | top_air_2_reg_1 | top_air_2_reg_2 \
                            | top_air_2_reg_hor | top_air_2_reg_ver | top_air_3_reg

                outer_tank_cover_reg = outer_tank_cover_reg_1 | outer_tank_cover_reg_hor \
                                    | outer_tank_cover_reg_ver | outer_tank_cover_reg_2
                outer_tank_cover_cell = openmc.Cell(region=outer_tank_cover_reg, fill=inconel625,
                                                    name='Outer Tank Top Cover')

                ## Salt region and cell
                salt_reg = +inner_cyl_4 & -outer_cyl_1 & +x_plane_4 & +y_plane_4 \
                            & +z_plane_4 & -salt_top_plane 
                salt_cell = openmc.Cell(region=salt_reg, fill=salt_material, name='Salt')

                ## Inner tank air
                inner_tank_air_reg = +inner_cyl_4 & -outer_cyl_1 & +x_plane_4 & +y_plane_4 \
                            & +salt_top_plane & -tank_top_cover_plane_1 
                inner_tank_air_cell = openmc.Cell(region=inner_tank_air_reg, fill=air, name='Inner Tank Headspace')

                ## Multiplier
                # multiplier_inner_cyl = openmc.ZCylinder(r=starting_radius_1)
                # multiplier_outer_cyl = openmc.ZCylinder(r=multiplier_inner_cyl.r +multiplier_thickness)
                multiplier_outer_cyl = openmc.ZCylinder(r=inner_cyl_1.r)
                multiplier_inner_cyl = openmc.ZCylinder(r=inner_cyl_1.r - multiplier_thickness)
                multiplier_reg = (+multiplier_inner_cyl & -multiplier_outer_cyl & +multiplier_bot_plane & -multiplier_top_plane_1) \
                                | (-multiplier_outer_cyl & +multiplier_top_plane_1 & -multiplier_top_plane_2)
                multiplier_cell = openmc.Cell(region=multiplier_reg, fill=multiplier_material, name='Multiplier')

                ### Center Tank Regions and Cells
                center_tank_out_gap_reg = -inner_cyl_1 & +center_tank_bot_plane_1 & -center_tank_top_plane_2 & +center_tank_cyl_4
                center_tank_out_gap_cell = openmc.Cell(region=center_tank_out_gap_reg, fill=air, name='Center Tank Outer Gap')

                center_tank_out_wall_reg = (-center_tank_cyl_4 & +center_tank_top_plane_1 & -center_tank_top_plane_2) \
                                         | (-center_tank_cyl_4 & +center_tank_cyl_3 & +center_tank_bot_plane_2 & -center_tank_top_plane_1) \
                                         | (-center_tank_cyl_4 & +center_tank_bot_plane_1 & -center_tank_bot_plane_2)
                center_tank_out_wall_cell = openmc.Cell(region=center_tank_out_wall_reg, fill=inconel625, name='center tank outer wall')

                center_tank_in_gap_reg = (-center_tank_cyl_3 & +center_tank_cyl_2 & +center_tank_bot_plane_3 & -center_tank_top_plane_1) \
                                       | (-center_tank_cyl_3 & +center_tank_bot_plane_2 & -center_tank_bot_plane_3)
                center_tank_in_gap_cell = openmc.Cell(region=center_tank_in_gap_reg, fill=air, name='center tank inner gap')

                center_tank_in_wall_reg = (-center_tank_cyl_2 & +center_tank_cyl_1 & +center_tank_bot_plane_3 & -center_tank_top_plane_1) \
                                        | (-center_tank_cyl_2 & +center_tank_bot_plane_3 & -center_tank_bot_plane_4)
                center_tank_in_wall_cell = openmc.Cell(region=center_tank_in_wall_reg, fill=inconel625, name='center tank inner wall')


                center_tank_salt_reg = (-center_tank_cyl_1 & +center_tank_bot_plane_4 & -center_tank_salt_top_plane)

                center_tank_salt_cell = openmc.Cell(region=center_tank_salt_reg, fill=salt_material, name='center tank salt')

                center_tank_headspace_reg = -center_tank_cyl_1 & +center_tank_salt_top_plane & -center_tank_top_plane_1
                center_tank_headspace_cell = openmc.Cell(region=center_tank_headspace_reg, fill=air, name='center tank headspace')


                lead_shield_reg = (-shield_in_cyl & +lead_shield_in_cyl & +z_plane_1 & -lead_shield_top_plane_1) \
                                  | (-shield_in_cyl & +lead_shield_top_plane_1 & -lead_shield_top_plane_2)
                lead_shield_cell = openmc.Cell(region=lead_shield_reg, fill=SS304, name='lead shield')

                inner_air_reg = -inner_cyl_1 & -center_tank_bot_plane_1 & +shield_bot_plane_1 & +x_plane_1 & +y_plane_1 \
                                & ~multiplier_reg & ~gen_1_region
                inner_air_cell = openmc.Cell(fill=air, region=inner_air_reg, name='Inner Air')



                # libra_outside_air_reg = -outer_cyl_4 & +z_plane_1 & -salt_gas_tube_top_plane & +x_plane_1 & +y_plane_1 \
                #                 & ~out_wall_reg & ~wall_gap_reg & ~inner_wall_reg \
                #                 & ~salt_reg & ~inner_tank_air_reg \
                #                 & ~outer_tank_cover_reg \
                #                 & ~inner_tank_cover_reg & ~fill_tube_reg \
                #                 & ~heater_overall_1_reg & ~heater_overall_2_reg \
                #                 & ~heater_overall_3_reg \
                #                 & ~salt_gas_tube_1_reg & ~salt_gas_tube_2_reg \
                #                 & ~thermocouple_tube_1_reg & ~thermocouple_tube_2_reg \
                #                 & ~thermocouple_tube_3_reg \
                #                 & ~multiplier_reg
                libra_outside_air_reg = top_air_reg

                libra_outside_air_cell = openmc.Cell(region=libra_outside_air_reg, fill=air, name='LIBRA Outside Air')

                support_plate_reg = +inner_cyl_1 & -shield_in_cyl & +support_plate_bot_plane & -z_plane_1
                support_plate_cell = openmc.Cell(region=support_plate_reg, fill=steel_lowC, name='Support Plate')

                libra_insulation_reg = (+outer_cyl_4 & -lead_shield_in_cyl & +support_plate_bot_plane & -shield_top_plane_1) \
                                     | (+inner_cyl_1 & -shield_in_cyl & +shield_bot_plane_2 & -support_plate_bot_plane)
                libra_insulation_cell = openmc.Cell(region=libra_insulation_reg, fill=air, name='LIBRA insulation')

                libra_shielding_reg = (-shield_out_cyl & +shield_top_plane_1 & -shield_top_plane_2 & +x_plane_1 & +y_plane_1) \
                                    | (-shield_out_cyl & +shield_in_cyl & +shield_bot_plane_2 & -shield_top_plane_1 & +x_plane_1 & +y_plane_1) \
                                    | (-shield_out_cyl & +inner_cyl_1 & +shield_bot_plane_1 & -shield_bot_plane_2 & +x_plane_1 & +y_plane_1)
                libra_shielding_cell = openmc.Cell(region=libra_shielding_reg, fill=reflector_material, name='LIBRA Shield')
                # print(libra_shielding_cell.fill.name)

                    # void region
                libra_quarter_1_reg = -libra_out_cyl & +libra_bot_plane & -libra_top_plane & +x_plane_1 & +y_plane_1

                libra_quarter_1_cells = [out_wall_cell, wall_gap_cell, inner_wall_cell,
                        inner_tank_cover_cell, outer_tank_cover_cell,
                        salt_cell, inner_tank_air_cell,
                        multiplier_cell, 
                        center_tank_out_gap_cell, center_tank_out_wall_cell,
                        center_tank_in_gap_cell, center_tank_in_wall_cell,
                        center_tank_salt_cell, center_tank_headspace_cell,
                        inner_air_cell,
                        libra_outside_air_cell,
                        support_plate_cell, libra_insulation_cell, 
                        lead_shield_cell, libra_shielding_cell,
                        gen_1_cell]
                libra_quarter_1_universe = openmc.Universe(cells=libra_quarter_1_cells)

                libra_quarter_1_cell = openmc.Cell(region=libra_quarter_1_reg, 
                                                    fill=libra_quarter_1_universe, name='Quad 1')

                libra_quarter_2_reg = libra_quarter_1_reg.rotate((0,0,90))
                libra_quarter_2_cell = openmc.Cell(region=libra_quarter_2_reg, 
                                                    fill=libra_quarter_1_universe, name='Quad 2')
                libra_quarter_2_cell.rotation = [0.0, 0.0, 90.0]

                libra_quarter_3_reg = libra_quarter_1_reg.rotate((0,0,180))
                libra_quarter_3_cell = openmc.Cell(region=libra_quarter_3_reg, 
                                                    fill=libra_quarter_1_universe, name='Quad 3')
                libra_quarter_3_cell.rotation = [0.0, 0.0, 180.0]

                libra_quarter_4_reg = libra_quarter_1_reg.rotate((0,0,270))
                libra_quarter_4_cell = openmc.Cell(region=libra_quarter_4_reg, 
                                                    fill=libra_quarter_1_universe, name='Quad 4')
                libra_quarter_4_cell.rotation = [0.0, 0.0, 270.0]

                libra_universe = openmc.Universe(cells=[libra_quarter_1_cell, libra_quarter_2_cell, 
                                                        libra_quarter_3_cell, libra_quarter_4_cell]) 

                libra_reg = -libra_out_cyl & +libra_bot_plane & -libra_top_plane 
                libra_system_cell = openmc.Cell(fill=libra_universe, region=libra_reg, name='LIBRA')

                floor_reg = -floor_rpp
                floor_cell = openmc.Cell(fill=Concrete, region=floor_reg, name='floor')

                room_air_reg = +floor_rpp.zmax & -boundary_top_plane \
                             & +floor_rpp.xmin & -floor_rpp.xmax \
                             & +floor_rpp.ymin & -floor_rpp.ymax \
                             & ~libra_reg
                room_air_cell = openmc.Cell(fill=air, region=room_air_reg, name='Room Air' )

                universe = openmc.Universe(cells=[libra_system_cell, floor_cell, room_air_cell])

                geometry = openmc.Geometry(universe)

                ### Source

                point = openmc.stats.Point((0.01, 0.01, source_z_point))
                src = openmc.IndependentSource(space=point)
                src.energy = openmc.stats.Discrete([14.1E6], [1.0])
                src.strength = 1.0

                # vol = openmc.VolumeCalculation(domains=cells, samples=int(1e7))
                settings = openmc.Settings()
                settings.run_mode = 'fixed source'
                settings.source = src
                settings.batches = 100
                settings.inactive = 0
                settings.particles = int(1e5)
                # settings.volume_calculations = [vol]
                # settings.photon_transport = True
                settings.photon_transport = False

                t_tally = openmc.Tally(name='tritium tally')
                salt_filter = openmc.MaterialFilter([salt_material])
                salt_cell_filter = openmc.CellFilter([center_tank_salt_cell, salt_cell])
                t_tally.filters.append(salt_filter)
                t_tally.filters.append(salt_cell_filter)
                t_tally.scores = ['(n,Xt)']

                t_li_tally = openmc.Tally(name='tritium lithium tally')
                t_li_tally.filters.append(salt_filter)
                t_li_tally.nuclides = ['Li6', 'Li7']
                t_li_tally.scores = ['(n,Xt)']


                tallies = openmc.Tallies([t_tally, t_li_tally])

                if __name__ == '__main__':
                    curr_dir = os.getcwd()

                    salt_directory = salt_material.name
                    multiplier_directory = 'm={}_{}_r={}_{}'.format(multiplier_thickness,
                                                                    multiplier_material.name, 
                                                                    reflector_thickness,
                                                                    reflector_material.name)
                    height_directory = 'height={:.0f}cm'.format(salt_height)
                    thickness_directory = 'th={:.0f}cm'.format(salt_thickness)

                    directories = [salt_directory, multiplier_directory, height_directory, thickness_directory]
                    directory = ''
                    for d in directories:
                        directory = os.path.join(directory, d)
                        if not os.path.isdir(directory):
                            os.mkdir(directory)
                    os.chdir(directory)
                    print(directory)
                    model = openmc.Model(geometry=geometry, materials=materials,
                                        settings=settings, tallies=tallies)
                    model.export_to_xml()

                    # openmc.calculate_volumes()
                    # vol_calc = openmc.VolumeCalculation.from_hdf5('volume_1.h5')
                    # print(vol_calc.volumes)
                    if not os.path.isfile('statepoint.100.h5'):
                        openmc.run(threads=16)

                    sp = openmc.StatePoint('statepoint.100.h5')
                    t_tally = sp.get_tally(name='tritium tally')
                    tbrs[i,r,j,k] = np.sum(t_tally.get_reshaped_data(value='mean').squeeze())

                    salt_volumes[i,r,j,k] = salt_volume

                    os.chdir(curr_dir)



## Calculate Reference Case Salt Volume
# Calculate area of quarter ring
inner_radius = 15.24
outer_radius = inner_radius + reference_thickness
ring_area = np.pi/4 * ((outer_radius)**2 - inner_radius**2)
# Calculate area of x cutoff strip
x_cutoff_area = circle_strip_area(x_plane_4.x0, outer_radius) \
              - circle_strip_area(x_plane_4.x0, inner_radius)
# Calculate area of y cutoff strip
y_cutoff_area = circle_strip_area(y_plane_4.y0, outer_radius) \
              - circle_strip_area(y_plane_4.y0, inner_radius)
# Calculate circular quadrant cross sectional area
quadrant_xs_area = ring_area - x_cutoff_area - y_cutoff_area

# Center tank volume
reference_center_bot_z = z_plane_4.z0 + reference_salt_height/2 + 14 + 5
reference_center_top_z = z_plane_4.z0 + reference_salt_height
reference_center_radius = 13.34 - 0.2 - 2*libra_wall_th - gap_thickness
reference_center_vol = reference_center_radius**2 * np.pi * (reference_center_top_z - reference_center_bot_z)
print('Center Tank Reference Volume = {:.2e} cc'.format(reference_center_vol))
# Calculate total salt volume without reentrant tubes
quadrant_salt_volume = quadrant_xs_area * reference_salt_height
print('Quadrant Reference Volume = {:.2e} cc'.format(quadrant_salt_volume))
reference_salt_volume = quadrant_salt_volume * 4 + reference_center_vol
print('\n Reference Design Volume: {:.2e} cc'.format(reference_salt_volume))

# print('Ring Area = {}'.format(ring_area))
# print('x_cutoff_area = {}'.format(x_cutoff_area))
# print('y_cutoff_area = {}'.format(y_cutoff_area))
# print('quadrant_xs_area = {}'.format(quadrant_xs_area))
# print('quadrant_salt_volume = {}'.format(quadrant_salt_volume))
# print('reference_center_vol = {}'.format(reference_center_vol))
# print('center tank salt height = {}'.format(reference_center_top_z - reference_center_bot_z))
# print('center tank inner radius = {}'.format(reference_center_radius))

xmesh, ymesh = np.meshgrid(salt_thicknesses, salt_heights)

tbr_levs = [0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15]

for i,salt_mat in enumerate(salt_materials):
    for r,reflector_thickness in enumerate(reflector_thicknesses):
        fig, ax = plt.subplots(figsize=[6,5])
        cntr = ax.contourf(xmesh, ymesh, tbrs[i,r,:,:], levels=tbr_levs, cmap='plasma', alpha=1.0)
        conlines = ax.contour(xmesh, ymesh, tbrs[i,r,:,:], levels=tbr_levs,
                            colors=['black'])
        ax.clabel(conlines, conlines.levels, inline=True, fmt='TBR=%.2f')
        cbar = plt.colorbar(cntr)
        cbar.set_label(label='TBR')

        # Plot volume
        vol_conlines = ax.contour(xmesh, ymesh, salt_volumes[i,r,:,:], levels=5, colors=['white'])
        ax.clabel(vol_conlines, vol_conlines.levels, inline=True, fmt='vol=%.1e')

        # Plot reference point
        ax.plot(reference_thickness, reference_salt_height, '.', ms=10, color='limegreen')

        ax.set_xlabel('Salt Thickness [cm]', fontsize=12)
        ax.set_ylabel('Salt Height [cm]', fontsize=12) 

        multiplier_directory = 'm={}_{}_r={}_{}'.format(multiplier_thickness,
                                                                    multiplier_material.name, 
                                                                    reflector_thickness,
                                                                    reflector_material.name)
        ax.set_title('{}, {} cm {}, {} cm {}'.format(salt_mat.name,
                                                     multiplier_thickness,
                                                     multiplier_material.name,
                                                     reflector_thickness,
                                                     reflector_material.name))
        fig.savefig('{}_{}_size_scan_2.png'.format(salt_mat.name, multiplier_directory))

plt.show()







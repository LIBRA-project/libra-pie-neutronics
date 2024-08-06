import openmc 
import numpy as np 

def build_vault_model(settings=openmc.Settings(), tallies=openmc.Tallies(),
                      added_cells=[], added_materials=[], overall_exclusion_region=None):
    #
    # **** Natural elements ****
    #
    # Aluminum : 2.6989 g/cm3
    Aluminum = openmc.Material() 
    Aluminum.set_density('g/cm3', 2.6989) 
    Aluminum.add_nuclide('Al27', 1.0, 'ao') 

    # Copper : 8.96 g/cm3
    Material_2 = openmc.Material() 
    Material_2.set_density('g/cm3', 8.96) 
    Material_2.add_nuclide('Cu63', 0.6917, 'ao') 
    Material_2.add_nuclide('Cu65', 0.3083, 'ao') 

    # Name: Air
    # Density : 0.001205 g/cm3
    # Reference: None
    # Describes: All atmospheric, non-object chambers
    Air = openmc.Material() 
    Air.set_density('g/cm3', 0.001205) 
    Air.add_element('C', 0.00015, 'ao') 
    Air.add_nuclide('N14', 0.784431, 'ao') 
    Air.add_nuclide('O16', 0.210748, 'ao') 
    Air.add_nuclide('Ar40', 0.004671, 'ao') 

    # Name: Portland concrete
    # Density: 2.3 g/cm3
    # Reference: PNNL Report 15870 (Rev. 1)
    # Describes: facility foundation, floors, walls
    Concrete = openmc.Material() 
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

    # Name: Portland iron concrete
    # Density: 3.8 g/cm3 as roughly measured using scale and assuming rectangular prism
    # Reference: PNNL Report 15870 (Rev. 1)
    # Describes: Potential new walls, shielding doors
    IronConcrete = openmc.Material() 
    IronConcrete.set_density('g/cm3', 3.8) 
    IronConcrete.add_nuclide('H1', 0.135585, 'ao') 
    IronConcrete.add_nuclide('O16', 0.150644, 'ao') 
    IronConcrete.add_element('Mg', 0.002215, 'ao') 
    IronConcrete.add_nuclide('Al27', 0.005065, 'ao') 
    IronConcrete.add_element('Si', 0.013418, 'ao') 
    IronConcrete.add_element('S', 0.000646, 'ao') 
    IronConcrete.add_element('Ca', 0.040919, 'ao') 
    IronConcrete.add_nuclide('Mn55', 0.002638, 'ao') 
    IronConcrete.add_element('Fe', 0.648869, 'ao') 

    # Name: Stainless steel 304
    # Density: 8.0 g/cm3
    # Reference: PNNL Report 15870 (Rev. 1)
    # Describes: vacuum pipes, flanges, general steel objects
    Material_6 = openmc.Material() 
    Material_6.set_density('g/cm3', 8.0) 
    Material_6.add_element('C', 0.00183, 'ao') 
    Material_6.add_element('Si', 0.009781, 'ao') 
    Material_6.add_nuclide('P31', 0.000408, 'ao') 
    Material_6.add_element('S', 0.000257, 'ao') 
    Material_6.add_element('Cr', 0.200762, 'ao') 
    Material_6.add_nuclide('Mn55', 0.010001, 'ao') 
    Material_6.add_element('Fe', 0.690375, 'ao') 
    Material_6.add_element('Ni', 0.086587, 'ao') 

    # Name: Wood (Southern Pine)
    # Density: 0.64 g/cm3
    # Reference: PNNL Report 15870 (Rev. 1)
    # Describes: doors
    Material_7 = openmc.Material() 
    Material_7.set_density('g/cm3', 0.64) 
    Material_7.add_nuclide('H1', 0.462423, 'ao') 
    Material_7.add_element('C', 0.323389, 'ao') 
    Material_7.add_nuclide('N14', 0.002773, 'ao') 
    Material_7.add_nuclide('O16', 0.208779, 'ao') 
    Material_7.add_element('Mg', 0.000639, 'ao') 
    Material_7.add_element('S', 0.001211, 'ao') 
    Material_7.add_element('K', 0.000397, 'ao') 
    Material_7.add_element('Ca', 0.000388, 'ao') 

    # Name: Gypsum (wallboard)
    # Density: 2.32 g/cm3
    # Reference: PNNL Report 15870 (Rev. 1)
    # Describes: drywall walls (GWB)
    Material_8 = openmc.Material() 
    Material_8.set_density('g/cm3', 2.32) 
    Material_8.add_nuclide('H1', 0.333321, 'ao') 
    Material_8.add_nuclide('O16', 0.500014, 'ao') 
    Material_8.add_element('S', 0.083324, 'ao') 
    Material_8.add_element('Ca', 0.083341, 'ao') 

    # **** Gamma shielding materials ****
    #
    # Tungsten : 19.3 g/cm3
    Material_10 = openmc.Material() 
    Material_10.set_density('g/cm3', 19.3) 
    Material_10.add_nuclide('W182', 0.265, 'ao') 
    Material_10.add_nuclide('W183', 0.1431, 'ao') 
    Material_10.add_nuclide('W184', 0.3064, 'ao') 
    Material_10.add_nuclide('W186', 0.2855, 'ao') 

    #
    # Lead : 11.34 g/cm3
    Lead = openmc.Material() 
    Lead.set_density('g/cm3', 11.34) 
    Lead.add_nuclide('Pb204', 0.014, 'ao') 
    Lead.add_nuclide('Pb206', 0.241, 'ao') 
    Lead.add_nuclide('Pb207', 0.221, 'ao') 
    Lead.add_nuclide('Pb208', 0.524, 'ao') 

    # Name: Borated Polyethylene (5% B in via B4C additive)
    # Density: 0.95 g/cm3
    # Reference: PNNL Report 15870 (Rev. 1) but revised to make it 5 wt.% B
    # Describes: General purpose neutron shielding
    BPE = openmc.Material() 
    BPE.set_density('g/cm3', 0.95) 
    BPE.add_nuclide('H1', 0.1345, 'wo') 
    BPE.add_element('B', 0.0500, 'wo') 
    BPE.add_element('C', 0.8155, 'wo')

    # Name: Non-borated polyethylene
    # Density: 0.93 g/cm3
    # Reference: PNNL Report 15870 (Rev. 1)
    # Describes: General purpose neutron shielding
    Polyethylene = openmc.Material() 
    Polyethylene.set_density('g/cm3', 0.93) 
    Polyethylene.add_nuclide('H1', 0.666662, 'ao') 
    Polyethylene.add_element('C', 0.333338, 'ao') 

    # High Density Polyethylene
    # Reference:  PNNL Report 15870 (Rev. 1)
    HDPE = openmc.Material(name='HDPE')
    HDPE.set_density('g/cm3', 0.95)
    HDPE.add_element('H', 0.143724, 'wo')
    HDPE.add_element('C', 0.856276, 'wo')

    # Name: Zirconium dihydride
    # Density: 5.6 g/cm3
    # Reference: JNM 386-388 (2009) 119-121
    # Describes: General purpose neutron shielding
    Material_22 = openmc.Material() 
    Material_22.set_density('g/cm3', 5.6) 
    Material_22.add_nuclide('H1', 0.0216, 'wo') 
    Material_22.add_element('Zr', 0.9784, 'wo') 

    # Name: Zirconium borohydride
    # Density: 1.18 g/cm3
    # Reference: JNM 386-388 (2009) 119-121
    # Describes: General purpose neutron shielding
    Material_23 = openmc.Material() 
    Material_23.set_density('g/cm3', 1.18) 
    Material_23.add_nuclide('H1', 0.1073, 'wo') 
    Material_23.add_nuclide('B10', 0.0571, 'wo') 
    Material_23.add_nuclide('B11', 0.23, 'wo') 
    Material_23.add_element('Zr', 0.6056, 'wo') 

    # Density: 1.848 g/cm3
    # Reference: None
    # Describes: Highest intenstiy neutron production target
    # Notes: Uses ENDF-derived proton nuclear data libray
    Material_30 = openmc.Material() 
    Material_30.set_density('g/cm3', 1.848) 
    Material_30.add_nuclide('Be9', 1.0, 'ao') 

    # Name: Concrete (Regular)
    # Density: 2.3 g/cm3
    # Reference: Provided by Matthey Carey, MIT EHS/RPP (mgcarey@mit.edu)
    # Describes: Facility walls, foundation, floors for activation calculations
    Material_40 = openmc.Material() 
    Material_40.set_density('g/cm3', 2.3) 
    Material_40.add_nuclide('Fe54', 2.0138e-05, 'ao') 
    Material_40.add_nuclide('Fe56', 0.00031874, 'ao') 
    Material_40.add_nuclide('Fe57', 7.2915e-06, 'ao') 
    Material_40.add_nuclide('Fe58', 1.0416e-06, 'ao') 
    Material_40.add_nuclide('H1', 0.01374, 'ao') 
    Material_40.add_nuclide('H2', 2.0613e-06, 'ao') 
    Material_40.add_nuclide('O16', 0.045685, 'ao') 
    Material_40.add_nuclide('O17', 1.8318e-05, 'ao') 
    Material_40.add_nuclide('Mg24', 9.0027e-05, 'ao') 
    Material_40.add_nuclide('Mg25', 1.1397e-05, 'ao') 
    Material_40.add_nuclide('Mg26', 1.2548e-05, 'ao') 
    Material_40.add_nuclide('Ca40', 0.001474, 'ao') 
    Material_40.add_nuclide('Ca42', 9.8378e-06, 'ao') 
    Material_40.add_nuclide('Ca43', 2.0527e-06, 'ao') 
    Material_40.add_nuclide('Ca44', 3.1718e-05, 'ao') 
    Material_40.add_nuclide('Ca46', 6.0821e-08, 'ao') 
    Material_40.add_nuclide('Ca48', 2.8434e-06, 'ao') 
    Material_40.add_nuclide('Si28', 0.015328, 'ao') 
    Material_40.add_nuclide('Si29', 0.00077613, 'ao') 
    Material_40.add_nuclide('Si30', 0.0005152, 'ao') 
    Material_40.add_nuclide('Na23', 0.00096395, 'ao') 
    Material_40.add_nuclide('K39', 0.00042949, 'ao') 
    Material_40.add_nuclide('K40', 4.6053e-08, 'ao') 
    Material_40.add_nuclide('K41', 3.0993e-05, 'ao') 
    Material_40.add_nuclide('Al27', 0.0017453, 'ao') 
    Material_40.add_nuclide('C12', 0.00011404, 'ao') 
    Material_40.add_nuclide('C13', 1.28e-06, 'ao') 

    # Soil material taken from PNNL Materials Compendium for Earth, U.S. Average
    Soil = openmc.Material(name='Soil')
    Soil.set_density('g/cm3', 1.52)
    Soil.add_element('O', 0.670604, percent_type='ao')
    Soil.add_element('Na', 0.005578, percent_type='ao')
    Soil.add_element('Mg', 0.011432 , percent_type='ao')
    Soil.add_element('Al', 0.053073, percent_type='ao')
    Soil.add_element('Si', 0.201665, percent_type='ao')
    Soil.add_element('K', 0.007653, percent_type='ao')
    Soil.add_element('Ca', 0.026664, percent_type='ao')
    Soil.add_element('Ti', 0.002009, percent_type='ao')
    Soil.add_element('Mn', 0.000272, percent_type='ao')
    Soil.add_element('Fe', 0.021050, percent_type='ao')


    # Brick material taken from "Brick, Common Silica" from the PNNL Materials Compendium
    # PNNL-15870, Rev. 2
    Brick=openmc.Material(name='Brick')
    Brick.set_density('g/cm3', 1.8)
    Brick.add_element('O', 0.663427, percent_type='ao')
    Brick.add_element('Al', 0.003747, percent_type='ao')
    Brick.add_element('Si', 0.323229, percent_type='ao')
    Brick.add_element('Ca', 0.007063, percent_type='ao')
    Brick.add_element('Fe', 0.002534, percent_type='ao')


    # Previous model uses 10% borated high density polyethylene, but 
    # according to Melhus, et. al., RicoRad consists of "2.00% mass boron 
    # in a polyethylene-based matrix having a mass density of 0.945 g/cm^3"
    # Source: 
    # Melhus, Christopher, et al. â€˜Storage Safe Shielding Assessment for a 
    # HDR Californium-252 Brachytherapy Sourceâ€™. 
    # Monte Carlo 2005 Topical Meeting, 01 2005, pp. 219â€“229.

    RicoRad = openmc.Material(name='RicoRad')
    RicoRad.set_density('g/cm3', 0.945)
    RicoRad.add_element('H', 0.14, percent_type='wo')
    RicoRad.add_element('C', 0.84, percent_type='wo')
    RicoRad.add_element('B', 0.02, percent_type='wo')

    ### LIBRA Materials
    Steel = openmc.Material(name="Steel")
    Steel.add_element('C',  0.005, "wo")
    Steel.add_element('Fe', 0.995, "wo")
    Steel.set_density("g/cm3", 7.82)

    # Stainless Steel 304 from PNNL Materials Compendium (PNNL-15870 Rev2)
    SS304 = openmc.Material(name="Stainless Steel 304")
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

    # Using Microtherm with 1 a% Al2O3, 27 a% ZrO2, and 72 a% SiO2
    # https://www.foundryservice.com/product/microporous-silica-insulating-boards-mintherm-microtherm-1925of-grades/
    Firebrick = openmc.Material(name="Firebrick")
    # Estimate average temperature of Firebrick to be around 300 C
    # Firebrick.temperature = 273 + 300
    Firebrick.add_element('Al', 0.004, 'ao')
    Firebrick.add_element('O', 0.666, 'ao')
    Firebrick.add_element('Si', 0.240, 'ao')
    Firebrick.add_element('Zr', 0.090, 'ao')
    Firebrick.set_density('g/cm3', 0.30)

    # Using 2:1 atom ratio of LiF to BeF2, similar to values in 
    # Seifried, Jeffrey E., et al. â€˜A General Approach for Determination of 
    # Acceptable FLiBe Impurity Concentrations in Fluoride-Salt Cooled High 
    # Temperature Reactors (FHRs)â€™. Nuclear Engineering and Design, vol. 343, 2019, 
    # pp. 85â€“95, https://doi.org10.1016/j.nucengdes.2018.09.038.
    # Also using natural lithium enrichment (~7.5 a% Li6)
    Flibe_nat = openmc.Material(name='Flibe_nat')
    # Flibe_nat.temperature = 700 + 273
    Flibe_nat.add_element('Be', 0.142857, 'ao')
    Flibe_nat.add_nuclide('Li6', 0.021685, 'ao')
    Flibe_nat.add_nuclide('Li7', 0.264029, 'ao')
    Flibe_nat.add_element('F', 0.571429, 'ao')
    Flibe_nat.set_density("g/cm3", 1.94)

    Copper = openmc.Material(name="Copper")
    # Estimate copper temperature to be around 100 C
    # Copper.temperature = 100 + 273
    Copper.add_element('Cu', 1.0, "ao")
    Copper.set_density("g/cm3", 8.96)

    Be = openmc.Material(name="Be")
    # Estimate Be temperature to be around 100 C
    # Be.temperature = 100 + 273
    Be.add_element('Be', 1.0, 'ao')
    Be.set_density('g/cm3', 1.848)


    materials = openmc.Materials([Aluminum, Material_2, Air, Concrete, 
                IronConcrete, Material_6, Material_7, Material_8, Material_10, 
                Lead, BPE, Polyethylene, HDPE, Material_22, Material_23, 
                Material_30, Material_40, Soil, Brick, RicoRad, Steel, SS304, Firebrick, 
                Flibe_nat, Copper, Be]) 

    # Add materials from imported model
    for mat in added_materials:
        materials.append(mat)


    #
    # Definition of the spherical void/blackhole boundary
    Surface_95 = openmc.Sphere(x0=1000.0, y0=1000.0, z0=0.0, r=2500.0, boundary_type='vacuum')

    # Explicit declaration of the outer void
    Region_1000 = +Surface_95  
    Cell_1000 = openmc.Cell(fill=None, region=Region_1000) 

    # 7
    # Surface box used to cutout Room III from the basement ceiling cell
    Surface_7 = openmc.model.RectangularParallelepiped(1023.62, 2323.62, -50.0, 749.62, 180.0, 280.0)

    #
    # 8
    Surface_8 = openmc.model.RectangularParallelepiped(0.0, 2247.9, 0.0, 1998.37, 213.62, 241.56)

    # 24
    Surface_24 = openmc.model.RectangularParallelepiped(1023.62, 2247.9, 0.0, 749.62, 0.0, 424.18)

    # with an angle of 2.8 degrees. The positive vector points towards the
    # lower-right (Southeast) corner of the geometry
    Surface_49 = openmc.Plane(a=0.99881, b=-0.04885, c=0.0, d=2144.83)

    #
    # 54
    Surface_54 = openmc.model.RectangularParallelepiped(0.0, 2247.9, 749.62, 1998.37, 0.0, 213.62)

    #
    # 93
    Surface_93 = openmc.model.RectangularParallelepiped(0.0, 1023.62, 0.0, 749.62, 0.0, 213.62)

    #
    # Outer surface definition of the foundation underneath all basement labs
    Surface_94 = openmc.model.RectangularParallelepiped(0.0, 2247.9, 0.0, 1998.37, -81.28, 0.0)

    ## Define Soil region
    Soil_south_y = openmc.YPlane(-500)
    Zero_y = openmc.YPlane(0.0)
    Soil_North_y = openmc.YPlane(1200)
    Soil_West_x = openmc.XPlane(0.0)
    Soil_bottom_z = openmc.ZPlane(-100)
    # Ground level is estimated at about 82 inches below top of vault ceiling
    ground_level_z = 425-82*2.54
    Soil_top_z = openmc.ZPlane(ground_level_z)

    # Define Soil cell 3 meters wide
    East_outer_plane = Surface_49.clone()
    East_outer_plane = East_outer_plane.translate([500*np.cos(np.deg2rad(2.8)), 0, 0])

    Soil_region = (+Soil_south_y & -Zero_y & +Soil_West_x & -East_outer_plane & +Soil_bottom_z & -Soil_top_z)
                # | (+Soil_south_y & -Soil_North_y & +Surface_49 & -East_outer_plane & +Soil_bottom_z & -Soil_top_z)
    Soil_cell = openmc.Cell(fill=Soil, region=Soil_region, name='Outer Soil')
    # The "inner void" air sphere surrounding the entire CSTAR geometry
    # inverse of the floor cell
    # inverse of the foundation cell
    # excluding Room II (and "subcells")
    # excluding Room III (and "subcells")          
    # excluding Room IV (and "subcells")

    #
    # 79
    Surface_79 = openmc.model.RectangularParallelepiped(623.62, 1023.62, 217.17, 725.17, 0.0, 10.16)

    # The raised floor in Room IV 
    Region_2 = -Surface_79  
    Cell_2 = openmc.Cell(fill=Concrete, region=Region_2) 

    #
    # 77
    Surface_77 = openmc.model.RectangularParallelepiped(474.98, 479.43, 60.96, 189.23000000000002, 0.0, 213.62)

    #
    # 78
    Surface_78 = openmc.model.RectangularParallelepiped(214.58, 377.14, 745.17, 749.62, 0.0, 213.62)

    #
    # 80
    Surface_80 = openmc.model.RectangularParallelepiped(66.51, 90.96000000000001, 603.99, 658.28, 0.0, 213.62)

    #
    # 81
    Surface_81 = openmc.model.RectangularParallelepiped(0.0, 90.97, 579.54, 603.99, 0.0, 213.62)

    #
    # 85
    Surface_85 = openmc.model.RightCircularCylinder((543.56, 690.03, 0.0), 213.62, 31.75, axis='z')

    #
    # 86
    Surface_86 = openmc.model.RightCircularCylinder((78.74, 690.03, 0.0), 213.62, 31.75, axis='z')

    #
    # 87
    Surface_87 = openmc.model.RightCircularCylinder((543.56, 371.47, 0.0), 213.62, 18.2, axis='z')

    #
    # 88
    Surface_88 = openmc.model.RightCircularCylinder((78.74, 371.47, 0.0), 213.62, 18.2, axis='z')

    #
    # 89
    Surface_89 = openmc.model.RectangularParallelepiped(474.98, 1023.62, 189.23, 217.07, 0.0, 213.62)

    #
    # 90
    Surface_90 = openmc.model.RectangularParallelepiped(0.0, 1023.62, 0.0, 60.96, 0.0, 213.62)

    #
    # 91
    Surface_91 = openmc.model.RectangularParallelepiped(214.58, 377.14, 700.0, 800.0, 0.0, 213.62)

    #
    # 92
    Surface_92 = openmc.model.RectangularParallelepiped(0.0, 1023.62, 725.17, 749.62, 0.0, 213.62)

    # The main air chamber of Room IV 
    Region_3 = -Surface_93 & (+Surface_92 | -Surface_91) & +Surface_89 & +Surface_87 & +Surface_88 & +Surface_90 & +Surface_79 & +Surface_85 & +Surface_86 & +Surface_80 & +Surface_81 & +Surface_78 & +Surface_77  
    Cell_3 = openmc.Cell(fill=Air, region=Region_3) 

    # The north CMU wall in Room IV
    Region_4 = -Surface_92 & +Surface_91  
    Cell_4 = openmc.Cell(fill=Concrete, region=Region_4) 

    # The southern (staircase) CMU wall in Room IV 
    Region_5 = -Surface_89  
    Cell_5 = openmc.Cell(fill=Concrete, region=Region_5) 

    # The south-east pillar in Room IV 
    Region_6 = -Surface_87  
    Cell_6 = openmc.Cell(fill=Concrete, region=Region_6) 

    # The south-west pillar in Room IV
    Region_7 = -Surface_88  
    Cell_7 = openmc.Cell(fill=Concrete, region=Region_7) 

    # The south foundation wall in Room IV 
    Region_8 = -Surface_90  
    Cell_8 = openmc.Cell(fill=Concrete, region=Region_8) 

    #
    # 74
    Surface_74 = openmc.model.RectangularParallelepiped(1304.29, 1326.74, 1183.96, 1698.63, 0.0, 213.62)

    # The CMU wall in Room II separating the Maze from NW13-016  
    Region_9 = -Surface_74  
    Cell_9 = openmc.Cell(fill=Concrete, region=Region_9) 

    #
    # 75
    Surface_75 = openmc.model.RectangularParallelepiped(1256.35, 1304.29, 1183.96, 1208.41, 0.0, 213.62)

    # The CMU wall in Room II separating the Maze from NW13-016 
    Region_10 = -Surface_75  
    Cell_10 = openmc.Cell(fill=Concrete, region=Region_10) 

    #
    # 42
    Surface_42 = openmc.model.RectangularParallelepiped(1231.9, 1256.3500000000001, 810.58, 942.6600000000001, 0.0, 213.62)

    #
    # 76
    Surface_76 = openmc.model.RectangularParallelepiped(1231.9, 1256.3500000000001, 749.62, 1208.41, 0.0, 213.62)

    # The CMU wall in Room II separating the Maze from NW13-016 
    Region_11 = -Surface_76 & +Surface_42  
    Cell_11 = openmc.Cell(fill=Concrete, region=Region_11) 

    #
    # The cuboid defining the outermost boundary of the Vault door in Room III
    Surface_13 = openmc.model.RectangularParallelepiped(1105.41, 1166.3700000000001, 368.0, 611.84, 0.0, 223.52)

    # The plane used to create the 30 degree north-most cut on the Vault door.
    # The positive vector points towards the lower-left
    Surface_14 = openmc.Plane(a=0.5, b=0.86603, c=0.0, d=1084.9)

    # The plane used to create the 30 degree south-most cut on the Vault door
    # the positive vector points towards the upper-left
    Surface_15 = openmc.Plane(a=0.5, b=-0.86603, c=0.0, d=238.93)

    # The main Vault shield door in Room III
    Vault_door_reg = -Surface_13 & -Surface_14 & -Surface_15  
    Vault_door_cell = openmc.Cell(fill=Concrete, region=Vault_door_reg) 

    #
    # North B-HDPE shield in entrance to Vault in Room III
    Surface_17 = openmc.model.RectangularParallelepiped(1066.8, 1104.8999999999999, 565.78, 598.8, 10.16, 213.35999999999999)

    # The northern Ricorad extra Vault door shielding in Room III
    Vault_door_shield_n_pillar_reg = -Surface_17  
    Vault_door_shield_n_pillar_cell = openmc.Cell(fill=RicoRad, region=Vault_door_shield_n_pillar_reg) 

    #
    # South B-HDPE shield in entrance to Vault in Room III
    Surface_18 = openmc.model.RectangularParallelepiped(1066.8, 1104.8999999999999, 380.71, 413.72999999999996, 10.16, 213.35999999999999)

    # The southern Ricorad extra Vault door shielding in Room III 
    Vault_door_shield_s_pillar_reg = -Surface_18  
    Vault_door_shield_s_pillar_cell = openmc.Cell(fill=RicoRad, region=Vault_door_shield_s_pillar_reg) 

    #
    # Surface definition for west iron-brick pile around DANTE selection magnet
    Surface_10 = openmc.model.RectangularParallelepiped(1741.65, 1808.49, 512.12, 637.85, 10.16, 152.4)

    # The western DANTE beamline (Fe or Pb fill?) concrete block shield 
    DANTE_vault_w_shield_reg = -Surface_10  
    DANTE_vault_w_shield_cell = openmc.Cell(fill=IronConcrete, region=DANTE_vault_w_shield_reg) 
    # DANTE_vault_w_shield_cell = openmc.Cell(fill=Air, region=DANTE_vault_w_shield_reg)

    #
    # Surface definition for east iron-brick pile around DANTE selection magnet
    Surface_9 = openmc.model.RectangularParallelepiped(1935.48, 1983.74, 512.12, 637.85, 10.16, 135.89000000000001)

    # The eastern DANTE beamline (Fe or Pb fill?) concrete block shield 
    DANTE_vault_e_shield_reg = -Surface_9  
    DANTE_vault_e_shield_cell = openmc.Cell(fill=IronConcrete, region=DANTE_vault_e_shield_reg) 
    # DANTE_vault_e_shield_cell = openmc.Cell(fill=Air, region=DANTE_vault_e_shield_reg) 

    #
    # 11
    Surface_11 = openmc.model.RightCircularCylinder((1858.01, 637.86, 111.76), 111.76, 15.24, axis='y')

    #
    # 2
    Surface_22 = openmc.model.RectangularParallelepiped(1699.2, 2119.2, 637.85, 668.33, 10.16, 363.22)

    # with an angle of 2.8 degrees. The positive vector points towards the 
    # lower-right (Southeast) corner of the geometry
    Surface_48 = openmc.Plane(a=0.99881, b=-0.04885, c=0.0, d=2063.64)

    # The CMU wall partially covering the north shield wall in Room III
    Vault_north_wall_ext_reg = -Surface_22 & -Surface_48 & +Surface_11  
    Vault_north_wall_ext_cell = openmc.Cell(fill=Concrete, region=Vault_north_wall_ext_reg) 

    # Surface of arbitrary size that will be cut by two 2.8 degree planes
    # in order to define the east foundation wall in Room II
    Surface_43 = openmc.model.RectangularParallelepiped(2016.62, 2266.62, 749.62, 1917.0900000000001, 0.0, 213.62)

    # The east foundation wall in Room II
    Region_18 = -Surface_43 & +Surface_48 & -Surface_49  
    Cell_18 = openmc.Cell(fill=Concrete, region=Region_18) 

    #
    # 40
    Surface_40 = openmc.model.RectangularParallelepiped(1589.09, 1613.54, 810.58, 942.6600000000001, 0.0, 213.62)

    #
    # 41
    Surface_41 = openmc.model.RectangularParallelepiped(1589.09, 1613.54, 1731.65, 1835.7900000000002, 0.0, 213.62)

    #
    # 44
    Surface_44 = openmc.model.RectangularParallelepiped(0.0, 1080.44, 998.54, 1000.14, 0.0, 213.62)

    #
    # 45
    Surface_45 = openmc.model.RectangularParallelepiped(1080.44, 1082.04, 998.54, 1342.71, 0.0, 213.62)

    #
    # 46
    Surface_46 = openmc.model.RectangularParallelepiped(1133.48, 1176.02, 1393.84, 1395.4399999999998, 0.0, 213.62)

    #
    # 47
    Surface_47 = openmc.model.RectangularParallelepiped(1176.02, 1177.62, 1393.84, 1910.73, 0.0, 213.62)

    #
    # 50
    Surface_50 = openmc.model.RectangularParallelepiped(658.6, 668.2, 749.62, 783.22, 0.0, 213.62)

    #
    # 51
    Surface_51 = openmc.model.RectangularParallelepiped(658.6, 668.2, 963.34, 996.94, 0.0, 213.62)

    #
    # 52
    Surface_52 = openmc.model.RectangularParallelepiped(658.6, 663.0500000000001, 783.22, 963.34, 0.0, 213.62)

    #
    # 53
    Surface_53 = openmc.model.RectangularParallelepiped(481.22, 2247.9, 1917.09, 1998.37, 0.0, 213.62)

    #
    # 56
    Surface_56 = openmc.model.RightCircularCylinder((1601.32, 1008.82, 0.0), 213.62, 18.21, axis='z')

    #
    # 57
    Surface_57 = openmc.model.RightCircularCylinder((1601.32, 1340.02, 0.0), 213.62, 31.75, axis='z')

    #
    # 58
    Surface_58 = openmc.model.RightCircularCylinder((1601.32, 1680.82, 0.0), 213.62, 18.21, axis='z')

    #
    # 59
    Surface_59 = openmc.model.RightCircularCylinder((1080.44, 1008.82, 0.0), 213.62, 18.21, axis='z')

    #
    # 60
    Surface_60 = openmc.model.RightCircularCylinder((1080.44, 1340.02, 0.0), 213.62, 31.75, axis='z')

    #
    # 61
    Surface_61 = openmc.model.RightCircularCylinder((1080.44, 1680.82, 0.0), 213.62, 18.21, axis='z')

    #
    # 62
    Surface_62 = openmc.model.RightCircularCylinder((532.82, 1008.82, 0.0), 213.62, 18.21, axis='z')

    #
    # 63
    Surface_63 = openmc.model.RightCircularCylinder((532.82, 1340.02, 0.0), 213.62, 31.75, axis='z')

    #
    # 64
    Surface_64 = openmc.model.RightCircularCylinder((532.62, 1680.82, 0.0), 213.62, 18.21, axis='z')

    #
    # 65
    Surface_65 = openmc.model.RectangularParallelepiped(1080.44, 1133.48, 1342.71, 1393.8400000000001, 0.0, 213.62)

    #
    # 66
    Surface_66 = openmc.model.RectangularParallelepiped(1231.9, 1236.3500000000001, 810.58, 942.6600000000001, 0.0, 213.62)

    #
    # 67
    Surface_67 = openmc.model.RectangularParallelepiped(1589.09, 1593.54, 810.58, 942.6600000000001, 0.0, 213.62)

    #
    # 68
    Surface_68 = openmc.model.RectangularParallelepiped(1589.09, 1593.54, 1731.65, 1835.7900000000002, 0.0, 213.62)

    #
    # 69
    Surface_69 = openmc.model.RectangularParallelepiped(1326.74, 1517.95, 1694.18, 1698.63, 0.0, 213.62)

    #
    # 70
    Surface_70 = openmc.model.RectangularParallelepiped(1098.65, 1231.9, 1008.82, 1013.2700000000001, 0.0, 213.62)

    #
    # 71
    Surface_71 = openmc.model.RectangularParallelepiped(1177.62, 1304.29, 1694.18, 1698.63, 0.0, 213.62)

    #
    # 72
    Surface_72 = openmc.model.RectangularParallelepiped(1589.09, 1613.54, 749.62, 1912.0900000000001, 0.0, 213.62)

    #
    # 73
    Surface_73 = openmc.model.RectangularParallelepiped(1517.97, 1589.0900000000001, 1674.18, 1698.63, 0.0, 213.62)

    # The main air chamber in Room II
    # excluding the east foundation wall
    # excluding the north foundatino wall
    Region_19 = -Surface_54 & -Surface_49 & \
        (+Surface_43 | -Surface_48 | +Surface_49) & \
        (+Surface_53 | +Surface_49) & \
        +Surface_74 & +Surface_75 & (+Surface_76 | -Surface_42) & +Surface_46 & +Surface_47 & +Surface_50 & +Surface_51 & (+Surface_72 | -Surface_40 | -Surface_41 | -Surface_56 | -Surface_57 | -Surface_58) & (+Surface_73 | -Surface_58) & (+Surface_44 | -Surface_59 | -Surface_62) & (+Surface_45 | -Surface_59 | -Surface_60) & (+Surface_65 | -Surface_60) & +Surface_59 & +Surface_60 & +Surface_61 & +Surface_56 & +Surface_57 & +Surface_58 & +Surface_62 & +Surface_63 & +Surface_64 & +Surface_52 & +Surface_66 & +Surface_67 & +Surface_68 & +Surface_69 & +Surface_70 & +Surface_71  
    Cell_19 = openmc.Cell(fill=Air, region=Region_19) 

    # The floor separating basement and first floor labs
    Region_20 = -Surface_8 & +Surface_7 & -Surface_49  
    Cell_20 = openmc.Cell(fill=Concrete, region=Region_20) 

    # The foundation underneath all basement lab rooms
    Region_21 = -Surface_94 & -Surface_49  
    Cell_21 = openmc.Cell(fill=Concrete, region=Region_21) 

    #
    # 36
    Surface_36 = openmc.model.RectangularParallelepiped(1104.9, 2254.9, 0.0, 99.38, 0.0, 363.22)

    # The south Vault shield wall in Room III
    South_vault_wall_reg = -Surface_36 & -Surface_49  
    South_vault_wall_cell = openmc.Cell(fill=Concrete, region=South_vault_wall_reg) 

    #
    # 16
    Surface_16 = openmc.model.RectangularParallelepiped(2050.0, 2200.0, 99.38, 668.34, 0.0, 363.22)

    # The east Vault shield wall in Room III with Room II entrance cutout
    East_vault_wall_reg = -Surface_16 & +Surface_48 & -Surface_49  
    East_vault_wall_cell = openmc.Cell(fill=Concrete, region=East_vault_wall_reg) 

    #
    # 38
    Surface_38 = openmc.model.RectangularParallelepiped(1000.0, 1150.0, 380.71, 598.8, 10.16, 213.35999999999999)

    #
    # 39
    Surface_39 = openmc.model.RectangularParallelepiped(1023.62, 1104.9, 0.0, 749.62, 0.0, 363.22)

    # The west Vault shield wall in Room III with Vault entrance cutout
    West_vault_wall_reg = -Surface_39 & +Surface_38  
    West_vault_wall_cell = openmc.Cell(fill=Concrete, region=West_vault_wall_reg) 

    #
    # 37
    Surface_37 = openmc.model.RectangularParallelepiped(1023.62, 2253.62, 0.0, 749.62, 363.22, 424.18)

    # The top (roof) Vault shield wall in Room III
    Vault_ceiling_reg = -Surface_37 & -Surface_49  
    Vault_ceiling_cell = openmc.Cell(fill=Concrete, region=Vault_ceiling_reg) 

    #
    # 12
    Surface_12 = openmc.model.RectangularParallelepiped(1169.67, 2169.67, 99.38, 668.34, 0.0, 10.16)

    # The bottom Vault floor in Room III 
    Vault_floor_reg = -Surface_12 & -Surface_48  
    Vault_floor_cell = openmc.Cell(fill=Concrete, region=Vault_floor_reg) 

    # 23
    Surface_23 = openmc.model.RectangularParallelepiped(1104.9, 2254.9, 668.34, 749.62, 0.0, 363.22)

    #
    # The cyclotron beamline cutout in the north Vault shield wall
    Surface_102 = openmc.model.RightCircularCylinder((1422.0, 668.34, 50.0), 81.28, 5.0, axis='y')

    # The north Vault shield wall in Room III with beamline cutouts
    North_vault_wall_reg = -Surface_23 & -Surface_49 & +Surface_11 & +Surface_102  
    North_vault_wall_cell = openmc.Cell(fill=Concrete, region=North_vault_wall_reg) 

    # The north foundation wall in Room II
    Region_29 = -Surface_53 & -Surface_49  
    Cell_29 = openmc.Cell(fill=Concrete, region=Region_29) 

    # The north-east pillar in Room IV 
    Region_30 = -Surface_85  
    Cell_30 = openmc.Cell(fill=Concrete, region=Region_30) 

    # The north-west pillar in Room IV 
    Region_31 = -Surface_86  
    Cell_31 = openmc.Cell(fill=Concrete, region=Region_31) 

    # Small CMU extenion in NW corner of Room IV (Piece 0)
    Region_32 = -Surface_80  
    Cell_32 = openmc.Cell(fill=Concrete, region=Region_32) 

    # Small CMU extenion in NW corner of Room IV (Piece 1)
    Region_33 = -Surface_81  
    Cell_33 = openmc.Cell(fill=Concrete, region=Region_33) 

    #
    # 82
    Surface_82 = openmc.model.RectangularParallelepiped(1135.9, 1147.3300000000002, 138.75, 628.97, 276.86, 279.40000000000003)

    #
    # 83
    Surface_83 = openmc.model.RectangularParallelepiped(1135.9, 1147.3300000000002, 138.75, 628.97, 297.18, 299.72)

    #
    # 84
    Surface_84 = openmc.model.RectangularParallelepiped(1140.35, 1142.8899999999999, 138.75, 628.97, 276.86, 299.72)

    # The I-beam support the main Vault shield door in Room III
    I_beam_reg = -Surface_82 | -Surface_83 | -Surface_84  
    I_beam_cell = openmc.Cell(fill=Material_6, region=I_beam_reg) 

    # The GWB wall separating the Maze from RPO storage 
    Region_35 = -Surface_46  
    Cell_35 = openmc.Cell(fill=Material_8, region=Region_35) 

    # The GWB wall separating the Maze from RPO storage 
    Region_36 = -Surface_47  
    Cell_36 = openmc.Cell(fill=Material_8, region=Region_36) 

    # The southern door frame in Room II separating Maze from hallway 
    Region_37 = -Surface_50  
    Cell_37 = openmc.Cell(fill=Material_8, region=Region_37) 

    # The northern door frame in Room II separating Maze from hallway  
    Region_38 = -Surface_51  
    Cell_38 = openmc.Cell(fill=Material_8, region=Region_38) 

    # The bottom-middle pillar in Room II (Pillar 4) 
    Region_39 = -Surface_59  
    Cell_39 = openmc.Cell(fill=Concrete, region=Region_39) 

    # The middle-middle pillar in Room II (Pillar 5)  
    Region_40 = -Surface_60  
    Cell_40 = openmc.Cell(fill=Concrete, region=Region_40) 

    # The top-middle pillar in Room II (Pillar 6)   
    Region_41 = -Surface_61  
    Cell_41 = openmc.Cell(fill=Concrete, region=Region_41) 

    # The bottom-right pillar in Room II (Pillar 1)  
    Region_42 = -Surface_56  
    Cell_42 = openmc.Cell(fill=Concrete, region=Region_42) 

    # The middle-right pillar in Room II (Pillar 2)  
    Region_43 = -Surface_57  
    Cell_43 = openmc.Cell(fill=Concrete, region=Region_43) 

    # The top-right pillar in Room II (Pillar 3)   
    Region_44 = -Surface_58  
    Cell_44 = openmc.Cell(fill=Concrete, region=Region_44) 

    # The CMU wall in Room II separating NW13-015 and -016
    Region_45 = -Surface_72 & +Surface_40 & +Surface_41 & +Surface_56 & +Surface_57 & +Surface_58  
    Cell_45 = openmc.Cell(fill=Concrete, region=Region_45) 

    # Small CMU wall bounding doors in Room II
    Region_46 = -Surface_73 & +Surface_58  
    Cell_46 = openmc.Cell(fill=Concrete, region=Region_46) 

    # GWB wall in Room II separating the Maze from RPO storage
    Region_47 = -Surface_44 & +Surface_59 & +Surface_62  
    Cell_47 = openmc.Cell(fill=Material_8, region=Region_47) 

    # GWB wall in Room II separating the Maze from RPO storage
    Region_48 = -Surface_45 & +Surface_59 & +Surface_60  
    Cell_48 = openmc.Cell(fill=Material_8, region=Region_48) 

    # The square brick pillar connect above GWB walls
    Region_49 = -Surface_65 & +Surface_60  
    Cell_49 = openmc.Cell(fill=Concrete, region=Region_49) 

    # The bottom-left pillar in Room II (Pillar 7)  
    Region_50 = -Surface_62  
    Cell_50 = openmc.Cell(fill=Concrete, region=Region_50) 

    # The middle-left pillar in Room II (Pillar 8)  
    Region_51 = -Surface_63  
    Cell_51 = openmc.Cell(fill=Concrete, region=Region_51) 

    # The top-left pillar in Room II (Pillar 9)  
    Region_52 = -Surface_64  
    Cell_52 = openmc.Cell(fill=Concrete, region=Region_52) 

    # The door connecting the hallway to NW13-039 in Room IV 
    Region_54 = -Surface_78  
    Cell_54 = openmc.Cell(fill=Material_7, region=Region_54) 

    # The door in Room IV (NW13-039) leading to the stairway 
    Region_55 = -Surface_77  
    Cell_55 = openmc.Cell(fill=Material_7, region=Region_55) 

    # The door in Room II separating the Maze from the hallway
    Region_56 = -Surface_52  
    Cell_56 = openmc.Cell(fill=Material_7, region=Region_56) 

    # The southern door into NW13-016 in Room II
    Region_57 = -Surface_66  
    Cell_57 = openmc.Cell(fill=Material_7, region=Region_57) 

    # The southern door into NW13-015 in Room II 
    Region_58 = -Surface_67  
    Cell_58 = openmc.Cell(fill=Material_7, region=Region_58) 

    # The northern door into NW13-015 in Room II  
    Region_59 = -Surface_68  
    Cell_59 = openmc.Cell(fill=Material_7, region=Region_59) 

    # The northern door into NW13-016 in Room II 
    Region_60 = -Surface_69  
    Cell_60 = openmc.Cell(fill=Material_7, region=Region_60) 

    # The south door into the hallway between NW13-016 and RPO in Room II
    Region_61 = -Surface_70  
    Cell_61 = openmc.Cell(fill=Material_7, region=Region_61) 

    # The north door into the hallway between NW13-016 and RPO in Room II 
    Region_62 = -Surface_71  
    Cell_62 = openmc.Cell(fill=Material_7, region=Region_62) 

    #
    # Inner surface defining the top/bottom DANTE selection magnets
    Surface_28 = openmc.model.RightCircularCylinder((1858.01, 597.22, 99.7), 75.0, 20.95, axis='z')

    # 
    # Outer surface defining the bottom DANTE selection magnet
    Surface_30 = openmc.model.RightCircularCylinder((1858.01, 597.22, 99.7), 8.0, 32.0, axis='z')

    # The bottom DANTE beamline selection magnet in Room III
    DANTE_vault_bot_magnet_reg = -Surface_30 & +Surface_28  
    DANTE_vault_bot_magnet_cell = openmc.Cell(fill=Material_2, region=DANTE_vault_bot_magnet_reg) 

    #
    # Outer surface defining the top DANTE selection magnet
    Surface_35 = openmc.model.RightCircularCylinder((1858.01, 597.22, 115.83), 8.0, 32.0, axis='z')

    # The top DANTE beamline selection magnet in Room III
    DANTE_vault_top_magnet_reg = -Surface_35 & +Surface_28  
    DANTE_vault_top_magnet_cell = openmc.Cell(fill=Material_2, region=DANTE_vault_top_magnet_reg) 

    #
    # Surface definition for selection magnet cutout of surface #27
    Surface_21 = openmc.model.RectangularParallelepiped(1825.87, 1890.1399999999999, 571.9, 621.9, 99.7, 123.83)

    #
    # Surface definition of square box that contains DANTE selection magnets
    Surface_27 = openmc.model.RectangularParallelepiped(1816.1, 1899.9199999999998, 576.9, 617.54, 89.54, 133.99)

    #
    # Selection magnet SE support leg
    Surface_29 = openmc.model.RectangularParallelepiped(1892.3, 1899.9199999999998, 576.9, 584.52, 10.16, 88.89999999999999)

    #
    # Selection magnet NE support leg
    Surface_31 = openmc.model.RectangularParallelepiped(1892.3, 1899.9199999999998, 609.92, 617.54, 10.16, 88.89999999999999)

    #
    # Selection magnet SW support leg
    Surface_33 = openmc.model.RectangularParallelepiped(1816.1, 1823.7199999999998, 576.9, 584.52, 10.16, 88.89999999999999)

    #
    # Thin selection magnet table top plate
    Surface_34 = openmc.model.RectangularParallelepiped(1816.1, 1899.9199999999998, 576.9, 617.54, 88.9, 89.54)

    # The DANTE beamline selection magnet stand in Room III
    DANTE_vault_mag_stand_reg = (-Surface_27 & +Surface_21) | -Surface_29 | -Surface_31 | -Surface_33 | -Surface_34  
    DANTE_vault_mag_stand_cell = openmc.Cell(fill=Aluminum, region=DANTE_vault_mag_stand_reg) 

    # Poly Cyclotron Shield in Room II
    # 103
    Surface_103 = openmc.model.RectangularParallelepiped(1270.0, 1570.0, 850.0, 950.0, 0.0, 150.0)

    # 104
    Surface_104 = openmc.model.RectangularParallelepiped(1270.0, 1370.0, 750.0, 850.0, 0.0, 150.0)

    # 105
    Surface_105 = openmc.model.RectangularParallelepiped(1470.0, 1570.0, 750.0, 850.0, 0.0, 150.0)

    # 106
    Surface_106 = openmc.model.RectangularParallelepiped(1270.0, 1570.0, 750.0, 950.0, 150.0, 200.0)

    # Poly Cyclotron Shield 
    Region_69 = -Surface_103 | -Surface_104 | -Surface_105 | -Surface_106  
    Cell_69 = openmc.Cell(fill=BPE, region=Region_69) 

    # Lead Cyclotron Shield in Room II
    # 107
    Surface_107 = openmc.model.RectangularParallelepiped(1265.0, 1575.0, 950.0, 955.0, 0.0, 200.0)

    # 108
    Surface_108 = openmc.model.RectangularParallelepiped(1265.0, 1270.0, 750.0, 950.0, 0.0, 200.0)

    # 109
    Surface_109 = openmc.model.RectangularParallelepiped(1570.0, 1575.0, 750.0, 950.0, 0.0, 200.0)

    # 110
    Surface_110 = openmc.model.RectangularParallelepiped(1265.0, 1575.0, 750.0, 955.0, 200.0, 205.0)

    # Lead Cyclotron Shield 
    Region_70 = -Surface_107 | -Surface_108 | -Surface_109 | -Surface_110  
    Cell_70 = openmc.Cell(fill=Lead, region=Region_70) 

    # Portland Iron Concrete Shield in Vault
    # 111
    # Surface_111 = openmc.model.RectangularParallelepiped(1295.0, 1545.0, 518.0, 568.0, 10.16, 160.16)

    # # 112
    # Surface_112 = openmc.model.RectangularParallelepiped(1495.0, 1545.0, 568.0, 668.0, 10.16, 160.16)

    # # 113
    # Surface_113 = openmc.model.RectangularParallelepiped(1295.0, 1345.0, 568.0, 668.0, 10.16, 160.16)

    # # 114
    # Surface_114 = openmc.model.RectangularParallelepiped(1295.0, 1545.0, 518.0, 668.0, 160.16, 210.16)

    # # Portland Concrete Brick Cyclotron Target Chamber
    # Region_71 = -Surface_111 | -Surface_112 | -Surface_113 | -Surface_114  
    # Cell_71 = openmc.Cell(fill=IronConcrete, region=Region_71) 

    # # 116
    # Surface_116 = openmc.model.RightCircularCylinder((1422.0, 799.62, 0.0), 2.0, 50.0, axis='z')

    # # 117
    # Surface_117 = openmc.model.RightCircularCylinder((1422.0, 799.62, 148.0), 2.0, 50.0, axis='z')

    # # 118
    # Surface_118 = openmc.model.RectangularParallelepiped(1397.0, 1447.0, 749.62, 849.62, 45.0, 55.0)

    # # 119
    # Surface_119 = openmc.model.RightCircularCylinder((1422.0, 799.62, 2.0), 146.0, 46.0, axis='z')

    # # 120
    # Surface_120 = openmc.model.RectangularParallelepiped(1395.0, 1449.0, 749.62, 849.62, 43.0, 57.0)

    # # 121
    # Surface_121 = openmc.model.RightCircularCylinder((1422.0, 799.62, 2.0), 146.0, 48.0, axis='z')

    # # Cyclotron
    # Region_72 = -Surface_121 & +Surface_119 | -Surface_120 & +Surface_118 | -Surface_117 | -Surface_116  
    # Cell_72 = openmc.Cell(fill=None, region=Region_72) 



    # The main air chamber of Room III
    # the north Vault shield wall
    # the south Vault shield wall
    # the east Vault shield wall
    # the west Vault shield wall
    # the top (ceiling) Vault shield wall
    # the bottom (floor) Vault shield wall
    # the main vault door
    # the Ricorad shields within the Vault entrance
    # the I-beam support for the Vault door
    # the north CMU wall with DANTE beamline cutout
    # the iron-brick piles around selection magnet 
    # the bottom selection magnet
    # the top selection magnet
    # the selection magnet support stand
    # DT Generator shield universe region

    if overall_exclusion_region:
        Region_28 = -Surface_24 & -Surface_49 & \
            ~North_vault_wall_reg & ~Vault_north_wall_ext_reg & \
            ~South_vault_wall_reg & \
            ~West_vault_wall_reg & \
            ~East_vault_wall_reg & \
            ~Vault_ceiling_reg & \
            ~Vault_floor_reg & \
            ~Vault_door_reg & \
            ~Vault_door_shield_n_pillar_reg & ~Vault_door_shield_s_pillar_reg & \
            ~I_beam_reg & \
            ~DANTE_vault_w_shield_reg & ~DANTE_vault_e_shield_reg & \
            ~DANTE_vault_bot_magnet_reg & \
            ~DANTE_vault_top_magnet_reg & \
            ~DANTE_vault_mag_stand_reg & \
            ~overall_exclusion_region
    else:
        Region_28 = -Surface_24 & -Surface_49 & \
            ~North_vault_wall_reg & ~Vault_north_wall_ext_reg & \
            ~South_vault_wall_reg & \
            ~West_vault_wall_reg & \
            ~East_vault_wall_reg & \
            ~Vault_ceiling_reg & \
            ~Vault_floor_reg & \
            ~Vault_door_reg & \
            ~Vault_door_shield_n_pillar_reg & ~Vault_door_shield_s_pillar_reg & \
            ~I_beam_reg & \
            ~DANTE_vault_w_shield_reg & ~DANTE_vault_e_shield_reg & \
            ~DANTE_vault_bot_magnet_reg & \
            ~DANTE_vault_top_magnet_reg & \
            ~DANTE_vault_mag_stand_reg

        # (+Surface_23 | +Surface_49 | -Surface_11 | -Surface_102) & \
        # (+Surface_36 | +Surface_49) & \
        # (+Surface_16 | -Surface_48 | +Surface_49) & \
        # (+Surface_39 | -Surface_38) & \
        # (+Surface_37 | +Surface_49) & \
        # (+Surface_12 | +Surface_48) & \
        # (+Surface_13 | +Surface_14 | +Surface_15) & \
        # +Surface_17 & +Surface_18 & \
        # (+Surface_82 & +Surface_83 & +Surface_84) & \
        # (+Surface_22 | +Surface_48 | -Surface_11) & \
        # +Surface_9 & +Surface_10 & \
        # (+Surface_30 | -Surface_28) & \
        # (+Surface_35 | -Surface_28) & \
        # (+Surface_27 | -Surface_21) & +Surface_29 & +Surface_31 & +Surface_33 & +Surface_34 & \
        # (-DT_BPE_west_xplane | +DT_BPE_east_xplane | -DT_BPE_south_yplane | +DT_BPE_north_yplane \
        # 				| -DT_BPE_bot_zplane | +DT_BPE_top_zplane)
        # +DT_BPE_shield_rpp
        # (+DT_BPE_shield_rpp | +DT_conc_shield_rpp | +DT_enclosure_rpp)
        # (-DT_conc_west_xplane | +DT_conc_east_xplane | -DT_conc_south_yplane | +DT_conc_north_yplane \
        # 				| -DT_conc_bot_zplane | +DT_conc_top_zplane)
        # +DT_conc_shield_rpp 
        # (+DT_enclosure_rpp) & (-DT_enclosure_rpp | +DT_conc_shield_rpp) & (-DT_BPE_shield_rpp | +DT_conc_shield_rpp)
        # & (+DT_BPE_shield_rpp | +DT_conc_shield_rpp | +DT_enclosure_rpp) # & \
    # excluding cyclotron target chamber
    # cyclotron 
        # (+Surface_111 & +Surface_112 & +Surface_113 & +Surface_114) & \
        # (+Surface_121 | -Surface_119) & (+Surface_120 | -Surface_118) & +Surface_117 & +Surface_116 & \
        # ~Region_72  
    Cell_28 = openmc.Cell(fill=Air, region=Region_28) 

    ##### s_wall_lev1_w Western portion of south wall of NW13 on level 1 (first floor)
    # Cell 8 is control room south wall



    # Western portion of south wall
    s_wall_lev1_w_rpp = openmc.model.RectangularParallelepiped(
                        0.0, 1023.62, 8*2.54, 16*2.54, 241.56, 241.56 + 14*12*2.54)

    sw_corner_vault_x = 1023.62
    lev1_floor_z = 241.56

    ## East Window Cell
    # Edge of east window is 20.5 inches west of the outer southwest corner of the vault
    # Eastern window is about 167 inches across
    # Bottom of both windows is about 8 feet above 1st floor level (top of control room ceiling)
    east_window_rpp = openmc.model.RectangularParallelepiped(
                    sw_corner_vault_x - (20.5 + 167)*2.54, sw_corner_vault_x - 20.5*2.54,
                    8*2.54, 16*2.54,
                    lev1_floor_z + 8*12*2.54, lev1_floor_z + (8*12 + 58)*2.54)
    east_window_region = -east_window_rpp
    east_window_cell = openmc.Cell(region=east_window_region, fill=Air, name='East Window')

    ## West Window Cell
    # Eastern edge of west window is about 241 inches west of the outer southwest corner of the vault
    # Western window is about 129 inches across
    # Y and Z dimensions/coordinates are the same as for East Window
    west_window_rpp = openmc.model.RectangularParallelepiped(
                        sw_corner_vault_x - (241 + 129)*2.54, sw_corner_vault_x - 241*2.54, 
                        8*2.54, 16*2.54,
                        lev1_floor_z + 8*12*2.54, lev1_floor_z + (8*12 + 58)*2.54)
    west_window_region = -west_window_rpp
    west_window_cell = openmc.Cell(region=west_window_region, fill=Air, name='West Window')


    s_wall_lev1_w_region = -s_wall_lev1_w_rpp & +east_window_rpp & +west_window_rpp

    ### Eastern portion of south wall
    s_wall_lev1_e_rpp = openmc.model.RectangularParallelepiped(
                        1023.62, 2247.9, 8*2.54, 16*2.54, 424.18, 241.56 + 14*12*2.54)
    ### Air handler opening in eastern portion of south wall
    # It's western edge is about 29 inches east of the southwest corner of vault
    # Air handler vent is 162 inches wide
    # Air handler bottom is about 35 inches above vault ceiling top
    # Air handler vent is 48 inches tall
    vault_ceiling_top_z = 424.18
    air_hand_rpp = openmc.model.RectangularParallelepiped(
                                sw_corner_vault_x + 29*2.54, sw_corner_vault_x + (29+162)*2.54,
                                8*2.54, 16*2.54,
                                vault_ceiling_top_z + 35*2.54, vault_ceiling_top_z + (35+48)*2.54)
    air_hand_region = -air_hand_rpp
    air_hand_cell = openmc.Cell(region=air_hand_region, fill=Air, name='Air Handler Vent')

    s_wall_lev1_e_region = -s_wall_lev1_e_rpp & -Surface_49 & +air_hand_rpp

    south_wall_lev1_region = s_wall_lev1_w_region | s_wall_lev1_e_region
    south_wall_lev1_cell = openmc.Cell(region=south_wall_lev1_region, fill=Brick, name='Floor 1 South Wall')


    #### South Wall western extension (increases thickness of wall by 8 inches above control room)
    # South wall extension extends to about 39 inches above the 1st level floor (about 4 feet above ground level)
    south_wall_w_ext_rpp = openmc.model.RectangularParallelepiped(
                        0.0, 1023.62, 0, 8*2.54, lev1_floor_z, lev1_floor_z + 39*2.54)

    s_wall_ext_region = -south_wall_w_ext_rpp

    s_wall_ext_cell = openmc.Cell(fill=Concrete, region=s_wall_ext_region, name='South Wall Extension')


    #### w_wall_lev1 Western brick wall on Level 1
    # western and eastern planes outlining walls are 
    # the planes 2.8 degrees off of an x-plane in Surface 49
    w_wall_lev1_east_x = Surface_49
    w_wall_lev1_west_x = w_wall_lev1_east_x.clone()
    # Brick wall is 8 inches thick at a 2.8 degree angle from x-plane
    w_wall_lev1_west_x = w_wall_lev1_west_x.translate([-8*2.54*np.cos(np.deg2rad(2.8)), 0, 0])
    w_wall_lev1_south_y = openmc.YPlane(s_wall_lev1_e_rpp.ymax.y0)
    # Surface 23 is the North Vault Wall
    w_wall_lev1_north_y = openmc.YPlane(Surface_23.ymax.y0)
    w_wall_lev1_bot_z = openmc.ZPlane(s_wall_lev1_e_rpp.zmin.z0)
    w_wall_lev1_top_z = openmc.ZPlane(s_wall_lev1_e_rpp.zmax.z0)

    w_wall_lev1_region = +w_wall_lev1_west_x & -w_wall_lev1_east_x & +w_wall_lev1_south_y & -w_wall_lev1_north_y \
                        & +w_wall_lev1_bot_z & -w_wall_lev1_top_z
    w_wall_lev1_cell = openmc.Cell(region=w_wall_lev1_region, fill=Brick, name='Level 1 West Wall')

    #### lev1_ceil The concrete slab between the 1st and 2nd floors of NW13
    # Floor thickness of Level 2 is about 11 inches
    lev1_ceil_rpp = openmc.model.RectangularParallelepiped(
                        0.0, 2247.9, 8*2.54, 1998.37, s_wall_lev1_e_rpp.zmax.z0, s_wall_lev1_e_rpp.zmax.z0 + 11*2.54)

    lev1_ceil_region = -lev1_ceil_rpp & -Surface_49
    lev1_ceil_cell = openmc.Cell(region=lev1_ceil_region, fill=Concrete, name='Floor 1 Ceiling')


    Region_1 = -Surface_95 & \
        (+Surface_8 | -Surface_7 | +Surface_49) & \
        (+Surface_94 | +Surface_49) & \
        (+Surface_54 | +Surface_49) & \
        (+Surface_24 | +Surface_49) & \
        +Surface_93  \
        & ~Soil_region \
        & +s_wall_lev1_w_rpp \
        & (+s_wall_lev1_e_rpp | +Surface_49) \
        & +south_wall_w_ext_rpp \
        & (-w_wall_lev1_west_x | +w_wall_lev1_east_x | -w_wall_lev1_south_y | +w_wall_lev1_north_y \
            | -w_wall_lev1_bot_z | +w_wall_lev1_top_z) \
        & (+lev1_ceil_rpp | +Surface_49)

    Cell_900 = openmc.Cell(fill=None, region=Region_1) 


    Cells = [Cell_1000, Cell_900, Cell_2, Cell_3, Cell_4, Cell_5, Cell_6, Cell_7, 
        Cell_8, Cell_9, Cell_10, Cell_11, Vault_door_cell, 
        Vault_door_shield_n_pillar_cell, Vault_door_shield_s_pillar_cell, 
        DANTE_vault_w_shield_cell, DANTE_vault_e_shield_cell, 
        Vault_north_wall_ext_cell, Cell_18, Cell_19, Cell_20, Cell_21, 
        South_vault_wall_cell, East_vault_wall_cell, West_vault_wall_cell, 
        Vault_ceiling_cell, Vault_floor_cell, North_vault_wall_cell, 
        Cell_29, Cell_30, Cell_31, Cell_32, Cell_33, 
        I_beam_cell, Cell_35, Cell_36, Cell_37, Cell_38, Cell_39, Cell_40, Cell_41, 
        Cell_42, Cell_43, Cell_44, Cell_45, Cell_46, Cell_47, Cell_48, Cell_49, Cell_50, 
        Cell_51, Cell_52, Cell_54, Cell_55, Cell_56, Cell_57, Cell_58, Cell_59, 
        Cell_60, Cell_61, Cell_62, DANTE_vault_bot_magnet_cell, DANTE_vault_top_magnet_cell, 
        DANTE_vault_mag_stand_cell, Cell_69, Cell_70, 
        # Cell_71, Cell_72, 
        # DT_BPE_shield_cell,
        # DT_enclosure_cell, DT_conc_shield_cell,
        # DT_enclosure_cell, DT_BPE_shield_cell,
        # test_cell,
        Cell_28, Soil_cell, south_wall_lev1_cell, east_window_cell,
        west_window_cell, air_hand_cell, s_wall_ext_cell, w_wall_lev1_cell,
        lev1_ceil_cell] 
    
    print(Cells)
    Cells += added_cells
    print(Cells)

    Universe_1 = openmc.Universe(cells=Cells) 
    geometry = openmc.Geometry(Universe_1) 
    # print(geometry.get_all_cells())
    geometry.remove_redundant_surfaces() 
    # print(geometry.get_all_cells())


    vault_model = openmc.model.Model(geometry=geometry, materials=materials, settings=settings, 
            tallies=tallies)

    return vault_model





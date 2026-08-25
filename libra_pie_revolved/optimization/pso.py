import numpy as np
from pyswarm import pso
import openmc

# Material properties: (density in g/cm³, cost in $/kg)
materials = {
    0: {'name': 'LiCl', 'density': 2.07, 'cost': 0.25},
    1: {'name': 'LiF', 'density': 2.64, 'cost': 0.30},
    2: {'name': 'PbF2', 'density': 8.24, 'cost': 0.40},
    3: {'name': 'PbCl2', 'density': 5.85, 'cost': 0.35},
}

# Tritium production threshold (to be met)
tritium_threshold = 1e12  # Example value

def run_openmc_simulation(thickness, height, material):
    """
    Run the OpenMC simulation with the given parameters and return the tritium production tally.
    Assumes OpenMC input files are prepared and takes thickness, height, and material as inputs.
    """
    # Modify the OpenMC input files based on the input geometry and material.
    # Assuming we modify 'geometry.xml' and 'materials.xml' here
    # (e.g., updating thickness, height, and material properties)
    
    # Here, we simulate a simple script that modifies OpenMC input:
    model, masses = modify_openmc_input(thickness, height, material)

    # Run OpenMC simulation
    subprocess.run(["openmc"], check=True)

    # Extract tritium tally from the output file (e.g., statepoint.h5)
    # This function will need to be adapted to parse the specific output format of OpenMC
    tritium_production = extract_tritium_tally()

    return tritium_production

def modify_openmc_input(thickness, height, material):
    """
    Modify the OpenMC input XMLs (geometry.xml, materials.xml) based on the tank dimensions
    and material selection. This is a placeholder function.
    """
    # Here you would add the code to modify OpenMC input files.
    # This will likely involve writing new XML files or modifying existing ones.

def extract_tritium_tally():
    """
    Extract the tritium tally from OpenMC simulation results.
    This is a placeholder function.
    """
    # For this example, we'll simulate tritium production output.
    # In practice, you'd extract the actual tally from OpenMC output files.
    return np.random.uniform(1e11, 2e12)  # Simulated tritium tally (replace with actual value)

def calculate_cost(thickness, height, material):
    """
    Calculate the cost of the tank based on its volume and the material used.
    """
    # Tank volume = pi * (radius^2) * height, assuming cylindrical shape
    radius = thickness
    volume = np.pi * (radius**2) * height  # in cm³

    # Convert volume to mass (volume in cm³, density in g/cm³)
    mass = volume * materials[material]['density']  # in grams
    mass_kg = mass / 1000.0  # Convert to kilograms

    # Calculate the cost: mass_kg * cost per kg
    cost = mass_kg * materials[material]['cost']

    return cost

def fitness_function(x):
    """
    Fitness function for PSO.
    x[0] = thickness (cm)
    x[1] = height (cm)
    x[2] = material (0=LiCl, 1=LiF, 2=PbF2, 3=PbCl2)
    """
    thickness = x[0]
    height = x[1]
    material = int(x[2])  # Discrete material choice


    # Run OpenMC simulation to get tritium production
    tbr, masses = run_openmc_simulation(thickness, height, material)

    # Calculate the cost of the tank
    cost = calculate_cost(masses, salt_material)

    # Apply a penalty if tritium production does not meet the threshold
    if tbr < tritium_threshold:
        penalty = 1e9 * (tritium_threshold - tbr)  # Large penalty
    else:
        penalty = 0

    return cost + penalty

# Bounds for PSO
# Thickness and height are continuous, while material is a discrete integer
lb = [0.1, 10, 0]  # Lower bounds: thickness, height, material index
ub = [5.0, 100, 3]  # Upper bounds: thickness, height, material index

# Run PSO
xopt, fopt = pso(fitness_function, lb, ub, swarmsize=50, maxiter=100)

print(f"Optimal solution: thickness={xopt[0]:.2f} cm, height={xopt[1]:.2f} cm, material={materials[int(xopt[2])]['name']}")
print(f"Minimum cost: ${fopt:.2f}")
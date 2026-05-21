"""
A basic example of a pack simulation
"""

import liionpack as lp
import pybamm
import numpy as np
import os

lp.set_logging_level("NOTICE")

# def custom_dfn_thermal_simulation(parameter_values=None):
#     model = pybamm.lithium_ion.DFN(  # Use DFN instead of SPMe
#         options={"thermal": "x-full"}
#     )
#     model = lp.add_events_to_model(model)
    
#     if parameter_values is None:
#         parameter_values = pybamm.ParameterValues("Chen2020")
    
#     parameter_values.update({
#         "Total heat transfer coefficient [W.m-2.K-1]": "[input]",
#     })
    
#     solver = pybamm.CasadiSolver(mode="safe")
#     sim = pybamm.Simulation(model=model, parameter_values=parameter_values, solver=solver)
#     return sim



# Define parameters
Np = 10
Ns = 1
Iapp = 10

# Generate the netlist
netlist = lp.setup_circuit(Np=Np, Ns=Ns)

# Define additional output variables
output_variables = ["Volume-averaged cell temperature [K]"]

# Define a cycling experiment using PyBaMM
experiment = pybamm.Experiment(
    [
        f"Charge at {Iapp} A for 30 minutes",
        "Charge at 0 A for 15 minutes",
        f"Discharge at {Iapp} A for 30 minutes",
        "Charge at 0 A for 30 minutes",
    ],
    period="10 seconds",
)

# Define the PyBaMM parameters
parameter_values = pybamm.ParameterValues("Chen2020")
# parameter_values.update({ # copied from Marquis2019
#     "Negative current collector thermal conductivity [W.m-1.K-1]": 401.0,
#     "Positive current collector thermal conductivity [W.m-1.K-1]": 237.0,
#     "Negative current collector surface heat transfer coefficient [W.m-2.K-1]": 0.0,
#     "Positive current collector surface heat transfer coefficient [W.m-2.K-1]": 0.0,
#     "Negative tab heat transfer coefficient [W.m-2.K-1]": 10.0,
#     "Positive tab heat transfer coefficient [W.m-2.K-1]": 10.0,
#     "Negative tab width [m]": 0.04,
#     "Positive tab width [m]": 0.04,
#     "Edge heat transfer coefficient [W.m-2.K-1]": 0.3,
# })
inputs = {"Total heat transfer coefficient [W.m-2.K-1]": np.ones(Np * Ns) * 10}

# Solve the pack
output = lp.solve(
    netlist=netlist,
    sim_func=lp.thermal_simulation,
    parameter_values=parameter_values,
    experiment=experiment,
    output_variables=output_variables,
    initial_soc=0.5,
    inputs=inputs,
    nproc=os.cpu_count(),
    manager="casadi",
)

# Plot the pack and individual cell results
lp.plot_pack(output)
lp.plot_cells(output)
lp.show_plots()

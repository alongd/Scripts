"""
A burner-stabilized, premixed  flat flame with multicomponent
transport properties and a specified temperature profile.
"""

import cantera as ct
import numpy as np

################################################################
# parameter values
p = 0.06 * ct.one_atm    ##1.e5 
tburner = 300.0
mdot = 0.02615      #0.018790 # kg/m^2/s
comp = 'NH3:0.25, H2:0.05, O2:0.21, AR:0.48' 

# The solution domain is chosen to be 1 cm
width = 0.02 # m

loglevel = 1  # amount of diagnostic output (0 to 5)
refine_grid = True  # 'True' to enable refinement

################ create the gas object ########################
#
# This object will be used to evaluate all thermodynamic, kinetic, and
# transport properties. It is created with two transport managers, to enable
# switching from mixture-averaged to multicomponent transport on the last
# solution.
gas = ct.Solution('mech.cti')

# set its state to that of the unburned gas at the burner
gas.TPX = tburner, p, comp

# create the BurnerFlame object.
f = ct.BurnerFlame(gas=gas, width=width)

# set the mass flow rate at the burner
f.burner.mdot = mdot

# read temperature vs. position data from a file.
# The file is assumed to have one z, T pair per line, separated by a comma.
zloc, tvalues = np.genfromtxt('tdata.dat', delimiter=',', comments='#').T
zloc /= max(zloc)

# set the temperature profile to the values read in
f.flame.set_fixed_temp_profile(zloc, tvalues)

# show the initial estimate for the solution
f.show_solution()

# don't solve the energy equation
f.energy_enabled = False

# first solve the flame with mixture-averaged transport properties
f.transport_model = 'Mix'
f.set_refine_criteria(ratio=3.0, slope=0.3, curve=1)

f.solve(loglevel, refine_grid)
f.save('flame_fixed_T.xml','mixav',
       'solution with mixture-averaged transport')

print('\n\n switching to multicomponent transport...\n\n')
f.transport_model = 'Multi'

f.set_refine_criteria(ratio=3.0, slope=0.1, curve=0.2)
f.solve(loglevel, refine_grid)
f.save('flame_fixed_T.xml','multi',
       'solution with  multicomponent transport')

# write the velocity, temperature, density, and mole fractions to a CSV file
f.write_csv('flame_fixed_T.csv', quiet=False)
f.show_stats()

# Data sources
database(
	thermoLibraries = ['primaryThermoLibrary'],
	reactionLibraries = [],
	seedMechanisms = [],
	kineticsDepositories = ['training'], 
	kineticsFamilies = 'default',
	kineticsEstimator = 'rate rules',
)

# List of species
species(
	label='SO3',
	reactive=True,
	structure=SMILES("O=S(=O)=O"),
)
species(
	label='N2',
	reactive=True,
	structure=SMILES("N#N"),
)

# Reaction systems
simpleReactor(
	temperature=(1350,'K'),
	pressure=(1.0,'bar'),
	initialMoleFractions={
		"SO3": 1,
		"N2": 1,
	},
	terminationTime=(1e-9,'s'),
)

simulator(
	atol=1e-16,
	rtol=1e-8,
)

model(
	toleranceKeepInEdge=1e-5,
	toleranceMoveToCore=0.01,
	toleranceInterruptSimulation=0.1,
	maximumEdgeSpecies=9999999
)

options(
	units='si',
	saveRestartPeriod=None,
	generateOutputHTML=True,
	generatePlots=False,
)

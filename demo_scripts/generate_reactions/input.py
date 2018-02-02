# Data sources
database(
    thermoLibraries = ['BurkeH2O2','primaryThermoLibrary','thermo_DFT_CCSDTF12_BAC','DFT_QCI_thermo','FFCM1(-)','CHN','GRI-Mech3.0-N'],
    reactionLibraries = ['BurkeH2O2inArHe','NOx','FFCM1(-)','Nitrogen_Dean_and_Bozzelli'],
    seedMechanisms = [],
    kineticsDepositories = ['training'],
    kineticsFamilies = 'default',
    kineticsEstimator = 'rate rules',
)

# List of species
species(
    label='NO2',
    reactive=True,
    structure=SMILES("[O]N=O"),
)

species(
    label='N',
    reactive=True,
    structure=SMILES("[N]"),
)

species(
    label='Ar',
    reactive=False,
    structure=adjacencyList(
                """
                1 Ar u0 p4 c0
                """),
)

# Reaction systems
simpleReactor(
    temperature=(1500,'K'),
    pressure=(1,'atm'),
    initialMoleFractions={
        "NO2": 0.0005,
		"N": 0.002,
		"Ar": 0.9975,
    },
    terminationTime=(0.002,'s'),
)

simulator(
    atol=1e-16,
    rtol=1e-8,
)

model(
    toleranceKeepInEdge=0,
    toleranceMoveToCore=0.2,
    toleranceInterruptSimulation=0.2,
    maximumEdgeSpecies=300000
)

options(
    units='si',
    generateOutputHTML=False,
    generatePlots=False,
    saveEdgeSpecies=True,
    saveSimulationProfiles=False,
	saveRestartPeriod=None,
)

generatedSpeciesConstraints(
    allowed=['input species','seed mechanisms','reaction libraries'],
    maximumCarbonAtoms=9,
    maximumOxygenAtoms=9,
    maximumNitrogenAtoms=9,
    maximumSiliconAtoms=0,
    maximumSulfurAtoms=9,
    maximumHeavyAtoms=15,
    maximumRadicalElectrons=3,
    allowSingletO2=False,
)

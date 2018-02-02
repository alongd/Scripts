
# Data sources
database(
    thermoLibraries = ['BurkeH2O2','primaryThermoLibrary','thermo_DFT_CCSDTF12_BAC','DFT_QCI_thermo','FFCM1(-)','JetSurF2.0'],
    reactionLibraries = ['BurkeH2O2inN2','FFCM1(-)','JetSurF2.0'],
    seedMechanisms = [],
    kineticsDepositories = ['training'],
    kineticsFamilies = 'default',
    kineticsEstimator = 'rate rules',
)

# List of species
species(
    label='fuel',
    reactive=True,
    structure=SMILES('OC(O)'),
)

species(
    label='O2',
    reactive=True,
    structure=SMILES('[O][O]'),
)

species(
    label='N2',
    reactive=False,
    structure=SMILES('N#N'),
)

species(
    label='OH',
    reactive=True,
    structure=SMILES('[OH]'),
)

# Reaction system
simpleReactor(
    temperature=(1500.0,'K'),
    pressure=(1.0,'atm'),
    initialMoleFractions={
        'fuel': 1.0,
        'O2': 1,
        'N2': 3.76,
    },
    terminationTime=(0.001,'s'),
    sensitivity=['OH'],
    sensitivityThreshold=0.01,
)

simulator(
    atol=1e-16,
    rtol=1e-8,
    sens_atol=1e-6,
    sens_rtol=1e-4,
)

model(
    toleranceKeepInEdge=0,
    toleranceMoveToCore=0.05,
    toleranceInterruptSimulation=0.05,
    maximumEdgeSpecies=300000
)

#pressureDependence(
#        method='modified strong collision',
#        maximumGrainSize=(0.5,'kcal/mol'),
#        minimumNumberOfGrains=250,
#        temperatures=(298,2500,'K',10),
#        pressures=(0.5,3,'bar',5),
#        interpolation=('Chebyshev', 6, 4),
#        maximumAtoms=16,
#)

options(
    units='si',
    generateOutputHTML=True,
    generatePlots=False,
    saveEdgeSpecies=False,
    saveSimulationProfiles=True,
    saveRestartPeriod=None,
)

generatedSpeciesConstraints(
    allowed=['input species','seed mechanisms','reaction libraries'],
    maximumCarbonAtoms=5,
    maximumOxygenAtoms=2,
    maximumNitrogenAtoms=0,
    maximumSiliconAtoms=0,
    maximumSulfurAtoms=0,
    maximumHeavyAtoms=6,
    maximumRadicalElectrons=2,
    allowSingletO2=False,
)



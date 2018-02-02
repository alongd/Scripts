#!/usr/bin/env python
# encoding: utf-8

# these are some supporting functions for the PDepPostProcessing iPython notebook

import os
    
def RMGlog(net):
    try:
        chem = open('runs/net'+str(net)+'/chemkin/chem_annotated.inp','r').readlines()
        lines = [x for x in chem[17:] if x != "\n"]
	readSpecies = False
	species = -2 # not counting CH4(1), O2(2)
	readRxns = False
	rxns = 0
	for line in lines:
	    if "SPECIES" in line:
		readSpecies = True
	    if "REACTIONS" in line:
		readRxns = True
	    if "END" in line:
		readSpecies = readRxns = False
	    if readSpecies:
		if '(' in line:
		    species += 1
	    if readRxns:
		if 'Reaction index' in line:
		    rxns += 1
	print("Done simulating net{0} with {1} species and {2} reactions.\n".format(net,species,rxns))
    except:
	return 1
    return 0

def saveFig(plt,run_name,subname):
    fig_path = run_name+'/AnalysisScriptFigs/'
    fig_name = fig_path+'{0}_{1}.png'.format(run_name,subname)
    if not os.path.exists(fig_path):   # create fig folder if doesnt exist
        os.mkdir(fig_path)
    plt.savefig(fig_name, dpi = 300)

def findClosest(value,list): # return the index of the entry with the closes value to the input
    index = 0
    for x in xrange(len(list)):
        if abs(value - list[x]) < abs(value - list[index]):
            index = x
    return index


def createInputFile(net):
    cwd = os.getcwd()
    if not os.path.exists(cwd+'/runs/'):
        os.mkdir(cwd+'/runs/')
    if not os.path.exists(cwd+'/runs/net{0}/'.format(net)):
        os.mkdir(cwd+'/runs/net{0}/'.format(net))

    inputFile = '''
database(
    thermoLibraries = ['BurkeH2O2','primaryThermoLibrary','NG_HTP','Chernov','Narayanaswamy'],
    reactionLibraries = [],
    seedMechanisms = ['networks/net'''+str(net)+''''],
    kineticsDepositories = [],
    kineticsFamilies = 'default',
    kineticsEstimator = 'rate rules',
)

species(
    label='CH4',
    reactive=True,
    structure=SMILES('C'),
)

species(
    label='O2',
    reactive=True,
    structure=SMILES('[O][O]'),
)


species(
    label='Ar',
    reactive=False,
    structure=adjacencyList(
                """
                1 Ar u0 p4 c0
                """),
)

simpleReactor(
    temperature=(2000,'K'),
    pressure=(1,'atm'),
    initialMoleFractions={
		"CH4": 0.015,
		"O2": 0.02,
		"Ar": 0.9,
    },
    terminationTime=(0.001,'s'),
)

simulator(
    atol=1e-16,
    rtol=1e-8,
)

model(
    toleranceKeepInEdge=0,
    toleranceMoveToCore=0.05,
    toleranceInterruptSimulation=0.05,
    maximumEdgeSpecies=300000
)

pressureDependence(
        method='modified strong collision',
        maximumGrainSize=(0.5,'kcal/mol'),
        minimumNumberOfGrains=250,
        temperatures=(1600,2200,'K',10),
        pressures=(0.5,1.5,'bar',5),
        interpolation=('Chebyshev', 6, 4),
        maximumAtoms=16,
)

options(
    units='si',
    generateOutputHTML=False,
    generatePlots=False,
    saveEdgeSpecies=False,
    saveSimulationProfiles=False,
    saveRestartPeriod=None,
)

generatedSpeciesConstraints(
    allowed=['input species','seed mechanisms','reaction libraries'],
    maximumCarbonAtoms=10,
    maximumOxygenAtoms=10,
    maximumNitrogenAtoms=0,
    maximumSiliconAtoms=0,
    maximumSulfurAtoms=0,
    maximumHeavyAtoms=15,
    maximumRadicalElectrons=1,
    allowSingletO2=False,
)

'''

    path = cwd+'/runs/net{0}/input.py'.format(net)
    with open(path,'w') as RMGInputFile:
        RMGInputFile.write(inputFile)
    return



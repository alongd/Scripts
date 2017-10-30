#!/usr/bin/env python
# encoding: utf-8

# these are some supporting functions for the ModelAnalysisScript iPython notebook

import os

def createInput(run_name = 'default', inputFile = ''):
    if not os.path.exists(run_name):   # create run folder if doesnt exist
        os.mkdir(run_name)
    full_path = run_name+'/input.py'
    os.system('rm -r '+run_name+'/*')  # clear the folder
    with open(full_path,'w') as RMGInputFile:
        RMGInputFile.write(inputFile)
    print("Crerated RMG input file: "+full_path)
    return
    
def RMGlog(run_name = 'default'):
    print("RMG Simulation Completed. Summary of log file:\n")
    try:
        RMG_log = open(run_name+'/RMG.log','r').readlines()
        lines = [x for x in RMG_log[-13:-1] if x != "\n"]
        matchers = ['DD','MODEL','used','final']   # print only lines contating these stings
        matching = [s for s in lines if any(xs in s for xs in matchers)]
        for line in matching: print line
    except: print("ERROR!")
    return

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













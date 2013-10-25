
class Parameters(object):
    # zmiany parametrow
    changeSeries = False
    seriesParameterToChange = "aqPositiveNegativeCount"
    seriesStart = 30
    seriesDelta = 10
    seriesNumber = 10
        
    
    
    #               EMAS                    GEN
    algorithms = ['GeneticSimulation', 'EvolutionarySimulation']
    algorithm = algorithms[0]

    mutationsType = ['continuousDistribution', 'normalDistribution','discreteDistribution1n1','discreteFlip','adaptiveMutation']

    '''Configuration of mutations'''
    mutation = mutationsType[4]
    
    crossoverTypes = ['SinglePoint','SinglePointPermutation']
    crossover = crossoverTypes[0]



    simSteps = 5000
    agentSteps = None

    
    '''Memetic parameters (general)'''   
    memeticsModes = ['None', 'Lamarck', 'Baldwin']
    memetics = memeticsModes[0]
    
    
    
    memetizationProbability = 10
    memeticMaxEvals = 10
    memeticRho = 0.1
    memeticMutations = ['SolisWets', 'Isotropic','Brent'] # brent dosc wyraznie preferuje poczatek ukladu wsp... 
    memeticMutation = memeticMutations[1]



    
    showOutput = False
    printStats = False
    printStatsGlobal = True
    printHerdStats = False
    drawCharts = False
    
    '''How many simulations to launch consecutively.'''
    simulations = 3
    
    '''In our example it means, that they are 3 normalized float values (RGB)'''
    genotypeLength = 50

    '''Machine Learning memetization managers'''
    memetizationManagers = ['None', 'AQMemetizationManager', 'NBMemetizationManager']
    memetizationManager = memetizationManagers[0]

    '''Number of positive/negative individuals'''
    aqPositiveNegativeCount = 50
    
    '''Monitors to use'''
    monitors = [
                #'AgentStepsCountMonitor',            # GEN -
                #'CenterOfGravityMonitor',            # GEN -
                #'CenterOfGravityMoveMonitor',        # -   -
                #'DieAndReproductionMonitor',         # GEN -
                #'DistFromCoGMonitor',                # -   -
                'PopulationCountMonitor',            # GEN -
                #'ReadyToReproductionMonitor',        # GEN -
                # 'ResultMonitor',                     # GEN EVOL
                #'SimStepsToMakeResultBetterMonitor', # GEN -                 
                #'StatsCollector',                    # GEN EVOL
                #'DiversityMonitor',                   # GEN EVOL                
                'DiversityMonitor','BestFitnessMonitor',                   # GEN EVOL
                'EnergyMonitor'                         #GEN
                ]
    
    actionMonitors = [
                #'ReproductionFailMonitor',           # GEN - 
                #'SimilarityReproductionMonitor',     # GEN -
                ]

    '''Fitness function'''
    
    
    # DYSKRETNE
    #http://www.lcc.uma.es/~ccottap/papers/labsASC.pdf
    #function = 'LABS'
    
#    function = 'LABS'
    
    # genotype length=16
#    function = 'RoyalRoad'
    
    
    # genotype length na razie 10
    #function = 'JobShop'
    #jobShopGenotypes=['SimplePermutation','JobPriority']
    #jobShopGenotype=jobShopGenotypes[1] 
    # przy simple permutation dlugosc genotypu jest taka jak liczba zadan
    # przy job probability dlugosc genotypu jest taka jak liczba zadan x liczba operacji
    
    # CIAGLE
    #http://sci2s.ugr.es/eamhco/functions1-19.pdf
    #http://www.geatbx.com/docu/fcnindex-01.html
    
    
    
    
    initializations = ['REAL', 'DISCRETE1n1','PERMUTATION','PERMUTATIONJS2']
    initialization = initializations[0]    
    
    
    
    # ALBO EWENTUALNIE DLA WSZYSTKICH
    #cubeSize = 10
    
    #function = 'Rastrigin'
    #cubeSize = 10
    #cubeSize = 5.12

    #function = 'FrequencyModulatedSoundWaves'
    #cubeSize = 6.35
    
    #function = 'Rosenbrock'
    #cubeSize = 2.048
    
    #function = 'Ackley'
    #cubeSize = 1

    function = 'DeJong'
    cubeSize = 5.12
    
    #function = 'AxisParallelHyperEllipsoid'
    #cubeSize = 5.12
    
    #function = 'RotatedHyperEllipsoid'
    #cubeSize = 65.536
    
    #function = 'MovedAxisParallelHyperEllipsoid'    
    #cubeSize = 5.12
    
    #function = 'Griewangk'
    #cubeSize = 600
    
    #function = 'SumOfPowerFunctions' #-1:1
    #cubeSize = 1
    
    
    #function = 'Schwefel' # -500:500
    #cubeSize = 500
    
    #function = 'DeJongDynamic'
    #function = 'RastriginDynamic'
    
    '''Determines size of space where we search for result. For example if cubeSize=a, 
       then coordinates is from [-a, a], so it creates a cube with lines of length equals 2a
    '''
#    
    
    agentCount = 30
    herdAgentsCount = 3
    
    '''Has to be divisible by 2'''
    initEnergy = 100
    
    fieldSize = 10
    
    reproductionMinEnergy = 90
    
    #ORYGINIALNE PARAMETRY
    #fightEnergyWin = 20
    #fightEnergyLoose = -20

    fightEnergyWin = 40
    fightEnergyLoose = -40

    
    dieEnergy = 0
    
    meetingProbability = 1
    
    
    '''Migration probability [0.0 - 1.0]'''
    migrationProbability = 0.01
    
    '''Used only in continuousDistribution. It has to be float (0,1)'''
    mutationFactor = [0.1]
    
    '''Normally mutation value is from [0,1], by it will by multiply by mutationMaxValue'''
    mutationMaxValue = 1

    '''Number of timestamps, after which stats are written into file'''
    statsCollectFreq = 100
    
    
    ''' ############################# Evolutionary alg params ################### '''
    matingPoolSize = 8
    bestNumber = 0

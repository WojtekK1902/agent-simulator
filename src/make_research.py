import os, datetime, subprocess, shutil
from implementation.Parameters import Parameters
from numpy import mean, std

files = ['count.txt', 'diversity.txt', 'fitness.txt', 'reproduceCount.txt', 'reproductionHistory.txt']

for i in range(Parameters.herdAgentsCount):
    files.append('energy' + str(i+1) + '.txt')

#usuwam stare pliki z wynikami
for f in files:
    if os.path.exists(f):
    	os.remove(f)

#tworze nowy folder
folder_name = Parameters.algorithm + Parameters.memetics + "_" + datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
os.makedirs('results/' + folder_name)

#uruchamiam obliczenia
execfile('main.py')

if 'fitness.txt' in files:
    #tworze slownik {iteracja:[lista wartosci fitness]}
    f = open('fitness.txt', 'r')
    fitness_dict = {}
    for line in f:
        l = line.strip().split(';')
        fits = fitness_dict.get(int(l[0]),[])
        fits.append(float(l[1]))
        fitness_dict[int(l[0])] = fits
    f.close()

    keys = fitness_dict.keys()
    keys.sort()

    f = open('results/'+folder_name+'/fitness.data','w')
    for i in keys:
        f.write(str(i) + ' ' + str(mean(fitness_dict[i])) + ' ' + str(std(fitness_dict[i])) + '\n')
    f.close()

if 'reproductionHistory.txt' in files:
    #tworze slownik {iteracja:[srednia ilosc udanych reprodukcji na wyspie]}
    f = open('reproductionHistory.txt', 'r')
    reprHistory_dict = {}
    for line in f:
        l = line.strip().split(';')
        rh = reprHistory_dict.get(int(l[0]), [])
        rh.append(float(l[1]))
        reprHistory_dict[int(l[0])] = rh
    f.close()

    keys = reprHistory_dict.keys()
    keys.sort()

    f = open('results/'+folder_name+'/reproductionHistory.data','w')
    for i in keys:
        f.write(str(i) + ' ' + str(mean(reprHistory_dict[i])) + ' ' + str(std(reprHistory_dict[i])) + '\n')
    f.close()

if 'energy1.txt' in files:
    for i in range(Parameters.herdAgentsCount):
        f = open('energy' + str(i+1) + '.txt')
        energy_dict = {}
        for line in f:
            l = line.strip().split(';')
            energies = [float(x) for x in l[1].strip('\n[]').split(', ')]
            en = energy_dict.get(int(l[0]), [])
            en.append(mean(energies))
            energy_dict[int(l[0])] = en
        f.close()

        f = open('results/' + folder_name + '/' + 'energy' + str(i+1) + '.data','w')
        for i in keys:
            f.write(str(i) + ' ' + str(mean(energy_dict[i])) + ' ' + str(std(energy_dict[i])) + '\n')
        f.close()

for f in files:
    if os.path.isfile(f):
        shutil.move(f, 'results/' + folder_name +'/' + f)
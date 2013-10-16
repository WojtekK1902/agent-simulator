import os, datetime, subprocess, shutil
from implementation.Parameters import Parameters
from numpy import mean, std

files = ['count.txt', 'diversity.txt', 'fitness.txt', 'reproduceCount.txt']

#usuwam stare pliki z wynikami
for f in files:
    if os.path.exists(f):
    	os.remove(f)

#tworze nowy folder
folder_name = Parameters.algorithm + Parameters.memetics + "_" + datetime.datetime.now().strftime("%Y-%m-%d_%H_%M")
os.makedirs('results/' + folder_name)

#uruchamiam obliczenia
execfile('main.py')

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

shutil.move('fitness.txt', 'results/'+folder_name+'/fitness.txt')
shutil.move('count.txt', 'results/'+folder_name+'/count.txt')
shutil.move('diversity.txt', 'results/'+folder_name+'/diversity.txt')
if os.path.isfile('reproduceCount.txt'):
    shutil.move('reproduceCount.txt', 'results/'+folder_name+'/reproduceCount.txt')

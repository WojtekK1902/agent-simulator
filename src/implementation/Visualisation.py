from implementation.Parameters import Parameters
class Visualisation(object):
    
    def __init__(self, filename='out.txt'):
        if(Parameters.drawCharts == False):
            return
        import os
        self.filename = filename
        if os.path.isfile(self.filename):
            os.remove(self.filename)
    
    def _sum(self, params, index):
        sumVal = 0
        for param in params:
            sumVal += param[index]
        return sumVal
    
    def _min(self, params, index):
        minVal = params[0][index]
        for param in params:
            minVal = min(minVal, param[index])
        return minVal
    
    def _max(self, params, index):
        maxVal = params[0][index]
        for param in params:
            maxVal = max(maxVal, param[index])
        return maxVal
    
    def visualise(self, params):
        f = None
        if(Parameters.drawCharts == True):
            f = open(self.filename, 'a')
        count = 0
        
        agregatedParams = [self._sum(params, 0),
                           self._sum(params, 1),
                           self._min(params, 2),
                           self._max(params, 3)]
        
        if Parameters.printHerdStats:
            for items in params:
                line = " ".join(map(lambda x: str(x), items)) + " "
                if(Parameters.showOutput):
                    print "herd "+str(count)+": "+line
                    count+=1
            
        line = " ".join(map(lambda x: str(x), agregatedParams)) + " "
        if(Parameters.showOutput):
            print "summary: "+line

        if f:
                f.write(line)
                
        

        if f:
            f.write('\n')
            f.close()

    def show(self):
        if(Parameters.drawCharts == False):
            return
        import matplotlib.pyplot as plt
        from collections import defaultdict
        
        lines = [line.strip().split(' ') for line in open(self.filename).readlines()]
        numparams = len(lines[0])
        
        values = []
        for num, line in enumerate(lines):
	    values += [[num] + map(lambda x: float(x), line)]
        
        #ymax = 0
        plots = defaultdict(list)
        for i in xrange(len(values)):
	    for j in xrange(0, numparams + 1):
		plots[j] += [values[i][j]]
		#if values[i][j] > ymax:
		    #ymax = values[i][j]
	ids = plots[0]
	del plots[0]
	
	# TODO - this is hardcoded. Prop. solution:
	# data to plot passed by dict with labels (name of the
	# parameter to visualise) so the file has heading with legend
	legends = {1: 'count', 2: 'energy', 3: 'min', 4: 'max'}#, 5: 'reproduce', 6: 'die'}
	
	for k, vals in plots.items():
	    plt.plot(ids, vals, label=legends[k])	 
	
	# TODO - yrange is hardcoded, prop. solution: multiple subplots
	plt.axis([0, len(lines), 0, 70])
	
	plt.legend()
	plt.xlabel('Population number')
	plt.title('Symulator')
        plt.show()

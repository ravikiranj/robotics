import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

#start drawBasePlot
def drawBasePlot(w_min, w_max):
    fig = plt.figure(figsize = (12,10))
    ax = fig.add_subplot(111)
    ax.set_xlim(w_min, w_max+10)
    ax.set_ylim(w_min, w_max+10)
    ax.set_title('Projectile Path')
    ax.set_xlabel('X - Axis')
    ax.set_ylabel('Y - Axis')

    return {'figure': fig, 'plot' : plt, 'axes' : ax}
#end of drawBasePlot

#start updatePlot
def updatePlot(initDraw, x, y):    
    fig = initDraw['figure']
    plt = initDraw['plot']
    ax = initDraw['axes']
    #plt.plot(x, y, 'g.', markersize = 10)
    c = mpatches.Circle((x, y), 1, fc="w")                
    ax.add_patch(c)
    return {'figure': fig, 'plot' : plt, 'axes' : ax}
    #filename = 'results/'+str(step)+'.png'
    #fig.savefig(filename)    
#end updatePlot

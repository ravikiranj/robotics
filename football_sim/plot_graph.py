import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

count = 0
draw_turn = 0
draw_size = 0

#start drawBasePlot
#def drawBasePlot(w_min, w_max, params):
def drawBasePlot(w_min, w_max, N, d):
    global draw_turn
    global draw_size
    draw_turn = int(N * 0.05)
    if(draw_turn < 1):
        draw_turn = 1
    draw_size = int(2 * d / 250)
    if(draw_size < 2):
        draw_size = 1
    fig = plt.figure(figsize = (12,10))
    ax = fig.add_subplot(111)
    ax.set_xlim(w_min, w_max + 0.25 * w_max)
    ax.set_ylim(w_min, w_max + 0.25 * w_max)
    title = "Projectile Trajectory Plot"
    ax.set_title(title)
    ax.set_xlabel('X - Axis')
    ax.set_ylabel('Y - Axis')

    return {'figure': fig, 'plot' : plt, 'axes' : ax}
#end of drawBasePlot

#start updatePlot
def updatePlot(initDraw, x, y, color):    
    global count
    fig = initDraw['figure']
    plt = initDraw['plot']
    ax = initDraw['axes']
    #plt.plot(x, y, 'g.', markersize = 10)
    if(count % draw_turn == 0):
        #plt.plot(x, y, 'g*', markersize = 5, markerfacecolor=color)
        c = mpatches.Circle((x, y), draw_size, fc=color)
        ax.add_patch(c)
    count += 1
    return {'figure': fig, 'plot' : plt, 'axes' : ax}
    #filename = 'results/'+str(step)+'.png'
    #fig.savefig(filename)    
#end updatePlot

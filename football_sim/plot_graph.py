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
def drawBasePlot(w_min, w_max, N, d, model_name):
    global draw_turn
    global draw_size
    draw_turn = int(N * 0.05)
    if(draw_turn < 1):
        draw_turn = 1
    draw_size = int(2 * d / 250)
    if(draw_size < 2):
        draw_size = 1
    temp = model_name.split('/')
    model_name = temp[len(temp)-1].split('.')[0].capitalize()
    fig = plt.figure(figsize = (12,10))
    ax = fig.add_subplot(111)
    ax.set_xlim(w_min, w_max + 0.25 * w_max)
    ax.set_ylim(w_min, w_max + 0.25 * w_max)
    title = "Projectile Trajectory Plot for " + model_name
    ax.set_title(title)
    ax.set_xlabel('X - Axis')
    ax.set_ylabel('Y - Axis')

    return {'figure': fig, 'plot' : plt, 'axes' : ax}
#end of drawBasePlot

#start updatePlot
def updatePlot(initDraw, posxy, color):    
    global count
    fig = initDraw['figure']
    plt = initDraw['plot']
    ax = initDraw['axes']
    #plt.plot(x, y, 'g.', markersize = 10)

    for xy in posxy:
        if(count % draw_turn == 0):
            c = mpatches.Circle((xy[0], xy[1]), draw_size, fc=color)
            ax.add_patch(c)
        count += 1
    #end loop

    return {'figure': fig, 'plot' : plt, 'axes' : ax}
    #filename = 'results/'+str(step)+'.png'
    #fig.savefig(filename)    
#end updatePlot

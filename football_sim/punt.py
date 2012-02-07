#!/usr/bin/python
#import required libraries
import math 
import random
import sys
import os
import glob
import plot_graph
from plot_graph import *

#Constants
DEBUG = False 
#DEBUG = True

#start get_models
def get_models():
    path = 'models/'
    return glob.glob(os.path.join(path, '*.ml'))
#end get_models    

#start read_params
def read_params(files):
    params = {}
    #Choose Model
    print "Available Models"
    print "================="
    count = 1
    for file in files:
        print "%d : %s" % (count, file)
        count += 1
    choice = int(raw_input("\nModel to load  = "))
    if(choice < 1 or choice > len(files)):
        print "Choosing default model = football"
        params['model'] = 'models/football.ml'
    else:
        params['model'] = files[choice-1]

    #Read the required parameters
    params['v'] = float(raw_input('Enter the velocity (m/s) = '))
    params['theta_deg'] = float(raw_input('Enter the launch angle (degrees) = '))
    params['theta'] = params['theta_deg'] * math.pi / 180;
    return params
#end read_params
#start init
def init():
    global initDraw
    files = get_models()
    params = read_params(files)
    v = params['v']
    model_file = params['model']
    theta_deg = params['theta_deg']
    theta = params['theta']

    g = 9.8
    max_dist = pow(v,2) * math.sin(2 * theta) / g
    t = 2 * v * math.sin(theta) / g
    dt = 0.1
    N = t / dt

    model_params = read_model(model_file);
    initDraw = drawBasePlot(0, max_dist+50, N, max_dist)
    projectile(v, theta, dt)
    projectile_with_drag(v, theta, float(model_params['drag_coefficient']), dt)
    initDraw['plot'].show()
#end init

#start projectile_with_drag
def projectile_with_drag(v, theta, drag_coefficient, dt):
    global initDraw
    #k = rho * C * A / 2
    k = drag_coefficient 
    vx = v * math.cos(theta)
    vy = v * math.sin(theta) 
    x = 0
    y = 0
    t = 0
    ax = 0
    ay = 0
    g = 9.8
    maxy = 0
    if(DEBUG):
        print "ax = %.3f, ay = %.3f, vx = %.3f, vy = %.3f, v = %.3f, x = %.3f, y = %.3f, t = %.3f" % (ax, ay, vx, vy, v, x, y, t)
    while(True):
        ax = -k * v * vx
        ay = -k * v * vy - g
        vx += ax * dt
        vy += ay * dt
        v = math.sqrt(pow(vx, 2) + pow(vy, 2))
        x += vx * dt + ax * pow(dt, 2)
        y += vy * dt + ay * pow(dt, 2)
        if(y > maxy):
            maxy = y
        if(y < 0):
            break
        t += dt
        if(DEBUG):
            print "ax = %.3f, ay = %.3f, vx = %.3f, vy = %.3f, v = %.3f, x = %.3f, y = %.3f, t = %.3f" % (ax, ay, vx, vy, v, x, y, t)
        updatePlot(initDraw, x, y, 'r')
    #end of while loop
    print "Projectile with Drag - Horizontal Distance = %.3f m, Max Height = %.3f m, Total time of flight = %.3f secs" % (x, maxy, t)
    annonate_str = "with drag\n======\nx = "+str(round(x,2))+"m\nmaxy = "+str(round(maxy,2))+"m\nt = "+str(round(t,2))+" secs"
    initDraw['axes'].annotate(annonate_str, xy=(0.1, 0.1), xycoords='axes fraction', xytext=(0.8, 0.8), textcoords='axes fraction')

    #initDraw['plot'].show()
#end projectile_with_drag

#start projectile
def projectile(v, theta, dt):
    global initDraw
    t = 0
    g = 9.8
    xprev = 0
    yprev = 0
    vv_prev = 0
    vh_prev = 0
    maxy = 0
    while(True):
        x = v * t * math.cos(theta)
        y = (v * t * math.sin(theta)) - (0.5 * g * t * t)
        if(y > maxy):
            maxy = y
        if(y < 0):
            #For better precision, don't exit unless you're 0.1m near the solution
            if(yprev > 0.1):
                t = t - dt
                dt = dt / 10
                continue
            t -= dt
            break
        updatePlot(initDraw, x, y, 'g')
        vv_curr = (y - yprev) / dt
        vh_curr = (x - xprev) / dt
        v_acc = (vv_curr - vv_prev) / dt
        h_acc = (vh_curr - vh_prev) / dt
        if(DEBUG):
            print "x = %.2f, y = %.2f, t = %.2f, vv = %.2f, vh = %.2f" % (x, y, t, vv_curr, vh_curr)
        t = t + dt
        xprev = x
        yprev = y
        vv_prev = vv_curr
        vh_prev = vh_curr
    #end while loop
    print "Projectile - Horizontal Distance = %.3f m, Max Height = %.3f m, Total time of flight = %.3f secs" % (x, maxy, t)
    annonate_str = "without drag\n========\nx = "+str(round(x,2))+"m\nmaxy = "+str(round(maxy,2))+"m\nt = "+str(round(t,2))+" secs"
    initDraw['axes'].annotate(annonate_str, xy=(0.1, 0.1), xycoords='axes fraction', xytext=(0.1, 0.8), textcoords='axes fraction')
#end projectile

#start read_model
def read_model(filename):
    params = {}
    try:
        f = open(filename)
        s = f.readline()
        while(s != ""):
            arr = s.split('=')
            params[arr[0].rstrip().strip()] = arr[1].rstrip().strip()
            s = f.readline()
        #end while
    except IOError as (errno, strerror):
        print "I/O error({0}): {1}".format(errno, strerror)
    return params
#end    

#Call init
if __name__ == "__main__":
    init()
#end 

#!/usr/bin/python
#import required libraries
import math 
import random
import sys
import os
import glob
import time
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
    if False:
        #Choose Model
        print "Available Models"
        print "================="
        count = 1
        for file in files:
            filename = file.split('/')
            print "%d : %s" % (count, filename[len(filename)-1])
            count += 1
        choice = int(raw_input("\nModel to load  = "))
        if(choice < 1 or choice > len(files)):
            print "Choosing default model = football"
            params['model'] = 'models/football.ml'
        else:
            params['model'] = files[choice-1]
    #end comment
    params['model'] = 'models/football.ml'

    #Read the required parameters
    params['dist'] = float(raw_input('Enter the target distance (m) = '))
    return params
#end read_params

#start init
def init():
    global initDraw
    files = get_models()
    params = read_params(files)
    x = params['dist']
    model_file = params['model']

    g = 9.8
    theta_deg_arr = range(20,45)
    opt_vel = 999999

    draw = 0
    firstOnly = False
    model_params = read_model(model_file);
    start_time = time.time()
    for theta_deg in theta_deg_arr:
        #Choose velocity such that we can reach the the target distance 'x', chosen the initial angle 'theta' 
        theta = (theta_deg * math.pi)/180
        v = math.sqrt((x * g) / math.sin(2 * theta))
        
        #Compute Max Height and Distance
        maxy = (math.pow(v, 2) * math.pow(math.sin(theta), 2)) / (2 * g)
        maxx = pow(v,2) * math.sin(2 * theta) / g

        t = 2 * v * math.sin(theta) / g
        dt = 0.1
        N = t / dt


        projectile(v, theta, dt, draw)
        projProps = projectile_with_drag(v, theta, x, float(model_params['drag_coefficient']), dt, draw, firstOnly)
        if(projProps['v'] < opt_vel and projProps['dist'] >= 0.95 * x and projProps['dist'] <= 1.05 *x):
            opt_dist = projProps['dist']
            opt_vel = projProps['v']
            opt_theta = projProps['theta']
        #end if
        if(draw):
            print "==========================================================================\n"
    #end loop
    if(opt_vel != 999999):
        draw = 1
        theta_deg = 45
        firstOnly = True
        theta = (theta_deg * math.pi) / 180
        v = math.sqrt((x * g) / math.sin(2 * theta))
        maxx = pow(v,2) * math.sin(2 * theta) / g
        initDraw = drawBasePlot(0, maxx+50, N, maxx, model_file)
        projectile(v, theta, dt, draw)
        projectile_with_drag(v, theta, x, float(model_params['drag_coefficient']), dt, draw, firstOnly)

        end_time = time.time()
        time_diff = end_time - start_time
        v = opt_vel
        theta = opt_theta
        firstOnly = False
        projectile_with_drag(v, theta, x, float(model_params['drag_coefficient']), dt, draw, firstOnly)
        print "Optimal Velocity = %.3f, Optimal Angle = %.3f, Optimal Distance = %.3f, CompTime = %.3f\n" % (opt_vel, (opt_theta * 180)/math.pi, opt_dist, time_diff)
        initDraw['plot'].show()
    else:
        print "No Solution found :(\n"
#end init

#start projectile_with_drag
def projectile_with_drag(v, theta, dist, drag_coefficient, dt, draw, firstOnly):
    global initDraw
    #k = rho * C * A / 2
    k = drag_coefficient 
    first = True
    iter_count = 1
    max_iter = 10000
    deltav = 0.1
    dist_low = 0.95 * dist
    dist_upp = 1.05 * dist
    accept_err = 0.01 * dist
    while(True): 
        v_init = v
        vx = v * math.cos(theta)
        vy = v * math.sin(theta) 
        x = 0
        y = 0
        t = 0
        theta_deg = (theta * 180) / math.pi
        ax = 0
        ay = 0
        g = 9.8
        maxy = 0
        posxy = []
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
            posxy.append([x, y])
        #end of while loop
        if(first and firstOnly):
            if(draw):
                print "With Drag - Distance = %.3f m, Max Height = %.3f m, Theta = %.2f, , Velocity = %.3f, Total time of flight = %.3f secs" % (x, maxy, theta_deg, v_init, t)
                annonate_str = "with drag (red)\n===========\nv = "+str(round(v_init,2))+"m/s\ntheta = "+str(round(theta_deg,2))+"deg\nx = "+str(round(x,2))+"m\nmaxy = "+str(round(maxy,2))+"m\nt = "+str(round(t,2))+" secs"
                initDraw['axes'].annotate(annonate_str, xy=(0.1, 0.1), xycoords='axes fraction', xytext=(0.38, 0.77), textcoords='axes fraction')
                updatePlot(initDraw, posxy, 'r')
            first = False
            break;
        #end if

        if(abs(x-dist) > accept_err and x >= dist_low and x <= dist_upp):
            lowdiff = abs(x - dist_low)
            highdiff = abs(x - dist_upp)
            if(lowdiff < highdiff):
                incr = deltav 
            else:
                incr = -deltav
            v = v_init + incr
        elif (x > dist):
            v = v_init - deltav 
        else:
            v = v_init + deltav 
        #end correction

        if(abs(x-dist) <= accept_err):
            if(draw):
                print "With Drag Corrected - Distance = %.3f m, Max Height = %.3f m, Theta = %.2f, Velocity = %.3f, Total time of flight = %.3f secs" % (x, maxy, theta_deg,  v_init, t)
                annonate_str = "with drag corrected (blue)\n==============\nv = "+str(round(v_init,2))+"m/s\ntheta = "+str(round(theta_deg,2))+"deg\nx = "+str(round(x,2))+"m\nmaxy = "+str(round(maxy,2))+"m\nt = "+str(round(t,2))+"\nIter Count = "+str(iter_count)
                initDraw['axes'].annotate(annonate_str, xy=(0.1, 0.1), xycoords='axes fraction', xytext=(0.68, 0.75), textcoords='axes fraction')
                updatePlot(initDraw, posxy, 'b')
            break
        #end exit condition

        iter_count += 1
        if(iter_count > max_iter):
            if(draw):
                print "Breaking after best possible solution found"
                print "With Drag Corrected - Distance = %.3f m, Max Height = %.3f m, Theta = %.2f, Velocity = %.3f, Total time of flight = %.3f secs" % (x, maxy, theta_deg,  v_init, t)
                annonate_str = "with drag corrected (blue)\n==============\nv = "+str(round(v_init,2))+"m/s\ntheta = "+str(round(theta_deg,2))+"deg\nx = "+str(round(x,2))+"m\nmaxy = "+str(round(maxy,2))+"m\nt = "+str(round(t,2))+"\nIter Count = "+str(iter_count)
                initDraw['axes'].annotate(annonate_str, xy=(0.1, 0.1), xycoords='axes fraction', xytext=(0.68, 0.75), textcoords='axes fraction')
                updatePlot(initDraw, posxy, 'b')
            break
        #end exit condition
    #end while loop
    return {'dist': x, 'v' : v_init, 'theta' : theta}
#end projectile_with_drag

#start projectile
def projectile(v, theta, dt, draw):
    global initDraw
    theta_deg = theta * 180 / math.pi
    t = 0
    g = 9.8
    xprev = 0
    yprev = 0
    vv_prev = 0
    vh_prev = 0
    maxy = 0
    v_init = v
    posxy = []
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
        posxy.append([x, y])
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
    if(draw):
        print "Without Drag - Distance = %.3f m, Max Height = %.3f m, Theta = %.2f, Velocity = %.3f, Total time of flight = %.3f secs" % (x, maxy, theta_deg, v_init, t)
        annonate_str = "without drag(green)\n========\nv = "+str(round(v_init,2))+"m/s\ntheta = "+str(round(theta_deg,2))+"deg\nx = "+str(round(x,2))+"m\nmaxy = "+str(round(maxy,2))+"m\nt = "+str(round(t,2))+" secs"
        updatePlot(initDraw, posxy, 'g')
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

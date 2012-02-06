#!/usr/bin/python
#import required libraries
import math 
import random
import plot_graph
from plot_graph import *

#start init
def init():
    parabolic_trajectory_model()
#end init

#start simulation
def simulation(u, d, theta, timestep, maxy):
    # s= u*t + 1/2*a*t^2;
    t = 0
    g = 9.8
    xprev = 0
    yprev = 0
    vv_prev = 0
    vh_prev = 0
    count = 0;
    initDraw = drawBasePlot(0, d)
    total_time = 2 * u * math.sin(theta) / g
    while(True):
        x = u * t * math.cos(theta)
        y = (u * t * math.sin(theta)) - (0.5 * g * t * t)
        if(y < 0 or count > 1000):
            #For better precision, don't exit unless you're 0.1m near the solution
            if(yprev > 0.1):
                t = t - timestep
                timestep = timestep / 10
                continue
            break
        #print "x = %.2f, y = %.2f, t = %.2f" % (x, y, t)
        #print "x = %.2f, y = %.2f, t = %.2f" % (x, y, t)
        updatePlot(initDraw, x, y)
        vv_curr = (y - yprev) / timestep
        vh_curr = (x - xprev) / timestep
        v_acc = (vv_curr - vv_prev) / timestep
        h_acc = (vh_curr - vh_prev) / timestep
        #print "vv = %.2f, vh = %.2f, v_acc = %.2f, h_acc = %.2f" % (vv_curr, vh_curr, v_acc, h_acc)
        t = t + timestep
        xprev = x
        yprev = y
        vv_prev = vv_curr
        vh_prev = vh_curr
        count = count + 1
    #end while loop
    t = t - timestep
    print "Total time of flight = %.2f secs, Predicted time of flight = %.2f" % (t, total_time)
    initDraw['plot'].show()
#end simulation

#start parabolic_trajectory_model
def parabolic_trajectory_model():
    #Refer http://en.wikipedia.org/wiki/Trajectory for explanation
    x = float(raw_input('Enter the target distance (m) = '))
    min_theta = 45
    max_theta = 75 
    #generate a random theta between min_theta and max_theta
    theta_deg = int((max_theta - min_theta) * random.random() + min_theta)
    theta = theta_deg * math.pi /180
    g = 9.8
    impact_time = 0.05
    football_weight = 0.425
    football_mass = football_weight / g
    
    v = math.sqrt((x * g) / math.sin(2 * theta))
    vv = v * math.sin(theta)
    vh = v * math.cos(theta)
    h = (math.pow(v, 2) * math.pow(math.sin(theta), 2)) / (2 * g)
    arclength = 0.25 * (2 * x * math.sqrt(1 + 4 * x * x) + math.asinh(2 * x)) 
    print "theta = %.2f deg, v = %.2f m/s, max_height = %.2f m" % (theta_deg, v, h)
    simulation(v, x, theta, 0.05, h)
#end parabolic_trajectory_model

#Start the program by invoking init
if __name__ == '__main__':
    init()

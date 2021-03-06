# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 João Faria
# This file is part of OPEN which is licensed under the MIT license.
# You should have received a copy of the license along with OPEN. See LICENSE.
#
"""
Utility functions or snippets for all sorts of things
"""

from math import sqrt, ceil
from sys import stdout
import os
import subprocess


## this code from 
##   http://code.activestate.com/recipes/502263-yet-another-unique-function/
## atributed to Paul Rubin
################################################################################
def unique(seq, keepstr=True):
    """ Return unique elements from enumerables (list, tuple, str)"""
    t = type(seq)
    if t==str:
        t = (list, ''.join)[bool(keepstr)]
    seen = []
    return t(c for c in seq if not (c in seen or seen.append(c)))



def day2year(day):
    """ Convert days to years """
    return day*0.00273791
    
    
def rms(array):
    return sqrt(sum(n*n for n in array)/len(array))
    
    
def stdout_write(msg):
	""" Print to stdout (without carriage return) and flush right away.
	Useful to print in the same line """
	stdout.write(msg)
	stdout.flush()



### Matplotlib advanced plot interaction stuff
from matplotlib.widgets import RectangleSelector
import numpy as np
import matplotlib.pyplot as plt

def line_select_callback(eclick, erelease):
    'eclick and erelease are the press and release events'
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    print ("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
    print (" The button you used were: %s %s" % (eclick.button, erelease.button))

def toggle_selector(event):
    print (' Key pressed.')
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        print (' RectangleSelector deactivated.')
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        print (' RectangleSelector activated.')
        toggle_selector.RS.set_active(True)

def selectable_plot(*args, **kwargs):
    fig, current_ax = plt.subplots()                    # make a new plotingrange

    plt.plot(*args, **kwargs)  # plot something

    # drawtype is 'box' or 'line' or 'none'
    toggle_selector.RS = RectangleSelector(current_ax, line_select_callback,
                                           drawtype='box', useblit=True,
                                           button=[1,3], # don't use middle button
                                           minspanx=5, minspany=5,
                                           spancoords='pixels')
    plt.connect('key_press_event', toggle_selector)
    plt.show()

def julian_day_to_date(J):
    """ Returns the date corresponding to a julian day number"""
    J = int(ceil(J))  # i think we need to do this...
    y=4716; v=3; j=1401; u=5; m=2; s=153; n=12; w=2; r=4; B=274277; p=1461; C=-38
    if len(str(int(J))) < 7: J = J+2400000
    f = J + j + (((4 * J + B)/146097) * 3)/4 + C
    e = r * f + v
    g = (e % p)/r
    h = u * g + w
    D = (h % s)/u + 1
    M = ((h/s + m) % n) + 1
    Y = e/p - y + (n + m - M)/n
    return (Y, M, D)


### Yorbit related I/O
def write_yorbit_macro(system):
    with open('./OPEN/yorbit.macro.template') as f:
        template = f.read()

    filenames = []
    for i,f in enumerate(system.provenance.keys()):
        cmd = 'cp ' + f + ' ' + '/home/joao/yorbit/data/rv_files/rv_file%d.rdb' % (i+1)
        filenames.append('rv_file%d.rdb' % (i+1))
        os.system(cmd)
        #print cmd
    #print filenames

    model = ''
    try:
        for key, val in system.model.iteritems():
            if val >0: model += '%s%d ' % (key, val)
    except AttributeError:
        model = raw_input('Which model? ')

    with open('/home/joao/yorbit/work/macros/macro1.macro', 'w') as f:
        print >>f, template % (' '.join(filenames), '', model)

    cmd = ['/home/joao/Software/yorbit/yorbit-1.4.6/src/batch/batch_macro.i']
    cmd += ['/home/joao/Software/yorbit/yorbit-1.4.6/src']
    cmd += ['macro1.macro']
    # print cmd
    with open('yorbit.log', "w") as outfile:
        subprocess.call(cmd, stdout=outfile)




def ask_yes_no(msg):
    # raw_input returns the empty string for "enter"
    yes = set(['yes','y', 'ye', ''])
    no = set(['no','n'])
    print msg,
    choice = raw_input().lower()
    if choice in yes:
        return True
    elif choice in no:
        return False
    else:
        stdout.write("Please respond with 'yes' or 'no'")
        return False
from pylab import figure, plot, ion, linspace, arange, sin, pi
from drawnow_lib import *
def draw_fig():
    # can be arbitrarily complex; just to draw a figure
    #figure() # don't call!
    plot(t, x)
    #show() # don't call!

N = 1e3
figure() # call here instead!
ion()    # enable interactivity
t = linspace(0, 2*pi, num=N)
for i in arange(100):
    x = sin(2 * pi * i**2 * t / 100.0)
    drawnow(draw_fig)

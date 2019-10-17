import numpy as np
import random
import scipy.misc as smp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib.widgets import Slider

def diamond(lx, ly, rx, ry, l): # upper left and lower right corners
    global heighmap, MAP_SIZE

    a = heighmap[lx, ly]
    b = heighmap[lx, ry]
    c = heighmap[rx, ly]
    d = heighmap[rx, ry]
    heighmap[lx + l, ly + l] = (a + b + c + d) / 4 + np.random.uniform(-roughness * l / MAP_SIZE, roughness * l / MAP_SIZE)

def square(x, y, l): # center of square
    global heighmap, MAP_SIZE

    a = heighmap[x - l, y] if (x - l) >= 0 else 0
    b = heighmap[x, y - l] if (y - l) >= 0 else 0
    c = heighmap[x + l, y] if (x + l) <= (MAP_SIZE - 1) else 0
    d = heighmap[x, y + l] if (y + l) <= (MAP_SIZE - 1) else 0

    heighmap[x, y] = (a + b + c + d) / 4 + np.random.uniform(-roughness * l / MAP_SIZE, roughness * l / MAP_SIZE)

def diamondSquare(lx, ly, rx, ry): # upper left and lower right corners
    l = (rx - lx) // 2
    
    diamond(lx, ly, rx, ry, l)
    square(lx, ly + l, l)
    square(lx + l, ly, l)
    square(rx - l, ry, l)
    square(rx, ry - l, l)

def generate():
    global heighmap, steps, save_path, MAP_SIZE

    heighmap[0, 0] = np.random.uniform(-roughness, roughness)
    heighmap[0, MAP_SIZE - 1] = np.random.uniform(-roughness, roughness)
    heighmap[MAP_SIZE - 1, 0] = np.random.uniform(-roughness, roughness)
    heighmap[MAP_SIZE - 1, MAP_SIZE - 1] = np.random.uniform(-roughness, roughness)
    
    if (save_path): steps.append(np.copy(heighmap))

    l = MAP_SIZE - 1
    while (l > 0):
        for x in range(0, MAP_SIZE - 1, l):
            for y in range(0, MAP_SIZE - 1, l):
                diamondSquare(x, y, x + l, y + l)
                if (save_path): steps.append(np.copy(heighmap))
        l = l // 2

def simple_visualization(): 
    global heighmap, MAP_SIZE
    
    x = range(MAP_SIZE)
    y = range(MAP_SIZE)
    X, Y = np.meshgrid(x, y)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    mycmap = plt.get_cmap('terrain')
    surf = ax.plot_surface(X, Y, heighmap, cmap=mycmap)
    fig.colorbar(surf, ax=ax)
    plt.show()

def slider_visualization(): 
    global heighmap, MAP_SIZE
    
    x = range(MAP_SIZE)
    y = range(MAP_SIZE)
    X, Y = np.meshgrid(x, y)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    mycmap = plt.get_cmap('terrain')
    surf = ax.plot_surface(X, Y, steps[0], cmap=mycmap)

    axhauteur = plt.axes([0.2, 0.1, 0.65, 0.03])
    slider = Slider(axhauteur, 'steps', 0, len(steps) - 1, valinit=0, valstep=1)

    def update(val): 
        i = int(slider.val) 
        ax.clear()
        surf = ax.plot_surface(X, Y, steps[i], cmap=mycmap)
        fig.canvas.draw_idle()

    slider.on_changed(update)
    plt.show()

def show_2dimage():
    global heighmap
    
    img = smp.toimage(heighmap)
    img.show() 

N = 3
MAP_SIZE = 2 ** N + 1 
heighmap = np.zeros((MAP_SIZE,MAP_SIZE), float)
roughness = 0.5 # roughness factor
steps = [np.copy(heighmap)]
save_path = True

generate()
print("Count steps: ", len(steps))

show_2dimage()
slider_visualization()
#simple_visualization()

import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import forward_model as fm
from crystal_dda.crystal_dda import branched_planar_dipoles
from crystal_dda.geometry import rotate
from crystal_dda.polygons import make_branched_planar

# canting
def cant(x, y, z, ang_side, ang_azi):
    ang_azi = ang_azi*np.pi/180.
    ang_side = ang_side*np.pi/180.

    meanx = np.mean(x)
    meany = np.mean(y)
    meanz = np.mean(z)
    x = x-meanx
    y = y-meany
    z = z-meanz

    xrot = np.cos(ang_side)*x-np.sin(ang_side)*z
    zrot = np.sin(ang_side)*x+np.cos(ang_side)*z
    return xrot+meanx, y+meany, zrot+meanz

# set values to create branched planar crystal with
a = 3.
amax = 3.
ac = 0.5

fb = 0.5
ft = 0.2
fg = 0.7

nsb = 5

ag = amax*fg

xp, yp = make_branched_planar(amax, ac, ft, fb, fg, nsb, 0.)
zp = xp[:]-xp[:]

# move polygon to location
sx = 0.
sy = 0.0017
sz = 0.03

sx = sx+xp/1.e3
sy = sy+yp/1.e3
sz = sz+zp/1.e3

# set camera properties
fov = 60.*np.pi/180.
lens_w = 8.e-3
nw = 300
nh = 300

# set time and velocity variables
dt = 0.002
u = 0.0
v = 0.0
w = -1.8
nt = 10
omega = 4800.
cant_max = 40.

for i in range(nt+1):
    # simulate image
    print i
    ax, ay, pf = fm.get_pixels_poly(sx, sy, sz, fov, fov, lens_w, lens_w, nw, nh)

    # plot
    plt.figure(i)
    plt.pcolormesh(ax*1.e3, ay*1.e3, pf, cmap='Blues')
    ax = plt.gca()

    ax.set_xlim([-lens_w/2.*1.e3, lens_w/2.*1.e3])
    ax.set_ylim([-lens_w/2.*1.e3, lens_w/2.*1.e3])
    ax.set_aspect(1.)

    plt.savefig('circ_{:03d}.png'.format(i))
    plt.close()

    # update position
    sx = dt*(u+(np.random.rand(1)-0.5)/1.)+sx
    sy = dt*(v+(np.random.rand(1)-0.5)/1.)+sy
    sx, sy = rotate(sx, sy, omega*dt)
    sz = dt*(w+(np.random.rand(1)-0.5)/2.)+sz
    #sx, sy, sz = cant(sx, sy, sz, 2.*np.pi/nt*cant_max*np.cos(2.*i*np.pi/nt), 0.)

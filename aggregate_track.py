import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import forward_model as fm
from crystal_dda.geometry import rotate
from crystal_dda.polygons import make_branched_planar

# create shape (in mm)
nump = 25
thpol = np.linspace(0., 2.*np.pi, nump)
rad_mean = 100.
pcvar = 0.2
rad = rad_mean*((np.random.rand(nump)-0.5)*2.*pcvar+1.)
xp = rad*np.cos(thpol)
yp = rad*np.sin(thpol)
zp = xp-xp

# move polygon to location (in m)
sx = 0.
sy = 0.
sz = 5.

sx = sx+xp/1.e3
sy = sy+yp/1.e3
sz = sz+zp/1.e3

# set camera properties
fov = 30.*np.pi/180.
nth = 200
nr = 200

# get grid of pixels
px, py, pxe, pye = fm.get_pixels(nth, nr)
pxf = px.flatten()
pyf = py.flatten()
pf_tot = np.zeros([nth, nr])

# set time and velocity variables
dt = 0.05
u = 0.0
v = 0.0
w = -1.5
nt = 50
omega = 200.
cant_max = 40.

for i in range(nt+1):
    # simulate image
    print i
    pf = fm.get_pixels_poly(sx, sy, sz, pxf, pyf, fov)
    pf.shape = (nth, nr)
    pf_tot = pf_tot+pf

    # plot
    plt.figure(i)
    plt.pcolormesh(pxe, pye, pf, cmap='Blues')
    ax = plt.gca()

    ax.set_xlim([-1., 1.])
    ax.set_ylim([-1., 1.])
    ax.set_aspect(1.)

    plt.savefig('img_{:03d}.png'.format(i), dpi=20)
    plt.close()

    # update position
    sx = dt*(u+(np.random.rand(1)-0.5)*0.2)+sx
    sy = dt*(v+(np.random.rand(1)-0.5)*0.2)+sy
    sx, sy = rotate(sx, sy, (omega+(np.random.rand(1)-0.5)*30.)*dt)
    sz = dt*(w+(np.random.rand(1)-0.5)/2.)+sz
    #sx, sy, sz = cant(sx, sy, sz, 2.*np.pi/nt*cant_max*np.cos(2.*i*np.pi/nt), 0.)

'''
# plot sum of images
plt.figure(i)
plt.pcolormesh(pxe, pye, pf_tot, cmap='Blues')
plt.colorbar()

ax = plt.gca()
ax.set_xlim([-1., 1.])
ax.set_ylim([-1., 1.])
ax.set_aspect(1.)

plt.savefig('img_total.png'.format(i), dpi=120)
'''

import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import forward_model as fm
from crystal_dda.geometry import rotate
from crystal_dda.polygons import make_branched_planar, make_poly3d

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
c = 0.5
amax = 3.
ac = 0.5

fb = 0.5
ft = 0.2
fg = 0.7

nsb = 5

ag = amax*fg

xp2, yp2 = make_branched_planar(amax, ac, ft, fb, fg, nsb, 0.)
xp, yp, zp = make_poly3d(xp2, yp2, 2.*c)
#zp = xp[:]-xp[:]

# move polygon to location
sx = 0.
sy = 0.
sz = 0.02

sx = sx+xp/1.e3
sy = sy+yp/1.e3
sz = sz+zp/1.e3
sx, sy, sz = cant(sx, sy, sz, 50., 0.)

# set camera properties
fov = 30.*np.pi/180.
nth = 200
nr = 200

# get grid of pixels
px, py, pxe, pye = fm.get_pixels(nth, nr)
pxf = px.flatten()
pyf = py.flatten()

# simulate image
pf = fm.get_pixels_poly(sx, sy, sz, pxf, pyf, fov)
pf.shape = (nth, nr)
cxp, cyp = fm.cam_pos_poly(sx, sy, sz, fov)

# plot
plt.pcolormesh(pxe, pye, pf, cmap='Blues')
plt.plot(cxp, cyp, 'r', lw=3.)
ax = plt.gca()

ax.set_xlim([-1., 1.])
ax.set_ylim([-1., 1.])
ax.set_aspect(1.)

plt.savefig('snap.png', dpi=90)

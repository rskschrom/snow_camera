import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import forward_model as fm
from crystal_dda.geometry import rotate
from crystal_dda.crystal_dda import branched_planar_dipoles

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

fb = 0.3
ft = 0.2
fg = 0.7

nsb = 3
nxp = 120
nzp = 12

ag = ac*(1.-fg)+amax*fg

xp, yp, zp = branched_planar_dipoles(a, amax, ac, ft, fb, fg, nsb, nxp, nzp)

# move polygon to location
sx = 0.
sy = 0.
sz = 0.01

sx = sx+xp/1.e3
sy = sy+yp/1.e3
sz = sz+zp/1.e3
sx, sy, sz = cant(sx, sy, sz, 30., 0.)
diplen  = (np.max(xp)-np.min(xp))/(nxp-1)/1.e3
print diplen

# set camera properties
fov = 30.*np.pi/180.
nth = 200
nr = 200

# get grid of pixels
px, py, pxe, pye = fm.get_pixels(nth, nr)
pxf = px.flatten()
pyf = py.flatten()

# get grid of pixels
#px, py, pxe, pye = fm.get_pixels(nth, nr)
#pxf = px.flatten()
#pyf = py.flatten()

# simulate image
pf = fm.cam_pixel_dipoles(sx, sy, sz, pxf, pyf, fov, diplen)
pf.shape = (nth, nr)

# plot
plt.pcolormesh(pxe, pye, pf, cmap='Blues')
#plt.scatter(cx, cy, c='b', s=2., alpha=0.4)
ax = plt.gca()

ax.set_xlim([-1., 1.])
ax.set_ylim([-1., 1.])
ax.set_aspect(1.)

plt.savefig('snap.png', dpi=120)

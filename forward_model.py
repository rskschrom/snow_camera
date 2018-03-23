import numpy as np
from crystal_dda.geometry import in_polygon

# get apparent size of sphere from camera
def app_size_sphere(rad, x, y, z, fovh, lenh):
    dist = np.sqrt(x**2.+y**2.+z**2.)
    app_frac = rad**2./(2.*dist**2.)
    app_rad = app_frac*lenh/(fovh/np.pi)
    return app_rad

# get position of sphere in camera coordinates
def cam_pos_sphere(x, y, z, fovw, fovh, lenw, lenh):
    angw = np.pi/2.-np.arctan2(z, x)
    angh = np.pi/2.-np.arctan2(z, y)
    cx = 0.5*angw/fovw*lenw
    cy = 0.5*angh/fovh*lenh
    return cx, cy

# get polygon in camera coordinates
def cam_pos_poly(xpoly, ypoly, zpoly, fov):
    angw = np.pi/2.-np.arctan2(zpoly, xpoly)
    angh = np.pi/2.-np.arctan2(zpoly, ypoly)
    cx = angw/fov
    cy = angh/fov
    return cx, cy

# get pixel grid
def get_pixels(nth, nr):
    pthed = np.linspace(0., 2.*np.pi, nth+1)
    pred = np.linspace(1./(nr+1), 1., nr+1)
    pthcen = 0.5*(pthed[1:nth+1]+pthed[0:nth])
    prcen = 0.5*(pred[1:nr+1]+pred[0:nr])

    # get centers and edges
    pth, pr = np.meshgrid(pthcen, prcen, indexing='ij')
    pthe, pre = np.meshgrid(pthed, pred, indexing='ij')

    # convert to cartesian
    px = pr*np.cos(pth)
    py = pr*np.sin(pth)
    pxe = pre*np.cos(pthe)
    pye = pre*np.sin(pthe)

    return px, py, pxe, pye

# get pixels in camera polygon
def get_pixels_poly(xpoly, ypoly, zpoly, px, py, fov):
    cxpoly, cypoly = cam_pos_poly(xpoly, ypoly, zpoly, fov)
    pfilf = in_polygon(cxpoly, cypoly, px, py)

    return pfilf

# project locations in cartesian space to camera coordinates
def cam_project(x, y, z, fov):
    angw = np.pi/2.-np.arctan2(z, x)
    angh = np.pi/2.-np.arctan2(z, y)
    cx = 0.5*angw/fov
    cy = 0.5*angh/fov

    return cx, cy

# get position of dipoles in camera coordinates
def cam_pixel_dipoles(x, y, z, px, py, fov, diplen):
    # assume dipoles are approximately spherical
    numdip = len(x)
    numpix = len(px)
    pfil_tot = np.zeros([numpix])

    # get pixel projections for each dipole
    print numdip
    #thet = np.linspace(0., 2.*np.pi, 7)
    xpert = np.array([1., -1., -1., 1.])
    ypert = np.array([1., 1., -1., -1.])
    xc = diplen/2.*xpert
    yc = diplen/2.*ypert

    for i in range(numdip):
        pfil_tot = pfil_tot+get_pixels_poly(xc+x[i], yc+y[i], xc/xc*z[i], px, py, fov)

    pfil_tot[pfil_tot>0] = 1

    return pfil_tot

# get position of dipole in camera coordinates
def cam_pixel_dipole(xd, yd, zd, fovw, fovh, lenw, lenh, nw, nh, diplen):
    # create dipole point appx
    xp = np.array([xd+diplen/2., xd-diplen/2., xd-diplen/2., xd+diplen/2.])
    yp = np.array([yd+diplen/2., yd+diplen/2., yd-diplen/2., yd-diplen/2.])

    angw = np.pi/2.-np.arctan2(zd, xp)
    angh = np.pi/2.-np.arctan2(zd, yp)
    cx = 0.5*angw/fovw*lenw
    cy = 0.5*angh/fovh*lenh

    # get grid of 
    px1d = np.linspace(-lenw/2., lenw/2., nw+1)
    py1d = np.linspace(-lenh/2., lenh/2., nh+1)

    for i in range(nw):
        for j in range(nh):
            cond = [(cx>px1d[i])&(cx<=px1d[i+1])&(cy>py1d[j])&(cy<=py1d[j+1])]
            cx_sub = cx[cond]
            pfilled[i,j] = min(1, len(cx_sub))

    return px, py, pfilled
    

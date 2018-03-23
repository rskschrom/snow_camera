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
def cam_pos_poly(xpoly, ypoly, zpoly, fovw, fovh, lenw, lenh):
    angw = np.pi/2.-np.arctan2(zpoly, xpoly)
    angh = np.pi/2.-np.arctan2(zpoly, ypoly)
    cx = 0.5*angw/fovw*lenw
    cy = 0.5*angh/fovh*lenh
    return cx, cy

# get pixels in camera polygon
def get_pixels_poly(xpoly, ypoly, zpoly, fovw, fovh, lenw, lenh, nw, nh):
    cxpoly, cypoly = cam_pos_poly(xpoly, ypoly, zpoly, fovw, fovh, lenw, lenh)

    # get camera pixel grids
    pxed = np.linspace(-lenw/2., lenw/2., nw+1)
    pyed = np.linspace(-lenh/2., lenh/2., nh+1)
    pxcen = 0.5*(pxed[1:nw+1]+pxed[0:nw])
    pycen = 0.5*(pyed[1:nh+1]+pyed[0:nh])
    px, py = np.meshgrid(pxcen, pycen, indexing='ij')
    pxf = px.flatten()
    pyf = py.flatten()

    # get pixels with part of polygon in them
    pfilf = in_polygon(cxpoly, cypoly, pxf, pyf)
    pfilf.shape = (nw, nh)
    pxe, pye = np.meshgrid(pxed, pyed, indexing='ij')

    return pxe, pye, pfilf

# get position of dipoles in camera coordinates
def cam_pixel_dipoles(x, y, z, fovw, fovh, lenw, lenh, nw, nh):
    angw = np.pi/2.-np.arctan2(z, x)
    angh = np.pi/2.-np.arctan2(z, y)
    cx = 0.5*angw/fovw*lenw
    cy = 0.5*angh/fovh*lenh

    # get dipoles in each pixel
    px1d = np.linspace(-lenw/2., lenw/2., nw+1)
    py1d = np.linspace(-lenh/2., lenh/2., nh+1)
    px, py = np.meshgrid(px1d, py1d, indexing='ij')
    pfilled = np.empty([nw, nh])

    for i in range(nw):
        for j in range(nh):
            cond = [(cx>px1d[i])&(cx<=px1d[i+1])&(cy>py1d[j])&(cy<=py1d[j+1])]
            cx_sub = cx[cond]
            pfilled[i,j] = min(1, len(cx_sub))

    return px, py, pfilled

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
    

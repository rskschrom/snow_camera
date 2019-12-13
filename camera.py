import numpy as np
from ray import Rays

# camera class
class Camera():
    '''Camera class to render simple shapes defined in scene.

    Attributes:
        camera_z -- z position of camera (relative to eye position, x-y position of camera same as eye)
        eye_pos -- position of viewer's eye
        light_pos -- position of light source
        pixel_dims -- tuple (number of pixels in x, number of pixels in y)
        pixel_len -- physical width of each pixel (constant)
        scene -- objects to be rendered
    '''
    def __init__(self, camera_z, eye_pos, light_pos, pixel_dims=(800,600), pixel_len=0.02, scene=None):
        self.camera_z = camera_z
        self.eye_pos = eye_pos
        self.light_pos = light_pos
        self.pixel_dims = pixel_dims
        self.pixel_len = pixel_len
        self.scene = scene
        self.rays = None

    # calculate positions camera pixel centers
    def get_pixel_grid(self):
        # make sure pixel dimensions are odd
        nxpix = 2*int(self.pixel_dims[0]/2)+1
        nypix = 2*int(self.pixel_dims[1]/2)+1

        # x and y positions 
        px1d = (np.arange(nxpix)-(nxpix-1)/2.)*self.pixel_len
        py1d = (np.arange(nypix)-(nypix-1)/2.)*self.pixel_len
        px, py = np.meshgrid(px1d, py1d, indexing='ij')

        # z position (constant) of same dimension
        pz = px[:]-px[:]+self.camera_z
        return px, py, pz

    # set scene for camera
    def set_scene(self, scene):
        self.scene = scene
        return

    # get scene for camera
    def get_scene(self):
        return self.scene

    # get rays
    def get_rays(self):
        return self.rays

    # create rays for camera
    def create_rays(self):
        px, py, pz = self.get_pixel_grid()
        pxf = px.flatten()
        pyf = py.flatten()
        pzf = pz.flatten()
        nray = len(pxf)

        # calculate directions from eye to pixel
        eye_pos = self.eye_pos
        dirx = pxf-eye_pos[0]
        diry = pyf-eye_pos[1]
        dirz = pzf-eye_pos[2]
        dir_vec = np.vstack((dirx,diry,dirz))

        # initialize rays object
        pos_vec = np.vstack((pxf,pyf,pzf))
        rays = Rays(pos_vec, dir_vec)
        self.rays = rays
        return

    # render scene (for 1 shape right now)
    def render(self):
        # make sure rays have been created
        if self.rays==None:
            self.create_rays()
        rays = self.rays
        nray = rays.get_nray()

        # calculate shading (0-dark,1-light)
        sfc_pnt, nvec, dist = self.scene.get_surface_overlap(rays)
        lgt_pos = self.light_pos[...,np.newaxis]
        lvec = sfc_pnt-lgt_pos
        ldist = np.sqrt(np.sum(lvec**2., axis=0))
        ldir = lvec/ldist[np.newaxis,...]

        shade = np.einsum("ij,ij->j", -nvec, ldir)
        #shade[dist==1.e9] = 1.
        shade = shade/(ldist/np.max(ldist))**2.
        shade = (shade-np.min(shade))/(np.max(shade)-np.min(shade))
        print(np.min(shade), np.max(shade))
        shade[dist==1.e9] = 0.

        # reshape
        nxpix = 2*int(self.pixel_dims[0]/2)+1
        nypix = 2*int(self.pixel_dims[1]/2)+1
        shade.shape = (nxpix,nypix)
        return shade

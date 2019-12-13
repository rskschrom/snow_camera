import numpy as np

# class for analytical shapes for scene
class Shape():
    def __init__(self, position):
        self.position = position

    def set_position(self, position):
        self.position = position
        return

# spheres
class Sphere(Shape):
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius

    def set_radius(self, radius):
        self.radius = radius
        return

    # get intersection point(s) of ray with sphere
    def get_surface_intersection(self, rays):
        ray_pnts = rays.get_points()
        ray_dirs = rays.get_directions()
        nray = ray_pnts.shape[1]
        sph_pnt = self.position[...,np.newaxis]
        sph_rad = self.radius

        # determine type of solution
        dot_prod = np.einsum("ij,ij->j", ray_dirs, (ray_pnts-sph_pnt))
        deter = dot_prod**2.-(np.sum((ray_pnts-sph_pnt)**2., axis=0)-sph_rad**2.)
        num_intersect = np.zeros([nray], dtype=int)
        num_intersect[deter==0.] = 1
        num_intersect[deter>0.] = 2

        # calculate distances to surface
        sfc_dist = np.empty([nray])
        sfc_dist[:] = 1.e9

        # find minimum surface distance in case of two intersections
        deter_double_inter = deter[num_intersect==2]
        sfc_dist1 = -dot_prod[num_intersect==2]+np.sqrt(deter_double_inter)
        sfc_dist2 = -dot_prod[num_intersect==2]-np.sqrt(deter_double_inter)
        sfc_dist_min = np.minimum(sfc_dist1, sfc_dist2)
        sfc_dist[num_intersect==2] = sfc_dist_min

        # surface points
        sfc_x = np.empty([nray])
        sfc_y = np.empty([nray])
        sfc_z = np.empty([nray])
        sfc_x[:] = 1.e9
        sfc_y[:] = 1.e9
        sfc_z[:] = 1.e9
        sfc_x[num_intersect==2] = ray_pnts[0,num_intersect==2]+sfc_dist_min*ray_dirs[0,num_intersect==2]
        sfc_y[num_intersect==2] = ray_pnts[1,num_intersect==2]+sfc_dist_min*ray_dirs[1,num_intersect==2]
        sfc_z[num_intersect==2] = ray_pnts[2,num_intersect==2]+sfc_dist_min*ray_dirs[2,num_intersect==2]
        sfc_pnt = np.vstack((sfc_x,sfc_y,sfc_z))

        # surface normal vectors
        nvec = np.zeros([3,nray])
        nvec[:,num_intersect==2] = (sfc_pnt[:,num_intersect==2]-sph_pnt)/sph_rad
        return sfc_pnt, nvec, sfc_dist

import numpy as np

# class defining scene (list of objects) for camera
class Scene():
    def __init__(self, objects):
        self.objects = objects

    def get_objects(self):
        return self.objects

    # get intersection points of overlapping objects by minimum distance
    def get_surface_overlap(self, rays):
        # get intersection info for first object
        objects = self.objects
        sfc_pnt, nvec, sfc_dist = objects[0].get_surface_intersection(rays)

        # loop over intersection points for each object and replace with closer ones
        for obj in objects:
            sfc_pnt_test, nvec_test, sfc_dist_test = obj.get_surface_intersection(rays)
            closer_inds = ((sfc_dist_test-sfc_dist)<0.)

            sfc_pnt[:,closer_inds] = sfc_pnt_test[:,closer_inds]
            nvec[:,closer_inds] = nvec_test[:,closer_inds]
            sfc_dist[closer_inds] = sfc_dist_test[closer_inds]

        return sfc_pnt, nvec, sfc_dist

import numpy as np
from camera import Camera
from shape import Sphere
from scene import Scene
import matplotlib.pyplot as plt

# create camera object
nx = 800
ny = int(nx/4*3)
cam = Camera(0., np.array([0.,0.,-500.]), np.array([0.,0.,-500.]),
             pixel_dims=(nx,ny),pixel_len=0.5)
cam.create_rays()
rays = cam.get_rays()

# create a bunch of spheres and add to scene
nsphere = 100
rad = 10.
xrnd = 400.*(np.random.rand(nsphere)-0.5)
yrnd = 400.*(np.random.rand(nsphere)-0.5)
zrnd = 500.*np.random.rand(nsphere)+50.
spheres = []

for i in range(nsphere):
    spheres.append(Sphere(np.array([xrnd[i],yrnd[i],zrnd[i]]), 10.))
scene = Scene(spheres)

# render scene and plot
cam.set_scene(scene)
shade = cam.render()
px, py,_ = cam.get_pixel_grid()

plt.imshow(shade[:,::-1].T, cmap='Greys_r')
plt.savefig('shade_test.png', dpi=375./(2400./nx))

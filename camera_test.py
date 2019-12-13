import numpy as np
from camera import Camera
from shape import Sphere
from scene import Scene
import matplotlib.pyplot as plt

# create camera object
nx = 800
ny = int(nx/4*3)
cam = Camera(0., np.array([0.,0.,-500.]), np.array([20.,25.,-30.]),
             pixel_dims=(nx,ny),pixel_len=0.5)
cam.create_rays()
rays = cam.get_rays()

# create sphere and add to scene
sphere1 = Sphere(np.array([0.,0.,100.]), 10.)
sphere2 = Sphere(np.array([-200.,0.,200.]), 10.)
scene = Scene([sphere1,sphere2])

# render scene and plot
cam.set_scene(scene)
shade = cam.render()
px, py,_ = cam.get_pixel_grid()

plt.imshow(shade[:,::-1].T, cmap='Greys')
plt.savefig('shade_test.png', dpi=375./(2400./nx))

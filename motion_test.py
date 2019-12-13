import numpy as np
from camera import Camera
from shape import Sphere
from scene import Scene
import matplotlib.pyplot as plt

# create camera object
nx = 800
ny = int(nx/4*3)
cam = Camera(0., np.array([0.,0.,-300.]), np.array([0.,0.,-500.]),
             pixel_dims=(nx,ny),pixel_len=0.4)
cam.create_rays()
rays = cam.get_rays()

# create a bunch of spheres and add to scene
nsphere = 300
rad = 10.
xrnd = 1200.*(np.random.rand(nsphere)-0.5)
yrnd = 1200.*(np.random.rand(nsphere)-0.5)
zrnd = 1000.*np.random.rand(nsphere)+50.
spheres = []

for i in range(nsphere):
    spheres.append(Sphere(np.array([xrnd[i],yrnd[i],zrnd[i]]), 10.))
scene = Scene(spheres)

# render initial scene
px, py,_ = cam.get_pixel_grid()
cam.set_scene(scene)
shade = cam.render()
plt.imshow(shade[:,::-1].T, cmap='Greys_r')
plt.savefig(f'shade_motion_000.png', dpi=375./(2400./nx))
plt.close()

# render images in time as particles move
ntime = 50
dt = 0.004
mot_vec = np.zeros([3,nsphere])
mot_vec[1,:] = -1.2e3
mot_vec[0,:] = -0.3e3
for i in range(ntime-1):
    print(i)
    scene = cam.get_scene()
    mot_vec[0,:] = mot_vec[0,:]+0.3*(np.random.rand(nsphere)-0.5)
    scene.motion(mot_vec, dt)
    cam.set_scene(scene)
    shade = cam.render()
    plt.imshow(shade[:,::-1].T, cmap='Greys_r')
    plt.savefig(f'shade_motion_{i+1:03d}.png', dpi=375./(2400./nx))
    plt.close()

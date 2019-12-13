import numpy as np
from camera import Camera
from shape import Sphere
from scene import Scene
import matplotlib.pyplot as plt
from netCDF4 import Dataset

# set dataset parameters
dat_type = 'test'
outdir = f'/vhtraid2/rschrom/snow_cam/{dat_type}_data/'

# create camera object
nx = 200
ny = int(nx/4*3)
cam = Camera(0., np.array([0.,0.,-300.]), np.array([0.,0.,-500.]),
             pixel_dims=(nx,ny),pixel_len=0.8)
cam.create_rays()
rays = cam.get_rays()
px, py,_ = cam.get_pixel_grid()
nx_dim, ny_dim = px.shape

# randomly samply number of particles and their radii
nsamp = 200
nsphere = np.random.randint(250, size=nsamp)+50
rad = 5.+25.*np.random.rand(nsamp)
shade = np.empty([nsamp,nx_dim,ny_dim])

# loop over samples and generate images
for j in range(nsamp):
    print(j, nsphere[j])
    xrnd = 1200.*(np.random.rand(nsphere[j])-0.5)
    yrnd = 1200.*(np.random.rand(nsphere[j])-0.5)
    zrnd = 1000.*np.random.rand(nsphere[j])+50.
    spheres = []

    for i in range(nsphere[j]):
        spheres.append(Sphere(np.array([xrnd[i],yrnd[i],zrnd[i]]), rad[j]))
    scene = Scene(spheres)

    # render scene
    cam.set_scene(scene)
    shade[j,:,:] = cam.render()

# write data to netcdf file
dataset = Dataset(f'{outdir}data.nc', 'w')
pxl_x = dataset.createDimension('px', nx_dim)
pxl_y = dataset.createDimension('py', ny_dim)
samp_ind = dataset.createDimension('sample_index', nsamp)

im_data = dataset.createVariable('im_data', 'f4', ('sample_index','px','py'))
rad_data = dataset.createVariable('radius', 'f4', 'sample_index')
ncon_data = dataset.createVariable('number_concentration', 'f4', 'sample_index')

rad_data.units = 'mm'
ncon_data.units = 'm^-3'

im_data[:] = shade
rad_data[:] = rad
ncon_data[:] = nsphere/(1.2*1.2*1.)

dataset.close()

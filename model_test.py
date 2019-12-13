import matplotlib.pyplot as plt
from keras.models import load_model
import numpy as np
from netCDF4 import Dataset

# open test data
data_dir = '/vhtraid2/rschrom/snow_cam/'
tncf = Dataset(f'{data_dir}test_data/data.nc', 'r')
im_test = tncf.variables['im_data'][:]
rad_test = tncf.variables['radius'][:]
ncon_test = tncf.variables['number_concentration'][:]
dims_test = im_test.shape

# normalize data
radmin = 5.
radmax = 30.
ncmin = 50.
ncmax = 300.
rad_test = (rad_test-radmin)/(radmax-radmin)
ncon_test = (ncon_test*1.2*1.2-ncmin)/(ncmax-ncmin)

# reshape data
ntest = dims_test[0]
nx = dims_test[1]
ny = dims_test[2]

# set input and output data
output_test = np.empty([ntest,2])
output_test[:,0] = rad_test
output_test[:,1] = ncon_test

input_test = np.empty([ntest,nx,ny,1])
input_test[:,:,:,0] = im_test

# predict and plot
model = load_model('snow_camera_model.h5')
output_predict = model.predict(input_test)

rad_predict = output_predict[:,0]
ncon_predict = output_predict[:,1]
rad_predict = rad_predict*(radmax-radmin)+radmin
ncon_predict = ncon_predict*(ncmax-ncmin)+ncmin

rad_test = rad_test*(radmax-radmin)+radmin
ncon_test = ncon_test*(ncmax-ncmin)+ncmin

fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(1,2,1)
plt.scatter(rad_test, rad_predict, c='k', s=2.)
plt.plot([radmin,radmax], [radmin,radmax], 'k--')
ax.set_xlim([radmin,radmax])
ax.set_ylim([radmin,radmax])
ax.set_aspect(1.)
ax.set_xlabel('radius (mm) - test data')
ax.set_ylabel('radius (mm) - prediction')

ax = fig.add_subplot(1,2,2)
plt.scatter(ncon_test/1.2**2., ncon_predict/1.2**2., c='k', s=2.)
plt.plot([ncmin/1.2**2.,ncmax/1.2**2.], [ncmin/1.2**2.,ncmax/1.2**2.], 'k--')
ax.set_xlim([ncmin/1.2**2.,ncmax/1.2**2.])
ax.set_ylim([ncmin/1.2**2.,ncmax/1.2**2.])
ax.set_aspect(1.)
ax.set_xlabel('number concentration (# m$^{-3}$) - test data')
ax.set_ylabel('number concentration (# m$^{-3}$) - prediction')

plt.suptitle('Snow Camera Retrieval - CNN->Dense Neural Network')
plt.savefig('model_test.png')

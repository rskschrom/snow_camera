from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D, Flatten
from keras.models import Model
from keras import backend as K
from keras.callbacks import Callback, TensorBoard, LambdaCallback
from keras.optimizers import Adam
import tensorflow as tf
import numpy as np
from netCDF4 import Dataset

class Clear(Callback):
    def on_epoch_end(self, epoch, logs):
        K.clear_session()

# open phidp/kdp paired data and prepare for model
print('opening training data...')
data_dir = '/vhtraid2/rschrom/snow_cam/'
tncf = Dataset(f'{data_dir}train_data/data.nc', 'r')
im_train = tncf.variables['im_data'][:]
rad_train = tncf.variables['radius'][:]
ncon_train = tncf.variables['number_concentration'][:]
dims_train = im_train.shape

vncf = Dataset(f'{data_dir}valid_data/data.nc', 'r')
im_valid = vncf.variables['im_data'][:]
rad_valid = vncf.variables['radius'][:]
ncon_valid = vncf.variables['number_concentration'][:]
dims_valid = im_valid.shape

# normalize data
print('normalizing data...')
rad_train = (rad_train-5.)/(30.-5.)
ncon_train = (ncon_train*1.2*1.2-50)/(300-50.)
rad_valid = (rad_valid-5.)/(30.-5.)
ncon_valid = (ncon_valid*1.2*1.2-50)/(300-50.)

# reshape data
ntrain = dims_train[0]
nx = dims_train[1]
ny = dims_train[2]
nvalid = dims_valid[0]

# set input and output data
output_train = np.empty([ntrain,2])
output_train[:,0] = rad_train
output_train[:,1] = ncon_train
output_valid = np.empty([nvalid,2])
output_valid[:,0] = rad_valid
output_valid[:,1] = ncon_valid

input_train = np.empty([ntrain,nx,ny,1])
input_train[:,:,:,0] = im_train
input_valid = np.empty([nvalid,nx,ny,1])
input_valid[:,:,:,0] = im_valid

# neural network parameters
nfilt = 6
filt_size = (3,3)
pool_fac = 4

# set up cnn->dense network
tf.config.threading.set_intra_op_parallelism_threads(1)
tf.config.threading.set_inter_op_parallelism_threads(1)
cs = Clear()

with tf.device('/CPU:0'):
    input_data = Input(shape=(nx,ny,1))

    # cnn part
    x = Conv2D(nfilt, filt_size, activation='relu', padding='same')(input_data)
    x = MaxPooling2D(pool_fac, padding='same')(x)
    x = Conv2D(nfilt, filt_size, activation='relu', padding='same')(x)
    x = MaxPooling2D(pool_fac, padding='same')(x)
    x = Conv2D(nfilt, filt_size, activation='relu', padding='same')(x)
    x = MaxPooling2D(pool_fac, padding='same')(x)
    cnn_out =  Conv2D(nfilt, filt_size, activation='relu', padding='same')(x)

    # fully connected part
    x = Flatten()(cnn_out)
    x = Dense(5, activation='relu')(x)
    dense_out = Dense(2, activation='relu')(x)

    # assemble model
    model = Model(input_data, dense_out)
    opt = Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, amsgrad=False)
    model.compile(optimizer=opt, loss='mean_squared_error')
    model.summary()

    
    # fit data with model
    model.fit(input_train, output_train,
              epochs=50,
              batch_size=5,
              shuffle=True,
              validation_data=(input_valid, output_valid),
              #callbacks=[TensorBoard(log_dir='/tmp/tb', histogram_freq=0, write_graph=False)],
              callbacks=[cs],
              workers=24,
              use_multiprocessing=True)
    
    
model.save('snow_camera_model.h5')

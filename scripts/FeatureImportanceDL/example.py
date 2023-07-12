import numpy as np
import os
import tensorflow.keras as keras
from tensorflow.keras import backend as K
from src.FeatureSelector import FeatureSelector
from DataGenerator import generate_data, get_one_hot

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

####################
# Code added for my task - Pranjal
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def create_dataset(dataset, look_back=3, time_step=3):
  dataX, dataY = [], []
  for i in range(len(dataset)- look_back - time_step - 1):
    a = np.array(dataset[i:(i + look_back), : 33])
    # dataX.append(np.array(dataset[i:(i + look_back), : 33]))
    dataX.append(a.flatten())
    dataY.append(dataset[i + look_back + time_step, 33:])
	
  return np.array(dataX), np.array(dataY)


# Read data
df = pd.read_csv("data.csv", index_col = 0)

columns = [x + "_0" for x in df.columns.values] + [x + "_1" for x in df.columns.values] + [x + "_2" for x in df.columns.values]

df = df.dropna()
df["memusedcat"] = pd.cut(df["%memused"], bins = [0, 85, 100], labels=[0, 1])

one_hot = pd.get_dummies(df["memusedcat"])
df = df.drop("memusedcat", axis = 1)
df = df.join(one_hot)

columns_req_norm = df.columns[:33]
scaler = MinMaxScaler()
df[columns_req_norm] = scaler.fit_transform(df[columns_req_norm])

values = df.values
dataX, dataY = create_dataset(values, 3, 3)

min = dataX.shape[0]

indices_with_class_list = []

for i in range(2):
  indices_with_class = np.where(dataY[:, i] == 1)[0]
  indices_with_class_list.append(indices_with_class)

  if len(indices_with_class) < min:
    min = len(indices_with_class)

to_be_removed = []

for i in range(2):
  count_to_be_removed = len(indices_with_class_list[i]) - min

  to_be_removed.extend(np.random.choice(indices_with_class_list[i], size = count_to_be_removed, replace=False))

dataX = np.delete(dataX, to_be_removed, axis = 0)
dataY = np.delete(dataY, to_be_removed, axis = 0)

from sklearn.utils import shuffle
dataX, dataY = shuffle(dataX, dataY, random_state = 0)

train_data_ratio = 0.80
val_data_ratio = 0.05
train_data_size = int(dataX.shape[0] * train_data_ratio)
val_data_size = int(dataX.shape[0] * val_data_ratio)

X_tr = dataX[:train_data_size]
y_tr = dataY[:train_data_size]

X_val = dataX[train_data_size:train_data_size + val_data_size]
y_val = dataY[train_data_size:train_data_size + val_data_size]

X_te = dataX[train_data_size + val_data_size:]
y_te = dataY[train_data_size + val_data_size:]

N_TRAIN_SAMPLES = train_data_size
N_VAL_SAMPLES = val_data_size
N_TEST_SAMPLES = dataX.shape[0] - (train_data_size + val_data_size)
N_FEATURES = 99
FEATURE_SHAPE = (99,)
dataset_label = "MEM_"

####################

# Dataset parameters
# N_TRAIN_SAMPLES = 512
# N_VAL_SAMPLES = 256
# N_TEST_SAMPLES = 1024
# N_FEATURES = 10
# FEATURE_SHAPE = (10,)
# dataset_label = "XOR_"

# Training parameters
data_batch_size = 16
mask_batch_size = 16
# final batch_size is data_batch_size x mask_batch_size
s = 48  # size of optimal subset that we are looking for
s_p = 4  # number of flipped bits in a mask when looking around m_opt
phase_2_start = 10000  # after how many batches phase 2 will begin
max_batches = 30000  # how many batches if the early stopping condition not satisfied
early_stopping_patience = 1000  # how many patience batches (after phase 2 starts)
# before the training stops

# Generate data for XOR dataset:
# First three features are used to create the target (y)
# All the following features are gaussian noise
# In total 10 features
######################
# X_tr, y_tr = generate_data(n=N_TRAIN_SAMPLES, seed=0)
# X_val, y_val = generate_data(n=N_VAL_SAMPLES, seed=0)
# X_te, y_te = generate_data(n=N_TEST_SAMPLES, seed=0)

# Get one hot encoding of the labels
# y_tr = get_one_hot(y_tr.astype(np.int8), 4)
# y_te = get_one_hot(y_te.astype(np.int8), 4)
# y_val = get_one_hot(y_val.astype(np.int8), 4)
######################

# Create the framework, needs number of features and batch_sizes, str_id for tensorboard
fs = FeatureSelector(FEATURE_SHAPE, s, data_batch_size, mask_batch_size, str_id=dataset_label)

# Create a dense operator net, uses the architecture:
# N_FEATURES x 2 -> 60 -> 30 -> 20 -> 4
# with sigmoid activation in the final layer.
fs.create_dense_operator([512, 256, 128, 32, 2], "softmax", metrics=[keras.metrics.CategoricalAccuracy()],
                       error_func=K.categorical_crossentropy)
# Ealy stopping activate after the phase2 of the training starts.
fs.operator.set_early_stopping_params(phase_2_start, patience_batches=early_stopping_patience, minimize=True)

# Create a dense selector net, uses the architecture:
# N_FEATURES -> 60 -> 30 -> 20 -> 4
fs.create_dense_selector([200, 100, 50, 10, 1])

# Set when the phase2 starts, what is the number of flipped bits when perturbin masks
fs.create_mask_optimizer(epoch_condition=phase_2_start, perturbation_size=s_p)

#Train networks and set the maximum number of iterations
fs.train_networks_on_data(X_tr, y_tr, max_batches, val_data=(X_val, y_val))

#Results
importances, optimal_mask = fs.get_importances(return_chosen_features=True)
optimal_subset = np.nonzero(optimal_mask)
test_performance = fs.operator.test_one(X_te, optimal_mask[None,:], y_te)
print("Importances: ", importances)
print("Optimal_subset: ", optimal_subset)
print("Test performance (CE): ", test_performance[0])
print("Test performance (ACC): ", test_performance[1])
print([columns[i] for i in optimal_subset[0].tolist()])
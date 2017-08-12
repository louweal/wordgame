import numpy as np
import pandas as pd
import tensorflow as tf
from keras.models import Model
from keras.layers import Dense, Conv2D, MaxPooling2D, Input, Flatten, Dropout, LSTM
from keras.layers.merge import Concatenate, Dot
from keras.callbacks import ModelCheckpoint
from gensim.models.keyedvectors import KeyedVectors
 
df = pd.read_csv('../../data/processed/wordgame_train.csv')
df['word'] = df['word'].astype(str)
df['association'] = df['association'].astype(str)

w2v_model = KeyedVectors.load_word2vec_format('../../data/external/GoogleNews-vectors-negative300.bin', binary=True)
print('Loaded word embeddings')

X1_train = df['word'].apply(lambda x: w2v_model.word_vec(x)).tolist() 
X2_train = df['association'].apply(lambda x: w2v_model.word_vec(x)).tolist() 
y_train = df['asd']

#reshape data for some reason..
X1_train = np.reshape(X1_train, newshape=(len(X1_train), 1, 300, 1))
X2_train = np.reshape(X2_train, newshape=(len(X2_train), 1, 300, 1))
y_train  = np.reshape(y_train,  newshape=(len(y_train),  1))

#w2v_model = None #memory!

#The Keras Network
print("Building neural network...")
# Shared CNN "legs"
sentence_input = Input(name='sentence_input', shape=(1,300,1)) # (height, width, depth)
convolution = Conv2D(name='convolution', filters=100, kernel_size=(1,300),padding='valid',strides=(1, 1))(sentence_input)
pooled_output  = MaxPooling2D(name='pooled_output', pool_size=(1, 1))(convolution)
pooled_output  = Flatten(name='pooled_output_flat')(pooled_output)
pooled_output  = Dropout(name='some_dropout', rate=0.25)(pooled_output)
#shared_cnn     = Model(name='shared_cnn', inputs=sentence_input, outputs=pooled_output)

#LSTM
sentence_input = Input(name='sentence_input', shape=(1,300)) # (timestep,input_dim)
lstm = LSTM(name='LSTM', units=225, activation='tanh', recurrent_activation='hard_sigmoid', dropout=0.15, recurrent_dropout=0.15)(sentence_input)
shared_cnn = Model(name='shared_lstm', inputs=sentence_input, outputs=lstm) #actually lstm ofcourse


print("shared_cnn summary:")
print(shared_cnn.summary())
print("\n")

input_1 = shared_cnn(Input(shape=(1,300,1), name='word1_input')) # (height, width, depth)
input_2 = shared_cnn(Input(shape=(1,300,1), name='word2_input'))

shared_cnn1 = shared_cnn(input_1)
shared_cnn2 = shared_cnn(input_2)

# Cosine similarity between q1 and q2 feature vectors
cos_sim = Dot(name='cosine_similarity', axes=1, normalize=True)([shared_cnn1, shared_cnn2])

# Merge (cos_sim in the middle) and add MPL
concat_layer = Concatenate(name='concat_layer')([shared_cnn1, cos_sim, shared_cnn2])
hidden_layer = Dense(name='hidden_layer', units=201, activation='relu')(concat_layer)
output_layer = Dense(name='output_layer', units=1, activation='sigmoid')(hidden_layer)

model = Model(inputs=[input_1, input_2], outputs=output_layer)
model.compile(loss= tf.losses.log_loss, optimizer='adadelta', metrics=['accuracy'])
print("Complete model summary:")
print(model.summary())
print("\n")

print("Training model...")
# Saving best versions of network

checkpoint = ModelCheckpoint('lstm.hdf5', monitor='val_loss', verbose=0, save_best_only=True, mode='min')
callbacks_list = [checkpoint]
#ifif
model.fit(x=[X1_train, X2_train], y=y_train, batch_size=50, epochs=10, validation_split=0.1, callbacks=[checkpoint])

# Load best found weights
print("Loading best found model...")
model.load_weights('lstm.hdf5')
# Just some validation that everything works
(loss, accuracy) = model.evaluate(x=[X1_train, X2_train], y=y_train, verbose=1)
print(" - loss: {} - acc: {}".format(loss, accuracy))

###

dft = pd.read_csv('../../data/processed/wordgame_test.csv')
dft['word'] = dft['word'].astype(str)
dft['association'] = dft['association'].astype(str)

X1_test = dft['word'].apply(lambda x: w2v_model.word_vec(x)).tolist() 
X2_test = dft['association'].apply(lambda x: w2v_model.word_vec(x)).tolist() 
y_test = dft['asd']

#reshape data for some reason..
X1_test = np.reshape(X1_test, newshape=(len(X1_test), 1, 300, 1)) #combine
X2_test = np.reshape(X2_test, newshape=(len(X2_test), 1, 300, 1))
y_test  = np.reshape(y_test,  newshape=(len(y_test),  1))

predictions = model.predict(x=[X1_test, X2_test])
dft['pred'] = predictions.flatten()
	
dft.to_csv("../../data/processed/wordgame_test_lstm.csv", sep=',', index=False)




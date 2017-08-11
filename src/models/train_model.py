import numpy as np
import pandas as pd
import tensorflow as tf
from keras.models import Model
from keras.layers import Dense, Conv2D, MaxPooling2D, Input, Flatten, Dropout
from keras.layers.merge import Concatenate, Dot
from keras.callbacks import ModelCheckpoint

 
df = pd.read_csv('../../data/processed/wordgame_20170807.csv')
df['word'] = df['word'].astype(str)
df['association'] = df['association'].astype(str)

df['asd'] = df['forumID'].apply(lambda x:(x%9==0))

df['word_count1'] = df['word'].apply(lambda x:(x.replace('  ',' ').count(' ')+1))
df = df[df['word_count1']==1]
df['word_count2'] = df['association'].apply(lambda x:(x.replace('  ',' ').count(' ')+1))
df = df[df['word_count2']==1]
len(df)

#X1_train = np.zeros(shape=(len(df), 1, 300), dtype=np.float16)
#X2_train = np.zeros(shape=(len(df), 1, 300), dtype=np.float16)
#y_train = np.zeros(shape=(len(df)), dtype=np.int8)

from gensim.models.keyedvectors import KeyedVectors
w2v_model = KeyedVectors.load_word2vec_format('../../data/external/GoogleNews-vectors-negative300.bin', binary=True)
print('Loaded word embeddings')

df['inw2v'] = df.apply(lambda r:((r.word in w2v_model.vocab) & (r.association in w2v_model.vocab)), axis=1)
print("Mean: "+str(df.inw2v.mean()))

#compute similarity
#df['sim'] = 0
#df.ix[df.inw2v, 'sim'] = df.ix[df.inw2v].apply(lambda r:w2v_model.similarity(r.word, r.association), axis=1)

# create word vectors
df['wv1'] = df['word'].apply(lambda x: np.zeros(300)) 
df['wv2'] = df['word'].apply(lambda x: np.zeros(300)) 

df.ix[df.inw2v, 'wv1'] = df.ix[df.inw2v, 'word'].apply(lambda x: w2v_model.word_vec(x)) 
df.ix[df.inw2v, 'wv2'] = df.ix[df.inw2v, 'association'].apply(lambda x: w2v_model.word_vec(x)) 

# pandas yes? 
X1_train = df['wv1'].tolist()
X2_train = df['wv2'].tolist()
y_train = df['asd']

w2v_model = None #memory!

#reshape data for some reason..
X1_train = np.reshape(X1_train, newshape=(len(X1_train), 1, 300, 1))
X2_train = np.reshape(X2_train, newshape=(len(X2_train), 1, 300, 1))
y_train  = np.reshape(y_train,  newshape=(len(y_train),  1))


#The Keras Network
print("Building neural network...")
# Shared CNN "legs"
sentence_input = Input(name='sentence_input', shape=(1,300,1)) # (height, width, depth)
convolution = Conv2D(name='convolution', filters=100, kernel_size=(1,300),padding='valid',strides=(1, 1))(sentence_input)
pooled_output  = MaxPooling2D(name='pooled_output', pool_size=(1, 1))(convolution)
pooled_output  = Flatten(name='pooled_output_flat')(pooled_output)
pooled_output  = Dropout(name='some_dropout', rate=0.25)(pooled_output)
shared_cnn     = Model(name='shared_cnn', inputs=sentence_input, outputs=pooled_output)

print("shared_cnn summary:")
print(shared_cnn.summary())
print("\n")

input_1 = Input(shape=(1,300,1), name='word1_input') # (height, width, depth)
input_2 = Input(shape=(1,300,1), name='word2_input')

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

checkpoint = ModelCheckpoint('cnn_best_weights2.hdf5', monitor='val_loss', verbose=0, save_best_only=True, mode='min')
#callbacks_list = [checkpoint]
model.fit(x=[X1_train, X2_train], y=y_train, batch_size=50, epochs=10, validation_split=0.1, callbacks=[checkpoint])
          # also validate at the same time

# Load best found weights
print("Loading best found model...")
model.load_weights('cnn_best_weights2.hdf5')
# Just some validation that everything works
(loss, accuracy) = model.evaluate(x=[X1_train, X2_train], y=y_train, verbose=1)
print(" - loss: {} - acc: {}".format(loss, accuracy))




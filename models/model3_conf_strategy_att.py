import tensorflow as tf
from tensorflow import keras
from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense

#CONFIGURAZIONE 1
def run_model1(X_graph,X_bert,dim_graph,dim_bert,y,epochs,batch_size):
  model = keras.Sequential()
  input_users_1 = keras.layers.Input(shape=(dim_graph,))
  input_items_1 = keras.layers.Input(shape=(dim_graph,))
  x1_user = input_users_1
  x1_item = input_items_1

  input_users_2 = keras.layers.Input(shape=(dim_bert,))
  input_items_2 = keras.layers.Input(shape=(dim_bert,))
  x2_user = keras.layers.Dense(768, activation=tf.nn.relu)(input_users_2)
  x2_item = keras.layers.Dense(768, activation=tf.nn.relu)(input_items_2)

  #user graph + user bert
  concatenated_1 = keras.layers.Concatenate()([x1_user, x2_user])

  #item graph + item bert
  concatenated_2 = keras.layers.Concatenate()([x1_item, x2_item])

  #dense after concat
  dense_graph = keras.layers.Dense(100, activation=tf.nn.relu)(concatenated_1)
  dense_bert = keras.layers.Dense(100, activation=tf.nn.relu)(concatenated_2)

  concatenated = keras.layers.Concatenate()([dense_graph, dense_bert])

  #BLOCCO DI ATTENZIONE 1
  attention_probs = keras.layers.Dense(200, activation='softmax')(concatenated)
  attention_mul = keras.layers.multiply([concatenated, attention_probs])

  '''
  #BLOCCO DI ATTENZIONE 2
  attention_probs = keras.layers.Dense(200, activation='softmax')(attention_mul)
  attention_mul = keras.layers.multiply([attention_mul, attention_probs])

  #BLOCCO DI ATTENZIONE 3
  attention_probs = keras.layers.Dense(200, activation='softmax')(attention_mul)
  attention_mul = keras.layers.multiply([attention_mul, attention_probs])
  '''

  dense_layer = keras.layers.Dense(100, activation=tf.nn.relu)(attention_mul)

  '''
  dropout = keras.layers.Dropout(0.2)(dense_layer)
  dense_layer = keras.layers.Dense(100, activation=tf.nn.relu)(dropout)
  '''

  out = keras.layers.Dense(1, activation=tf.nn.sigmoid)(dense_layer)
  model = keras.models.Model(inputs=[input_users_1,input_items_1,input_users_2,input_items_2],outputs=out)
  model.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9), metrics=['accuracy'])
  model.fit([X_graph[:,0],X_graph[:,1],X_bert[:,0],X_bert[:,1]], y, epochs=epochs, batch_size=batch_size)
  return model

#CONFIGURAZIONE 2
def run_model2(X_graph,X_bert,dim_graph,dim_bert,y,epochs,batch_size):
  model = keras.Sequential()
  input_users_1 = keras.layers.Input(shape=(dim_graph,))
  input_items_1 = keras.layers.Input(shape=(dim_graph,))
  x1_user = input_users_1
  x1_item = input_items_1

  input_users_2 = keras.layers.Input(shape=(dim_bert,))
  input_items_2 = keras.layers.Input(shape=(dim_bert,))
  x2_user = keras.layers.Dense(768, activation=tf.nn.relu)(input_users_2)
  x2_item = keras.layers.Dense(768, activation=tf.nn.relu)(input_items_2)

  #user graph + item graph
  concatenated_1 = keras.layers.Concatenate()([x1_user, x1_item])

  #user bert + item bert
  concatenated_2 = keras.layers.Concatenate()([x2_user, x2_item])

  #dense after concat
  dense_graph = keras.layers.Dense(100, activation=tf.nn.relu)(concatenated_1)
  dense_bert = keras.layers.Dense(100, activation=tf.nn.relu)(concatenated_2)

  concatenated = keras.layers.Concatenate()([dense_graph, dense_bert])

  #BLOCCO DI ATTENZIONE 1
  attention_probs = keras.layers.Dense(200, activation='softmax')(concatenated)
  attention_mul = keras.layers.multiply([concatenated, attention_probs])

  dense_layer = keras.layers.Dense(100, activation=tf.nn.relu)(attention_mul)

  out = keras.layers.Dense(1, activation=tf.nn.sigmoid)(dense_layer)
  model = keras.models.Model(inputs=[input_users_1,input_items_1,input_users_2,input_items_2],outputs=out)
  model.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9), metrics=['accuracy'])
  model.fit([X_graph[:,0],X_graph[:,1],X_bert[:,0],X_bert[:,1]], y, epochs=epochs, batch_size=batch_size)
  return model
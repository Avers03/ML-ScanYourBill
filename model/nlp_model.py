import numpy as np
import pandas as pd
import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split


# Dataset
data = pd.read_csv('data/data.csv')

# Separate the features and the labels
texts = data['nama']
labels = data['kategori']


# Convert labels to integers
unique_labels = ['Clothing', 'Food', 'Stationery', 'Others', 'Toiletries', 'Medical & Healthcare', 'Entertainment']
labels = [unique_labels.index(label) for label in labels]

# Tokenize the texts
tokenizer = Tokenizer(num_words=1000)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)

# Pad the sequences
data = pad_sequences(sequences, maxlen=100)

# Convert labels to categorical
labels = to_categorical(np.asarray(labels))

# Split the data into a training set and a validation set
x_train, x_val, y_train, y_val = train_test_split(data, labels, test_size=0.2)


# Define the model
model = Sequential()
model.add(Embedding(1000, 128, input_length=100))
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(LSTM(32, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(7, activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# Train the model
# early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True)

model.fit(x_train, y_train,
          batch_size=32,
          epochs=100,
          validation_data=(x_val, y_val))


# Predict the category of a new item
new_text = ['obat demam']
sequences = tokenizer.texts_to_sequences(new_text)
data = pad_sequences(sequences, maxlen=100)
predictions = model.predict(data)

# Get the category with the highest probability
predicted_category = unique_labels[np.argmax(predictions)]
print(predicted_category)


# Save the model
model.save('model/model.h5')

# Save the tokenizer
import pickle
with open('model/tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
# reference: https://medium.com/holler-developers/intent-detection-using-sequence-models-ddae9cd861ee
# Personally I do not know too much technical details about deep learning. Most of the code is from above

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import utils
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.metrics import Precision, Recall
from sklearn import metrics
dataset_path = "./new_dataset_more_intents/dataset.json"
df = pd.read_json(dataset_path)
df.columns = ["text", "intent"]
X_train, X_test, y_train, y_test = train_test_split(df["text"], df["intent"],
                                                    test_size = 0.2)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(list(X_train))

X_seq = tokenizer.texts_to_sequences(list(X_train))
X_test_seq = tokenizer.texts_to_sequences(list(X_test))

MAX_SEQ_LEN = 35

X = pad_sequences(X_seq, maxlen = MAX_SEQ_LEN, padding = 'post')
X_test = pad_sequences(X_test_seq, maxlen = MAX_SEQ_LEN, padding = 'post')


y = y_train.to_numpy()
encoder = LabelEncoder()
encoder.fit(y)

encoded_y = encoder.transform(y)
y_train_encoded = utils.to_categorical(encoded_y)

y_test = y_test.to_numpy()
encoded_y_test = encoder.transform(y_test)
y_test_encoded = utils.to_categorical(encoded_y_test)

VAL_SPLIT = 0.1
BATCH_SIZE = 32
EPOCHS = 35
EMBEDDING_DIM = 16
NUM_UNITS = 16
NUM_CLASSES = len(df['intent'].unique())
VOCAB_SIZE = len(tokenizer.word_index) + 1


lstm_model = Sequential()
lstm_model.add(Embedding(input_dim = VOCAB_SIZE, output_dim = EMBEDDING_DIM, input_length = MAX_SEQ_LEN, mask_zero = True))
lstm_model.add(LSTM(NUM_UNITS, activation='relu'))
lstm_model.add(Dense(NUM_CLASSES, activation='softmax'))

lstm_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=[Precision(), Recall(), 'accuracy'])
lstm_history = lstm_model.fit(X, y_train_encoded, batch_size = BATCH_SIZE, epochs = EPOCHS, verbose = 1, validation_split = VAL_SPLIT)
lstm_score = lstm_model.evaluate(X_test, y_test_encoded, batch_size = BATCH_SIZE, verbose = 1)



y_pred_labels_lstm = [encoder.classes_[x] for x in np.argmax(lstm_model.predict(X_test), axis=-1)]
print(metrics.classification_report(y_test, y_pred_labels_lstm))

text_file = open(dataset_path.replace(".json", "_result_EPOCHS_35.json"), "w")
text_file.write(metrics.classification_report(y_test, y_pred_labels_lstm))
text_file.close()
import librosa
import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Flatten, LSTM
from keras.layers import Dropout, BatchNormalization

def extract_feature(file_name):
    X, sample_rate = librosa.load(file_name)
    X = librosa.util.pad_center(X, 30*sample_rate)
    mfcc = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40), axis=1)
    return mfcc


def parse_audio_files(filename):
    print(filename)
    features = []
    try:
        extracted = extract_feature(filename)
    except Exception as e:
        print('cannot open', e)
    
    ext_features = np.hstack(extracted)
    features.append(ext_features) 
    return np.array(features)


def create_model(X):  
    model = Sequential()
    model.add(BatchNormalization(axis=-1, input_shape=(X.shape[1],X.shape[2]))) 
    model.add(LSTM(256, return_sequences=True))  
    model.add(LSTM(256, return_sequences=True))
    model.add(LSTM(256, return_sequences=True))
    model.add(Flatten())
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))
              
    # model compilation
    model.compile(loss='binary_crossentropy', metrics=['accuracy'])  
    return model


def detect(filename):
    X = parse_audio_files(filename)
    X = X.reshape((X.shape[0], 1, X.shape[1]))

    model = create_model(X)
    model.load_weights('src/controllers/detection/model_coswaranew_lstm_mfccmean_smote.h5')


    classes = model.predict(X)
    selisih_to_0 = abs(0-classes[0][0])
    selisih_to_1 = abs(1-classes[0][0])
    if(min(selisih_to_0, selisih_to_1) == selisih_to_0):
        return 'negatif', classes[0][0]
    else:
        return 'positif', classes[0][0]



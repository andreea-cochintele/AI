from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.models import Sequential
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from sklearn import preprocessing
import librosa
import tensorflow as tf
import matplotlib.pyplot as plt
import glob
import numpy as np
import os

train_names = []
train_data = []
test_data = []
test_names = []
valid_data = []
valid_names = []
data_changed = []

# citim datele de train le transformam in MFCC si le normalizam
for filepath in glob.glob('../input/ml231/train/train' + '/*.wav'):
    # citim wav-urile
    data, sample_rate = librosa.load(filepath)
    # le transformam in mfcc
    spec_data = librosa.feature.mfcc(y=data, sr=sample_rate, n_mfcc=44)
    # retinem numele fisierului
    train_names.append(os.path.basename(filepath))
    # normalizam datele pentru a le aduce intre -1 si 1
    spec_data = preprocessing.normalize(spec_data)
    # in cazul in care avem date goale dupa transformare le umplem
    if np.any(np.isnan(spec_data)):
        np.nan_to_num(spec_data)
    # retinem datele normalizate
    train_data.append(spec_data)
    # plt.pcolormesh(segment_time,sample_freq,spec_data)
    # plt.show()

train_data = np.array(train_data)
number = train_data.shape[0]
spec_height = train_data.shape[1]
spec_width = train_data.shape[2]

# preprocesare pentru datele de train
train_data = np.expand_dims(train_data, axis=0)
train_data = train_data.reshape(number, spec_height, spec_width, 1)
train_data = train_data.astype('float32')


# citim etichetele datelor de train
train_labels_file = open('../input/ml231/train.txt', 'r')
train_labels = [0] * 8000
for line in train_labels_file.readlines():
    name = line.split(',')[0]
    label = line.split(',')[1]
    if name in train_names:
        train_labels[train_names.index(name)] = int(label)
train_labels = np.array(train_labels)
# ii specificam clar ca putem avea doar doua clase
train_labels = to_categorical(train_labels, 2)

# citim datele de validare le transformam in MFCC si le normalizam
for filepath in glob.glob('../input/ml231/validation/validation' + '/*.wav'):
    # citim wav-urile
    data, sample_rate = librosa.load(filepath)
    # le transformam in MFCC
    spec_data = librosa.feature.mfcc(y=data, sr=sample_rate, n_mfcc=44)
    # retinem numele datelor de validare
    valid_names.append(os.path.basename(filepath))
    # normalizam datele pentru a fi intre -1 si 1
    spec_data = preprocessing.normalize(spec_data)
    # in cazul in care avem date goale dupa transformare le umplem
    if np.any(np.isnan(spec_data)):
        np.nan_to_num(spec_data)
    # retinem datele de validare
    valid_data.append(spec_data)


valid_data = np.array(valid_data)

# preprocesare pentru datele de validare
valid_data = np.expand_dims(valid_data, axis=0)
valid_data = valid_data.reshape(1000, spec_height, spec_width, 1)
valid_data = valid_data.astype('float32')

# citim etichetele datelor de validare
validation_labels_file = open('../input/ml231/validation.txt', 'r')
valid_labels = [0] * 1000
for line in validation_labels_file.readlines():
    name = line.split(',')[0]
    label = line.split(',')[1]
    if name in valid_names:
        valid_labels[valid_names.index(name)] = int(label)
valid_labels = np.array(valid_labels)
# ii spunem ca avem doua categorii
valid_labels = to_categorical(valid_labels, 2)

# citim datele de test le transformam in MFCC si le normalizam
for filepath in glob.glob('../input/ml231/test/test' + '/*.wav'):
    # citim wav-urile
    data, sample_rate = librosa.load(filepath)
    # le transformam in MFCC
    spec_data = librosa.feature.mfcc(y=data, sr=sample_rate, n_mfcc=44)
    # retinem numele
    test_names.append(os.path.basename(filepath))
    # normalizam datele pentru a fi intre -1 si 1
    spec_data = preprocessing.normalize(spec_data)
    # in cazul in care avem date goale dupa transformare le umplem
    if np.any(np.isnan(spec_data)):
        np.nan_to_num(spec_data)
    #retinem datele
    test_data.append(spec_data)


test_data = np.array(test_data)

# preprocesare pentru datele de test
test_data = np.expand_dims(test_data, axis=0)
test_data = test_data.reshape(3000, spec_height, spec_width, 1)
test_data = test_data.astype('float32')




# creem modelul
model = Sequential()

# ii adaugam straturi 
model.add(Conv2D(10, kernel_size=(3, 3), activation='relu', input_shape=(spec_height, spec_width, 1), padding='same'))
model.add(MaxPooling2D())
model.add(Dropout(0.2))
model.add(Conv2D(50, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D())
model.add(Dropout(0.2))
model.add(Conv2D(100, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D())
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(50, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(2, activation='softmax'))
#model.summary()
model.compile(optimizer='rmsprop', loss="mse", metrics=['accuracy'])

#am impartit datele de train pentru a vedea daca are overfit mai rapid si dupa aceea i-am dat fit pe toate datele de train
# train_data1, train_data2, train_labels1, train_labels2 = train_test_split(train_data, train_labels, test_size=0.3)
history = model.fit(train_data, train_labels, epochs=50, shuffle=True)

print("Validation data:")
valid_loss, valid_acc = model.evaluate(valid_data, valid_labels)
print(valid_loss)
print(valid_acc)
print("Train data:")
valid_loss, valid_acc = model.evaluate(train_data, train_labels)
print(valid_loss)
print(valid_acc)

#am impartit datele de validare pentru a vedea daca scorurile sunt asemanatoare
valid_data1, valid_data2, valid_labels1, valid_labels2 = train_test_split(valid_data, valid_labels, test_size=0.3)
valid_loss, valid_acc = model.evaluate(valid_data1, valid_labels1)
print("Validation data(70%):")
print(valid_loss)
print(valid_acc)
valid_loss, valid_acc = model.evaluate(valid_data2, valid_labels2)
print("Validation data(30%):")
print(valid_loss)
print(valid_acc)

test_labels = model.predict_classes(test_data)
print(model.predict(test_data))

# adaugam in csv datele pe care le-a prezis modelul
f = open("predict.csv", "w+")
f.write("name,label\n")
i = 0
for name in test_names:
    f.write(name)
    f.write(',')
    f.write(str(test_labels[i]))
    i = i + 1
    f.write('\n')

import random

import keras.layers
import numpy as np
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras.optimizers import SGD

from modules.classifiers.common.intentclassifier import IntentClassifier


class TF_IDF(IntentClassifier):
    """
    Classifier using TF-IDF model.
    """
    
    def train_model(self, epochs: int = 250):
        """
        Implementation of the training function.
        """
        print("Training with TF-IDF")

        tfidf_vectorizer = keras.layers.TextVectorization(output_mode='tf-idf',
                                                          standardize="lower_and_strip_punctuation")
        tfidf_vectorizer.adapt([doc[0] for doc in self.documents])

        # we need numerical values of the words because a neural network needs numerical values to work with
        self.training = []
        output_empty = [0] * len(self.classes)
        for document in self.documents:
            # making a copy of the output_empty
            output_row = list(output_empty)
            output_row[self.classes.index(document[2])] = 1
            self.training.append([document[0], output_row])

        random.shuffle(self.training)
        self.training = np.array(self.training, dtype=object)

        # splitting the data
        train_x = list(self.training[:, 0])
        train_y = list(self.training[:, 1])

        # creating a Sequential machine learning model
        model = Sequential()
        model.add(tfidf_vectorizer)
        model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(train_y[0]), activation='softmax'))

        # compiling the model
        sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
        hist = model.fit(np.array(train_x), np.array(train_y), epochs=epochs, batch_size=5, verbose=1)

        return (model, hist)

    def predict(self, sentence: str, verbose: int = 0) -> list[dict]:
        """
        Implementation of the predict function.
        """
        return self.model.predict([sentence], verbose=verbose)[0]

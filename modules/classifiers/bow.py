import random
import nltk
import numpy as np
import numpy.typing as npt
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras.optimizers import SGD
from modules.classifiers.common.intentclassifier import IntentClassifier


class BagOfWords(IntentClassifier):
    def train_model(self, epochs: int = 250):
        """
        Model training implementation
        """
        print("Training with Bag-of-Words")

        # we need numerical values of the words because a neural network needs numerical values to work with
        self.training = []
        output_empty = [0] * len(self.classes)
        for document in self.documents:
            bag = []
            word_patterns = document[1]
            word_patterns = [self.lemmatizer.lemmatize(word.lower()) for word in word_patterns]
            for word in self.words:
                bag.append(1) if word in word_patterns else bag.append(0)

            # making a copy of the output_empty
            output_row = list(output_empty)
            output_row[self.classes.index(document[2])] = 1
            self.training.append([bag, output_row])

        random.shuffle(self.training)
        self.training = np.array(self.training, dtype=object)

        # splitting the data
        train_x = list(self.training[:, 0])
        train_y = list(self.training[:, 1])

        # creating a Sequential machine learning model
        model = Sequential()
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

    def clean_up_sentences(self, sentence: str) -> list[str]:
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(word) for word in sentence_words]
        return sentence_words

    def bag_of_words(self, sentence: str) -> npt.NDArray:
        sentence_words = self.clean_up_sentences(sentence)
        bag = [0] * len(self.words)
        for w in sentence_words:
            for i, word in enumerate(self.words):
                if word == w:
                    bag[i] = 1
        return np.array(bag)

    def predict(self, sentence: str, verbose=0) -> list[dict]:
        """
        Model prediction implementation
        """
        bow: npt.NDArray = self.bag_of_words(sentence)
        return self.model.predict(np.array([bow]), verbose=verbose)[0]
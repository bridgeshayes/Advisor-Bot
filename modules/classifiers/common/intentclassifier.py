import json
import os
import pickle
import random
import string
from abc import ABC, abstractmethod

import nltk
import pymongo
from dotenv import load_dotenv
from keras.models import load_model
from keras.models import Model
from keras.callbacks import History
from nltk.stem import WordNetLemmatizer


class IntentClassifier(ABC):
    """
    Generic classifier that can be implemented by various models.
    """

    def __init__(self, bot_name: str):
        if load_dotenv():
            mongo_uri = os.getenv('MONGO_URI')
            cl = pymongo.MongoClient(mongo_uri)
            self.db = cl["chatbot-database"]
            self.coll = self.db.intents
            self.intents = self.coll.find()
            MODEL_DIR = os.getenv('MODEL_DIR')

        else:
            self.intents = json.loads(open("data/intents_2.json").read())

        self.name: str = bot_name
        self.words: list[str] = []
        self.classes: list[str] = []
        self.documents = []
        self.training = []
        self.lemmatizer = WordNetLemmatizer()
        self.model = None
        self.trained = False
        self.chatbotmodel_file = MODEL_DIR + self.name + 'chatbotmodel.tf'
        self.wordspkl_file: str = "/" + self.name + 'words.pkl'
        self.classespkl_file: str = "/" + self.name + 'classes.pkl'

    def load_chatbot_model(self) -> None:
        """
        Assumes that the model has been trained and that the MongoDB is instantiated and executing
        """
        # load the model
        self.model = load_model(self.chatbotmodel_file)

        # load the vocabulary
        if self.db is not None:
            query = {"index": "data"}
            doc = self.db.dictionary.find_one(query)
            if doc:
                self.words = doc["words"]
                self.classes = doc["classes"]
        else:
            self.words = pickle.load(open(self.wordspkl_file, 'rb'))
            self.classes = pickle.load(open(self.classespkl_file, 'rb'))

        self.trained = True

    @abstractmethod
    def train_model(self, epochs: int) -> tuple[Model, History]:
        """
        Your implementation of the training of some model. You will probably need to use
        the self.documents and self.classes variables
        :param epochs: number of epochs to train
        :return: a trained model and a history object
        """
        pass

    def train(self, epochs: int = 250) -> None:
        ignore_letters: list[str] = [p for p in string.punctuation]

        for intent in self.intents:
            for pattern in intent['patterns']:
                # separating words from patterns
                word_list: list[str] = nltk.word_tokenize(pattern)
                self.words.extend(word_list)  # and adding them to words list

                # associating patterns with respective tags
                self.documents.append((pattern, word_list, intent['tag']))

                # appending the tags to the class list
                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])

        # storing the root words or lemma
        self.words: list[str] = [self.lemmatizer.lemmatize(word) for word in self.words if word not in ignore_letters]
        self.words = sorted(set(self.words))

        # saving the words and classes list to binary files
        learner_doc = {"index": "data", "words": self.words, "classes": self.classes}

        if self.db is not None:
            coll_list = self.db.list_collections()
            if "dictionary" not in coll_list:
                dictionary = self.db["dictionary"]
            else:
                dictionary = self.db.dictionary
            query = {"index": "data"}
            doc = dictionary.find_one(query)
            if doc:
                dictionary.update_one(query, {"$set": learner_doc})
            else:
                dictionary.insert_one(learner_doc)
        else:
            pickle.dump(self.words, open(self.wordspkl_file, 'wb'))
            pickle.dump(self.classes, open(self.classespkl_file, 'wb'))

        model, hist = self.train_model(epochs)

        # saving the model
        model.save(self.chatbotmodel_file, hist, save_format='tf')
        self.trained = True

    @abstractmethod
    def predict(self, sentence: str, verbose=0) -> list[dict]:
        """
        Your implementation of the prediction of some sentence. You will probably want to call
        the self.model.predict function, passing the sentence in the correct way.
        :param sentence: the sentence to be predicted
        :return: a list of dictionaries containing the prediction and the probability
        """
        pass

    def predict_class(self, sentence: str, debug=False) -> list[dict]:
        """
        Predicts an intent class using an implemented classifier
        :param sentence: message from the user
        :param debug: output in verbose mode if True
        :return: string with the intent class
        """
        if not self.trained:
            self.load_chatbot_model()
        verbose: int = 0 if not debug else 1
        res = self.predict(sentence, verbose)
        error_threshold = 0.25
        results = [[i, r] for i, r in enumerate(res) if r > error_threshold]
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({'intent': self.classes[r[0]], 'probability': str(r[1])})
            return return_list
        
        '''
        TODO: It seems that not all models return probability lists if they are not confident
        in anything. Probably need to return a fallback statement here as a default.
        '''

    def get_response(self, sentence: str, debug: bool = False) -> tuple[str, str]:
        """
        Used to predict an intent of an input and outputs a response appropriate to the intent
        :param sentence: user message
        :param debug: if True, output extra debug information
        :param mode: Prediction algorithm (should be same as training)
        :return: message
        """
        intents_list = self.predict_class(sentence, debug)
        if intents_list is not None:
            tag: str = intents_list[0]['intent']
            list_of_intents: list[dict] = self.intents
            result = ""
            for i in list_of_intents:
                if i['tag'] == tag:
                    result = random.choice(i['responses'])
                    self.intents.rewind()
                    break
            if debug:
                result = str(intents_list) + " " + result
        else:
            result = "I am able to do many things."
            intents_list = [{'intent': 'clueless', 'probability': '1.0'}]
        return result, intents_list

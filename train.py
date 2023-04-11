# importing the required modules.
import os
from dotenv import load_dotenv
import nltk

from modules.classifiers.common.intentclassifier import IntentClassifier

from modules.classifiers.bow import BagOfWords
from modules.classifiers.tfidf import TF_IDF


def load_classifier(CLASSIFICATION_MODEL: str, channel_name: str) -> IntentClassifier:
    """
    Load classifier from string name
    :param channel_name:
    :param CLASSIFICATION_MODEL: name of the classifier
    :return: the loaded classifier
    """
    if CLASSIFICATION_MODEL == "BagOfWords":
        return BagOfWords(channel_name)
    elif CLASSIFICATION_MODEL == "TF_IDF":
        return TF_IDF(channel_name)
    else:
        print("Specified predictor is invalid. Falling back to BagOfWords")
        return BagOfWords(channel_name)


if __name__ == "__main__":
    if load_dotenv():
        CLASSIFICATION_MODEL = os.getenv('CLASSIFICATION_MODEL')
        
        nltk.download('punkt')
        nltk.download('wordnet')

        classifier = load_classifier(CLASSIFICATION_MODEL, "advisor")
        
        classifier.train(180)
        print("System Trained ")
    else:
        print("No .env file found")
from parsa import Interpreter
import pickle as pickle
import cloudpickle
import spacy
from parsa.featurizers.spacy_featurizer import SpacyFeaturizer
from parsa.extractors.spacy_entity_extractor import SpacyEntityExtractor
#from parsa.

class SpacySklearnInterpreter(Interpreter):
    def __init__(self,entity_extractor=None,intent_classifier=None,**kwargs):
        self.nlp = spacy.load('en')
        self.featurizer = SpacyFeaturizer(self.nlp)        
        with open(intent_classifier,'rb') as f:
            self.classifier = cloudpickle.load(f)

        self.extractor = SpacyEntityExtractor(self.nlp,entity_extractor)
            
    def get_intent(self,text):
        X = self.featurizer.create_bow_vecs([text])
        return self.classifier.predict(X)[0]
        
    def parse(self,text):
        intent = self.get_intent(text)
        entities = self.extractor.extract_entities(self.nlp,text)

        return {'text':text,'intent':intent,'entities': entities}


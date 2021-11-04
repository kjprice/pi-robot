from .resnet_classification import Resnet_Classification
from .faces_classification import Faces_Classification
from ..config import CLASSIFICATION_MODELS

def load_classification_model_by_name(model_name: CLASSIFICATION_MODELS):
  if model_name == CLASSIFICATION_MODELS.RESNET_COCO:
    return Resnet_Classification()
  if model_name == CLASSIFICATION_MODELS.FACES_ONLY:
    return Faces_Classification()
  
  raise ValueError('Unknown model_name: "{}"'.format(model_name))

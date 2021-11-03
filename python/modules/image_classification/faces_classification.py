from .image_classification import Image_Classification
from ..config import get_face_classifiers

class Faces_Classification(Image_Classification):
  def __init__(self) -> None:
      self.face_cascades = get_face_classifiers()
  def find_faces_in_any_classifier(self, img):
      for classifier in self.face_cascades:
          faces = classifier.detectMultiScale(img, 1.1, 4)
          if len(faces) > 0:
              return faces
      return None

  def predict(self, img):
      return self.find_faces_in_any_classifier(img)

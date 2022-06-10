from ..config import RESNET_MODEL_FILEPATH, SAVE_IMAGE_DIR
from .image_classification import Image_Classification

import os
import time

class Resnet_Classification(Image_Classification):
  time_to_load_model = None
  def __init__(self) -> None:
    start_time = time.time()
    self.load_model()
    super().__init__()
    end_time = time.time()
    self.time_to_load_model = end_time - start_time

    print('it took {} seconds to load the model'.format(self.time_to_load_model))
  
  def predict(self, img):
    # TODO: Instead of saving, just return the image
    output_image_path = os.path.join(SAVE_IMAGE_DIR, 'imagenew.jpg')
    detections = self.model.detectObjectsFromImage(input_image=img, output_image_path=output_image_path, input_type="array", output_type="file")
    return detections
    
  def load_model(self):
    print('loading model')
    # Import the model here instead of globally because it takes such a long time to load and may not be used by its dependencies
    from imageai.Detection import ObjectDetection
    self.model = detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(RESNET_MODEL_FILEPATH)
    detector.loadModel()

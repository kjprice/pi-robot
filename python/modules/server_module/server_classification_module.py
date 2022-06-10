from .server_module import ServerModule
from ..config import CLASSIFICATION_MODELS, DEFAULT_CLASSIFICATION_MODEL, SERVER_NAMES
from ..image_processor import Image_Processor

class Server_Classification_Module(ServerModule):
  def __init__(self, server_name: SERVER_NAMES, arg_flags):
      super().__init__(server_name, arg_flags)
      self.image_processor = Image_Processor(send_output=self.send_output)
      self.set_new_classification_model(self.classification_model)

  @property
  def classification_model(self):
    return self.get_args().classification_model

  def other_socket_events(self):
    super().other_socket_events()
    sio = self.sio
        
    @sio.event
    def set_new_classification_model(classification_model: str):
        self.send_output('Setting new classification model: ', classification_model)
        self.set_new_classification_model(classification_model)

  def other_args(self):
    super().other_args()
    self.send_output('setting argument for classification model')
    self.parser.add_argument(
      '--classification_model',
      type=str,
      default=DEFAULT_CLASSIFICATION_MODEL.name
    )

  def set_new_classification_model(self, classification_model_name: str):
    classification_model = CLASSIFICATION_MODELS[classification_model_name]
    self.image_processor.set_preferred_classification_model_name(classification_model)

export const SET_SERVER_INITIAL_STATE = 'SET_SERVER_INITIAL_STATE';
export const SERVER_START_INIT = 'SERVER_START_INIT';
export const SERVER_START_UPDATE = 'SERVER_START_UPDATE';
export const SERVER_START_COMPLETE = 'SERVER_START_COMPLETE';
export const SET_WAIT_BETWEEN_IMAGES = 'SET_NEW_WAIT_BETWEEN_IMAGES';
export const SERVER_STOP_INIT = 'SERVER_STOP_INIT';
export const SERVER_STOP_COMPLETE = 'SERVER_STOP_COMPLETE';
export const SERVER_OUTPUT_RECEIVED = 'SERVER_OUTPUT_RECEIVED';
export const SERVER_PROCESSED_IMAGE_RECEIVED = 'SERVER_PROCESSED_IMAGE_RECEIVED';
export const SERVER_SET_CLASSIFICATION_MODEL = 'SERVER_SET_CLASSIFICATION_MODEL';
export const SET_SERVER_WEBSERVER_OFFLINE = 'SET_SERVER_WEBSERVER_OFFLINE';
export const SET_SERVER_WEBSERVER_CONNECTED = 'SET_SERVER_WEBSERVER_CONNECTED';

export const SERVER_STATUSES = {
  STARTING: 'starting',
  ONLINE: 'online',
  STOPPING: 'stopping',
  OFFLINE: 'offline'
};

// Taken from config.py: TODO: Consolidate somehow
export const CLASSIFICATION_MODELS = {
  RESNET_COCO: 'RESNET_COCO',
  FACES_ONLY: 'FACES_ONLY'
};

// TODO: This should probably go in a config file
export const SERVER_DESCRIPTIONS = {
  webApp: 'Web Server: Controls everything',
  allServers: 'Camera head, Image Processor, and Servo Server (if running remote servers)'
}
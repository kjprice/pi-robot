import * as serverConstants from '../constants/server-constants';
const {
  SERVER_PROCESSED_IMAGE_RECEIVED,
  SERVER_START_INIT,
  SERVER_START_UPDATE,
  SERVER_START_COMPLETE,
  SERVER_STOP_INIT,
  SERVER_STOP_COMPLETE,
  SET_SERVER_INITIAL_STATE,
  SERVER_OUTPUT_RECEIVED,
  SET_WAIT_BETWEEN_IMAGES,
} = serverConstants;

export const setServerStartInit = () => ({ type:SERVER_START_INIT });
export const setServerStartUpdateStatus = (payload) => ({ type:SERVER_START_UPDATE, payload });
export const setServerStartComplete = (payload) => ({ type:SERVER_START_COMPLETE, payload });
export const setServerInitialStatus = (payload) => ({ type: SET_SERVER_INITIAL_STATE, payload})
export const setWaitBetweenImages = (payload) => ({ type: SET_WAIT_BETWEEN_IMAGES, payload})
export const setServerStopInit = () => ({ type: SERVER_STOP_INIT })
export const setServerStopComplete = () => ({ type: SERVER_STOP_COMPLETE })
export const setServerOutputReceived = (payload) => ({ type: SERVER_OUTPUT_RECEIVED, payload})
export const setServerProcessedImageReceived = (payload) => ({ type: SERVER_PROCESSED_IMAGE_RECEIVED, payload})

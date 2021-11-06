import {
  SERVER_START_INIT,
  SERVER_START_UPDATE,
  SERVER_START_COMPLETE,
  SERVER_STOP_INIT,
  SERVER_STOP_COMPLETE,
  SERVER_STATUSES,
  SET_SERVER_INITIAL_STATE,
  SERVER_OUTPUT_RECEIVED,
  SET_WAIT_BETWEEN_IMAGES,
  SERVER_SET_CLASSIFICATION_MODEL,
  SERVER_PROCESSED_IMAGE_RECEIVED,
  CLASSIFICATION_MODELS,
  SET_SERVER_WEBSERVER_OFFLINE,
  SET_SERVER_WEBSERVER_CONNECTED,
} from '../constants/server-constants';

const getDefaultState = () => ({
  serversStatuses: {
    webAppStatus: SERVER_STATUSES.OFFLINE,
    allServersStatus: SERVER_STATUSES.OFFLINE,
  },
  serverStatusInitMessages: [],
  waitTimeBetweenImages: 1, // Time in seconds
  serverOutputByProcessName: {},
  processedImage: null,
  classificationModel: CLASSIFICATION_MODELS.FACES_ONLY
});

const setServerInitialState = (state, payload) => {
  const { jobs_running: jobsRunning } = payload;

  let allServersStatus = SERVER_STATUSES.OFFLINE;
  if (jobsRunning.length > 0) {
    allServersStatus = SERVER_STATUSES.ONLINE;
  }

  const { serversStatuses } = state;

  return {
    ...state,
    serversStatuses: {
      ...serversStatuses,
      allServersStatus,
      webAppStatus: SERVER_STATUSES.ONLINE,
    }
  }
}

const setServerInitUpdates = (state, statusMessage) => {
  const timestamp = Date.now();
  const messageObject = {
    statusMessage,
    timestamp
  };

  const serverStatusInitMessages = [...state.serverStatusInitMessages, messageObject];

  return {
    ...state,
    serverStatusInitMessages
  }}

function setServerStartInit(state, serverName) {
  const { serversStatuses } = state;
  return {
    ...state,
    serversStatuses: {
      ...serversStatuses,
      [serverName]: SERVER_STATUSES.STARTING
    }
  }
}

function setServerStartComplete(state, serverName) {
  const { serversStatuses } = state;
  return {
    ...state,
    serversStatuses: {
      ...serversStatuses,
      [serverName]: SERVER_STATUSES.ONLINE
    }
  }
}

function setWaitBetweenImages(state, waitTimeBetweenImages) {
  return {
    ...state,
    waitTimeBetweenImages
  };
}

function setServerStopInit(state, serverName) {
  const { serversStatuses } = state;
  return {
    ...state,
    serversStatuses: {
      ...serversStatuses,
      [serverName]: SERVER_STATUSES.STOPPING
    }
  }
}

function setServerStopComplete(state, serverName) {
  const { serversStatuses } = state;
  return {
    ...state,
    serversStatuses: {
      ...serversStatuses,
      [serverName]: SERVER_STATUSES.OFFLINE
    }
  }
}

function setServerOutputReceived(state, data) {
  const { server_name: serverName, message } = data;

  const { serverOutputByProcessName: serverOutputByProcessNameFromState } = state;
  const serverOutputMessages = serverOutputByProcessNameFromState[serverName] || [];
  const newOutputMessage = {
    timestamp: (new Date()).toISOString(),
    message
  }
  const serverOutputByProcessName = {
    ...serverOutputByProcessNameFromState,
    [serverName]: [
      newOutputMessage,
      ...serverOutputMessages
    ]
  };

  return {
    ...state,
    serverOutputByProcessName
  }
}

function setServerProcessedImageReceived(state, processedImage) {
  return {
    ...state,
    processedImage
  }
}

function setServerProcessedClassificationModel(state, classificationModel) {
  return {
    ...state,
    classificationModel
  }
}

export default function serverReducer(state = getDefaultState(), data) {
  const { type } = data;

  switch (type) {
    case SERVER_START_INIT:
      return setServerStartInit(state, 'allServersStatus');
    case SERVER_START_UPDATE:
      return setServerInitUpdates(state, data.payload);
    case SERVER_START_COMPLETE:
      return setServerStartComplete(state, 'allServersStatus');
    case SET_SERVER_INITIAL_STATE:
      return setServerInitialState(state, data.payload);
    case SET_WAIT_BETWEEN_IMAGES:
      return setWaitBetweenImages(state, data.payload);
    case SERVER_STOP_INIT:
      return setServerStopInit(state, 'allServersStatus');
    case SERVER_STOP_COMPLETE:
      return setServerStopComplete(state, 'allServersStatus');
    case SERVER_OUTPUT_RECEIVED:
      return setServerOutputReceived(state, data.payload);
    case SERVER_PROCESSED_IMAGE_RECEIVED:
      return setServerProcessedImageReceived(state, data.payload);
    case SERVER_SET_CLASSIFICATION_MODEL:
      return setServerProcessedClassificationModel(state, data.payload);
    case SET_SERVER_WEBSERVER_OFFLINE:
      return setServerStopComplete(state, 'webAppStatus');
    case SET_SERVER_WEBSERVER_CONNECTED:
      return setServerStartInit(state, 'webAppStatus');
    default:
      return state;
  }
}
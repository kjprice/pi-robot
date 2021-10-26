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
  SERVER_PROCESSED_IMAGE_RECEIVED
} from '../constants/server-constants';

const getDefaultState = () => ({
  serversStatus: SERVER_STATUSES.OFFLINE,
  serverStatusInitMessages: [],
  waitTimeBetweenImages: 1, // Time in seconds
  serverOutputByProcessName: {},
  processedImage: null
});

const setServerInitialState = (state, payload) => {

  const { jobs_running: jobsRunning } = payload;

  let serversStatus = SERVER_STATUSES.OFFLINE;
  if (jobsRunning.length > 0) {
    serversStatus = SERVER_STATUSES.ONLINE;
  }

  return {
    ...state,
    serversStatus
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

function setServerStartComplete(state) {
  return {
    ...state,
    serversStatus: SERVER_STATUSES.ONLINE
  }
}

function setWaitBetweenImages(state, waitTimeBetweenImages) {
  return {
    ...state,
    waitTimeBetweenImages
  };
}

function setServerStopInit(state) {
  return {
    ...state,
    serversStatus: SERVER_STATUSES.STOPPING
  }
}

function setServerStopComplete(state) {
  return {
    ...state,
    serversStatus: SERVER_STATUSES.OFFLINE,
    serverStatusInitMessages: []
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

export default function serverReducer(state = getDefaultState(), data) {
  const { type } = data;

  switch (type) {
    case SERVER_START_INIT:
      return {
        ...state,
        serversStatus: SERVER_STATUSES.STARTING
      };
    case SERVER_START_UPDATE:
      return setServerInitUpdates(state, data.payload);
    case SERVER_START_COMPLETE:
      return setServerStartComplete(state);
    case SET_SERVER_INITIAL_STATE:
      return setServerInitialState(state, data.payload);
    case SET_WAIT_BETWEEN_IMAGES:
      return setWaitBetweenImages(state, data.payload);
    case SERVER_STOP_INIT:
      return setServerStopInit(state);
    case SERVER_STOP_COMPLETE:
      return setServerStopComplete(state);
    case SERVER_OUTPUT_RECEIVED:
      return setServerOutputReceived(state, data.payload);
    case SERVER_PROCESSED_IMAGE_RECEIVED:
      return setServerProcessedImageReceived(state, data.payload);
    default:
      return state;
  }
}
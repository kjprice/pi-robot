import * as serverConstants from '../constants/server-constants';
const {
  SET_SERVERS_ONLINE
} = serverConstants;

export const setServerLoaded = () => ({ type:SET_SERVERS_ONLINE });
import { SET_SERVERS_ONLINE } from '../constants/server-constants';

export default function serverReducer(state = [], action) {
  switch (action) {
    case SET_SERVERS_ONLINE:
      return state;
    default:
      return state;
  }
}
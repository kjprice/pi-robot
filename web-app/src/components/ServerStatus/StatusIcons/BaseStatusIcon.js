import { CircleFill } from 'react-bootstrap-icons';

function BaseStatusIcon(props) {
  const { color } = props;

  return <CircleFill color={color} />
}

export default BaseStatusIcon;
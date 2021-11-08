import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Popover from 'react-bootstrap/Popover';

function Tooltip(props) {
  const { message, children } = props;

  return (
    <OverlayTrigger
      trigger={["hover", "focus"]}
      placement="bottom-start"
      overlay={
        <Popover id="popover-contained" body>
          {message}
        </Popover>
      }
    >
      <span>{children}</span>
    </OverlayTrigger>
  );
}

export default Tooltip
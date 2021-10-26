import ServerStatusOutput from './ServerStatusOutput';
import ServerStatusStdOut from './ServerStatusStdOut';

export default function ServerOutput() {
  return (
    <div>
      <ServerStatusOutput />
      <ServerStatusStdOut />
    </div>
  );
}
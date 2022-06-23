port=$1
process_id=$(lsof -i :$port -t)

if [ ! -z $process_id ]; then
  echo killing process $process_id on port $port
  kill $process_id
fi
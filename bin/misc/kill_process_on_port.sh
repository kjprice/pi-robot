port=$1
process_id=$(lsof -i :$port -t)

for i in $(lsof -i :$port -t); do
  echo killing process $process_id on port $port
  kill $process_id
done
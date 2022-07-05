from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
# import array

import time

# a, b = Pipe()
# a.send([1, 'hello', None])
# b.recv()
# b.send_bytes(b'thank you')
# print(a.recv_bytes())


# arr1 = array.array('i', range(5))
# arr2 = array.array('i', [0] * 10)
# a.send_bytes(arr1)
# count = b.recv_bytes_into(arr2)
# assert count == len(arr1) * arr1.itemsize
# arr2

a, b = Pipe()

def count(q: Connection):
  for i in range(5):
    q.send(i)
    time.sleep(0.5)
  # q.close()

job = Process(
  target=count,
  args=(a,)
)

job.start()


# while True:
#   print(job.is_alive())
#   if not job.is_alive():
#     print('dead')
#     b.close()
#     break
#   if b.poll(0.1):
#     print(b.recv())
  # time.sleep(0.1)

send_output = None

import asyncio
async def poll():
  await asyncio.sleep(0.1)
  items = []
  while True:
    if b.poll():
      output = b.recv()
      send_output('output', output)
      items.append(output)

    if not job.is_alive():
      break
    await asyncio.sleep(0.1)

async def continuous_print():
  global send_output
  def _send_output(*args):
    # pass
    print(*args)
  send_output = _send_output

  for i in range(5):
    print(i)
    await asyncio.sleep(1)
  
# asyncio.run(main())

async def main():
  task1 = asyncio.create_task(poll())
  task2 = asyncio.create_task(continuous_print())

  await task1
  await task2

asyncio.run(main())
print('done')
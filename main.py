import mido
import time
from iothreads import InputThread
from iothreads import OutputThread

ins = mido.get_input_names()
input = InputThread(ins[0])
input.start()

outs = mido.get_output_names()
output = OutputThread(outs[0])
output.start()

while True:
  print(input.ticks)
  time.sleep(1)
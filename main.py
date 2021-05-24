import time
import threading
import mido

class InputThread(threading.Thread):
  def __init__(self, port):
    threading.Thread.__init__(self)
    self.port = port
    self.messages = []
  
  def run(self):
    with mido.open_input(self.port) as input:
      for msg in input:
        self.messages.append(self.parse_message(msg))

  def receive(self):
    return self.messages.pop() if self.messages else None

  def parse_message(self, message):
    data = str(message).split(" ")
    output = {}
    for i, x in enumerate(data):
      if i == 0:
        output["type"] = x
      else:
        output[x.split("=")[0]] = x.split("=")[1]
    return output


class OutputThread(threading.Thread):
  def __init__(self, port):
    threading.Thread.__init__(self)
    self.port = port
    self.messages = []

  def run(self):
    output = mido.open_output(self.port)
    while True:
      for message in self.messages:
        output.send(message)
        self.messages.remove(message)

  def send(self, message):
    self.messages.append(message)

ins = mido.get_input_names()
input = InputThread(ins[0])
input.start()

outs = mido.get_output_names()
output = OutputThread(outs[0])
output.start()

ticks = 0
eighth_note = 0

while True:
  try:
    print(input.receive())
  except KeyboardInterrupt:
    output.send(mido.Message('note_off', note=72))
    break
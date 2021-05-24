import threading
import mido

class InputThread(threading.Thread):
  def __init__(self, port):
    threading.Thread.__init__(self)
    self.port = port
    self.ticks = 0
    self.eighth_note = 0
  
  def run(self):
    with mido.open_input(self.port) as input:
      for message in map(self.parse_message, input):
        if message["type"] == "clock":
          self.ticks += 1
        elif message["type"] == "songpos":
          self.ticks = int(message["pos"])
        else: 
          print(message)

  def parse_message(self, message):
    data = str(message).split(" ")
    output = {}
    for i, x in enumerate(data):
      if i == 0: output["type"] = x
      else: output[x.split("=")[0]] = x.split("=")[1]
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
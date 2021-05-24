import mido
from iostreams import InputThread
from iostreams import OutputThread

ins = mido.get_input_names()
input = InputThread(ins[0])
input.start()

outs = mido.get_output_names()
output = OutputThread(outs[0])
output.start()

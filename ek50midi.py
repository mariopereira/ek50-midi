import mido as mido

class Ek50Midi:
    def __init__(self):
        """Initialize class"""
        mido.Backend('mido.backends.rtmidi')

        self.output = None
        self.outputChannel = 4


    def open_output(self, device = 'EK-50:EK-50 MIDI 1'):
        """Open the output port"""
        if self.output is not None:
            self.close_output()
            self.output = None

        self.output = mido.open_output(device) # pylint: disable=no-member


    def close_output(self):
        """Close the output port"""
        if self.output is not None:
            self.output.close()
            del self.output

        self.output = None


    def is_output_open(self):
        """Check if we have the output port open"""
        return self.output is not None


    def patch_change(self, msb, lsb, pc, channel = 4):
        """Changes the instrument in the output device"""
        return None
        #if not self.is_output_open():
        #    self.open_output()

        #msgMsb = mido.Message('control_change', control = 0, value = msb, channel = channel)
        #msgLsb = mido.Message('control_change', control = 0x20, value = lsb, channel = channel)
        #msgPc = mido.Message('program_change', program = pc, channel = channel)

        #self.output.send(msgMsb)
        #self.output.send(msgLsb)
        #self.output.send(msgPc)

import mido as mido

class Ek50Midi:
    def __init__(self):
        """Initialize class"""
        mido.Backend('mido.backends.rtmidi')

        self.output = None
        self.outputChannel = 4


    def adjust_port_list(self, ports):
        """Removes the device id from the ports"""
        ret = []

        for p in ports:
            parts = p.split()
            parts.pop()
            ret.append(' '.join(parts))

        return ret


    def output_list(self):
        """Get the names of the output ports found"""
        outputs = mido.get_output_names()
        return self.adjust_port_list(outputs)


    def input_list(self):
        """Get the names of the input ports found"""
        inputs = mido.get_input_names()
        return self.adjust_port_list(inputs)


    def open_output(self, device = 'EK-50:EK-50 MIDI 1'):
        """Open the output port"""
        if self.output is not None:
            self.close_output()
            self.output = None

        if device not in self.output_list():
            return False

        self.output = mido.open_output(device) # pylint: disable=no-member
        return True


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
        if not self.is_output_open():
            if not self.open_output():
                return False

        msgMsb = mido.Message('control_change', control = 0, value = msb, channel = channel)
        msgLsb = mido.Message('control_change', control = 0x20, value = lsb, channel = channel)
        msgPc = mido.Message('program_change', program = pc, channel = channel)

        self.output.send(msgMsb)
        self.output.send(msgLsb)
        self.output.send(msgPc)

        return True

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import mido as mido

class Ek50Midi:
    def __init__(self):
        """Initialize class"""
        mido.Backend('mido.backends.rtmidi')

        self.input = None
        self.inputChannel = -1

        self.output = None
        self.outputChannel = 4


    def adjust_device_list(self, devices):
        """Removes the device id from the device name"""
        ret = []

        for p in devices:
            parts = p.split()
            parts.pop()
            ret.append(' '.join(parts))

        return ret


    def output_list(self):
        """Get the names of the output devices found"""
        outputs = mido.get_output_names()
        return self.adjust_device_list(outputs)


    def input_list(self):
        """Get the names of the input devices found"""
        inputs = mido.get_input_names()
        return self.adjust_device_list(inputs)


    def valid_input_device(self, device):
        """Check if the device is an existing input device"""
        if type(device) is not str:
            return False

        return device in self.input_list()


    def valid_output_device(self, device):
        """Check if the device is an existing output device"""
        if type(device) is not str:
            return False

        return device in self.output_list()


    def valid_channel(self, channel):
        """
        Check if channel is a valid midi channel
        Note: Internally, we use channels from 0 to 15, not 1 to 16
        """
        if type(channel) is not int:
            return False

        return channel >= 0 and channel <= 15


    def open_output(self, device = 'EK-50:EK-50 MIDI 1'):
        """Open the output device"""
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
        """Check if we have the output device open"""
        return self.output is not None


    def patch_change(self, msb, lsb, pc):
        """Changes the instrument in the output device"""
        if not self.is_output_open():
            if not self.open_output():
                return False

        msgMsb = mido.Message('control_change', control = 0, value = msb, channel = self.outputChannel)
        msgLsb = mido.Message('control_change', control = 0x20, value = lsb, channel = self.outputChannel)
        msgPc = mido.Message('program_change', program = pc, channel = self.outputChannel)

        self.output.send(msgMsb)
        self.output.send(msgLsb)
        self.output.send(msgPc)

        return True

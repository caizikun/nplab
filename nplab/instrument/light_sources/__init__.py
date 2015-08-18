__author__ = 'alansanders'

from nplab.instrument import Instrument
from nplab.utils.gui import *
from PyQt4 import uic
from nplab.ui.ui_tools import UiTools
from nplab.instrument.shutter import Shutter


class LightSource(Instrument):

    def __init__(self, shutter=None):
        assert isinstance(shutter, Shutter) or shutter == None, 'invalid shutter supplied'
        super(LightSource, self).__init__()
        self.min_power = 0
        self.max_power = 1
        self.shutter = shutter

    def get_power(self):
        pass

    def set_power(self, value):
        print value

    power = property(get_power, set_power)

    def get_qt_ui(self):
        return LightSourceUI(self)


class LightSourceUI(QtGui.QWidget, UiTools):
    def __init__(self, light_source, parent=None):
        assert isinstance(light_source, LightSource), 'instrument must be a LightSource'
        self.light_source = light_source
        super(LightSourceUI, self).__init__(parent)
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'light_source.ui'), self)
        self.control_group.setTitle(self.light_source.__class__.__name__)
        self.power.setValidator(QtGui.QDoubleValidator())
        self.power.textChanged.connect(self.check_state)
        self.power.returnPressed.connect(self.update_param)
        self.power_slider.setRange(self.light_source.min_power, self.light_source.max_power)
        self.power_slider.valueChanged[int].connect(self.update_param)
        self.power_slider.sliderReleased.connect(self.update_param)
        self.set_power_button.clicked.connect(self.on_click)

        if self.light_source.shutter is not None:
            self.control_layout.addWidget(self.light_source.shutter.get_qt_ui())

    def on_click(self):
        sender = self.sender()
        if sender == self.set_power_button:
            self.power_slider.blockSignals(True)
            self.power_slider.setValue(float(self.power.text()))
            self.power_slider.blockSignals(False)
            self.light_source.power = float(self.power.text())

    def update_param(self, *args, **kwargs):
        sender = self.sender()
        index = self.senderSignalIndex()
        if sender == self.power:
            self.power_slider.blockSignals(True)
            self.power_slider.setValue(float(self.power.text()))
            self.power_slider.blockSignals(False)
            self.light_source.power = float(self.power.text())
        if sender == self.power_slider:
            if len(args) != 0:  # slider is moving and the value is changing
                value, = args
                self.power.setText(str(value))
            else:  # slider is released and signal has no arguments
                value = sender.value()
                self.light_source.power = float(self.power.text())


if __name__ == '__main__':
    import sys
    app = get_qt_app()
    ls = LightSource()
    ui = ls.get_qt_ui()
    ui.show()
    sys.exit(app.exec_())
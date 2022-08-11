import logging
import os
from slined_onboarding.common import SoPiUi
from PyQt5.QtCore import QCoreApplication, QObject, pyqtSignal
from slined_onboarding.lamp import SoLamp

class LampUi(SoPiUi):
    def __init__(self, iface_name):
        super().__init__(LampWorker(), iface_name)

    def toggle_switch(self):
        self.logger.debug('Toggle button pressed')
        if self.qr_code_shown:
            self.toggle_qr_code()

        self.logger.debug('Toggling light')
        self.event_worker.ocf_device.toggle_lamp()

    def _state_update_ui(self, device_state):
        (discovered, state, error_state, error_message) = device_state
        self.logger.debug('State update called...')
        self.logger.debug('Current state: discovered {}, state {} error_state {} error_message {}'.format(discovered, state, error_state, error_message))
        if error_state:
            self.logger.error('Error flag set')
            error_text = '<font color="red">{}</font>'.format(error_message.decode('ascii'))
            self.append_output_text(error_text)
            return
        self.img_label.set_img(self._on_img if state else self._off_img)

    def _set_buttons(self):
        super()._set_buttons()
        self.toggle_button.clicked.connect(self.toggle_switch)
        self.discover_button.setEnabled(False)

    def _retranslateUi(self):
        super()._retranslateUi()
        _translate = QCoreApplication.translate
        self.toggle_button.setText(_translate("MainWindow", "Toggle"))

class LampWorker(QObject):
    device_state = pyqtSignal(tuple)
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.ocf_device = SoLamp(os.environ.get('WPA_CTRL_IFACE'), os.environ.get('SO_LIGHTSWITCH_CREDS'), self._state_update, os.environ.get('SO_PERSIST_CREDS'))

    def run(self):
        self.logger.debug('Thread run called')
        self.ocf_device.main_event_loop()

    def stop(self):
        self.logger.debug('Stopping switch worker')
        self.ocf_device.stop_main_loop()

    def _state_update(self, discovered, state, error_state, error_message):
        self.logger.debug('State update called...')
        self.logger.debug('Current state: discovered {}, state {} error_state {} error_message {}'.format(discovered, state, error_state, error_message))
        self.device_state.emit((discovered, state, error_state, error_message))


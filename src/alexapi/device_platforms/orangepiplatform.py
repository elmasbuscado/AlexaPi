import time
import threading

from pyA20.gpio import gpio as GPIO  # pylint: disable=import-error

from .rpilikeplatform import RPiLikePlatform


class OrangepiPlatform(RPiLikePlatform):

	def __init__(self, config):
		super(OrangepiPlatform, self).__init__(config, 'orangepi', GPIO)

	def setup(self):
		GPIO.init()
		GPIO.setcfg(self._pconfig['button'], GPIO.INPUT)
		GPIO.pullup(self._pconfig['button'], GPIO.PULLUP)
		GPIO.setcfg(self._pconfig['rec_light'], GPIO.OUTPUT)
		GPIO.setcfg(self._pconfig['plb_light'], GPIO.OUTPUT)

	def after_setup(self, trigger_callback=None):

		self._trigger_callback = trigger_callback

		if self._trigger_callback:
			thread = threading.Thread(target=self.wait_for_button, args=())
			thread.daemon = True
			thread.start()

	def wait_for_button(self):
		while True:
			if GPIO.input(self._pconfig['button']) == 0:
				self.detect_button()
			time.sleep(.1)

	def cleanup(self):
		GPIO.output(self._pconfig['rec_light'], GPIO.LOW)
		GPIO.output(self._pconfig['plb_light'], GPIO.LOW)

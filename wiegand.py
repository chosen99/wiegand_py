class decoder:
    """
   Una clase para leer códigos Wiegand de una longitud arbitraria.
   Se devuelven la longitud y el valor del código.
   """

    def __init__(self, pi, gpio_0, gpio_1, callback, bit_timeout=6):

        """
      Cree una instancia con pi, gpio para 0 (cable verde), gpio para 1
      (cable blanco), la función de devolución de llamada y el tiempo de espera del bit en
      milisegundos que indica el final de un código.
      A la devolución de llamada se le pasa la longitud del código en bits y el valor.
      """

        self.pi = pi
        self.gpio_0 = gpio_0
        self.gpio_1 = gpio_1

        self.callback = callback

        self.bit_timeout = bit_timeout

        self.in_code = False

        self.pi.set_mode(gpio_0, pigpio.INPUT)
        self.pi.set_mode(gpio_1, pigpio.INPUT)

        self.pi.set_pull_up_down(gpio_0, pigpio.PUD_UP)
        self.pi.set_pull_up_down(gpio_1, pigpio.PUD_UP)

        self.cb_0 = self.pi.callback(gpio_0, pigpio.FALLING_EDGE, self._cb)
        self.cb_1 = self.pi.callback(gpio_1, pigpio.FALLING_EDGE, self._cb)

    def _cb(self, gpio, level, tick):

        """
      Acumule bits hasta que se agote el tiempo de espera de gpios 0 y 1.
      """

        if level < pigpio.TIMEOUT:

            if self.in_code == False:
                self.bits = 1
                self.num = 0

                self.in_code = True
                self.code_timeout = 0
                self.pi.set_watchdog(self.gpio_0, self.bit_timeout)
                self.pi.set_watchdog(self.gpio_1, self.bit_timeout)
            else:
                self.bits += 1
                self.num = self.num << 1

            if gpio == self.gpio_0:
                self.code_timeout = self.code_timeout & 2  # clear gpio 0 timeout
            else:
                self.code_timeout = self.code_timeout & 1  # clear gpio 1 timeout
                self.num = self.num | 1

        else:

            if self.in_code:

                if gpio == self.gpio_0:
                    self.code_timeout = self.code_timeout | 1  # timeout gpio 0
                else:
                    self.code_timeout = self.code_timeout | 2  # timeout gpio 1

                if self.code_timeout == 3:  # both gpios timed out
                    self.pi.set_watchdog(self.gpio_0, 0)
                    self.pi.set_watchdog(self.gpio_1, 0)
                    self.in_code = False
                    self.callback(self.bits, self.num)

    def cancel(self):

        """
      Cancele el decodificador Wiegand.
      """

        self.cb_0.cancel()
        self.cb_1.cancel()


if __name__ == "__main__":
    import time

    import pigpio

    import wiegand

    def callback(bits, value):
        print("bits={} value={:026b}".format(bits, value))
        card_id = int("{:026b}".format(value)[1:25], 2)
        print("Card ID: {:010d}".format(card_id))

    pi = pigpio.pi()

    w = wiegand.decoder(pi, 14, 15, callback)

    time.sleep(1000)

    w.cancel()

    pi.stop()



#----------------------------------------------------------------------------------------
# This file allows you to transform the MIDI output this script sends to the LEDs of
# buttons on your controller.
#
# PLEASE NOTE:
# This is strictly intended for use by users who understand Python.  Incorrect formatting
# or code written in this file could cause the script to stop working.
#----------------------------------------------------------------------------------------
import sys

class OutputTransformer(object):

    def log(self, message):
        sys.stderr.write("LOG: " + message.encode("utf-8"))

    def transform_output(self, button, status_byte, channel, identifier, value):
        """ This method is called when the script needs to send a MIDI message to the LED
        of a button on the controller.  Below, you can see what happens by default with
        no transformation.  The button is simply sent the same MIDI message it sends
        with the given value.

        METHOD ARGS:
        button:
            the button object, which contains the send_midi method you will need.
        status_byte:
            the status byte of the MIDI message the button sends and typically,
            but not always, receives.
        channel:
            this is unused presently.
        identifier:
            the note or CC number of the button.
        value:
            the value that the script needs to send to the LED of the button.

        SEND_MIDI ARGS:
        send_midi simply accepts a tuple containing a valid MIDI message to send.
        """

        self.log("status_byte : " + str(status_byte))
        self.log("identifier : " + str(identifier))
        self.log("value : " + str(value))
        self.log("button : " + str(button))
        self.log("channel : " + str(channel))
        
        button.send_midi((status_byte, identifier, value))

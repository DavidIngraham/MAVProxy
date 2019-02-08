#!/usr/bin/env python
'''
iridium_air Module
David Ingraham, February 2019

This modules handles an Iridium IR9523 module on an aircraft.

1. Controls modem/answers calls using AT Commands
2. Forwards essential messages and commands from autopilot to irdium module, limiting to rate of 2.4kbps
3. Forwards all received messages from iridium module to autopilot
'''

import os
import os.path
import sys
from pymavlink import mavutil
import errno
import time

from MAVProxy.modules.lib import mp_module
from MAVProxy.modules.lib import mp_util
from MAVProxy.modules.lib import mp_settings


class iridium_air(mp_module.MPModule):
    def __init__(self, mpstate):
        """Initialise module"""
        super(iridium_air, self).__init__(mpstate, "iridium_air", "")

        self.iridium_air_settings = mp_settings.MPSettings(
            [ ('verbose', bool, False),
          ])
        self.add_command('iridium_air', self.cmd_iridium_air, "iridium_air module", ['set (LOGSETTING)'])

        self.modem_port = None
        self.modem_ready = False

    def cmd_iridium_air(self, args):
        '''control behaviour of the module'''
        if len(args) == 0:
            print(self.usage())
        elif args[0] == "set":
            self.iridium_air_settings.command(args[1:])
        else:
            print(self.usage())

    def open_modem_port(self, args):
        ''' Open the Serial or Network port connected to the and initialize the modem '''
        if self.modem_port is not None:
            return False

        try:
            self.modem_port = mavutil.mavlink_connection(args)
            self.modem_ready = self.configure_modem()
            return True
        except Exception as e:
            modem_port = None
            return False

    def configure_modem(self):
        if not isinstance(self.modem_port, mavutil.mavlink_connection()):
            return False

        success = True
        # Enable Reporting
        success &= self.send_AT_command("AT+CR=1") 

        # Register with the Network
        success &= self.send_AT_command("AT+CREG=1") 

        # Configure data rates and encoding for Mobile Originated calls (shouldn't be needed) to 9600 Baud V.32
        success &= self.send_AT_command("AT+CBST=7,0,1")

        # Configure to auto-answer calls after 1 ring
        success &= self.send_AT_command("ATS0=1")

        # Unlock SIM Card
        success &= self.send_AT_command("AT+CPIN=\"2222\"")

        return success

    def send_AT_command(self, cmd, check_ack=True):
        if not isinstance(self.modem_port, mavutil.mavlink_connection()):
            return False
        try:
            command_string = string(cmd) + '\n \r'
            self.modem_port.write(command_string)

            if check_ack:
                self.modem_port.recv(3)
        except Exception as E:
            return False

        return True

    def usage(self):
        '''show help on command line options'''
        return "Usage: iridium_air <status|set>"

    def idle_task(self):
        ''' Answer Calls and forward to Autopilot here'''
        pass


def init(mpstate):
    '''initialise module'''
    return iridium_air(mpstate)

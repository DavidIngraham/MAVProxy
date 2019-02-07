#!/usr/bin/env python
'''
iridium_air Module
David Ingraham, February 2019

This modules handles an Iridium IR9523 module on an aircraft.

1. Controls modem/answers calls using AT Commands
2. Forwards essential messages and commands from autopilot to irdium module
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

    def cmd_iridium_air(self, args):
        '''control behaviour of the module'''
        if len(args) == 0:
            print(self.usage())
        elif args[0] == "set":
            self.iridium_air_settings.command(args[1:])
        else:
            print(self.usage())

    def usage(self):
        '''show help on command line options'''
        return "Usage: iridium_air <status|set>"


def init(mpstate):
    '''initialise module'''
    return iridium_air(mpstate)

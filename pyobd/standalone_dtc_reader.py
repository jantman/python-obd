#!/usr/bin/env python
###########################################################################
# odb_io.py
# 
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)
# Copyright 2009 Secons Ltd. (www.obdtester.com)
#
# This file is part of pyOBD.
#
# pyOBD is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# pyOBD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyOBD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###########################################################################

import serial
import string
import time
from math import ceil
import logging
import argparse
import sys

import obd_sensors


GET_DTC_COMMAND   = "03"
CLEAR_DTC_COMMAND = "04"
GET_FREEZE_DTC_COMMAND = "07"

FORMAT = "%(asctime)s [%(levelname)s %(filename)s:%(lineno)s - " \
         "%(name)s.%(funcName)s() ] %(message)s"
logging.basicConfig(level=logging.WARNING, format=FORMAT)
logger = logging.getLogger()


def printable_response(response):
    data = []
    s = ''
    for x in response:
        hex_repr = '%#x' % ord(x)
        data.append(hex_repr)
        # replace non-printable characters with their hex codes
        if x in string.digits or x in string.letters or x in string.punctuation:
            s += x
        else:
            s += '<%s>' % hex_repr
    return '"%s" (%s)' % (s, data)


def hex_to_int(s):
    return int(s.lower(), 16)


def decrypt_dtc_code(code):
    """Returns the 5-digit DTC code from hex encoding"""
    dtc = []
    current = code
    for i in range(0,3):
        if len(current)<4:
            raise "Tried to decode bad DTC: %s" % printable_response(code)

        tc = obd_sensors.hex_to_int(current[0]) #typecode
        tc = tc >> 2
        if   tc == 0:
            type = "P"
        elif tc == 1:
            type = "C"
        elif tc == 2:
            type = "B"
        elif tc == 3:
            type = "U"
        else:
            raise tc

        dig1 = str(obd_sensors.hex_to_int(current[0]) & 3)
        dig2 = str(obd_sensors.hex_to_int(current[1]))
        dig3 = str(obd_sensors.hex_to_int(current[2]))
        dig4 = str(obd_sensors.hex_to_int(current[3]))
        dtc.append(type+dig1+dig2+dig3+dig4)
        current = current[4:]
    return dtc


class OBDPort:
    """ OBDPort abstracts all communication with OBD-II device."""

    def __init__(self, portnum, baud=9600, timeout=4, reconn_attempts=5):
        """Initializes port by resetting device and gettings supported PIDs. """
        databits = 8
        par      = serial.PARITY_NONE  # parity
        sb       = 1                   # stop bits
        self.ELMver = "Unknown"
        # state SERIAL is 1 connected, 0 disconnected (connection failed)
        self.State = 1

        logger.info("Opening interface (serial port) %s at %s bps",
                     portnum, baud)

        try:
            self.port = serial.Serial(
                portnum, baud, parity=par, stopbits=sb, bytesize=databits,
                timeout=timeout
            )
        except serial.SerialException:
            self.State = 0
            logger.critical('Exception opening serial port', exc_info=True)
            return None

        logger.info("Interface %s successfully opened", self.port.portstr)
        logger.info("Connecting to ECU...")

        count=0
        while 1:  # until error is returned try to connect
            try:
                self.ELMver = self.send_and_get("atz")   # initialize
                logger.info("atz response: %s", printable_response(self.ELMver))
            except serial.SerialException:
                self.State = 0
                logger.critical('Exception sending "atz"', exc_info=True)
                return None
            resp = self.send_and_get("ate0")  # echo off
            logger.info("ate0 response: %s", printable_response(resp))
            logger.info('Current Protocol: %s', printable_response(self.send_and_get('ATDP')))
            logger.info('Battery Voltage: %s', printable_response(self.send_and_get('ATRV')))
            logger.info('Set protocol automatic: %s',
                        printable_response(self.send_and_get('ATSP0')))
            logger.info('Sleep 2s...')
            time.sleep(2)
            logger.info('Current Protocol: %s', printable_response(self.send_and_get('ATDP')))
            ready = self.send_and_get("0100")
            logger.info("0100 response1: '%s'", printable_response(ready))
            if ready == "BUSINIT: ...OK":
                ready = self._read_result()
                logger.info("0100 response2: %s", printable_response(ready))
                logger.info('Current Protocol: %s', printable_response(self.send_and_get('ATDP')))
                return None
            elif ready.startswith('SEARCHING...'):
                logger.info('ELM searching for protocol...')
                time.sleep(3)
                #ready = self._read_result()
                ready = self.send_and_get("0100")
                logger.info('0100 response2: %s', printable_response(ready))
                logger.info('Current Protocol: %s', printable_response(self.send_and_get('ATDP')))
                return None
            elif ready.startswith('AUTO,'):
                logger.info('ELM searching for protocol...')
                ready = self.send_and_get('0100')
                logger.info('0100 response2: %s', printable_response(ready))
                logger.info('Current Protocol: %s', printable_response(self.send_and_get('ATDP')))
                return None
            else:
                # ready=ready[-5:]
                # Expecting error message: BUSINIT:.ERROR (parse last 5 chars)
                logger.info("Connection attempt failed: %s; sleeping 5s", printable_response(ready))
                time.sleep(5)
                if count == reconn_attempts:
                    self.close()
                    self.State = 0
                    logger.critical('Reached maximum connection attempts')
                    return None
                logger.info("Connection attempt: %d", count)
                count += 1

    def close(self):
        """ Resets device and closes all associated filehandles"""
        if self.port is not None and self.State == 1:
            logger.info('Sending "atz" and closing port')
            self.send_command("atz")
            self.port.close()
        self.port = None
        self.ELMver = "Unknown"

    def send_and_get(self, cmd):
        self.send_command(cmd)
        return self._read_result()

    def send_command(self, cmd):
        """Internal use only: not a public interface"""
        self.port.flushOutput()
        self.port.flushInput()
        logger.debug('SEND: "%s"', printable_response(cmd))
        for c in cmd:
            self.port.write(c)
        self.port.write("\r\n")

    def interpret_result(self,code):
        """Internal use only: not a public interface"""
        # Code will be the string returned from the device.
        # It should look something like this:
        # '41 11 0 0\r\r'
         
        # 9 seems to be the length of the shortest valid response
        if len(code) < 7:
            logger.critical('Result: %s', printable_response(code))
            raise RuntimeError("Bogus Result: %s" % printable_response(code))

        # get the first thing returned, echo should be off
        code = string.split(code, "\r")
        code = code[0]

        #remove whitespace
        code = string.split(code)
        code = string.join(code, "")

        #cables can behave differently
        if code[:6] == "NODATA": # there is no such sensor
            return "NODATA"
        # first 4 characters are code from ELM
        code = code[4:]
        return code

    def get_result(self):
        """Internal use only: not a public interface"""
        time.sleep(0.1)
        if self.port:
            return self._read_result()
        else:
            logger.error("NO self.port!; buffer: %s", printable_response(buffer))
        return None

    def _read_result(self):
        buffer = ""
        while True:
            c = self.port.read(1)
            # logger.debug("BUFFER='%s' (%s) c='%s'", buffer,
            #             ['%x' % ord(x) for x in buffer], c)
            if c == '>' and len(buffer) > 0:
                break
            else:
                if c == '>':
                    logger.debug('Got promot character')
                if buffer != "" or c != ">":
                    # if something is in buffer, add everything
                    buffer = buffer + c
        logger.debug("RESPONSE: %s", printable_response(buffer))
        return buffer.strip("\r\n" + chr(13) + chr(12))

    # get sensor value from command
    def get_sensor_value(self, sensor):
        """Internal use only: not a public interface"""
        cmd = sensor.cmd
        logger.debug('Reading sensor %s (%s)', sensor.name.strip(), sensor.cmd)
        self.send_command(cmd)
        data = self.get_result()
        if data:
            data = self.interpret_result(data)
            if data != "NODATA":
                data = sensor.value(data)
                logger.debug('Sensor %s response: %s', sensor.cmd, data)
        else:
            return "NORESPONSE"
        return data

    # return string of sensor name and value from sensor index
    def sensor(self , sensor_index):
        """Returns 3-tuple of given sensors. 3-tuple consists of
        (Sensor Name (string), Sensor Value (string), Sensor Unit (string) ) """
        sensor = obd_sensors.SENSORS[sensor_index]
        r = self.get_sensor_value(sensor)
        logger.debug('Sensor response: name=%s unit=%s value: %s',
                     sensor.name, sensor.unit, r)
        return sensor.name, r, sensor.unit

    def sensor_names(self):
        """Internal use only: not a public interface"""
        names = []
        for s in obd_sensors.SENSORS:
            names.append(s.name)
        return names

    def get_tests_MIL(self):
        statusText=["Unsupported","Supported - Completed","Unsupported","Supported - Incompleted"]
        statusRes = self.sensor(1)[1] #GET values
        statusTrans = [] #translate values to text
        statusTrans.append(str(statusRes[0])) #DTCs
        if statusRes[1]==0: #MIL
            statusTrans.append("Off")
        else:
            statusTrans.append("On")
        for i in range(2,len(statusRes)): #Tests
            statusTrans.append(statusText[statusRes[i]])
        return statusTrans

     #
     # fixme: j1979 specifies that the program should poll until the number
     # of returned DTCs matches the number indicated by a call to PID 01
     #
    def get_dtc(self):
        """Returns a list of all pending DTC codes. Each element consists of
        a 2-tuple: (DTC code (string), Code description (string) )"""
        logger.info('Reading DTCs')
        dtcLetters = ["P", "C", "B", "U"]
        r = self.sensor(1)[1] #data
        logger.debug('DTC sensor data: %s', r)
        dtcNumber = r[0]
        mil = r[1]
        DTCCodes = []

        logger.info("Number of stored DTC: %s; MIL: %s", dtcNumber, mil)
        # get all DTC, 3 per mesg response
        for i in range(0, ((dtcNumber+2)/3)):
            res = self.send_and_get(GET_DTC_COMMAND)
            logger.info("DTC result: %s", printable_response(res))
            for i in range(0, 3):
                val1 = hex_to_int(res[3+i*6:5+i*6])
                val2 = hex_to_int(res[6+i*6:8+i*6]) #get DTC codes from response (3 DTC each 2 bytes)
                val  = (val1<<8)+val2 #DTC val as int
                if val==0: #skip fill of last packet
                  break
                DTCStr=dtcLetters[(val&0xC000)>14]+str((val&0x3000)>>12)+str(val&0x0fff)
                DTCCodes.append(["Active",DTCStr])

        #read mode 7
        logger.info('Reading Mode 7 data')
        res = self.send_and_get(GET_FREEZE_DTC_COMMAND)
        logger.debug('Mode 7 result: %s', printable_response(res))

        if res[:7] == "NO DATA": #no freeze frame
            logger.warning('No freeze frame data')
            return DTCCodes

        logger.info("DTC freeze result: %s", printable_response(res))
        for i in range(0, 3):
            val1 = hex_to_int(res[3+i*6:5+i*6])
            val2 = hex_to_int(res[6+i*6:8+i*6]) #get DTC codes from response (3 DTC each 2 bytes)
            val  = (val1<<8)+val2 #DTC val as int

            if val==0: #skip fill of last packet
                break
            DTCStr=dtcLetters[(val&0xC000)>14]+str((val&0x3000)>>12)+str(val&0x0fff)
            DTCCodes.append(["Passive",DTCStr])
        return DTCCodes

    def clear_dtc(self):
        """Clears all DTCs and freeze frame data"""
        return self.send_and_get(CLEAR_DTC_COMMAND)

    def log(self, sensor_index, filename):
        file = open(filename, "w")
        start_time = time.time()
        if file:
            data = self.sensor(sensor_index)
            file.write(
                "%s     \t%s(%s)\n" % (
                    "Time", string.strip(data[0]), data[2])
            )
            while 1:
                now = time.time()
                data = self.sensor(sensor_index)
                line = "%.6f,\t%s\n" % (now - start_time, data[1])
                file.write(line)
                file.flush()


class OBDSimpleReader(object):

    def __init__(self, port='/dev/ttyUSB0', baud=9600):
        self.port = port
        self.obd = OBDPort(self.port, baud=baud)
        logger.info('Connected to version %s', self.obd.ELMver)
        if self.obd.State == 0:
            raise RuntimeError("Can't read serial port")

    def read(self):
        logger.info('Supported PIDS: %s', self.obd.sensor(0)[1])
        print(self.obd.get_dtc())

def parse_args(argv):
    """
    parse arguments/options

    this uses the new argparse module instead of optparse
    see: <https://docs.python.org/2/library/argparse.html>
    """
    p = argparse.ArgumentParser(description='Sample python script skeleton.')
    p.add_argument('-b', '--baud', dest='baud', action='store', type=int,
                   default=9600,
                   help="Baud rate - 9600 or 38400")
    p.add_argument('-v', '--verbose', dest='verbose', action='count', default=0,
                   help='verbose output. specify twice for debug-level output.')
    p.add_argument('PORT', action='store', type=str,
                   help='serial port path')
    args = p.parse_args(argv)
    if args.baud not in [9600, 38400]:
        raise RuntimeError('Invalid baud rate')
    return args

def set_log_info():
    """set logger level to INFO"""
    set_log_level_format(logging.INFO,
                         '%(asctime)s %(levelname)s:%(name)s:%(message)s')


def set_log_debug():
    """set logger level to DEBUG, and debug-level output format"""
    set_log_level_format(
        logging.DEBUG,
        "%(asctime)s [%(levelname)s %(filename)s:%(lineno)s - "
        "%(name)s.%(funcName)s() ] %(message)s"
    )


def set_log_level_format(level, format):
    """
    Set logger level and format.

    :param level: logging level; see the :py:mod:`logging` constants.
    :type level: int
    :param format: logging formatter format string
    :type format: str
    """
    formatter = logging.Formatter(fmt=format)
    logger.handlers[0].setFormatter(formatter)
    logger.setLevel(level)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    # set logging level
    if args.verbose > 1:
        set_log_debug()
    elif args.verbose == 1:
        set_log_info()

    OBDSimpleReader(port=args.PORT, baud=args.baud).read()

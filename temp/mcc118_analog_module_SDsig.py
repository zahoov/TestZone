#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
    MCC 118 Functions Demonstrated:
        mcc118.a_in_read

    Purpose:
        Read a single data value for each channel in a loop.

    Description:
        This example demonstrates acquiring data using a software timed loop
        to read a single value from each selected channel on each iteration
        of the loop.
"""
from __future__ import print_function
from time import sleep
import datetime
from sys import stdout
from daqhats import mcc118, OptionFlags, HatIDs, HatError
from daqhats_utils import select_hat_device, enum_mask_to_string
import sys
import os

import subprocess
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN, GPIO.PUD_DOWN)

# Constants
CURSOR_BACK_2 = '\x1b[2D'
ERASE_TO_END_OF_LINE = '\x1b[0K'


def main():
    """
    This function is executed automatically when the module is run directly.
    """
    
    outDir = sys.argv[1]
    CANtype = sys.argv[2]
    truckname = sys.argv[3]
    
    options = OptionFlags.DEFAULT
    low_chan = 0
    high_chan = 7
    mcc_118_num_channels = mcc118.info().NUM_AI_CHANNELS
    sample_interval = 0.10  # Seconds

    try:
        # Ensure low_chan and high_chan are valid.
        if low_chan < 0 or low_chan >= mcc_118_num_channels:
            error_message = ('Error: Invalid low_chan selection - must be '
                             '0 - {0:d}'.format(mcc_118_num_channels - 1))
            raise Exception(error_message)
        if high_chan < 0 or high_chan >= mcc_118_num_channels:
            error_message = ('Error: Invalid high_chan selection - must be '
                             '0 - {0:d}'.format(mcc_118_num_channels - 1))
            raise Exception(error_message)
        if low_chan > high_chan:
            error_message = ('Error: Invalid channels - high_chan must be '
                             'greater than or equal to low_chan')
            raise Exception(error_message)

        # Get an instance of the selected hat device object.
        address = select_hat_device(HatIDs.MCC_118)
        hat = mcc118(address)

        print('\nMCC 118 single data value read example')
        print('    Function demonstrated: mcc118.a_in_read')
        print('    Channels: {0:d} - {1:d}'.format(low_chan, high_chan))
        print('    Options:', enum_mask_to_string(OptionFlags, options))
        #try:
        #    input("\nPress 'Enter' to continue")
        #except (NameError, SyntaxError):
        #    pass

        print('\nAcquiring data ... Press Ctrl-C to abort')

        # Display the header row for the data table.
        print('\nDate', end='')
        print('                Time', end='')
        print('             Samples/Channel', end='')
        for chan in range(low_chan, high_chan + 1):
            print('     Channel', chan, end='')
        print('')
        
        #create .txt file 
        date_time = datetime.datetime.now()
        
        outFname = outDir + truckname + "_" + '{:%Y%m%d%H}'.format(date_time) + "_" + CANtype + "_analogMeas.txt"
        if os.path.isfile(outFname):
            outF = open(outFname, "a")
        else:
            outF = open(outFname, "w")
            #create header row for .txt file
            colnames = ["Date", "Time", "Samples"]
            
            for chan in range(low_chan, high_chan + 1):
                colnames.append(str("Channel" + str(chan)))

            outF.writelines("\t".join(colnames) + "\n")

        curHr = '{:%H}'.format(date_time)
        prevHr = '{:%H}'.format(date_time)
        
        try:
            samples_per_channel = 0
            while True:
                if GPIO.input(6):
                    outF.close()
                    subprocess.call(['shutdown -h -P now "System halted by GPIO action"'], shell=True)
                    exit()

                #create new .txt file every hour 
                date_time = datetime.datetime.now()
                curHr = '{:%H}'.format(date_time)
                if (prevHr != curHr):
                    outF.close()

                    outFname = outDir + truckname + "_" + '{:%Y%m%d%H}'.format(date_time) + "_" + CANtype + "_analogMeas.txt"
                    if os.path.isfile(outFname):
                        outF = open(outFname, "a")
                    else:
                        outF = open(outFname, "w")
                        #create header row for .txt file
                        outF.writelines("#mcc118\n")
                        colnames = ["#Date", "Time", "samples"]

                        for chan in range(low_chan, high_chan + 1):
                            colnames.append(str("Channel" + str(chan)))
                        outF.writelines("\t".join(colnames) + "\n")
                    samples_per_channel = 0
                
                # Displays the time
                date_time = datetime.datetime.now()
                print('\r{:%Y-%m-%d}'.format(date_time), end='')
                print('{:    %H:%M:%S:%f}'.format(date_time)[:-3], end='')
                                
                # Display the updated samples per channel count
                samples_per_channel += 1
                print('{:20}'.format(samples_per_channel), end='')

                # Read a single value from each selected channel.
                valueL=[]
                for chan in range(low_chan, high_chan + 1):
                    value = hat.a_in_read(chan, options)
                    valueL.append(value) 
                    print('{:12.5} V'.format(value), end='')
                
                newL = [str('{:%Y-%m-%d}'.format(date_time)),
                        str('{:%H:%M:%S:%f}'.format(date_time)[:-3]),
                        str(samples_per_channel)]

                for v in range(low_chan, high_chan + 1):
                    newL.append(str(round(valueL[v],4)))
                
                outF.writelines("\t".join(newL) + "\n")
                stdout.flush()
                
                # Wait the specified interval between reads.
                sleep(sample_interval)
                prevHr = '{:%H}'.format(date_time)
                
            f.close()
            
        except KeyboardInterrupt:
            # Clear the '^C' from the display.
            print(CURSOR_BACK_2, ERASE_TO_END_OF_LINE, '\n')

    except (HatError, ValueError) as error:
        print('\n', error)


if __name__ == '__main__':
    # This will only be run when the module is called directly.
    main()

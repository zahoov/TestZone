#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
    MCC 134 Functions Demonstrated:
        mcc134.t_in_read

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
from daqhats import mcc134, HatIDs, HatError, TcTypes
from daqhats_utils import select_hat_device, tc_type_to_string

# Constants
CURSOR_BACK_2 = '\x1b[2D'
ERASE_TO_END_OF_LINE = '\x1b[0K'


def main():
    """
    This function is executed automatically when the module is run directly.
    """
    tc_type = TcTypes.TYPE_K   # change this to the desired thermocouple type
    delay_between_reads = 1  # Seconds
    channels = (0, 1, 2, 3)

    try:
        # Get an instance of the selected hat device object.
        address = select_hat_device(HatIDs.MCC_134)
        hat = mcc134(address)

        for channel in channels:
            hat.tc_type_write(channel, tc_type)

        print('\nMCC 134 single data value read example')
        print('    Function demonstrated: mcc134.t_in_read')
        print('    Channels: ' + ', '.join(str(channel) for channel in channels))
        print('    Thermocouple type: ' + tc_type_to_string(tc_type))
        #try:
        #    input("\nPress 'Enter' to continue")
        #except (NameError, SyntaxError):
        #    pass

        print('\nAcquiring data ... Press Ctrl-C to abort')

        # Display the header row for the data table.
        print('\nDate', end='')
        print('                Time', end='')
        print('             Samples/Channel', end='')
        for channel in channels:
            print('     Channel', channel, end='')
        print('')
        
        #create .txt file 
        date_time = datetime.datetime.now()
        f = open('/home/pi/Desktop/PiDAQ/out/' + '{:%Y-%m-%d_%H:%M:%S}'.format(date_time) + "_thermoc_meas.txt", "w+")
        #create header row for .txt file
        f.write("Date" + "\t" + "Time" + "\t" + "Samples" + "\t") 
        for channel in channels:
            f.write(str("Channel" + str(channel) + "\t"))

        curHr = '{:%H}'.format(date_time)
        prevHr = '{:%H}'.format(date_time)
        

        try:
            samples_per_channel = 0
            while True:
                
                #create new .txt file every hour 
                date_time = datetime.datetime.now()
                curHr = '{:%H}'.format(date_time)
                if (prevHr != curHr):
                    f.close()
                    f = open('/home/pi/Desktop/PiDAQ/out/' + '{:%Y-%m-%d_%H:%M:%S}'.format(date_time) + "_thermoc_meas.txt", "w+")
                    #create header row for .txt file
                    f.write("Date" + "\t" + "Time" + "\t" + "Samples" + "\t") 
                    for channel in channels:
                        f.write(str("Channel" + str(channel) + "\t"))
                    samples_per_channel = 0
                                               
                # Displays the time
                date_time = datetime.datetime.now()
                print('\r{:%Y-%m-%D}'.format(date_time), end='')
                print('{:    %H:%M:%S:%f}'.format(date_time)[:-3], end='')
                
                # Display the updated samples per channel count
                samples_per_channel += 1
                print('{:20d}'.format(samples_per_channel), end='')

                # Read a single value from each selected channel.
                valueL=[]
                for channel in channels:
                    value = hat.t_in_read(channel)
                    valueL.append(value) 
                    if value == mcc134.OPEN_TC_VALUE:
                        print('     Open     ', end='')
                    elif value == mcc134.OVERRANGE_TC_VALUE:
                        print('     OverRange', end='')
                    elif value == mcc134.COMMON_MODE_TC_VALUE:
                        print('   Common Mode', end='')
                    else:
                        print('{:12.2f} C'.format(value), end='')
                
                f.write(str('\r{:%Y-%m-%d}'.format(date_time)) + "\t" + \
                str('{:    %H:%M:%S:%f}'.format(date_time)[:-3]) + "\t" + \
                str(samples_per_channel) + "\t")    
                for channel in channels:
                    f.write(str(round(valueL[channel],4)) + "\t")
                
                stdout.flush()

                # Wait the specified interval between reads.
                sleep(delay_between_reads)
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

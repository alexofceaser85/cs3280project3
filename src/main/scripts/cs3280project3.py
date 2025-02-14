#!/usr/bin/env python3

"""
This is the main method for the port scanner
"""
import sys
import multiprocessing
import scan_utils

__author__ = 'Alex DeCesare'
__version__ = '30-October-2020'

def get_ip_address():

    """
    Gets the ip address from the command line arguments
    """

    try:
        return sys.argv[1]
    except IndexError:
        print('Please include an ip address')
        return None

def get_start_port():

    """
    Gets the start port from the command line arguments
    """

    try:
        return int(sys.argv[2])
    except IndexError:
        print('Please include a starting port')
        return None
    except ValueError:
        print('There is an invalid value for the starting port, please only include integers')
        return None

def get_end_port():

    """
    Gets the end port from the command line arguments and add one to it,
    if there is no end port then return the start port plus one. This is
    needed for the range function in the scan method
    """

    try:
        return int(sys.argv[3]) + 1
    except IndexError:
        return int(sys.argv[2]) + 1
    except ValueError:
        print('There is an invalid value for the ending port, please only include integers')
        return None


def handle_scan_connection(ip_address, start_port, end_port, connection):
    """
    Gets the parameters for the scan function, calls the scan function, and sends the output of
    the scan function to the main method via a pipe. If the any of the parameters are equal to
    None then the function does not call the scan function and sends a None type to the main method
    """

    if ip_address is not None and start_port is not None:
        scanned_ports = scan_utils.scan(ip_address, start_port, end_port)
        connection.send(scanned_ports)
    else:
        connection.send(None)

if __name__ == '__main__':
    PARENT_CONNECTION, CHILD_CONNECTION = multiprocessing.Pipe()
    PROCESS_ARGUMENTS = (get_ip_address(), get_start_port(), get_end_port(), CHILD_CONNECTION, )
    PROCESSES = multiprocessing.Process(target=handle_scan_connection, args=(PROCESS_ARGUMENTS))
    PROCESSES.start()
    PROCESSES.join()
    OUTPUT = PARENT_CONNECTION.recv()
    print(OUTPUT)

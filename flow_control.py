#!/usr/bin/python3

from argparse import ArgumentParser
import bisect
import os
import sys
import time

"""Represents a simulation of flow control"""
class Simulation:
    def __init__(self, settings):
        self._settings = settings

    def step(self, t):

        # TODO

        return NetworkState(t, [], [], [], [])

"""Represents the state of the network after a given time step"""
class NetworkState:
    """The state of the network"""
    def __init__(self, t, sendbuf, recvbuf, torecv, tosend):
        self._t = t
        self._sendbuf = sendbuf
        self._recvbuf = recvbuf
        self._torecv = torecv
        self._tosend = tosend
        return

    """Format the state of the network in a way that displays nicely for an
    animation"""
    def display(self, settings):
        parts = []

        parts.append(('= %d ' % self._t).ljust(80, '='))

        left = "SENDER"
        right = "RECEIVER"
        parts.append(left + right.rjust(80 - len(left)))

        string = "%s" % self._sendbuf
        parts.append(string)
        string = "%s" % self._recvbuf
        parts.append(string.rjust(80))

        for pkt in self._torecv:
            string = '- Data[%d] -->' % pkt[1]
            percent = 1 - ((pkt[0] - self._t) / settings.delay)
            parts.append(''.rjust(int(percent * 80), '-') + string)
        parts.extend([''] * (settings.recvbuf - len(self._torecv)))

        for pkt in self._tosend:
            string = '<-- ACK[%d,win=%d] -' % (pkt[1], pkt[2])
            percent = (pkt[0] - self._t) / settings.delay
            parts.append(string.rjust(int(percent * 80)).ljust(80, '-'))

        return '\n'.join(parts)

    """Format the state in a way that provides a raw dump of the state"""
    def __str__(self):
        return '%d;%s;%s;%s;%s' % (self._t, self._sendbuf, self._recvbuf, 
                self._torecv, self._tosend)

def main():
    # Parse arguments
    arg_parser = ArgumentParser(description='Flow control simulator')
    arg_parser.add_argument('--data', dest='data', action='store',
            type=int, default=6, help='Number of data packets')
    arg_parser.add_argument('--delay', dest='delay', action='store',
            type=int, default=3, help='One-way delay')
    arg_parser.add_argument('--sendbuf', dest='sendbuf', action='store',
            type=int, default=3, help="Sender's buffer capacity")
    arg_parser.add_argument('--recvbuf', dest='recvbuf', action='store',
            type=int, default=3, help="Receiver's buffer capacity")
    arg_parser.add_argument('--prodrate', dest='prodrate', action='store',
            type=int, default=3, help="Rate at which sender produces data")
    arg_parser.add_argument('--consrate', dest='consrate', action='store',
            type=int, default=3, help="Rate at which receiver consumes data")
    arg_parser.add_argument('--steps', dest='steps', action='store',
            type=int, default=10, help="How many time steps to simulate")
    arg_parser.add_argument('--speed', dest='speed', action='store',
            type=float, default=-1, help="Speed at which to display")
    settings = arg_parser.parse_args()

    # Create simulation
    simulation = Simulation(settings)

    # Run simulation for specified number of steps
    for t in range(settings.steps):
        state = simulation.step(t)

        # Display animation or raw output
        if (settings.speed > 0):
            os.system('clear')
            print('%s\n' % state.display(settings))
            time.sleep(settings.speed)
        else:
            print('%s' % state)

if __name__ == '__main__':
    main()

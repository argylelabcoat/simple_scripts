#!/usr/bin/python3
import random

LocalBit = 2
Unicast = 0xFE

def randomOctet():
    return random.randrange(0x00,0xFF)

def randomMac():
    octets = [ randomOctet() for i in range(6) ]
    
    octets[0] |= LocalBit
    octets[0] &= Unicast

    return octets

octets = randomMac()
hex = ['{:02X}'.format(a) for a in octets]
# Print for Arduino/C:
print("{ %s }"%','.join('0x'+a for a in hex))
# Print with colons:
print(':'.join(hex))
# Print with hypens:
print('-'.join(hex))
# Dotted:
dotted = '.'.join([hex[a]+hex[a+1] for a in range(0,6,2)])
print(dotted)


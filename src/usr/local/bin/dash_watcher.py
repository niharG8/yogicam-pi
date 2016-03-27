#!/usr/bin/env python

import socket
import struct
import binascii
import pigpio

DASH_MAC = "7475482056cf"
TGT_PIN = 25  # TODO: don't hardcode this

def eventloop(pi):
    rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
    while True:
        packet = rawSocket.recvfrom(2048)
        ethernet_header = packet[0][0:14]
        ethernet_detailed = struct.unpack("!6s6s2s", ethernet_header)
        arp_header = packet[0][14:42]
        arp_detailed = struct.unpack("2s2s1s1s2s6s4s6s4s", arp_header)
        # skip non-ARP packets
        ethertype = ethernet_detailed[2]
        if ethertype != "\x08\x06":
            continue
        source_mac = binascii.hexlify(arp_detailed[5])
        dest_ip = socket.inet_ntoa(arp_detailed[8])
        if source_mac == DASH_MAC:  
            toggle_pin(pi, TGT_PIN)

def toggle_pin(pi, pin_bcm):
    """Toggle the digital state of a given GPIO pin in BCM numbering"""
    pi.set_mode(TGT_PIN, pigpio.OUTPUT)
    pin_status = ( pi.read_bank_1() & ( 1 << pin_bcm ) ) != 0  # True for pin HIGH 
    pi.write(pin_bcm, int(not pin_status)) 

def main():
    pi = pigpio.pi()
    eventloop(pi)

main()

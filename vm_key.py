#!/usr/bin/env python3
#coding: utf-8

'''vm_key.py'''

import argparse
import atexit
import socket
import sys
from pyVim import connect
from pyVmomi import vim

# Source : https://gist.github.com/MightyPork/6da26e382a7ad91b5496ee55fdc73db2
# Description HIDCode : ('KEY_NAME', 'HEX_CODE', [('VALUE1', [ 'MODIFIER1', 'MODIFIER2', ... ]), ('VALUE2', [ 'MODIFIER1', 'MODIFIER2', ... ]), ... ])
HIDCODE = [
        ('KEY_A', '0x04', [('a', []), ('A', ['KEY_LEFTSHIFT'])]),
        ('KEY_B', '0x05', [('b', []), ('B', ['KEY_LEFTSHIFT'])]),
        ('KEY_C', '0x06', [('c', []), ('C', ['KEY_LEFTSHIFT'])]),
        ('KEY_D', '0x07', [('d', []), ('D', ['KEY_LEFTSHIFT'])]),
        ('KEY_E', '0x08', [('e', []), ('E', ['KEY_LEFTSHIFT'])]),
        ('KEY_F', '0x09', [('f', []), ('F', ['KEY_LEFTSHIFT'])]),
        ('KEY_G', '0x0a', [('g', []), ('G', ['KEY_LEFTSHIFT'])]),
        ('KEY_H', '0x0b', [('h', []), ('H', ['KEY_LEFTSHIFT'])]),
        ('KEY_I', '0x0c', [('i', []), ('I', ['KEY_LEFTSHIFT'])]),
        ('KEY_J', '0x0d', [('j', []), ('J', ['KEY_LEFTSHIFT'])]),
        ('KEY_K', '0x0e', [('k', []), ('K', ['KEY_LEFTSHIFT'])]),
        ('KEY_L', '0x0f', [('l', []), ('L', ['KEY_LEFTSHIFT'])]),
        ('KEY_M', '0x10', [('m', []), ('M', ['KEY_LEFTSHIFT'])]),
        ('KEY_N', '0x11', [('n', []), ('N', ['KEY_LEFTSHIFT'])]),
        ('KEY_O', '0x12', [('o', []), ('O', ['KEY_LEFTSHIFT'])]),
        ('KEY_P', '0x13', [('p', []), ('P', ['KEY_LEFTSHIFT'])]),
        ('KEY_Q', '0x14', [('q', []), ('Q', ['KEY_LEFTSHIFT'])]),
        ('KEY_R', '0x15', [('r', []), ('R', ['KEY_LEFTSHIFT'])]),
        ('KEY_S', '0x16', [('s', []), ('S', ['KEY_LEFTSHIFT'])]),
        ('KEY_T', '0x17', [('t', []), ('T', ['KEY_LEFTSHIFT'])]),
        ('KEY_U', '0x18', [('u', []), ('U', ['KEY_LEFTSHIFT'])]),
        ('KEY_V', '0x19', [('v', []), ('V', ['KEY_LEFTSHIFT'])]),
        ('KEY_W', '0x1a', [('w', []), ('W', ['KEY_LEFTSHIFT'])]),
        ('KEY_X', '0x1b', [('x', []), ('X', ['KEY_LEFTSHIFT'])]),
        ('KEY_Y', '0x1c', [('y', []), ('Y', ['KEY_LEFTSHIFT'])]),
        ('KEY_Z', '0x1d', [('z', []), ('Z', ['KEY_LEFTSHIFT'])]),
        ('KEY_1', '0x1e', [('1', []), ('!', ['KEY_LEFTSHIFT'])]),
        ('KEY_2', '0x1f', [('2', []), ('@', ['KEY_LEFTSHIFT'])]),
        ('KEY_3', '0x20', [('3', []), ('#', ['KEY_LEFTSHIFT'])]),
        ('KEY_4', '0x21', [('4', []), ('$', ['KEY_LEFTSHIFT'])]),
        ('KEY_5', '0x22', [('5', []), ('%', ['KEY_LEFTSHIFT'])]),
        ('KEY_6', '0x23', [('6', []), ('^', ['KEY_LEFTSHIFT'])]),
        ('KEY_7', '0x24', [('7', []), ('&', ['KEY_LEFTSHIFT'])]),
        ('KEY_8', '0x25', [('8', []), ('*', ['KEY_LEFTSHIFT'])]),
        ('KEY_9', '0x26', [('9', []), ('(', ['KEY_LEFTSHIFT'])]),
        ('KEY_0', '0x27', [('0', []), (')', ['KEY_LEFTSHIFT'])]),
        ('KEY_ENTER', '0x28', [('', [])]),
        ('KEY_ESC', '0x29', [('', [])]),
        ('KEY_BACKSPACE', '0x2a', [('', [])]),
        ('KEY_TAB', '0x2b', [('', [])]),
        ('KEY_SPACE', '0x2c', [(' ', [])]),
        ('KEY_MINUS', '0x2d', [('-', []), ('_', ['KEY_LEFTSHIFT'])]),
        ('KEY_EQUAL', '0x2e', [('=', []), ('+', ['KEY_LEFTSHIFT'])]),
        ('KEY_LEFTBRACE', '0x2f', [('[', []), ('{', ['KEY_LEFTSHIFT'])]),
        ('KEY_RIGHTBRACE', '0x30', [(']', []), ('}', ['KEY_LEFTSHIFT'])]),
        ('KEY_BACKSLASH', '0x31', [('\\', []), ('|', ['KEY_LEFTSHIFT'])]),
        ('KEY_SEMICOLON', '0x33', [(';', []), (':', ['KEY_LEFTSHIFT'])]),
        ('KEY_APOSTROPHE', '0x34', [('\'', []), ('"', ['KEY_LEFTSHIFT'])]),
        ('KEY_GRAVE', '0x35', [('`', []), ('~', ['KEY_LEFTSHIFT'])]),
        ('KEY_COMMA', '0x36', [(',', []), ('<', ['KEY_LEFTSHIFT'])]),
        ('KEY_DOT', '0x37', [('.', []), ('>', ['KEY_LEFTSHIFT'])]),
        ('KEY_SLASH', '0x38', [('/', []), ('?', ['KEY_LEFTSHIFT'])]),
        ('KEY_CAPSLOCK', '0x39', []),
        ('KEY_F1', '0x3a', [('', [])]),
        ('KEY_F2', '0x3b', [('', [])]),
        ('KEY_F3', '0x3c', [('', [])]),
        ('KEY_F4', '0x3d', [('', [])]),
        ('KEY_F5', '0x3e', [('', [])]),
        ('KEY_F6', '0x3f', [('', [])]),
        ('KEY_F7', '0x40', [('', [])]),
        ('KEY_F8', '0x41', [('', [])]),
        ('KEY_F9', '0x42', [('', [])]),
        ('KEY_F10', '0x43', [('', [])]),
        ('KEY_F11', '0x44', [('', [])]),
        ('KEY_F12', '0x45', [('', [])]),
        ('KEY_DELETE', '0x4c', [('', [])]),
        ('CTRL_ALT_DEL', '0x4c', [('', ['CTRL', 'ALT'])]),
        ('CTRL_C', '0x06', [('', ['CTRL'])]),
    ]

def key_to_hid(input_key):
    '''Convert KEY to HID'''
    for key, code, values in HIDCODE:
        if input_key == key:
            key, modifiers = values[0]
            return code, modifiers
    return False

def character_to_hid(char):
    '''Convert CHARACTER to HID'''
    for code, values in HIDCODE[1:]:
        for word, modifiers in values:
            if char == word:
                return code, modifiers
    return False

def hid_to_hex(hid):
    '''Convert HID to HEX'''
    return int(hid, 16) << 16 | 7

def key_stroke(virtual_machine, hid, debug=False):
    '''Sent KEYSTROKE to VIRTUAL MACHINE'''
    code, modifiers = hid
    tmp = vim.UsbScanCodeSpecKeyEvent()
    modifier = vim.UsbScanCodeSpecModifierType()
    if "KEY_LEFTSHIFT" in modifiers:
        modifier.leftShift = True
    if "KEY_RIGHTALT" in modifiers:
        modifier.rightAlt = True
    if "CTRL" in modifiers:
        modifier.leftControl = True
    if "ALT" in modifiers:
        modifier.leftAlt = True
    tmp.modifiers = modifier
    tmp.usbHidCode = hid_to_hex(code)
    inject_hid = vim.UsbScanCodeSpec()
    inject_hid.keyEvents = [tmp]
    virtual_machine.PutUsbScanCodes(inject_hid)
    if debug:
        print("Send : Keystroke: { code: %s, modifiers: %s } on VM : %s" % (code, modifiers, virtual_machine.name))

def get_vm(arguments):
    '''Get VIRTUAL MACHINE'''
    try:
        virtual_machine = None
        socket.setdefaulttimeout(arguments.timeout)
        esxi = connect.SmartConnectNoSSL(host=arguments.host, user=arguments.username, pwd=arguments.password, port=arguments.port)
        atexit.register(connect.Disconnect, esxi)
        entity_stack = esxi.content.rootFolder.childEntity
        while entity_stack:
            entity = entity_stack.pop()
            if entity.name == arguments.virtual_machine:
                virtual_machine = entity
                del entity_stack[0:len(entity_stack)]
                return virtual_machine
            if hasattr(entity, 'childEntity'):
                entity_stack.extend(entity.childEntity)
            if isinstance(entity, vim.Datacenter):
                entity_stack.append(entity.vmFolder)
        if not isinstance(virtual_machine, vim.VirtualMachine):
            msg = "Virtual Machine %s not found." % arguments.virtual_machine
            sys.exit(msg)
    except vim.fault.InvalidLogin:
        msg = "Cannot complete login due to an incorrect user name or password."
        sys.exit(msg)
    except socket.timeout as exception:
        msg = "Unable to connect to %s:%s (%s)" % (arguments.host, arguments.port, exception)
        sys.exit(msg)
    except socket.gaierror as exception:
        msg = "Unable to resolve %s (%s)" % (arguments.host, exception)
        sys.exit(msg)

def args():
    '''Get ARGS'''
    parser = argparse.ArgumentParser(description="VM keystrokes using the vSphere API")
    parser.add_argument('host', help="vSphere IP or Hostname")
    parser.add_argument('username', help="vSphere Username")
    parser.add_argument('password', help="vSphere Password")
    parser.add_argument('virutal_machine', help="VM Name")
    parser.add_argument('--port', type=int, default=443, help="alternative TCP port to communicate with vSphere API (default: 443)")
    parser.add_argument('--timeout', type=int, default=10, help="timeout for VSphere API connection (default: 10s)")
    parser.add_argument('--debug', action='store_true', help="Enable debug mode")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--key', type=str, choices=[key[0] for key in HIDCODE], help="key to passed to VM")
    group.add_argument('--string', type=str, help="string to passed to VM (Standard ASCII characters only)")
    return parser.parse_args()

if __name__ == "__main__":
    ARGS = args()
    VIRTUAL_MACHINE = get_vm(ARGS)
    if ARGS.key:
        key_stroke(VIRTUAL_MACHINE, key_to_hid(ARGS.key), debug=ARGS.debug)
        print("Send : Key: [%s] on VM : %s" % (ARGS.key, VIRTUAL_MACHINE.name))
    if ARGS.string:
        for character in list(ARGS.string):
            key_stroke(VIRTUAL_MACHINE, character_to_hid(character), debug=ARGS.debug)
        print("Send : String: [%s] on VM : %s" % (ARGS.string, VIRTUAL_MACHINE.name))

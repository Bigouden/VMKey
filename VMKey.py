#!/usr/bin/python
#coding: utf-8

import argparse
import atexit
import socket
import sys
from pyVim import connect
from pyVmomi import vim

# Source : https://gist.github.com/MightyPork/6da26e382a7ad91b5496ee55fdc73db2
# Description HIDCode : ('KEY_NAME', 'HEX_CODE', [('VALUE1', [ 'MODIFIER1', 'MODIFIER2', ... ]), ('VALUE2', [ 'MODIFIER1', 'MODIFIER2', ... ]), ... ])
HIDCode = [
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

def KEY2HID(char):
    for key, code, values in HIDCode:
        if char == key:
            key, modifiers = values[0]
            return code, modifiers

def CHAR2HID(char, args):
    for key, code, values in HIDCode:
        for key, modifiers in values:
            if char == key:
                return code, modifiers

def HID2HEX(hid):
    return (int(hid, 16) << 16 | 0007)

def Keystroke(vm, (code, modifiers), args):
    tmp = vim.UsbScanCodeSpecKeyEvent()
    m = vim.UsbScanCodeSpecModifierType()
    if "KEY_LEFTSHIFT" in modifiers:
        m.leftShift = True
    if "KEY_RIGHTALT" in modifiers:
        m.rightAlt = True
    if "CTRL" in modifiers:
        m.leftControl = True
    if "ALT" in modifiers:
        m.leftAlt = True
    tmp.modifiers = m
    tmp.usbHidCode = HID2HEX(code)
    sp = vim.UsbScanCodeSpec()
    sp.keyEvents = [tmp]
    vm.PutUsbScanCodes(sp)
    if args.debug:
        print("Send : Keystroke: { code: %s, modifiers: %s } on VM : %s" % (code, modifiers, vm.name))

def getVM(args):
    try:
        vm = None
        socket.setdefaulttimeout(args.timeout)
        esxi = connect.SmartConnectNoSSL(host=args.host, user=args.username, pwd=args.password, port=args.port)
        atexit.register(connect.Disconnect, esxi)
        entity_stack = esxi.content.rootFolder.childEntity
        while entity_stack:
            entity = entity_stack.pop()
            if entity.name == args.vm:
                vm = entity
                del entity_stack[0:len(entity_stack)]
                return vm
            elif hasattr(entity, 'childEntity'):
                entity_stack.extend(entity.childEntity)
            elif isinstance(entity, vim.Datacenter):
                entity_stack.append(entity.vmFolder)
        if not isinstance(vm, vim.VirtualMachine):
            msg =  "Virtual Machine %s not found." % args.vm
            sys.exit(msg)
    except vim.fault.InvalidLogin as e:
        msg = "Cannot complete login due to an incorrect user name or password."
        sys.exit(msg)
    except socket.timeout as e:
        msg = "Unable to connect to %s:%s (%s)" % (args.host, args.port, e)
        sys.exit(msg)
    except socket.gaierror as e:
        msg = "Unable to resolve %s (%s)" % (args.host, e)
        sys.exit(msg)
    except Exception as e:
        sys.exit(e)

def args():
    parser = argparse.ArgumentParser(description="VM keystrokes using the vSphere API")
    parser.add_argument('host', help="vSphere IP or Hostname")
    parser.add_argument('username', help="vSphere Username")
    parser.add_argument('password', help="vSphere Password")
    parser.add_argument('vm', help="VM Name")
    parser.add_argument('--port', type=int, default=443, help="alternative TCP port to communicate with vSphere API (default: 443)")
    parser.add_argument('--timeout', type=int, default=10, help="timeout for VSphere API connection (default: 10s)")
    parser.add_argument('--debug', action='store_true', help="Enable debug mode")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--key', type=str, choices=[ key[0] for key in HIDCode], help="key to passed to VM")
    group.add_argument('--string', type=unicode, help="string to passed to VM (Standard ASCII characters only)")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = args()
    vm = getVM(args)
    if args.key:
        Keystroke(vm, KEY2HID(args.key), args)
        print("Send : Key: [%s] on VM : %s" % (args.key, vm.name))
    if args.string:
        for char in list(args.string):
            Keystroke(vm, CHAR2HID(char, args), args)
        print("Send : String: [%s] on VM : %s" % (args.string, vm.name))

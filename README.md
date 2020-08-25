# VMKey
vm_key.py is an usefull tool write in Python to send keystrokes on VMware virtual machine throught vSphere API.

__Requirements__

- vSphere 6.5 or higher
- argparse
- pyvmomi

__Usage__

```
vm_key.py -h

positional arguments:

host                  vSphere IP or Hostname
username              vSphere Username
password              vSphere Password
virtual_machine       VM Name

optional arguments:

-h, --help            show this help message and exit
--port PORT           alternative TCP port to communicate with vSphere API (default: 443)
--timeout TIMEOUT     timeout for VSphere API connection (default: 10s)
--debug               enable debug mode
--key                 key to passed to VM
--string STRING       string to passed to VM (Standard ASCII characters only)
```

__Examples__

```
vm_key.py host username password virtual_machine --string "Hello World !"
vm_key.py host username password virtual_machine --key CTRL_ALT_DEL
```

__Notes__

Available keys are listed in HIDCode variable.

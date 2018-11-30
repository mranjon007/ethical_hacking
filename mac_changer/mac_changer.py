#!/user/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("--i", "--interface", dest="interface", help = "Interface to change it's MAC address")
    parser.add_option("--m", "--mac", dest="new_mac", help = "New mac address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use   --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify an mac address, use --help for more info")
    return options


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode('utf-8')
    mac_address_search_result = re.search("\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] could not read mac address")


def change_mac(interface, mac_address):
    print("[+] changing " + interface + "  interface mac address to " + mac_address)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac_address])
    subprocess.call(["ifconfig", interface, "up"])


options = get_arguments()
current_mac = get_current_mac(options.interface)
print("current mac: "+str(current_mac))
change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] Mac address was successfully changed to "+current_mac)
else:
    print("[-] Mac address didn't get changed")






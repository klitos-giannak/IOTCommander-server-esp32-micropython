This is an implementation of the IOT Commander service targeting an esp32 microcontroller running micropython. It has not been through limited testing with an esp32 but it might work with other microcontrollers as well. Please let us know of results in case you try it.
Please find more information about IOT Commander functionality in its [sibling CPython project](https://github.com/klitos-giannak/IOTCommander-server-python)

There are slight differences in this micropython version. In the [config file](commands_config.json) configuration file, there is no "shell_command",but rather an "execute" field for each command. The value of this field points to a method inside the [executables.py](executables.py) file. These methods should be the trigger points for your special ESP32 functionality.

Steps:
1. First of all make sure your esp32 can connect to your WIFI network.
You can do so by adding the following code to 'boot.py' file:

```python
def connect_wifi(essid, password):
    import time
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(essid, password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

    
def connect():
    wifi_ssid = 'YOUR-WIFI-SSID'
    wifi_password = 'YOUR-WIFI-PASSWORD'
    connect_wifi(wifi_ssid, wifi_password)
    
connect()
```

2. Copy all the project files(except [commands_config.json](commands_config.json) and [executables.py](executables.py)) inside your ESP32 root directory. Please be careful with [main.py](main.py) in case you already have other functionality in it. In this case please append the contents of [main.py](main.py) to your main file.
3. Make the necessary changes to [commands_config.json](commands_config.json). Here is your IOTCommander configuration. Configure your IOT's commands based on the functionality you need.
4. Make the necessary changes to [executables.py](executables.py) according to your commands_config.json. The functions mentioned inside the config file need to exist inside the executables file. Inside these functions call your special IOT functionality

At this point you should be done. Power up your ESP32 and give it a moment to boot. If you haven't done already, download [the IOT Commander client app](https://play.google.com/store/apps/details?id=mobi.duckseason.iotcommander), make sure your phone is on the same network as your microcontroller and open the client app. Your device should appear within the app and it will advertise it's functionality.

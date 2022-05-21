This is an implementation of the IOT Commander service targeting an esp32 microcontroller running micropython. Please find more information about IOT Commander in its [sibling CPython project](https://github.com/klitos-giannak/IOTCommander-server-python)


To enable further functionality please make sure your esp32 can connect to your WIFI network.
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

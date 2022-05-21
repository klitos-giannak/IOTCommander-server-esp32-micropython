# This is IOT Commander Discover service

import machine
import ubinascii

running = False
    
def parse_broadcast_message(to_parse):
    """Parse the given string as a json and return a dictionary with the json's contents"""
    
    import json
    try:
        decoded = json.loads(to_parse)
        if decoded is not None:
            return decoded
    except ValueError:
        # this is a JSONDecodeError, but we are catching superclass for backwards compatibility
        return None

    
def start():
    global running
    if running:
        return
    else:
        running = True
    
    PORT_TO_BIND = 9977
    
    machine_id = ubinascii.hexlify(machine.unique_id()).decode()
    discover_response = '{"deviceName":"micro-' + machine_id + '"}'
    
    print('Starting Broadcast service')
    import socket
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    broadcast_socket.bind(socket.getaddrinfo("0.0.0.0", PORT_TO_BIND)[0][-1])
    broadcast_socket.setblocking(0)
    
    import select
    poll = select.poll()
    poll.register(broadcast_socket, select.POLLIN)
    
    import uasyncio
    async def loop():
        while running: 
            events = poll.poll(1) #milliseconds
            if not events:
                await uasyncio.sleep(2) #seconds
                continue # todo async wait?
            print('got it')
            if broadcast_socket == events[0][0]:
                (message, address) = broadcast_socket.recvfrom(1024)
                decoded_message = message.decode().rstrip('\n')
                ip = str(address[0])
                port = str(address[1])
                print("In <-" + ip + ":" + port + " : " + decoded_message)

                parsed_message = parse_broadcast_message(decoded_message)

                if parsed_message is not None:
                    if parsed_message['action'] == "discover":
                        print('action "discover" found. Responding...')
                        outgoing_message = discover_response.encode()
                        broadcast_socket.sendto(outgoing_message, address)
                        print("Out -> " + ip + ":" + port + " : " + discover_response)

        poll.unregister(broadcast_socket)
        broadcast_socket.close()
        print("\nBroadcast Serveice stopped\n")
        
    import _thread
    _thread.start_new_thread(uasyncio.run, (loop(),))
    print("Broadcast Service started: listening to port " + str(PORT_TO_BIND) + "\n")
    

def stop():
    global running
    running = False
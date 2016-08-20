#! /usr/bin/env python

import socket
import struct
import json

def main():
    controller = Controller()
    controller.start()

class Connection:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', 8081))
    def receive_message(self):
        data = self.sock.recv(2)
        size = struct.unpack('!h', data)[0]
        data = self.sock.recv(size)
        return json.loads(data)
    def send_message(self, message):
        json_str = json.dumps(message)
        packed_message = struct.pack('!' + str(len(json_str)) + 's', json_str)
        packed_size = struct.pack('!h', len(packed_message))
        self._send_data(packed_size)
        self._send_data(packed_message)
    def _send_data(self, data):
        bytes_sent = 0
        while bytes_sent < len(data):
            bytes_sent += self.sock.send(data[bytes_sent:])

class Controller:
    def __init__(self):
        self._connection = Connection()
        self._action_id = 0
    def start(self):
        while True:
            event = self._connection.receive_message()
            self._process_event(event)
    def _process_event(self, event):
        if event['type'] == 'carRequested':
            description = event['description']
            self._send_car(0, description['floor'], 'up')
    def _send_car(self, car, floor, next_direction):
        action = {}
        action['type'] = 'sendCar'
        action['id'] = self._action_id
        self._action_id += 1

        params = {}
        params['car'] = car
        params['floor'] = floor
        params['nextDirection'] = next_direction

        action['params'] = params

        self._connection.send_message(action)

if __name__ == '__main__':
    main()

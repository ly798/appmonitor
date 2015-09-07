#!/usr/bin/env python
# coding: utf8
import socket
import time
import signal


# Define signal handler function
def TimeOutHandler(signum, frame):
    raise Exception


class SocketIoChannel:
    def __init__(self, cmd, server_address='/tmp/qga.sock'):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server_address = server_address
        self.sock.connect(self.server_address)
        self.cmd = cmd
        self._buf = ''

    def read_buf(self):
        buf = self.sock.recv(4096)
        if buf:
            self._buf += buf
        else:
            time.sleep(1)

    def _readline(self):
        newline = self._buf.find('\n\r')
        while newline < 0:
            self.read_buf()
            newline = self._buf.find('\n\r')
        if newline >= 0:
            line, self._buf = self._buf.split('\n\r', 1)
        else:
            line = None
        return line

    def read(self):
        return self._readline()

    def return_result(self):
        self.sock.send(self.cmd)
        try:
            # register signal.SIGALRM's handler
            # signal.signal(signal.SIGALRM, TimeOutHandler)
            # signal.alarm(3)
            result = self.read()
        except Exception:
            raise
        finally:
            self.sock.close()

        if self.cmd.split('"')[3] == result.split('"')[3]:
            return result
        else:
            raise Exception('Unknow Error')

    def get_result(self):
        # time_out: get result timeout
        try:
            _str = self.return_result()
            _tmp_str = _str[_str.index(',') + 1:].strip()
            result = _tmp_str[_tmp_str.index(':') + 1:].strip()[:-1]
            return result
        except Exception as e:
            print e


if __name__ == '__main__':
    # win
    # linux
    server_address = '/var/lib/libvirt/qemu/com.eayun.eayunstack.0.6e4c4a95-329e-4859-a622-9d8865364a0a.sock'
    cmd = '{"operation":"get_infomation","name":"mysql_uptime"}\n\r'
    print SocketIoChannel(cmd=cmd, server_address=server_address).get_result()

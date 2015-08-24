#!/usr/bin/env python
# coding: utf8
#########################################
import socket
import time


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

    def return_result(self, time_out=3):
        # time_out: get result timeout
        try:
            self.sock.send(self.cmd)
            result = self.read()
        except AssertionError:
            raise AssertionError
        finally:
            self.sock.close()

        if self.cmd.split('"')[3] == result.split('"')[3]:
            return result
        else:
            raise Exception('Unknow Error')

    def get_result(self, time_out=2):
        # time_out: get result timeout
        try:
            _str = self.return_result(time_out)
            _tmp_str = _str[_str.index(',') + 1:].strip()
            result = _tmp_str[_tmp_str.index(':') + 1:].strip()[:-1]
            return result
        except Exception as e:
            print e


if __name__ == '__main__':
    pass
    ########### win

    ########### linux
    # print SocketIoChannel(cmd='{"operation":"eho","cmd":"dir"aa}\n\r', server_address='/tmp/xp.qga.sock').get_result()
    import sys

    server_address = '/var/lib/libvirt/qemu/com.eayun.eayunstack.0.6e4c4a95-329e-4859-a622-9d8865364a0a.sock'
    cmd = '{"operation":"execute_command","cmd":"%s"}\n\r' % sys.agrv[1]
    print SocketIoChannel(cmd=cmd, server_address=server_address).get_result()

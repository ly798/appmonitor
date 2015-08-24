#!/usr/bin/env python
# @@@-*- coding: utf8-*-@@@
#########################################
import socket
import time


class SocketIoChannel:
    def __init__(self, cmd, server_address='/tmp/qga.sock'):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server_address = server_address
        # try:
        self.sock.connect(self.server_address)
        # except AssertionError:
        #    raise AssertionError

        self.cmd = cmd
        self._buf = ''

    def read_buf(self):
        buf = self.sock.recv(4096)
        if buf:
            self._buf += buf
        else:
            time.sleep(1)

    def _readline(self):
        newline = self._buf.find('##end_flag##')
        while newline < 0:
            self.read_buf()
            newline = self._buf.find('##end_flag##')
        if newline >= 0:
            line, self._buf = self._buf.split('##end_flag##', 1)
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
    # /var/lib/libvirt/qemu/com.eayun.eayunstack.0.137e9287-743c-4b79-9c7c-6d6b5d0a79cf.sock
    # print SocketIoChannel(cmd='{"operation":"echo","cmd":"dir"}\n').get_result()
    print SocketIoChannel(cmd='{"operation":"eho","cmd":"dir"aa}\n', server_address='/tmp/xp.qga.sock').get_result()
    print SocketIoChannel(cmd='{"operation":"echo","cmd":"dir"}\n', server_address='/tmp/xp.qga.sock').get_result()
    # print SocketIoChannel(
    #    server_address='/var/lib/libvirt/qemu/com.eayun.eayunstack.0.137e9287-743c-4b79-9c7c-6d6b5d0a79cf.sock', \
    #    cmd='{"operation":"echo","cmd":"dir"}\n').get_result()

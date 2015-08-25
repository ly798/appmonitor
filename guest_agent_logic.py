#!/usr/bin/env python
# coding: utf8
#########################################
#
# class DataRetriverBase:
# 数据收集基类，定义了收集各类数据的方法
#
# class AgentLogicBase:
# 即插件的逻辑启动流程，主要是方法run、stop
#########################################

import thread
from threading import Event
import platform
import os
import importlib
import re

from guest_io_channel import VirtIoChannel


class AgentLogicBase:
    def __init__(self):
        self.wait_stop = Event()
        if (platform.system() == 'Windows') or (platform.system() == 'Microsoft'):
            vport_name = '\\\\.\\Global\\com.eayun.eayunstack.0'
        else:
            vport_name = '/dev/virtio-ports/com.eayun.eayunstack.0'
        self.vio = VirtIoChannel(vport_name)
        self.modules = []
        self.module_root_path = None
        self.register_module()

    def _send(self, name, arguments=None):
        self.vio.write(name, arguments or {})

    def run(self):
        thread.start_new_thread(self.doListen, ())
        while not self.wait_stop.isSet():
            self.wait_stop.wait(1)

    def stop(self):
        self.wait_stop.set()

    def doListen(self):
        while not self.wait_stop.isSet():
            try:
                cmd, args = self.vio.read()
                if cmd:
                    self.parseCommand(cmd, args)
            except Exception as e:
                raise

    def register_module(self):
        sys_plat = platform.system().lower()
        our_dir = 'modules/%s' % sys_plat
        dirpath, dirnames, filenames = os.walk(our_dir).next()
        for fname in filenames:
            root, ext = os.path.splitext(fname)
            if ext != '.py' or root == '__init__':
                continue
            self.modules.append(root)
        self.module_root_path = re.sub('/', '.', our_dir)

    def parseCommand(self, command, args):
        if command == 'get_infomation':
            name = args.get('name')
            if name in self.modules:
                m = importlib.import_module('%s,%s' % (self.module_root_path, name))
                result = m.module().get_result()
                self._send('get_infomation', {'result': result})
        elif command == 'echo':
            self._send('echo', args)
        else:
            self._send(command, {'result': '0e0r0r0o0r0'})


if __name__ == '__main__':
    pass

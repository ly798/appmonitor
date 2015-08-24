#!/usr/bin/env python
# coding: utf8
#########################################
# @author yippee
# @date 2015-07-17
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
import socket
import platform

from guest_io_channel import VirtIoChannel

multiproc = None
try:
    import multiprocessing

    multiproc = multiprocessing
except ImportError:
    class MultiProcessingFake:
        def cpu_count(self):
            return -1


    multiproc = MultiProcessingFake()


class DataRetriverBase:
    def __init__(self):
        self.memStats = {
            'mem_total': 0,
            'mem_free': 0,
            'mem_unused': 0,
            'swap_in': 0,
            'swap_out': 0,
            'pageflt': 0,
            'majflt': 0}

    def getMachineName(self):
        pass

    def getOsVersion(self):
        pass

    def getAllNetworkInterfaces(self):
        pass

    def getApplications(self):
        pass

    def getAvailableRAM(self):
        pass

    def getUsers(self):
        pass

    def getActiveUser(self):
        pass

    def getDisksUsage(self):
        pass

    def getDiskMapping(self):
        pass

    def getMemoryStats(self):
        pass

    def getFQDN(self):
        return socket.getfqdn()

    def getOsInfo(self):
        pass

    def getNumberOfCPUs(self):
        try:
            return multiproc.cpu_count()
        except NotImplementedError:
            return -1

    def getTimezoneInfo(self):
        pass
        # return timezone.get_timezone_info()


class AgentLogicBase:
    def __init__(self):
        self.wait_stop = Event()
        if (platform.system() == 'Windows') or (platform.system() == 'Microsoft'):
            vport_name = '\\\\.\\Global\\com.eayun.eayunstack.0'
        else:
            vport_name = '/dev/virtio-ports/com.eayun.eayunstack.0'
        self.vio = VirtIoChannel(vport_name)
        self.commandHandler = None

    def _send(self, name, arguments=None):
        self.vio.write(name, arguments or {})

    def run(self):
        thread.start_new_thread(self.doListen, ())
        while not self.wait_stop.isSet():
            self.wait_stop.wait(1)

    def stop(self):
        self.wait_stop.set()

    def doListen(self):
        if self.commandHandler is None:
            return
        while not self.wait_stop.isSet():
            try:
                cmd, args = self.vio.read()
                if cmd:
                    self.parseCommand(cmd, args)
            except:
                pass

    def parseCommand(self, command, args):
        if command == 'get_infomation':
            name = args.get('name')
            result = self.commandHandler.get_infomation(name)
            self._send('get_infomation', {'result': result})

        elif command == 'execute_script':
            path = args.get('path')
            type = args.get('type')
            result = self.commandHandler.execute_script(path, type)
            self._send('execute_script', {'result': result})

        elif command == 'execute_command':
            cmd = args.get('cmd')
            try:
                result = self.commandHandler.execute_command(cmd)
                self._send('execute_command', {'result': result})
            except:
                self._send('execute_command', {'result': '0e0r0r0o0r1'})

        elif command == 'echo':
            self._send('echo', args)

        else:
            self._send(command, {'result': '0e0r0r0o0r0'})


if __name__ == '__main__':
    from guest_agent_linux import LinuxVdsAgent

    agent = LinuxVdsAgent()
    agent.run()

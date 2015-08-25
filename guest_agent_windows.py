#!/usr/bin/env python
# @@@-*- coding: utf8-*-@@@
#########################################
#
# class LinuxDataRetriver(DataRetriverBase):
# 数据收集的实现类
#
# class LinuxVdsAgent(AgentLogicBase):
# 运行插件的实现类
#
# class CommandHandlerLinux:
# 通过插件执行的动作实现类
#
#########################################

import subprocess
import socket
import os
import commands

from guest_agent_logic import AgentLogicBase, DataRetriverBase


class CommandHandlerWindows:
    def __init__(self, agent):
        self.agent = agent

    def execute_command(self, cmd):
        # {"__name__":"execute_command","cmd":"ps aux|awk '{print $11}'"}
        r = os.popen(cmd).read()
        if not r:
            raise Exception
        else:
            return r

    def get_infomation(self, name):
        # {"__name__":"get_infomation","name":"os_info"}
        if name == 'os_info':
            return self.agent.getOsInfo()
        elif name == 'machine_name':
            return self.agent.getMachineName()
        else:
            return '0e0r0r0o0r2'


class WindowsVdsAgent(AgentLogicBase):
    def __init__(self):
        self.dr = WindowsDataRetriver()
        AgentLogicBase.__init__(self)
        self.commandHandler = CommandHandlerWindows(self.dr)

    def run(self):
        AgentLogicBase.run(self)

    def stop(self):
        AgentLogicBase.stop(self)


class WindowsDataRetriver(DataRetriverBase):
    def __init__(self):
        pass

    def getMachineName(self):
        return socket.getfqdn()

    def getOsInfo(self):
        import platform

        info = platform.linux_distribution()
        result = {
            'version': '',
            'distribution': '',
            'codename': '',
            'arch': '',
            'type': 'linux',
            'kernel': ''}
        try:
            result['version'] = info[0]
            result['distribution'] = info[1]
            result['codename'] = info[2]
            result['arch'] = platform.uname()[-1]
            result['type'] = platform.system()
            result['kernel'] = platform.release()
        except Exception:
            pass
        return result

    # ----------------------------------------------------#
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

    def _get_meminfo(self):
        pass

    def _get_vmstat(self):
        pass


# ----------------------------------------------------#

def test():
    dr = WindowsDataRetriver()
    print "Os Info:", dr.getOsInfo()


if __name__ == '__main__':
    pass
    test()

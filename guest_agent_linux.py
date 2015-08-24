#!/usr/bin/env python
# coding: utf8
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
# 因为虚拟机中python一般没有安装rthtool模块，在all_network_interfaces会返回空
#########################################

import subprocess
import socket
import os
import commands
import time

from guest_agent_logic import AgentLogicBase, DataRetriverBase


class CommandHandlerLinux:
    def __init__(self, agent):
        self.agent = agent

    def execute_command(self, cmd):
        # {"__name__":"execute_command","cmd":"ps aux|awk '{print $11}'"}
        s, r = commands.getstatusoutput(cmd)
        if s:
            raise Exception
        else:
            return r

    def execute_script(self, path, type='py'):
        if type == 'py':
            return self.execute_command('python %s' % path)
        elif type == 'sh':
            return self.execute_command('/bin/bash %s' % path)
        else:
            raise Exception

    def get_infomation(self, name):
        if name == 'os_info':
            return self.agent.getOsInfo()
        elif name == 'machine_name':
            return self.agent.getMachineName()
        elif name == 'os_version':
            return self.agent.getOsVersion()
        elif name == 'all_network_interfaces':
            return self.agent.getAllNetworkInterfaces()
        elif name == 'available_ram':
            return self.agent.getAvailableRAM()
        elif name == 'users':
            return self.agent.getUsers()
        elif name == 'active_user':
            return self.agent.getActiveUser()
        elif name == 'disks_usage':
            return self.agent.getDisksUsage()
        elif name == 'memory_stats':
            return self.agent.getMemoryStats()
        else:
            return '0e0r0r0o0r2'


class LinuxVdsAgent(AgentLogicBase):
    def __init__(self):
        self.dr = LinuxDataRetriver()
        AgentLogicBase.__init__(self)
        self.commandHandler = CommandHandlerLinux(self.dr)

    def run(self):
        AgentLogicBase.run(self)

    def stop(self):
        AgentLogicBase.stop(self)


class LinuxDataRetriver(DataRetriverBase):
    def __init__(self):
        self._init_vmstat()
        DataRetriverBase.__init__(self)

    def getMachineName(self):
        return socket.getfqdn()

    def getOsVersion(self):
        return os.uname()[2]

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
            result['type'] = 'linux'
            result['kernel'] = platform.release()
        except Exception:
            pass
            # logging.exception('ovirt-osinfo invocation failed')
        return result

    def getAllNetworkInterfaces(self):
        try:
            nicmgr = NicMgr()
        except NotImplementedError:
            # self.list_nics = lambda: []
            # raise NotImplementedError
            import re

            dev = []
            s, o = commands.getstatusoutput('ip addr show')
            if s:
                raise Exception('execute failed')
            else:
                # 按网络设备段落划分
                devs_str = re.split('\n\d:', o)
                # 每个段落再划分每行
                dev_str_line = [i.split('\n') for i in devs_str]
                for i in dev_str_line:
                    mes = {}
                    inet4s = []
                    # 对每行进行判断解析
                    for j in i:
                        m = re.search('\s([a-z]+\d*):\s', j)
                        if hasattr(m, 'group'):
                            name = m.group(1)
                            mes['name'] = name

                        m = re.search('\s<(.+?)>\s', j)
                        if hasattr(m, 'group'):
                            attr = m.group(1)
                            mes['attr'] = attr

                        m = re.search('link/ether\s(\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})\s', j)
                        if hasattr(m, 'group'):
                            mac = m.group(1)
                            mes['mac'] = mac

                        m = re.search('inet\s(\d+\.\d+\.\d+\.\d+/\d+.)\s', j)
                        if hasattr(m, 'group'):
                            inet4 = m.group(1)
                            inet4s.append(inet4)

                        m = re.search('inet6\s(\S+)\s', j)
                        if hasattr(m, 'group'):
                            inet6 = m.group(1)
                            mes['inet6'] = inet6

                    if inet4s:
                        mes['inet4'] = inet4s
                    dev.append(mes)
            return dev
        else:
            self.list_nics = nicmgr.list_nics

        return self.list_nics()

    def getApplications(self):
        pass

    def getAvailableRAM(self):
        free = 0
        for line in open('/proc/meminfo'):
            var, value = line.strip().split()[0:2]
            if var in ('MemFree:', 'Buffers:', 'Cached:'):
                free += long(value)
        return str(free / 1024)

    def getUsers(self):
        users = ''
        try:
            cmdline = '/usr/bin/users | /usr/bin/tr " " "\n" | /usr/bin/uniq'
            users = ' '.join(os.popen(cmdline).read().split())
        except:
            pass
        return users

    def getActiveUser(self):
        users = ''
        try:
            cmdline = '/usr/bin/users | /usr/bin/tr " " "\n" | /usr/bin/uniq'
            users = ' '.join(os.popen(cmdline).read().split())
        except:
            pass
        return users

    def getDisksUsage(self):
        ignored_fs = set("rootfs tmpfs autofs cgroup selinuxfs udev mqueue "
                         "nfsd proc sysfs devtmpfs hugetlbfs rpc_pipefs devpts "
                         "securityfs debugfs binfmt_misc fuse.gvfsd-fuse "
                         "fuse.gvfs-fuse-daemon fusectl usbfs".split())
        ignore_zero_size_fs = True
        usages = list()
        try:
            mounts = open('/proc/mounts', 'r')
            for mount in mounts:
                try:
                    (device, path, fs) = mount.split()[:3]
                    if fs not in ignored_fs:
                        # path might include spaces.
                        path = path.decode("string-escape")
                        statvfs = os.statvfs(path)
                        total = statvfs.f_bsize * statvfs.f_blocks
                        used = total - statvfs.f_bsize * statvfs.f_bfree
                        if ignore_zero_size_fs and used == total == 0:
                            continue
                        usages.append({'path': path, 'fs': fs, 'total': total,
                                       'used': used})
                except:
                    pass
            mounts.close()
        except Exception:
            pass
            if mounts:
                mounts.close()

        return usages

    def getDiskMapping(self):
        pass

    def getMemoryStats(self):
        try:
            self._get_meminfo()
            self._get_vmstat()
        except:
            pass
        return self.memStats

    def _get_meminfo(self):
        fields = {'MemTotal:': 0, 'MemFree:': 0, 'Buffers:': 0,
                  'Cached:': 0, 'SwapFree:': 0, 'SwapTotal:': 0}
        free = 0
        for line in open('/proc/meminfo'):
            (key, value) = line.strip().split()[0:2]
            if key in fields.keys():
                fields[key] = int(value)
            if key in ('MemFree:', 'Buffers:', 'Cached:'):
                free += int(value)

        self.memStats['mem_total'] = fields['MemTotal:']
        self.memStats['mem_unused'] = fields['MemFree:']
        self.memStats['mem_free'] = free
        self.memStats['mem_buffers'] = fields['Buffers:']
        self.memStats['mem_cached'] = fields['Cached:']
        swap_used = fields['SwapTotal:'] - fields['SwapFree:']
        self.memStats['swap_usage'] = swap_used
        self.memStats['swap_total'] = fields['SwapTotal:']

    def _init_vmstat(self):
        self.vmstat = {}
        self.vmstat['timestamp_prev'] = time.time()
        fields = ['swap_in', 'swap_out', 'pageflt', 'majflt']
        for field in fields:
            self.vmstat[field + '_prev'] = None
            self.vmstat[field + '_cur'] = None

    def _get_vmstat(self):
        """
        /proc/vmstat reports cumulative statistics so we must subtract the
        previous values to get the difference since the last collection.
        """
        fields = {'pswpin': 'swap_in', 'pswpout': 'swap_out',
                  'pgfault': 'pageflt', 'pgmajfault': 'majflt'}

        self.vmstat['timestamp_cur'] = time.time()
        interval = self.vmstat['timestamp_cur'] - self.vmstat['timestamp_prev']
        self.vmstat['timestamp_prev'] = self.vmstat['timestamp_cur']

        for line in open('/proc/vmstat'):
            (key, value) = line.strip().split()[0:2]
            if key in fields.keys():
                name = fields[key]
                self.vmstat[name + '_prev'] = self.vmstat[name + '_cur']
                self.vmstat[name + '_cur'] = int(value)
                if self.vmstat[name + '_prev'] is None:
                    self.vmstat[name + '_prev'] = self.vmstat[name + '_cur']
                self.memStats[name] = int((self.vmstat[name + '_cur'] -
                                           self.vmstat[name + '_prev']) /
                                          interval)


class NicMgr(object):
    def __init__(self):
        try:
            import ethtool
        except ImportError:
            raise NotImplementedError
        self.ethtool = ethtool
        self.list_nics = self.ethtool_list_nics

    def _get_ipv4_addresses(self, dev):
        if hasattr(dev, 'get_ipv4_addresses'):
            ipv4_addrs = []
            for ip in dev.get_ipv4_addresses():
                ipv4_addrs.append(ip.address)
            return ipv4_addrs
        if dev.ipv4_address is not None:
            return [dev.ipv4_address]
        else:
            return []

    def _get_ipv6_addresses(self, dev):
        ipv6_addrs = []
        for ip in dev.get_ipv6_addresses():
            ipv6_addrs.append(ip.address)
        return ipv6_addrs

    def ethtool_list_nics(self):
        interfaces = list()
        try:
            for dev in self.ethtool.get_devices():
                flags = self.ethtool.get_flags(dev)
                if flags & self.ethtool.IFF_UP and \
                        not (flags & self.ethtool.IFF_LOOPBACK):
                    devinfo = self.ethtool.get_interfaces_info(dev)[0]
                    interfaces.append(
                        {'name': dev,
                         'inet': self._get_ipv4_addresses(devinfo),
                         'inet6': self._get_ipv6_addresses(devinfo),
                         'hw': self.ethtool.get_hwaddr(dev)})
        except:
            pass
        return interfaces


def test():
    dr = LinuxDataRetriver()
    print "Os Info:", dr.getOsInfo()


if __name__ == '__main__':
    pass
    test()

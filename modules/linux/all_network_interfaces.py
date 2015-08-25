#!/usr/bin/env python
# coding: utf8
import commands


class AllNetworkInterfaces(object):
    def __init__(self):
        self.name = 'all_network_interfaces'

    def get_result(self):

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
                        mes['inet4'] = inet4
                    dev.append(mes)
            return dev
        else:
            self.list_nics = nicmgr.list_nics

        return self.list_nics()


def module():
    return AllNetworkInterfaces()


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


if __name__ == '__main__':
    import pprint

    i = AllNetworkInterfaces()
    pprint.pprint(i.get_result())

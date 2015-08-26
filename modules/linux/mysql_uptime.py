#!/usr/bin/env python
# coding: utf8
import commands
import re


class MysqlUptime(object):
    def __init__(self):
        self.name = 'mysql_uptime'

    def get_result(self):
        s, o = commands.getstatusoutput('mysqladmin -uroot -pabc123 extended-status | grep "\sUptime\s"')
        m = re.search('\s(\d+)\s', o)
        if hasattr(m, 'group'):
            uptime = m.group(1)
            result = uptime
        return result


def module():
    return MysqlUptime()


if __name__ == '__main__':
    import pprint

    i = MysqlUptime()
    pprint.pprint(i.get_result())

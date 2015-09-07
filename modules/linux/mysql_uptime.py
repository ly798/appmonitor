#!/usr/bin/env python
# coding: utf8
import commands
import re


class MysqlUptime(object):
    def __init__(self):
        self.name = 'mysql_uptime'

    def get_result(self, attr):
        # username = attr.get('username', None)
        # password = attr.get('password', None)
        s, o = commands.getstatusoutput(
            'mysqladmin -u%(username)s -p%(password)s extended-status | grep "\sUptime\s"' % attr)
        m = re.search('\s(\d+)\s', o)
        if hasattr(m, 'group'):
            uptime = m.group(1)
            return uptime


def module():
    return MysqlUptime()


if __name__ == '__main__':
    import pprint

    i = MysqlUptime()
    pprint.pprint(i.get_result())

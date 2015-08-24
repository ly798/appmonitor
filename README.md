# Ovirt

"/var/lib/libvirt/qemu/%s.%s.sock" % ("org.qemu.guest_agent.0", instance['name']))
com.eayun.eayunstack.0


## 虚拟机启动参数

### linux

```
kvm \
 -drive file=centos7.qcow2,snapshot=off,if=virtio \
 -net nic,model=virtio,macaddr=52:54:00:12:34:00 \
 -net tap,script=/etc/qemu-ifup \
 -m 1024 --enable-kvm \
 -chardev socket,path=/tmp/qga.sock,server,nowait,id=qga0 \
 -device virtio-serial \
 -device virtserialport,chardev=qga0,name=org.qemu.guest_agent.0
```

### windows

需安装virtio的网卡驱动、serial串口驱动
```
kvm \
-hda xp.qcow2 \
-cdrom virtio-win-0.1.105.iso \
-net nic,model=virtio -net user \
-m 1024 --enable-kvm \
-chardev socket,path=/tmp/xp.qga.sock,server,nowait,id=qga0 \
-device virtio-serial \
-device virtserialport,chardev=qga0,name=org.qemu.guest_agent.0
```

## 代码结构

OVirt<br/>
\-\-\-    GuestAgentService.py<br/>
\-\-\-    OVirtIoChannel.py<br/>
\-\-\-    OVirtAgentLogic.py<br/>
\-\-\-    GuestAgentLinux.py<br/>
\-\-\-    GuestAgentwindows.py<br/>
\-\-\-    OSocketIoChannel.py<br/>

## 功能
数据格式：JSON
### globle

其实现代码在OVirtAgentLogic.py

* echo<br/>
测试连通性。<br/>
`{"operation":"echo","cmd":"dir"}`<br/>
`{"operation": "echo", "cmd": "dir"}`

### linux
其实现代码在GuestAgentLinux.py

* execute command<br/>
`{"operation":"execute_command","cmd":"ps aux|wc -l"}`<br/>
`{"operation": "execute_command", "result": "115"}`

* execute script
支持.py、.sh<br/>
`{"operation":"execute_script","path":"/root/hello.py","type":"py"}`<br/>
`{"operation": "execute_script", "result": "hello"}`

* get information
	1. os info<br/>
	`{"operation":"get_infomation","name":"os_info"}`<br/>
    ```{"operation": "get_infomation", "result": {"kernel": "3.10.0-229.7.2.el7.x86_64", "type": "linux", "version": "CentOS Linux", "distribution": "7.1.1503", "arch": "x86_64", "codename": "Core"}}```
	2. machine name<br/>
	`{"operation":"get_infomation","name":"machine_name"}`<br/>
    `{"operation": "get_infomation", "result": "ea"}`
	3. os version<br/>
	`{"operation":"get_infomation","name":"os_version"}`<br/>
    `{"operation": "get_infomation", "result": "3.10.0-229.7.2.el7.x86_64"}`
    4. all network interfaces<br/>
    `{"operation":"get_infomation","name":"all_network_interfaces"}`<br/>
    `{"operation": "get_infomation", "result": [{"attr": "LOOPBACK,UP,LOWER_UP", "inet6": "::1/128", "name": "lo"}, {"attr": "BROADCAST,MULTICAST,UP,LOWER_UP", "mac": "52:54:00:12:34:00", "inet6": "fe80::5054:ff:fe12:3400/64", "name": "eth0", "inet4": ["192.168.1.103/24"]}]}`
    5. available ram<br/>
    `{"operation":"get_infomation","name":"available_ram"}`<br/>
    `{"operation": "get_infomation", "result": "110"}`
    6. users<br/>
    `{"operation":"get_infomation","name":"users"}`<br/>
    `{"operation": "get_infomation", "result": "root"}`
    7. active user<br/>
    `{"operation":"get_infomation","name":"active_user"}`<br/>
    `{"operation": "get_infomation", "result": "root"}`
    8. disks usage<br/>
    `{"operation":"get_infomation","name":"disks_usage"}`<br/>
    `{"operation": "get_infomation", "result": [{"path": "/", "total": 9124708352, "used": 2270470144, "fs": "xfs"}, {"path": "/boot", "total": 520794112, "used": 145895424, "fs": "xfs"}]}`
    9. memory stats<br/>
    `{"operation":"get_infomation","name":"memory_stats"}`<br/>
    `{"operation": "get_infomation", "result": {"swap_out": 0, "majflt": 0, "swap_usage": 171992, "mem_cached": 39692, "mem_free": 113456, "mem_buffers": 0, "swap_in": 0, "swap_total": 1048572, "pageflt": 0, "mem_total": 1017096, "mem_unused": 73764}}`


### windows
其实现代码在GuestAgentwindows.py

* execute command<br/>
`{"operation":"execute_command","cmd":"dir"}`<br/>
` `

* get information
	1. os info<br/>
	`{"operation":"get_infomation","name":"os_info"}`<br/>
    ` `
	2. machine name<br/>
	`{"operation":"get_infomation","name":"machine_name"}`<br/>
    ` `



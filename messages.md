#针对虚拟机的监控
## ceilometer已实现

### libvirt可支持的监控
memory          分配给实例的内存数量  
memory.usage    x  
  
cpu             CPU使用时间             ns  
cpu_util        平均CPU使用             %  
vcpus           分配给实例的vcpu数量  

disk.read.requests          读请求数        request         Cumulative  
disk.read.requests.rate     平均读请求率      request/s       Gauge  
disk.write.requests         写请求数        request         Cumulative  
disk.write.requests.rate    平均写请求率      request/s       Gauge  
disk.read.bytes             读               B               Cumulative  
disk.read.bytes.rate        平均读速率       B/S  
disk.write.bytes  
disk.write.bytes.rate  
disk.root.size              根磁盘大小       GB  
disk.ephemeral.size         临时磁盘大小      GB  
  



## OVirt

### Linux

### Windows
可实现  
内存总大小、可用内存大小、虚拟内存交换内存  
驱动器号、总容量、空闲容量、文件系统类型等  

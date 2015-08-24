# 与ceilometer结合

## eg: guest process number

1. /usr/lib/python2.7/site-packages/ceilometer-2014.2-py2.7.egg-info/entry_points.txt

    ```
    
    [ceilometer.poll.compute]
    ...
    process.num = ceilometer.compute.pollsters.process:ProcessNumPollster
    
    ```

2. ceilometer/compute/pollsters/process.py

    ```
    import ceilometer
    from ceilometer.compute import plugin
    from ceilometer.compute.pollsters import util
    from ceilometer.compute.virt import inspector as virt_inspector
    from ceilometer.openstack.common.gettextutils import _
    from ceilometer.openstack.common import log
    from ceilometer import sample
    
    LOG = log.getLogger(__name__)
    
    class ProcessNumPollster(plugin.ComputePollster):
        def get_samples(self, manager, cache, resources):
            for instance in resources:
                LOG.debug(_('checking instance %s'), instance.id)
                #instance_name = util.instance_name(instance)
                try:
                    process_info = manager.inspector.inspect_process(instance.id)
                    LOG.debug(_("process: %(instance)s %(process)d"),
                              {'instance': instance.__dict__,
                               'process': process_info.num})
                    yield util.make_sample_from_instance(
                        instance,
                        name='process.num',
                        type=sample.TYPE_GAUGE,
                        unit='number',
                        volume=process_info.num,
                    )
                except virt_inspector.InstanceNotFoundException as err:
                    LOG.debug(_('Exception while getting samples %s'), err)
                except ceilometer.NotImplementedError:
                    LOG.debug(_('Obtaining process_info is not implemented for %s'
                                ), manager.inspector.__class__.__name__)
                except Exception as err:
                    LOG.exception(_('could not get process.num for %(id)s: %(e)s'),
                                  {'id': instance.id, 'e': err})
    ```

3. ceilometer/compute/virt/inspector.py

    ```
    class Inspector(object):
        ...
        def inspect_process(self,instance,duration=None):
            raise ceilometer.NotImplementedError
            
    ProcessNum = collections.namedtuple('ProcessNum', ['num',])
    
    ```
    
4. 将OVirt中的OSocketIoChannel.py引入virt包内;

5. ceilometer/compute/virt/libvirt/inspector.py

    ```
    class LibvirtInspector(virt_inspector.Inspector):
        from ceilometer.compute.virt.OSocketIoChannel import SocketIoChannel
        def inspect_mems(self, instance_id):
            sic = SocketIoChannel(
                server_address='/var/lib/libvirt/qemu/com.eayun.eayunstack.0.%s.sock' % instance_id,
                cmd='''{"operation":"execute_command","cmd":"ps aux|wc -l"}\n''')
            process_num = sic.get_result()
            process_num = int(process_num)-1
            return virt_inspector.ProcessNum(num=process_num)
            
    ```
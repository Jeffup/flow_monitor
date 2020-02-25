'''
此脚本用于获取PC信息（回路除外）
'''
from time import sleep

from flask_socketio import emit
from psutil import net_if_addrs, cpu_percent, cpu_times, virtual_memory, net_io_counters, disk_partitions, disk_usage

from settings import NETCARD, NETCARD_LIST

def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9.8 K'
    >>> bytes2human(100001221)
    '95.4 M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f %s' % (value, s)
    return '%.2f B' % (n)

def get_netcard():
    netcard_info = []
    info = net_if_addrs()
    for k,v in info.items():
        for item in v:
            if item[0] == 2 and not item[1]=='127.0.0.1':
                netcard_info.append((k,item[1]))
    # 存储网卡信息
    global NETCARD_LIST
    NETCARD_LIST = netcard_info

    return netcard_info

def get_cpuinfo():
    # function of Get CPU State;
    return {"cpu":cpu_percent()}

def get_meminfo():
    phymem = virtual_memory()
    # line = "Memory: %5s%% %6s/%s" % (
    #     phymem.percent,
    #     str(int(phymem.used / 1024 / 1024)) + "M",
    #     str(int(phymem.total / 1024 / 1024)) + "M"
    # )
    return {"mem":phymem.percent}

def get_diskinfo():
    disk = disk_partitions()
    percent = 0.0
    for i in disk:
        disk_use = disk_usage(i.device)
        percent += float(disk_use.percent)
    return {'disk': percent}

def get_netinfo(netcard=NETCARD):
    # net_state = net_io_counters()
    net_state = net_io_counters(pernic=True)
    net_state = net_state[netcard]
    # return "Sent:%s  Recv:%s"%(net_state[])
    return {"send":net_state.bytes_sent,"recv":net_state.bytes_recv}


# socketio线程：发送pc信息
def thread_of_pcinfo():
    olddata = {'send':0, 'recv':0}
    i = 2
    while True:
        global NETCARD
        cpuinfo = get_cpuinfo()
        meminfo = get_meminfo()
        diskinfo = get_diskinfo()
        netinfo = get_netinfo(NETCARD)
        newdata = {'send': bytes2human((netinfo['send']-olddata['send'])/2 if(netinfo['send']-olddata['send']>0) else 0)+'/s',
                   'recv': bytes2human((netinfo['recv']-olddata['recv'])/2 if(netinfo['recv']-olddata['recv']>0) else 0)+'/s'}
        olddata = netinfo

        newdata.update(cpuinfo)
        newdata.update(meminfo)
        newdata.update(diskinfo)
        if i > 1:
            sleep(2)
            i = 0
            continue
        else:
            print(newdata)
            emit('pcinfo_response', newdata, namespace='/capture')
            sleep(2)





# def poll():
#     """Retrieve raw stats within an interval window."""
#     tot_before = net_io_counters()
#     pnic_before = net_io_counters(pernic=True)
#     # sleep some time
#     sleep(1)
#     tot_after = net_io_counters()
#     pnic_after = net_io_counters(pernic=True)
#     # get cpu state
#     cpu_state = get_cpuinfo()
#     # get memory
#     memory_state = get_meminfo()
#     return (tot_before, tot_after, pnic_before, pnic_after, cpu_state, memory_state)

# print(get_netcard())
# print(get_cpuinfo())
# print(get_meminfo())
# print(poll())
# print(get_netinfo())
# print(thread_of_pcinfo())
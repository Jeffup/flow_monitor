
import socket
import sys
import struct
from optparse import OptionParser
from time import time

from flask_socketio import emit

priority=['Routine(普通)','Priority（优先）','Immediate（快速）','Flash（闪速）','Flash Override（疾速）'
    ,'Critic（关键）','Internetwork Control（网间控制）','Network Control（网络控制）']
precedence=['ICMP差错/查询 或 TCP查询 或 BOOTP','NNTP','ICMP任何IGP 或 SNMP','','DNS区域传输 或 SMTP数据阶段 或 FTP任意块数据'
            ,'','','','','Telnet/Rlogin 或 SMTP命令阶段 或 DNS-UDP阶段']+['']*9
flags={128:'保留字段',64:'不分段', 32:'还有更多的分段',0:'已是最后分段'}
protocol={1:'ICMP',2:'IGMP',6:'TCP',7:'UDP',89:'OSPF'}

otherLine = '\n'

class ip(object):
    """ This class deals with the ip header level"""


    def __init__(self, header):
        self.header = header

    def extract(self):
        """ Extract IP Header elements """

        """ unpack header into:
            |_ B(Version+IHL)|B(TOS)|H(TotalLength)|H(ID)
            |_ H(Flags+FragmentOffset)|B(TTL)|B(Protocol)|H(CheckSum)
            |_ I(Source)|I(Destination)
            Note: "R" used to hold the reserved bits"""

        unpacked = struct.unpack("!BBHHHBBHII", self.header)
        header = []
        # ip版本和报文长度(IHL)
        header += unpackBit("4b4b", unpacked[0])
        # 优先权和推荐应用
        header += unpackBit("3b4b", unpacked[1])  # omit Reserved
        # 总长度
        header += [unpacked[2]]
        # 标识
        header += [unpacked[3]]
        # 标志位(reserved, df, mf), 段偏移
        header += unpackBit("3b13b", unpacked[4])  # omit Reserved
        # Time to live in seconds（TTL）
        header += [unpacked[5]]
        #协议（ICMP=1,IGMP=2,TCP=6,UDP=17,OSPF=89）
        header += [unpacked[6]]
        #校验和
        header += [unpacked[7]]
        # Source IP Address
        source = struct.pack("!I", unpacked[8])  # Pack address in "\xNN\xNN\xNN\xNN" format
        source = socket.inet_ntoa(source)
        header += [source]
        # Destination IP Address
        destination = struct.pack("!I", unpacked[9])
        destination = socket.inet_ntoa(destination)
        header += [destination]
        return header

    def parse(self):
        header = self.extract()
        dict_heard={}
        # print("IP 头:")
        # print("|_ IP版本: IPv%d" % header[0])
        dict_heard['ipversion'] = header[0]
        # print("|_ 报文长度: %d bytes" % (header[1] * 4))
        # dict_heard['headerlen'] = header[1]*4
        # print("|_ 服务类型:")
        try:
            # print("|___ 优先级: " + priority[header[2]])
            dict_heard['priority'] = priority[header[2]]
        except:
            # print("|___ 优先级: No Found!")
            dict_heard['priority'] = 'No Found!'
        try:
            # print("|___ 应用程序: " + precedence[header[3]])
            dict_heard['delay'] = precedence[header[3]]
        except:
            # print("|___ 应用程序: No Found!")
            dict_heard['delay'] = 'No Found!'
        # print("|_ 总长度: " + hex(header[4]))
        dict_heard['packetlen'] = hex(header[4])
        # print("|_ 标识: " + hex(header[5]))
        # dict_heard['identification:'] = hex(header[5])
        # try:
        #     print("|_ 标志: " + flags[header[6]])
        # except:
        #     print("|_ 标志: No Found!")
        # print("|_ 段内偏移: " + hex(header[7]))

        # print("|_ TTL: %d seconds" % header[8])
        dict_heard['ttl'] = header[8]
        try:
            # print("|_ 协议: " + protocol[header[9]])
            dict_heard['protocol'] = protocol[header[9]]
        except:
            # print("|_ 协议: No Found!")
            dict_heard['protocol'] = 'No Found!'
        # print("|_ 校验和: " + hex(header[10]))
        # dict_heard['checksum'] = hex(header[10])
        # print("|_ 源ip地址: " + header[11])
        dict_heard['sourceip'] = header[11]
        # print("|_ 目的ip地址: " + header[12])
        dict_heard['destinip'] = header[12]
        return dict_heard


def asciiDump(data):
    # print("  ", end="")
    data_str = "   "
    for x in data:
        if x in range(32, 127):
            # print(chr(x), end="")
            data_str += chr(x)
        else:
            # print(".", end="")
            data_str += '.'
    # print()  # new line
    data_str += '</br>'
    return data_str

def dump(data):
    # print("--- STA 数据块 ---")
    # print("Offset(h)  ", end="")
    data_str = "--- STA 数据块 ---</br>&nbsp;Offset(h)&nbsp;&nbsp;"
    for i in range(16):
        # print("%02X " % i, end="")
        data_str += "%02X " % i
    # print("\tASCII")
    data_str += "&nbsp;&nbsp;ASCII"
    line = 0  # every line holds 16 bytes
    index = 0  # index of the current line in data
    for i in range(len(data)):
        if i % 16 == 0:
            # asciiDump(data[index:i])
            data_str += asciiDump(data[index:i])
            index = i
            # print the new line address
            # print("%08X   " % line, end="")
            data_str += "%08X   " % line
            line += 1
        # print("%02X " % data[i], end="")
        data_str += "%02X " % data[i]

    # Padding
    i += 1
    while i % 16:
        # print("   ", end="")
        data_str += "   "
        i += 1
    # Last line ASCII dump
    # asciiDump(data[index:])
    data_str += asciiDump(data[index:])
    # print("--- END 数据块  ---")
    data_str += "--- END 数据块  ---</br>"
    return data_str


def unpackBit(fmt, data):
    """ unpack data at the bit level """
    # header += unpackBit("4b4b", unpacked[0])
    try:
        # 获取格式内容（以b断）
        elements = fmt.split("b")
        # 去除最后一个空的元素
        elements = elements[:-1]
        # str to int
        for i in range(len(elements)):
            elements[i] = int(elements[i])
        # 位的长度
        length = sum(elements, 0)
        # 转成二进制
        binary = bin(data)
        # 删除 '0b' 前缀
        binary = binary[2:]
        # 填补
        if length > len(binary):
            binary = '0' * (length - len(binary)) + binary
        if length != len(binary):
            raise ValueError("Unmatched size of data")
    except ValueError as err:
        print("[-] Error: %s" % str(err))
        sys.exit(1)

    # List of unpacked Data
    uData = []
    for l in elements:
        # Convert the first l bits to decimal
        unpacked = int(binary[:l], 2)
        uData.append(unpacked)
        # git rid of the last unpacked data
        binary = binary[l:]

    return uData


def sniff(sock):
    """ sniff a packet, parse it's header and dump the sniffed data """
    packet, address = sock.recvfrom(65565)
    ipheader = ip(packet[:20])  # IP Header
    dict = ipheader.parse()  # display IP header descriptions
    dict['dump'] = dump(packet[20:])  # 数据块
    print(dict)



def thread_of_sniff():
    parser = OptionParser()
    parser.add_option("-n", dest="npackets", type="int", \
                      help="Number of packets to sniff")
    (options, args) = parser.parse_args()
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    try:
        # 获得网络接口
        host = socket.gethostbyname(socket.gethostname())
        s.bind(('192.168.247.10', 0))
        # 混杂模式
        # s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        if options.npackets != None:
            for i in range(options.npackets):
                sniff(s)
        else:
            old_time = time()
            id = 1
            while True:
                # sniff(s)
                packet, address = s.recvfrom(65565)
                ipheader = ip(packet[:20])  # IP Header
                dict = ipheader.parse()  # display IP header descriptions
                dict['dump'] = dump(packet[20:])  # 数据块
                dict['id'] = id
                id += 1
                new_time = time()
                dict['time'] = new_time

                dict['level'] = 'danger'

                dict['isdanger'] = 1
                if new_time-old_time >= 5:
                    old_time = new_time
                    emit('packet_response', dict, namespace='/capture')
    except socket.error as err:
        print("[-] 错误: %s" % str(err))
    except KeyboardInterrupt:
        print("[+] 获得键盘输入: Existing")

    # 关闭混杂模式
    # s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
    s.close()



# if __name__ == "__main__":
#     sniffer()
    # import socket
    # print(socket.IPPROTO_RAW)
    # s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    # s.bind(('192.168.247.10', 0))
    # while True:
    #     print(s.recvfrom(65565))

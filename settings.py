from threading import Lock

# netcard
NETCARD = ''
NETCARD_LIST = {}

# 过滤规则
FILTER = ''

# 多个线程对象
# to send pc information
pcinfo_thread = None
pcinfo_thread_lock = Lock()

# to send notification
notify_thread = None
notify_thread_lock = Lock()

# to sniff
sniff_thread = None
sniff_thread_lock = Lock()

# to...

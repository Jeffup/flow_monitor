from flask_socketio import emit

from App.function import thread_of_pcinfo, thread_of_sniff
from App.function.sendMsg import projectStart_Msg, projectStop_Msg
from settings import pcinfo_thread_lock, pcinfo_thread, sniff_thread_lock, sniff_thread


def init_socket(socketio):
    @socketio.on('startpc', namespace='/capture')
    def pcinfo(data):
        global pcinfo_thread, pcinfo_thread_lock
        if data['data']=='start':
            if projectStart_Msg():
                with pcinfo_thread_lock:
                    print("OK!")
                    if pcinfo_thread is None:
                        # 开一个后台线程
                        pcinfo_thread = socketio.start_background_task(thread_of_pcinfo())
            else:
                return
        else:
            if pcinfo_thread is not None:
                # stop it!
                projectStop_Msg()

    @socketio.on('startsniff', namespace='/capture')
    def packetinfo(data):
        global sniff_thread, sniff_thread_lock
        if data['data'] == 'start':
            if projectStart_Msg():
                with sniff_thread_lock:
                    print("OK!")
                    if sniff_thread is None:
                        # 开一个后台线程
                        sniff_thread = socketio.start_background_task(thread_of_sniff())
            else:
                return
        else:
            if sniff_thread is not None:
                # stop it!
                projectStop_Msg()

    @socketio.on('my_event', namespace='/capture')
    def hello(data):
        print(data)
        emit('testresponse', data)

from flask_socketio import emit

from App.function.getComInfo import get_netcard
from settings import NETCARD, FILTER


class NotifyMsg:
    title = ''
    text = ''
    level = 0

    def json(self):
        if self.level > 3:
            self.level = 3
        elif self.level < 0:
            self.level = 0
        json_data = {'title': self.title, 'data': self.text, 'level': self.level}
        return json_data


def sendNotify(msg):
    '''
    if danger do color and icon, and link to the detail view if that is possible
    first str: danger level
    second str: icon name
    third str: title
    forth str: 简述
    :param msg: eg:{title: '' , data: '' , level = numer[0:3]}
    :return:
    '''
    if msg['level'] not in range(0, 4):
        return
    if msg['data'].__len__() > 120:
        data = msg['data'][:118] + '...'
    else:
        data = msg['data']
    iconlist = ['bell', 'info-sign', 'exclamation-sign', 'warning-sign']
    dangerlist = ['default', 'info', 'warning', 'danger']
    sendmsg = '''
                             <div class="media list-group-item-%s">
                          <div class="media-left">
                              <span class="glyphicon glyphicon-%s"></span>
                          </div>
                          <div class="media-body">
                            <h4 class="media-heading">%s</h4>
                            %s
                          </div>
                        </div>
    ''' % (dangerlist[msg['level']], iconlist[msg['level']], msg['title'], data)

    emit('notify_response', {'msg': sendmsg, 'data': msg['data']}, namespace='/capture')

def inspectNetcard():
    nm = NotifyMsg()
    if NETCARD == '':
        nm.title = '网卡不存在'
        nm.text = '可能情况有：1. 网卡没有设置 2.没有找到您所设置的网卡。建议您在设置中重新设置网卡！'
        nm.level = 1
        sendNotify(nm.json())
        return False
    return True


def projectStart_Msg():
    nm = NotifyMsg()
    if inspectNetcard():
        nm.title = '项目已启动'
        nm.text = '配置信息如下：1. 网卡：%s ；2. 过滤规则：%s'%(NETCARD, FILTER)
        nm.level = 0
        sendNotify(nm.json())
        return True
    else:
        nm.title = '项目启动失败'
        nm.text = '可能情况有：网卡设置不正确'
        nm.level = 1
        sendNotify(nm.json())
        return False


def projectStop_Msg():
    nm = NotifyMsg()
    nm.title = '项目已暂停'
    nm.text = '项目已暂停'
    nm.level = 0
    sendNotify(nm.json())

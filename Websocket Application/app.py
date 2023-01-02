from aiohttp import web
import socketio
import time

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

ip_allowed = ['127.0.0.1']


@sio.event
async def connect(sid, environ):
    if environ["REMOTE_ADDR"] not in ip_allowed:
        print(environ["REMOTE_ADDR"],' trying to connect.')
        await sio.emit('forceDisconnect','Not allowed to connect.')
    else:
        print("connect ", sid)

@sio.event
async def login(sid,data):
    time.sleep(4)
    sio.enter_room(sid,data['userkey'])
    cars = ['Lexus','Honda']
    msg = "Select The Car"
    await sio.emit('next',{"msg":msg,"data":cars},room=data["userkey"])





@sio.event
def disconnect(sid):
    sio.leave_room(sid,'shreyash123456')
    print('disconnect ', sid)

if __name__ == '__main__':
    #app.run(port=5050)
    web.run_app(app)
    print(sio.sid)
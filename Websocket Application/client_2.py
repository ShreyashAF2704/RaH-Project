import socketio
import asyncio
import time 
import aiohttp

sio = socketio.AsyncClient()

@sio.on('*')
def catch_all(event, sid):
    print("Event Not found",event,sid)


@sio.event
async def next(data):
    print(data["msg"])
    
    time.sleep(20)
    await sio.emit('disconnect',{'return':'relation','node':data},)


@sio.event
async def connect():
    print("I'm connected!")
    print("My Sid: ",sio.sid)
    await sio.emit('login',{'userkey':'shreyash123456'})

async def main():
    await sio.connect('http://localhost:8080')
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())

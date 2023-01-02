# Async Socket Client
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
    for i in range(len(data["data"])):
        print(f"Type {i} for :",data["data"][i]["Name"])
    time.sleep(4)
    res = int(input("Type : "))
    #print(data["data"][res])
    await sio.emit('get_data',{'return':'relation','node':data["data"][res]})


@sio.event
async def return_data(msg):
    print("[Question] : ",msg['question'])
    print("----------------------")
    if len(msg["data"]) == 0:
        await sio.emit('my_response','Thank You.')
    else:
        for i in range(len(msg["data"])):
            print(f"Type {i} for :",msg["data"][i][0])
        print(f'Type {i+1} to exit.')
        res = int(input("Type: "))
        if res == i+1:
            await sio.emit('my_response','Thank You.')
        else:
            #print(msg["data"][res][1])
            print("------------------------")
            await sio.emit('get_data',{'node':msg["data"][res][1]})

@sio.event
async def result_conversation(msg):
    print("[Question] : ",msg["question"])
    print("----------------------")
    for i in range(len(msg["data"])):
        print(f"Type {i} for :",msg["data"][i][0])
    print(f"Type {i+1} to exit.")
    res = int(input("Type: "))
    if res == i+1:
        await sio.emit('my_response','Thank You for your assistance')
    else:
        print("Possible Problem are realted to.")
        print(msg["data"][res][1])
        print("-----------------------")
        await sio.emit('my_response','Thank You for your assistance')


@sio.on(f"disconnectNow")
async def disconnectNow(msg):
    print(msg)
    time.sleep(2)
    await sio.disconnect()
    print("Client Disconnected")

@sio.event
async def forceDisconnect(msg):
    await sio.disconnect()
    print("Force Disconnected: ",msg)


#------------------------------------

@sio.event
async def connect():
    print("I'm connected!")
    await sio.emit('login',{'userkey':'shreyash123456'})
    
    
@sio.event
async def connect_error(data):
    print("The connection failed!")


#-------------------------------------

async def main():
    await sio.connect('http://localhost:8080')
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())




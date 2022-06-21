import websocket
import _thread
import time
import rel
import ast
import threading

from open_door import open_door,close_door
from save_new_faces import getting_new_faces

rel.safe_read()

socket_waiting = None

def on_message(ws, message):
    global socket_waiting
    massage1=ast.literal_eval(message)
    if(massage1["code"] == 1011):
        open_door()
        pass
    elif massage1["code"] == 1012:
        # on detect and open with them
        pass
    elif massage1["code"] == 1013:
        # off detect and open with them
        pass
    elif massage1["code"] == 1014:
        # add new member
        socket_waiting[0] = 1
        getting_new_faces()
        socket_waiting[0] = 0
        #idMember=massage1["id_member"]
        pass
    elif massage1["code"] == 1015:
        # update member
        socket_waiting[0] = 1
        getting_new_faces()
        socket_waiting[0] = 0
        #idMember = massage1["id_member"]
        pass
    elif massage1["code"] == 1016:
        # OK
        pass
    elif massage1["code"] == 1018:
        # delete member
        socket_waiting[0] = 1
        getting_new_faces()
        socket_waiting[0] = 0
        #idMember=massage1["id_member"]
        pass

    print(massage1["code"])
    print(massage1["massege"])



def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")


def start(socket_called):
    global socket_waiting
    socket_waiting = socket_called
    header={'token':'12345', 'serial-rasperypi':'1234567891234567'}
    ws = websocket.WebSocketApp("wss://smartvideodoorphoneproject.herokuapp.com/ws/open_door_websocket/",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                                on_close=on_close,
                                header=header
                                )

    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()
    

import requests
import Url
import cv2
import base64
def add_history(id_member,status,picture,waiting):
    waiting[1] = 1
    url = Url.base + Url.add_history
    
    retval, buffer = cv2.imencode('.jpg', picture)
    jpg_as_text = base64.b64encode(buffer)
        
    data = {"serial_rasperyPi": "1234567891234567",
            "token": "12345",
            "id_member": id_member,
            "request_status" : status,
            "picture" : str(jpg_as_text)[2:-1]
    }
    
    try :
        #x = requests.post(url, data = data)
        pass
    except:
        pass
    waiting[1] = 0
import Url
import requests
import json
import base64
import os
<<<<<<< HEAD
#from Diologs import noWifi
=======
# from Diologs import noWifi
>>>>>>> 8a98cede0e4e26a971f05df0dd9972117eda8811
import shutil


def saving_new_faces(users):
    if os.path.exists('faces'):
        shutil.rmtree('faces')

    os.makedirs('faces', mode=0o777)
    for user in users:
        name = user['name']
        folder = str(user['id']) + '(' + name + ')'
        path = os.path.join('faces', folder)
        if not os.path.exists('faces/' + folder):
            os.makedirs(path, mode=0o777)

            newfile = base64.b64decode(user['picture'][2:-1])
            filename = 'faces/' + folder + '/' + name + '.jpg'
            with open(filename, 'wb') as f:
                f.write(newfile)

    print('Done!')


def getting_new_faces():
    print('Getting Faces ...')
    url = Url.base + Url.get_new_faces
    data = {"serial_rasperyPi": "1234567891234567", "token": "12345", "id_member": "-1"}
    response_json = requests.post(url, data)
    response_data = json.loads(response_json.text)
    saving_new_faces(response_data["members"])


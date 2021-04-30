import os
import json


def generate_negative_description_file():
    with open('neg.text', 'w') as f:
        for filename in os.listdir('negative'):
            f.write("negative/" + filename + '\n')


def change_json_positive_to_text():
    f = open('face_annotation/annotations.json', "r")
    data = json.loads(f.read())
    f.close()

    with open('pos.text', 'w') as f:

        for i, p in enumerate(data):
            if i > 0:
                x1 = int(data[p]['instances'][0]['points']['x1'])
                y1 = int(data[p]['instances'][0]['points']['y1'])

                w = int(data[p]['instances'][0]['points']['x2']) - x1
                h = int(data[p]['instances'][0]['points']['y2']) - y1

                item = 'positive/' + p + ' ' + '1' + ' ' + str(x1) + ' ' + str(y1) + ' ' + str(w) + ' ' + str(h)
                f.write(item + '\n')


# change_json_positive_to_text()
    2
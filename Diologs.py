# from ui.wifi import Ui_wifi
# from ui.Confirmation import Ui_confirmation
# import re
# from PyQt5 import QtCore, QtGui, QtWidgets
# import Url
# import requests
# import partial
#
# def noWifi():
#     global dialog_wifi
#     dialog_wifi = QtWidgets.QDialog()
#     dialog_wifi.ui = Ui_wifi()
#
#     dialog_wifi.ui.setupUi(dialog_wifi)
#
#     dialog_wifi.setAttribute(QtCore.Qt.WA_DeleteOnClose)
#     dialog_wifi.exec_()
#
#
# def confirmation(uuid):
#     print(uuid)
#     try:
#         url = Url.base + Url.confirmation
#         data = {
#             'uuid': uuid,
#         }
#         requests.post(url, data=data)
#     except:
#         noWifi()
#     dialog_confirmation.close()
#
#
# def unconfirmation():
#     dialog_confirmation.close()
#
#
# def asking_for_confirmation(info):
#     global match, found, dialog_confirmation
#     match, found = None, False
#
#     name = re.search("\((.+)\)", info)[1]
#     uuid = re.sub(r"(\(.+\))", "", info)
#
#     dialog_confirmation = QtWidgets.QDialog()
#     dialog_confirmation.ui = Ui_confirmation()
#
#     dialog_confirmation.ui.setupUi(dialog_confirmation)
#
#     dialog_confirmation.ui.name.setText(name)
#
#     dialog_confirmation.ui.confim.clicked.connect(partial(confirmation, uuid=uuid))
#     dialog_confirmation.ui.unconfirm.clicked.connect(partial(unconfirmation))
#
#     dialog_confirmation.setAttribute(QtCore.Qt.WA_DeleteOnClose)
#
#     dialog_confirmation.exec_()
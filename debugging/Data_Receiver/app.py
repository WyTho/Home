import sys
from PyQt5.QtWidgets import QApplication, QDialog
from Dialogs.MainWindow import Ui_MainWindow
from Classes.TCPThread import TCPThread


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Ui_MainWindow()
    ui.setupUi(Dialog)
    socketThread = TCPThread(1, "Thread-1", 1)
    socketThread.subscribe(ui)
    socketThread.daemon = True
    socketThread.start()
    Dialog.show()
    sys.exit(app.exec_())

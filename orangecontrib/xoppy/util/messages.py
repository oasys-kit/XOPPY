###############################################################
#
# MESSAGING (copied from srw_util)
#
###############################################################

from PyQt5.QtWidgets import QMessageBox

def showConfirmMessage(message, informative_text, parent=None):
    msgBox = QMessageBox()
    if not parent is None: msgBox.setParent(parent)
    msgBox.setIcon(QMessageBox.Question)
    msgBox.setText(message)
    msgBox.setInformativeText(informative_text)
    msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msgBox.setDefaultButton(QMessageBox.No)

    return msgBox.exec_() == QMessageBox.Yes

def showWarningMessage(message, parent=None):
    msgBox = QMessageBox()
    if not parent is None: msgBox.setParent(parent)
    msgBox.setIcon(QMessageBox.Warning)
    msgBox.setText(message)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec_()

def showCriticalMessage(message, parent=None):
    msgBox = QMessageBox()
    if not parent is None: msgBox.setParent(parent)
    msgBox.setIcon(QMessageBox.Critical)
    msgBox.setText(message)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec_()
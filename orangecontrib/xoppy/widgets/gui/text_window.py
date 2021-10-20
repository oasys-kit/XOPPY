from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QDialog
from PyQt5.QtWidgets import QPlainTextEdit, QTextEdit


class TextWindow(QMainWindow):

    def __init__(self, parent=None, title="", file=""):
        QMainWindow.__init__(self, parent)

        left = 10
        top = 10
        width = 700
        height = 850
        self.setWindowTitle(title)
        self.setGeometry(left, top, width, height)

        self.text_edit = QPlainTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setFixedHeight(height-top)
        self.text_edit.setFixedWidth(width-left)

        if file != "":
            self.set_file(file)

        self.show()

    def clear(self):
        self.text_edit.setPlainText("")

    def set_text(self,text):
        self.clear()
        self.text_edit.setPlainText(text)

    def set_file(self,filename):
        text = open(filename).read()
        print("Displaying file: "+filename)
        self.setWindowTitle(filename)
        self.set_text(text)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])

    oo = TextWindow(file="/home/manuel/OASYS1.2/xoppy/orangecontrib/xoppy/util/doc_txt/us.txt")

    app.exec_()
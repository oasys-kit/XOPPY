import os, sys, code, itertools

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from orangewidget import gui
from oasys.widgets import gui as oasysgui

from PyQt5.QtWidgets import QWidget, QVBoxLayout

from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt


class PythonScript(QWidget):


    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.code_area = oasysgui.textArea(readOnly=False)
        self.code_area.setStyleSheet("background-color: white; font-family: Courier, monospace;")
        self.console = PythonConsole(self.__dict__, self)


        button_box = oasysgui.widgetBox(None, "", addSpace=True, orientation="horizontal")
        gui.button(button_box, self, "Run Script", callback=self.execute_script, height=40)
        gui.button(button_box, self, "Save Script to File", callback=self.save_script, height=40)

        layout.addWidget(self.code_area)
        layout.addWidget(self.console)
        layout.addWidget(button_box)

        self.setLayout(layout)


    def execute_script(self):
        self._script = str(self.code_area.toPlainText())
        self.console.write("\nRunning script:\n")
        self.console.push("exec(_script)")
        self.console.new_prompt(sys.ps1)

    def save_script(self):
        file_name = QFileDialog.getSaveFileName(self, "Save File to Disk", os.getcwd(), filter='*.py')[0]

        if not file_name is None:
            if not file_name.strip() == "":
                if os.path.splitext(file_name)[1].lower() != ".py":
                    file_name += ".py"
                file = open(file_name, "w")
                file.write(str(self.code_area.toPlainText()))
                file.close()

                QtWidgets.QMessageBox.information(self, "Information",
                                              "File " + file_name + " written to disk",
                                              QtWidgets.QMessageBox.Ok)


    def clear(self):
        self.code_area.setText("")

    def set_code(self,text):
        self.clear()

        try:
            self.code_area.setText(text)
        except Exception as e:
            self.code_area.setText("Problem in writing python script:\n" + str(sys.exc_info()[0]) + ": " + str(sys.exc_info()[1]))

    def add_code(self,text):
        code_old = self.get_code()
        self.set_code(code_old + "\n" + text)

    def get_code(self):
        return self.code_area.toPlainText()


def interleave(seq1, seq2):
    """
    Interleave elements of `seq2` between consecutive elements of `seq1`.

        >>> list(interleave([1, 3, 5], [2, 4]))
        [1, 2, 3, 4, 5]

    """
    iterator1, iterator2 = iter(seq1), iter(seq2)
    leading = next(iterator1)
    for element in iterator1:
        yield leading
        yield next(iterator2)
        leading = element

    yield leading


class PythonConsole(QtWidgets.QPlainTextEdit, code.InteractiveConsole):
    def __init__(self, locals=None, parent=None):
        QtWidgets.QPlainTextEdit.__init__(self, parent)
        code.InteractiveConsole.__init__(self, locals)
        self.history, self.historyInd = [""], 0
        self.loop = self.interact()
        next(self.loop)
        self.setStyleSheet("background-color:black; color: white; font-family: Courier, monospace;")

    def setLocals(self, locals):
        self.locals = locals


    def flush(self):
        pass

    def interact(self, banner=None):
        try:
            sys.ps1
        except AttributeError:
            sys.ps1 = ">>> "
        try:
            sys.ps2
        except AttributeError:
            sys.ps2 = "... "
        cprt = ('Type "help", "copyright", "credits" or "license" '
                'for more information.')
        if banner is None:
            self.write("Python %s on %s\n%s\n(%s)\n" %
                       (sys.version, sys.platform, cprt,
                        self.__class__.__name__))
        else:
            self.write("%s\n" % str(banner))
        more = 0
        while 1:
            try:
                if more:
                    prompt = sys.ps2
                else:
                    prompt = sys.ps1
                self.new_prompt(prompt)
                yield
                try:
                    line = self.raw_input(prompt)
                except EOFError:
                    self.write("\n")
                    break
                else:
                    more = self.push(line)
            except KeyboardInterrupt:
                self.write("\nKeyboardInterrupt\n")
                self.resetbuffer()
                more = 0

    def raw_input(self, prompt):
        input = str(self.document().lastBlock().previous().text())
        return input[len(prompt):]

    def new_prompt(self, prompt):
        self.write(prompt)
        self.newPromptPos = self.textCursor().position()

    def write(self, data):
        cursor = QTextCursor(self.document())
        cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
        cursor.insertText(data)
        self.setTextCursor(cursor)
        self.ensureCursorVisible()

    def writelines(self, lines):
        for line in lines:
            self.write(line)

    def push(self, line):
        if self.history[0] != line:
            self.history.insert(0, line)
        self.historyInd = 0

        saved = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = self, self
            return code.InteractiveConsole.push(self, line)
        finally:
            sys.stdout, sys.stderr = saved

    def setLine(self, line):
        cursor = QTextCursor(self.document())
        cursor.movePosition(QTextCursor.End)
        cursor.setPosition(self.newPromptPos, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        cursor.insertText(line)
        self.setTextCursor(cursor)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.write("\n")
            next(self.loop)
        elif event.key() == Qt.Key_Up:
            self.historyUp()
        elif event.key() == Qt.Key_Down:
            self.historyDown()
        elif event.key() == Qt.Key_Tab:
            self.complete()
        elif event.key() in [Qt.Key_Left, Qt.Key_Backspace]:
            if self.textCursor().position() > self.newPromptPos:
                QtWidgets.QPlainTextEdit.keyPressEvent(self, event)
        else:
            QtWidgets.QPlainTextEdit.keyPressEvent(self, event)

    def historyUp(self):
        self.setLine(self.history[self.historyInd])
        self.historyInd = min(self.historyInd + 1, len(self.history) - 1)

    def historyDown(self):
        self.setLine(self.history[self.historyInd])
        self.historyInd = max(self.historyInd - 1, 0)

    def complete(self):
        pass

    def _moveCursorToInputLine(self):
        """
        Move the cursor to the input line if not already there. If the cursor
        if already in the input line (at position greater or equal to
        `newPromptPos`) it is left unchanged, otherwise it is moved at the
        end.

        """
        cursor = self.textCursor()
        pos = cursor.position()
        if pos < self.newPromptPos:
            cursor.movePosition(QTextCursor.End)
            self.setTextCursor(cursor)

    def pasteCode(self, source):
        """
        Paste source code into the console.
        """
        self._moveCursorToInputLine()

        for line in interleave(source.splitlines(), itertools.repeat("\n")):
            if line != "\n":
                self.insertPlainText(line)
            else:
                self.write("\n")
                next(self.loop)

    def insertFromMimeData(self, source):
        """
        Reimplemented from QPlainTextEdit.insertFromMimeData.
        """
        if source.hasText():
            self.pasteCode(str(source.text()))
            return



if __name__ == "__main__":

    from PyQt5.QtWidgets import QApplication
    app = QApplication([])

    widget = QWidget()

    layout = QVBoxLayout()

    oo = PythonScript()

    oo.set_code("print('Hello world')\n")
    oo.add_code("print('Hello moon')\n")


    print(">>",oo.get_code())

    layout.addWidget(oo)

    widget.setLayout(layout)

    widget.show()

    app.exec_()

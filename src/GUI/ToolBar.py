
from PyQt5.QtWidgets import QToolBar, QAction, QMessageBox, QDialog, QVBoxLayout, QTextEdit

from src.GUI import OpenSave
from src.GUI.HeaderInfoLookUp import LookupTableThread, LookupTableWindow


class Toolbar(QToolBar):
    """
    A dialog window to display raw VCF data.
    """
    def __init__(self, parent, main_window):
        """
        Initialize the RawDataWindow with the given raw data.

        Args:
            raw_data (str): The raw VCF data to be displayed.
        """
        super().__init__("Main toolbar", parent)
        self.main_window = main_window  # Store the reference to MainWindow
        self.initUI()
        self.raw_vcf_text = None

        self.lookup_thread = None  # Initialize the thread as None
        self.lookup_window = None  # Initialize the lookup window as None



    def initUI(self):
        """
        Initialize the UI components for the RawDataWindow.
        (is also dragable to a prefered side of the main window (BUT you can drag it out freely even out of the mainwindow))

        Args:
            raw_data (str): The raw VCF data to be displayed.
        """
        button_action = QAction("Quicksave", self)
        button_action.setStatusTip("Quicksave")
        button_action.triggered.connect(self.onQuickSave)

        button_action2 = QAction("Refresh", self)
        button_action2.setStatusTip("Refresh the Table")
        button_action2.triggered.connect(self.onRefresh)

        #create a show raw data (var file as text)
        button_action3 = QAction("Show Raw Data", self)
        button_action3.setStatusTip("Display Raw Data of file as txt-box")
        button_action3.triggered.connect(self.showRawData)

        #lookup table for header info/columns
        button_action4 = QAction("Show Lookup Table", self)
        button_action4.setStatusTip("Display VCF Lookup Table")
        button_action4.triggered.connect(self.showLookupTable)

        self.addAction(button_action)
        self.addAction(button_action2)
        self.addAction(button_action3)
        self.addAction(button_action4)

    #function for toolbar placeholder
    def onMyToolBarButtonClick(self, s):
        print("click", s)

    #just uses the normal save as csv
    def onQuickSave(self):
        OpenSave.save_as_csv(self)

    def loadVCFFile(self, file_path):
        #load the file and set self.raw_vcf_data
        with open(file_path, 'r') as f:
            self.raw_vcf_data = f.read()


    def onRefresh(self):
        """
        Refreshes the table columns
        (if all were hidden -> shows them)
        """
        if hasattr(self.main_window, 'showAllColumns'):
            self.main_window.showAllColumns()
        else:
            QMessageBox.warning(self, "Error", " ")


    def setRawVCFData(self, vcf_text):
        self.raw_vcf_text = vcf_text

    def showRawData(self):
        """
        Displays the raw file data in a Msg Box
        """
        if not self.raw_vcf_text:
            QMessageBox.warning(self, "Error", "You need to open a VCF file first.")
            return
        raw_data_dialog = RawDataWindow(self.raw_vcf_text)
        raw_data_dialog.exec_()

    #thread handeling stuff so main window GUI can still function
    def showLookupTable(self):
        if self.lookup_window is None:
            self.lookup_thread = LookupTableThread()
            self.lookup_thread.dataReady.connect(self.displayLookupTable)
            self.lookup_thread.start()

    def displayLookupTable(self, lookup_data):
        self.lookup_window = LookupTableWindow(lookup_data)
        self.lookup_window.show()

        self.lookup_window.finished.connect(self.cleanupLookupWindow)

    def cleanupLookupWindow(self):
        self.lookup_window = None
        self.lookup_thread = None



class RawDataWindow(QDialog):
    """
    Defines the Popup Window in witch the raw file data gets displayed
    """
    def __init__(self, raw_data):
        super().__init__()
        self.initUI(raw_data)

    def initUI(self, raw_data):
        self.setWindowTitle('Raw VCF Data')
        self.setGeometry(200, 200, 800, 600)

        layout = QVBoxLayout()
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setPlainText(raw_data)

        layout.addWidget(self.textEdit)
        self.setLayout(layout)
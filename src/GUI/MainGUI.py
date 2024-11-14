import sys, os
import time

from PyQt5.QtGui import QDesktopServices
#import things from PyQt libraries
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QAbstractItemView, QMenu, QFileDialog,
    QPushButton, QHBoxLayout, QCheckBox, QMessageBox, QLineEdit,
    QLabel, QHeaderView, QGridLayout, QDialog, QTextEdit, QTableWidget, QTabWidget, QToolBar, QAction, QStatusBar,
    QComboBox, QDoubleSpinBox, QSpinBox, QProgressBar, QGroupBox, QTextBrowser, QToolTip,

)

from PyQt5.QtCore import (Qt, QSettings, QThread, pyqtSignal, QTimer, QSortFilterProxyModel, QEvent, QUrl)

from typing import List, Dict
from src.GUI.FilterSection.LayoutFilter import LayoutFilter
from src.GUI.SettingsSection.SettingManager import SettingsManager
from src.GUI.TaskBar import TaskBar
from src.util.parseVCF import parseVCFfile
from src.util.config import load_config
from src.GUI.OpenSave import *
from src.GUI.ToolBar import Toolbar
from src.GUI.FetchDataWorker import FetchDataWorker
from src.GUI.FilterSection.FilteringLogic import FilteringLogic




vcf_dataEmpty = " "


# VCF data as a string (normaly this would be read from a file)
vcf_dataExample = """\

#CHROM	POS	ID	REF	ALT	    QUAL	FILTER	INFO	FORMAT	NA12878_73
chr1	2556714	.	A	G	5200	.	MQM=60;SAP=23;SAR=123;SAF=80;ABP=19	GT:DP:AO:GQ	0/1:465:203:136
chr1	2559766	.	C	T	4507	off-target	MQM=60;SAP=262;SAR=17;SAF=164;ABP=13	GT:DP:AO:GQ	0/1:324:181:138
chr1	2562891	.	G	A	10042	.	MQM=60;SAP=228;SAR=310;SAF=103;ABP=12	GT:DP:AO:GQ	0/1:886:413:141
chr1	2563346	.	G	A	3516	off-target	MQM=60;SAP=158;SAR=122;SAF=21;ABP=7	GT:DP:AO:GQ	0/1:265:143:136
chr1	4789324	.	T	C	7281	.	MQM=60;SAP=13;SAR=121;SAF=156;ABP=12	GT:DP:AO:GQ	0/1:603:277:160
chr1	4895802	.	C	T	12548	.	MQM=60;SAP=32;SAR=209;SAF=291;ABP=58	GT:DP:AO:GQ	0/1:1172:500:160
chr1	4896010	.	T	C	584	off-target	MQM=60;SAP=70;SAR=31;SAF=0;ABP=3	GT:DP:AO:GQ	0/1:62:31:144
chr1	6197766	.	T	C	9275	.	MQM=60;SAP=321;SAR=308;SAF=72;ABP=44	GT:DP:AO:GQ	0/1:889:380:133
chr1	6197796	.	G	A	6672	off-target	MQM=60;SAP=451;SAR=263;SAF=21;ABP=10	GT:DP:AO:GQ	0/1:611:284:160
chr1	7374483	.	C	T	7314	.	MQM=60;SAP=3;SAR=140;SAF=148;ABP=45	GT:DP:AO:GQ	0/1:691:288:133
chr1	7460069	.	C	T	14337	.	MQM=60;SAP=7;SAR=297;SAF=264;ABP=28	GT:DP:AO:GQ	0/1:1242:561:133
chr1	7460198	.	C	T	3075	off-target	MQM=60;SAP=260;SAR=130;SAF=4;ABP=4	GT:DP:AO:GQ	0/1:278:134:160
chr1	9717393	.	G	GGA	1496	off-target	MQM=60;SAP=101;SAR=2;SAF=51;ABP=0	GT:DP:AO:GQ	1/1:55:53:153
chr1	9721354	.	C	G	14379	off-target	MQM=60;SAP=75;SAR=280;SAF=159;ABP=0	GT:DP:AO:GQ	1/1:439:439:160
chr1	9722498	.	C	T	20652	off-target	MQM=60;SAP=149;SAR=218;SAF=426;ABP=0	GT:DP:AO:GQ	1/1:644:644:143
chr1	11127836	.	T	C	18630	off-target	MQM=60;SAP=192;SAR=404;SAF=179;ABP=0	GT:DP:AO:GQ	1/1:583:583:160
chr1	11145001	.	C	T	34108	.	MQM=60;SAP=37;SAR=455;SAF=583;ABP=0	GT:DP:AO:GQ	1/1:1038:1038:147
"""



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        gui_config = load_config("config/gui.ini", "gui")
        self.settings_manager = SettingsManager()
        # self.qual_cutoff = int(gui_config["qual_cutoff"])
        self.vep_placeholder = gui_config["vep_placeholder"]

        # Loading qual cutoff from gui.ini
        self.qual_cutoff = self.settings_manager.load_setting('qual_cutoff', 0, int)

        # Dictionary to keep track of sort orders
        self.sort_orders = {}
        
        self.initUI()
        self.initFilters()
        # Initial filtering
        self.filterTable()

    filtered_data = [] # all data except with hard QUAL cutoff
    filterList = []
    
    headers_vcf = ["#CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "MQM", "SAP", "SAR", "SAF", "ABP", "GT", "DP", "AO", "GQ"]
    # headers_vep = ["AlphaMissense", "cadd", "spliceaAI", "gencode_basic", "hgvs", "mane", "gene_id", "gene_symbol", "gene_symbol_source", "hgnc_id", "clin_sig"
    #                    , "clin_sig_allele", "phenotype_or_disease"]
    
    headers_vep = ['clinical significance',
        'gnomAD amr',
        'gnomAD nfe',
        'gnomAD sas',
        'gnomAD afr',
        'gnomAD eas',
        'impact',
        'consequence terms',
        'gene symbol']

    vep_placeholder = "...#placeholder#..."
    #qual_cutoff  = 0


    def initUI(self):
        # Set the window geometry
        self.setGeometry(100, 100, 1600, 800)
        # Set the window title
        self.setWindowTitle('GUI')


        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        # Matrix/ grid layout with individual cells (for more see PyQt docs)
        self.gridLayout = QGridLayout()
        centralWidget.setLayout(self.gridLayout)

        # Adding widgets to the grid layout
        # Table at top left Corner
        self.createTable()
        self.gridLayout.addWidget(self.tableWidget, 0, 0)

        # Adding side panel at top right corner cell
        self.filterSidePanel = QVBoxLayout()
        self.addWidgetsToSidePanel()
        self.gridLayout.addLayout(self.filterSidePanel, 0, 10)

        # For displaying Headerinfos
        #self.gridLayout.addWidget(self.displayHeaderInfo(), 1,0)


        # Stretching the second column of the grid
        # (stretch column 1 to occupy twice the space of column 0)
        self.gridLayout.setColumnStretch(0, 2)

        self.toolbar = Toolbar(self,self)

        self.addToolBar(self.toolbar)

        self.setStatusBar(QStatusBar(self))

        # add taskbar
        self.taskbar = TaskBar(self, self.settings_manager)
        self.setMenuBar(self.taskbar)


        #Progressbar for API calling
        self.progressBar = QProgressBar()
        self.statusBar().addPermanentWidget(self.progressBar)
        self.progressBar.setVisible(False)  # Initially hidden


        # Create 3 labels
        self.rowInfoLabel1 = QLabel()
        self.rowInfoLabel1.setText("Click vertical Header rows to display Info")
        self.rowInfoLabel1.setTextFormat(Qt.RichText)
        self.rowInfoLabel1.setAlignment(Qt.AlignTop)

        self.rowInfoLabel2 = QLabel()
        self.rowInfoLabel2.setTextFormat(Qt.RichText)
        self.rowInfoLabel2.setAlignment(Qt.AlignTop)

        self.rowInfoLabel3 = QLabel()
        self.rowInfoLabel3.setTextFormat(Qt.RichText)
        self.rowInfoLabel3.setAlignment(Qt.AlignTop)

        # Add the labels to the layout
        self.hboxLayout = QHBoxLayout()
        self.hboxLayout.addWidget(self.rowInfoLabel1)
        self.hboxLayout.addWidget(self.rowInfoLabel2)
        self.hboxLayout.addWidget(self.rowInfoLabel3)

        # Add the hbox layout to the grid layout
        #self.gridLayout.addLayout(self.hboxLayout, 2, 10)


        self.tableWidget.verticalHeader().sectionClicked.connect(self.displayRowInfo)


        header_container = QWidget()
        header_layout = QHBoxLayout(header_container)

        # Add header text and row info to the container layout
        header_layout.addWidget(self.displayHeaderInfo())
        header_layout.addWidget(self.rowInfoLabel1)
        header_layout.addWidget(self.rowInfoLabel2)
        header_layout.addWidget(self.rowInfoLabel3)

        # For displaying Headerinfos
        #self.gridLayout.addWidget(self.displayHeaderInfo(), 1,0)

        # Add the container to the grid layout
        self.gridLayout.addWidget(header_container, 1, 0)




        # Tooltip for column headers
        self.tableWidget.horizontalHeader().setToolTip("Click to sort ascending/descending")


        # For displaying links to other tools and websites
        self.linksLabel = QLabel()
        self.linksLabel.setTextFormat(Qt.RichText)
        self.linksLabel.setAlignment(Qt.AlignTop)
        self.linksLabel.setText("Other Websites/Tools: <a href='https://igv.org/'>IGV</a> , "
                                "<a href='https://www.omim.org/'>OMIM</a> , "
                                "<a href='https://www.ncbi.nlm.nih.gov/clinvar/'>ClinVar</a> , "
                                "<a href='https://www.ensembl.org/index.html'>Ensembl</a> , "
                                "<a href='https://www.ncbi.nlm.nih.gov/snp/'>dbSNP</a> , "
                                "<a href='https://www.genecards.org/'>GeneCards</a>  "
                                )
        # can adjust the row and column span
        self.gridLayout.addWidget(self.linksLabel, 3, 0)

        # so links can be clicked and opened
        self.linksLabel.setOpenExternalLinks(True)
        self.linksLabel.linkActivated.connect(self.openLink)

        # To make window visiable
        self.show()

        # Start fetching data in a separate thread
        #self.fetchVEPData()


    #function to create Table with all functions
    def createTable(self):
        # initialize the table widget
        self.tableWidget = QTableWidget()

        # Set the column count
        self.tableWidget.setColumnCount(75) # FIXME: should not be hardcoded

        # Set the horizontal header labels
        self.tableWidget.setHorizontalHeaderLabels(self.headers_vcf + self.headers_vep)

        self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked)
        # Enable default sorting behavior
        self.tableWidget.setSortingEnabled(False)

        self.tableWidget.horizontalHeader().setSectionsMovable(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)






        self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.tableWidget.setSortingEnabled(False)  # Enable default sorting behavior

        self.tableWidget.horizontalHeader().setSectionsMovable(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)


        # connect header section click to sort function
        self.tableWidget.horizontalHeader().sectionClicked.connect(self.onSectionClicked)

        #self.tableWidget.setSortingEnabled(True)





        # Enable interactive resizing of columns
        self.tableWidget.horizontalHeader().setSectionsMovable(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

        header = self.tableWidget.horizontalHeader()
        header.setSectionsMovable(True)
        header.setSectionResizeMode(QHeaderView.Interactive)
        # Add context menu to header
        header.setContextMenuPolicy(Qt.CustomContextMenu)
        header.customContextMenuRequested.connect(self.showHeaderMenu)


    def populateTableWithVCFData(self, vcf_data: list):
        """
        Populate the table widget with VCF data.
        :param vcf_data: Parsed VCF data as a dictionary
        """
        # Clear table widget (clear items and headers)
        self.tableWidget.clear()
        
        filtered_data = []

        # Filter out variants with QUAL below the cutoff
        for entry in vcf_data:
            if float(entry['QUAL']) >= self.qual_cutoff:
                filtered_data.append(entry)
            
        # Set the row count to the number of filtered lines
        self.tableWidget.setRowCount(len(filtered_data))

        # Initialize sets to store INFO and FORMAT column headers
        info_columns = set()
        format_keys = set()

        # First pass: Collect all possible INFO and FORMAT keys
        for item in filtered_data:
            info_fields = item['INFO'].split(';')
            info_dict = {key: value for key, value in (field.split('=') for field in info_fields if '=' in field)}
            info_columns.update(info_dict.keys())

            if 'FORMAT' in item:
                format_keys.update(item['FORMAT'].split(':'))

        # Sort the collected INFO and FORMAT keys for consistency
        info_columns = sorted(info_columns)
        format_keys = sorted(format_keys)

        # Combine headers: VCF columns, dynamic INFO and FORMAT keys, and VEP headers
        headers = (
                ["CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER"]
                + info_columns
                + format_keys
                + self.headers_vep  # Adding the VEP headers
        )

        # Set the column count based on the combined headers
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)

        # Second pass: Populate table rows
        for row in range(0, len(filtered_data)):
            item = filtered_data[row]
            # Extract INFO fields and create a dictionary
            info_fields = item['INFO'].split(';')
            info_dict = {key: value for key, value in (field.split('=') for field in info_fields if '=' in field)}

            # Split FORMAT and sample columns
            if 'FORMAT' in item:
                format_keys_list = item['FORMAT'].split(':')
                sample_column_name = 'NA12878_73' # FIXME get this dynamically at load of vcf file!!
                sample_column_name = 'unknown' # FIXME get this dynamically at load of vcf file!!
                sample_values = item[sample_column_name].split(':')
            else:
                format_keys_list = []
                sample_values = []

            # Placeholder for VEP data (ensure actual VEP data is included in `item`)
            vep_data = [str(item.get(col, self.vep_placeholder)) for col in self.headers_vep]

            # Combine the data into a single list for the row
            columns_data = (
                    [item.get(col, '') for col in ["CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER"]]
                    + [info_dict.get(col, '') for col in info_columns]
                    + [sample_values[format_keys_list.index(key)] if key in format_keys_list else '' for key in format_keys]
                    + vep_data
            )

            # Populate the table widget with the row data
            for col, val in enumerate(columns_data):
                self.tableWidget.setItem(row, col, QTableWidgetItem(val))

        # Store the filtered data
        self.filtered_data = filtered_data

        self.filterTable()


    # Helper function for opening/saving contents
    def openVCF_file(self):
        openFile(self)

    def openCSV_file(self):
        openCSVFile(self)

    def saveCSV_file(self):
        save_as_csv(self)

    def saveTXT_file(self):
        save_as_txt(self)

    def saveJSON_file(self):
        save_as_json(self)

    def saveHTML_file(self):
        save_as_html(self)


    # Adds the Filtersection
    def addWidgetsToSidePanel(self):
        layout_filter = LayoutFilter(self)
        self.filterSidePanel.addWidget(layout_filter)


    # series of functions to display visual loading while API calls are running
    def fetchVEPData(self):
        if(self.filtered_data == []):
            return
        self.progressBar.setVisible(True)
        self.progressBar.setRange(0, 0)
        self.statusBar().showMessage("Fetching data...")

        self.worker = FetchDataWorker(self.filtered_data)
        self.worker.dataFetched.connect(self.onDataFetched)
        self.worker.fetchStarted.connect(self.onFetchStarted)
        self.worker.fetchFailed.connect(self.onFetchFailed)
        self.worker.start()

    def onDataFetched(self, data):
        self.progressBar.setVisible(False)
        self.statusBar().showMessage("Data fetched successfully", 5000)
        print("data fetched successfully")
        self.populateTableWithVCFData(data)

    def onFetchStarted(self):
        print("Fetch started")

    def onFetchFailed(self, error):
        self.progressBar.setVisible(False)
        self.statusBar().showMessage("Error fetching data: " + error, 5000)


    # Function to display the additional Headerinfos at the start of a vcf file
    def displayHeaderInfo(self):
        # For displaying Headerinfos
        self.headerLabel = QTextEdit()
        self.headerLabel.setReadOnly(True)

        self.headerLabel.setFixedHeight(200)

        self.headerLabel.setFixedWidth(800)
        #self.gridLayout.addWidget(self.headerLabel, 1, 0)
        return self.headerLabel


    # Functions for sorting columns ascending/descending
    def onSectionClicked(self, index):
        try:
            current_order = self.sort_orders.get(index, Qt.AscendingOrder)
            new_order = Qt.DescendingOrder if current_order == Qt.AscendingOrder else Qt.AscendingOrder

            # Reorder the entire table based on the sorted column
            self.reorder_table(index, new_order)

            # Update the sort order for the column
            self.sort_orders[index] = new_order
        except Exception as e:
            print(f"Error occurred in onSectionClicked: {str(e)}")


    def reorder_table(self, column, order):
        try:
            # collect row data along with their original indices
            rows_data = []
            for row in range(self.tableWidget.rowCount()):
                if self.tableWidget.isRowHidden(row):
                    # Skip hidden row
                    continue

                row_data = [self.tableWidget.item(row, col).text() if self.tableWidget.item(row, col) else '' for col in range(self.tableWidget.columnCount())]
                # Store original row index and data
                rows_data.append((row, row_data))

            # Sort rows based on the specified column and order
            rows_data.sort(key=lambda x: self.parse_value(x[1][column]), reverse=(order == Qt.DescendingOrder))

            # Clear the table
            self.tableWidget.setRowCount(0)

            # Reinsert rows in sorted order
            for new_row_index, (original_row_index, row_data) in enumerate(rows_data):
                self.tableWidget.insertRow(new_row_index)
                for col, value in enumerate(row_data):
                    self.tableWidget.setItem(new_row_index, col, QTableWidgetItem(value))

            # Ensure the table reflects changes
            self.tableWidget.viewport().update()

        except Exception as e:
            print(f"Error occurred in reorder_table: {str(e)}")



    # Value conversion
    def parse_value(self, value):
        try:
            return float(value) if value else float('-inf')
        except ValueError:
            return value


    # might not be needed anymore
    def sort_numeric_column(self, column, order):
        try:
            # Collect and sort items
            rows = self.tableWidget.rowCount()
            items = [(row, self.tableWidget.item(row, column)) for row in range(rows)]
            items.sort(key=lambda x: self.to_numeric(x[1]), reverse=(order == Qt.DescendingOrder))

            # Reinsert sorted items back into the table
            for new_row, (row, item) in enumerate(items):
                self.tableWidget.setItem(new_row, column, item)

            # Ensure the table reflects changes
            self.tableWidget.viewport().update()
        except Exception as e:
            print(f"Error occurred in sort_numeric_column: {str(e)}")



    def to_numeric(self, item):
        try:
            return float(item.text()) if item and item.text() else float('-inf')
        except ValueError:
            return float('-inf')



    # function to rightclick column headers (show/hide/all)
    def showHeaderMenu(self, pos):
        header = self.tableWidget.horizontalHeader()
        try:
            logicalIndex = header.logicalIndexAt(pos)
            if logicalIndex < 0 or logicalIndex >= self.tableWidget.columnCount():
                return  # for invalid index, exit early

            menu = QMenu(self)

            hideAction = QAction(f"Hide {self.tableWidget.horizontalHeaderItem(logicalIndex).text()} Column", self)
            hideAction.triggered.connect(lambda: self.hideColumn(logicalIndex))
            menu.addAction(hideAction)

            showMenu = QMenu("Show Column", self)
            for i in range(self.tableWidget.columnCount()):
                if self.tableWidget.isColumnHidden(i):
                    showAction = QAction(self.tableWidget.horizontalHeaderItem(i).text(), self)
                    showAction.triggered.connect(lambda _, col=i: self.showColumn(col))
                    showMenu.addAction(showAction)

            showAllAction = QAction("Show All Columns", self)
            showAllAction.triggered.connect(self.showAllColumns)
            menu.addAction(showAllAction)

            menu.addMenu(showMenu)
            menu.exec_(header.mapToGlobal(pos))

        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {e}")


    # General Helper functions
    def hideColumn(self, col):
        self.tableWidget.hideColumn(col)

    def showColumn(self, col):
        self.tableWidget.showColumn(col)

    def showAllColumns(self):
        for i in range(self.tableWidget.columnCount()):
            self.tableWidget.showColumn(i)



    def get_cell_value_by_column_name(self, row_ind, column_name) -> str:
        # Find the column index for the given column name
        column_index = -1
        for col in range(self.tableWidget.columnCount()):
            header_item = self.tableWidget.horizontalHeaderItem(col)
            if header_item and header_item.text() == column_name:
                column_index = col
                break
        
        # If the column was found, get the cell value
        if column_index != -1:
            item = self.tableWidget.item(row_ind, column_index)
            if item:
                return item.text()
        
        return ""
        
    def filterTable(self):
        self.filterLogic.filterTable(self.tableWidget)
        
    def initFilters(self):
        self.filterLogic = FilteringLogic(self.filterList)



    # Cleanup here or other functions before closing Application
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Confirm Exit', 'Are you sure you want to exit? \n (Unsaved changes will be lost)',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()



    # Function for parsing a single row to label
    def displayRowInfo(self, row):
        try:
            # columns to display
            columns_to_display = [0, 2, 4, 6, 7, 8 , 9 , 10, 11, 12, 13, 14, 65,66,67,68,69,70,71,72,73]


            row_data = []
            for col in columns_to_display:
                item = self.tableWidget.item(row, col)
                if item:
                    header = self.tableWidget.horizontalHeaderItem(col).text()
                    value = item.text()
                    row_data.append(f"<b>{header}:</b> {value}<hr>")

            # Split the data into 3 parts
            part1 = "".join(row_data[:len(row_data)//3])
            part2 = "".join(row_data[len(row_data)//3:2*len(row_data)//3])
            part3 = "".join(row_data[2*len(row_data)//3:])

            # Update the labels
            self.rowInfoLabel1.setText(part1)
            self.rowInfoLabel2.setText(part2)
            self.rowInfoLabel3.setText(part3)

        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred while displaying row info: {str(e)}")

    # needed for links to work
    def openLink(self, link):
        QDesktopServices.openUrl(QUrl(link))


# Some things needed for application to work/show
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    #simulate fetching data on startup
    #window.fetchData()

    sys.exit(app.exec_())

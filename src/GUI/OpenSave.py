"""
File handling functions for opening and saving files.

This module provides functions for opening VCF and CSV files, and saving data to CSV, TXT, JSON, and HTML files.
These functions only save what is currently seen on the table.
"""
import csv, json

from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem

from src.util.parseVCF import parseVCFfile



def openFile(self, filename=None):
    """
    Opens a VCF file and populates the table with the parsed data.

    Args:
        self: The main window instance.
    """
    if not filename:
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '.', 'VCF Files (*.vcf);;All Files (*)')
    if filename:
        #read the file content as text
        with open(filename, 'r') as file:
            vcf_text = file.read()
        #use the parseVCFfile function to get the VCF data
        vcf_data = parseVCFfile(filename, '\t', 'list')
        #store the parsed VCF data
        self.raw_vcf_data = vcf_data
        #set the raw VCF data in the toolbar
        if hasattr(self.toolbar, 'setRawVCFData'):
            self.toolbar.setRawVCFData(vcf_text)
        headers = '\n'.join(vcf_data['header'])
        self.headerLabel.setText(headers)
        #pass the parsed data to populateTableWithVCFData
        self.populateTableWithVCFData(vcf_data['data'])



# Function to open a CSV file and populate the table
def openCSVFile(self):
    """
    Opens a CSV file and populates the table with the parsed data.

    Args:
        self: The main window instance.
    """
    filename, _ = QFileDialog.getOpenFileName(self, 'Open CSV File', '.', 'CSV Files (*.csv);')
    if filename:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            csv_data = list(reader)

            #clear the table before loading new data
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)

            # set the headers
            if csv_data:
                self.tableWidget.setColumnCount(len(csv_data[0]))
                self.tableWidget.setHorizontalHeaderLabels(csv_data[0])

                #populate the table with data
                for row_index, row_data in enumerate(csv_data[1:]):  #skip header row
                    self.tableWidget.insertRow(row_index)
                    for col_index, cell_data in enumerate(row_data):
                        self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(cell_data))

            #clear the table before loading new data
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)

def save_as_csv(self):
    """
    Saves the table data to a CSV file.

    Args:
        self: The main window instance.
    """
    filename, _ = QFileDialog.getSaveFileName(self, 'Save as CSV', '.', 'CSV Files (*.csv);;All Files (*)')
    if filename:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            # Write headers
            headers = [self.tableWidget.horizontalHeaderItem(i).text() for i in range(self.tableWidget.columnCount())]
            writer.writerow(headers)
            # Write data for visible rows
            for row in range(self.tableWidget.rowCount()):
                if self.tableWidget.isRowHidden(row):
                    continue
                row_data = []
                for col in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(row, col)
                    row_data.append(item.text() if item else '')
                writer.writerow(row_data)


def save_as_txt(self):
    """
    Saves the table data to a TXT file.

    Args:
        self: The main window instance.
    """
    filename, _ = QFileDialog.getSaveFileName(self, 'Save as TXT', '.', 'Text Files (*.txt);;All Files (*)')
    if filename:
        with open(filename, 'w') as f:
            # Write headers
            headers = '\t'.join([self.tableWidget.horizontalHeaderItem(i).text() for i in range(self.tableWidget.columnCount())])
            f.write(headers + '\n')
            # Write data for visible rows
            for row in range(self.tableWidget.rowCount()):
                if self.tableWidget.isRowHidden(row):
                    continue
                row_data = []
                for col in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(row, col)
                    row_data.append(item.text() if item else '')
                f.write('\t'.join(row_data) + '\n')



def save_as_json(self):
    """
    Saves the table data to a JSON file.

    Args:
        self: The main window instance.
    """
    filename, _ = QFileDialog.getSaveFileName(self, 'Save as JSON', '.', 'JSON Files (*.json);;All Files (*)')
    if filename:
        data = []
        headers = [self.tableWidget.horizontalHeaderItem(i).text() for i in range(self.tableWidget.columnCount())]
        for row in range(self.tableWidget.rowCount()):
            if self.tableWidget.isRowHidden(row):
                continue
            row_data = {}
            for col, header in enumerate(headers):
                item = self.tableWidget.item(row, col)
                row_data[header] = item.text() if item else ''
            data.append(row_data)

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)


def save_as_html(self):
    """
    Saves the table data to as a HTML file.

    Args:
        self: The main window instance.
    """
    filename, _ = QFileDialog.getSaveFileName(self, 'Save as HTML', '.', 'HTML Files (*.html);;All Files (*)')
    if filename:
        with open(filename, 'w') as f:
            f.write('<html><body><table border="1">\n')
            # Write headers
            f.write('<tr>')
            headers = [self.tableWidget.horizontalHeaderItem(i).text() for i in range(self.tableWidget.columnCount())]
            for header in headers:
                f.write(f'<th>{header}</th>')
            f.write('</tr>\n')
            # Write data for visible rows
            for row in range(self.tableWidget.rowCount()):
                if self.tableWidget.isRowHidden(row):
                    continue
                f.write('<tr>')
                for col in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(row, col)
                    f.write(f'<td>{item.text() if item else ""}</td>')
                f.write('</tr>\n')
            f.write('</table></body></html>')
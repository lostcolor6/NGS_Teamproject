class FilteringLogic:
    def __init__(self, filterList):
        self.filterList = filterList

    def filterTable(self, tableWidget):
        for filter in self.filterList:
            filter.initFilter()
        for row_ind in range(tableWidget.rowCount()):
            tableWidget.setRowHidden(row_ind, False) # unhide all rows
            for filter in self.filterList:
                if not filter.filterPass(self.annotateRow(tableWidget, row_ind)):
                    # if a entry does not pass a filter, hide it
                    tableWidget.setRowHidden(row_ind, True)

    def annotateRow(self, tableWidget, rowInd):
        row = {}
        for colInd in range(tableWidget.columnCount()):
            cell = tableWidget.item(rowInd, colInd)
            colName = tableWidget.horizontalHeaderItem(colInd)
            if not colName:
                colName = str(colInd)
            else:
                colName = colName.text()
            if not cell:
                row[colName] = ''
            else:
                row[colName] = cell.text()
        return row

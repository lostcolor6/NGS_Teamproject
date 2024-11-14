"""
LookupTableWindow class to display the lookup data.

This class provides a window with to display the lookup data (parsed from the headers of a vcf) in a table format.
"""

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QTableWidget, QHeaderView, QTableWidgetItem


# LookupTableWindow class to display the lookup data
class LookupTableWindow(QDialog):
    """
    A dialog window to display the lookup data.

    Attributes:
        lookup_data: The lookup data to be displayed.
    """
    def __init__(self, lookup_data):
        super().__init__()
        self.lookup_data = lookup_data
        self.initUI()

    def initUI(self):
        self.setWindowTitle('VCF Lookup Table for Headers')
        self.setGeometry(300, 200, 750, 400)

        layout = QVBoxLayout()

        #add search bar
        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Search...")
        self.searchBar.textChanged.connect(self.onSearchTextChanged)
        layout.addWidget(self.searchBar)

        #add table widget
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(self.lookup_data))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Number", "Type", "Description"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.setSortingEnabled(True)

        self.populateTable(self.lookup_data)

        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

    def populateTable(self, data):
        """
        Populates the table with the provided data.

        Args:
            data: The data to be populated in the table.
        """
        self.tableWidget.setRowCount(len(data))
        for i, (id_, number, type_, description) in enumerate(data):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(id_))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(number))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(type_))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(description))

    def onSearchTextChanged(self):
        """
        Filters the lookup data based on the search query.
        """

        #get search query
        search_query = self.searchBar.text().lower()

        #filter lookup data based on the search query
        filtered_data = [
            row for row in self.lookup_data
            if search_query in row[0].lower() or search_query in row[3].lower()
        ]

        #update table with the filtered data
        self.populateTable(filtered_data)



class LookupTableThread(QThread):
    """
    A background thread to load the lookup data. (while still beeing able to use main GUI window)

    Attributes:
        dataReady: A signal emitted when the data is ready.
    """
    dataReady = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def run(self):
        """
        Loads the lookup data in the background thread.
        """
        #data fetched from an example output.vcf after a ngs pipeline run
        lookup_data = [
            ("NS", "1", "Integer", "Number of samples with data"),
            ("DP", "1", "Integer", "Total read depth at the locus"),
            ("DPB", "1", "Float", "Total read depth per bp at the locus; bases in reads overlapping / bases in haplotype"),
            ("AC", "A", "Integer", "Total number of alternate alleles in called genotypes"),
            ("AN", "1", "Integer", "Total number of alleles in called genotypes"),
            ("AF", "A", "Float", "Estimated allele frequency in the range (0,1]"),
            ("RO", "1", "Integer", "Count of full observations of the reference haplotype"),
            ("AO", "A", "Integer", "Count of full observations of this alternate haplotype"),
            ("PRO", "1", "Float", "Reference allele observation count, with partial observations recorded fractionally"),
            ("PAO", "A", "Float", "Alternate allele observations, with partial observations recorded fractionally"),
            ("QR", "1", "Integer", "Reference allele quality sum in phred"),
            ("QA", "A", "Integer", "Alternate allele quality sum in phred"),
            ("PQR", "1", "Float", "Reference allele quality sum in phred for partial observations"),
            ("PQA", "A", "Float", "Alternate allele quality sum in phred for partial observations"),
            ("SRF", "1", "Integer", "Number of reference observations on the forward strand"),
            ("SRR", "1", "Integer", "Number of reference observations on the reverse strand"),
            ("SAF", "A", "Integer", "Number of alternate observations on the forward strand"),
            ("SAR", "A", "Integer", "Number of alternate observations on the reverse strand"),
            ("SRP", "1", "Float", "Strand balance probability for the reference allele"),
            ("SAP", "A", "Float", "Strand balance probability for the alternate allele"),
            ("AB", "A", "Float", "Allele balance at heterozygous sites"),
            ("ABP", "A", "Float", "Allele balance probability at heterozygous sites"),
            ("RUN", "A", "Integer", "Run length: the number of consecutive repeats of the alternate allele in the reference genome"),
            ("RPP", "A", "Float", "Read Placement Probability"),
            ("RPPR", "1", "Float", "Read Placement Probability for reference observations"),
            ("RPL", "A", "Float", "Reads Placed Left"),
            ("RPR", "A", "Float", "Reads Placed Right"),
            ("EPP", "A", "Float", "End Placement Probability"),
            ("EPPR", "1", "Float", "End Placement Probability for reference observations"),
            ("DPRA", "A", "Float", "Alternate allele depth ratio"),
            ("ODDS", "1", "Float", "The log odds ratio of the best genotype combination to the second-best"),
            ("GTI", "1", "Integer", "Number of genotyping iterations required to reach convergence or bailout"),
            ("TYPE", "A", "String", "The type of allele"),
            ("CIGAR", "A", "String", "The extended CIGAR representation of each alternate allele"),
            ("NUMALT", "1", "Integer", "Number of unique non-reference alleles in called genotypes at this position"),
            ("MEANALT", "A", "Float", "Mean number of unique non-reference allele observations per sample with the corresponding alternate alleles"),
            ("LEN", "A", "Integer", "Allele length"),
            ("MQM", "A", "Float", "Mean mapping quality of observed alternate alleles"),
            ("MQMR", "1", "Float", "Mean mapping quality of observed reference alleles"),
            ("PAIRED", "A", "Float", "Proportion of observed alternate alleles supported by properly paired read fragments"),
            ("PAIREDR", "1", "Float", "Proportion of observed reference alleles supported by properly paired read fragments"),
            ("MIN_DP", "1", "Integer", "Minimum depth in gVCF output block"),
            ("END", "1", "Integer", "Last position in gVCF output record"),
            ("GT", "1", "String", "Genotype"),
            ("GQ", "1", "Float", "Genotype Quality"),
            ("GL", "G", "Float", "Genotype Likelihood"),
            ("DP", "1", "Integer", "Read Depth"),
            ("AD", "R", "Integer", "Number of observations for each allele"),
            ("RO", "1", "Integer", "Reference allele observation count"),
            ("QR", "1", "Integer", "Sum of quality of the reference observations"),
            ("AO", "A", "Integer", "Alternate allele observation count"),
            ("QA", "A", "Integer", "Sum of quality of the alternate observations"),
        ]
        self.dataReady.emit(lookup_data)
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton
from src.util.config import load_config
from src.connector.apifetch import apifetch

class HpoFilter(QWidget):
    def __init__(self, main_window, settings_manager=None, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.settings_manager = settings_manager

        api_config = load_config("config/API.ini", "api")
        self.api_address = api_config['host']
        self.api_port = api_config['port']
        
    groupLabel = 'HPO Terms'
    
    def initFilter(self):
        self.hpo_terms = self.hpoTextInput.text().split(',')
        self.hpo_genes = self.getHPOGenes(self.hpo_terms)

    def filterPass(self, entry):
        """decide whether entry should remain in dataset which is display or not

        Args:
            entry (_type_): _description_

        Returns:
            _type_: true if entry should be displayed
                    false if entry should not be displayed
        """
        if(self.hpo_terms == ['']):
            return True
        
        gene_symbol = entry['gene symbol']
        if(gene_symbol == self.main_window.vep_placeholder):
            return False
        elif gene_symbol in self.hpo_genes:
            return True
        else:
            return False

    def initUI(self):
        layout = QVBoxLayout()

        self.hpoLabel = QLabel('HPO')
        layout.addWidget(self.hpoLabel)

        self.hpoTextInput = QLineEdit()
        layout.addWidget(self.hpoTextInput)

        apply_button = QPushButton("Apply Filter")
        apply_button.clicked.connect(self.main_window.filterTable)
        layout.addWidget(apply_button)

        self.setLayout(layout)
        layout.addStretch()

    def getHPOGenes(self, hpo_ids):
        """
            receives a list of HPO ids and looks up the gene_symbols associated with the terms in the DB;
            returns list of corresponding gene symbols
        """
        ret = []
        if(self.hpo_terms == ['']):
            return ret
        for hpo_id in hpo_ids:
            rows = apifetch("http://" +  self.api_address + ":" + self.api_port +  "/hpo_gs/" + hpo_id)
            for row in rows: 
                ret.append(row['gene_symbol'])
             
        return ret
            
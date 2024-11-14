from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton
from src.util.config import load_config
from src.connector.apifetch import apifetch

class ConsequenceTermFilter(QWidget):
    def __init__(self, main_window, settings_manager=None, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.settings_manager = settings_manager
        
    groupLabel = 'Consequence Term'
    
    def initFilter(self):
        self.input_terms = list(map(lambda x: x.strip(), self.textInput.text().split(',')))

    def filterPass(self, entry):
        """decide whether entry should remain in dataset which is display or not

        Args:
            entry (_type_): _description_

        Returns:
            _type_: true if entry should be displayed
                    false if entry should not be displayed
        """
        if(self.input_terms == ['']):
            return True
        
        if entry['consequence terms'] in self.input_terms:
            return True
        else:
            return False
       

    def initUI(self):
        layout = QVBoxLayout()

        self.qLabel = QLabel('Consequence Term')
        layout.addWidget(self.qLabel)

        self.textInput = QLineEdit()
        layout.addWidget(self.textInput)

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
            
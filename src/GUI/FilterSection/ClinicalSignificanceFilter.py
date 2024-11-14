from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton
from src.util.config import load_config
from src.connector.apifetch import apifetch

class ClinicalSignificanceFilter(QWidget):
    def __init__(self, main_window, settings_manager=None, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.settings_manager = settings_manager
        
    groupLabel = 'Clinical Significance'
    
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
        
        entry_terms = list(map(lambda x: x.strip('{ }'), entry['clinical significance'].split(',')))
        
        for entry_term in entry_terms:
            if entry_term in self.input_terms:
                return True
            
        return False
       

    def initUI(self):
        layout = QVBoxLayout()

        self.qLabel = QLabel('Clinical Significance')
        layout.addWidget(self.qLabel)

        self.textInput = QLineEdit()
        layout.addWidget(self.textInput)

        apply_button = QPushButton("Apply Filter")
        apply_button.clicked.connect(self.main_window.filterTable)
        layout.addWidget(apply_button)

        self.setLayout(layout)
        layout.addStretch()
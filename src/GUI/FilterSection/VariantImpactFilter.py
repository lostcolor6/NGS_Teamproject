from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QVBoxLayout

class VariantImpactFilter(QWidget):
    def __init__(self, main_window, settings_manager, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.settings_manager = settings_manager

    groupLabel = 'VariantImpact'

    def initFilter(self):
        self.impactFilter = self.variantImpactDropdown.currentText()

    def initUI(self):
        layout = QVBoxLayout()

        self.variantImpactLabel = QLabel('Variant Impact')
        layout.addWidget(self.variantImpactLabel)

        self.variantImpactDropdown = QComboBox()
        self.variantImpactDropdown.addItems(['All', 'HIGH', 'MODERATE', 'LOW', 'MODIFIER', 'None'])
        self.variantImpactDropdown.currentIndexChanged.connect(self.main_window.filterTable)
        layout.addWidget(self.variantImpactDropdown)

        self.setLayout(layout)
        layout.addStretch()

    def filterPass(self, entry):
        if self.impactFilter == 'All':
            return True
        return self.impactFilter == entry['impact']


    def save_settings(self):
        """
        Saves the selected Item from the Dropdown
        """
        self.settings_manager.save_setting('impact_filter', self.variantImpactDropdown.currentText())

    def load_settings(self):
        """
        Loads in item to Dropdown
        """
        impact_filter = self.settings_manager.load_setting('impact_filter', 'All')
        index = self.variantImpactDropdown.findText(impact_filter)
        if index != -1:
            self.variantImpactDropdown.setCurrentIndex(index)
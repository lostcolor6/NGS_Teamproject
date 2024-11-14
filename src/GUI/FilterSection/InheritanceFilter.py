from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QVBoxLayout

class InheritanceFilter(QWidget):
    def __init__(self, main_window, settings_manager=None, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.settings_manager = settings_manager

    groupLabel = 'Inheritance Mode'

    def initFilter(self):
        self.inheritance_mode = self.inheritanceModeDropdown.currentText()

    def initUI(self):
        layout = QVBoxLayout()

        self.inheritanceModeLabel = QLabel('Inheritance Mode')
        layout.addWidget(self.inheritanceModeLabel)

        self.inheritanceModeDropdown = QComboBox()
        self.inheritanceModeDropdown.addItems(['All', 'Dominant', 'Recessive'])
        self.inheritanceModeDropdown.currentIndexChanged.connect(self.main_window.filterTable)
        layout.addWidget(self.inheritanceModeDropdown)

        self.setLayout(layout)
        layout.addStretch()

    def filterPass(self, entry):
        if self.inheritance_mode == 'Dominant' or self.inheritance_mode == 'All':
            return True
        elif self.inheritance_mode == 'Recessive':
            # filter out all heterozygote variants
            genotype = entry['GT']
            return self.computeRecessiveInheritance(genotype)
        
    def computeRecessiveInheritance(self, genotype: str) -> bool:
        """computes wether the variant with the given genotype if relevant for recessive inheritance

        Args:
            genotype (str): string indicating the genotype as described in the VCF format (GT field)

        Returns:
            bool: true if variant could be relevant for recessive inheritance, false otherwise 
        """
        if len(genotype) == 1:
            # haploid cell => relevant for recessive
            return True
        elif '|' in genotype:
            # phased genotype => only relevant if homozygote
            references = genotype.split('|')
            return references[0] == references[1]
        elif '/' in genotype:
            # phased genotype => only relevant if homozygote
            references = genotype.split('/')
            return references[0] == references[1]
        else:
            # unphased genotype
            # TODO: meaning of phased vs unphased
            return True


    def save_settings(self):
        self.settings_manager.save_setting('inheritance_mode', self.inheritanceModeDropdown.currentText())

    def load_settings(self):
        inheritance_mode = self.settings_manager.load_setting('inheritance_mode', 'All')
        index = self.inheritanceModeDropdown.findText(inheritance_mode)
        if index != -1:
            self.inheritanceModeDropdown.setCurrentIndex(index)
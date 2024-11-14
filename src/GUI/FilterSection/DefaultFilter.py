"""
DefaultFilter class for applying default filters.

This class provides a way to apply default filters to the filtersection.
"""
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QCheckBox, QLineEdit, QLabel


class DefaultFilter(QWidget):
    """
    A widget for applying default filters.

    Attributes:
        main_window: The main window instance.
        inheritance_filter: The inheritance filter instance.
        variant_impact_filter: The variant impact filter instance.
    """
    def __init__(self, main_window, inheritance_filter, variant_impact_filter, quality_filter, target_filter,  parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.inheritance_filter = inheritance_filter
        self.variant_impact_filter = variant_impact_filter
        self.quality_filter = quality_filter
        self.target_filter = target_filter
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()



        self.applyDefaultFilterButton = QPushButton('Apply Default Filter')
        self.applyDefaultFilterButton.clicked.connect(self.applyDefaultFilter)
        layout.addWidget(self.applyDefaultFilterButton)

        self.setLayout(layout)
        layout.addStretch()

    def applyDefaultFilter(self):
        """
        Applies the default filters.

        Resets the inheritance filter and variant impact filter to their default values and reapplies the filters to the table.
        """
        #reset Inheritance Filter to default value
        self.inheritance_filter.inheritanceModeDropdown.setCurrentIndex(0)  #set to 'All'

        #reset Variant Impact Filter to default value
        self.variant_impact_filter.variantImpactDropdown.setCurrentIndex(0)  #set to 'All'

        #reset Qual values min to 0 max to 100000
        self.quality_filter.min_qual_spin.setValue(0)
        self.quality_filter.max_qual_spin.setValue(100000)

        #reset Target Filter to all checked
        self.target_filter.filterOffTarget.setChecked(True)
        self.target_filter.filterMosaic.setChecked(True)
        self.target_filter.filterMappability.setChecked(True)
        self.target_filter.filterNoInfo.setChecked(True)

        #call filterTable to reapply filters
        self.main_window.filterTable()


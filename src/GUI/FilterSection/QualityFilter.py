"""
QualityFilter class for filtering data based on quality scores.

This class provides a way to filter data based on minimum and maximum quality scores.
"""
from PyQt5.QtWidgets import QWidget, QLabel, QDoubleSpinBox, QPushButton, QVBoxLayout, QMessageBox

class QualityFilter(QWidget):
    """
    A widget for filtering data based on quality scores.

    Attributes:
        main_window: The main window instance.
        settings_manager: The settings manager instance.
    """
    def __init__(self, main_window, settings_manager, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.settings_manager = settings_manager

    groupLabel = 'VCF Quality'

    def initFilter(self):
        self.min_qual = self.min_qual_spin.value()
        self.max_qual = self.max_qual_spin.value()

    def initUI(self):
        # Load settings using settings_manager
        min_qual_value = self.settings_manager.load_setting('min_qual', 0, int)
        max_qual_value = self.settings_manager.load_setting('max_qual', 10000, int)
        min_qual_range_lower = self.settings_manager.load_setting('min_qual_range_lower', -10000, int)
        min_qual_range_upper = self.settings_manager.load_setting('min_qual_range_upper', 100000000, int)
        max_qual_range_lower = self.settings_manager.load_setting('min_qual_range_lower', -10000, int)
        max_qual_range_upper = self.settings_manager.load_setting('min_qual_range_upper', 100000000, int)

        layout = QVBoxLayout()
        min_label = QLabel("Min QUAL:")
        layout.addWidget(min_label)
        self.min_qual_spin = QDoubleSpinBox()
        self.min_qual_spin.setRange(min_qual_range_lower, min_qual_range_upper)
        self.min_qual_spin.setDecimals(0)
        self.min_qual_spin.setValue(min_qual_value)
        layout.addWidget(self.min_qual_spin)

        max_label = QLabel("Max QUAL:")
        layout.addWidget(max_label)
        self.max_qual_spin = QDoubleSpinBox()
        self.max_qual_spin.setRange(max_qual_range_lower, max_qual_range_upper)
        self.max_qual_spin.setDecimals(0)
        self.max_qual_spin.setValue(max_qual_value)
        layout.addWidget(self.max_qual_spin)

        apply_button = QPushButton("Apply Filter")
        apply_button.clicked.connect(self.main_window.filterTable)
        layout.addWidget(apply_button)

        self.setLayout(layout)
        layout.addStretch()

    def filterPass(self, entry):
        """
        Checks if an entry passes the quality filter.

        Args:
            entry: The entry to be filtered.

        Returns:
            True if the entry passes the filter, False otherwise.
        """
        qual_value = float(entry['QUAL'])
        return (self.min_qual <= qual_value <= self.max_qual)

    #functions that later get wrapped / connected all to the save/load buttons in the GUI
    def save_settings(self):
        """
        Saves the Qual value for filtering.
        """
        self.settings_manager.save_setting('min_qual', self.min_qual_spin.value())
        self.settings_manager.save_setting('max_qual', self.max_qual_spin.value())


    def load_settings(self):
        """
        Loads the Qual value for filtering.
        """
        min_qual_value = self.settings_manager.load_setting('min_qual', 0, int)
        max_qual_value = self.settings_manager.load_setting('max_qual', 10000, int)
        self.min_qual_spin.setValue(min_qual_value)
        self.max_qual_spin.setValue(max_qual_value)


        min_qual_range_lower = self.settings_manager.load_setting('min_qual_range_lower', -10000, int)
        min_qual_range_upper = self.settings_manager.load_setting('min_qual_range_upper', 100000000, int)
        max_qual_range_lower = self.settings_manager.load_setting('min_qual_range_lower', -10000, int)
        max_qual_range_upper = self.settings_manager.load_setting('min_qual_range_upper', 100000000, int)
        self.min_qual_spin.setRange(min_qual_range_lower, min_qual_range_upper)
        self.max_qual_spin.setRange(max_qual_range_lower, max_qual_range_upper)



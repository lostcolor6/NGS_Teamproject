"""
TargetFilter class for filtering data based on target filters.

This class provides a way to filter data based on off-target, mosaic, low mappability, and no info (.) filters.
"""
from PyQt5.QtWidgets import QWidget, QCheckBox, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox

from src.GUI.FilterSection.QualityFilter import *


class TargetFilter(QWidget):
    """
    A widget for filtering data based on target filters.

    Attributes:
        main_window: The main window instance.
        settings_manager: The settings manager instance.
    """
    def __init__(self, main_window, settings_manager, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.settings_manager = settings_manager
        
    groupLabel = 'VCF Filter'
        
    def initFilter(self):
        self.showOffTarget = self.filterOffTarget.isChecked()
        self.showMosaic = self.filterMosaic.isChecked()
        self.showLowMappability = self.filterMappability.isChecked()
        #self.showNoInfo = self.filterNoInfo.isChecked()

    def initUI(self):
        # Load settings using settings_manager
        off_target_bool = self.settings_manager.load_setting('off_target', False, bool)
        mosaic_bool = self.settings_manager.load_setting('mosaic', False, bool)
        lowmap_bool = self.settings_manager.load_setting('low_map', False, bool)
        noinfo_bool = self.settings_manager.load_setting('no_info', False, bool)


        layout = QVBoxLayout()

        self.filterOffTarget = QCheckBox('Show Off-Target')
        self.filterOffTarget.setChecked(off_target_bool)
        self.filterOffTarget.stateChanged.connect(self.main_window.filterTable)
        layout.addWidget(self.filterOffTarget)

        self.filterMosaic = QCheckBox('Show Mosaic')
        self.filterMosaic.setChecked(mosaic_bool)
        self.filterMosaic.stateChanged.connect(self.main_window.filterTable)
        layout.addWidget(self.filterMosaic)

        self.filterMappability = QCheckBox('Show Low Mappability')
        self.filterMappability.setChecked(lowmap_bool)
        self.filterMappability.stateChanged.connect(self.main_window.filterTable)
        layout.addWidget(self.filterMappability)

        self.filterNoInfo = QCheckBox('Show . (No Info)')
        self.filterNoInfo.setChecked(noinfo_bool)
        self.filterNoInfo.stateChanged.connect(self.main_window.filterTable)
        layout.addWidget(self.filterNoInfo)


        self.setLayout(layout)



    def filterPass(self, entry):
        """
        Checks if an entry passes the target filter.

        Args:
            entry: The entry to be filtered.

        Returns:
            True if the entry passes the filter, False otherwise.
        """

        #TODO: implement
        entry_filter_value = entry['FILTER']

        return True


    def save_settings(self):
        """
        Saves the checked parameters for filtering.
        """
        try:
            self.settings_manager.save_setting("off_target", self.filterOffTarget.isChecked())
            self.settings_manager.save_setting("mosaic", self.filterMosaic.isChecked())
            self.settings_manager.save_setting("low_map", self.filterMappability.isChecked())
            self.settings_manager.save_setting("no_info", self.filterNoInfo.isChecked())
        except Exception as e:
            error_message = f"Error saving settings: {e}"
            print(error_message)
            QMessageBox.critical(self, "Error", error_message)

    def load_settings(self):
        """
        loads from ini file witch parameters should be checked.
        """
        try:
            self.filterOffTarget.setChecked(self.settings_manager.load_setting("off_target", False, bool))
            self.filterMosaic.setChecked(self.settings_manager.load_setting("mosaic", False, bool))
            self.filterMappability.setChecked(self.settings_manager.load_setting("low_map", False, bool))
            self.filterNoInfo.setChecked(self.settings_manager.load_setting("no_info", False, bool))
        except Exception as e:
            error_message = f"Error loading settings: {e}"
            print(error_message)
            QMessageBox.critical(self, "Error", error_message)


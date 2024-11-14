"""
LayoutFilter class for filtering and settings management.

This class creates a layout for filtering and settings management in the main window.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolBox, QPushButton, QLineEdit, QLabel, QTextEdit, QGroupBox, \
    QScrollArea, QTabWidget, QCheckBox, QMessageBox

from src.GUI.FilterSection.DefaultFilter import DefaultFilter
from src.GUI.FilterSection.HPOFilter import HpoFilter
from src.GUI.FilterSection.InheritanceFilter import InheritanceFilter
from src.GUI.FilterSection.QualityFilter import QualityFilter
from src.GUI.FilterSection.TargetFilter import TargetFilter
from src.GUI.FilterSection.GnomFilter import GnomAmrFilter, GnomAfrFilter, GnomEasFilter, GnomNfeFilter, GnomSasFilter
from src.GUI.FilterSection.AlphaScoreFilter import AlphaScoreFilter
from src.GUI.FilterSection.VariantImpactFilter import VariantImpactFilter
from src.GUI.FilterSection.ConsequenceTermFilter import ConsequenceTermFilter
from src.GUI.FilterSection.ClinicalSignificanceFilter import ClinicalSignificanceFilter
from src.GUI.SettingsSection.SettingManager import SettingsManager






class LayoutFilter(QWidget):
    """
    A widget space for filtering and settings management in the GUI.

    """
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        #create an instance of SettingsManager
        self.settings_manager = SettingsManager()
        self.initUI()


    def on_toggled(self, checked):
        """
        Slot for toggling the visibility of filter groups.

        Args:
            checked (bool): Whether the group box is checked.
        """
        group_box = self.sender()
        layout = group_box.layout()
        if checked:
            for i in range(layout.count()):
                layout.itemAt(i).widget().setVisible(True)
        else:
            for i in range(layout.count()):
                layout.itemAt(i).widget().setVisible(False)



    def initUI(self):
        """
        Initializes the user interface.
        """
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.scroll_area = QScrollArea()
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)
        self.scroll_area.setWidget(self.content_widget)
        self.scroll_area.setWidgetResizable(True)
        
        self.main_window.filterList.extend([HpoFilter(self.main_window, self.settings_manager),
                                            # AlphaScoreFilter(self.main_window),
                                            GnomAmrFilter(self.main_window),
                                            GnomAfrFilter(self.main_window),
                                            GnomSasFilter(self.main_window),
                                            GnomNfeFilter(self.main_window),
                                            GnomEasFilter(self.main_window),
                                            InheritanceFilter(self.main_window, self.settings_manager, ),
                                            QualityFilter(self.main_window, self.settings_manager),
                                            TargetFilter(self.main_window, self.settings_manager),
                                            VariantImpactFilter(self.main_window, self.settings_manager),
                                            ConsequenceTermFilter(self.main_window, self.settings_manager),
                                            ClinicalSignificanceFilter(self.main_window, self.settings_manager),
                                        ])
        
        for filter in self.main_window.filterList:
            filter_group = QGroupBox(filter.groupLabel)
            filter_group.setCheckable(True)
            filter_layout = QVBoxLayout()
            filter.initUI()
            filter_layout.addWidget(filter)
            filter_group.setLayout(filter_layout)
            filter_group.toggled.connect(self.on_toggled)
            self.content_layout.addWidget(filter_group)

        # default_filter_group = QGroupBox('Default Filter')
        # default_filter_group.setCheckable(True)
        # default_filter_layout = QVBoxLayout()
        # default_filter = DefaultFilter(self.main_window, self.inheritance_mode_filter, self.variant_impact_filter)
        # default_filter_layout.addWidget(default_filter)
        # default_filter_group.setLayout(default_filter_layout)
        # self.content_layout.addWidget(default_filter_group)

        layout.addWidget(self.scroll_area)


        # Deafult Filter apply button
        # self.default_filter = DefaultFilter(self.main_window,
        #                                     self.inheritance_mode_filter,
        #                                     self.variant_impact_filter,
        #                                     self.quality_filter,
        #                                     self.target_filter)

        # layout.addWidget(self.default_filter)

        # Other UI components
        self.openAnnotateButton = QPushButton('Annotate Variant')
        self.openAnnotateButton.clicked.connect(self.main_window.fetchVEPData)
        layout.addWidget(self.openAnnotateButton)

        self.pingAPIButton = QPushButton('Ping API')
        self.pingAPIButton.clicked.connect(self.fetchData)
        layout.addWidget(self.pingAPIButton)

        self.textField = QLineEdit()
        self.textField.setPlaceholderText("Enter some text")
        layout.addWidget(self.textField)

        self.addProfileName = QLabel("Profile Name")
        layout.addWidget(self.addProfileName)

        self.line_edit1 = QLineEdit(self)
        self.line_edit1.setFixedWidth(250)
        self.line_edit1.setFixedHeight(25)
        layout.addWidget(self.line_edit1)

        self.notizLabel = QLabel("Notes:")
        layout.addWidget(self.notizLabel)

        self.text_edit1 = QTextEdit(self)
        self.text_edit1.setFixedSize(250, 100)
        layout.addWidget(self.text_edit1)

        self.save_button = QPushButton("Save Settings", self)
        self.load_button = QPushButton("Load Settings", self)
        self.save_button.clicked.connect(self.save_settings)
        self.load_button.clicked.connect(self.load_settings)
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)

        layout.addStretch()


    def fetchData(self):
        # Call the fetchData method of the main window instance
        self.main_window.fetchData()






    def save_settings(self):
        """
        Saves the settings and filters to the settings manager (gets saved in the gui.ini).
        """
        try:
            self.settings_manager.save_setting("addProfileName", self.line_edit1.text())
            #this is the Notes txt field
            self.settings_manager.save_setting("text_edit1", self.text_edit1.toPlainText())

            # Save settings for TargetFilter
            self.target_filter.save_settings()
            self.quality_filter.save_settings()
            self.inheritance_mode_filter.save_settings()
            self.variant_impact_filter.save_settings()


        except Exception as e:
            error_message = f"Error loading settings: {e}"
            print(error_message)
            QMessageBox.critical(self, "Error", error_message)

    def load_settings(self):
        """
        Loads the settings and filters from the settings manager (gets loaded from the gui.ini).
        """
        try:
            self.line_edit1.setText(self.settings_manager.load_setting("addProfileName", ""))
            self.text_edit1.setPlainText(self.settings_manager.load_setting("text_edit1", ""))

            # Load settings for TargetFilter
            self.target_filter.load_settings()
            self.quality_filter.load_settings()
            self.inheritance_mode_filter.load_settings()
            self.variant_impact_filter.load_settings()

        except Exception as e:
            error_message = f"Error loading settings: {e}"
            print(error_message)
            QMessageBox.critical(self, "Error", error_message)


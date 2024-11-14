"""
TaskBar class to create a menu bar with File, Help, and Settings menus.

This class provides a menu bar with options to open VCF and CSV files, save data to various formats,
and access help, doc and settings windows.
"""
from PyQt5.QtWidgets import QMenuBar, QMenu, QAction, QMessageBox, QVBoxLayout, QTabWidget, QWidget, QDialog, QLabel, \
    QCheckBox, QPushButton, QLineEdit, QFormLayout, QHBoxLayout, QGroupBox
from PyQt5.QtCore import Qt




class TaskBar(QMenuBar):
    """
    TaskBar class to create a menu bar with File, Help, and Settings menus.

    Args:
        parent: The main window instance.
        settings_manager: The settings manager instance.
    """
    def __init__(self, parent, settings_manager):
        super().__init__(parent)

        self.parent = parent
        self.settings_manager = settings_manager

        # create a File menu
        fileMenu = self.addMenu('File')

        # add Open vcf action to the File menu
        openVCFAction = fileMenu.addAction('Open VCF')
        openVCFAction.setStatusTip('Open a Variant Call Format (VCF) file')
        openVCFAction.triggered.connect(self.parent.openVCF_file)

        # add Open csv action to the File menu
        openCSVAction = fileMenu.addAction('Open CSV')
        openCSVAction.setStatusTip('Open a Comma-Separated Values (CSV) file')
        openCSVAction.triggered.connect(self.parent.openCSV_file)

        # add Save action to the File menu
        saveAsMenu = fileMenu.addMenu('Save as')
        saveAsMenu.setStatusTip('Save the current table')
        #saveAction.triggered.connect(self.parent.save_file)

        # Add Save As CSV action
        saveAsCSVAction = saveAsMenu.addAction('CSV')
        saveAsCSVAction.setStatusTip('Save the current table as a CSV file')
        saveAsCSVAction.triggered.connect(self.parent.saveCSV_file)

        # Add Save As TXT action
        saveAsTXTAction = saveAsMenu.addAction('TXT')
        saveAsTXTAction.setStatusTip('Save the current table as a TXT file')
        saveAsTXTAction.triggered.connect(self.parent.saveTXT_file)

        # Add Save As JSON action
        saveAsJSONAction = saveAsMenu.addAction('JSON')
        saveAsJSONAction.setStatusTip('Save the current table as a JSON file')
        saveAsJSONAction.triggered.connect(self.parent.saveJSON_file)

        # Add Save As HTML action
        saveAsHTMLAction = saveAsMenu.addAction('HTML')
        saveAsHTMLAction.setStatusTip('Save the current table as an HTML file')
        saveAsHTMLAction.triggered.connect(self.parent.saveHTML_file)








        # add Exit action to the File menu
        exitAction = fileMenu.addAction('Exit')
        exitAction.triggered.connect(parent.close)

        # create a Help menu
        helpMenu = self.addMenu('Help')
        helpAction = helpMenu.addAction('Open Doc')
        helpAction.triggered.connect(self.openHelpWindow)

        # create a Settings menu
        settingsMenu = self.addMenu('Settings')
        genSettingsAction = settingsMenu.addAction('General Settings')
        genSettingsAction.triggered.connect(self.openSettingsWindow)


    #msgbox/label showing docs
    def showDocumentation(self):
        """
        Show documentation in a message box.
        """
        QMessageBox.information(self, "Documentation",
                                "Further Documentation can be found on: \n https://github.com/imgag/Teamprojekt_SS24_Gruppe2 ")

        #simple helpwindow function
    def openHelpWindow(self):
        """
        Open a help window with tabs for getting started, basic usage, and about.
        """
        help_dialog = HelpWindow()
        help_dialog.exec_()


    def openSettingsWindow(self):
        """
        Open a settings window with tabs for connections info, theme(color), and filter settings.
        """
        settings_dialog = SettingsWindow(self, self.settings_manager)
        settings_dialog.exec_()


    #function to enable a darkTheme to our application
    def applyDarkMode(self, enabled):
        """
        Apply a dark theme to the application.

        Args:
            enabled: A boolean indicating whether to enable the dark theme.
        """
        if enabled:
            dark_stylesheet = """
                QMainWindow {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QTableWidget {
                    background-color: #3b3b3b;
                    alternate-background-color: #2b2b2b;
                    color: #ffffff;
                }
                QHeaderView::section {
                    background-color: #3b3b3b;
                    color: #ffffff;
                }
                QTextEdit, QLineEdit, QPlainTextEdit {
                    background-color: #3b3b3b;
                    color: #ffffff;
                }
                QPushButton {
                    background-color: #3b3b3b;
                    color: #ffffff;
                }
                QCheckBox, QLabel {
                    color: #ffffff;
                }
                QMenuBar {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QMenu {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QMenu::item:selected {
                    background-color: #3b3b3b;
                }
                QTabWidget::pane {
                    background-color: #2b2b2b;
                }
                QTabBar::tab {
                    background-color: #3b3b3b;
                    color: #ffffff;
                }
                QTabBar::tab:selected {
                    background-color: #2b2b2b;
                }
                """
            self.parent.setStyleSheet(dark_stylesheet)
        else:
            self.parent.setStyleSheet("")




class HelpWindow(QDialog):
    """
    Help window with tabs for getting started, basic usage, and about.
    this should have taps to guide user through all functions of our application aswell as extern link to repo or external doc
    """
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Help and Documentation')
        self.setGeometry(200, 200, 800, 600)

        layout = QVBoxLayout()
        self.tabWidget = QTabWidget()
        layout.addWidget(self.tabWidget)

        self.gettingStartedTab = QWidget()
        self.basicsTab = QWidget()
        self.AboutTab = QWidget()



        self.tabWidget.addTab(self.gettingStartedTab, 'Getting Started')
        self.tabWidget.addTab(self.basicsTab, 'Basic Usage')
        self.tabWidget.addTab(self.AboutTab, 'About')

        #add content to the tabs
        gettingStartedLayout = QVBoxLayout()
        gettingStartedLabel = QLabel('<h2>Getting Started</h2>'
                                     '<p>Welcome to our application! This help window will guide you through the basic usage and features of our application.</p>'
                                     '<p>For further documentation, please visit our GitHub repositories:</p>'
                                     '<ul>'
                                     '<li><a href="https://github.com/lostcolor6/NGS_PyQt">Private GitHub</a></li>'
                                     '<li><a href="https://github.com/imgag/Teamprojekt_SS24_Gruppe2">Project GitHub</a></li>'
                                     '</ul>')

        gettingStartedLabel.setOpenExternalLinks(True)

        gettingStartedLayout.addWidget(gettingStartedLabel)
        #add stretch to push widgets to the top
        gettingStartedLayout.addStretch()


        self.gettingStartedTab.setLayout(gettingStartedLayout)

        basicsLayout = QVBoxLayout()
        basicsLabel = QLabel('<h2>Basic Usage</h2>'
                             '<p>The main window of our application consists of a table and several filtering options.</p>'
                             '<h3>Table</h3>'
                             '<p>The table displays the data loaded from the VCF file. Each row represents a single variant, and the columns display various attributes of the variant.</p>'
                             '<ul>'
                             '<li>Variant ID: Unique identifier for each variant.</li>'
                             '<li>Chromosome: The chromosome on which the variant is located.</li>'
                             '<li>Position: The position of the variant on the chromosome.</li>'
                             '<li>Reference: The reference allele for the variant.</li>'
                             '<li>Alternate: The alternate allele for the variant.</li>'
                             '</ul>'
                             '<p>You can customize the table by:</p>'
                             '<ul>'
                             '<li>Right-clicking to show or hide columns, drag them around, and resize them.</li>'
                             '<li>Left-clicking a header column to sort by ascending or descending order.</li>'
                             '<li>Left-clicking a vertical header to display certain information about that entry on the bottom right of the GUI.</li>'
                             '</ul>'
                             '<h3>Filtering</h3>'
                             '<p>The filtering options allow you to narrow down the variants displayed in the table based on various criteria.</p>'
                             '<ul>'
                             '<li>Quality Filter: Filter variants based on their quality score.</li>'
                             '<li>Variant Impact Filter: Filter variants based on their impact on the genome.</li>'
                             '<li>Inheritance Filter: Filter variants based on their inheritance pattern.</li>'
                             '<li>Target Filter: Filter variants based on their target region.</li>'
                             '</ul>'
                             '<p>You can also:</p>'
                             '<ul>'
                             '<li>Choose to hide certain filter categories.</li>'
                             '<li>Use the Apply Default Filter button to reset the filters to a default value based on user settings/ini file.</li>'
                             '<li>Use the Annotate Variant button to annotate a entry.</li>'
                             '<li>Enter a Profile Name and Notes below that also get saved to the ini file.</li>'
                             '<li>Save and Load the filter settings using the buttons at the end of the Filter Section.</li>'
                             '</ul>'
                             '<h3>Toolbar</h3>'
                             '<p>The toolbar is draggable to either side or bottom/top.</p>'
                             '<ul>'
                             '<li>Quicksave: Save the current visible table.</li>'
                             '<li>Refresh: Reload the table and make all columns visible again.</li>'
                             '<li>Show Raw Data: Open a window where all of the VCF as a raw text format gets loaded up (this takes long for big VCF files).</li>'
                             '<li>Show Lookup Table: Open up a search query for you to lookup meaning of certain headers and their type.</li>'
                             '</ul>'
                             '<h3>Taskbar</h3>'
                             '<p>The taskbar provides access to various functions:</p>'
                             '<ul>'
                             '<li>On File:</li>'
                             '<ul>'
                             '<li>Open a VCF (Variant Call Format) or CSV (Comma Separated Value) file into the table.</li>'
                             '<li>Save in the file formats: CSV, TXT, JSON, and HTML.</li>'
                             '<li>Exit: Close the application.</li>'
                             '</ul>'
                             '<li>On Help:</li>'
                             '<ul>'
                             '<li>Find the repositories of this project as well as further documentation.</li>'
                             '</ul>'
                             '<li>On Settings:</li>'
                             '<ul>'
                             '<li>See the current information about connections such as APIs.</li>'
                             '<li>Select a dark theme for less eye strain.</li>'
                             '<li>In the Quality Settings:</li>'
                             '<ul>'
                             '<li>Choose max/min quality values to get saved into the ini file.</li>'
                             '<li>Set the respective Spinbox ranges for the filters.</li>'
                             '<li>Set a quality cutoff so only entries over a certain value get displayed initially.</li>'
                             '</ul>'
                             '<li>All of these settings get saved in the gui.ini file.</li>'
                             '</ul>'
                             '</ul>'
                             '<h3>General</h3>'
                             '<p>On the bottom left, your opened VCF header gets displayed for easy access and lookup.</p>')

        basicsLayout.addWidget(basicsLabel)
        #add stretch to push widgets to the top
        basicsLayout.addStretch()
        self.basicsTab.setLayout(basicsLayout)


        self.setLayout(layout)



class SettingsWindow(QDialog):
    """
   Settings window with tabs for connections, theme/color, and quality settings.
   this should have functions to edit general Settings and or visuales of our application
   """
    def __init__(self, main_window, settings_manager):
        super().__init__()
        self.main_window = main_window
        self.settings_manager = settings_manager
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Settings')
        self.setGeometry(200, 200, 300, 400)

        layout = QVBoxLayout()
        self.tabWidget = QTabWidget()
        layout.addWidget(self.tabWidget)

        self.ConnectionsTab = QWidget()
        self.ThemeColorTab = QWidget()
        self.QualityTab = QWidget()  # Tab for Quality Settings

        self.tabWidget.addTab(self.ConnectionsTab, 'Connections')
        self.tabWidget.addTab(self.ThemeColorTab, 'Theme/Color')
        self.tabWidget.addTab(self.QualityTab, 'Quality Settings')

        # Theme/Color Tab
        themeColorLayout = QVBoxLayout()

        # Dark Mode Toggle
        self.darkModeCheckBox = QCheckBox('Enable Dark Mode')
        self.darkModeCheckBox.stateChanged.connect(self.toggleDarkMode)
        themeColorLayout.addWidget(self.darkModeCheckBox)

        themeColorLayout.addStretch()
        self.ThemeColorTab.setLayout(themeColorLayout)

        # Connections Tab
        ConnectionsLayout = QVBoxLayout()
        ConnectionsLabelAPI = QLabel('Connections API')
        ConnectionsLayout.addWidget(ConnectionsLabelAPI)

        try:
            api_info_host = self.settings_manager.load_infoAPI('host', '', str)
            api_info_port = self.settings_manager.load_infoAPI('port', '', str)

            api_info = f"Host: {api_info_host}\nPort: {api_info_port}"
            ConnectionsInfoLabel = QLabel(api_info)
            ConnectionsLayout.addWidget(ConnectionsInfoLabel)
        except Exception as e:
            ConnectionsInfoLabel = QLabel("Error loading API info: " + str(e))
            ConnectionsLayout.addWidget(ConnectionsInfoLabel)

        ConnectionsLayout.addStretch()
        self.ConnectionsTab.setLayout(ConnectionsLayout)

        # Quality Settings Tab
        qualityLayout = QFormLayout()





        # Max Qual group
        maxQualGroup = QGroupBox("Max Qual")
        maxQualLayout = QVBoxLayout()
        maxQualRangeLayout = QHBoxLayout()

        maxQualLabel = QLabel("Max Qual:")
        self.maxQualEdit = QLineEdit(self)
        self.maxQualEdit.setText(str(self.settings_manager.load_setting('max_qual', 10000, int)))
        maxQualLayout.addWidget(maxQualLabel)
        maxQualLayout.addWidget(self.maxQualEdit)

        LowerRangeLabel = QLabel("Spinbox Qual lower bound:")
        self.maxQualRangeLower = QLineEdit(self)
        self.maxQualRangeLower.setText(str(self.settings_manager.load_setting('max_qual_range_lower', 10000000, int)))
        maxQualRangeLayout.addWidget(LowerRangeLabel)
        maxQualRangeLayout.addWidget(self.maxQualRangeLower)
        UpperRangeLabel = QLabel("Spinbox Qual upper bound:")
        self.maxQualRangeUpper = QLineEdit(self)
        self.maxQualRangeUpper.setText(str(self.settings_manager.load_setting('max_qual_range_upper', 10000000, int)))
        maxQualRangeLayout.addWidget(UpperRangeLabel)
        maxQualRangeLayout.addWidget(self.maxQualRangeUpper)

        maxQualLayout.addLayout(maxQualRangeLayout)
        maxQualGroup.setLayout(maxQualLayout)
        qualityLayout.addWidget(maxQualGroup)






        # Min Qual group
        minQualGroup = QGroupBox("Min Qual")
        minQualLayout = QVBoxLayout()
        minQualRangeLayout = QHBoxLayout()

        # Min Qual Label and Line Edit
        minQualLabel = QLabel("Min Qual:")
        self.minQualEdit = QLineEdit(self)
        self.minQualEdit.setText(str(self.settings_manager.load_setting('min_qual', 0, int)))
        minQualLayout.addWidget(minQualLabel)
        minQualLayout.addWidget(self.minQualEdit)

        # Add the LowerRangeLabel and its corresponding QLineEdit to minQualRangeLayout
        LowerRangeLabel = QLabel("Spinbox Qual lower bound:")
        self.minQualRangeLower = QLineEdit(self)
        self.minQualRangeLower.setText(str(self.settings_manager.load_setting('min_qual_range_lower', -10000, int)))
        minQualRangeLayout.addWidget(LowerRangeLabel)
        minQualRangeLayout.addWidget(self.minQualRangeLower)

        # Add the UpperRangeLabel and its corresponding QLineEdit to minQualRangeLayout
        UpperRangeLabel = QLabel("Spinbox Qual upper bound:")
        self.minQualRangeUpper = QLineEdit(self)
        self.minQualRangeUpper.setText(str(self.settings_manager.load_setting('min_qual_range_upper', 10000000, int)))
        minQualRangeLayout.addWidget(UpperRangeLabel)
        minQualRangeLayout.addWidget(self.minQualRangeUpper)

        # Add the range layout to the main layout
        minQualLayout.addLayout(minQualRangeLayout)
        minQualGroup.setLayout(minQualLayout)
        qualityLayout.addWidget(minQualGroup)







        # Qual Cutoff group
        qualCutoffGroup = QGroupBox("Qual Cutoff")
        qualCutoffLayout = QVBoxLayout()

        qualCutoffLabel = QLabel("Qual Cutoff:")
        self.qualCutoffEdit = QLineEdit(self)
        self.qualCutoffEdit.setText(str(self.settings_manager.load_setting('qual_cutoff', 0, int)))
        qualCutoffLayout.addWidget(qualCutoffLabel)
        qualCutoffLayout.addWidget(self.qualCutoffEdit)

        qualCutoffGroup.setLayout(qualCutoffLayout)
        qualityLayout.addWidget(qualCutoffGroup)

        # Save Button
        saveButton = QPushButton("Save")
        saveButton.clicked.connect(self.save_quality_settings)
        qualityLayout.addRow(saveButton)

        self.QualityTab.setLayout(qualityLayout)

        self.setLayout(layout)

    # Toggle dark mode based on the state of the checkbox
    def toggleDarkMode(self, state):
        """
        Toggle dark mode on or off.

        Args:
            state: A boolean indicating whether to enable dark mode.
        """
        self.main_window.applyDarkMode(state == Qt.Checked)

    # Function to save quality settings
    def save_quality_settings(self):
        """
        Save settings to the ini file
        """
        min_qual = self.minQualEdit.text()
        min_qual_range_lower = self.minQualRangeLower.text()
        min_qual_range_upper = self.minQualRangeUpper.text()
        max_qual = self.maxQualEdit.text()
        max_qual_range_lower = self.maxQualRangeLower.text()
        max_qual_range_upper = self.maxQualRangeUpper.text()
        qual_cutoff = self.qualCutoffEdit.text()


        # Save the settings using SettingsManager
        self.settings_manager.save_setting('min_qual', min_qual)
        self.settings_manager.save_setting('min_qual_range_lower', min_qual_range_lower)
        self.settings_manager.save_setting('min_qual_range_upper', min_qual_range_upper)


        self.settings_manager.save_setting('max_qual', max_qual)
        self.settings_manager.save_setting('max_qual_range_lower', max_qual_range_lower)
        self.settings_manager.save_setting('max_qual_range_upper', max_qual_range_upper)

        self.settings_manager.save_setting('qual_cutoff', qual_cutoff)

        QMessageBox.information(self, "Settings", "Settings have been saved!")
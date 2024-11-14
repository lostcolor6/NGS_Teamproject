from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QCheckBox, QPushButton, QDoubleSpinBox

class CutoffFilter(QWidget):
    def __init__(self):
        super().__init__()
        
    noInfo = True
        
    def initFilter(self):
        self.inputValue = self.cutoffInput.value()
    
    def initUI(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel(self.label))

        self.cutoffInput = QDoubleSpinBox()
        self.cutoffInput.setRange(self.lowerBound, self.upperBound)
        self.cutoffInput.setDecimals(self.decimals)
        self.cutoffInput.setValue(self.initValue)
        layout.addWidget(self.cutoffInput)
        
        self.includeWithOutInfo = QCheckBox("Include Entries without Info")
        self.includeWithOutInfo.setChecked(True)
        layout.addWidget(self.includeWithOutInfo)
        self.includeWithOutInfo.toggled.connect(self.noInfoToggle)

        apply_button = QPushButton("Apply Filter")
        apply_button.clicked.connect(self.main_window.filterTable)
        layout.addWidget(apply_button)

        self.setLayout(layout)
        layout.addStretch()
        
            
    def filterPass(self, entry):
        """decide whether entry should remain in dataset which is display or not

        Args:
            entry (_type_): _description_

        Returns:
            _type_: true if entry should be displayed
                    false if entry should not be displayed
        """
        if not self.active:
            return True
        
        if entry[self.colLabel] == 'None' or entry[self.colLabel] == self.main_window.vep_placeholder:
            return self.noInfo 
        
        self.rowValue = float(entry[self.colLabel])
        return self.rowValue >= self.inputValue
    
    def on_toggled(self, state):
        self.active = state
        
    def noInfoToggle(self, state):
        self.noInfo = state
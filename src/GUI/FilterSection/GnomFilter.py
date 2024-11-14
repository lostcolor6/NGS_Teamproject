from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QDoubleSpinBox
from src.GUI.FilterSection.CutoffFilter import CutoffFilter

class GnomAmrFilter(CutoffFilter):
    def __init__(self, main_window):
        self.main_window = main_window
        super().__init__()

    label = 'Gnom amr freq'
    lowerBound = 0
    upperBound = 1
    decimals = 5
    initValue = 0
    colLabel = 'gnomAD amr'
    groupLabel = 'Gnom Freq'
    active = True
    
class GnomNfeFilter(CutoffFilter):
    def __init__(self, main_window):
        self.main_window = main_window
        super().__init__()

    label = 'Gnom nfe freq'
    lowerBound = 0
    upperBound = 1
    decimals = 5
    initValue = 0
    colLabel = 'gnomAD nfe'
    groupLabel = 'Gnom Freq'
    active = True
    
class GnomSasFilter(CutoffFilter):
    def __init__(self, main_window):
        self.main_window = main_window
        super().__init__()

    label = 'Gnom sas freq'
    lowerBound = 0
    upperBound = 1
    decimals = 5
    initValue = 0
    colLabel = 'gnomAD sas'
    groupLabel = 'Gnom Freq'
    active = True
    
class GnomAfrFilter(CutoffFilter):
    def __init__(self, main_window):
        self.main_window = main_window
        super().__init__()

    label = 'Gnom afr freq'
    lowerBound = 0
    upperBound = 1
    decimals = 5
    initValue = 0
    colLabel = 'gnomAD afr'
    groupLabel = 'Gnom Freq'
    active = True
    
class GnomEasFilter(CutoffFilter):
    def __init__(self, main_window):
        self.main_window = main_window
        super().__init__()

    label = 'Gnom eas freq'
    lowerBound = 0
    upperBound = 1
    decimals = 5
    initValue = 0
    colLabel = 'gnomAD eas'
    groupLabel = 'Gnom Freq'
    active = True
    

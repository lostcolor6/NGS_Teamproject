from .CutoffFilter import CutoffFilter

class AlphaScoreFilter(CutoffFilter):
    def __init__(self, main_window):
        self.main_window = main_window
        super().__init__()
        
    label = 'AlphaMissense Score'
    lowerBound = 0
    upperBound = 1
    decimals = 5
    initValue = 0
    colLabel = 'AlphaMissense'
    groupLabel = 'AlphaMissense Score'
    active = True

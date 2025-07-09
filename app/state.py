class AppState:
    def __init__(self):
        self.rx_vars = {}         # Holds Rx min/max StringVars
        self.axis_labels = {}     # Holds axis label StringVars
        self.data = None
        self.graph = None

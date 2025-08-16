import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from .state import AppState
from .plotter import draw

class PlotFrame(tk.Frame):
    def __init__(self, parent, state: AppState):
        super().__init__(parent, bg="white")
        self.state = state

        self.figure = Figure(figsize=(6, 6), dpi=120)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

    def redraw(self):
        if self.state.df is None:
            # blank axes when no data
            self.ax.clear()
            self.ax.set_title("Choose a CSV to begin (File → Open or right panel)")
            self.canvas.draw_idle()
            return
        draw(self.ax, self.state)
        self.canvas.draw_idle()

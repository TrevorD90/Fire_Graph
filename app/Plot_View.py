# app/Plot_View.py
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from .State import AppState
from .Plotter import draw

class PlotFrame(tk.Frame):
    """
    Embeds a Matplotlib plot in Tk.

    Features:
      • Mouse wheel zoom (centered at cursor) — smooth and jitter-free
      • Native toolbar pan/zoom — smooth; we only do a full redraw on mouse release
      • Reset View — snaps back to data-driven extents
      • Lines are anchored in data/world coordinates (handled in Plotter.draw)
    """
    def __init__(self, parent, state: AppState):
        super().__init__(parent, bg="white")
        self.state = state

        # Figure + Axes
        self.figure = Figure(figsize=(6, 6), dpi=120)
        self.ax = self.figure.add_subplot(111)

        # Canvas
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

        # Native Matplotlib toolbar (pan/zoom tools)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()

        # Events
        self.canvas.mpl_connect("scroll_event", self._on_scroll)
        # When user finishes a toolbar pan/zoom, do one full redraw to sync secondary axes
        self.canvas.mpl_connect("button_release_event", self._on_mouse_release)

    # ---------------- Public API ----------------
    def redraw(self):
        """Full redraw via Plotter.draw(state)."""
        if self.state.df is None:
            self.ax.clear()
            self.ax.set_title("Choose a CSV to begin (File → Open or right panel)")
            self.canvas.draw_idle()
            return
        draw(self.ax, self.state)
        self.canvas.draw_idle()

    def reset_view(self):
        """Snap back to data-driven bounds and redraw."""
        self.state.use_manual_axes = False
        self.state.x_min_manual = self.state.x_max_manual = None
        self.state.y_min_manual = self.state.y_max_manual = None
        self.redraw()

    # ---------------- Event handlers ----------------
    def _on_scroll(self, event):
        """Smooth zoom at mouse cursor; commits limits to state and redraws."""
        if self.state.df is None or event.inaxes != self.ax:
            return

        # Zoom factor
        scale = 0.9 if event.step > 0 else 1.1  # wheel up=in, down=out

        x, y = event.xdata, event.ydata
        x0, x1 = self.ax.get_xlim()
        y0, y1 = self.ax.get_ylim()

        w = (x1 - x0) * scale
        h = (y1 - y0) * scale

        # Keep cursor location anchored proportionally
        relx = (x - x0) / (x1 - x0) if (x1 - x0) != 0 else 0.5
        rely = (y - y0) / (y1 - y0) if (y1 - y0) != 0 else 0.5

        new_xlim = (x - w * relx, x + w * (1 - relx))
        new_ylim = (y - h * rely, y + h * (1 - rely))

        # Commit to state so secondary axes / labels / lines sync on redraw
        self.state.use_manual_axes = True
        self.state.x_min_manual, self.state.x_max_manual = new_xlim
        self.state.y_min_manual, self.state.y_max_manual = new_ylim

        self.redraw()

    def _on_mouse_release(self, event):
        """
        If the Matplotlib toolbar was in pan or zoom mode, commit current limits
        and do ONE full redraw to sync mirrored top/right axes and labels.
        """
        # NavigationToolbar2Tk.mode is '' (empty) when idle; values like 'pan/zoom' or 'zoom rect' when active
        try:
            mode = getattr(self.toolbar, "mode", "")
        except Exception:
            mode = ""

        if mode:  # only act if a toolbar interaction just happened
            # Capture current limits and redraw once
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()
            self.state.use_manual_axes = True
            self.state.x_min_manual, self.state.x_max_manual = xlim
            self.state.y_min_manual, self.state.y_max_manual = ylim
            self.redraw()

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk

class GraphView:
    def __init__(self, parent, state):
        self.parent = parent
        self.state = state

        self.figure = plt.Figure(figsize=(7, 6))
        self.ax = self.figure.add_subplot(111)  # Bottom X: Temp, Left Y: Wind

        # Top axis (RH)
        self.ax_rh = self.figure.add_axes(self.ax.get_position(), frameon=False)
        self.ax_rh.xaxis.set_ticks_position('top')
        self.ax_rh.xaxis.set_label_position('top')
        self.ax_rh.spines['top'].set_position(('outward', 40))
        self.ax_rh.spines['left'].set_color('none')
        self.ax_rh.spines['right'].set_color('none')
        self.ax_rh.spines['bottom'].set_color('none')
        self.ax_rh.yaxis.set_visible(False)

        # Right axis (Fuel Moisture)
        self.ax_fuel = self.figure.add_axes(self.ax.get_position(), frameon=False)
        self.ax_fuel.yaxis.set_ticks_position('right')
        self.ax_fuel.yaxis.set_label_position('right')
        self.ax_fuel.spines['right'].set_position(('outward', 60))
        self.ax_fuel.spines['left'].set_color('none')
        self.ax_fuel.spines['top'].set_color('none')
        self.ax_fuel.spines['bottom'].set_color('none')
        self.ax_fuel.xaxis.set_visible(False)

        self.canvas = FigureCanvasTkAgg(self.figure, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, parent)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(fill="both", expand=True)

        self.redraw_button = tk.Button(parent, text="Redraw Graph", command=self.plot_data)
        self.redraw_button.pack(pady=5)

    def padded_limits(self, series):
        min_val, max_val = series.min(), series.max()
        pad = (max_val - min_val) * 0.1 if max_val != min_val else 1
        return min_val - pad, max_val + pad

    def plot_data(self):
        self.ax.clear()
        self.ax_rh.clear()
        self.ax_fuel.clear()

        data = self.state.data
        if data is None:
            return

        try:
            temp = data['Temp']
            wind = data['Wind']
            rh = data['RH']
            fuel = data['Fuel Moisture']
            time = data['Time']
        except KeyError:
            print("Missing required columns")
            return

        # Main axis: Temp vs Wind
        self.ax.scatter(temp, wind, color='blue')
        for i in range(len(temp)):
            self.ax.text(temp[i], wind[i], str(time[i]), fontsize=7, ha='left', va='bottom', color='black')

        # Top axis (RH vs Index for layout only)
        self.ax_rh.scatter(rh, wind, color='blue')
        self.ax_rh.set_xlim(*self.padded_limits(rh))

        # Right axis (Fuel vs Wind)
        self.ax_fuel.scatter(wind, fuel, color='blue')
        self.ax_fuel.set_ylim(*self.padded_limits(fuel))
        self.ax_fuel.set_xlim(*self.padded_limits(wind))

        # Set axis labels
        self.ax.set_xlabel(self.state.axis_labels.get("bottom", "Temperature") or "Temperature", labelpad=10)
        self.ax.set_ylabel(self.state.axis_labels.get("left", "Wind Speed") or "Wind Speed", labelpad=10)
        self.ax_rh.set_xlabel(self.state.axis_labels.get("top", "Relative Humidity") or "Relative Humidity", labelpad=10)
        self.ax_fuel.set_ylabel(self.state.axis_labels.get("right", "Fuel Moisture") or "Fuel Moisture", labelpad=10)

        # Set main axis limits
        self.ax.set_xlim(*self.padded_limits(temp))
        self.ax.set_ylim(*self.padded_limits(wind))

        # Reapply label positions (reset by .clear())
        self.ax.yaxis.set_label_position("left")
        self.ax.yaxis.tick_left()
        self.ax_rh.xaxis.set_label_position("top")
        self.ax_rh.xaxis.tick_top()
        self.ax_fuel.yaxis.set_label_position("right")
        self.ax_fuel.yaxis.tick_right()

        self.ax.grid(True)
        self.canvas.draw()
        self.draw_rx_lines()

    def draw_rx_lines(self):
        try:
            t_min = float(self.state.rx_vars["Temp"][0].get())
            t_max = float(self.state.rx_vars["Temp"][1].get())
            rh_min = float(self.state.rx_vars["RH"][0].get())
            rh_max = float(self.state.rx_vars["RH"][1].get())
            w_min = float(self.state.rx_vars["Wind"][0].get())
            w_max = float(self.state.rx_vars["Wind"][1].get())
            fm_min = float(self.state.rx_vars["Fuel"][0].get())
            fm_max = float(self.state.rx_vars["Fuel"][1].get())
        except ValueError:
            return

        # Rx lines for RH (top axis, x = RH)
        self.ax_rh.plot([rh_max, rh_max], [w_min, w_max], color='red', linestyle='--')  # Min Temp → Max RH
        self.ax_rh.plot([rh_min, rh_min], [w_max, w_min], color='red', linestyle='--')  # Max Temp → Min RH

        # Rx lines for Fuel (right axis, y = Fuel, x = Wind)
        self.ax_fuel.plot([w_min, w_min], [fm_min, fm_max], color='red', linestyle='--')  # Min Wind → Max Fuel
        self.ax_fuel.plot([w_max, w_max], [fm_max, fm_min], color='red', linestyle='--')  # Max Wind → Min Fuel

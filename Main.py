from matplotlib.lines import drawStyles

from utilities import ReadData as rd
from utilities import Settings as sg
from utilities import Draw_Graph as drawg

data = rd.import_csv()
settings = sg.set_axis_parameters(data)
drawg.set_axis(settings)

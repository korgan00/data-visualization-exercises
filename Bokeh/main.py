import pandas as pd
import numpy as np

from bokeh.plotting import figure
from bokeh.io import show, curdoc
from bokeh.plotting import ColumnDataSource
from bokeh.palettes import Spectral
from bokeh.models import CategoricalColorMapper, HoverTool, Slider, Select, Range1d
from bokeh.models.filters import Filter
from bokeh.models.annotations import Title
from bokeh.layouts import row, column, widgetbox
from bokeh import models

# BEGIN functions

def createFigure():
	"create a figure"
	p = figure(title = 'Gapminder Data for %d' % yearSlider.value,
						 plot_width = 800,
						 plot_height = 600,
						 tools = [hover],
						 x_range = (min(gapminderData[xCombobox.value]), 
												max(gapminderData[xCombobox.value])),
						 y_range = (min(gapminderData[yCombobox.value]), 
												max(gapminderData[yCombobox.value])))

	print(xCombobox.value)
	print(yCombobox.value)
	
	p.circle(x = 'x', 
					 y = 'y', 
					 color = {'field': 'region', 'transform': colorMapper}, 
					 alpha = 0.7, 
					 legend = 'region',
					 radius = 'z',
					 source = gapminderSource,
					 line_width = 1,
					 line_color = (50, 50, 50),
					 line_alpha = 0.3)
	p.xaxis.axis_label = xCombobox.value
	p.yaxis.axis_label = yCombobox.value

	return p

def cbYearSelector(attr, old, new):
	gapminderSource.data = ColumnDataSource(createDict()).data
	layout.children[1].title.text = 'Gapminder Data for %d' % yearSlider.value

def cbOnAxisChange(attr, old, new):
	fig.xaxis.axis_label = xCombobox.value
	fig.yaxis.axis_label = yCombobox.value
	fig.x_range.start = min(gapminderData[xCombobox.value])
	fig.x_range.end = max(gapminderData[xCombobox.value])
	fig.y_range.start = min(gapminderData[yCombobox.value])
	fig.y_range.end = max(gapminderData[yCombobox.value])
	gapminderSource.data = ColumnDataSource(createDict()).data
		
  
def createDict():
	return dict(x = gapminderIndexedData.loc[yearSlider.value][xCombobox.value], 
							y = gapminderIndexedData.loc[yearSlider.value][yCombobox.value], 
							z = gapminderIndexedData.loc[yearSlider.value][zCombobox.value], 
							region = gapminderIndexedData.loc[yearSlider.value]['region'], 
							Country = gapminderIndexedData.loc[yearSlider.value]['Country'], 
							Population = gapminderIndexedData.loc[yearSlider.value]['population (10^8)'] * 100000000, 
							GDP = gapminderIndexedData.loc[yearSlider.value]['gdp (10^4)'] * 10000)
#1000000000

# END functions

###################
# APP interactions
###################

# hovertool
hover = HoverTool(tooltips = [("Country", "@Country"), ("Population", "@Population"), ("GDP", "@GDP")])

# year selector
yearSlider = Slider(title = 'Year', start = 1970, end = 2010, step = 1, value = 1970)
yearSlider.on_change('value', cbYearSelector)

# data selector
xCombobox = Select(title = "x-axis data", options = ['fertility', 'life', 'population (10^8)', 'child_mortality', 'gdp (10^4)'], value = 'fertility')
xCombobox.on_change('value', cbOnAxisChange)
yCombobox = Select(title = "y-axis data", options = ['fertility', 'life', 'population (10^8)', 'child_mortality', 'gdp (10^4)'], value = 'life')
yCombobox.on_change('value', cbOnAxisChange)
zCombobox = Select(title = "size data", options = ['population radius', 'gdp radius'], value = 'population radius')
zCombobox.on_change('value', cbOnAxisChange)


#######################
# DATA & VISUALIZATION
#######################

# SRCs
gapminderData = pd.read_csv('gapminder_data.csv')
gapminderData['population (10^8)'] = gapminderData['population']/100000000
gapminderData['gdp (10^4)'] = gapminderData['gdp']/10000
gapminderData['population radius'] = np.sqrt(gapminderData['population (10^8)']/(np.pi*10))
gapminderData['gdp radius'] = np.sqrt(gapminderData['gdp (10^4)']/(np.pi*10))
gapminderIndexedData = gapminderData.set_index('Year')
gapminderSource = ColumnDataSource(createDict())
#gapminderSource = ColumnDataSource(gapminderIndexedData.loc[1970])

# color mapper
colorMapper = CategoricalColorMapper(factors=['South Asia', 'Europe & Central Asia', 'Middle East & North Africa', 'East Asia & Pacific', 'Sub-Saharan Africa', 'America'], palette = Spectral[6])

# Figure
fig = createFigure()

#########
# LAYOUT
#########

col = column([widgetbox(yearSlider), widgetbox(xCombobox), widgetbox(yCombobox), widgetbox(zCombobox)])
layout = row([col, fig])
curdoc().add_root(layout)
curdoc().title = "Gapminder"

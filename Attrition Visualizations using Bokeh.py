"""
MFG: 598
Engineering Computing with Python
Final Project
Author: RajHukre
ASU ID: 1227157726
Description: This project analyzes the IBM HR Analytics dataset to uncover factors driving employee attrition.
Using causal discovery tools like CDT and libraries such as NumPy and scikit-learn, 
it generates actionable insights through graphs and charts, aiding organizations in improving retention strategies.
"""

# Imports
import numpy as np
import pandas as pd
from math import pi
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper, ColorBar
from bokeh.layouts import gridplot
from bokeh.transform import cumsum, transform
from bokeh.palettes import Viridis256, Category20

# Load the dataset
data = pd.read_csv('attrition.csv')

#######################################################################################################################

# SCATTER PLOT
scatter_source = ColumnDataSource(data=dict(age=data['Age'], income=data['MonthlyIncome'], exit=data['Attrition']))
attrition_color = transform('exit', LinearColorMapper(palette=['blue', 'orange'], factors=['No', 'Yes']))

scatter = figure(title="Age vs Monthly Income with Attrition", tools="hover")
scatter.scatter(x='age', y='income', source=scatter_source, size=10, color=attrition_color)
scatter.add_tools(HoverTool(tooltips=[("Age", "@age"), ("Income", "@income"), ("Attrition", "@exit")]))

scatter.xaxis.axis_label = "Age"
scatter.yaxis.axis_label = "Monthly Income"

#######################################################################################################################

# DONUT CHART
education_groups = data.groupby(['EducationField', 'Attrition']).size().unstack(fill_value=0)
edu_labels = education_groups.columns.values
edu_data = dict(field=education_groups.index.values)

for label in edu_labels:
    edu_data[label] = education_groups[label].values

edu_angles = [sum(edu_data[label]) / sum(sum(edu_groups)) * 2 * pi for label in edu_labels]
edu_colors = Category20[len(edu_angles)]

donut_source = ColumnDataSource(data=dict(labels=edu_labels, angle=edu_angles, color=edu_colors))
donut = figure(title="Attrition by Education Field", tools="hover", tooltips="@labels: @angles")
donut.wedge(x=0, y=0, radius=0.9, start_angle=cumsum('angle'), color=factor.fill_labels)
show(grid)

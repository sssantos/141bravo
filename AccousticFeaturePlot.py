from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.charts import Bar
from bokeh.models import HoverTool, CustomJS, ColumnDataSource
from bokeh.models.widgets import Select
from bokeh.layouts import column, widgetbox
from bokeh.io import output_file, show
import Tasks2
import pandas as pd
data = Tasks2.final_data

output_file("AccousticFeaturePlot.html")

source = ColumnDataSource(data = {
    "x": data['Year'],
    "y": data['acousticness'],
    "acousticness": data['acousticness'],
    "energy": data['energy'],
    "instrumentalness": data['instrumentalness'],
    "danceability": data['danceability'],
    "key": data['key'],
    "liveness": data['liveness'],
    "loudness": data['loudness'],
    "songLength": data['songLength'],
    "speechiness": data['speechiness'],
    "tempo": data['tempo'],
    "valence": data['valence'], 
    "Title": data['Title'],
    "Artist": data["Artist"]
})

hover = HoverTool(tooltips=[
    ('Title', '@Title'),
    ('Artist', '@Artist'),
    ('(x,y)', '($x,$y)')])

plot = figure(title="Year vs Feature", tools=[hover], plot_width=400,plot_height=400)
plot.circle(x = "x", y = "y",legend = False, source = source)
plot.xaxis.axis_label = 'Year'
plot.yaxis.axis_label = 'Feature'
# In the JavaScript code, `cb_obj` is the widget object and `source` is the
# data object.
callback = CustomJS(args=dict(source=source), code="""
        var data = source.data;
        x = data['x'];
        data['y'] = data[cb_obj.value];
        title: data['Title']
        source.trigger('change');
    """)

select = Select(title="Acoustic Feature:", value="acousticness", options=['acousticness','energy','instrumentalness', 'danceability',
                     'key','liveness','loudness','songLength','speechiness','tempo','valence'])
select.js_on_change('value', callback)
layout = column(select, plot)

show(layout)
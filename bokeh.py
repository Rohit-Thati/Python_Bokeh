import MySQLdb
from bokeh import *
from bokeh.sampledata import us_states
from bokeh.plotting import *
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LogColorMapper
)
from bokeh.palettes import Viridis6 as palette
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label


def state():
    db = MySQLdb.connect("reports-rds.adfdata.net" ,"raviranjan" ,"raviranjan123" ,"decision")
    cursor = db.cursor()
    cur = db.cursor(MySQLdb.cursors.DictCursor)
    query = " select  s_name, count(applicationid) app, count(distinct case when applicationid is not null and appstatus like '%approve%' then ApplicationID end)appr \
                from reports.state_map left join contact on code = state left join application using(lead_id)  where s_name not in ('Hawaii','Alaska')  group by 1;"
    cur.execute(query)
    result = cur.fetchall()
    print result
    return result

res  = state()
app = []
appr = []
 

palette.reverse()    
us_states = us_states.data.copy()

del us_states["HI"]
del us_states["AK"]

# separate latitude and longitude points for the borders
#   of the states.
state_xs = [us_states[code]["lons"] for code in us_states]
state_ys = [us_states[code]["lats"] for code in us_states]
state_name = [us_states[code]["name"] for code in us_states]


for k in range(0, len(state_name)):
    for i in range(0,49):
       if state_name[k] == res[i]["s_name"]:
           #print res[i]["s_name"]
           #print res[i]["app"]
           app.append(res[i]["app"])
           appr.append(res[i]["appr"])



print (state_name)
print (app)
print (appr)


color_mapper = LogColorMapper(palette=palette)
source = ColumnDataSource(data=dict(
x = state_xs,
y = state_ys,
states = state_name,
applications = app,
approvals = appr,
name=['Alabama','Alaska','Arizona','California','Colorado','Connecticut','Delaware','District of Columbia','Florida','Georgia','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming'],

lats=['32.806671','61.370716','33.729759','36.116203','39.059811','41.597782','39.318523','38.897438','27.766279','33.040619','44.240459','40.349457','39.849426','42.011539','38.5266','37.66814','31.169546','44.693947','39.063946','42.230171','43.326618','45.694454','32.741646','38.456085','46.921925','41.12537','38.313515','43.452492','40.298904','34.840515','42.165726','35.630066','47.528912','40.388783','35.565342','44.572021','40.590752','41.680893','33.856892','44.299782','35.747845','31.054487','40.150032','44.045876','37.769337','47.400902','38.491226','44.268543','42.755966'],


lons=['-86.79113','-152.404419','-111.431221','-119.681564','-105.311104','-72.755371','-75.507141','-77.026817','-81.686783','-83.643074','-114.478828','-88.986137','-86.258278','-93.210526','-96.726486','-84.670067','-91.867805','-69.381927','-76.802101','-71.530106','-84.536095','-93.900192','-89.678696','-92.288368','-110.454353','-98.268082','-117.055374','-71.563896','-74.521011','-106.248482','-74.948051','-79.806419','-99.784012','-82.764915','-96.928917','-122.070938','-77.209755','-71.51178','-80.945007','-99.438828','-86.692345','-97.563461','-111.862434','-72.710686','-78.169968','-121.490494','-80.954453','-89.616508','-107.30249']
))



TOOLS = "pan,wheel_zoom,reset,hover,save"
# init figure
p = figure(title="State Portfolio",tools=TOOLS,
           toolbar_location="left", plot_width=1100, plot_height=700)
mytext=Label(x=-100,y=30,text='TEXAS')

# Draw state lines
#p.patches('x', 'y', source=source,
 #        fill_alpha=0.7, line_color="#884444", line_width=1.5)



labels = LabelSet(text='name', level='glyph',
              source=source, render_mode='canvas')
p.add_layout(labels)
p.add_layout(mytext)

p.grid.grid_line_color = None

p.patches('x', 'y', source=source,
          fill_color={'field': 'applications', 'transform': color_mapper},
          fill_alpha=0.7, line_color="white", line_width=0.5)



hover = p.select_one(HoverTool)
hover.point_policy = "follow_mouse"

hover.tooltips = [
    ("Name", "@states"),
    ("App Count", "@applications"),
    ("Approval Count", "@approvals"),
  
]


# output to static HTML file
output_file("state_Portfolio.html")


# show results
show(p)

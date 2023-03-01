import dash
import dash_cytoscape as cyto
import networkx as nx
import plotly.colors as colors
from dash import html
from collections import Counter
from dash import dcc
from dash.dependencies import Output, Input, State
from dash import dash_table

app = dash.Dash(__name__)

# read networkx graph that we created using notebook
G = nx.read_gml("layout2.gml")
server = app.server


#setting colors of the nodes on the basis of there catagoires
channel_catagory = {}
for node in G.nodes(data=True):
    channel_catagory[node[0]] = node[1]["channel_catagory"]

## setting node positions
node_pos = {}
for node in G.nodes(data=True):
    #print(node)
    node_pos[node[0]] = node[1]["postions"]

##Total availibale catagories
lss = list()
for lis in list(channel_catagory.values()):
    for cat in lis:
        lss.append(cat)
#print("Total unique content catagoires : ",len(set(lss)))
my_counter = Counter(lss)
#print(my_counter)
total_Catagories = len(set(my_counter.keys()))

"""print(channel_catagory.values())
my_counter = Counter(channel_catagory.values())
total_Catagories = len(set(my_counter.keys()))
"""

# Sort the values in descending order
sorted_values = [value for value, count in my_counter.most_common()]
colornames = """aliceblue, antiquewhite, aqua, aquamarine, azure,
              beige, bisque, black, blanchedalmond, blue,
                blueviolet, brown, burlywood, cadetblue,
                chartreuse, chocolate, coral, cornflowerblue,
                cornsilk, crimson, cyan, darkblue, darkcyan,
                darkgoldenrod, darkgray, darkgrey, darkgreen,
                darkkhaki, darkmagenta, darkolivegreen, darkorange,
                darkorchid, darkred, darksalmon, darkseagreen,
                darkslateblue, darkslategray, darkslategrey,
                darkturquoise, darkviolet, deeppink, deepskyblue,
                dimgray, dimgrey, dodgerblue, firebrick,
                floralwhite, forestgreen, fuchsia, gainsboro,
                ghostwhite, gold, goldenrod, gray, grey, green,
                greenyellow, honeydew, hotpink, indianred, indigo,
                ivory, khaki, lavender, lavenderblush, lawngreen,
                lemonchiffon, lightblue, lightcoral, lightcyan,
                lightgoldenrodyellow, lightgray, lightgrey,
                lightgreen, lightpink, lightsalmon, lightseagreen,
                lightskyblue, lightslategray, lightslategrey,
                lightsteelblue, lightyellow, lime, limegreen,
                linen, magenta, maroon, mediumaquamarine,
                mediumblue, mediumorchid, mediumpurple,
                mediumseagreen, mediumslateblue, mediumspringgreen,
                mediumturquoise, mediumvioletred, midnightblue,
                mintcream, mistyrose, moccasin, navajowhite, navy,
                oldlace, olive, olivedrab, orange, orangered,
                orchid, palegoldenrod, palegreen, paleturquoise,
                palevioletred, papayawhip, peachpuff, peru, pink"""
color_name = []

for color in colornames.split(","):
  if(color== "\n"):
    continue
  else:
    color_name.append(color.strip())


import random
color_names = random.sample(color_name, k=total_Catagories)


#color_names = [name.strip() for name in color_name][:total_Catagories:]

#print(len(color_names))
#print(total_Catagories)
#print(len(my_counter))
#print(len(sorted_values))

color_map = {}
for i in range(len(color_names)):
    color_map[sorted_values[i]] = color_names[i]

#print(color_map)


# Convert the graph to a Cytoscape-compatible format



elements_nodes = []
elements_edges = []
for node in G.nodes(data=True):
    role = ""
    if("Employee_Role" in node[1].keys()):
      role = node[1]["Employee_Role"]
    else:
      role = "No Role Info"
    #print(node_pos[node[0]][0], node_pos[node[0]][1])
    color_m = node[1]["channel_catagory"][0]
    element = {'data': {'id': str(node[0]),
                       'size':float(node[1]["sub_count"])*1.4,
                       'fontsize':float(node[1]["sub_count"])*0.8,
                       'sub_c':float(node[1]["sub_count"]),
                        "label":str(node[0]),
                        "url":node[1]["Image"],
                       "color":color_map[color_m],
                       "niche":node[1]["channel_catagory"],
                      "channel_emp":node[1]["channel_employess"],
                      "role":role},
                'position':{'x':node_pos[node[0]][0], 'y':node_pos[node[0]][1]}
                      }
    elements_nodes.append(element)

#print(elements_nodes)
for edge in G.edges():
    colo_ede=channel_catagory[edge[0]][0]
    element = {'data': {'source': str(edge[0]), 'target': str(edge[1]),'color':color_map[colo_ede]}}
    elements_edges.append(element)

cyto_data = {'elements': elements_nodes+elements_edges}

# Create a Cytoscape layout 
layout = {'name': 'preset',
      'nodeSpacing': 100,
      'padding': 50,
      'avoidOverlap': True
    }

# Set the style of the Cytoscape component of the graph
style = {'width': '78%', 'height': '600px', 'border-width': '1px', 'float': 'right'}

# Define the style of the Cytoscape node
node_style = {
    'width': 'data(size)',
    'height': 'data(size)',
    'label': 'data(label)',
    'font-size': 'data(fontsize)',
    'background-color': 'data(color)',
    'text-halign': 'center',
    'text-valign': 'center',
    'background-fit': 'cover',
    'background-image': 'data(url)'
}

# set edge style
edge_style = {
    'width': '0.4px',
    'curve-style': 'bezier',
    'line-color':'data(color)'
}

# set the style of the navigation panel
nav_style = {
    'position': 'absolute',
    'top': '0',
    'left': '0',
    'bottom': '0',
    'width': '28%',
    'height':'90%',
    'padding': '20px',
    'background-color': '#f8f8f8',
    'overflow': 'scroll'
}

# Define the dropdown options
dropdown_options = [{'label': 'Preset', 'value': 'preset'},
                    {'label': 'Circular layout', 'value': 'circle'},
                    #{'label': 'Concentric layout', 'value': 'concentric'},
                    #{'label': 'cose', 'value': 'cose'},
                    {'label': 'grid', 'value': 'grid'}]

#callback function for drop down
@app.callback(Output('Graph', 'children'),
              [Input('my-dropdown', 'value')])
def update_output(value):
    if(value == "preset"):
      # Create a Cytoscape layout

      layout = {'name': 'preset',
            'nodeSpacing': 100,
            'padding': 50,
            'avoidOverlap': True
          }
    if(value == "circle"):
      # Create a Cytoscape layout
      layout = {'name': 'circle',
            'nodeSpacing': 100,
            'padding': 50,
            'avoidOverlap': True
          }
    elif(value == "concentric"):
      layout = {'name': 'concentric',
            'nodeSpacing': 100,
            'padding': 50,
            'avoidOverlap': True
          }
    elif(value == 'cose'):
      layout = {'name': 'cose',
            'nodeSpacing': 100,
            'padding': 50,
            'avoidOverlap': True
          }
    elif(value == "grid"):
      layout = {'name': 'grid',
            'nodeSpacing': 100,
            'padding': 50,
            'avoidOverlap': True
          }
    # Create the Cytoscape component with the specified style
    cyto_component = cyto.Cytoscape(
        id='cytoscape',
        elements=cyto_data['elements'],
        layout=layout,
        style=style,
        stylesheet=[{
            'selector': 'node',
            'style': node_style
        },
        {
            'selector': 'edge',
            'style': edge_style
        }]
    )
    return cyto_component

def get_selected_elements(selected_elements):
  elements_nodes_1 = []
  elements_edges_2 = []

  for node in G.nodes(data=True):
      role = ""
      if("Employee_Role" in node[1].keys()):
        role = node[1]["Employee_Role"]
      else:
        role = "No Role Info"

      color_m = node[1]["channel_catagory"]
      for cat in color_m:
        if(cat in selected_elements):
          element = {'data': {'id': str(node[0]),
                       'size':float(node[1]["sub_count"])*1.4,
                       'fontsize':float(node[1]["sub_count"])*0.8,
                       'sub_c':float(node[1]["sub_count"]),
                        "label":str(node[0]),
                        "url":node[1]["Image"],
                       "color":color_map[cat],
                       "niche":node[1]["channel_catagory"],
                      "channel_emp":node[1]["channel_employess"],
                      "role":role},
          'position':{'x':node_pos[node[0]][0], 'y':node_pos[node[0]][1]}}
          elements_nodes_1.append(element)
          break
  for edge,edge2 in G.edges():
    for cat in selected_elements:
      if(cat in channel_catagory[edge] and cat in channel_catagory[edge2]):

        #if(channel_catagory[edge] in selected_elements and channel_catagory[edge2] in selected_elements):
        """if(len(channel_catagory[edge[0]])>1 and len(channel_catagory[edge[1]]) >1):
                  if(channel_catagory[edge[0]][0] in selected_elements and channel_catagory[edge[0]][1] in selected_elements and channel_catagory[edge[1]][0] in selected_elements and channel_catagory[edge[1]][1] in selected_elements):
                    #print(edge[0])
                    #print(selected_elements,channel_catagory[edge[0]], channel_catagory[edge[1]])"""
        element = {'data': {'source': str(edge), 'target': str(edge2),'color':color_map[colo_ede]}}
        elements_edges_2.append(element)
  return elements_nodes_1, elements_edges_2


@app.callback(Output('cytoscape', 'elements'),
              Input('my-checkbox', 'value'),
              State('cytoscape', 'stylesheet'))

def update_output(value,stylesheet):
    if(len(value)>1):
      value = value[1:]
    print(value)
    if 'edges' in value:
      cyto_data = {'elements': elements_nodes+elements_edges}
      return cyto_data['elements']
    elif('notedges' in value):
      cyto_data = {'elements': elements_nodes}
      return cyto_data['elements']
    else:
      elements_nodes_1,elements_edges_2 = get_selected_elements(value)
      cyto_data = {'elements': elements_nodes_1+elements_edges_2}
      print("print:",len(elements_nodes_1))
      return cyto_data['elements']
    



catagoires =color_map.keys()
options = [{'label': 'Show edges', 'value': 'edges'}]
options = options+[{'label': f'{i}', 'value': f'{i}'} for i in catagoires]



# Define the content of the navigation panel
nav_content = html.Div([
    dcc.Dropdown(id='my-dropdown',
                 options=dropdown_options,
                 value='preset',disabled=True),
    #html.Div(id='my-output'),
    html.Div(id='node-info'),
    html.Hr(),
    html.H3('Top catagoires'),
    html.Hr(),
    dcc.Checklist(
        id='my-checkbox',
        options=options,
        value=["edges"],
        labelStyle={'display': 'block'}
    ),

    html.Div(id='output'),

    

])

#callback function to display node features on click
@app.callback(Output('node-info', 'children'),
              Input('cytoscape', 'tapNode'),
              State('cytoscape', 'elements'))

def display_node_info(node, elements):
    nav_content_for_node = html.Div([
      html.H3("Click Node to see details"),
      html.Hr(),
      ])

    style2= {
      'position': 'absolute', 'bottom': '0'
    }
    if not node:
      return html.Div( children=nav_content_for_node)
   
    node_data = next((x for x in elements if x['data']['id'] == node['data']['id']))
    if not node_data:
        return html.Div()

    node_id = node_data['data']['id']
    node_label = node_data['data']['label']
    # Add more node features as needed

    # create emplyoee details rows using a for loop
    chan_emp = node_data['data']['channel_emp']
    emp_role = node_data['data']['role']
    chan_emp_dic ={}
    loop_len = 0
    if(len(chan_emp)>len(emp_role)):
      loop_len = len(chan_emp)
    else:
      loop_len = len(emp_role)

    for i in range(loop_len):
      if(len(chan_emp)>i):
        print(chan_emp[i])
      else:
        print("No emplyee name")
      if(len(emp_role)>i):
        print(emp_role[i])
      else:
        emp_role.append("No role defined")

    rows = []
    for i in range(0, len(chan_emp)):
        row = {'Column 1': f'{chan_emp[i]}', 
           'Column 2': f'{emp_role[i]}'}
        rows.append(row)
  

    nav_content_for_node = html.Div([
      html.H3("Click Node to see details"),
      html.Hr(),

      html.Table([
                html.Tr([
                    html.Td(html.Strong(f"Label")),
                    html.Td(f"{node_data['data']['label']}")
                ]),
                html.Tr([
                    html.Td(html.Strong(f"Subsriber Count:")),
                    html.Td(f"{node_data['data']['sub_c']}")
                ]),
                html.Tr([
                    html.Td(html.Strong(f"niche:")),
                    html.Td(f"{node_data['data']['niche']}")
                ]),
               
      ]),

      dash_table.DataTable(
                      columns=[{'name': 'Employee Name', 'id': 'Column 1'},
                               {'name': 'Employee Role', 'id': 'Column 2'}],
                      data=rows,
                      style_table={'maxWidth': '100%'}

                ),
      
      ])
    

    return html.Div(children=nav_content_for_node)
    """return html.Div([
                    html.H4(f'Node: {node_label} ({node_id})'),
                    # Display more node features here
                ])"""


# Add the Cytoscape component to the app layout
#app.layout = html.Div([cyto_component])
# Add the Cytoscape component and navigation panel to the app layout
app.layout = html.Div([
    html.Div(style=nav_style, children=[nav_content]

      ),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(id ="Graph",label='Graph', value='tab-1', children=[
            html.Div([
                cyto.Cytoscape(
                id='cytoscape',
                elements=cyto_data['elements'],
                layout=layout,
                style=style,
                stylesheet=[{
                    'selector': 'node',
                    'style': node_style
                },
                {
                    'selector': 'edge',
                    'style': edge_style
                }]
            )
            ], style={"height":"100%",'float': 'right'}), 
        ],style={'width': '120%', "height":"100%",'float': 'left'}),
    ], style={'width': '120%', "height":"100%",'float': 'left'}),
    
])

if __name__ == '__main__':
    app.run_server(debug=True)

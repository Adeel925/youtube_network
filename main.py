## Importing some required libraires
import dash
import dash_cytoscape as cyto
import networkx as nx
import plotly.colors as colors
from dash import html
from collections import Counter
from dash import dcc
from dash.dependencies import Output, Input, State
from dash import dash_table
import pandas as pd
#import dash_bootstrap_components as dbc



## Calling dash app function
#app = dash.Dash(__name__)#,external_stylesheets=[dbc.themes.BOOTSTRAP])

app = dash.Dash(__name__, external_stylesheets=[
    "https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css"
])
server = app.server


## Read networkx graph that we created using notebook
G = nx.read_gml("Final2.gml")


## setting colors of the nodes on the basis of there catagoires
channel_catagory = {}
for node in G.nodes(data=True):
    channel_catagory[node[0]] = node[1]["channel_catagory"]

## setting node positions for the graph
node_pos = {}
for node in G.nodes(data=True):
    #print(node)
    node_pos[node[0]] = node[1]["postions"]

##Total availibale catagories
lss = list()
for lis in list(channel_catagory.values()):
    for cat in lis:
        lss.append(cat)


my_counter = Counter(lss)
total_Catagories = len(set(my_counter.keys()))

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


#color_names = [name.strip() for name in color_name][:total_Catagories

color_map = {}
for i in range(len(color_names)):
    color_map[sorted_values[i]] = color_names[i]

#print(color_map)
max_sub = 0
min_sub = 58

node_labe={}

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
    subcount = node[1]["sub_count"]

    if(pd.isna(subcount)):
      pass
    else:
      sub_end = subcount[-1:]
      sub_num = float(subcount.strip()[:-1])

      if(sub_end == "k" or sub_end == "K"):
        sub_num = sub_num/1000
      

      #settig maximum and minimu values for subsriber count
      if(max_sub < sub_num):
      	max_sub=sub_num
      if(min_sub < sub_num):
      	min_sub =sub_num


      if(sub_num <= 1):
        sub_num *= 12.4
      elif(sub_num <= 5):
        sub_num *= 5
      else:
        sub_num *= 4
    node_labe[node[0]]=str(node[0])
    element = {'data': {'id': str(node[0]),
                       'size':float(sub_num),
                       'fontsize':float(sub_num)*0.4,
                       'sub_c':str(node[1]["sub_count"]),
                        "label":str(node[0]),
                        "url":node[1]["Image"],
                       "color":color_map[color_m],
                       "niche":node[1]["channel_catagory"],
                      "channel_emp":node[1]["channel_employess"],
                      "emp_r":node[1]["Role_Classification"],
                      "emp_social":node[1]["Social_Handle"],
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
style = {'width': '80%', 'height': '740px','float':'right'}

# Define the style of the Cytoscape node
node_style = {
    'width': 'data(size)',
    'height': 'data(size)',
    'label': 'data(label)',
    'font-size': 'data(fontsize)',
    'background-color': 'data(color)',
    'text-halign': 'center',
    'text-valign': 'bottom',
    'background-fit': 'cover',
    'padding': '5px',
    'background-image': 'data(url)',
    #'shape': 'rectangle',
    'border-color': '#000000',
    'border-width': '1px',
    'color':'#1f77b4'
}

# set edge style
edge_style = {
    'width': '0.1px',
    'curve-style': 'bezier',
    'line-color':'data(color)',

}

# set the style of the navigation panel
nav_style = {
    'position': 'absolute',
    'top': '0',
    'left': '0',
    'bottom': '0',
    'width':"20%",
    'height':'600px',
    'overflow': 'scroll',
    #'background-color': 'blue'
}

def get_selected_elements(selected_elements,value2,label_scale):
  elements_nodes_1 = []
  elements_edges_2 = []

  for node in G.nodes(data=True):
      role = ""
      if("Employee_Role" in node[1].keys()):
        role = node[1]["Employee_Role"]
      else:
        role = "No Role Info"

      color_m = node[1]["channel_catagory"]

      subcount = node[1]["sub_count"]

      
      if(pd.isna(subcount)):
        pass
      else:
        sub_end = subcount[-1:]
        sub_num = float(subcount.strip()[:-1])
        
        
        if(sub_end == "k" or sub_end == "K"):
          sub_num = sub_num/1000
        #print(sub_num)
        #print(value2[0], value2[1], sub_num)
        if(sub_num<value2[0] and sub_num > value2[1]):
          continue
        else:
          for cat in color_m:
            if(cat in selected_elements):
              if(sub_num>value2[0] and sub_num <value2[1]):
                #print(sub_num)
                node_lab=""
                if(sub_num >= label_scale):
                  
                    node_lab  =node[0]
                else:
                    node_lab = ""

                if(sub_num <= 1):
                  sub_num *= 14.4
                elif(sub_num<=5):
                  sub_num*=5
                else:
                  sub_num *= 4
               
                
                element = {'data': {'id': str(node[0]),
                             'size':float(sub_num),
                             'fontsize':float(sub_num)*0.4,
                             'sub_c':str(node[1]["sub_count"]),
                              "label":node_lab,
                              "url":node[1]["Image"],
                             "color":color_map[cat],
                             "niche":node[1]["channel_catagory"],
                            "channel_emp":node[1]["channel_employess"],
                            "emp_r":node[1]["Role_Classification"],
                            "emp_social":node[1]["Social_Handle"],
                            "role":role},
                'position':{'x':node_pos[node[0]][0], 'y':node_pos[node[0]][1]}}
                elements_nodes_1.append(element)
                break

  for edge,edge2 in G.edges():
    selected_nodes = []
    for cat in elements_nodes_1:
      selected_nodes.append(cat["data"]["id"])
      #print(cat)
    if(edge in selected_nodes and edge2 in selected_nodes):

      color_m = G.nodes[edge]["channel_catagory"][0]
      element = {'data': {'source': str(edge), 'target': str(edge2),'color':color_map[color_m]}}
      elements_edges_2.append(element)
  return elements_nodes_1, elements_edges_2

def get_selected_channel(selected_elements,label_scale):
  elements_nodes_1 = []
  elements_edges_2 = []

  #print(selected_elements)
  for searched_node in selected_elements:
    #print(searched_node)
    for node in G.nodes(data=True):
      if(node[0] == searched_node):
          role = ""
          if("Employee_Role" in node[1].keys()):
            role = node[1]["Employee_Role"]
          else:
            role = "No Role Info"

          color_m = node[1]["channel_catagory"][0]
          subcount = node[1]["sub_count"]

        
          if(pd.isna(subcount)):
            pass
          else:
            sub_end = subcount[-1:]
            sub_num = float(subcount.strip()[:-1])

            if(sub_end == "k" or sub_end == "K"):
              sub_num = sub_num/1000

            node_lab=""
            if(sub_num>=label_scale):
                node_lab  =node[0]
            else:
                node_lab = ""
            
         
            if(sub_num <= 1):
              sub_num *= 14.4
            elif(sub_num <= 5):
              sub_num*=5
            else:
              sub_num *= 4

              
          element = {'data': {'id': str(node[0]),
                             'size':float(sub_num),
                             'fontsize':float(sub_num)*0.4,
                             'sub_c':str(node[1]["sub_count"]),
                              "label":node_lab,
                              "url":node[1]["Image"],
                             "color":color_map[color_m],
                             "niche":node[1]["channel_catagory"],
                            "channel_emp":node[1]["channel_employess"],
                            "emp_r":node[1]["Role_Classification"],
                            "emp_social":node[1]["Social_Handle"],
                            "role":role},
                      'position':{'x':node_pos[node[0]][0], 'y':node_pos[node[0]][1]}
                            }
          elements_nodes_1.append(element)
          break

  #print(elements_nodes_1)
  if(len(elements_nodes_1) >1):
    for edge1,edge2 in G.edges():
        if(edge1 in elements_nodes_1 and edge2 in elements_nodes_1):
          colo_ede=channel_catagory[edge1][0]
          if(G.has_edge(edge1, edge2)):
            #print(edge1, edge2)
            element = {'data': {'source': str(edge1), 'target': str(edge2),'color':color_map[colo_ede]}}
            elements_edges_2.append(element)
    u_data = elements_nodes_1+elements_edges_2
    return u_data
  else:
    return elements_nodes_1

#########################
#Edge width callback
#########################  
## Optimizing the edge width
@app.callback(
    Output('cytoscape', 'stylesheet'),
    [Input('edge-slider', 'value')]
)
def update_stylesheet(edge_width):
	# set edge style
    print(edge_width)
    node_style = {
    'width': 'data(size)',
    'height': 'data(size)',
    'label': 'data(label)',
    'font-size': 'data(fontsize)',
    'background-color': 'data(color)',
    'text-halign': 'center',
    'text-valign': 'bottom',
    'background-fit': 'cover',
    'padding': '5px',
    'background-image': 'data(url)',
    #'shape': 'rectangle',
    'border-color': '#000000',
    'border-width': "0.1px",
    'color':'#1f77b4'
    }

    # set edge style
    edge_style = {
    'width': f'{edge_width}px',
    'curve-style': 'bezier',
    'line-color':'data(color)'
    }
    style_output=[
        {
            'selector': 'node',
            'style': node_style
        },
        {
            'selector': 'edge',
            'style': edge_style
        }
    ]
    return style_output

#########################
#Update label, search label, content catagory callback
#########################

@app.callback(Output('cytoscape', 'elements'),
              [Input('catagory_search', 'value'), #reading input for specific content category
               Input('my-slider', 'value'),  #reading the inpit value for 
               Input("search-input", "value"), # searching the specific channel
               Input('label-slider', 'value'), # adjusting the labels.
               ],
              State('cytoscape', 'elements'))

def update_output(value,value2,search_term,label_scale,elements_u):
    value.append("edges")
    print(label_scale)
    label_scale = label_scale*(-1)
    
    ## searching the term
    if len(search_term) > 0:
      filtered_nodes = []
      for e in elements_nodes:
        #print(e["data"]["label"])
        if(e["data"]["label"] in search_term):
          filtered_nodes.append(e["data"]["label"])
          #print(e["data"]["label"], search_term,filtered_nodes)   
      if(len(filtered_nodes) == 0):
        return filtered_nodes,style_output#,'Selected  range "{}" and "{}"'.format(value2[0], value2[1]),"Channel Not found"
      else:#filtered_nodes = [e for e in elements if search_term.lower() in e["data"]["label"].lower()
        udata = get_selected_channel(filtered_nodes,label_scale)
        return udata
    else:
      ## selecting the specific content category
      if 'edges' in value and len(value) == 1:
        elements_nodes_1, elements_edges_2=get_selected_elements(list(color_map.keys()),value2,label_scale)
        return elements_nodes_1+elements_edges_2#cyto_data['elements']
      else:
        value.remove('edges')
        elements_nodes_1,elements_edges_2 = get_selected_elements(value,value2,label_scale)
        return elements_nodes_1+elements_edges_2#cyto_data['elements']
    
catagoires =color_map.keys()
options = []
options = options+[{'label': f'{i}', 'value': f'{i}'} for i in catagoires]


# Define the dropdown options"""
dropdown_options2 = [{"label": f'{node}', 'value':f'{node}'} for node in G.nodes()]



##############################
## Theme change call back
##############################
@app.callback(
    Output('theme_change', 'style'),
    Input('theme-selector', 'value')
)

def update_theme(theme):
    if theme == 'dark':
        return {'color': 'white', 'backgroundColor': 'black'}
    else:
        return {'color': 'black', 'backgroundColor': 'white'}

nav_content = html.Div([
    html.H6('Choose a Theme'),
    dcc.RadioItems(
        id='theme-selector',
        options=[
            {'label': 'Light', 'value': 'light'},
            {'label': 'Dark', 'value': 'dark'}
        ],
        value='dark',
        labelStyle={'display': 'inline-block'}
    ),
    html.Hr(style={'backgroundColor': 'green'}),
    html.H6("Search Channel"),
    dcc.Dropdown(
        id='search-input',
        multi=True,
        placeholder='Search channels...',
        options=dropdown_options2,
        value='',
        disabled=False,
        #className='mb-3',
        style={'color': 'black'}
    ),
    html.H6('Search Categories'),
    dcc.Dropdown(
        id='catagory_search',
        multi=True,
        placeholder='Search Categories...',
        options=options,
        value=[],
        disabled=False,
        #className='mb-3',
        style={'color': 'black'}
    ),
    html.Hr(style={'backgroundColor': 'green'}),
    html.H6('Set Line Width'),
    dcc.Slider(
        id='edge-slider',
        min=0,
        max=1,
        step=0.005,
        value=0.25,
        marks={
            0: {'label': 'Thinner'},
            1: {'label': 'Thicker'}
        },
        
    ),
    html.H6('Visible Channel Names'),
    dcc.Slider(
        id='label-slider',
        min=-60,
        max=0,
        step=4,
        value=-30,
        marks={
            -60: {'label': 'Less'},
            0: {'label': 'More'}
        },
        className='mb-3'
    ),
    html.H6('Subscriber Range'),
    dcc.RangeSlider(
        id='my-slider',
        min=0,
        max=60,
        step=4,
        value=[0,60],
        marks={
            0: {'label': '0m'},
            60: {'label': '58m'}
        },
      
    ),
    html.Hr(style={'backgroundColor': 'green'}),
],)


#########################
#Node details callback
#########################

#callback function to display node features on click
@app.callback(Output('node-info', 'children'),
              Input('cytoscape', 'tapNode'),
              State('cytoscape', 'elements'))
def display_node_info(node, elements):
    html.Hr(style={'backgroundColor': 'green'}),
    nav_content_for_node = html.Div([
      html.H3("Click Node to see details"),
      ],)

    if not node:
      return html.Div( children=nav_content_for_node)
   
    node_data = next((x for x in elements if x['data']['id'] == node['data']['id']))
    if not node_data:
        return html.Div()

    node_id = node_data['data']['id']
    node_label = node_data['data']['label']
    
    # create emplyoee details rows using a for loop
    chan_emp = node_data['data']['channel_emp']
    emp_role = node_data['data']['role']
    emp_role_class = node_data['data']['emp_r']
    emp_social_handle= node_data['data']['emp_social']
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
    df = pd.DataFrame(columns=["Employee Name", "Employee Role", "Role classification", "Socail Handle"])
    for i in range(0, len(chan_emp)):
        new_row = pd.Series({"Employee Name":chan_emp[i],
         "Employee Role":emp_role[i],
         "Role classification":emp_role_class[i],
         "Socail Handle":emp_social_handle[i],
        })
        new_row_df = pd.DataFrame([new_row], columns=df.columns)
        df = pd.concat([df, new_row_df], ignore_index=True)
    
    #print(df.head())
    groups = df.groupby('Role classification')
    separator = " "
    niches = separator.join(node_data['data']['niche'])


    nav_content_for_node = html.Div([
      html.H3("Channel Details"),
      html.Hr(style={'backgroundColor': 'green'}),

      html.Table([
                html.Tr([
                    html.Td(html.Strong(f"Channel Name:")),
                    html.Td(f"{node_labe[node_data['data']['id']]}")
                ]),
                html.Tr([
                    html.Td(html.Strong(f"Subscriber Count:")),
                    html.Td(f"{node_data['data']['sub_c']}")
                ]),
                html.Tr([
                    html.Td(html.Strong(f"Niche(s):")),
                    html.Td(f"{niches}")
                ]),
               
      ],style={"textAlign": "left","widht":"100%"}),
      html.Hr(style={'backgroundColor': 'green'}),
      *[html.Div(children=[
            html.H4(children=f"Role Classification: {name}"),
            dash_table.DataTable(
                columns=[{'name': col, 'id': col} for col in group.columns],
                data=group.to_dict('records'),
                style_cell={'backgroundColor': '#F1F1F1',},
                style_table={"color":"black"},
                style_header= {'fontWeight': 'bold',}
            )
        ]) for name, group in groups]
      
      ])

    return html.Div(children=nav_content_for_node)

# Adding the Cytoscape component and navigation panel to the app layout
app.layout = html.Div(children=[

  #nav division
    html.Div(style=nav_style, children=[nav_content]),
    
    #graph
    html.Div(id='tabs', children=[
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
            ]), 
        ]),

    ], style={'width': '100%','float': 'right'}),
    
    html.Div(id='node-info',style={"textAlign": "center", 
          "margin": "auto", "width": "80%",
        'overflow': 'scroll','background-color': 'lightseagreen',}),
    
],id="theme_change", 

style={
        'color': 'white',
        'backgroundColor': 'black',
        "width":"100%",
        'margin': 0,
        'padding': 0
    },

)

if __name__ == '__main__':
    app.run_server(debug=True)

# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 11:16:59 2020

@author: terry
"""
import random
from copy import deepcopy
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib.patches as patches


node_prob = 0.2
building_prob = 0.2

edgelist = pd.read_csv('edge.csv')
nodelist = pd.read_csv('nodes.csv')

#edgelist = pd.read_csv('C:/Users/terry/Desktop/TA/edge.csv')
#nodelist = pd.read_csv('C:/Users/terry/Desktop/TA/nodes.csv')

#print(edgelist.head(5))
#print(nodelist.head(10))

g = nx.Graph()

#for i,element in edgelist.iterrows():
#    g.add_edge(element[0],element[1], attr_dict=element[2:].to_dict())

for i,element in edgelist.iterrows():
    g.add_edge(element[0],element[1], weight=random.randint(5, 50),color= element[3])
    
    
#print(g.nodes)
#print(element[2:].to_dict())   
for i,element in nodelist.iterrows():
    g.nodes[element['id']].update(element[1:].to_dict())  
    
#for e in g.edges(data=True):
#   print(e[2]['attr_dict']['color'])
fig = plt.figure()
plt.title('Graph Representation', size=15)
#print(g.nodes['n32'])
#print('# of edges: {}'.format(g.number_of_edges()))
#print('# of nodes: {}'.format(g.number_of_nodes()))

# delete some nodes randomly
for node in list(g.nodes):    
    if(node == 'n00' or node == 'n44'):
        continue
    else:
        if(random.random() < node_prob):
            t = deepcopy(g)
            t.remove_node(node)
            if nx.is_connected(t):            
                g.remove_node(node)
            t.clear()
            
    
x_coor=[]  
y_coor=[]
for node in list(g.nodes): 
#    print(g.nodes[node]['x'])
    x_coor.append(g.nodes[node]['x'])
    y_coor.append(g.nodes[node]['y'])
   
nodemap = {'id': list(g.nodes),
     'x' : x_coor,
     'y' : y_coor
                                }
random_nodes = pd.DataFrame(nodemap,columns=['id','x','y'])
random_nodes.to_csv('random_nodes.csv',index=False)   

                         


            
# add buildings randomly
building_nodes = []
i=1
for node in list(g.nodes):    
    dic = {}
    if(g.nodes[node]['x'] ==0 or g.nodes[node]['x'] ==900 or  g.nodes[node]['y'] ==0 or  g.nodes[node]['y'] ==900):
        continue
    else:
        if(random.random() < building_prob or i == 0):
#            dic['id'] = 'building' + str(i)
            dic['id'] = chr(ord('@')+i)
            dic['x'] = g.nodes[node]['x'] + 50
            dic['y'] = g.nodes[node]['y']
            building_nodes.append(dic) 
            i = i+1
            
            g.add_node(dic['id'],x= dic['x'],y= dic['y'],height =random.randint(5, 20)  ) 
            g.add_edge(node,dic['id'],weight=random.randint(5, 50),color= 'black')

            adj_node = [x for x,y in g.nodes(data=True) if y['x']==g.nodes[node]['x']+100 and y['y'] ==g.nodes[node]['y']]
            for n in adj_node:
                g.remove_edge(node,n)   
                g.add_edge(n,dic['id'],weight=random.randint(5, 50),color= 'black')
#            print(adj_node)
#            print(g.nodes[node]['x'],g.nodes[node]['y'])
#            building_nodes.append([g.nodes[node]['x'] + 50,g.nodes[node]['y']])
   

build_id = []    
build_x = []
build_y = []
for build in building_nodes:
    build_id.append(build['id'])
    build_x.append(build['x'])
    build_y.append(build['y'])
    
building = {'id': build_id,
     'x' : build_x,
     'y' : build_y }

buildingnodes = pd.DataFrame(building,columns=['id','x','y'])
buildingnodes.to_csv('building_nodes.csv',index=False)  

edgenode = []
weight = []
for edge in list(g.edges):
    edgenode.append(edge)
    weight.append(g.edges[edge]['weight'])

left = []
right = []
#print(edgenode)

for item in edgenode:
    left.append(item[0])
    right.append(item[1])
    #    print(item[0])


edgenodes = {'node1': left,
     'node2' : right,
     'weight' : weight }

ednodes = pd.DataFrame(edgenodes,columns=['node1','node2','weight'])
ednodes.to_csv('random_edges.csv',index=False) 

#print(weight)
#print(list(g.edges))

#nx.write_edgelist(g,'random_edges.csv',data=['weight'])
#g.add_nodes_from(building_nodes)

for build in building_nodes:
#    print(build['id'])
#    g.add_node(build['id'],x= build['x'],y= build['y'] )
    fig.gca().add_patch(patches.Rectangle((build['x']-30,build['y']-80),60,60,edgecolor = 'black',facecolor = 'none'))
#print(building_nodes)    



       
#print(nx.shortest_path(g, source='n00', target='n44'))     
        
node_positions = {node[0]: (node[1]['x'], node[1]['y']) for node in g.nodes(data=True)}
#print(dict(list(node_positions.items())[0:5]))
#edge_colors = [e[2]['attr_dict']['color'] for e in g.edges(data=True)]  
edge_colors = [e[2]['color'] for e in g.edges(data=True)]  
labels = nx.get_node_attributes(g,'height')
print(labels)

nx.draw(g, pos=node_positions, edge_color=edge_colors,node_size=10, node_color='red')
nx.draw_networkx_labels(g,pos=node_positions,labels=labels,font_size=12,font_color='blue')



bbox = {'ec':[1,1,1,0], 'fc':[1,1,1,0]}
# hack to label edges over line (rather than breaking up line)
edge_labels = nx.get_edge_attributes(g,'weight')
#print(edge_labels)
nx.draw_networkx_edge_labels(g, pos=node_positions, edge_labels=edge_labels, bbox=bbox, font_size=10)
plt.axis('square')  
plt.show()


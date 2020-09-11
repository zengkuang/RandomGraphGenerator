# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 15:58:01 2020

@author: terry
"""


import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib.patches as patches
import matplotlib.animation as animation

edgelist = pd.read_csv('random_edges.csv')
nodelist = pd.read_csv('random_nodes.csv')
buildingnode = pd.read_csv('building_nodes.csv')

source_building = 'A'
destination_building = 'B'


g = nx.Graph()

for i,element in edgelist.iterrows():
    g.add_edge(element[0],element[1], weight=element[2])

for i,element in nodelist.iterrows():
    g.nodes[element['id']].update(element[1:].to_dict()) 
    
building_nodes = []    
for i,element in buildingnode.iterrows():
    g.nodes[element['id']].update(element[1:].to_dict()) 
    dic = {}
    dic['id'] = element['id']
    dic['x'] = element['x']
    dic['y'] = element['y']
    building_nodes.append(dic) 
   
#fig = plt.figure()
#ax = fig.add_subplot(111)

ax = plt.subplot(111)

plt.title('Graph Representation', size=15)

#for i,element in buildingnode.iterrows():
#    fig.gca().add_patch(patches.Rectangle((element['x']-30,element['y']-80),60,60,edgecolor = 'black',facecolor = 'none'))
number_id = 0
for build in building_nodes:
    number_id = number_id+1
        
    draw_x = [build['x'],build['x']]
    draw_y = [build['y'],build['y']-20]

    ax.add_patch(plt.Rectangle((build['x']-30,build['y']-80),60,60,edgecolor = 'black',facecolor = 'none'))    
    plt.plot(draw_x,draw_y,color='blue',linewidth=1,alpha=0.2)
    plt.text(build['x'],build['y']-50,chr(ord('@')+number_id),horizontalalignment='center',verticalalignment='center',fontsize=15,color='blue')
   
 
node_positions = {node[0]: (node[1]['x'], node[1]['y']) for node in g.nodes(data=True)}
label_positions = {node[0]: (node[1]['x']-15, node[1]['y']+10) for node in g.nodes(data=True)}



node_labels = {}
for node in g.nodes(data=True):
    print(node[0])
    node_labels.update({node[0]:node[0]})

#print(node_labels)
#nx.draw(g, pos=node_positions, edge_color='blue',node_size=10, node_color='black',alpha=0.2,ax=ax)
nx.draw_networkx_nodes(g, pos=node_positions,node_size=10,node_color='black',alpha=0.2)
nx.draw_networkx_labels(g,pos=label_positions,labels=node_labels,font_size=8,font_color='black',horizontalalignment='center',verticalalignment='center')
nx.draw_networkx_edges(g, pos=node_positions,edge_color='blue',alpha=0.2)

#p = nx.shortest_path(g,source=building_nodes[0]['id'],target=building_nodes[len(building_nodes)-1]['id'])
p = nx.shortest_path(g,source=source_building, target=destination_building )

shortest_path_list = []
for i in range(len(p)-1):
    shortest_path_list.append([p[i],p[i+1]])


def path_animation(i):
    nx.draw_networkx_edges(g, pos=node_positions,edgelist = shortest_path_list[i:i+1], edge_color= 'r',ax=ax)


'''
bbox = {'ec':[1,1,1,0], 'fc':[1,1,1,0]}
edge_labels = nx.get_edge_attributes(g,'weight')
nx.draw_networkx_edge_labels(g, pos=node_positions, edge_labels=edge_labels, bbox=bbox, font_size=10,ax=ax)
'''

plt.axis('square')
plt.show()
anim = animation.FuncAnimation(plt.gcf(), path_animation, frames=range(len(p)-1), interval=500)



# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 10:32:36 2020

@author: terry
"""


import random
from copy import deepcopy
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib.patches as patches
import matplotlib.animation as animation




node_prob = 0.2
building_prob = 0.2

edgelist = pd.read_csv('edge_standard.csv')
nodelist = pd.read_csv('nodes.csv')

g = nx.Graph()

for i,element in edgelist.iterrows():
    g.add_edge(element[0],element[1], weight=element[2],color= element[3])
    
    
for i,element in nodelist.iterrows():
    g.nodes[element['id']].update(element[1:].to_dict())  
    

fig = plt.figure()
plt.title('Graph Representation', size=15)


# delete some nodes
node_iter = 0
for node in list(g.nodes):    
    if(node == 'n00' or node == 'n99'):
        continue
    else:
        if(node_iter % 4 == 1):
            t = deepcopy(g)
            t.remove_node(node)
            if nx.is_connected(t):            
                g.remove_node(node)
            t.clear()
    
    node_iter = node_iter + 1
    
# add buildings
building_nodes = []
i,building_iter=0,0
for node in list(g.nodes):    
    dic = {}
    if(g.nodes[node]['x'] ==0 or g.nodes[node]['x'] ==900 or  g.nodes[node]['y'] ==0 or  g.nodes[node]['y'] ==900):
        continue
    else:
        if(building_iter%5 ==0 or i == 0): 
            dic['id'] = 'building' + str(i)
            dic['x'] = g.nodes[node]['x'] + 50
            dic['y'] = g.nodes[node]['y']
            building_nodes.append(dic) 
            i = i+1
            
            g.add_node( dic['id'],x= dic['x'],y= dic['y'],height = (g.nodes[node]['y']%13+g.nodes[node]['x']%19) ) 
            g.add_edge(node,dic['id'],weight= (g.nodes[node]['y']+g.nodes[node]['x'])%19,color= 'black')

            adj_node = [x for x,y in g.nodes(data=True) if y['x']==g.nodes[node]['x']+100 and y['y'] ==g.nodes[node]['y']]
            for n in adj_node:
                g.remove_edge(node,n)   
                g.add_edge(n,dic['id'],weight=(g.nodes[node]['y']+g.nodes[node]['x'])%29,color= 'black')
    building_iter = building_iter + 1
   



for build in building_nodes:
#    print(build['id'])
#    g.add_node(build['id'],x= build['x'],y= build['y'] )
    fig.gca().add_patch(patches.Rectangle((build['x']-30,build['y']-80),60,60,edgecolor = 'black',facecolor = 'none'))
#print(building_nodes)    


p = nx.shortest_path(g,source=building_nodes[0]['id'],target=building_nodes[9]['id'])



shortest_path_list = []
for i in range(len(p)-1):
    shortest_path_list.append([p[i],p[i+1]])


def path_animation(i):
    nx.draw_networkx_edges(g, pos=node_positions,edgelist = shortest_path_list[i:i+1], edge_color= 'r')

print(shortest_path_list)    
#print(nx.shortest_path(g, source='n00', target='n44'))     
        
node_positions = {node[0]: (node[1]['x'], node[1]['y']) for node in g.nodes(data=True)}
shortest_node = {}
#print(dict(list(node_positions.items())[0:5]))
#edge_colors = [e[2]['attr_dict']['color'] for e in g.edges(data=True)]  
edge_colors = [e[2]['color'] for e in g.edges(data=True)]  
labels = nx.get_node_attributes(g,'height')

nx.draw(g, pos=node_positions, edge_color=edge_colors,node_size=10, node_color='black')
nx.draw_networkx_labels(g,pos=node_positions,labels=labels,font_size=12,font_color='blue')
#nx.draw(g, labels = labels)
#nx.draw_networkx_edges(g, pos=node_positions,edgelist = shortest_path_list[0:1], edge_color= 'r')

bbox = {'ec':[1,1,1,0], 'fc':[1,1,1,0]}
# hack to label edges over line (rather than breaking up line)
edge_labels = nx.get_edge_attributes(g,'weight')
#print(edge_labels)
nx.draw_networkx_edge_labels(g, pos=node_positions, edge_labels=edge_labels, bbox=bbox, font_size=10)
plt.axis('square')  
plt.show()
anim = animation.FuncAnimation(fig, path_animation, frames=range(len(p)-1), interval=1000)
#anim = animation.FuncAnimation(fig, path_animation, frames=range(len(p)-1), interval=500, blit=True)
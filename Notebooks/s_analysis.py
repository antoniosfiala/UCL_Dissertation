# collection of functions to do analysis in Notebook 210 and Notebook 220.

import matplotlib.pyplot as plt
import networkx as nx

def f_210_short_route(p_path_list,p_graph,p_positions,p_save_path,p_high_colour = "orange",p_back_colour = "black"):
    """This function takes the stated parameters and generates a network graph which it saves in the notebook"""

    # General visual rules
    fig, ax = plt.subplots(figsize = (25,10),dpi = 150)

    plt.ylabel("Count",fontsize = 15)
    plt.xlabel("Degree", fontsize = 15)
    ax.tick_params(axis='y', labelsize= 15)
    plt.axis('off') # no outline for this graph

    # Visualise layers

    path_list = p_path_list
    graph_vis = p_graph
    highlight_colour = p_high_colour
    background_colour = p_back_colour
    positions = p_positions


    # Chosen path
    nx.draw_networkx_nodes(path_list[0], positions, node_size=100,
                           node_color = highlight_colour,alpha = 0.5,dpi=150)
    nx.draw_networkx_edges(graph_vis, positions,edgelist = path_list[1],
                           dpi=150,width = 5,alpha = 0.3, ax=ax, edge_color = highlight_colour)
    # add labels to chosen path
    nx.draw_networkx_labels(graph_vis, pos=positions,labels = {n:n for index,n in enumerate(path_list[0])})

    # Background path
    nx.draw_networkx_nodes(path_list[2], positions, node_size=40,
                           node_color = background_colour,alpha = 0.3,dpi=150)
    nx.draw_networkx_edges(graph_vis, positions,edgelist = path_list[3],
                           dpi=150,width = 1,alpha = 0.3, ax=ax, edge_color = background_colour)

    plt.savefig(p_save_path,dpi = 300,transparent = True,pad_inches = 0,bbox_inches= "tight")
    plt.show()

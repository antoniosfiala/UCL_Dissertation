"""
Package documentation:
A collection of functions that allows one to create adjacency matrices and plot network graphs.
"""

#=== Importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def f_file_test():
    print("Funciton package loaded")

#=== adjacency matrix function
def f_adj_matrix(p_df,p_col,p_index,p_contiguity_flag = 1,p_col_full = None,p_index_full = None):
    """Function returns an adjecency matrix and a list of tuples with the combination of countries
    that are contiguous based on a binary column in the input dataframe.

    Input dataframe should ONLY contain unique combinations as no filtering or checks will be done.

    p_col : define column key (string) that will serve as column list in adjacency matrix
    p_index : define column key (string) that will serve as index/rows list in adjacency matrix

    p_col and p_index can use the same string if required
    """

    #=== Set up variables

    # create working raw dataframe and sort
    f_df = p_df.copy()
    f_df.sort_values(by = [p_col,p_index], inplace = True)

    # unique values for both column keys
    s_rep_col = list(f_df.loc[:,p_col].unique())
    s_rep_ind = list(f_df.loc[:,p_index].unique())

    # sort lists
    s_rep_col.sort()
    s_rep_ind.sort()

    #=== Check in reporting:
    # if columns used for adj matrix are both for both axes
    if p_col == p_index:
        start_report = f"There are {len(p_df.loc[:,p_col].unique())} unique value(s) from one column key ('{p_col}')."
    else:
        # check if their lengths are equal
        if len(s_rep_col) == len(s_rep_ind):
            s_rep_equal = f"equal count ({len(s_rep_col)})"
        else:
            s_rep_equal = f"unequal count (col: {len(s_rep_col)} index: {len(s_rep_ind)})"

        start_report = f"Two different {s_rep_equal} columns are used."

    print(f"Start-up report | {start_report}")

    #=== create zeroed dataframe
    f_df_am = pd.DataFrame(np.zeros(shape = (len(s_rep_ind),len(s_rep_col))),columns = s_rep_col,index = s_rep_ind)

    #=== populate adjacency matrix dataframe and create list of tuples

    # list of tuples to return
    f_list_of_neighbours = []

    # Check if separate tuple values are needed
    if p_col_full is None:
        f_tuple_col = p_col
    else:
        f_tuple_col = p_col_full

    if p_index_full is None:
        f_tuple_ind = p_index
    else:
        f_tuple_ind = p_index_full

    # for loop through every destination
    for destination in s_rep_col:

        # filter based on country code/index/value in column
        f_for_df_filter = f_df[f_df.loc[:,p_col] == destination].copy()

        # (tuple) full name of the country
        f_for_df_full_name = list(f_for_df_filter.loc[:,f_tuple_col].unique())[0]

        # (adj. matrix) only those that are contiguous
        f_for_df_filter = f_for_df_filter[f_for_df_filter.contiguity == p_contiguity_flag].copy()
        # (adj. matrix) list of all neighbouring countries
        f_neighbour_countries = list(f_for_df_filter.loc[:,p_index])
        # (adj. matrix) set values to '1'
        f_df_am.loc[f_neighbour_countries,destination] = 1

        # (tuple) save pairings as a tuple
        f_temp_tuple = (f_for_df_full_name,list(f_for_df_filter.loc[:,f_tuple_ind]))
        f_list_of_neighbours.append(f_temp_tuple)

    # unique list of countries
    f_unique_country_col = list(f_df.loc[:,f_tuple_col].unique())
    f_unique_country_ind = list(f_df.loc[:,f_tuple_ind].unique())
    f_unique_country_list = list(set(f_unique_country_col+f_unique_country_ind))
    f_unique_country_list.sort()

    return_values = [f_df_am,f_list_of_neighbours,f_unique_country_list]

    return return_values

#=== draw graphs
def f_graph(p_tuples,p_df,p_group_of_countries = None,p_colour_group = "yellow", p_colour_default = "blue", p_edge_colour = "red",
            p_seed = None, p_weight = None,p_edge_traits_columns = [None],p_visualise = True, p_fig_size = (40,40),p_dpi = 150,
            p_node_size = 500, p_node_font = 50
            ):

    """This function takes in the list of tuples from f_adj_matrix() (should be at index [1])
    Plus list of countries (full name, i.e. country_o or country_d columns) for colournig, else defaults to blue nodes"""
    import networkx as nx

    #=== Set up network
    f_G = nx.Graph()

    # Add nodes based on full country names
    #f_G.add_nodes_from(p_uniques)

    #=== base for checking nodes and edges
    def f_add_node_and_edge(p_graph,p_central_node,p_node_list,p_edges_chars):
        # list of edges
        temp_edges = []
        # list of neighbours
        p_node_list

        try:
            p_graph.add_node(p_central_node)
        except:
            pass

        for country in p_node_list:
            temp_tuple = (p_central_node,country)
            temp_edges.append(temp_tuple)

            # try tp create edges with distance values, otherwise just pass the edge
            try:
                temp_0 = p_df[(p_df.country_d == temp_tuple[0]) & (p_df.country_o == temp_tuple[1])].loc[:,p_edges_chars[0]].values
                temp_1 = p_df[(p_df.country_d == temp_tuple[0]) & (p_df.country_o == temp_tuple[1])].loc[:,p_edges_chars[1]].values
                temp_2 = p_df[(p_df.country_d == temp_tuple[0]) & (p_df.country_o == temp_tuple[1])].loc[:,p_edges_chars[2]].values
                temp_3 = p_df[(p_df.country_d == temp_tuple[0]) & (p_df.country_o == temp_tuple[1])].loc[:,p_edges_chars[3]].values
                temp_4 = p_df[(p_df.country_d == temp_tuple[0]) & (p_df.country_o == temp_tuple[1])].loc[:,p_edges_chars[4]].values
                p_graph.add_edge(temp_tuple[0], temp_tuple[1], dw =temp_0[0], di = temp_1[0], de = temp_2[0],di_min_max = temp_3[0],de_min_max = temp_4[0])
            except:
                #print("Distance weights were not assigned")
                p_graph.add_edge(temp_tuple[0], temp_tuple[1])

    #=== run function to add values
    for entry in p_tuples:
        f_add_node_and_edge(f_G,entry[0],entry[1],p_edge_traits_columns)

    #=== node colouring | compare list of countries to be treated differently to list of nodes
    colour_list = []

    try:
        for entry in list(f_G.nodes):
            if entry in p_group_of_countries:
                colour_list.append(p_colour_group)
            else:
                colour_list.append(p_colour_default)
    except:
        print("Colouring didn't work, defaulting to {p_col_default}")
        colour_list = p_colour_default

    #=== report
    print("nodes:",f_G.number_of_nodes())
    print("edges:",f_G.number_of_edges())

    #=== visualise graph
    #pos = nx.spring_layout(Test_G, weight='length')
    if p_visualise:
        plt.figure(1,figsize = p_fig_size,dpi = p_dpi)
        nx.draw_spring(f_G, with_labels = True, font_weight = "light",node_color = colour_list,edge_color = p_edge_colour,node_size=p_node_size,font_size=p_node_font, seed = p_seed, weight = p_weight)
        plt.show()
    else:
        print(f"Message: visualisations turned off.")

    return f_G

    #=== save graph file
    #nx.write_gexf(Test_G,"test.gexf")

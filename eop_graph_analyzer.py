import networkx as nx

class GraphAnalyzer:

    def __init__(self, graph, filename, metric_selection="rand") :
        self.graph = graph
        self.filename = filename
        self.metric_selection =  metric_selection

        self.pagerank = nx.pagerank(self.graph, alpha=0.15) #dict node->value
        hits = nx.hits(self.graph)
        self.hubs = hits[0] #dict node->value
        self.authorities = hits[1] #dict node->value
        #list of sets of nodes sorted by the size od sets
        self.strongly_connected_components = sorted(nx.strongly_connected_components(self.graph))
        self.root_components = self.__roots_scc_graph()
        self.selected_nodes = self.__select_nodes(metric_selection)

    # returns pagerank for all nodes
    def getPageRank(self):
        return self.pagerank
    
    # returns pagerank value for specific node
    def getPageRankNode(self, node):
        return self.pagerank[node]

    # returns hubs for all nodes
    def getHubs(self):
        return self.hubs

    # returns hubs value for specific node
    def getHubsNode(self, node):
        return self.hubs[node]

    # returns authorities for all nodes
    def getAuthorities(self):
        return self.authorities

    # returns authorities value for specific node
    def getAuthoritiesNode(self, node):
        return self.authorities[node]
    
    # returns all detected strongly connected components
    def getSCC(self):
        return self.strongly_connected_components
    
    # returns largest detected SCC
    def getLargestSCC(self):
        return self.strongly_connected_components[0]
    
    def __components_connected(self, comp1, comp2):
        for node1 in comp1:
            for node2 in comp2:
                if (node1, node2) in self.graph.edges:
                    return True
        return False

    def getSCCGraph(self):
        comp_graph = nx.DiGraph()
        for i in range(0, len(self.strongly_connected_components)):
            comp_graph.add_node(i)

        for i in range(0, len(self.strongly_connected_components)):
            for j in range(0, len(self.strongly_connected_components)):
                comp1 = self.strongly_connected_components[i]
                comp2 = self.strongly_connected_components[j]
                if i != j and self.__components_connected(comp1, comp2):
                    comp_graph.add_edge(i, j)

        return comp_graph

    def getSCCGraphNX(self):
        return nx.condensation(self.graph, self.strongly_connected_components)

    '''
    def all_scc_indeg_zero(self):
        all_zero = []
        for comp in self.strongly_connected_components:
            zeros = set()
            for node in comp:
                if self.graph.in_degree(node) == 0:
                    zeros.add(node)
            all_zero.append(zeros)
        
        return all_zero
    '''

    def __roots_scc_graph(self):
        #list of all scc-s with indegree 0
        all_zero = []
        sccGraph = self.getSCCGraph()
        for node in sccGraph.nodes:
            if sccGraph.in_degree(node) == 0:
                all_zero.append(node)
        
        return all_zero

    def get_roots(self):
        return self.root_components

    def __select_nodes(self, metric):
        best = []
        if metric == "rand":
            for comp_ind in self.root_components:
                best.append(list(self.strongly_connected_components[comp_ind])[0])
        else:
            for comp_ind in self.root_components:
                values = dict()
                if metric == "pr":
                    for node in self.strongly_connected_components[comp_ind]:
                        values[node] = self.pagerank[node]
                elif metric == "hubs":
                    for node in self.strongly_connected_components[comp_ind]:
                        values[node] = self.hubs[node]  
                elif metric == "auth":
                    for node in self.strongly_connected_components[comp_ind]:
                        values[node] = self.authorities[node]
                else:
                    #indegree
                    for node in self.strongly_connected_components[comp_ind]:
                        values[node] = self.graph.in_degree(node)

                values = dict(sorted(values.items(), key=lambda x:x[1], reverse=True))
                best.append(list(values.keys())[0])

        return best          

    def get_selected_nodes(self):
        return self.selected_nodes

    def scc_report(self):
        roots = self.root_components
        file = open(self.filename + "_scc_report.csv", "w")
        file.write("SCC_ID, is_root, number_of_nodes, nodes\n")
        for i in range(0, len(self.strongly_connected_components)):
            is_root = i in roots
            output = str(i) + ", " + str(is_root) + ", " + str(len(self.strongly_connected_components[i]))
            for node in self.strongly_connected_components[i]:
                output = output + ", " + str(node)
            file.write(output + "\n")
        file.close()

    def nodes_report(self):
        file = open(self.filename + "_nodes_report_" + self.metric_selection + ".csv", "w")
        file.write("ID, is_sensor, SCC_ID, pagerank, authority, hub, indegree\n")
        for node in self.graph.nodes:
            is_sensor = node in self.selected_nodes
            scc_id = None
            for i in range(0, len(self.strongly_connected_components)):
                if node in self.strongly_connected_components[i]:
                    scc_id = i
                    break
            pr = self.pagerank[node]
            auth = self.authorities[node]
            hub = self.hubs[node]
            indeg = self.graph.in_degree(node)

            line = str(node) + ", " + str(is_sensor) + ", " + str(scc_id) + ", " + str(pr) + ", " + str(auth) + ", " + str(hub) + ", " + str(indeg) + "\n"
            file.write(line)
        file.close()

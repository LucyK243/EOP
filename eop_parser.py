import re
import networkx as nx

def parse_line(line):
    param_arr = []

    line_split = line.split("|")
    #zavisna promenljiva
    param_arr.append(line_split[0].strip())

    #nezavisne promenljive u j-ni
    line_split = line_split[1].split(",")
    i = 0
    while i < len(line_split):
        part = line_split[i]
        if "ARR" in part:
            part = part + ", " +line_split[i+1] + ", " +  line_split[i+2]
            i = i + 3
            pattern = re.compile(r"ARR\[(.*?)\]")
            match_found = pattern.search(part).group(1)
            arr_parts = match_found.split(",")
            param = arr_parts[0].strip()
            start = int(arr_parts[1].strip())
            stop = int(arr_parts[2].strip())
            for j in range(start, stop + 1):
                param_arr.append(param + "_" + str(j))
        else:
            param_arr.append(part.strip())
            i = i + 1
    
    return param_arr
            

            

def parse(file_name):
    file = open(file_name)
    ret_graph = nx.DiGraph()
    for line in file:
        param_arr = parse_line(line)

        src = param_arr[0]
        for i in range(1, len(param_arr)):
            dest = param_arr[i]
            ret_graph.add_edge(src, dest)
    
    return ret_graph

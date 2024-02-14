from eop_parser import parse
import eop_graph_analyzer as analyzer
import sys

def print_help():
    print("\nprogram should be called as:")
    print("python main.py filename.extension (criterion)\n")
    print("criterion is optional; it can be:")
    print("rand  -- default; random selection of nodes from root scc")
    print("pr    -- node wiht highest PageRank is selected from root scc")
    print("auth  -- node with highest authority score is selected from root scc")
    print("hub   -- node with highest hub score is selected from root scc")
    print("indeg -- node with highest indegree is selected from root scc")

def main(args):
    
    if len(args) == 1 and args[0] == "-h":
        print_help()
    elif len(args) == 1:
        try:
            graph = parse(args[0])
        except:
            print("file can not be parsed")
    elif len(args) > 2:
        print("arguments fault:")
        print_help()
    else:
        try:
            graph = parse(args[0])
        except:
            print("file can not be parsed")

        filename = args[0].split(".")[0]
        metric = args[1]
        ga = analyzer.GraphAnalyzer(graph, filename, metric)
        ga.scc_report()
        ga.nodes_report()


if __name__ == "__main__":
    main(sys.argv[1:])
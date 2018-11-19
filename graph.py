import os
import glob
import argparse
import hcl
from graphviz import Digraph

PARSER = argparse.ArgumentParser()

PARSER.add_argument("-s", "--source", action="store",
                    dest="source_path", default='.',
                    help="The path to the -live repository clone")

PARSER.add_argument("-r", "--root", action="store",
                    dest="root_path", default='.',
                    help="The path to root node in the -live repository clone")

ARGS = PARSER.parse_args()
ROOT = ARGS.source_path + ARGS.root_path

G = Digraph(name="frontend", format='png', strict='true')
G.node_attr['shape'] = 'rectangle'
G.node_attr['fontsize'] = '8'
G.node_attr['style'] = 'filled'
G.graph_attr['label'] = ROOT[len(ARGS.source_path)+1:]
G.graph_attr['ratio'] = '1.3'
# G.graph_attr['rankdir'] = 'LR'
G.graph_attr['strict'] = 'true'
G.edge_attr['color'] = '#000000'

with G.subgraph(name='cluster_0') as us_west_2:
    us_west_2.attr(style='filled')
    us_west_2.attr(color='lightgrey')
    us_west_2.node_attr.update(style='filled', color='white')
    us_west_2.attr(label='us-west-2')

with G.subgraph(name='cluster_1') as us_east_1:
    us_east_1.attr(style='filled')
    us_east_1.attr(color='lightgrey')
    us_east_1.node_attr.update(style='filled', color='white')
    us_east_1.attr(label='us-east-1')

with G.subgraph(name='cluster_2') as _global:
    _global.attr(style='filled')
    _global.attr(color='lightgrey')
    _global.node_attr.update(style='filled', color='white')
    _global.attr(label='global')

for filename in glob.iglob('{}/**/*.tfvars'.format(ROOT), recursive=True):
    print(filename)
    object_path = filename[len(ROOT)+1:-len("/terraform.tfvars")]
    print(" -> {}".format(object_path))

    with open(filename, 'rt') as in_file:
        g = Digraph(object_path)
        g.graph_attr['label'] = object_path

        item = hcl.load(in_file)
        if 'terraform' in item['terragrunt']:
            print(item['terragrunt']['terraform']['source'])
        else:
            print("No terragrunt configuration in this file")

        if 'dependencies' in item['terragrunt']:
            deps = item['terragrunt']['dependencies']['paths']
            for dep in deps:
                full_path = filename[:-len("/terraform.tfvars")]+'/'+dep
                if os.path.isdir(os.path.abspath(full_path)):
                    g.edge_attr['color'] = '#1100FF'
                else:
                    print(" ** " +os.path.abspath(full_path) + " does not exist")
                    g.edge_attr['color'] = '#FF0000'
                dep_path = os.path.abspath(full_path)[len(ROOT)+1:]
                g.edge(dep_path[dep_path.index('/')+1:], object_path[object_path.index('/')+1:])
        else:
            print("No dependencies defined in this file")

        if object_path.split('/')[0] == "us-west-2":
            us_west_2.subgraph(g)
        elif object_path.split('/')[0] == "us-east-1":
            us_east_1.subgraph(g)
        if object_path.split('/')[0] == "_global":
            _global.subgraph(g)
        else:
            G.subgraph(g)

G.subgraph(us_west_2)
G.subgraph(us_east_1)
G.subgraph(_global)

G.render()

""" This is my docstring."""
import os

import argparse
# import datetime
# import fnmatch
# import hcl
from graphviz import Digraph


PARSER = argparse.ArgumentParser()

PARSER.add_argument("-p", "--path", action="store",
                    dest="code_path", default='~',
                    help="The directory where this code should start generating the graph.")

PARSER.add_argument("-a" "--app", action="store", dest="app_name",
                    help="Which application to generate a graph for.")

PARSER.add_argument("-e" "--env", action="store", dest="app_env",
                    help="Which application environment to generate a graph for.")

PARSER.add_argument("-f", "--file", action="store", dest="output_file", default="output.pdf",
                    help="The name of the pdf file to be generated.")

PARSER.add_argument("-d", "--directory", action="store", dest="output_dir", default="~",
                    help="The name of the directory where the output file should be stored.")

ARGS = PARSER.parse_args()

#filename = args[output_dir] + "/" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M.dot")

# Open the file, write the header

FH = open(ARGS.output_dir + "/" + ARGS.output_file, "w")


for ARGS.app_name in os.listdir(ARGS.code_path):

    if os.path.isdir(ARGS.code_path + "/" + ARGS.app_name):

        G = Digraph(name=ARGS.app_name)
        G.attr(kw='graph', compound='true', strict='true')
        G.node_attr['shape'] = 'rectangle'
        G.node_attr['fixedsize'] = 'true'
        G.node_attr['fontsize'] = '8'
        G.node_attr['style'] = 'filled'
        G.graph_attr['outputorder'] = 'edgesfirst'
        G.graph_attr['label'] = ARGS.app_name
        G.graph_attr['ratio'] = '1.0'
        G.edge_attr['color'] = '#1100FF'
       # G.edge_attr['style']='setlinewidth(2)'

        for env in os.listdir(ARGS.code_path + "/" + ARGS.app_name):
            try:

                if os.path.isdir(ARGS.code_path + "/" + ARGS.app_name + "/" + env)\
                        and env == ARGS.app_env:

                    g = Digraph(name='cluster_' + env)
 #                   g.edge(args.app_env + "-env", args.app_name)

                    for root, dirs, files in os.walk(ARGS.code_path +
                                                     "/" + ARGS.app_name + "/" + env):

                        parent_dir=root.split("/")[-1]

 #                       if len(dirs) > 0:
                        for directory in dirs:
                           # g.node(dir)
                            if env not in (directory, parent_dir):
                                # if directory == '_global', differentiate between global->qa-env
                                # and global -> qa-app

                                if directory == '_global':
                                    if root.split("/")[-1] == env:
                                        # This is the env. layer, not the app layer.
                                        g.edge(parent_dir + "-" + env, directory + "-" + env)
                                else:
                                        g.edge(directory + "-" + env, parent_dir + "-app")



                                #g.edge( root.split("/")[-1] + "-" + env, directory + "-" + env)
                            elif directory == env:

                                if root.split("/")[-2] == env:
                                    # This is the app layer, not the env. layer.
                                    g.edge(directory + "-app", parent_dir + "-" + env)
                                else:
  #wrong
                                    g.edge(parent_dir + "-env", directory + "-" + env)

                            elif parent_dir == env:
                                g.edge(parent_dir + '-env', directory + "-" + env)


                            else:
                                g.edge()

                            g.view('latest', ARGS.code_path)

                                #g.node_attr['comment']= env
                    g.view('latest', ARGS.code_path)

                    G.subgraph(g)
                    G.view('latest', ARGS.code_path)


            except NotADirectoryError as err:
                print("error : {}".format(err))
                continue

#             G.subgraph(g)
# G.view(filename,start_dir)


#             for file in files:
#                 if file.endswith(".tfvars"):
#                     with open(root + "/" + file, 'r') as fh:
#                         obj=hcl.load(fh)
#                         try:
#
#                             mod_version = obj['terragrunt']['terraform']['source'].split("ref=")
#
#                         except Exception as e:
#                             print('No terragrunt/terraform/source in this file {}'.format(e))
#                             continue
#
#                         try:
#                             label = root.split('/')[-1]
#                             g = Digraph(name=label)
#                             g.node(label)
#                             g.node_attr['fillcolor'] = 'lightgrey'
#                             g.node_attr['comment'] = mod_version
#                             G.subgraph(g)
#
#
#                         except Exception as e:
#                             print('Exception {}'.format(e))
#
#
#                         try:
#                             paths=obj['terragrunt']['dependencies']['paths']
#                             referenced=str(paths[-1]).split('../')
#                             source = mod_version[0].split('//')
#                             print("graphing {} : {}".format(source[-1], str(referenced[-1])))
#
#                             G.edge(source[-1], referenced[-1])
#
#                         except Exception as e:
#                             print("edge exception {}".format(e))
#
# G.view('test.dot',start_dir)
#
#
#g.Digraph()
 #       G.subgraph(g)

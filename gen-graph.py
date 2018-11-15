import os
import datetime
import argparse
import fnmatch
from graphviz import Digraph
import hcl

parser = argparse.ArgumentParser()

parser.add_argument("-p", "--path", action="store",
                    dest="code_path", default='~',
                    help="The directory where this code should start generating the graph.")

parser.add_argument("-a" "--app", action="store", dest="app_name",
                    help="Which application to generate a graph for.")

parser.add_argument("-e" "--env", action="store", dest="app_env",
                    help="Which application environment to generate a graph for.")

parser.add_argument("-f", "--file", action="store", dest="output_file", default="output.pdf",
                    help="The name of the pdf file to be generated.")

parser.add_argument("-d", "--directory", action="store", dest="output_dir", default="~",
                    help="The name of the directory where the output file should be stored.")

args = parser.parse_args()

#filename = args[output_dir] + "/" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M.dot")

# Open the file, write the header

f = open(args.output_dir + "/" + args.output_file, "w")


for args.app_name in os.listdir(args.code_path):

    if os.path.isdir(args.code_path + "/" + args.app_name):

        G=Digraph(name=args.app_name)
        G.attr(kw='graph', compound='true', strict='true')
        G.node_attr['shape']='rectangle'
        G.node_attr['fixedsize']='true'
        G.node_attr['fontsize']='8'
        G.node_attr['style']='filled'
        G.graph_attr['outputorder']='edgesfirst'
        G.graph_attr['label']=args.app_name
        G.graph_attr['ratio']='1.0'
        G.edge_attr['color']='#1100FF'
       # G.edge_attr['style']='setlinewidth(2)'

        for env in os.listdir(args.code_path + "/" + args.app_name):
            try:

                if os.path.isdir(args.code_path + "/" + args.app_name + "/" + env)\
                        and env == args.app_env:

                    g = Digraph(name='cluster_' + env)
 #                   g.edge(args.app_env + "-env", args.app_name)

                    for root, dirs, files in os.walk(args.code_path + "/" + args.app_name + "/" + env):

                        if len(dirs) > 0:
                            for dir in dirs:
                               # g.node(dir)
                                if dir != env and root.split("/")[-1] != env:
                                    g.edge(dir + "-" + env, root.split("/")[-1] + "-" + env)
                                elif dir == env:
                                    g.edge(dir + "-app", root.split("/")[-1] + "-" + env)
                                elif root.split("/")[-1] == env:
                                    g.edge(root.split("/")[-1] + "-" + env, dir + "-app")

                                #g.node_attr['comment']= env
                    g.view('latest',args.code_path)

                    G.subgraph(g)
                    G.view('latest',args.code_path)


            except NotADirectoryError as e:
                print("error : {}".format(e))
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



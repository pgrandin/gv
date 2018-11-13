import os
import datetime
import fnmatch
from graphviz import Digraph
import hcl

start_dir="/Users/lkoivu/tmp3/"

path = "/Users/lkoivu/tmp/"
filename = path + "/" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M.dot")

# Open the file, write the header
f = open( filename, "w")

for app in os.listdir(start_dir):

    G=Digraph(name=app)
    G.attr(kw='graph', compound="true")
    G.node_attr['shape']='circle'
    G.node_attr['fixedsize']='true'
    G.node_attr['fontsize']='8'
    G.node_attr['style']='filled'
    G.graph_attr['outputorder']='edgesfirst'
    G.graph_attr['label']=app
    G.graph_attr['ratio']='1.0'
    G.edge_attr['color']='#1100FF'
    G.edge_attr['style']='setlinewidth(2)'

    # if os.path.isdir(start_dir + "/" + app):
    #     add_cluster(app)

#    for dir in os.listdir(start_dir + "/" + app):
    for root, dir, files in os.walk(start_dir + "/" + app):
        for dir in os.listdir(start_dir + "/" + app + "/"):
            g = Digraph(name=dir)

            # if os.path.isdir(root + "/" + dir ):
            #     gg = Digraph(name=dir)
            #     g.subgraph(gg)

            for file in files:
                if file.endswith(".tfvars"):
                    with open(root + "/" + file, 'r') as fh:
                        obj=hcl.load(fh)
                        try:

                            mod_version = obj['terragrunt']['terraform']['source'].split("ref=")
                        except Exception as e:
                            print('No terragrunt/terraform/source in this file {}'.format(e))
                            continue

                        try:
                            label = root.split('/')[-1]
                            G.node(label)
                            G.node_attr['fillcolor'] = 'lightgrey'
                            # n = G.get_node(label)


                        except Exception as e:
                            print('Exception {}'.format(e))


                        try:
                            paths=obj['terragrunt']['dependencies']['paths']
                            referenced=str(paths[-1]).split('../')
                            source = mod_version[0].split('//')
                            print("graphing {} : {}".format(source[-1], str(referenced[-1])))

                            G.edge(source[-1], referenced[-1])

                        except Exception as e:
                            print("edge exception {}".format(e))
        G.subgraph(g)


    # for root, dir, files in os.walk(start_dir + "/" + app):
    #
    #     print('stop')
    #
    #     # g = Digraph (name=dir)
    #     # # g.edge(dir, app)
    #     # # G.subgraph(g)
    #
    #     for items in fnmatch.filter(files, "*.tfvars"):
    #         # print (root)
    #         with open(root + "/" + items, 'r') as file:
    #             obj=hcl.load(file)
    #             try:
    #
    #                 mod_version = obj['terragrunt']['terraform']['source'].split("ref=")
    #             except Exception as e:
    #                 print('No terragrunt/terraform/source in this file {}'.format(e))
    #                 continue
    #
    #             try:
    #                 label = root.split('/')[-1]
    #                 G.node(label)
    #                 G.node_attr['fillcolor'] = 'lightgrey'
    #                 # n = G.get_node(label)
    #
    #
    #             except Exception as e:
    #                 print('Exception {}'.format(e))
    #
    #
    #             try:
    #                 paths=obj['terragrunt']['dependencies']['paths']
    #                 referenced=str(paths[-1]).split('../')
    #                 source = mod_version[0].split('//')
    #                 print("graphing {} : {}".format(source[-1], str(referenced[-1])))
    #
    #                 G.edge(source[-1], referenced[-1])
    #
    #             except Exception as e:
    #                 print("edge exception {}".format(e))

G.view('test.dot',start_dir)

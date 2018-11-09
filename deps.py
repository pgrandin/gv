


import os
import datetime
import fnmatch
from graphviz import Source
import hcl

def clean_text(in_string):
    return in_string.replace('-','_').replace('/','_')


def add_node(label, color, mod_version):
    f.write("\n\n\t")

    # The first label for each node cannot include a dash
    f.write(clean_text(label) + """ [ label=<
        <table border="1" cellborder="0" cellspacing="1">
          <tr><td align="left"><b>""" + label + """</b></td></tr>
          <tr><td align="left">infrastructure-modules</td></tr>
          <tr><td align="left"><font color=""" + "\"" + color + """">""" + mod_version + """</font></td></tr>
        </table>>];""")


def add_edge(from_node, to_node):
    f.write("\n\n")
    f.write("\t" + clean_text(from_node) + " -> " + clean_text(to_node) + ";")


#start_dir="/Users/lkoivu/workspace/Infrastructure-Live/"
start_dir="/Users/lkoivu/tmp3/"

path = "/Users/lkoivu/tmp/"
filename = path + "/" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M.dot")

# Open the file, write the header
f = open( filename, "w")

# Strict keyword enforces only one edge between two nodes. 
f.write("strict digraph D {\n\n")
f.write("""\tnode [shape=plaintext fontname="Sans serif" fontsize="8"];\n""")

for root, dir, files in os.walk(start_dir):

    for items in fnmatch.filter(files, "*.tfvars"):
       # print (root)
        with open(root + "/" + items, 'r') as file:
            obj=hcl.load(file)
            try:
                mod_version = obj['terragrunt']['terraform']['source'].split("ref=")
                label = root.split('/')[-1]
                add_node(label, 'red', str(mod_version[1]))
            except Exception as e:
                print(e)


            try:
                paths=obj['terragrunt']['dependencies']['paths']
                referenced=str(paths[-1]).split('../')
                source = mod_version[0].split('//')
                print("graphing {} : {}".format(source[-1], str(referenced[-1])))
                add_edge(referenced[-1],label)
            except Exception as e:
                print(e)

f.write("}")
f.close()



# dir_len = len(start_dir)
# #dir = os.getcwd()
#
# graph = Digraph(comment = 'first try')
#
# for root, dir, files in os.walk(start_dir):
#
#     for items in fnmatch.filter(files, "*.tfvars"):
#        # print (root)
#         with open(root + "/" + items, 'r') as f:
#             obj=hcl.load(f)
# #        with open(root + "/" + items, 'r') as f:
#             hierarchy = root[dir_len-1:].split('/')
#             for i in (1, len(hierarchy)-2):
#                 graph.edge(hierarchy[i], hierarchy[i+1])
#             print(hierarchy[0])
#             # This will error out if this file does not have a source def.
#             try:
#                 source=obj['terragrunt']['terraform']['source']
#             except:
#                 continue
#
#             # This will error out if this file does not have a dependencies def.
#             try:
#                 paths=obj['terragrunt']['dependencies']['paths']
#                 print("graphing {} : {}".format(source, paths[0]))
#                 graph.edge(source,paths[0])
#             except:
#                 continue
#
# graph.render('test.gv', view=True)
#     #graph.view()

# digraph = Digraph(comment='first')
#
# digraph.node('node1', 'label1')
# digraph.node('node2', 'label2')
# digraph.node('node3', 'label3')
# digraph.edge('node1', 'node2', )
# digraph.edge('node1', 'node3', )
#
#
# digraph.render('round-table.gv', view=True)
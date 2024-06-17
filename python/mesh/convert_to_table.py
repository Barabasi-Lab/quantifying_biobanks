import pandas as pd
# import libraries to read xml file
import xml.etree.ElementTree as ET


FILE = '../../data/mesh_and_meta/desc2023.xml'
# read xml file as a dictionary
tree = ET.parse(FILE)
# convert xml to dictionary
root = tree.getroot()
# parse all DescriptorUI and DescriptorName from dict_mesh
# add them to a list
mesh = []
for child in root:
    des_id = child.find('DescriptorUI').text
    des_name = child.find('DescriptorName').find('String').text
    tree_list = child.find('TreeNumberList')
    if tree_list is None:
        continue
    tree_numbers = tree_list.findall('TreeNumber')
    for tree_number in tree_numbers:
        mesh.append([des_id, des_name, tree_number.text])

        

# create dataframe with columns "mesh_id" and "mesh_name"
df_mesh = pd.DataFrame(mesh, columns=['mesh_id', 'mesh_name', 'tree_number'])

df_mesh.to_csv('../../data/database/meta/mesh.csv', index=False)
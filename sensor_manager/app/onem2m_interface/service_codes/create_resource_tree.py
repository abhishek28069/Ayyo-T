from oneM2M_functions import *

server = "http://127.0.0.1:5089"
cse = "/~/in-cse/in-name/"


# ------------------------------------------
# Fill code here to create AE
# specified by the URI
# ------------------------------------------
ae = "IIITH"
lbl_ae = ["Sensor Management", "Sensors in IIIT-Hyderabad"]
create_ae(server+cse, ae, lbl_ae)
# ------------------------------------------


# ------------------------------------------
# Fill code here to create container in the AE
# specified by the URI
# ------------------------------------------

# node_container_name = "Node-1"
# lbl_cnt = ["CNT-Label-1", "CNT-Label-2"]
# create_cnt(server+cse+ae, node_container_name, lbl_cnt)

# descriptor_container_name = "Descriptor"
# lbl_cnt = ["CNT-Label-1", "CNT-Label-2"]
# create_cnt(server+cse+ae + "/" + node_container_name, descriptor_container_name, lbl_cnt)

# data_container_name = "Data"
# lbl_cnt = ["CNT-Label-1", "CNT-Label-2"]
# create_cnt(server+cse+ae + "/" + node_container_name, data_container_name, lbl_cnt)
# ------------------------------------------


# ------------------------------------------
# Fill code here to create content_instance
# specified by the URI
# ------------------------------------------

# content_instance = "[Timestamp, Occupancy-State, Distance]"
# lbl_cin = ["CIN-Label-1", "CIN-Label-2"]
# create_data_cin(server+cse+ae + "/" + node_container_name +"/"+ descriptor_container_name, content_instance, lbl_cin)

# content_instance = 0
# lbl_cin = ["CIN-Label-1", "CIN-Label-2"]
# create_data_cin(server+cse+ae + "/" + node_container_name +"/"+ data_container_name, content_instance, lbl_cin)


# ------------------------------------------


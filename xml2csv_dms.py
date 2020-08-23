import xml.etree.ElementTree as ET
import os
import pandas as pd
import numpy as np
from datetime import date, timedelta
import datetime as dt
from xml.sax.saxutils import escape

input_path='/Users/aravind/Downloads/InTrans/Apr-16-2020/dms'
folder= [ fol for fol in os.listdir(input_path) if not fol.startswith('.')]
k=0
while (k<len(folder)):
    output_path='/Users/aravind/Desktop'
    data_files = [f for f in os.listdir(input_path+'/'+folder[k]) if 'dms' in f]
    output_csv_file =output_path+'/'+folder[k]+'/unprocessed.csv'
    if not os.path.exists(os.path.dirname(output_csv_file)):
        os.makedirs(os.path.dirname(output_csv_file))
    lines_to_print = []
    name_space_tag = ""
    result=[]
    headers= ["Heading","Device_Id","Device_Name","Comm_Mode","Device_Mode","Time_Received","Current_Message","Multi_Tag_Message","Message_Priority"]
    result.append(",".join(headers))
    i=0
    while i<len(data_files):
        #tree = ET.parse(path+'/'+data_files[i])
        f=open(input_path+'/'+folder[k]+'/'+data_files[i],"r")
        contents=f.read()
        contents=contents.replace("&","and")
        f1=open("test.txt","w")
        f1.write(contents)
        f1.close()
        tree = ET.parse("test.txt")
        root = tree.getroot()
        root_tags = root.tag.split('}')

        #name_space_tag = ""
        #root_tags = root.tag.split('}')
        if len(root_tags) > 1:
           name_space_tag = root_tags[0] + '}'
        heading = root.find(name_space_tag+'Heading').text
        heading=heading.replace(","," ")
        collection_periods_list = root.findall(name_space_tag + 'DMS_DETAIL')
        for collection_period in collection_periods_list:
            res=[]
            Device_Id = collection_period.find(name_space_tag + 'Device_Id').text
            res.append(Device_Id)
            Device_Name = collection_period.find(name_space_tag + 'Device_Name').text
            res.append(Device_Name)
            Comm_Mode = collection_period.find(name_space_tag + 'Comm_Mode').text
            res.append(Comm_Mode)
            Device_Mode = collection_period.find(name_space_tag + 'Device_Mode').text
            res.append(Device_Mode)
            Time_Received = collection_period.find(name_space_tag + 'Time_Received').text
            res.append(Time_Received)
            Current_Message = collection_period.find(name_space_tag + 'Current_Message').text
            if Current_Message is None:
                Current_Message=""
                res.append(0)
            else:
                res.append(Current_Message)
            Multi_Tag_Message = collection_period.find(name_space_tag + 'Multi_Tag_Message').text
            if Multi_Tag_Message is None:
                Multi_Tag_Message=""
                res.append(0)
            else:
                res.append(Multi_Tag_Message)
            Message_Priority = collection_period.find(name_space_tag + 'Message_Priority').text
            res.append(Message_Priority)
            lines =[heading,Device_Id,Device_Name,Comm_Mode,Device_Mode,Time_Received,Current_Message,Multi_Tag_Message,Message_Priority]
            result.append(",".join(lines))
        i=i+1

    os.remove("test.txt")

    with open(output_csv_file, 'w') as filehandle:
        for detectorData in result:
            filehandle.write('%s\n' % detectorData)
    k=k+1


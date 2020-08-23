import xml.etree.ElementTree as ET
import os
import pandas as pd
import numpy as np
from datetime import date, timedelta
import datetime as dt
from xml.sax.saxutils import escape

input_path='/Users/aravind/Downloads/InTrans/Apr-16-2020/incidents'
folder= [ fol for fol in os.listdir(input_path) if not fol.startswith('.')]
k=0
while (k<len(folder)):
    output_path='/Users/aravind/Desktop'
    data_files = [f for f in os.listdir(input_path+'/'+folder[k]) if 'incident' in f]
    output_csv_file =output_path+'/'+folder[k]+'/unprocessed.csv'
    if not os.path.exists(os.path.dirname(output_csv_file)):
        os.makedirs(os.path.dirname(output_csv_file))
    lines_to_print = []
    name_space_tag = ""
    result=[]
    headers= ["Heading","ID","External_ID","State","Link_ID","Associated_Link","Start_Time","Type","Related_Links","Comment","Modified_By","Last_Modified","Est_Duration_min","Longitude","Latitude","Coordinate_Type","Confirmation_Timeout","Lanes_Blocked","Source","Control_Station"]
    result.append(",".join(headers))
    #headers = ["heading", "device_id", "device_name", "comm_mode", "device_mode", "time_received", "current_message", "multi_tag_message", "message_priority"]
    i=0
    while i<len(data_files):
        try:
            tree = ET.parse(input_path+'/'+folder[k]+'/'+data_files[i])
            root = tree.getroot()
            root_tags = root.tag.split('}')

            #name_space_tag = ""
            #root_tags = root.tag.split('}')
            if len(root_tags) > 1:
               name_space_tag = root_tags[0] + '}'
            heading = root.find(name_space_tag+'Heading').text
            heading=heading.replace(","," ")
            collection_periods_list = root.findall(name_space_tag + 'INCHISTRPT')
            for collection_period in collection_periods_list:
                res=[]
                id = collection_period.find(name_space_tag + 'ID').text
                res.append(id)
                External_ID = collection_period.find(name_space_tag + 'External_ID')
                if External_ID.text is None:
                    External_ID=""
                    res.append(0)
                else:
                    External_ID=External_ID.text
                    res.append(External_ID)
                State = collection_period.find(name_space_tag + 'State').text
                res.append(State)
                Link_ID = collection_period.find(name_space_tag + 'Link_ID').text
                res.append(Link_ID)
                Associated_Link = collection_period.find(name_space_tag + 'Associated_Link').text
                res.append(Associated_Link)
                Start_Time = collection_period.find(name_space_tag + 'Start_Time').text
                res.append(Start_Time)
                Type = collection_period.find(name_space_tag + 'Type').text
                res.append(Type)
                Related_Links = collection_period.find(name_space_tag + 'Related_Links')
                if Related_Links.text is None:
                    Related_Links=""
                    res.append(0)
                else:
                    Related_Links=Related_Links.text
                    res.append(Related_Links)
                Comment = collection_period.find(name_space_tag + 'Comment').text
                res.append(Comment)
                Modified_By = collection_period.find(name_space_tag + 'Modified_By').text
                res.append(Modified_By)
                Est_Duration_min = collection_period.find(name_space_tag + 'Est_Duration_min').text
                res.append(Est_Duration_min)
                Longitude = collection_period.find(name_space_tag + 'Longitude').text
                res.append(Longitude)
                Latitude = collection_period.find(name_space_tag + 'Latitude').text
                res.append(Latitude)
                Coordinate_Type = collection_period.find(name_space_tag + 'Coordinate_Type')
                if Coordinate_Type.text is None:
                    Coordinate_Type=""
                    res.append(Coordinate_Type)
                else:
                    Coordinate_Type=Coordinate_Type.text
                    res.append(Coordinate_Type)
                Confirmation_Timeout = collection_period.find(name_space_tag + 'Confirmation_Timeout').text
                Lanes_Blocked = collection_period.find(name_space_tag + 'Lanes_Blocked')
                if Lanes_Blocked.text is None:
                    Lanes_Blocked=""
                else:
                    Lanes_Blocked=Lanes_Blocked.text
                Source = collection_period.find(name_space_tag + 'Source').text
                Control_Station = collection_period.find(name_space_tag + 'Control_Station').text
                lines =[heading,id,External_ID,State,Link_ID,Associated_Link,Start_Time,Type,Related_Links,Comment,Modified_By,Est_Duration_min,Longitude,Latitude,Coordinate_Type,Confirmation_Timeout,Lanes_Blocked,Source,Control_Station]
                result.append(",".join(lines))
        except:
            pass
        i=i+1

    with open(output_csv_file, 'w') as filehandle:
        for detectorData in result:
            filehandle.write('%s\n' % detectorData)
    k=k+1

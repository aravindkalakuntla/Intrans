import xml.etree.ElementTree as ET
import os

input_path='/Users/aravind/Downloads/InTrans/inrix'
folder= [ fol for fol in os.listdir(input_path) if not fol.startswith('.')]
k=0
while (k<len(folder)):
    output_path='/Users/aravind/Desktop'
    data_files = [f for f in os.listdir(input_path+'/'+folder[k]) if 'inrix' in f]
    output_csv_file =output_path+'/'+folder[k]+'/unprocessed.csv'
    if not os.path.exists(os.path.dirname(output_csv_file)):
        os.makedirs(os.path.dirname(output_csv_file))
    result=[]
    headers=["Code","c-value","SegmentClosed","Score","Speed","Average","Reference","TraveltimeinMinutes","Time"]
    result.append(",".join(headers))
    i=0
    while i<len(data_files):
        res=[]
        tree = ET.parse(input_path+'/'+folder[k]+'/'+data_files[i])
        i=i+1
        root = tree.getroot()
        root_tags = root.tag.split('}')
        for child in root:
            for a in child:
                time=a.attrib['timestamp']
                for b in a:
                    x=b.attrib
                    code=(x['code'])
                    if 'c-value' in x:
                        cvalue=x['c-value']
                    else:
                        cvalue=""
                    if 'segmentClosed' in x:
                        segmentclosed=x['segmentClosed']
                    else:
                        segmentclosed=""
                    if 'score' in x:
                        score=x['score']
                    else:
                        score=""
                    if 'speed' in x:
                        speed=x['speed']
                    else:
                        speed=""
                    if 'average' in x:
                        average=x['average']
                    else:
                        average=""
                    if 'reference' in x:
                        reference=x['reference']
                    else:
                        reference=""
                    if 'travelTimeMinutes' in x:
                        traveltime=x['travelTimeMinutes']
                    else:
                        traveltime=""
                    lines=[code,cvalue,segmentclosed,score,speed,average,reference,traveltime,time]
                    result.append(",".join(lines))

    with open(output_csv_file, 'w') as filehandle:
        for detectorData in result:
            filehandle.write('%s\n' % detectorData)

    k=k+1

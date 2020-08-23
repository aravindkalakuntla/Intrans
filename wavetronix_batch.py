import xml.etree.ElementTree as ET
import os
from datetime import date, timedelta
import datetime as dt

#specification of the path of the input data.here it is indicated as current folder since the process runs inside the raw file folder
input_path='/Users/aravind/Downloads/InTrans/wavetronix'
folder= [ fol for fol in os.listdir(input_path) if not fol.startswith('.')]
k=0

while (k<len(folder)):
    output_path='/Users/aravind/Desktop'
    data_files = [f for f in os.listdir(input_path+'/'+folder[k])]
    output_csv_file =output_path+'/'+folder[k]+'/unprocessed.csv'
    if not os.path.exists(os.path.dirname(output_csv_file)):
        os.makedirs(os.path.dirname(output_csv_file))
    result=[]
    headers = ["owner-id", "network-id", "local-date", "local-time", "utc-offset", "start-time", "end-time","detector-id", "status", "lane-id","lane-count","lane-volume", "lane-occupancy","lane-speed","small-class-count","small-class-volume", "medium-class-count", "medium-class-volume", "large-class-count", "large-class-volume"]
    result.append(",".join(headers))
    i=0
    while i<len(data_files):
        if data_files[i].endswith('.xml'):
            try:
                tree = ET.parse(input_path+'/'+folder[k]+'/'+data_files[i])
                root = tree.getroot()
                name_space_tag = ""
                root_tags = root.tag.split('}')
                if len(root_tags) > 1:
                    name_space_tag = root_tags[0] + '}'
                
                owner_id = root.find(name_space_tag + 'owner-id').text
                network_id = root.find(name_space_tag + 'network-id').text
                collection_periods_list = root.find(name_space_tag + 'collection-periods')
                
                #fetch all elements within the tag collection-period.The tag detection time-stamp has children utc-offset,local-time,local-date,start-time,end-time,detector-reports read and stored into separate variables
                for collection_period in collection_periods_list.findall(name_space_tag + 'collection-period'):
                    detection_time_stamp = collection_period.find(name_space_tag + 'detection-time-stamp')
                    utc_offset = detection_time_stamp.find(name_space_tag + 'utc-offset').text
                    local_time = detection_time_stamp.find(name_space_tag + 'local-time').text
                    local_date = detection_time_stamp.find(name_space_tag + 'local-date').text
                    start_time = collection_period.find(name_space_tag + 'start-time').text
                    end_time = collection_period.find(name_space_tag + 'end-time').text
                    detector_reports = collection_period.find(name_space_tag + 'detector-reports')
                    for detector_report in detector_reports:
                        detector_id = detector_report.find(name_space_tag + 'detector-id').text
                        detector_status = detector_report.find(name_space_tag + 'status')
                        
                        #where ever the detector_status may be None a null value is to be inserted and where there exits a value that value is read.The same applies to other variables as well
                        if detector_status is None:
                            detector_status=""
                        else:
                            detector_status=detector_status.text
                        all_lanes=detector_report.find(name_space_tag + 'lanes')
                        if all_lanes is None:
                            continue
                        for lane in all_lanes.findall(name_space_tag + 'lane'):
                            speed = lane.find(name_space_tag + 'speed')
                            if speed is None:
                                speed = ""
                            else:
                                speed = speed.text
                            lane_id = lane.find(name_space_tag + 'lane-id')
                            if lane_id is None:
                                lane_id = ""
                            else:
                                lane_id = lane_id.text
                            lane_count = lane.find(name_space_tag + 'count')
                            if lane_count is None:
                                lane_count = ""
                            else:
                                lane_count = lane_count.text
                            lane_occupancy = lane.find(name_space_tag + 'occupancy')
                            if lane_occupancy is None:
                                lane_occupancy = ""
                            else:
                                lane_occupancy = lane_occupancy.text
                            lane_volume = lane.find(name_space_tag + 'volume')
                            if lane_volume is None:
                                lane_volume = ""
                            else:
                                lane_volume = lane_volume.text
                            all_classes = lane.find(name_space_tag + 'classes')
                            class_types_count_volume = []
                            if all_classes is None:
                                continue
                            else:
                                for class_type in all_classes.findall(name_space_tag + 'class'):
                                    class_count = class_type.find(name_space_tag + 'count')
                                    if class_count is None:
                                        class_types_count_volume.append("")
                                    else:
                                        class_types_count_volume.append(class_count.text)
                                    class_volume = class_type.find(name_space_tag + 'volume')
                                    if class_volume is None:
                                        class_types_count_volume.append("")
                                    else:
                                        class_types_count_volume.append(class_volume.text)
                            #All the values read into the variables are brought together as a list
                            lines = [owner_id, network_id, local_date, local_time, utc_offset, start_time, end_time, detector_id, detector_status,
                                                 lane_id,lane_count,lane_volume,lane_occupancy,speed,",".join(class_types_count_volume)]
                            # The list of values need to appended as a line of csv
                            result.append(",".join(lines))
            except:
                pass

        i=i+1

#The output file is opened and the list of values are written into it
    with open(output_csv_file, 'w') as filehandle:
        for detectorData in result:
            filehandle.write('%s\n' % detectorData)
        
    k=k+1

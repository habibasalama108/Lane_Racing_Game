import os
import json


folder_files = os.listdir("raw_images")

for file_name in folder_files:
    if file_name.endswith(".jpg"):
        
        name_only = file_name.split(".")[0]
        
        json_path = "raw_images/" + name_only + ".json"
        txt_path = "raw_labels/" + name_only + ".txt"
        
        if os.path.exists(json_path) == True:
            f = open(json_path, "r")
            data_string = f.read()
            data = json.loads(data_string)
            f.close()
            
            img_width = data["imageWidth"]
            img_height = data["imageHeight"]
            
            out_file = open(txt_path, "w")
            
            for shape in data["shapes"]:
                label_name = shape["label"]
                
                if label_name == "steer":
                    class_id = "0"
                elif label_name == "kachow":
                    class_id = "1"
                else:
                    continue
                    
                x1 = shape["points"][0][0]
                y1 = shape["points"][0][1]
                x2 = shape["points"][1][0]
                y2 = shape["points"][1][1]
                
                center_x = ((x1 + x2) / 2) / img_width
                center_y = ((y1 + y2) / 2) / img_height
                box_width = abs(x2 - x1) / img_width
                box_height = abs(y2 - y1) / img_height
        
                line = class_id + " " + str(center_x) + " " + str(center_y) + " " + str(box_width) + " " + str(box_height) + "\n"
                out_file.write(line)
                
            out_file.close()
            
        else:
            empty_file = open(txt_path, "w")
            empty_file.close()

print("Conversion done.")
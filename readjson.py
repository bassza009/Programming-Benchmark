import json
import csv
import os

def json_to_csv(json_filename,csv_filename):
    if not os.path.exists(json_filename):
        print(f"Error : file {json_filename} not found")
        return
    with open(json_filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    results =data.get("result",[])

    file_exist = os.path.isfile(csv_filename)

    with open(csv_filename, "a", newline= "",encoding="utf-8") as f :
        writer = csv.writer(f)

        if not file_exist :
            writer.writerow(["Command","Mean","StdDev","Min","Max","User_tag"])
            
            for res in results:
                command = res.get("command")
                mean = res.get("mean")
                stddev = res.get("stddev")
                min = res.get("min")
                max = res.get("max")

                tag = json_filename.replace(".json","")

                writer.writerow([command,mean,stddev,min,max,tag])
    print(f"convert {json_filename} to {csv_filename} success!!")

json_to_csv(results.json,results.csv)

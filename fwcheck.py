# load fwdb.json
# load list of *.bin files
# parse input command

# fwcheck.py usage:
# ○ fwcheck.py -c <fwfile.bin>
# ○ fwcheck.py -u <fwfile.bin>
# ○ fwcheck.py -ru <filter or file name> (qualifies each unlinked firmware file before removing)
# ○ fwcheck.py -l (can grep this list to filter on things)
# ○ fwcheck.py -lu (can grep this list to filter on things)

# Other notes
# Check FW binary size before checking in for that product. Right now can make this fixed in the script. Eventually it should be referencecd to data base. 
# Check for conflict in update revision+PID

##################
# Checkinlink
##################
# look for filename.bin in unlinkedfw folder
# build filename for json. filename_uniqueid (increased number)
# check for filename.info in unlinkedfw folder and pull-in params which are listed and needed
# check for missing or conflicting params and prompt user for those inputs
# once all check out, move file.bin to fw folder and add json entry. Save json. 
# if -ri is added then remove file.info (can do this later)

# {
#     "filenamehere": {
#         "PRODUCT": {
#             "hwid": 10001,
#             "hwversion_compatibility": [[0.01,0.01],[0.03,0.03]]
#         },
#         "FIRMWARE": {
#             "fwrelease_name":"developer release",
#             "fwrelease_level":0,
#             "fwdev_branch":"master",
#             "fwversion": 0.01
#         },
#         "RELEASE_DATE": "2022.05.23.01.59.01",
#         "META_DATA": {
#             "fwdescription": "some purpose for release",
#             "fwfeatures_updated": ["ota","something else"],
#             "fwsize": 102400230
#         }
#     }
# }

import argparse
from ast import Break
import os
import numpy as np
import json
from datetime import datetime

from numpy import array
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
relpath_fw = "fw"
abspath_fw = os.path.join(script_dir, relpath_fw)
# Instantiate the parser
parser = argparse.ArgumentParser(description='Optional app description')
# Required positional argument
parser.add_argument('-c', type=str, nargs=1, metavar="<filename>", dest='checkinfilename', default="not set",
                    help='Use to check-in a link to firmware binary file')
# Optional positional argument
parser.add_argument('-u', type=str, nargs=1, metavar="<filename>", dest='unlinkfilename', default="not set",
                    help='Unlink binary file')
# Optional argument
parser.add_argument('-ru', action='store_true',
                    help='remove unlinked binary files')
# Optional argument
parser.add_argument('-lu', action='store_true',
                    help='list unlinked binary files')

class parsefw():
    def __init__(self) -> None:
        self.args = parser.parse_args()
        self.hwid = "not set"
        self.hwversion_compatibility = "not set"
        self.fwrelease_name = "not set"
        self.fwrelease_level = "not set"
        self.fwdev_branch = "not set"
        self.fwversion = "not set"
        self.fwdescription = "not set"
        self.fwfeatures_updated = "not set"
        self.RELEASE_DATE = 0
        self.fwsize = 0
        self.paramdict = {"hwid":self.hwid,
        "hwversion_compatibility":self.hwversion_compatibility,
        "fwrelease_name":self.fwrelease_name,
        "fwrelease_level":self.fwrelease_name,
        "fwdev_branch":self.fwdev_branch,
        "fwversion":self.fwversion,
        "fwdescription":self.fwdescription,
        "fwfeatures_updated":self.fwfeatures_updated}

    def listargs(self):
        for arg in vars(self.args):
            print (arg, getattr(self.args, arg))


    def info(self,dirname, filename):
        f = open("{}\\{}.info".format(dirname,filename), 'r')
        Lines = f.readlines()
        count = 0
        # Strips the newline character
        for line in Lines:
            for key,value in self.paramdict.items():
                if ":" in line:
                    linekey = line.strip().split(':',1)[0]
                    lineval = line.strip().split(':',1)[1]
                if key in linekey:
                    self.parse_keyval(key, lineval)
        f.close()

    def parse_keyval(self, key, string):
        if key == "hwid":  
            value = int(string.strip().replace(" ",""))
            self.paramdict[key] = value
        elif key == "hwversion_compatibility":
            value = json.loads(string.strip().replace(" ",""))
            self.paramdict[key] = value
        elif key == "fwrelease_name":
            value = (string.strip().replace(" ",""))
            self.paramdict[key] = value
        elif key == "fwrelease_level":
            value = int(string.strip().replace(" ",""))
            self.paramdict[key] = value
        elif key == "fwdev_branch":
            value = (string.strip().replace(" ",""))
            self.paramdict[key] = value
        elif key == "fwversion":
            value = float(string.strip().replace(" ",""))
            self.paramdict[key] = value
        elif key == "fwdescription":
            value = (string.strip())
            self.paramdict[key] = value
        elif key == "fwfeatures_updated":
            value = json.loads(string.strip())
            self.paramdict[key] = value   

    def validate_info(self):
        for key,value in self.paramdict.items():
            if value == "not set":
                value = input("Enter value for {}:  ".format(key))
                self.parse_keyval(key, value)
            else:
                print("{} = {}".format(key,value))

    def validate_unique_version(self,jsondict):
        for fwkey in jsondict.keys():
            match = 0
            if float(jsondict[fwkey]["PRODUCT"]["hwid"]) == float(self.paramdict["hwid"]):
                match +=1
            if float(jsondict[fwkey]["FIRMWARE"]["fwversion"]) == float(self.paramdict["fwversion"]):
                match +=1
            if match >= 2:
                return False
        return True

    def generate_unique_nameid(self,jsondict,filename):
        maxindex = 0
        for fwkey in jsondict.keys():
            fwidname = fwkey.split('___',1)[0]
            fwidnumber = int(fwkey.split('___',1)[1], 16)
            if fwidname == filename:
                maxindex = max(maxindex,fwidnumber+1)
        self.fwkey = "{}___{}".format(filename,hex(maxindex))
        return maxindex

class parsejson():
    def __init__(self) -> None:
        self.jsondict = "not set"

    def loadjsonfile(self, filepath):
        path = os.path.join(filepath,"fwdb.json")
        f = open(path)
        # returns JSON object as a dictionary
        self.jsondict = json.load(f)
        f.close()

    def addtojsondict(self,fwkey, paramdict, size):
        # this needs to
        tempdict = {}
        tempdict["PRODUCT"] = {}
        tempdict["FIRMWARE"] = {}
        tempdict["META_DATA"] = {}
        tempdict["RELEASE_DATE"] = {}
        
        tempdict["PRODUCT"]["hwid"] = paramdict["hwid"]
        tempdict["PRODUCT"]["hwversion_compatibility"] = paramdict["hwversion_compatibility"]

        tempdict["FIRMWARE"]["fwrelease_name"] = paramdict["fwrelease_name"]
        tempdict["FIRMWARE"]["fwrelease_level"] = paramdict["fwrelease_level"]
        tempdict["FIRMWARE"]["fwdev_branch"] = paramdict["fwdev_branch"]
        tempdict["FIRMWARE"]["fwversion"] = paramdict["fwversion"]
        
        tempdict["META_DATA"]["fwdescription"] = paramdict["fwdescription"]
        tempdict["META_DATA"]["fwfeatures_updated"] = paramdict["fwfeatures_updated"]
        
        tempdict["META_DATA"]["fwsize"] = size
        now = datetime.now()
        tempdict["RELEASE_DATE"] = now.strftime('%Y.%m.%d.%H.%M.%S')
        self.jsondict[fwkey] = tempdict


    def exportjson(self, abspath_fwbinfile, fwkey):
        json_object = json.dumps(self.jsondict, indent = 4)
        # make copy of fwdb.json to .old_fwdb_json blowing away others
        unlinked_filename = os.path.basename(abspath_fwbinfile)
        os.rename(abspath_fwbinfile,"{}\\fw\\{}.bin".format(script_dir,fwkey))
        os.popen("copy {}\\fwdb.json {}\\.old_fwdb_json".format(script_dir,script_dir)) 

        with open("{}\\fwdb.json".format(script_dir), "w") as outfile:
            json.dump(self.jsondict, outfile, indent=4)



PARSEFW = parsefw()
PJSON = parsejson()

if PARSEFW.args.checkinfilename != "not set":
    filepath = os.path.join(script_dir,PARSEFW.args.checkinfilename[0])
    unlinked_filenameext = os.path.basename(filepath)
    unlinked_dirname = os.path.dirname(filepath)
    unlinked_filename = str(unlinked_filenameext).split('.',1)[0]
    print("\nUpdating firmware database with {}.bin".format(unlinked_filename))

    size = os.path.getsize("{}\\{}.bin".format(unlinked_dirname,unlinked_filename))
    # parse info file for firmware data
    PARSEFW.info(unlinked_dirname, unlinked_filename)
    # collect info from user for missing data
    PARSEFW.validate_info()
    # import json file. check for unique hwid+fwversion
    PJSON.loadjsonfile(script_dir)
    # if all looks good assign unique filename id, add to json list and them move binary file to destination folder
    if PARSEFW.validate_unique_version(PJSON.jsondict) == False:
        print("\nYou have chosen poorly! Firmware version conflict. Exiting...")
    else:
        PARSEFW.generate_unique_nameid(PJSON.jsondict, unlinked_filename)
        PJSON.addtojsondict(PARSEFW.fwkey,PARSEFW.paramdict,size)
        # print(PJSON.jsondict)
        # move binary file to folder
        path = os.path.join(unlinked_dirname,unlinked_filenameext)
        PJSON.exportjson(path, PARSEFW.fwkey)
        print("\nDONE...")

# load fwdb.json
# load list of *.bin files
# parse input command

# fwcheck.py usage:
# ○ fwcheck.py --checkinlink| -c <fwfile.bin>
# ○ fwcheck.py --unlink | -u <fwfile.bin>
# ○ fwcheck.py --removeunlinked | -ru <filter or file name> (qualifies each unlinked firmware file before removing)
# ○ fwcheck.py --list | -l (can grep this list to filter on things)
# ○ fwcheck.py --listunlinked | -lu (can grep this list to filter on things)

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
#             "hwversion": 0.01
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

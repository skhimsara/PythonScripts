#!/usr/bin/python
import os, csv, hashlib, filecmp, argparse
import shutil
import photohash
from PIL import Image
from PIL.ExifTags import TAGS
import time

csv_cols = ["Type" ,"Name","Path","Exif DateTime", "File DateTime", "File Size", "Result", "Remarks", "DupFile File DateTime", "DupFile Exif DateTime","File Date Different", "Hash"]
cwd = os.getcwd()

def is_exif_and_file_datetime_same(exifdatetime, filedatetime):
    tmp = filedatetime.split()
    filedate = tmp[0].split(':')
    filetime = tmp[1].split(':')

def get_filesize(filename):
   return os.path.getsize(filename)/(1024*1024.0)

def get_file_datetime(filename):
    return time.strftime("%Y:%m:%d %I:%M:%S %p",time.localtime(os.path.getmtime(filename)))

def get_field (exif,field) :
  for (k,v) in exif.iteritems():
    if TAGS.get(k) == field:
        return v

def get_exif_datetime(filename):
    return ""
    if((os.path.splitext(file_basename)[1]).lower() == ".jpg" ): 
        exif = Image.open(filename)._getexif()
        return get_field(exif,'DateTime')
    else:
        return "" 

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_or_folder_path", type=str, help="Input file name (csv) or folder path")   
    parser.add_argument("file_type", type=str, help="Input file extension (jpg mp4 etc). Use 'all' for including all files ")   

    # parser.add_argument("-read_codec_from_csv","--read_codec_id_from_csv",action="store", type=str, choices=["vp8d","vp9d"] ,help="Some csv files have codec id in first col. Read it from first col of csv.")
    args = parser.parse_args()
    return args


def get_files_from_folder(folder):
    entries=[]
    for root, dirs, files in os.walk(folder):
        for file in files:     
            #if ".jpg" == os.path.splitext(file)[-1].lower() or ".mp4" == os.path.splitext(file)[-1].lower() or ".mov" == os.path.splitext(file)[-1].lower() or ".3gp" == os.path.splitext(file)[-1].lower():
            p=os.path.join(root,file)               
            entries.append(os.path.abspath(p))                
    return entries  

args = parse_arguments()

output_list_file= open("results_" + (args.file_type).upper() +".csv",'wb')
writer = csv.writer(output_list_file, delimiter=',')
writer.writerow(csv_cols) #write the header


all_files = []

counter=0
unique_file_set = set() #saves only unique files 
md5_hash_set = set() #stores all md5 hashes
md5_hash_lookup_dict = dict() #key is the md5 hash and value is the filename
current_file_hash = None


all_files = get_files_from_folder(args.input_file_or_folder_path)


# number of clips to be decoded
num_of_clips=int(len(all_files))
print "Found "+str(num_of_clips)+" files."


for x in range(num_of_clips):

    filename = os.path.abspath((all_files[x]).strip())
    file_basename = os.path.basename(filename)
    
    filetype = ((os.path.splitext(file_basename)[1]).lower())[1:]
    if (filetype != args.file_type and args.file_type != "all"):
        continue
    
    #if args.file_type == 
    print "Processing..("+str(counter)+") - "+filename
    current_file_hash = hashlib.md5(open(filename,'rb').read()).hexdigest()

    # tmp = filedatetime.split()
    # filedate = tmp[0].split(':')
      


        # tmp = exifdatetime.split()
        # exifdate = tmp[0].split(':')

    #if file_basename in unique_file_set:
    if current_file_hash in md5_hash_set:
        dup_file = ""
        if 1:#(filename != md5_hash_lookup_dict[current_file_hash]):
            dup_file = md5_hash_lookup_dict[current_file_hash]         
            
            templist = [filetype, file_basename, 
                            "=HYPERLINK(\""+filename+"\")", 
                            get_exif_datetime(filename),
                            get_file_datetime(filename), 
                            get_filesize(filename) ,
                            "Duplicate of ",
                            "=HYPERLINK(\""+dup_file+"\")", 
                            get_file_datetime(dup_file),                            
                            get_exif_datetime(dup_file),                        
                            get_file_datetime(filename)==get_file_datetime(dup_file), current_file_hash]

            writer.writerow(templist)                
            output_list_file.flush()
            print ".......Duplicate of "+dup_file
            counter=counter+1
            
            continue
            #add to set if not seen before
    elif current_file_hash not in md5_hash_set:
        md5_hash_lookup_dict[current_file_hash] = filename
        md5_hash_set.add(current_file_hash)  
    else:
        print "something wrong.."
        sys.exit()
    #unique_file_set.add(file_basename)
    
    templist = [filetype, file_basename, 
                            "=HYPERLINK(\""+filename+"\")", 
                            get_exif_datetime(filename),
                            get_file_datetime(filename), 
                            get_filesize(filename) ,
                            None,
                            None,
                            None, None,
                            None, current_file_hash]


    writer.writerow(templist) 
    output_list_file.flush()
    counter=counter+1

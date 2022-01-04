import csv
import os
import shutil
import subprocess
import logging
import datetime


inputfile = "C:\Temp\work\python\opc_tlrs.csv"
output_dir = "TLRS-channels"
parent_dir = "C:\Temp\work"
operator = "TLRS"
operator_code = "3200"
proto_dir = "C:\Temp\work\python\prototypy"
scr_num = 100
proto_dir_a = os.path.join(proto_dir, operator)
longKS = "djJ8MzIwMHyHQFr96QF0fjOP3st3L7pd2jumTfn8QxxqsdaAB3QuA4D7_oH2ZB_YNMeL-G6aYYKhZlPhMxgV_KzBfDGJ24pCXbm1qqQAKnSU09y-xyrglo8JicvwByvzuWdnHhYfsaGd5Va8G6nOZ25rxII1-yEJ"

# initializing rows list
rows = []

# create project directory
ts = datetime.datetime.now().strftime("%Y.%m.%d_%H%M%S")
output_dir = "TLRS-channels-" + ts
path = os.path.join(parent_dir, output_dir)
os.mkdir(path)

#logging
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename=os.path.join(path, "makelog.log"), filemode="a+",
                        format="%(asctime)-1s %(levelname)-0.5s %(message)s")

logging.info("LOGGER say hello")

logging.info("inputfile = " + inputfile)
logging.info("output_dir = " + output_dir)
logging.info("parent_dir = " + parent_dir )
logging.info("operator_code = " + operator_code)
logging.info("proto_dir = " + proto_dir)
logging.info("scr_num = " + str(scr_num))
logging.info("Dir --> " + path + "  was created")

#copy pre-requisites
shutil.copy(os.path.join(proto_dir, "all.bat"), os.path.join(path, "all.bat"))
logging.info("file --> " + os.path.join(path, "all.bat") + "  was copied")
shutil.copy(os.path.join(proto_dir, "amonscript.exe"), os.path.join(path, "amonscript.exe"))
logging.info("file --> " + os.path.join(path, "amonscript.exe") + "  was copied")
shutil.copy(inputfile, os.path.join(path, "source_opc_channel_lineup.csv"))
logging.info("file --> " + inputfile + "  was copied")
#inputfile

# append to all.bat sentence with path
all_b_sentense = "set PATH="+path+"\n\n"
f = open(os.path.join(path, "all.bat"), "a")
f.write(all_b_sentense)
f.close()

# reading csv file
with open(inputfile, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile, delimiter = ';')
    logging.info("CSV: " + inputfile + " opened")

    # extracting each data row one by one
    for row in csvreader:
        rows.append(row) 
        chanel_nu = row[2]
        chanel_na = row[0]
        chanel_id = row[1]
        logging.info("RAW data readed:" +chanel_nu+ "|"+chanel_na+ "|"+chanel_id)

        #create channel directory (HLS)
        dir_name_hls = operator+"-channel_"+chanel_na+"_HLS"
        dir_path = os.path.join(path, dir_name_hls)
        os.mkdir(dir_path)
        print("Directory '% s' created" % dir_path)
        logging.info("Directory '% s' created" % dir_path)

        # append to all.bat sentence with directory
        all_b_sentense = "amonscript -b "+dir_name_hls+"\n"
        f = open(os.path.join(path, "all.bat"), "a")
        f.write(all_b_sentense)
        f.close()
        print("file --> " + os.path.join(path, "all.bat") + "  new sentence append")
        logging.info("file --> " + os.path.join(path, "all.bat") + "  new sentence append")

        #copy file
        #shutil.copy(os.path.join(proto_dir_a, "KALT_login_to_getKS_a.yaml"), os.path.join(dir_path, "KALT_login_to_getKS.yaml"))
        #print("file --> " + os.path.join(dir_path, "KALT_login_to_getKS_a.yaml") + "  was copied")
        #logging.info("file --> " + os.path.join(dir_path, "KALT_login_to_getKS_a.yaml") + "  was copied")
        shutil.copy(os.path.join(proto_dir_a, "defaults.include"), os.path.join(dir_path, "defaults.include"))
        print("file --> "  +os.path.join(dir_path, "defaults.include") + "  was copied")
        logging.info("file --> "  +os.path.join(dir_path, "defaults.include") + "  was copied")
        kalt_f_name = os.path.join(dir_path, "KALT_play_live_channel_"+chanel_na+"_HLS.yaml")
        brpk_f_name = os.path.join(dir_path, "BRPK_play_live_channel_"+chanel_na+"_HLS.yaml")
        shutil.copy(os.path.join(proto_dir, "main.lua"), os.path.join(dir_path, "main.lua"))
        print("file --> " + os.path.join(dir_path, "main.lua") + "  was copied")  
        logging.info("file --> " + os.path.join(dir_path, "main.lua") + "  was copied")      
        shutil.copy(os.path.join(proto_dir, "KALT_play_live_XXXX_HLS.yaml"), kalt_f_name)
        print("file --> " + os.path.join(dir_path, kalt_f_name) + "  was copied")
        logging.info("file --> " + os.path.join(dir_path, "main.lua") + "  was copied")
        shutil.copy(os.path.join(proto_dir, "BRPK_play_live_XXXX_HLS.yaml"), brpk_f_name)
        print("file --> " + os.path.join(dir_path, brpk_f_name) + "  was copied")
        logging.info("file --> " + os.path.join(dir_path, brpk_f_name) + "  was copied")
        shutil.copy(os.path.join(proto_dir, "tests.list"), os.path.join(dir_path, "tests.list"))
        print("file --> " + os.path.join(dir_path, "tests.list") + "  was copied")
        logging.info("file --> " + os.path.join(dir_path, "tests.list") + "  was copied")


        #open file, find string replace it KALT
        with open(kalt_f_name) as r:
            text = r.read().replace("XXXX", ("channel_"+chanel_nu+"_"+chanel_na))
        with open(kalt_f_name, "w") as w:
            w.write(text)
            w.close()
        with open(kalt_f_name) as r:
            text = r.read().replace("YY-YY", longKS)
        with open(kalt_f_name, "w") as w:
            w.write(text)
            w.close()
        print("file --> " + kalt_f_name + "  was edit")
        logging.info("file --> " + kalt_f_name + "  was edit")


        #open file, find string replace it BRPK
        with open(brpk_f_name) as r1:
            text1 = r1.read().replace("XXXX", ("channel_"+chanel_nu+"_"+chanel_na))
        with open(brpk_f_name, "w") as w1:
            w1.write(text1)
            w1.close()
        print("file --> " + brpk_f_name + "  was edit")
        logging.info("file --> " + brpk_f_name + "  was edit")


        # append to tests.list
        #./KALT_login_to_getKS.yml 13 3 3200
        #test_list_sentense1 = " "+operator_code+"\n"
        #./KALT_play_live_1_RTS_1_DASH.yml 100 3 3200 800398
        scr_num = scr_num+1
        test_list_sentense2 = "\n./KALT_play_live_channel_"+chanel_na+"_HLS.yaml "+str(scr_num)+" 3 "+operator_code+" "+chanel_id+ "\n"
        #./BRPK_play_live_1_RTS_1_DASH.yml 101 3 3200
        scr_num = scr_num+1
        test_list_sentense3 = "./BRPK_play_live_channel_"+chanel_na+"_HLS.yaml "+str(scr_num)+" 3 "+operator_code+"\n"
        
        
        f = open(os.path.join(dir_path, "tests.list"), "a")
        #f.write(test_list_sentense1)
        f.write(test_list_sentense2)
        f.write(test_list_sentense3)
        f.close()
        print("file --> " + os.path.join(dir_path, "tests.list") + "  new sentence append")
        logging.info("file --> " + os.path.join(dir_path, "tests.list") + "  new sentence append")
       

        #create channel directory (DASH)
        dir_name_dash = operator+"-channel_"+chanel_na+"_DASH"
        dir_path = os.path.join(path, dir_name_dash)
        os.mkdir(dir_path)
        print("Directory '% s' created" % dir_path)
        logging.info("Directory '% s' created" % dir_path)
        # append to all.bat sentence with directory
        all_b_sentense = "amonscript -b "+dir_name_dash+"\n"
        f = open(os.path.join(path, "all.bat"), "a")
        f.write(all_b_sentense)
        f.close()
        print("file --> " + os.path.join(path, "all.bat") + "  new sentence append")
        logging.info("file --> " + os.path.join(path, "all.bat") + "  new sentence append")

        #copy file
        #shutil.copy(os.path.join(proto_dir_a, "KALT_login_to_getKS_b.yaml"), os.path.join(dir_path, "KALT_login_to_getKS.yaml"))
        #print("file --> " + os.path.join(dir_path, "KALT_login_to_getKS_b.yaml") + "  was copied")
        #logging.info("file --> " + os.path.join(dir_path, "KALT_login_to_getKS_b.yaml") + "  was copied")
        shutil.copy(os.path.join(proto_dir_a, "defaults.include"), os.path.join(dir_path, "defaults.include"))
        print("file --> "  +os.path.join(dir_path, "defaults.include") + "  was copied")
        logging.info("file --> "  +os.path.join(dir_path, "defaults.include") + "  was copied")
        kalt_f_name = os.path.join(dir_path, "KALT_play_live_channel_"+chanel_na+"_DASH.yaml")
        brpk_f_name = os.path.join(dir_path, "BRPK_play_live_channel_"+chanel_na+"_DASH.yaml")       
        shutil.copy(os.path.join(proto_dir, "main.lua"), os.path.join(dir_path, "main.lua"))
        print("file --> " + os.path.join(dir_path, "main.lua") + "  was copied") 
        logging.info("file --> " + os.path.join(dir_path, "main.lua") + "  was copied")       
        shutil.copy(os.path.join(proto_dir, "KALT_play_live_XXXX_DASH.yaml"), kalt_f_name)
        print("file --> " + os.path.join(dir_path, kalt_f_name) + "  was copied")
        logging.info("file --> " + os.path.join(dir_path, kalt_f_name) + "  was copied")
        shutil.copy(os.path.join(proto_dir, "BRPK_play_live_XXXX_DASH.yaml"), brpk_f_name)
        print("file --> " + os.path.join(dir_path, brpk_f_name) + "  was copied")
        logging.info("file --> " + os.path.join(dir_path, brpk_f_name) + "  was copied")
        shutil.copy(os.path.join(proto_dir, "tests.list"), os.path.join(dir_path, "tests.list"))
        print("file --> " + os.path.join(dir_path, "tests.list") + "  was copied")
        logging.info("file --> " + os.path.join(dir_path, "tests.list") + "  was copied")

        #open file, find string replace it KALT
        with open(kalt_f_name) as r:
            text = r.read().replace("XXXX", ("channel_"+chanel_nu+"_"+chanel_na))
        with open(kalt_f_name, "w") as w:
            w.write(text)
            w.close()
        print("file --> " + kalt_f_name + "  was edit")
        logging.info("file --> " + kalt_f_name + "  was edit")

        #open file, find string replace it BRPK
        with open(brpk_f_name) as r1:
            text1 = r1.read().replace("XXXX", ("channel_"+chanel_nu+"_"+chanel_na))
        with open(brpk_f_name, "w") as w1:
            w1.write(text1)
            w1.close()
        with open(brpk_f_name) as r1:
            text1 = r1.read().replace("YY-YY", longKS)
        with open(brpk_f_name, "w") as w1:
            w1.write(text1)
            w1.close()
        print("file --> " + kalt_f_name + "  was edit")
        logging.info("file --> " + kalt_f_name + "  was edit")

        # append to tests.list
        #./KALT_login_to_getKS.yml 13 3 3200
        #test_list_sentense1 = " "+operator_code+"\n"
        #./KALT_play_live_1_RTS_1_DASH.yml 100 3 3200 800398
        scr_num = scr_num+1
        test_list_sentense2 = "\n./KALT_play_live_channel_"+chanel_na+"_DASH.yaml "+str(scr_num)+" 3 "+operator_code+" "+chanel_id+ "\n"
        #./BRPK_play_live_1_RTS_1_DASH.yml 101 3 3200
        scr_num = scr_num+1
        test_list_sentense3 = "./BRPK_play_live_channel_"+chanel_na+"_DASH.yaml "+str(scr_num)+" 3 "+operator_code+"\n"
        
        f = open(os.path.join(dir_path, "tests.list"), "a")
        #f.write(test_list_sentense1)
        f.write(test_list_sentense2)
        f.write(test_list_sentense3)
        f.close()
        print("file --> " + os.path.join(dir_path, "tests.list") + "  new sentence append")
        logging.info("file --> " + os.path.join(dir_path, "tests.list") + "  new sentence append")
        
# get total number of rows
print("Total of channels: %d"%(csvreader.line_num))
logging.info("Total of channels: %d"%(csvreader.line_num))

os.chdir(path)
print("Changed DIR: " + path)
logging.info("Changed DIR: " + path)
p = subprocess.run(os.path.join(path, "all.bat > testlog.log"))
print("Done with subprocess" + os.path.join(path, "all.bat > testlog.log"))
logging.info("Done with subprocess " + os.path.join(path, "all.bat > testlog.log"))

searchstr = "Exit Message:"
searchstr1 = "OK"

fopen = open(os.path.join(path,"testlog.log"), mode = "r")
fread = fopen.readlines()
logging.info("Reading file " + os.path.join(path,"testlog.log")+ " for any errors occured")
ch = 0
for line in fread:
    if searchstr in line:
        if not searchstr1 in line:
            ch = ch + 1
            print(line)
            logging.info(line)
print("Found "+ str(ch) + " errors")
logging.info("Found "+ str(ch) + " errors")
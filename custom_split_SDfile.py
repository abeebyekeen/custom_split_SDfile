'''
A python script to split huge compound library in sd/sdf format into user-defined smaller sub-libraries
	Author: Abeeb A. YEKEEN
	Contact: yekeenaa@mail.ustc.edu.cn, abeeb.yekeen@hotmail.com
Date: 2021.11.03
'''
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from builtins import round
from builtins import input
from builtins import open
from builtins import str
#from future import standard_library
#standard_library.install_aliases()
import time

def track_status():
	print(status)
	log_file.write(status)
	
def citation():
	status='\nIf you use this script in your work, please cite the relevant paper:\n\n    "Yekeen et al. (2022). To be published..."\n'
	print(status)
	log_file.write(status)

def functn():
	purpose='\nThis script will help you split a huge compound library in sd/sdf format into user-defined smaller sub-libraries\n'
	print(purpose)

functn()

print("Please provide the following input to customize the splitting process based on your need\n")

status="Give a name to this job: "
job_name=str(input(status ))
record="log_"+job_name+".txt"
status="\n--> Jobname: "+job_name+"\n"
print(status)
log_file=open(record, "w")
log_file.close()
log_file=open(record, "a")
log_file.write(status)
status="How many compounds do you want in each sub-library? "
sublib_size=input(status )
status="\nYou entered: "+str(sublib_size)+"\n"
track_status()

while sublib_size.isnumeric() == False:
	print("ENTRY REJECTED!\n**PLEASE MAKE SURE YOU PROVIDE AN INTEGER!\n")
	sublib_size=input("How many compounds do you want in each sub-library? " )
	status="\nYou entered: "+str(sublib_size)+"\n"
	track_status()
status="--> "+str(sublib_size)+" compounds will be saved into each sub-library.\n"+"--> "+"Please note that the last sub-library may be much lesser than this value.\n"
track_status()
#inputing the file to be split
status="Please copy the name of the SD/SDF file to be processed and paste here: "
log_file.write(status)
filename=str(input(status ))
status="\nYou entered: "+str(filename)+"\n"
track_status()
if filename[-4:]==".sdf":
	filename=filename[0:-4]
	status="File name has the extension .SDF!\nCorrected file name is: "+filename+"\n"
	track_status()
elif filename[-3:]==".sd":
	filename=filename[0:-3]
	status="--> File name has the extension .SD!\n--> Corrected file name is: "+filename+"\n"
	track_status()
sdfile=filename+".sdf"
#opening the full SD/SDF file
status="Opening "+sdfile+" ...\n"
track_status()

ini1_time = time.process_time() #start time of split_sdf

library=open(sdfile, "r")
#reading the SDF files in the library
status="Reading the contents of "+sdfile+" ...\n"
track_status()
datalines=library.readlines()
status="Contents of "+sdfile+" have been read, now assigning variables...\n"
track_status()
sublib_size=int(sublib_size)
compd_no=0
milestone_factor=0
cycle=1
timercyc=0
all_compds=0
liner=1
endtm=0
endt_temp=0
dataline_no=0
status="Reading structures from "+sdfile+" ...\n"
track_status()
for data in datalines:
	dataline_no+=1
	if "$$$$" in data:
		compd_no+=1
		if compd_no%50000==0:
			milestone_factor+=1
			milestone_count=milestone_factor*50000
			status="No of compounds processed: " +str(milestone_count)+"\n"
			track_status()
		if liner==0:
			status="\nFirst line of "+"sub-library "+str(cycle)+" has been created\nWriting the first structure of "+"sub-library "+str(cycle)+"...\n"
			track_status()
			liner+=1
			continue
	if compd_no<=sublib_size:
		if compd_no<sublib_size:
			cycle=cycle
			sublib_name=filename+"_sublib_"+str(cycle)+".sdf"
			sub_lib=open(sublib_name, "a")
			#writing out the SDF lines
			sub_lib.write(data)
		if compd_no==sublib_size:
			sub_lib.write(data)
			sub_lib.write("$$$$")
			sub_lib.close()
			status="\nSub-library "+str(cycle)+" has been successfully written\n"
			track_status()
			timercyc+=1
			cycle+=1
			endt_temp=time.process_time()
			endtm+=endt_temp
			sublib_name=filename+"_sublib_"+str(cycle)+".sdf"
			all_compds+=compd_no
			compd_no=0
			liner=0
	if dataline_no==len(datalines):
		all_compds+=compd_no
status="Last file has been successfully written\n"
track_status()
status="-->"+str(all_compds)+" compounds have been split into "+str(cycle)+" sub-libraries\n"+"--> Record of this job can be found in the file \""+record+"\"\n"
track_status()

end1_t = time.process_time() #end time of split_sdf
end1_time = (end1_t)+(endtm)
#calculate elapsed time
runtime1_sec = (end1_time-ini1_time)

if runtime1_sec>60.0:
	runtime1_sec_2d = float("{:.2f}".format(runtime1_sec%60))
elif runtime1_sec<60.0:
	runtime1_sec_2d = float("{:.2f}".format(runtime1_sec))
runtime1_min = round(runtime1_sec//60)
runtime1_hr = round(runtime1_sec//3600)
status="Time elapsed: "+str(runtime1_hr)+" hr "+str(runtime1_min)+" min "+str(runtime1_sec_2d)+" sec\n"
track_status()
citation()
library.close()
log_file.close()
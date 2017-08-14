
from matplotlib.dates import DayLocator, HourLocator, DateFormatter
from Tkinter import *
from tkFileDialog import askopenfilename

import csv, os, sys, numpy, datetime

edrow=[]
printlist=[]
printr=[]

class MyFrame(Frame):
   
    def __init__(self):
        
        #creating main window structure
        Frame.__init__(self)
        self.master.title("ODV2CA")
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid(sticky=W+E+N+S)
        self.linecountstr=[]
        self.button = Button(self, text="Browse", command=self.browse, width=25)
        self.button.grid(row=1, column=0, sticky=W)
        self.button = Button(self, text="Launch", command=self.launch, width=25)
        self.button.grid(row=2, column=0, sticky=W)
      
    def browse(self, parent=__init__):
        #browsing for input file
        fname = askopenfilename(filetypes=(("CSV", "*.csv"),("All files", "*.*") ))
         
        if fname:
            try:
                self.name=fname
            except:                    
                pass
            return
        
    def launch(self, parent=__init__):  
        #opening file for reading and writing
        basename=os.path.splitext(self.name)[0]
        inf = open(self.name, "r")
        outf = open('%s_out.csv' % basename, "w") 
        reader = csv.reader(inf, delimiter=',')
        writer = csv.writer(outf, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        writer2 = csv.writer(outf, quoting=csv.QUOTE_ALL)
        linecount=0
        rowcount=0
        
        #counting rows
        for line in reader:
            writer2.writerow(line)
            for row in line:
                rowcount+=1   
            break
        
        #going to the 3rd line
        inf.seek(0)
        next(inf)  
        next(inf)
        next(inf)
        
        #counting lines
        for line in reader:
            linecount+=1
                
           
        self.linecountstr=[]
        for i in range(rowcount):   
            self.linecountstr.append(str(linecount))
        
       #going to the 3rd line
        inf.seek(0)
        next(inf)  
        next(inf)
        next(inf)
        
       #creating 2nd line with sample count
        writer.writerow(self.linecountstr)
        
        
        #converting starting datetime
        for line in reader:
            for row in line:
                print(row)
                st=datetime.datetime.strptime(row, "%Y-%m-%d %H:%M:%S")
                weeksst=datetime.datetime.strptime(row, "%Y-%m-%d %H:%M:%S").timetuple().tm_yday
                
                st=datetime.datetime(st.year, st.month, st.day, st.hour, st.minute, st.second )
                st=datetime.timedelta(days=weeksst, hours=st.hour,minutes=st.minute,seconds=st.second).total_seconds()
                
                break
            break
        
        inf.seek(0)
        next(inf)  
        next(inf)
        next(inf)
        
        #converting dates into seconds since starting datetime
        for line in reader:
            for row in line:
                
                rowd=datetime.datetime.strptime(row, "%Y-%m-%d %H:%M:%S")
                weeksrowd=datetime.datetime.strptime(row, "%Y-%m-%d %H:%M:%S").timetuple().tm_yday
                rowd=datetime.datetime(rowd.year, rowd.month, rowd.day, rowd.hour, rowd.minute, rowd.second)
                
                rowd=datetime.timedelta(days=weeksrowd, hours=rowd.hour,minutes=rowd.minute,seconds=rowd.second).total_seconds()
                edrow.append(rowd-st)
                
                break
        
        inf.seek(0)
        next(inf)  
        next(inf)
        next(inf)
        
        
        linenumber=0
        
        
        #printing data to file with desired precision, filtering typical major erorrs
        for line in reader:
            printr=[]
            conv="%.4f" % float(edrow[linenumber])
            printr.append("%s" % conv)
            for i in range(1,rowcount):
                if (("nie" not in line[i]) and ("NaN" not in line[i]) and ((float(line[i]))>-9000)):
                    conv="%.4f" % float(line[i])
                    printr.append("%s" % conv)
                else:
                    printr.append("0.000")
            printlist.append(printr)
            
            linenumber+=1
            
        writer.writerows(printlist)
 
        inf.close()
        outf.close()
        return  
        
           
if __name__ == "__main__":
    
    MyFrame().mainloop()
    

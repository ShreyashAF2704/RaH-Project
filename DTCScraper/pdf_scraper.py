from PyPDF2 import PdfFileReader
import re 

contents = ""
with open(r"C:\Users\Sahil\Documents\Shreyash_files\Projects\Amberflux RaH Project\DTCScraper\MC-10184330-0001.pdf", 'rb') as f:
    pdf = PdfFileReader(f)
    for page_num in range(pdf.getNumPages()):
        page = pdf.getPage(page_num)
        contents += page.extractText()
        
content_arr = contents.split("\n")
months = ["January","February", "March" ,"April" ,"May" ,"June" ,"July" ,"August" ,"September" ,"October" ,"November" ,"December" ]

topic = "" 
for i in range(len(content_arr)):
    ele = content_arr[i].split(" ")
    if ele[0] in months:
        topic = content_arr[i+1]
        if content_arr[i+2] != "AFFECTED VEHICLES":
            topic += content_arr[i+2]
        break
subtopics = ["AFFECTEDVEHICLES","REVISIONSUMMARY","SYMPTOM","POSSIBLECAUSE","CORRECTIVEACTION","WARRANTYCLAIMINFORMATION","PARTSINFORMATION","REPAIRPROCEDURE","BACKGROUND","CUSTOMERNOTIFCATION","CUSTOMERNOTIFCATION","REPAIRPROCEDUREA","REPAIRPROCEDUREB"]

info = {}
print(topic)
print("-----------")

for k in range(i,len(content_arr)):
    ele = ""
    z = content_arr[k].replace(" ","")
    if z in subtopics:
        counter = k+1
        
        while counter < len(content_arr):
            z_ = content_arr[counter].replace(" ","")
            if z_ in subtopics:
                break
            
            ele += content_arr[counter]
            if z == "REPAIRPROCEDURE":
                ele += "\n"
            counter += 1
        print(content_arr[k])
        print(ele)
        print("--------------")
        info[z] = ele 
        ele = ""
        k = counter-1
        


ele = []
for j in info["REPAIRPROCEDURE"].split("\n"):
    if j != "" and j[0].isnumeric():
        print(j)
        ele.append(j)

info["REPAIRPROCEDURE"] = ele


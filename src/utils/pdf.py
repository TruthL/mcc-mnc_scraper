import PyPDF2 as pdf
import re

def get_page(obj):
    num = obj.getNumPages()
    string = "for the international identification plan"
    for i in range(2,num):
        page = obj.getPage(i)
        text = page.extract_text()
        if re.search(string,text):
            return i
    return (None) 

#get table 
#read what is updated
#get table and give date updated (bulletin num)
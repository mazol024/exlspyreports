
import os
from sqlalchemy import false, true


def readonefile(fname = ".\query\query1.sql"):
    f = open(fname)
    comments = []
    selects=[]
    flag =false
    qstring = ''
    for i in f:
        if i.strip().startswith('-'):
            comments.append(i.strip().replace('-',''))
            continue
        elif i.strip().lower().startswith('select ') and i.find(';') >= 0 :
            selects.append(i.strip()[:i.find(';')+1])
            flag=false
            continue
        elif i.strip().lower().startswith('select '): 
            qstring+=(i.strip().title() +' ')
            flag= true
            continue
        elif flag and i.find(';') >= 0 :
            qstring+=(i.strip() )
            flag= false
            selects.append(qstring)
            qstring =''
            continue
        elif flag :
            qstring+=(i.strip() +' ')
            continue
        elif i.strip(): 
            continue
    for v in comments:
         print(v )
    for v in selects:
         print(v )
    counter = 0         
    rows = len(comments)
    p=[]
    for q in selects:
        if counter < rows:
            comment = comments[counter]
            counter+=1
        else:
            comment = 'No name'
        p.append({comment:q})
    result = {fname[8:fname.find('.sql')] : p}
    print( result)
def listdir(dir1 = "./query/"):
    arr = [x for x in  os.listdir(dir1) if  x.lower().find('.sql')>0 ]
    #print(arr)
    for i in arr:
        readonefile(dir1+i)
    
        
if __name__ == "__main__":
    #readonefile()
    listdir()
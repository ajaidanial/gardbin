import pymysql.cursors
from itertools import islice
connection = pymysql.connect(host='localhost',user='root',password='EClavan956#',db='tagsys',cursorclass=pymysql.cursors.DictCursor)
print("connect successful!!!")
def concateFunc(list1):
    str1 = ' '.join([elem for elem in list1[1:]])
    return str1
file1 = open('GARDBIB.TXT', 'r')
dict1 = {'I3': None, 'IB': None, 'AV': None, 'BI': None, 'AU':None, 'BC':None, 'CO':None,'ED': None, 'IL':None, 'EI': None, 'IU': None, 'CP': None, 'LA': None, 'MP': None, 'NC': None, 'PD': None, 'PA': None, 'NP': None, 'RP': None, 'RI': None, 'RE': None, 'DI': None, 'PU': None, 'YP': None, 'RC': None, 'RS': None, 'SR': None, 'SE':None, 'TI': None, 'ST': None, 'PT': None, 'TR': None, 'PN': None, 'DE': None, 'EA': None, 'RF': None, 'RD': None, 'SI':None, 'WE': None, 'SG':None, 'PI': None, 'GC': None, 'TP': None}
count_records=0
l1=[]
#for line in islice(file1,1000):
for line in file1:
    line1 = line.split()
    index1=0
    if line.find("**")==0:
        if line.find("**START")==0:
            index1=1
        else:
            index1=0
    else:
        index1=-1
    if len(line1) > 1:
        if dict1[line1[0]] is not None:
            dict1[line1[0]]+=','+concateFunc(line1)
        else:
            dict1[line1[0]]=concateFunc(line1)
    if index1==0:
        dict1['I3']=int(dict1['I3'])
        l1.append(tuple(dict1.values()))
        dict1.update((k, None) for k in dict1)
    if len(l1)==5000:
      with connection.cursor() as cursor:
          placeholders=','.join(['%s']*len(dict1))
          columns = ','.join(dict1.keys())
          sql = "INSERT INTO `mytable1` (%s) VALUES (%s)" % (columns, placeholders)
          count_records+=5000;
          print("Iterator : ",count_records)
          cursor.executemany(sql,l1)
          del l1[:]
          connection.commit()
print("Total Records : ",count_records)
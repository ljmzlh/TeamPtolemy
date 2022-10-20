import os
import json
import time
import pandas as pd
import csv

def aggre():
    #dlist=os.listdir('amazon_processed')
    dlist=os.listdir('output')
    dlist.sort()

    raid,row,col,x,y=[],[],[],[],[]

    for sb in dlist:
        dn=sb

        cvs=pd.read_csv('output/'+dn)
        print(dn)
        for t in cvs['raster_ID']:
            raid.append(t)
        for t in cvs['row']:
            row.append(t)
        for t in cvs['col']:
            col.append(t)
        for t in cvs['NAD83_x']:
            x.append(t)
        for t in cvs['NAD83_y']:
            y.append(t)
    
    with open('output.csv', 'w', newline='') as csvfile:
        fieldnames = ['raster_ID', 'row','col','NAD83_x','NAD83_y']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(len(raid)):
            writer.writerow({'raster_ID':raid[i], 'row':row[i],'col':col[i],
                            'NAD83_x':x[i],'NAD83_y':y[i]})

        

        


if(__name__=='__main__'):
    aggre()

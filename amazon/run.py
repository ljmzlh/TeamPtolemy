import os
import cv2
from tqdm import tqdm
from call_amazon import call_amazon
import json
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--tif_path",type=str,default='../dataset/Validation/')
args = parser.parse_args()

dlt=1280

try:
    os.mkdir('amazon_res')
except:
    pass

flist=os.listdir(args.tif_path)
for i in tqdm(range(len(flist))):
    fn=flist[i]
    if(not fn.endswith('.tif')):
        continue
    fn=fn[:fn.find('.tif')]
    path=args.tif_path+fn+'.tif'
    
    try:
    
        image=cv2.imread(path)

        cnt=0
        H,W=image.shape[0],image.shape[1]
        
        for hst in range(0,H,dlt):
            for wst in range(0,W,dlt):
                hed,wed=min(H,hst+dlt),min(W,wst+dlt)
                
                cnt+=1
                doc=fn+'_'+str(cnt)+'.tif'
                
                box=call_amazon(doc)
                
                output={'hst':hst,'wst':wst,'h':hed-hst,'w':wed-wst,
                        'box':box}

                with open('amazon_res/'+fn+'_'+str(cnt),'w') as f:
                    f.write(json.dumps(output))
    except:
        pass



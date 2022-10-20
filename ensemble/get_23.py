import pstats
from utils import glo,output_can,filter_by_constr,glo,choose_cand,get_vec
from utils import verti,horiz,get_output

def get_23(target,clue_lat,clue_long,dn):

    can_lat,can_long=glo.can_lat,glo.can_long

    output_can(can_lat,'lat')
    output_can(can_long,'long')

    #distance(pixel)=distance()
    ret=None
    if(len(can_lat)==2):
        v_ver,v_hor,s=get_vh(can_long,'long',dn)

        std=can_lat[0]
        pos,val,f=None,None,None
        if(not horiz(can_lat[0],can_lat[1])):
            pos=(std['pos'][0]+v_hor[0],std['pos'][1]+v_hor[1])
            val,f=std['val'],std['f']
        else:
            pos=(std['pos'][0]+v_ver[0],std['pos'][1]+v_ver[1])
            val,f=std['val']-norm(v_ver)/s,std['f']
        
        can_lat.append({'pos':pos,'val':val,'f':f})

        ret,_=get_output(target,can_lat,clue_lat,'lat',dn)
    else:
        v_ver,v_hor,s=get_vh(can_lat,'lat',dn)
        std=can_long[0]
        pos,val,f=None,None,None
        if(not verti(can_long[0],can_long[1])):
            pos=(std['pos'][0]+v_ver[0],std['pos'][1]+v_ver[1])
            val,f=std['val'],std['f']
        else:
            pos=(std['pos'][0]+v_hor[0],std['pos'][1]+v_hor[1])
            val,f=std['val']-norm(v_hor)/s,std['f']
        
        can_long.append({'pos':pos,'val':val,'f':f})

        ret,_=get_output(target,can_long,clue_long,'long',dn)

    
    print(ret)

    return ret

    


    
def get_vh(candi,tag,dn):
    candi=filter_by_constr(candi,glo.constr,dn)
    candi=choose_cand(candi,tag)

    v_ver,v_hor=None,None

    
    v1,v2=get_vec(candi[0],candi[1]),get_vec(candi[0],candi[2])

    if(abs(v1['val'])<glo.eps):
        if(tag=='lat'):
            v_hor=v1['pos']
        else:
            v_ver=v1['pos']
    elif(abs(v2['val'])<glo.eps):
        if(tag=='lat'):
            v_hor=v2['pos']
        else:
            v_ver=v2['pos']
    else:
        #kv1+v2=0
        k=-v2['val']/v1['val']
        pos=(k*v1['pos'][0]+v2['pos'][0], k*v1['pos'][1]+v2['pos'][1])
        if(tag=='lat'):
            v_hor=pos
        else:
            v_ver=pos


    if(v_ver==None):
        v_ver=(-v_hor[1],v_hor[0])
    else:
        v_hor=(-v_ver[1],v_ver[0])



    if(v_hor[1]<0):
        v_hor=(-v_hor[0],-v_hor[1])
    
    if(v_ver[0]<0):
        v_ver=(-v_ver[0],-v_ver[1])
    

    
    if(tag=='lat'):
        s=get_scale(v_ver,v1,v2)
    else:
        s=get_scale(v_hor,v1,v2)
    
    

    return v_ver,v_hor,s


def get_scale(v_std,v1,v2):
    v,val=None,None
    if(abs(v1['val'])>glo.eps):
        v,val=v1['pos'],v1['val']
    elif(abs(v2['val'])>glo.eps):
        v,val=v2['pos'],v2['val']
    
    v_proj=proj(v,v_std)

    s=norm(v_proj)/abs(val)

    return s
    

def proj(v,v_std):
    fz=v[0]*v_std[0]+v[1]*v_std[1]
    fm=norm(v)*norm(v_std)

    k=fz/fm
    return (k*v_std[0],k*v_std[1])


def norm(v):
    return (v[0]**2+v[1]**2)**0.5

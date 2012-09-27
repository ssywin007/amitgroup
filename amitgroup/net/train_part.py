import numpy as np
import sys
import copy
import time
import train_net as tn
from pylab import *

def extract_parts(expi):

   XY=tn.rearrange(expi.ddtr,0,expi.numtrain)
   X=XY[0]
   nt=X.shape[0]
   num_samps=50
   ps2=np.floor(expi.pp.part_size/2)
   imsize=np.sqrt(X.size/(8*nt))
   X.shape=[nt,8,imsize,imsize]
   ZZ=[]
   for t in range(nt):
       ii=np.floor(np.random.rand(num_samps)*(imsize-expi.pp.part_size))+ps2
       jj=np.floor(np.random.rand(num_samps)*(imsize-expi.pp.part_size))+ps2
       for s in range(num_samps):
           Z=X[t,:,ii[s]-ps2:ii[s]+ps2+1,jj[s]-ps2:jj[s]+ps2+1]
           if (np.sum(Z)>expi.pp.min_edges):
               Z.shape=[8,expi.pp.part_size,expi.pp.part_size]
               ZZ.append(Z)

   pptr=np.array(ZZ)
   
   return(pptr)
           
       


                
def train_parts(expi):

    
    pptr=extract_parts(expi)
    print 'No of windows ', pptr.shape[0]
    raw_input()
    Jmid=expi.pp.Jmax/2
    Jqtr=Jmid*expi.pp.reduction_factor
    numtrain=pptr.shape[0]
    numfeat=pptr.size/numtrain
    TT=range(numtrain)
    Parts=[]
    for it in range(expi.pp.numit):
        print 'iteration ', it, len(Parts)
        raw_input()
        np.random.shuffle(TT)
        inp=[]
        for t in TT:
            hits=0
            XI=(pptr[t,:].flatten())==1
            XI.shape=[numfeat,1]
            i=0
            for P in Parts:
                h=np.dot(pptr[t,:].flatten(),P-Jmid)
                print 'image ', t,' part ', i,' field ', h
                inp=raw_input('--> ')
                if (inp=='s'):
                   break
                # Part activated, apply potentiations.
                if (h>expi.pp.theta):
                    hits+=1
                    tn.potentiate_ff(expi.pp,h,XI,P,Jmid)
                    break
                else:
                   tn.depress_ff(expi.pp,h,XI,P,Jmid)
                i+=1
            if (inp=='s'):
               break
            if (hits==0):
                J=np.ones((numfeat,1))*Jqtr
                h=np.dot(pptr[t,:].flatten(),J-Jmid)
                print 'h before ', h
                tn.potentiate_ff(expi.pp,h,XI,J,Jmid)
                print J
                print 'h after ', np.dot(pptr[t,:].flatten(),J-Jmid)
                Parts.append(J)
                print t, len(Parts)
    print len(Parts)
    inp=raw_input('--> ')
    if (inp!='s'):
       for P in Parts:
          fig=figure()
          G=np.copy(P)
          G.shape=[8,expi.pp.part_size,expi.pp.part_size]
          for a in range(181,189):
             subplot(a)
             imshow(G[a-181,:,:])
          
    return Parts
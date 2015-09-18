import json
from pprint import pprint
from scipy.stats.stats import pearsonr
from geopy.geocoders import Nominatim
import pickle
import tarfile
from spyderlib.utils.iofuncs import load_dictionary
##Database Connection
import couchdb
import time
import matplotlib.pyplot as plt
from numpy import loadtxt
import re
import us
import numpy as np


class Correlation_tool:
    
    
    @staticmethod
    def Correlate(x, y, plot):
        
        if not len(x) == len(y):
            print "***error: x.length != y.length***"
            print "x.length: " + str(len(x)) + ", y.length: " + str(len(y));
        
        ##NORMALIZE THE STATE DATA:
        norm = [((float(i)/max(x)) * 10) for i in x]
        
        
        
        ## correlate the data, print the result
        corr = pearsonr(norm,y);
        print "CORRELATION: "+ str(corr)
        
        ## Plot the tweets over the real data, also optional
        if plot:
            scale = range(len(y))
            f1 = plt.figure();
            l1 = plt.plot(scale,norm,color="red")
            l2 = plt.plot(scale,y,color="blue")
            plt.ylim(-0.5,10.5)
            plt.xlim(-0.5,53.5)
            
        return corr
        
        
        
        
        
        

#this stores all my unit tests
import unittest
import sys
import pandas as pd
from hw3.functions import *

class hw3TestCase (unittest.TestCase):
    
    
#************************verbosity tests*****************
    
    def test__test1(self):
        #Test 1 check if verbosity treats consecutive speech acts as 1 in same episode (should)
        m = pd.read_csv("t1_data.csv", sep = '\t',index_col = "new")
        v = cnt_sa(m,0)
        self.assertEqual(v,1)
        
    def test__test2(self):
        #Test 2 check if verbosity treats speech acts spanning 2 episodes as 1 (should not!)
        m2 = pd.read_csv("t2_data.csv", sep = '\t')
        v2 = cnt_sa(m2,0)
        self.assertEqual(v2,3)
        
    def test__test3(self):
        #Test 3 checks if separate speech acts are counted separately (should)
        m3=pd.read_csv("t3_data.csv", sep = '\t',index_col = "new")
        v3 = cnt_sa(m3,0)
        self.assertEqual(v3,2)
        
    
#**********************mention tests********************
        
        
    def test__test4(self):
        #Test 4 checks if mention counts multiple occurences of pony name in a single speech (should)
        m4 = pd.read_csv("t4_data.csv", sep = '\t')
        dict1 = mention_single(m4,0)
        pink = dict1['pinkie']
        self.assertEqual(pink,1)
        
    def test__test5(self):
        #Test 5 checks if mention counts all lower cases (should not!)
        m5 =pd.read_csv("t5_data.csv", sep = '\t')
        dict2 = mention_single(m5,0)
        self.assertEqual(dict2,{})
        
    
#****************follow_on comments tests***************
        
        
    def test__test6(self):
        #Test 6 checks if follow-on counts the right order: stats showing how much this pony speaks after others
            #not the other way round
        f1 = pd.read_csv("t6_data.csv", sep = '\t')
        fd1 = follow_on(f1,0)
        flut = fd1["fluttershy"]
        self.assertEqual(flut,0.33)
        
    def test__test7(self):
        #Test 7 checks if follow-on counting ignores speech-acts in-between (should not!)
        f7 = pd.read_csv("t7_data.csv", sep = '\t')
        fd2 = follow_on (f7,0)
        pinkie = fd2['pinkie']
        self.assertEqual(pinkie,0)
        
    def test__test8(self):
        #Test 8 checks if follow-on includes following speech act in anoter episode (should not!)
        f8 = pd.read_csv("t8_data.csv", sep = '\t')
        fd3 = follow_on(f8,0)
        flut1 = fd3['fluttershy']
        self.assertEqual(flut1,0)
   
   
#**************non_dictionary words tests*****************
        
        
    def test__test9(self):
        #Test 9 checks if non-dict words do appear in dictionary (should not!)
        d = "dictionary.txt"
        n1 = pd.read_csv("t9_data.csv", sep = '\t')
        lst = non_dict_p(d,n1,3)
        self.assertEqual(lst,['he', 'is', 'gr', 'wa', 'mtrces'])
        
    def test__test10(self):
        #Test 10 checks if non-dict words removes all unicodes
        d = "dictionary.txt"
        n2 = pd.read_csv("t10_data.csv",sep = '\t')
        lst2= non_dict_p(d,n2,3)
        self.assertEqual(lst2,['he', 'is', 'wa', 'gr', 'by'])
        
        

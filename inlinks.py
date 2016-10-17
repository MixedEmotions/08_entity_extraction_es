#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
author: @marco
'''
import time
try:
    # version 2.6+
    import json
except:
    # version 2.5
    import simplejson as json
import logging

class Inlinks(object):
    '''
    classdocs
    '''
    ws_array=[]
    text=''
    inlink_threeshold=0
    concepts_inlinks={}
    stopwords=set()
    left=[]
    right=[]
    '''
    generate the whitespace array of the text
    '''
    def generate_ws(self):
        ws_array = [0]
        a = 0
        for c in self.text:
            if c == ' ':
                ws_array.append(a)
            a += 1
        
        ws_array.append(len(self.text))
        return ws_array


    def __init__(self, text, inlinks_threeshold, concepts_inlinks,stopwords,composition):
        '''
        Constructor
        '''
        self.text=text
        #generate the white space array to process the text
        self.ws_array=self.generate_ws()
        self.inlink_threeshold=int(inlinks_threeshold)
        self.concepts_inlinks=concepts_inlinks
        self.stopwords=stopwords
        self.left=[]
        self.rigth=[]
        self.composition=composition
        

    def contains_substring(self, left_position, right_position, position):
        return left_position >= self.left[position] and right_position <= self.right[position]
    
    def no_all_sw(self,text):
        result=True
        for part in text.split(' '):
            if part in self.stopwords:
                result=True
                break
        return result
    
    def check_composition(self,s):
          #split the string
        ws_parts=s.split(' ')
        past_str=''
        index_substr=0
        tuttoBene=True
        compositionVal=0
        for part in ws_parts:
            if part in self.stopwords:
                #no stopword at the beginning
                if index_substr==0 or index_substr+1==len(ws_parts):
                    tuttoBene=False
                    break
                else:
                    past_str=past_str.strip()
                    concept_val=self.concepts_inlinks.get(past_str)
                    if concept_val==None or len(past_str)==1:
                        tuttoBene=False
                        break;
                    else:
                        compositionVal+=int(concept_val)
                        past_str=''
            else:
                past_str=past_str+' '+part
                if index_substr+1==len(ws_parts):
                    past_str=past_str.strip()
                    concept_val=self.concepts_inlinks.get(past_str.strip())
                    if concept_val==None or len(past_str)==1:
                        tuttoBene=False
                        break;
                    else:
                        compositionVal+=int(concept_val)
                        past_str=''
            index_substr+=1
        if tuttoBene==True:
            return compositionVal
        else:
            return 0
        
        

    def process_substr(self,i,results):
        #get the length of the array to generate the substrings
        index=len(self.ws_array)-1
        left_position=self.ws_array[i]
        while index>i:
            # position of the right part to get the substring 
            right_position=self.ws_array[index]+1
            s=self.text[left_position:right_position]
            #trim
            s=s.strip()
            # check if the substring has inlinks
            val=self.concepts_inlinks.get(s)
            if val:
                logging.debug("Substring: '%s'" % s)
                logging.debug("Has inlinks: '%s'" % val.strip())
            composition=False
            #check composition of concepts
            if val==None and self.composition==True:
                aux_val=self.check_composition(s)
                #if all ok, set the compositionVal to the vala
                if aux_val!=0:
                    composition=True
                    val=aux_val
            #check the concept
            if s in self.stopwords:
                logging.debug("%s is a stopword" % s)
            if val!=None and s not in self.stopwords and int(val)>=self.inlink_threeshold and self.no_all_sw(s) and len(s)>1:
                logging.debug("Concept not filtered: '%s'" % s)
                self.left.append(left_position)
                self.right.append(right_position)
                is_entity=False
                results[s]={'inlinks':int(val),'start':left_position+1,'end':right_position,'composition':composition}
            
            index-=1
            
            
    def eliminate_duplicates(self,results):
        keys=[]
        
        # get the keys values
        for k,v in results.items():
            if v['composition']==False:
                keys.append(k)
        # sort the list by length    
        keys.sort(key = len)
    
        # check if the smaller keys are contained in the greater keys
        i=0
        while i<len(keys):
            j=i+1
            while j<len(keys):
                if keys[i] in keys[j]:
                    #contained, so remove it
                    results.pop(keys[i])
                    break
                j+=1
            i+=1
    
        
    def process(self):
        i=0
        start = time.time()
        results={}
        # get smaller substrings in each iteration and process it looking the inlinks hashmap and 
        # do a soft check to ensure is not contained in the previous results
        while i<len(self.ws_array):
            self.process_substr(i,results)
            i+=1
        logging.debug("Pre eliminate duplicates: Results:'%s'" % results)
        # eliminates duplicates
        self.eliminate_duplicates(results)
        res={'results':results}
        res['text']=self.text
        res['elapsed_time']=time.time() - start
        logging.debug("Entities: '%s'" % res['results'].keys())
        #return json.dumps(res)
        return res        
        
        
        

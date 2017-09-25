# RTB-ipinyou
This repository contains the code of the paper "An Optimal Budget Management Framework for Real Time Bidding in Online Advertising" 
and other baseline models.
 
Requirements:
===================           
System: Linux                                                                                                                      
python3.5                                                                                                                       
libffm: https://github.com/guestwalk/libffm                       
libfm：http://www.libfm.org/                                                                                                
Vowpal Wabbit：http://hunch.net/~vw/                                                
sklearn                   
matplotlib                            
csv                         


How to Use
====================                
For simplicity, we use iPinYou dataset at make-ipinyou-data https://github.com/wnzhang/make-ipinyou-data.                  
Follow the instructions and update the soft link data:         
XXX/RTB$:ln -sfn XXX/make-ipinyou-data/1458 data                                                    
or just copy the train.log.txt of an advertiser here

run a demo:               
cd src                          
python3 demo.py            


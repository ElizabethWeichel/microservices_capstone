#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 08:35:28 2023

@author: lizzieweichel
"""
with open('top_pyits.txt') as f:
    lines=f.readlines()

#for line in lines:
#    line.strip()
#print(line)

print(lines[1][24:28])

mysum=0
for i in range(0, len(lines)):
    mysum+=float(lines[i][24:28])

avg=mysum/len(lines)
print(avg)
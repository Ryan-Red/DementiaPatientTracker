import requests
import socket

import time
import numpy
from numpy import sqrt,dot,cross
from numpy.linalg import norm

sock = socket.socket()
sock.connect(("IP",PORT))

def getRoomFromCoordinates(coords):
   return 1
   ##Get the room Coordinates and compare it to the given coordinate

def associate(macID):
    #Example: ["macID",x,y,z]
    macIDToXYZ = []
    for i in range(0,len(macIDToXYZ),1):
       if macID == macIDToXYZ[i][0]:
          return [macIDToXYZ[i][1],macIDToXYZ[i][2],macIDToXYZ[i][3]]     

    return []

def legality(coords, legalZone):
   if coords[0] <= xBoundary and coords[1] <= yBoundary:
      return True
     
   if coords[0] >= legalZone[0][0]:
       if coords[0] <= legalZone[0][1]:
           if coords[1] >= legalZone[1][0]:
               if coords[1] <= legalZone[1][1]:
                   if coords[2] >= legalZone[2][0]:
                       if coords[2] <= legalZone[2][1]:
                           return True

   return False
    

def trilaterate(P1,P2,P3,r1,r2,r3):                      
    temp1 = P2-P1                                        
    e_x = temp1/norm(temp1)                              
    temp2 = P3-P1                                        
    i = dot(e_x,temp2)                                   
    temp3 = temp2 - i*e_x                                
    e_y = temp3/norm(temp3)                              
    e_z = cross(e_x,e_y)                                 
    d = norm(P2-P1)                                      
    j = dot(e_y,temp2)                                   
    x = (r1*r1 - r2*r2 + d*d) / (2*d)                    
    y = (r1*r1 - r3*r3 -2*i*x + i*i + j*j) / (2*j)       
    temp4 = r1*r1 - x*x - y*y                            
    if temp4<0:
        return []
    z = sqrt(temp4)                                      
    p_12_a = P1 + x*e_x + y*e_y + z*e_z                  
    p_12_b = P1 + x*e_x + y*e_y - z*e_z
    p_mid = 0.5*(p_12_a + p_12_b)
    return p_mid    



TheRequest = None
split = []
average = numpy.array([0,0,0])
n = 0

for i in range(0,10,1):
    TheRequest = requests.get("IP")
    split = (TheRequest.text).split(",")
    split = split[1:len(split)-1]
    SSID = []
    Strength = []
    macID =[]
    distance = []
    print(split)
    for i in range(0,len(split),1):
        if i % 4 == 0:
            SSID = SSID + [split[i]]
        elif i%4 == 1:
            Strength = Strength + [(float)(split[i])]
        if i%4 == 2:
            macID = macID + [split[i]]
        elif i%4 == 3:
            distance = distance + [(float)(split[i])]
        
    count = 0
    coordList = []
    coordIdx = []
    coordAccum = []
    coordIdxAccum = []
    for j in range(0,len(macID),1):
       for i in range(j,len(macID)+j,1):
           if i >= len(macID):
              newI = i- len(macID)
           else:
              newI = i
           if len(coordIdx) == 3:
              break
      
           coords = associate(macID[newI])
           if coords != []:
               coordIdx += [newI]
               coordList = coordList + [coords]
     
       coordAccum = coordAccum + [coordList]
       coordIdxAccum = coordIdxAccum + [coordIdx]
       coordList = []
       coordIdx = []
        
    distList = []
    distListAccum = []
    for ele in coordAccum:
       for i in coordIdxAccum:
           for j in range(0,len(i),1):
              
              distList = distList + [distance[i[j]]]
           distListAccum = distListAccum + [distList]
           distList = []

    print(SSID)
    print(Strength)
    print(macID)
    print(distance)
   
    print(coordAccum)

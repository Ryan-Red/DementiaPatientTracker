import requests
import socket

import time
import numpy
from numpy import sqrt,dot,cross
from numpy.linalg import norm

sock = socket.socket()
sock.connect(("24.114.75.10",3000))

def getRoomFromCoordinates(coords):
   return 1
   ##Get the room Coordinates and compare it to the given coordinate

def associate(macID):
    #Floor 27 macIDToXYZ = [["96:00:81:12:F4:8B",2,2,2],["46:91:60:9B:7E:32",0,0,0],["96:00:41:12:F3:B9",2,4,4],
    #              ["96:00:41:12:F3:B9",4,6,7],["56:02:81:32:BA:2A",1,-15,-4],["56:02:81:32:B9:84",-10,1,-4],
    #              ["2A:74:02:D0:AF:CA",-1,0,0],["56:01:41:3F:08:06",2,-46,-5],["56:02:81:3F:08:A8",5,-55,-5]]
    #IDK where this works, probably at home macIDToXYZ = [["1A:90:D8:C7:84:0F",0,1,0],["18:90:D8:C7:83:0E",0,0,0],
    #["88:36:6C:3D:B0:A0",4,-160,-1],["A8:4E:3F:48:9C:88",-202,5,2],["A8:9A:93:F9:C0:C6",-200,6,2],["30:B7:D4:BB:35:68",216,5,0]]
    macIDToXYZ = [["56:02:81:3F:05:F6",1,120,3],["46:91:60:9B:7E:32",0,0,0],["46:91:60:9B:7E:32",10,100,20],
                  ["10:62:E5:37:61:EE",0,20,4],["56:02:81:3F:05:F6",-3,40,5],["2A:74:02:D0:AF:CA",1,2,1.5],
                  ["56:02:81:32:B6:08",10,155,-10]]
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
        print("yeet")
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
    TheRequest = requests.get("http://192.168.43.156/Info")
    #print(TheRequest.text)
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
    for j in range(0,len(coordAccum),1):
       if len(coordAccum[j]) > 2:
          P1 = numpy.array(coordAccum[j][0])
          P2 = numpy.array(coordAccum[j][1])
          P3 = numpy.array(coordAccum[j][2])
          R1 = distListAccum[j][0]
          R2 = distListAccum[j][1]
          R3 = distListAccum[j][2]

          points = trilaterate(P1,P2,P3,R1,R2,R3)
          if points != [] and numpy.isnan(points.any()) == False:
             average = average + points
             print("added to average")
             n +=1
             average = average/n
             print("Average is of", average)

             
          #print("Points are of",points)
           
          # if points[0][2] < points[1][2]:
          #    TrueVal = points[0]
          # else:
          #    TrueVal = points[1]
        
           #if legality(TrueVal,legalZone) == True:
           #    continue
           #else:
#string = "ID " + idNumber + " Is in room number: " + getRoomFromCoordinates(TrueVal) 
string = str(average)
socket.emit("/ret",string)


print(average)

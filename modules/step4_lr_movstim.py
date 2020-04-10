# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 11:42:54 2019

@author: mathilde.josserand
"""
import numpy as np
import sys
import math
import cv2
import random

#Rotate a point counterclockwise by a given angle (in radians) around a given origin      
def rotate(originx, originy, pointx, pointy, angle):
    qx = originx + math.cos(angle) * (pointx - originx) - math.sin(angle) * (pointy - originy)
    qy = originy + math.sin(angle) * (pointx - originx) + math.cos(angle) * (pointy - originy)
    return qx, qy

# find slope between two points
def slope(x1, y1, x2, y2): 
    return (y2-y1)/(x2-x1)    
    
def yintercept(x, y, m):
    return y - m * x

# compute visual fields in the left side
def visual_fields_left(txtFile, final4, asym):
    
    # find stim according to conditions
    if (asym==False) :
        stim = final4["stimy"]
    if (asym==True):
        stim = final4["stimlefty"]
    
    # Give name to variable to make the next step easier to read and understand :    
    frontalR = final4["interceptfrontalRleft"]
    frontalL = final4["interceptfrontalLleft"]
    blindR = final4["interceptblindRleft"]
    blindL = final4["interceptblindLleft"]
    middle = final4['interceptmiddleleft']
    
    # SPECIAL CASE : only frontal    
    final4['frontalleft'] = np.where( ((np.isnan(frontalL)==True) & (np.isnan(frontalR)==False) & (frontalR<stim)) | ((np.isnan(frontalR)==True) & (np.isnan(frontalL)==False) & (frontalL > stim)) | ((np.isnan(frontalR)==False) & (np.isnan(frontalL)==False) & (frontalL>stim) & (frontalR<stim)), 1, final4['frontalleft'])

    # SPECIAL CASE : only blind     
    final4['blindleft'] = np.where( (((np.isnan(blindL)==True) & (np.isnan(blindR)==False) & (blindR>stim)) | ((np.isnan(blindR)==True) & (np.isnan(blindL)==False) & (blindL<stim)) | ((np.isnan(blindR)==False) & (np.isnan(blindL)==False) & (blindR>stim) & (blindL<stim))), 1, final4['blindleft'])

    # SPECIAL CASE : only lateral-right           
    final4['lateralRightleft'] = np.where( ((np.isnan(blindR)== False) & (blindR<stim) & ((frontalR>stim)|(np.isnan(frontalR)== True))) | ((np.isnan(frontalR)== False) & (frontalR>stim) & ((blindR<stim)|(np.isnan(blindR)== True))), 1, final4['lateralRightleft'])
    
    # SPECIAL CASE : only lateral-left                 
    final4['lateralLeftleft'] = np.where( ((np.isnan(blindL)== False) & (blindL>stim) & ((frontalL<stim)|(np.isnan(frontalL)== True))) | ((np.isnan(frontalL)== False) & (frontalL<stim) & ((blindL>stim)|(np.isnan(blindL)== True))), 1, final4['lateralLeftleft'])

    # check if error : if not, this column is supposed to be always equal to 1
    final4['sumallleft']= final4['blindleft'] + final4['frontalleft'] + final4['lateralRightleft'] + final4['lateralLeftleft']
    
    # lateral without frontal
    final4['LeftALLleft']  = np.where( ((np.isnan(middle) == False) & (middle<stim) & (final4['blindleft']!=1)) | ((np.isnan(middle) == True) & (np.isnan(blindL) == False) & (blindL>stim)), 1, final4['LeftALLleft'])
    final4['RightALLleft']  = np.where( ((np.isnan(middle) == False) & (middle>stim) & (final4['blindleft']!=1)) | ((np.isnan(middle) == True) & (np.isnan(blindR) == False) & (blindR<stim)), 1, final4['RightALLleft'])
    
    return final4

# compute visual fields in the right side
def visual_fields_right(txtFile, final4, asym):
      
    # find stim according to conditions
    if (asym==False) :
        stim = final4["stimy"]
    if (asym==True):
        stim = final4["stimrighty"]
    
    # Give name to variable to make the next step easier to read and understand :
    frontalR = final4["interceptfrontalRright"]
    frontalL = final4["interceptfrontalLright"]
    blindR = final4["interceptblindRright"]
    blindL = final4["interceptblindLright"]
    middle = final4['interceptmiddleright']
    
    # SPECIAL CASE : only frontal    
    final4['frontalright'] = np.where( ((np.isnan(frontalL)==True) & (np.isnan(frontalR)==False) & (frontalR>stim)) | ((np.isnan(frontalR)==True) & (np.isnan(frontalL)==False) & (frontalL<stim)) | ((np.isnan(frontalR)==False) & (np.isnan(frontalL)==False) & (frontalL<stim) & (frontalR>stim)), 1, final4['frontalright'])

    # SPECIAL CASE : only blind     
    final4['blindright'] = np.where( ((np.isnan(blindL)==True) & (np.isnan(blindR)==False) & (blindR<stim)) | ((np.isnan(blindR)==True) & (np.isnan(blindL)==False) & (blindL > stim)) | ((np.isnan(blindR)==False) & (np.isnan(blindL)==False) & (blindL>stim) & (blindR<stim)), 1, final4['blindright'])

    # SPECIAL CASE : only lateral-right           
    final4['lateralRightright'] = np.where( ((np.isnan(frontalR)== False) & (frontalR<stim) & ((blindR>stim)|(np.isnan(blindR)== True))) | ((np.isnan(blindR)== False) & (blindR>stim) & ((frontalR<stim)|(np.isnan(frontalR)== True))), 1, final4['lateralRightright'])
    
    # SPECIAL CASE : only lateral-left                 
    final4['lateralLeftright'] = np.where( ((np.isnan(frontalL)== False) & (frontalL>stim) & ((blindL<stim)|(np.isnan(blindL)== True))) | ((np.isnan(blindL)== False) & (blindL<stim) & ((frontalL>stim)|(np.isnan(frontalL)== True))), 1, final4['lateralLeftright'])
  
    # check if error : if not, this column is supposed to be always equal to 1
    final4['sumallright']= final4['blindright'] + final4['frontalright'] + final4['lateralRightright'] + final4['lateralLeftright']
    
    # lateral without frontal
    final4['RightALLright']  = np.where( ((np.isnan(middle) == False) &  (middle<stim) & (final4['blindright']!=1)) | ((np.isnan(middle) == True) & (np.isnan(blindR) == False) & (blindR>stim)), 1, final4['RightALLright'])
    final4['LeftALLright']  = np.where( ((np.isnan(middle) == False) & (middle>stim) & (final4['blindright']!=1))| ((np.isnan(middle) == True) & (np.isnan(blindL) == False) & (blindL<stim)), 1, final4['LeftALLright'])
    
    return final4



## create data points to determinate visual fields
def create_visual_fields(txtFile, final4, frontalangle, lateralangle, cap, numbframes, asym, problem) :    
    import interface
    ## create data points to determinate visual fields
    # create column for point between the eyes : x and y
    final4['betweeneyesX'] = (final4['leftheadx'] + final4['rightheadx'])/2
    final4['betweeneyesY'] = (final4['leftheady'] + final4['rightheady'])/2
    
    #rotate point created with 16.5 degrees difference (binoc vision)
    final4['frontalRX'], final4['frontalRY'] = rotate(final4['betweeneyesX'], final4['betweeneyesY'], final4['topheadx'], final4['topheady'], math.radians(frontalangle))
    final4['frontalLX'], final4['frontalLY'] = rotate(final4['betweeneyesX'], final4['betweeneyesY'], final4['topheadx'], final4['topheady'], math.radians(-frontalangle))
    
    #rotate point created with 27 degrees difference (blind vision)
    final4['blindRX'], final4['blindRY'] = rotate(final4['betweeneyesX'], final4['betweeneyesY'], final4['topheadx'], final4['topheady'],  math.radians(lateralangle))
    final4['blindLX'], final4['blindLY'] = rotate(final4['betweeneyesX'], final4['betweeneyesY'], final4['topheadx'], final4['topheady'],  math.radians(-lateralangle))

    #straight line between-the-eyes-point and top head y
    final4['m'] = slope(final4['topheadx'], final4['topheady'], final4['betweeneyesX'], final4['betweeneyesY'])
    final4['c'] = yintercept(final4['betweeneyesX'], final4['betweeneyesY'], final4['m'])  
    final4['interceptmiddleleft'] = np.where((final4['topheadx']<final4['betweeneyesX']), (final4['m']*txtFile.leftborder[0] + final4['c']),  np.NaN)
    final4['interceptmiddleright'] = np.where((final4['topheadx']>final4['betweeneyesX']), (final4['m']*txtFile.rightborder[0] + final4['c']), np.NaN)
    
    #straight line between-the-eyes-point and FRONTAL-vision-RIGHT point
    final4['m'] = slope(final4['frontalRX'], final4['frontalRY'], final4['betweeneyesX'], final4['betweeneyesY'])
    final4['c'] = yintercept(final4['betweeneyesX'], final4['betweeneyesY'], final4['m'])  
    final4['interceptfrontalRleft'] = np.where((final4['frontalRX']<final4['betweeneyesX']), (final4['m']*txtFile.leftborder[0] + final4['c']),  np.NaN)
    final4['interceptfrontalRright'] = np.where((final4['frontalRX']>final4['betweeneyesX']), (final4['m']*txtFile.rightborder[0] + final4['c']), np.NaN)
    
    #straight line between-the-eyes-point and FRONTAL-vision-LEFT point
    final4['m'] = slope(final4['frontalLX'], final4['frontalLY'], final4['betweeneyesX'], final4['betweeneyesY'])
    final4['c'] = yintercept(final4['betweeneyesX'], final4['betweeneyesY'], final4['m'])      
    final4['interceptfrontalLleft'] = np.where((final4['frontalLX']<final4['betweeneyesX']), (final4['m']*txtFile.leftborder[0] + final4['c']), np.NaN)
    final4['interceptfrontalLright'] = np.where((final4['frontalLX']>final4['betweeneyesX']), (final4['m']*txtFile.rightborder[0] + final4['c']), np.NaN)
    
    #straight line between-the-eyes-point and BLIND-vision-RIGHT point
    final4['m'] = slope(final4['blindRX'], final4['blindRY'], final4['betweeneyesX'], final4['betweeneyesY'])
    final4['c'] = yintercept(final4['betweeneyesX'], final4['betweeneyesY'], final4['m'])     
    final4['interceptblindRleft'] = np.where((final4['blindRX']<final4['betweeneyesX']), (final4['m']*txtFile.leftborder[0] + final4['c']), np.NaN)
    final4['interceptblindRright'] = np.where((final4['blindRX']>final4['betweeneyesX']), (final4['m']*txtFile.rightborder[0] + final4['c']), np.NaN)
    
    #straight line between-the-eyes-point and BLIND-vision-LEFT point
    final4['m'] = slope(final4['blindLX'], final4['blindLY'], final4['betweeneyesX'], final4['betweeneyesY'])
    final4['c'] = yintercept(final4['betweeneyesX'], final4['betweeneyesY'], final4['m'])      
    final4['interceptblindLleft'] = np.where((final4['blindLX']<final4['betweeneyesX']), (final4['m']*txtFile.leftborder[0] + final4['c']), np.NaN)
    final4['interceptblindLright'] = np.where((final4['blindLX']>final4['betweeneyesX']), (final4['m']*txtFile.rightborder[0] + final4['c']), np.NaN)
    
    
    # find visual fields for BOTTOM #
    final4['frontalleft'] = 0
    final4['blindleft']  = 0
    final4['lateralLeftleft']  = 0
    final4['lateralRightleft']  = 0  
    final4['LeftALLleft']  = 0
    final4['RightALLleft']  = 0  
    final4 = visual_fields_left(txtFile, final4, asym)

    # find visual fields for TOP #
    final4['frontalright'] = 0
    final4['blindright']  = 0
    final4['lateralLeftright']  = 0
    final4['lateralRightright']  = 0
    final4['LeftALLright']  = 0
    final4['RightALLright']  = 0
    final4 = visual_fields_right(txtFile, final4, asym)
    
 
    # VISUALIZE 
    
    # copy table (useful if problem == True)
    finalgood = final4.copy()
    
    # ask user if he wants to visualize
    response = interface.visualize_fields_q1()

    
    if response == 'y':
        
        # if problem == True, reduced all dimensions by 2
        if problem == True :
            final4.iloc[:,2:final4.columns.get_loc("frontalleft")] = final4.iloc[:,:final4.columns.get_loc("frontalleft")]/2
            txtFile.iloc[:,8:] = txtFile.iloc[:,8:]/2
        
        # ask user to select the number of random frames
        numbpic = interface.visualize_fields_q2()  
        
        # numbpic random frames selected
        randompic = random.sample(range(int(final4.frame_number[0]),int(final4.frame_number[-1:])), numbpic)

        # visualize for all frames        
        for picnum in randompic :
            indexpic = picnum - txtFile.startingframe[0] 
            cap.set(1,picnum); 
            ret, frame = cap.read() 
            
            # print text in each frame
            textprint=list() 
            textprint2=list() 
            for el in range(final4.columns.get_loc("frontalleft"), final4.columns.get_loc("sumallleft")):
                if final4.iloc[indexpic, el] != 0:
                    textprint.append(final4.columns[el][:-4] + ' ' + str(round(final4.iloc[indexpic, el],3)))
            for el in range(final4.columns.get_loc("frontalright"), final4.columns.get_loc("sumallright")):
                if final4.iloc[indexpic, el] != 0:
                    textprint2.append(final4.columns[el][:-5] + ' ' + str(round(final4.iloc[indexpic, el],3)))
                    
            lengthArena = txtFile.rightborder[0] - txtFile.leftborder[0]
            for i in range(0,len(textprint)):
                starttextpoint1 = txtFile.leftborder[0] + lengthArena/10
                cv2.putText(frame, textprint[i], (int(starttextpoint1),150+i*30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250),1)
            for i in range(0,len(textprint2)): 
                starttextpoint2 = txtFile.leftborder[0] + 7*lengthArena/10
                cv2.putText(frame, textprint2[i], (int(starttextpoint2),150+i*30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250),1)
            
            cv2.putText(frame, 'index'+str(indexpic), (200,400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250),1)
             
             # print visual fields
            if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRleft")])== False:
                cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(txtFile.leftborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRleft")])),(0,0,255),2)
            if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRright")])== False:
                cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(txtFile.rightborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRright")])),(0,0,255),2)
            if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLleft")])== False:
                cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(txtFile.leftborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLleft")])),(0,0,255),2)        
            if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLright")])== False:
                cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(txtFile.rightborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLright")])),(0,0,255),2)
            if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRleft")])== False:
                cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(txtFile.leftborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRleft")])),(255,0,0),2)
            if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRright")])== False:
                cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(txtFile.rightborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRright")])),(255,0,0),2)
            if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLleft")])== False:
                cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(txtFile.leftborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLleft")])),(255,0,0),2)
            if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLright")])== False:
                cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(txtFile.rightborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLright")])),(255,0,0),2)
            if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddleleft")])== False:
                cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(txtFile.leftborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddleleft")])),(0,255,0),2)
            if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddleright")])== False:
                cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(txtFile.rightborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddleright")])),(0,255,0),2)
            
            # print stimuli
            if asym == False :
                if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("stimy")])== False:
                    cv2.circle(frame, (int(txtFile.leftborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("stimy")])), 3, (0,255,0), -1)
                    cv2.circle(frame, (int(txtFile.rightborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("stimy")])), 3, (100,150,0), -1)
            if asym == True :
                 if (math.isnan(final4.iloc[indexpic, final4.columns.get_loc("stimlefty")]) & (math.isnan(final4.iloc[indexpic, final4.columns.get_loc("stimrighty")])) )== False:
                    cv2.circle(frame, (int(txtFile.leftborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("stimlefty")])), 3, (0,255,0), -1)
                    cv2.circle(frame, (int(txtFile.rightborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("stimrighty")])), 3, (100,150,0), -1)
           
            # show frame on window
            cv2.imshow('Random_pictures', frame)
            
            # press any keyboard key to go to the next image
            cv2.waitKey(0)
            cv2.destroyAllWindows
        
    #cv2.destroyWindow('Random_pictures')  
    
    # if group by seconds, divide the results by the framerate            
    finalgood['frontalleft'] = finalgood['frontalleft']/ numbframes
    finalgood['blindleft']  = finalgood['blindleft']/ numbframes
    finalgood['lateralLeftleft']  =  finalgood['lateralLeftleft']/ numbframes
    finalgood['lateralRightleft']  = finalgood['lateralRightleft'] / numbframes
    finalgood['LeftALLleft']  = finalgood['LeftALLleft']/ numbframes
    finalgood['RightALLleft']  = finalgood['RightALLleft'] / numbframes
    finalgood['frontalright'] = finalgood['frontalright']/ numbframes
    finalgood['blindright']  = finalgood['blindright']/ numbframes
    finalgood['lateralLeftright']  = finalgood['lateralLeftright']/ numbframes
    finalgood['lateralRightright']  = finalgood['lateralRightright']/ numbframes
    finalgood['LeftALLright']  = finalgood['LeftALLright']/ numbframes
    finalgood['RightALLright']  = finalgood['RightALLright']/ numbframes
    
    # aks user if he wants to continue
    resp = interface.visualize_fields_q3()
    
    # if no, exit system
    if resp == 'n':
        sys.exit()
    
    return finalgood
    
        



## If you want to check a specific frame, write in indexpic the index of the frame you want to visualize, uncomment and run this part
## to run this part, you have to run main_coordinator and answer no to 'Do you want to continue ?' question        
#        
#        problem = True
#        if problem == True :
#           
#            final4.iloc[:,2:final4.columns.get_loc("interceptblindLright")] = final4.iloc[:,:final4.columns.get_loc("interceptblindLright")]/2
#            txtFile.iloc[:,8:] = txtFile.iloc[:,8:]/2
#    ####### STEP 5 : compute visual fields
#            cap = cv2.VideoCapture(pathvideo + animal_type + '%sbadversion.avi' %ID )
#        
#      
#        indexpic = 2363
#        picnum = indexpic + txtFile.startingframe[0] 
#        
#        cap.set(1,picnum); 
#        ret, frame = cap.read() 
#
#        import math
#        # print text in each frames
#        textprint=list() 
#        textprint2=list() 
#        #textprint.append('index' + str(indexpic))
#        for el in range(final4.columns.get_loc("frontalleft"), final4.columns.get_loc("sumallleft")):
#            if final4.iloc[indexpic, el] != 0:
#                textprint.append(final4.columns[el][:-4] + ' ' + str(round(final4.iloc[indexpic, el],3)))
#        for el in range(final4.columns.get_loc("frontalright"), final4.columns.get_loc("sumallright")):
#            if final4.iloc[indexpic, el] != 0:
#                textprint2.append(final4.columns[el][:-5] + ' ' + str(round(final4.iloc[indexpic, el],3)))
#    
#
#        lengthArena = txtFile.rightborder[0] - txtFile.leftborder[0]
#        for i in range(0,len(textprint)):
#            starttextpoint1 = txtFile.leftborder[0] + lengthArena/20
#            cv2.putText(frame, textprint[i], (int(starttextpoint1),150+i*30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250),1)
#        for i in range(0,len(textprint2)): 
#            starttextpoint2 = txtFile.leftborder[0] + 7*lengthArena/20
#            cv2.putText(frame, textprint2[i], (int(starttextpoint2),150+i*30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250),1)
#        
#        # print visual fields
#        if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRleft")])== False:
#            cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(txtFile.leftborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRleft")])),(0,0,255),2)
#        if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRright")])== False:
#            cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(txtFile.rightborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalRright")])),(0,100,255),2)
#        if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLleft")])== False:
#            cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(txtFile.leftborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLleft")])),(0,100,255),2)        
#        if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLright")])== False:
#            cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(txtFile.rightborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("interceptfrontalLright")])),(0,0,255),2)
#        if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRleft")])== False:
#            cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(txtFile.leftborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRleft")])),(255,0,0),2)
#        if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRright")])== False:
#            cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(txtFile.rightborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindRright")])),(255,100,0),2)
#        if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLleft")])== False:
#            cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(txtFile.leftborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLleft")])),(255,100,0),2)
#        if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLright")])== False:
#            cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(txtFile.rightborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("interceptblindLright")])),(255,0,0),2)
#        if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddleleft")])== False:
#            cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(txtFile.leftborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddleleft")])),(255,100,0),2)
#        if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddleright")])== False:
#            cv2.line(frame,(int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]), int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])),(int(txtFile.rightborder[0]), int(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddleright")])),(255,0,0),2)
#        
#        if math.isnan(final4.iloc[indexpic, final4.columns.get_loc("stimy")])== False:
#            cv2.circle(frame, (int(txtFile.leftborder[0]), int(final4.stimy[indexpic])), 3, (0,255,0), -1)
#            cv2.circle(frame, (int(txtFile.rightborder[0]), int(final4.stimy[indexpic])), 3, (100,150,0), -1)
#
#        cv2.imshow('great_window', frame)
#        cv2.waitKey(0)
#        cv2.destroyAllWindows
#
#        cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("leftheadx")]),int(final4.iloc[indexpic, final4.columns.get_loc("leftheady")])), 3, (255,255,255), -1)
#        cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("rightheadx")]),int(final4.iloc[indexpic, final4.columns.get_loc("rightheady")])), 3, (255,255,255), -1)
#        cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("topheadx")]),int(final4.iloc[indexpic, final4.columns.get_loc("topheady")])), 3, (255,255,255), -1)
#    
#        cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesX")]),int(final4.iloc[indexpic, final4.columns.get_loc("betweeneyesY")])), 3, (0,255,0), -1)
#        cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("frontalRX")]),int(final4.iloc[indexpic, final4.columns.get_loc("frontalRY")])), 3, (255,0,0), -1)
#        cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("frontalLX")]),int(final4.iloc[indexpic, final4.columns.get_loc("frontalLY")])), 3, (255,100,0), -1)
#        cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("blindRX")]),int(final4.iloc[indexpic, final4.columns.get_loc("blindRY")])), 3, (0,100,255), -1)
#        cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("blindLX")]),int(final4.iloc[indexpic, final4.columns.get_loc("blindLY")])), 3, (0,0,255), -1)
#    
#
#        
#        cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("interceptmiddletop")]),int(txtFile.topborder[0])), 3, (0,100,255), -1)
#        cv2.circle(frame, (int(final4.iloc[indexpic, final4.columns.get_loc("blindLX")]),int(final4.iloc[indexpic, final4.columns.get_loc("blindLY")])), 3, (0,0,255), -1)
#
#        
#        # show frame on window
#        cv2.imshow('great_window', frame)
##                

#biomotion serial dependence experiment
#one target walker followed by a noise mask followed by a single walker method of adjustment task

from psychopy import visual, core, event, data, gui, monitors #import some libraries from PsychoPy
import numpy as np
import random
from pyglet.window import key
import csv

mywin = visual.Window([1600,900],monitor='HomeMonitor', units="deg",color=(-1,-1,-1),fullscr=1) #create a window


info = {'Observer':'WC3','L or R':'L'}
#Parameters
fixPos = [0,0]
if info['L or R'] == "R":
    targetExc = [6,0]
elif info['L or R'] == "L":
    targetExc = [-6,0]


trialDur = 60    #Durations in frames
maskDur = 30
iti = 0.5                   #mean InterTrialInterval in seconds
nTrials = 100
targetorientations = np.random.randint(180,size=nTrials)


#Calculations
targetPos = np.add(fixPos,targetExc)

#load all textures
all_walkers = [[] for x in xrange(180)]
for i in xrange(180):
    for j in xrange(60):
        all_walkers[i].append(visual.ImageStim(win=mywin, image='walker - {0} - {1}.png'.format(i,j), size = [3,3],pos=targetPos))
        all_walkers[i][j].draw()

#Trial Handler
conditions = []
for targetOrientation in targetorientations:
	conditions.append(
		{ 'targetOrientation':targetOrientation}
		)

trials = data.TrialHandler(conditions,1, method = 'sequential')
trials.data.addDataType('response')

#create some stimuli
fixation = visual.PatchStim(win=mywin, size=0.2, mask = 'circle', pos=fixPos, sf=0)
fixation.setAutoDraw(True)
RTClock = core.Clock()

responses = []
#TrialLoop
for thisTrial in trials:
    target = []
    for k in range(60):
        target.append(visual.ImageStim(win=mywin, image='walker - {0} - {1}.png'.format(thisTrial.targetOrientation,k), size = [3,3],pos=targetPos))
    mask_array = np.random.randint(2,size=(64,64))*2-1
    mask = visual.PatchStim(win=mywin,tex=mask_array,size = [3,4],pos=targetPos)
    #frame loops
    for frame in range(trialDur):
        fixation.draw()
        target[np.mod(frame,60)].draw()
        mywin.flip()    
    for frame in range(maskDur):
        mask.draw()
        fixation.draw()
        mywin.flip()
    fixation.draw()
    mywin.flip()
    RTClock.reset()


    thisResp = None
    keyState=key.KeyStateHandler()
    resp_ori = np.random.randint(180)
    k = np.random.randint(60)
    mywin.winHandle.push_handlers(keyState)
    all_walkers[resp_ori][k].draw()
    while 1:
        k += 1
        k = k%60
        
        if keyState[key.LEFT]:
            resp_ori -= 1
        if keyState[key.RIGHT]:
            resp_ori += 1
        if keyState[key.SPACE]:
            thisResp = resp_ori%180
            responses.append(thisResp)
            break
        elif keyState[key.ESCAPE]:
            with open('motionsd_'+info['Observer'] +'.csv','wb') as csvfile:
                datawriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                datawriter.writerow(targetorientations)
                datawriter.writerow(responses)
            core.quit()
        resp_ori = resp_ori%180
        all_walkers[resp_ori][k].draw()
        mywin.flip()
        
    for frame in range(maskDur):
        mask.draw()
        fixation.draw()
        mywin.flip()
    fixation.draw()
    mywin.flip()
    core.wait(iti)



#save dataFile
with open('motionsd_'+info['Observer'] +'.csv','wb') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    datawriter.writerow(targetorientations)
    datawriter.writerow(responses)



#cleanup
mywin.close()
core.quit()
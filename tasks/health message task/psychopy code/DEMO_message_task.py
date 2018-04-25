#######################################
#
# MESSAGE TASK for Physical Activity 2
#
#

# Timings:
#   Disdaq    8 sec
#   Message   8 secq
#   Relevance rating  4 secq
#   Fixation  3 sec
#   Disdaq    8 sec
#
# trials    72 (36 PA + 36 Control)



# Import modules

import csv

from psychopy import visual, core, event, gui, data, sound, logging
import datetime

# parameters
useFullScreen = False

frame_rate = 60
message_dur = 8 * frame_rate
rating_dur = 4 * frame_rate
fixation_dur = 3 * frame_rate
disdaq_dur = 8 * frame_rate
button_labels = { 'b': 0, 'y': 1, 'g': 2, 'r': 3 }
button_labels = { '1': 0, '2': 1, '3': 2, '4': 3, 'space': 0 }
buttons = button_labels.keys()

instruct_dur = 8 * frame_rate

subj_id='DEMO'
log_filename = 'logs/%s.csv' % subj_id



run_data = {
    'Participant ID': subj_id,
    'Date': str(datetime.datetime.now()),
    'Description': 'Physical Activity 2 Project CNLab - Message Task'
}

# Define Stimulus 

# Set up window
win=visual.Window([1024,768], fullscr=useFullScreen, monitor='testMonitor', units='deg') 


ready_screen = visual.TextStim(win, text="Press space to continue", height=1.2)
fixation = visual.TextStim(win,text='+', height=3, color="#FFFFFF") # Cross Fixation

# message screen
#
#             IMAGE     
#
#            message

pictureStim = visual.ImageStim(win, pos=(0,6), size=(12.6,9.2) )
messageStim = visual.TextStim(win, text='', pos=(0,0), color="#FFFFFF", wrapWidth=20)

#  response screen
#
#           IMAGE
#
#        message 
#
#       rating scale

#     1       2       3       4
#   not                       relevant
#  relevant

rate1 = visual.TextStim(win,text='1', color="#FFFFFF", pos=(-8,-4))
rate2 = visual.TextStim(win,text='2', color="#FFFFFF", pos=(-3,-4))
rate3 = visual.TextStim(win,text='3', color="#FFFFFF", pos=(3,-4))
rate4 = visual.TextStim(win,text='4', color="#FFFFFF", pos=(8,-4))
ratingStim = [rate1, rate2, rate3, rate4]

anchor1 = visual.TextStim(win, text='Not\nrelevant', color="#FFFFFF", pos=(-8,-6))
anchor4 = visual.TextStim(win, text='Relevant', color="#FFFFFF", pos=(8,-6))



# instrcution screen
instruction_image = visual.SimpleImageStim(win,image="buttonpad.png",pos=(-1,-3.5))
instruction_text = visual.TextStim(win, height=1.3,color="#FFFFFF", 
        text="Use the buttons to indicate how relevant each statement is to you", 
        pos=(0,+5), wrapWidth=24)



# load messages from the CSV file into a list of dictonaries 
# with keys matching column headers:
# [ {'cond': 'activity', 
#        'theme': 'aging', 
#       'type': 'risk', 
#        'message': 'You are more likely ... etc'},
        

stimuli  = [i for i in csv.DictReader(open('stimuli.csv','rU')) if i['cond']=='control']

# set up trial handler
demo_num=2
trials = data.TrialHandler(stimuli[:demo_num], nReps=1, extraInfo=run_data, dataTypes=['stim_onset', 'resp_onset', 'rt'], method="random")

################
# setup logging #
log_file = logging.LogFile("logs/%s.log" % (subj_id),  level=logging.DATA, filemode="w")

globalClock = core.Clock()
logging.setDefaultClock(globalClock)



##############################

# 1. display ready screen and wait for 'T' to be sent to indicate scanner trigger


#ready_screen.draw()
#win.flip()
#event.waitKeys(keyList='space')

# reset globalClock
globalClock.reset()

# send START log event
logging.log(level=logging.DATA, msg='******* START (trigger from scanner) *******')



################ 
# SHOW INSTRUCTIONS
################ 

itext = '''
In this task you will see and listen to messages about activities in everyday living.

Then you will be asked to rate how relevant each statement is to you.

From 1 (Not relevant) to 4 (Relevant)
'''

instruction_text.setText(itext.strip())
instruction_text.draw()
win.flip()
event.waitKeys(keyList=('space'))



instruction_text.setText('Use the buttons to indicate how relevant each statement is to you')
instruction_image.draw()
instruction_text.draw()
win.flip()
event.waitKeys(keyList=('space'))






################
# MAIN LOOP 
# present trials

for tidx,trial in enumerate(trials):

    # ------------ FIXATION ------------
    # send FIXATION log event
    logging.log(level=logging.DATA, msg='FIXATION')
    # show fixation
    for frame in range(fixation_dur):
        fixation.draw()
        win.flip()

    trial_type = trial['type']
    theme = trial['theme']
    cond = trial['cond']
    image = "images/%s/%s_%s.png" % (cond, theme, trial_type)
    audio = "audio/%s_%s_%s.wav" % (theme, trial_type, cond)
    message = trial['message']
    
    pictureStim.setImage(image)
    messageStim.setText(message)
    
    message_audio = sound.Sound(audio)


    # send MESSAGE log event
    logging.log(level=logging.DATA, msg="MESSAGE: %s - %s - %s" % (cond, theme, trial_type))

    trials.addData('stim_onset', globalClock.getTime())

    # play sound file for message
    message_audio.play()
    # show mesage 
    for frame in range(message_dur):
        pictureStim.draw()
        messageStim.draw()
        win.flip()
    
    
    # send SHOW RATING log event
    logging.log(level=logging.DATA, msg="SHOW RATING")

    trials.addData('resp_onset', globalClock.getTime())

    if tidx % 2 == 0:
        event.waitKeys(keyList='space')


    # clear event buffer
    event.clearEvents()
    resp_onset = globalClock.getTime()
    # show rating and collect response 
    
    timer = core.Clock()
    timer.reset()
    space_pressed = False
    while (tidx % 2 != 0 and timer.getTime()<rating_dur/frame_rate) or (tidx % 2 == 0 and space_pressed==False):
    #for frame in range(rating_dur):
        pictureStim.draw()
        messageStim.draw()
        
        for rate_stim in ratingStim:
            rate_stim.draw()
        
        anchor1.draw()
        anchor4.draw()
        win.flip()
        

        # get key response
        resp = event.getKeys(keyList = buttons)
    
        if len(resp) > 0 : 
            resp_value = resp[0]
            if resp_value == 'space':
                space_pressed = True
                continue
            ratingStim[button_labels[resp_value]].setColor('red')
            
            # add response value to the trial handler logging
            trials.addData('resp',resp_value)
            trials.addData('rt', globalClock.getTime() - resp_onset)
            
            
        
    # reset rating number color
    for rate in ratingStim:
        rate.setColor('#FFFFFF')
   
 
    
    if tidx == demo_num-1:
        ready_screen.setText('Any questions?')
    else:
        ready_screen.setText('OK now try another')
    ready_screen.draw()
    win.flip()
    event.waitKeys(keyList=['space'])



# send END log event
logging.log(level=logging.DATA, msg='******* END *******')

# save the trial infomation from trial handler
trials.saveAsText(log_filename, delim=',', dataOut=('n', 'all_raw'))

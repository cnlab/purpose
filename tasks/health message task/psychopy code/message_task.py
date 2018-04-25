#######################################

#

# MESSAGE TASK for Physical Activity 2

#

#


# Timings:

#   

#   Message   8 secq

#   Relevance rating  4 secq

#   Fixation  3 sec (with 5 dispersed rest fixations of 12 secs)

#   

#

# trials    72 (36 PA + 36 Control)







# Import modules



import csv



from psychopy import visual, core, event, gui, data, sound, logging

import datetime

import random



# parameters

useFullScreen = True



frame_rate = 1

message_dur = 8 * frame_rate

rating_dur = 4 * frame_rate

fixation_dur = 3 * frame_rate

rest_dur = 12 * frame_rate

disdaq_dur = 8 * frame_rate

button_labels = { 'b': 0, 'y': 1, 'g': 2, 'r': 3 }

#button_labels = { '1': 0, '2': 1, '3': 2, '4': 3 }

buttons = button_labels.keys()



instruct_dur = 8 * frame_rate





# get subjID

subjDlg = gui.Dlg(title="Messages Task")

subjDlg.addField('Enter Subject ID:')

subjDlg.show()



if gui.OK:

    subj_id=subjDlg.data[0]

else:

    sys.exit()



log_filename = 'logs/%s.csv' % subj_id



run_data = {

    'Participant ID': subj_id,

    'Date': str(datetime.datetime.now()),

    'Description': 'Physical Activity 2 Project CNLab - Message Task'

}







# Set up window

win=visual.Window([1024,768], fullscr=useFullScreen, monitor='testMonitor', units='deg') 



# Define Stimulus 



ready_screen = visual.TextStim(win, text="Ready.....", height=1.5, color="#FFFFFF")

fixation = visual.TextStim(win,text='+', height=5, color="#FFFFFF") # Cross Fixation



# message screen

#

#             IMAGE

#

#            message



pictureStim = visual.ImageStim(win, pos=(0,6.5), size=(12.6,9.2) )

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

        pos=(0,+5))



# sound test stimuli

test_instructions = visual.TextStim(win, text='', pos=(0,4), height=1.2, wrapWidth=20)

test_message = visual.TextStim(win, text='Please listen to the message', pos=(0,2), height=1.2, color='#FFFFFF')

lower = visual.TextStim(win, text='Button 1 = Reduce volume', pos=(0,1))

higher = visual.TextStim(win, text='Button 2 = Increase volume', pos=(0,-1))

ok = visual.TextStim(win, text='Button 4 = Volume is good', pos=(0,-3))







# load messages from the CSV file into a list of dictonaries 

# with keys matching column headers:

# [ {'cond': 'activity', 

#        'theme': 'aging', 

#       'type': 'risk', 

#        'message': 'You are more likely ... etc'},

        



stimuli  = [i for i in csv.DictReader(open('stimuli.csv','rU'))]



# set up trial handler



runs = [ [], [] ]

for i in range(len(stimuli)):

    if i%2==0:

        runs[0].append(stimuli[i])

    else:

        runs[1].append(stimuli[i])



fixations = [[], []]



durs = [fixation_dur, fixation_dur, fixation_dur, rest_dur]



for r in (0,1):

    for j in range(6):

        random.shuffle(durs)

        fixations[r].append(fixation_dur)

        for d in durs:

            fixations[r].append(d)

            

#print fixations



################

# setup logging #

log_file = logging.LogFile("logs/%s.log" % (subj_id),  level=logging.DATA, filemode="w")



globalClock = core.Clock()

logging.setDefaultClock(globalClock)





def do_sound_test():

    timer = core.Clock()

    test_message_text = '''

Before you begin this task we want to play you some audio to test the volume. 



You will hear the same message three times. 



Please indicate whether you'd like the volume adjusted after each

    '''

    

    audio = 'audio/TEST.wav'

    message_audio = sound.Sound(audio)

    

    timer.reset()

    test_instructions.setText(test_message_text.strip())

    while timer.getTime()<8:

        test_instructions.draw()

        win.flip()

        

    for test in range(3):

        timer.reset()

        message_audio.play()

        while timer.getTime()<8:

            test_message.draw()

            win.flip()

            

        timer.reset()

        while timer.getTime()<4:        

            lower.draw()

            higher.draw()

            ok.draw()

            win.flip()

            

            resp = event.getKeys(keyList=('b','y', 'r'))

            if len(resp)>0:

                if resp[0]=='b':

                    lower.setColor('#FF0000')

                elif resp[0]=='y':

                    higher.setColor('#FF0000')

                else:

                    ok.setColor('#FF0000')

            

        for stim in [ok, lower, higher]:

            stim.setColor('#FFFFFF')

    

    test_message.setText("OK great! Now we'll begin the MESSAGE TASK...")

    timer.reset()

    while timer.getTime()<4:

        test_message.draw()

        win.flip()











def do_run(run_number, trials):



    timer = core.Clock()

    ##############################



    # 1. display ready screen and wait for 'T' to be sent to indicate scanner trigger





    ready_screen.draw()

    win.flip()

    event.waitKeys(keyList='t')



    # reset globalClock

    globalClock.reset()



    # send START log event

    logging.log(level=logging.DATA, msg='******* START (trigger from scanner) - run %i *******' % run_number)





    if run_number == 1:

        do_sound_test()



    ################ 

    # SHOW INSTRUCTIONS

    ################ 



    timer.reset()

    while timer.getTime() < instruct_dur:

    #for frame in range(instruct_dur):

        instruction_image.draw()

        instruction_text.draw()

        win.flip()



    while timer.getTime() < fixation_dur:

        #for frame in range(fixation_dur):

            fixation.draw()

            win.flip()



    ################

    # MAIN LOOP 

    # present trials



    for tidx, trial in enumerate(trials):

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

        timer.reset()

        while timer.getTime() < message_dur:

        #for frame in range(message_dur):

            pictureStim.draw()

            messageStim.draw()

            win.flip()

        

        

        # send SHOW RATING log event

        logging.log(level=logging.DATA, msg="SHOW RATING")



        trials.addData('resp_onset', globalClock.getTime())





        # clear event buffer

        event.clearEvents()

        resp_onset = globalClock.getTime()

        # show rating and collect response  

        timer.reset()

        while timer.getTime() < rating_dur:

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

                ratingStim[button_labels[resp_value]].setColor('red')

                

                # add response value to the trial handler logging

                trials.addData('resp',resp_value)

                trials.addData('rt', globalClock.getTime() - resp_onset)

                

                

            

        # reset rating number color

        for rate in ratingStim:

            rate.setColor('#FFFFFF')

       

        # ------------ FIXATION ------------

        # send FIXATION log event

        logging.log(level=logging.DATA, msg='FIXATION')

        # show fixation

        timer.reset()

        fixation_for_trial = fixations[run_number-1][tidx]

        while timer.getTime() < fixation_for_trial:

        #for frame in range(fixation_dur):

            fixation.draw()

            win.flip()

            





    # write logs



    # send END log event

    logging.log(level=logging.DATA, msg='******* END run %i *******' % run_number)
#    log_file.logger.flush()

    # save the trial infomation from trial handler

    log_filename2 = "%s_%i.csv" % (log_filename[:-4], run_number )

    trials.saveAsText(log_filename2, delim=',', dataOut=('n', 'all_raw'))



    event.waitKeys(keyList=('space'))



# =====================

# MAIN 

#

# - set up stimuli and runs



for ridx, run in enumerate(runs):

    

    trials = data.TrialHandler(run, nReps=1, extraInfo=run_data, dataTypes=['stim_onset', 'resp_onset', 'rt', 'resp'], method="random")

    do_run(ridx+1, trials)

    

    




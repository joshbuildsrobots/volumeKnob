import board
import rotaryio
import digitalio
import time
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

##i don't know what this does but this is the only way it works; arguably the most important
##line of code in the entire program
cc = ConsumerControl(usb_hid.devices)

##sets up the rotary encoder to handle directional control
knob = rotaryio.IncrementalEncoder(board.D3, board.D4)
last_pos = 0

##sets up various buttons
playPause = digitalio.DigitalInOut(board.D0)
playPause.direction = digitalio.Direction.INPUT
playPause.switch_to_input(pull = digitalio.pull.DOWN)
playPausePrevState = playPause.value

##cont'd button setup
nextTrack = digitalio.DigitalInOut(board.D1)
nextTrack.direction = digitalio.Direction.INPUT
nextTrack.switch_to_input(pull = digitalio.pull.DOWN)
nextTrackPrevState = nextTrack.value

##cont'd button setup
previousTrack = digitalio.DigitalInOut(board.D2)
previousTrack.direction = digitalio.Direction.INPUT
previousTrack.switch_to_input(pull = digitalio.pull.DOWN)
previousTrackPrevState = previousTrack.value

print("now reading!")

##dictionary #1 to set up what two states we have
stateList = [
    {
        "Playing...",
    },
    {
        "Pausing..."
    }
]

##whichever state we are NOT in gets put in this list
notCurrState = []
##moves the state we are not utilizing away from action
notCurrState.append(stateList.pop(0))

while True:
##checks to see if variation of rotary encoder reading
    current_pos = knob.position
    if last_pos == 0 or current_pos != last_pos:
        print(current_pos)

        ##volume up
        if current_pos > last_pos:
            for i in range(5):
                cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        ##volume down
        if current_pos < last_pos:
            for i in range(5):
                cc.send(ConsumerControlCode.VOLUME_DECREMENT)
    ##sets the current position relative to itself
    last_pos = current_pos

##will play or pause track
    playPauseCurrState = playPause.value
    if playPauseCurrState != playPausePrevState:
        if playPauseCurrState:
            ##prints the state we are currently in
            print(stateList[0])
            cc.send(ConsumerControlCode.PLAY_PAUSE)
            ##sets up a temporary list to move states back and forth
            temp = []
            ##moves the just utilized state into the temporary list
            temp.append(stateList.pop(0))
            ##moves the unused state into the to-be-used list
            stateList.append(notCurrentState.pop(0))
            ##moves the just used state into the do-not-use list
            notCurrentState.append(temp.pop(0))
            playPausePrevState = playPauseCurrState
        else:
            playPausePrevState = False
            pass

##will skip or go back one track
    nextTrackCurrState = nextTrack.value
    if nextTrackCurrState != nextTrackPrevState:
        if nextTrackCurrState:
            print("skipping onto next track")
            cc.send(ConsumerControlCode.SCAN_NEXT_TRACK)
            nextTrackPrevState = nextTrackCurrState
        else:
            nextTrackPrevState = False
            pass

    previousTrackCurrState = previousTrack.value
    if previousTrackCurrState != previousTrackPrevState:
        if previousTrackCurrState:
            ##go back one track
            print("going back one track")
            cc.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
            previousTrackPrevState = previousTrackCurrState
        else:
            previousTrackPrevState = False
            pass

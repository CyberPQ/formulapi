#!/usr/bin/env python
# coding: utf8
import logging
import time
import cv2

from Formula import CarControl

carcontrol = CarControl()    

#Camera processing results
def CurrentTrackPosition():
    """
    Where the YetiBorg is across the track.
    Values range from +3 for the outside wall to -3 for the inside wall, the center of the track is 0.
    """
    return processing.CurrentTrackPosition()


def TrackFound():
    """
    Use this to check if the YetiBorg can see the track, True for when it can be seen, False for when it cannot be seen.
    The calls below are only valid if True.
    """
    return processing.TrackFound()


def AimForLane(position):
    """
    Changes where on the track the YetiBorg is aiming for.
    Values range from +3 for the outside wall to -3 for the inside wall.
    Center of the track is 0, we recommend staying between +2.5 and -2.5 to avoid driving into the wall itself.
    """
    raise NotImplementedError()

def WaitForWaypoint(waypoint):
    """
    Wait until a waypoint is reached, see the track layout for waypoint numbers.
    If you are already between the requested waypoint and the next one the call will come back immediately.
    """
    raise NotImplementedError()

def WaitForDistance(distance):
    """
    Wait until a distance in meters has been reached, see the track layout for relevant distances.
    The track distance is always based on the centre line, which is 22 meters long in total
    """
    raise NotImplementedError()
 
def CurrentAngle():
    """
    What angle the YetiBorg is facing verses the track.
    Values range from +90 for facing the outside wall to -90 for facing the inside wall.
    0 means we are driving parallel to the track.
    """
    return processing.CurrentAngle()

def TrackCurve():
    """
    Measures how quickly the track is curving in front of the YetiBorg.
    Positive values mean the track is curving towards the left, negative values mean the track is curving to the right.
    Low numbers (< ±0.1) typically mean the track is straight ahead.
    The Largest numbers are typically seen when the YetiBorg has just entered the corner itself.
    """
    raise NotImplementedError()

def TrackLines():
    """
    Gets the points found by the image processing used to calculate the above results.
    This is probably only useful to advanced users who need more information than the other functions return.
    Each lane on the track (such as the red/green boundary) is represented as a list of the points found.
    These lists are then returned as a list containing each list of points separately.
    """
    raise NotImplementedError()


def WaitForGo():
    """
    Waits for the starting signal lights before continuing.
    This will also control the LED on the ZeroBorg to indicate the YetiBorg is ready.
    """
    #TODO
    time.sleep(2)

def Speed(value):
    """
    Sets the speed of the YetiBorg in percent, 0 to 100.
    Values which are too low will prevent movement, especially when turning.
    """
    carcontrol.Speed(value)


def WaitForSeconds(sec):
    """
    Delays the code for a fixed amount of time in seconds.
    This is the same as using the standard time.sleep call from the Python library.
    """
    time.sleep(sec)

def LapCount():
    """
    Read the current number of completed laps.
    Useful to know if you have finished the race or not
    """
    raise NotImplementedError()

def FinishRace():
    """
    Turns the motors off and tells the main Formula.py script the race has ended.
    This will also control the LED on the ZeroBorg to indicate the YetiBorg has finished
    """
    carcontrol.Stop()



def GetDistance():
    """
    Read the distance in meters along the current lap.
    This is based on the speed travelled and gets reset to 0 when crossing the start/finish line.
    """
    raise NotImplementedError()


#Camera images

def GetLatestImage():
    """
    Get an OpenCV compatible image of the last raw frame grabbed from the camera.
    This is the same image used by the internal camera processing
    """
    return carcontrol.GetLatestImage()

def PerformProcessingStage(stage, image):
    """
    Perform one of the processing stages used by the standard camera processing.
    See the current guide for a list of the processing stages and the expected input and output images.
    Mostly for testing or experimentation use
    """
    raise NotImplementedError()

def SaveImage(image, filename):
    """
    Saves an image to the race results folder.
    """
    logger = logging.getLogger('formulapi')
    logger.debug('Save image to '+str(filename))
    cv2.imwrite(filename, image)


#Race logging

def StartUserLog():
    """
    Begins recording a log of what commands are given to the auto-drive system from the script.
    """
    format = '%(asctime)-15s %(message)s'
    logging.basicConfig(format=format)
    logger = logging.getLogger('formulapi')
    logger.setLevel(logging.INFO)

def StartDetailedLog():
    """
    Begins recording a log of what the various parts of the auto-drive system are doing.
    """
    format = '[%(filename)s:%(lineno)s - %(funcName)20s() ] %(asctime)-15s %(message)s'
    logging.basicConfig(format=format)
    logger = logging.getLogger('formulapi')
    logger.setLevel(logging.DEBUG)


def EndUserLog():
    """
    Stops recording the user commands log.
    """
    pass

def EndDetailedLog():
    """
    Stops recording the auto-drive system log.
    """
    pass
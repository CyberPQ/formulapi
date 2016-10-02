#!/usr/bin/env python
# coding: utf8
import RaceCodeFunctions
from RaceCodeFunctions import *

#wait control module to start
WaitForSeconds(1)

# Start logging what happens
StartUserLog()
StartDetailedLog()

### Settings for this race ###
laps = 10
 
### Start of the race ###
if TrackFound():
    # We can see the track, start by following the lane we are on
    trackLane = round(CurrentTrackPosition())
    AimForLane(trackLane)
else:
    # Cannot see the track, aim for the center instead (stopgap measure)
    AimForLane(0)
# Save a start-line image
photo = GetLatestImage()
SaveImage(photo, 'Start-line.jpg')

# Wait for the go signal from the start/stop lights.
WaitForGo()
# Go at max speed
Speed(20)
 
### During the race ###
# Keep going until we have fished all of the laps
while LapCount() < laps:
    # Full speed to the first corner
    WaitForSeconds(0.1)
 
### End of the race ###
# Save a finish-line image
photo = GetLatestImage()
SaveImage(photo, 'Finished.jpg')
# Slow the YetiBorg down gradually from 100% to 0%
for slowing in range(99, -1, -1):
    Speed(slowing)
    WaitForSeconds(0.01)
# Stop the logging
EndUserLog()
EndDetailedLog()
# End the race (will stop the robot and end the program)
FinishRace()
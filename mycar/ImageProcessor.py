#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import numpy
import math
import logging
import socket


class ImageProcessor(object):
    def __init__(self):
        self.trackcurve = 0.
        self.angle = 0.
        self.trackoffset = None

    """
    The only trouble here is that cv2.imwrite will not handle this data type.
    We can make a function to help us by making the values between 0 and 255 instead:
    """
    @staticmethod
    def _WriteMask(name, mask):
        image = mask * 255
        cv2.imwrite(name, image)


    """We make ourselves a little function which will find the edges in a mask image:
    """
    @staticmethod
    def _SweepLine(width, mask, y):
        # le mask est binaire, 1 représente la couleur
        found_color_other = []
        found_other_color = []
        # Grab the line of interest
        line = mask[y, :]
        # Get numpy to give us a list of the positions where the line changes in value
        changed_other_color = numpy.where(line[:-1] < line[1:])[0]
        changed_color_other = numpy.where(line[:-1] > line[1:])[0]
        # Remove changes too close to the edge of the image
        for i in changed_other_color:
            if i < 2:
                pass
            elif i > (width - 3):
                pass
            else:
                found_other_color.append(i)

        for i in changed_color_other:
            if i < 2:
                pass
            elif i > (width - 3):
                pass
            else:
                found_color_other.append(i)
        # Return the found values
        return found_color_other, found_other_color

    # The values of try1, try2, try3 are used to attempt a match with target
    # Any matches are added to existing lists matched1, matched2, matched3
    # Any values which cannot be matched are added to the existing list unmatched
    @staticmethod
    def _FindMatches(width, y, target, try1, try2, try3, matched1, matched2, matched3, unmatched):
        """The function is fairly long but quite simple.
        It takes a list of points to try and match and one or more lists to try and match it with.
        Each point is then added to one of the matched lists, or is added to the unmatched list.
        """
        maxSeperation = int(width * 0.05)
        # Loop over all the values in target:
        while len(target) > 0:
            # Remove the next value from the list of targets
            xt = target.pop()
            matched = False
            # See if try1 can match it
            if try1:
                for x1 in try1:
                    if abs(x1 - xt) < maxSeperation:
                        # Matched, work out the point and add it
                        matched = True
                        try1.remove(x1)
                        x = (xt + x1) / 2
                        matched1.append((x, y))
                        break
                if matched:
                    continue
            # See if try2 can match it
            if try2:
                for x2 in try2:
                    if abs(x2 - xt) < maxSeperation:
                        # Matched, work out the point and add it
                        matched = True
                        try2.remove(x2)
                        x = (xt + x2) / 2
                        matched2.append((x, y))
                        break
                if matched:
                    continue
            # See if try3 can match it
            if try3:
                for x3 in try3:
                    if abs(x3 - xt) < maxSeperation:
                        # Matched, work out the point and add it
                        matched = True
                        try3.remove(x3)
                        x = (xt + x3) / 2
                        matched3.append((x, y))
                        break
                if matched:
                    continue
            # No matches
            unmatched.append((xt, y))

    """It would help a lot if we could see our points at this stage.
    We can make a quick function to draw a cross on the image like this
    """
    @staticmethod
    def DrawCross(image, (x, y), (r, g, b)):
        crossSize = 5
        width = image.shape[1]
        height = image.shape[0]
        # Build the list of points to change
        points = []
        for i in range(-crossSize, crossSize + 1):
            points.append((x + i, y))
            points.append((x, y + i))
        # Change the points on the image
        for point in points:
            x = point[0]
            y = point[1]
            if (x >= 0) and (y >= 0) and (x < width) and (y < height):
                image.itemset((y, x, 0), b)
                image.itemset((y, x, 1), g)
                image.itemset((y, x, 2), r)

    def ProcessingImage(self, image, saveimages=False):
        """
        process image from camera
        """
        #What we want to do is known as cropping.
        #This is where we chop out the parts of the image we do not want.
        #In our image we do not need the top part.
        #We can remove it like this:
        height, width, channels = image.shape
        cropTop = int(height * 0.3)
        cropBottom = int(height * 1.0)
        cropped = image[cropTop:cropBottom, :, :]
        croppedheight = cropBottom - cropTop
        if saveimages:
            cv2.imwrite('cropped.jpg', cropped)

        #Now we have removed the background we can try and find any walls.
        #Looking at the image they should be much darker than the rest of the track.
        #We can generate a mask of what parts of the image are dark enough like this
        wallR = 60
        wallG = 60
        wallB = 60
        walls = cv2.inRange(cropped, numpy.array((0, 0, 0)), numpy.array((wallB, wallG, wallR)))
        if saveimages:
            cv2.imwrite('walls.jpg', walls)

        #The walls are a bit untidy, we can remove some of the noise by using a filter.
        #We will use an erosion filter to reduce the mask slightly, this is cheap and will remove small areas of noise.
        erodeSize = 5
        erodeKernel = numpy.ones((erodeSize, erodeSize), numpy.uint8)
        walls = cv2.erode(walls, erodeKernel)
        if saveimages:
            cv2.imwrite('walls2.jpg', walls)
        #The larger erodeSize is, the more the edge of the wall is taken away.
        #Too large and the wall will be inaccurate, too small and we will see bits of "wall" in strange places.

        #The next step is to split the colour channels apart.
        blue, green, red = cv2.split(cropped)
        if saveimages:
            cv2.imwrite('blue.jpg', blue)
            cv2.imwrite('green.jpg', green)
            cv2.imwrite('red.jpg', red)

        #In each image the track of interest is bright compared to the others.

        #If we get the largest of the three channels we can compare them
        maxImage = numpy.maximum(numpy.maximum(blue, green), red)
        if saveimages:
            cv2.imwrite('max.jpg', maxImage)

        #The levels are not quite the same, but they are roughly correct.
        #We can do a bit better by adjusting the green and blue levels a bit:
        # Apply gains
        red = red * 1.0
        green = green * 1.2
        blue = blue * 1.5
        # Limit the range of values to the standard limits
        red   = numpy.clip(red,   0, 255)
        green = numpy.clip(green, 0, 255)
        blue  = numpy.clip(blue,  0, 255)
        red   = numpy.array(red,   dtype = numpy.uint8)
        green = numpy.array(green, dtype = numpy.uint8)
        blue  = numpy.array(blue,  dtype = numpy.uint8)
        # Redo the maximum calculation
        maxImage = numpy.maximum(numpy.maximum(blue, green), red)
        if saveimages:
            cv2.imwrite('max2.jpg', maxImage)

        #Now we remove any areas which are not the highest from each image:
        red  [red   < maxImage] = 0
        green[green < maxImage] = 0
        blue [blue  < maxImage] = 0
        if saveimages:
            cv2.imwrite('blue2.jpg', blue)
            cv2.imwrite('green2.jpg', green)
            cv2.imwrite('red2.jpg', red)

        #We can see this a bit clearer as a single image
        merged = cv2.merge([blue, green, red])
        if saveimages:
            cv2.imwrite('merged.jpg', merged)

        """What we want to do is 'scan' along the image in many places and find the outsides of the three colours.
        Before we can do that they need to be simplified to True or False arrays.
        We can do this very simply by using the inbuilt functionality of numpy:
        """
        red   = red   > 60
        green = green > 60
        blue  = blue  > 60
        walls = walls > 60

        if saveimages:
            self._WriteMask('blue-mask.jpg',  blue)
            self._WriteMask('green-mask.jpg', green)
            self._WriteMask('red-mask.jpg',   red)
            self._WriteMask('walls-mask.jpg', walls)


        """The next thing to do is decide where in the image we will take slices.
        This code will generate 100 slices along the original image:
        """
        grid = 100
        scanLines = []
        for i in range(grid):
            # Work out the position in the original image
            position = (i / float(grid)) * croppedheight
            position = int(position)
            
            scanLines.append(position)

        """We can better illustrate where these lines are by drawing them.
        We do this by making a brand new image the same size as the cropped one.
        Then we draw our lines on top of it:
        """
        # Make a black image the same size as our cropped image
        scanLineImage = numpy.zeros_like(cropped)
        colourWhite = (255, 255, 255)
        # Loop over each line
        for y in scanLines:
            cv2.line(scanLineImage, (0,y), (width-1,y), colourWhite, 1)
        if saveimages:
            cv2.imwrite('scanlines.jpg', scanLineImage)

        """We can now process each line, but we still need to match the lines together.
        We do this by looking for similar positions:
        """
        """So we now have:
            Four image masks we can match
            A set of lines to scan over
            A function to scan for changes
            A function to find matches between two or more lists
        We are now ready to find all of our points :)

        What we do is go through each line in turn and:

        Scan each mask for the changes (if any) on that line
        Attempt to match each line with any it might be next to
        Keep all the matches in the same list for all of the lines
        """
        # Make our matched lists
        matchWR = []
        matchRB = []
        matchBR = []
        matchRG = []
        matchGB = []
        matchBG = []
        matchGW = []
        unmatched = []
        # Loop over each line
        for y in scanLines:
            # Scan the masks
            edge_Ro, edge_oR = self._SweepLine(width, red,   y)
            edge_Go, edge_oG = self._SweepLine(width, green, y)
            edge_Bo, edge_oB = self._SweepLine(width, blue,  y)
            edge_Wo, edge_oW = self._SweepLine(width, walls, y)
            # Do the matching
            self._FindMatches(width, y, edge_Ro, edge_oG, edge_oB, None, matchRG, matchRB, None, unmatched)
            self._FindMatches(width, y, edge_Go, edge_oB, edge_oW, None, matchGB, matchGW, None, unmatched)
            self._FindMatches(width, y, edge_Bo, edge_oR, edge_oG, None, matchBR, matchBG, None, unmatched)
            self._FindMatches(width, y, edge_Wo, edge_Ro, None, None,    matchWR, None, None, unmatched)
            # Add any left over points to the unmatched list
            others = edge_oR[:] + edge_oG[:] + edge_oB[:] + edge_oW[:]
            for x in others:
                unmatched.append((x, y))

        if saveimages:
            pointImage = numpy.zeros_like(cropped)
            for point in matchRG:
                self.DrawCross(pointImage, point, (255, 255, 0))
            for point in matchRB:
                self.DrawCross(pointImage, point, (255, 0, 255))
            for point in matchRW:
                self.DrawCross(pointImage, point, (255, 0, 0))
            for point in matchGB:
                self.DrawCross(pointImage, point, (0, 255, 255))
            for point in matchGW:
                self.DrawCross(pointImage, point, (0, 255, 0))
            for point in unmatched:
                self.DrawCross(pointImage, point, (127, 127, 127))
            cv2.imwrite('points.jpg', pointImage)

            pointImage = cropped[:,:,:]
            for point in matchRG:
                self.DrawCross(pointImage, point, (255, 255, 0))
            for point in matchRB:
                self.DrawCross(pointImage, point, (255, 0, 255))
            for point in matchRW:
                self.DrawCross(pointImage, point, (255, 0, 0))
            for point in matchGB:
                self.DrawCross(pointImage, point, (0, 255, 255))
            for point in matchGW:
                self.DrawCross(pointImage, point, (0, 255, 0))
            for point in unmatched:
                self.DrawCross(pointImage, point, (127, 127, 127))
            cv2.imwrite('points2.jpg', pointImage)

        #From the end of previous part we package up the matched points into a list of lists like this
        lines = [matchWR, matchRB, matchBR, matchRG, matchGB, matchBG, matchGW]

        """The first thing we do is pick a line to work with.
        While it would be more accurate to use as much data as possible, it is quicker to use a single line.

        In our case we decide to go with the line that has the largest number of available points.
        We can do that quickly by comparing the list lengths like so
        """
        count = 0
        index = 0
        for i in range(len(lines)):
            if len(lines[i]) > count:
                index = i
                count = len(lines[i])


        """To determine where we actually are on the track the code needs to know which lane this is.
        We can build a simple lookup table to determine the lane like this
        """
        lineIndexToOffset = {
            0 : +3.0,
            1 : +2.0,
            2 : +1.0,
            3 :  0.0,
            4 : -1.0,
            5 : -2.0,
            6 : -3.0
        }
        lineOffset = lineIndexToOffset[index]
        bestLine = lines[index]

        r"""There are a few different ways of approaching this problem.
        Two good ways are:

        Take an average of where all the points are
        Take the point at a position in the image
        Option 1 is potentially more accurate, but it can get confused by curves and parts of the image which are hidden.
        Option 2 is simpler, but it can get confused if there is no point near enough to the position we are looking for.

        As we have a large number of varying curves along with robots which can block our view we will use option 2.
        This means we need to decide on a position in the image, ideally a bit ahead of where we are.
        We will go for 33% of the way down the image, which is here
        """
        targetY = (cropBottom - cropTop) * 0.33
        """The next thing to do is find the point closest to this target.
        This is very similar to the search for the best line to use
        """
        if len(bestLine) == 0:
            return
        offsetIndex = 0
        offsetErrorY = abs(targetY - bestLine[0][1])
        for i in range(len(bestLine)):
            errorY = abs(targetY - bestLine[i][1])
            if errorY < offsetErrorY:
                offsetIndex = i
                offsetErrorY = errorY
        offsetPoint = bestLine[offsetIndex]

        """
        Now we have our point we need to measure how far out it is.
        To do this we need an X position we are aiming for and we need to know how far apart the lanes are.
        We have worked these out as:
        """
        targetX = width / 2.0
        laneWidth = 1250.0
        offsetX = offsetPoint[0] - targetX
        #Then see how it compares to a whole track
        offsetX = offsetX / laneWidth

        #We can compute the full track offset by summing the offset of the line from center with the offset from the line
        self.trackoffset = lineOffset + offsetX

        """
        We can measure this by comparing how far apart each point is in X verses Y compared to the one before it.
        These changes in the numbers we will refer to as dX and dY
        """
        dXdY = []
        for i in range(offsetIndex, len(bestLine)):
            dX = float(bestLine[i-1][0] - bestLine[i][0])
            dY = float(bestLine[i][1] - bestLine[i-1][1])
            if dY:
                dXdY.append((dX, dY))

        """
        To work out the amount the angle the line is at we need to divide dX by dY.
        For example if X is always the same (dX = 0) and Y changes by 10 each time (dY = 10) then dX ÷ dY = 0, in other words 0°.
        If X and Y both change by 10 each time (dX = 10, dY = 10) then dX / dY = 1, in other words 45°.
        To get an average change we simply average these values:
        """
        gradient = 0
        for dx, dy in dXdY:
            gradient += dx / dy
        gradient /= len(dXdY)

        """
        The YetiBorg is basically central (around 0°), but the lines in the image are angled.
        Also notice how the angle for the lines further from the center of the image are worse?
        This is called perspective error.

        In order to correct for this error we need to measure the error in a 0° image.
        In this case we see a gradient of about 2.6 at an offset of about 0.25 of a lane.
        The offset matters as the error will scale with this offset.
        Note the offset between the center of the image and the line, the value in offsetX from last time.

        We can work out our correction factor as:
        Note that this value is dependant on the image resolution, changing it will require the correction factor to be measured again.
        """
        correctionFactor = 2.6 / 0.25

        correction = correctionFactor * offsetX
        gradient -= correction
        self.angle = math.atan(gradient) * 180 / math.pi

        """
        We still need these to calculate our track curvature value
        This will be the value returned from the TrackCurve() Race Code Function.

        We can measure this by comparing how different the changes between points are.
        Consider two measured changes when on a curve
        The second change is about the same for Y, but much larger in X.
        This means the changes are growing as the curve bends, large growth means a sharper curve.
        When looking at these changes:

        A perfectly straight line will give 0
        A gentle curve to the left sees negative changes
        A sharp curve to the left sees large negative changes
        A gentle curve to the right sees positive changes
        A sharp curve to the right sees large positive changes
        We calculate this in a similar way as the first set of changes, but using the dXdY values this time
        """
        gradient2 = 0.0
        lastG = dXdY[0][0] / dXdY[0][1]
        for i in range(1, len(dXdY)):
            nextG = dXdY[i][0] / dXdY[i][1]
            changeG = lastG - nextG
            gradient2 += changeG / dXdY[i][1]
            lastG = nextG
        gradient2 /= len(dXdY)
        self.trackcurve = gradient2





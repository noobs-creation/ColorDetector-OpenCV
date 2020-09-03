
# Importing required packages
import cv2
import pandas as pd
import argparse

# Argument parser to get image path from command line
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Enter Image Path")
args = vars(ap.parse_args())
imagePath = args['image']

# Using OpenCV to read image
image = cv2.imread(imagePath)

# declaring and initialising variables later to be used as global
clicked = False
r = g = b = 0

# Reading csv file with pandas and naming each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csvColor = pd.read_csv('colors.csv', names=index, header=None)


# function to find the matching color by calculating minimum distance from colors
def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csvColor)):
        d = abs(R - int(csvColor.loc[i, "R"])) + abs(G - int(csvColor.loc[i, "G"])) + abs(B - int(csvColor.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            colorname = csvColor.loc[i, "color_name"]
    return colorname


# function to get x,y coordinates of mouse on double click
def draw_function(event, x, y, flags, param):
    # This checks the double click event inside the window
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, clicked
        clicked = True
        # Getting the the BGR value at the selected coordinate or pixel
        b, g, r = image[y, x]
        b, g, r = int(b), int(g), int(r)


cv2.namedWindow('Selected-image')
cv2.setMouseCallback('Selected-image', draw_function)

while 1:
    cv2.imshow("Selected-image", image)
    if clicked:
        # cv2.rectangle(image, startpoint, endpoint, color, thickness=-1) this fills entire rectangle with selected color
        # Text string to display( Color name and RGB values )
        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.rectangle(image, (20, 20), (750, 60), (b, g, r), -1)
        text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        cv2.putText(image, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colors text will be displayed in black colour
        if r + g + b >= 600:
            cv2.putText(image, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    # Break the loop and destroy window when user hits 'esc'
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()

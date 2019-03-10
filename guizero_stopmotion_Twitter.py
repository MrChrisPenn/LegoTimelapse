# This is a simple gui for creating stop motion animations using the Pi camera
# martin@ohanlonweb.com
# stuffaboutcode.com

# Instructions:
# - Connect a camera module
# - Enable the camera (Menu > Preferences > Raspberry Pi Configuration, Interfaces, Camera)
# - Install the relevant modules, open a terminal (Menu > Accessories > Terminal) and run:
#   - sudo pip3 install guizero
#   - sudo pip3 install imageio
# - Run the program
#   - python3 guizero_stopmotion.py

#A few bits bolted on by Chris Penn @ChrisPenn84
from twython import Twython
from guizero import App, Box, Picture, Text, PushButton, info
from io import BytesIO
import imageio
from PIL import Image
from picamera import PiCamera
from picamera.array import PiRGBArray
import time


consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''


api = Twython(consumer_key,consumer_secret,access_token,access_token_secret)


def Tweet():
    time.sleep(6)
    msg = "Test animation"+" :)"+"@ChrisPenn84"
    photo = open('/home/pi/ani1.gif', 'rb')
    response = api.upload_media(media=photo)
    api.update_status(status = msg, media_ids=[response['media_id']])



def update_gui():
    if len(animation.images) == 0:
        instructions.value = "take your first image"
        pic_button.enable()
        del_button.disable()
        reset_button.disable()
        save_button.disable()
        animation.hide()
    else:
        # build gif from animation.images
        # write the animated gif to BytesIO object
        gif_output = BytesIO()
        imageio.mimsave(gif_output, animation.images, format="gif")
        
        # set the animation to a PIL image of the gif 
        animation.image = Image.open(gif_output)
        
        instructions.value = "take another image"
        
        # enable the gui
        pic_button.enable()
        del_button.enable()
        reset_button.enable()
        save_button.enable()
        animation.show()

def take_pic():
    # take a picture
    pic_button.disable()
    instructions.value = "adding ..."
    gui.tk.update()
    
    # capture the image
    camera.capture(camera_output, "rgb")
    # append the camera image to the list as a numpy array
    animation.images.append(camera_output.array)
    # truncate the camera output now we have dealt with it
    camera_output.truncate(0)

    update_gui()
    
def del_pic():
    instructions.value = "deleting ..."
    gui.tk.update()
    animation.images.pop()
    update_gui()

def reset():
    animation.images = []
    update_gui()
    
def save():
    file_name = "ani1.gif"
    imageio.mimsave(
        file_name, 
        animation.images, 
        format="gif",duration=0.5)
    info("save", "animation saved as {}".format(file_name))
    
# create the camera
camera = PiCamera(resolution="640x480")
camera_output = PiRGBArray(camera)

# create the gui
gui = App(title="stop motion animation")
controls = Box(gui, layout="grid")
instructions = Text(gui)

pic_button = PushButton(
    controls,
    text="take image",
    command=take_pic,
    grid=[0,0])

del_button = PushButton(
    controls,
    text="delete last",
    command=del_pic,
    grid=[1,0])

reset_button = PushButton(
    controls,
    text="reset",
    command=reset,
    grid=[2,0])

save_button = PushButton(
    controls,
    text="save",
    command=save,
    grid=[3,0])

save_button = PushButton(
    controls,
    text="Tweet",
    command=Tweet,
    grid=[4,0])

animation = Picture(gui)
animation.images = []

update_gui()

gui.display()

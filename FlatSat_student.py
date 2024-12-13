"""
The Python code you will write for this module should read
acceleration data from the IMU. When a reading comes in that surpasses
an acceleration threshold (indicating a shake), your Pi should pause,
trigger the camera to take a picture, then save the image with a
descriptive filename. You may use GitHub to upload your images automatically,
but for this activity it is not required.

The provided functions are only for reference, you do not need to use them. 
You will need to complete the take_photo() function and configure the VARIABLES section
"""

# AUTHOR: GatorSAT
# DATE: 12/4/2024

# Import libraries
import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from git import Repo
from picamera2 import Picamera2

# VARIABLES
THRESHOLD = 13
REPO_PATH = "/home/tanya/FlatSAT-Camera"  # Path to GitHub repo
FOLDER_PATH = "/Images"  # Path to image folder in GitHub repo
NAME = "MasonH"  # Your name for file naming

# IMU and camera initialization
i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)
picam2 = Picamera2()

def git_push():
    """
    This function is complete. Stages, commits, and pushes new images to your GitHub repo.
    """
   
    try:
         repo = Repo(REPO_PATH)
         origin = repo.remote('origin')
         print('added remote')
         origin.pull()
         print('pulled changes')
         repo.git.add(REPO_PATH + FOLDER_PATH)
         repo.index.commit('New Photo')
         print('made the commit')
         origin.push()
         print('pushed changes')
    except:
         print('Couldn\'t upload to git')

def img_gen(name):
    """
    This function generates a new image name.
    """
    t = time.strftime("_%H%M%S")
    imgname = f"{REPO_PATH}/{FOLDER_PATH}/{name}{t}.jpg"
    return imgname

def take_photo():
    """
    Takes a photo when the FlatSat is shaken.
    """
    while True:
        # Get accelerometer readings
        accel_x, accel_y, accel_z = accel_gyro.acceleration
        total_accel = (accel_x**2 + accel_y**2 + accel_z**2)**0.5
        print("Hola")
        if total_accel > THRESHOLD:  # Check if acceleration exceeds the threshold
           # time.sleep(1)  # Pause
            image_path = img_gen(NAME)  # Generate image path
            
            picam2.configure(picam2.create_still_configuration())
            capture_config = picam2.create_still_configuration()
            picam2.start()
            time.sleep(1)
            picam2.capture_image()
            print("Hello")
            picam2.switch_mode_and_capture_file(capture_config, image_path)  # Capture the image
            picam2.stop()
            print(f"Photo saved: {image_path}")
            git_push()  # Push photo to GitHub
            
        time.sleep(2)  # Pause after processing

def main():
    try:
        take_photo()
    except KeyboardInterrupt:
        print("Program interrupted. Exiting...")

if __name__ == '__main__':
    main()

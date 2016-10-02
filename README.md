Formulapi Simulator in Python
===============================

Install Simulator
-------------------

install python 2.7.12 (choose 32 or 64 bits appropriately with your computer)

install pyopengl from http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl

install wxPython from https://wxpython.org/download.php#msw (choose 32 or 64 bits appropriately with your python version)

install standard librairies

	pip install numpy
	pip install pillow

install these .whl files for 64 bits:

	pip install PyOpenGL-3.1.1-cp27-cp27m-win_amd64.whl
	pip install PyOpenGL_accelerate-3.1.1-cp27-cp27m-win_amd64.whl

install these .whl files for 32 bits:

	pip install PyOpenGL-3.1.1-cp27-cp27m-win32.whl 
	pip install PyOpenGL_accelerate-3.1.1-cp27-cp27m-win32.whl


Run the simulator and robot
----------------------------

### Locally

To run the simulator **and** the robot both locally on your computer, use the provided batch file :

	run_simu_local.bat

### Using a raspberry Pi

To run the simulator only on your computer, use the provided batch file:

	run_simu.bat
	
Then, start the robot artificial intelligence with the following command (`0` parameter for robot number 0):

	./run_robot.sh 0



source of Information:
-----------------------

 - https://github.com/AidanHaddonWright/OpenGL_tutorials/blob/master/Lessons/02-%20Creating_a_first_person_perspective/main.py


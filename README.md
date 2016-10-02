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




todo list:
--------------

- [ ] add lap time per car
- [ ] add starter light
- [ ] add track wall
- [X] draw car in 3d
- [ ] enhance track texture
- [X] capture car view and send over tcp
- [X] fix motor control from tcp
- [ ] add collision detection
- [X] add other car (multi car view)


collision for lap count:
-------------------------

The problem reduces to this question: Do two lines from A to B and from C to D intersect?
Then you can ask it four times (between the line and each of the four sides of the rectangle).

Here's the vector math for doing it. I'm assuming the line from A to B is the line in question and the line from C to D is one of the rectangle lines.
My notation is that Ax is the "x-coordinate of A" and Cy is the "y-coordinate of C." And "*" means dot-product, so e.g. A*B = Ax*Bx + Ay*By.

	E = B-A = ( Bx-Ax, By-Ay )
	F = D-C = ( Dx-Cx, Dy-Cy ) 
	P = ( -Ey, Ex )
	h = ( (A-C) * P ) / ( F * P )

This h number is the key. If h is between 0 and 1, the lines intersect, otherwise they don't. If F*P is zero,
of course you cannot make the calculation, but in this case the lines are parallel and therefore only intersect in the obvious cases.

The exact point of intersection is C + F*h.


source of Information:
-----------------------

 - https://github.com/AidanHaddonWright/OpenGL_tutorials/blob/master/Lessons/02-%20Creating_a_first_person_perspective/main.py

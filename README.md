1. Objectives: there are several objectives in this project. (1) use NEC2++ API to set up a code (impedance.py) for the simulation of a monopole antenna. The impedance will be computed based on the input dimensions and the best design will be identified based on the impedance matching principle (i.e. minimum reflection). (2) matplotlib module will be used to render the results in 2D and 3D (i.e. imshow() and plot_surface()) to give an intuitive presentation of correlation between dimensions and reflection coefficient. (3) finally a GUI is designed with tabs to embed the introduction, codes and simulation interface. User can update the range of the parameter sweep and the intrinsic impedance and click the button to refresh the plots. A progressbar is embeded to show the progress of the simulation. 

2. Keywords: Antenna, NEC2++, GUI, EM Simulation, Monopole, QThread, ProgressBar, QWidget, impedance, matplotlib

3. Files in the folder: 
        impedance.py is imported in plot.py
        plot.py is imported in gui.py
        snapshots are provided to give user a first view of gui. 

4. NEC2++ Intro: NEC2++ is a free (GPL v2) electromagnetic simulation software compatable with NEC-2. It has been rewritten from the ground up.Nec2++ consists of a library that can be called from C++, C, python and Ruby, and so it can incorporated into other projects like GUI tools and automatic antenna optimization systems. There is also an executable necpp that can read antenna description files (like the original). Nec2++ is developed on Debian linux, but will work on a variety of other operating systems. (Timothy C.A. Molteno, ''NEC2++: An NEC-2 compatible Numerical Electromagnetics Code'', Electronics Technical Reports No. 2014-3, ISSN 1172-496X, October 2014.). Link for Python API: http://tmolteno.github.io/necpp/libnecpp_8h.html#a03d9347b31b3558fb40130e490314ae0. A brief list of notes can also be found in the folder (see nec2ppAPI_quicknotes.txt).

5. Remaining Work: Although QThread is used to set up a parallel running with the main thread, it awaits a further improvement. The problem is 'connect' method used to update progressbar is using a function (updatebar) in the main thread/main class. So, though the signal 'val' is triggered in the QThread to update the progressbar based on 'plot.prog' (a mark for computation progress), it won't be executed until the event in the main thread (updatefig) is done. QThread has a lower priority than main thread. 

6. A personal perspective on the relation between main thread and QThread: the main thread will execute everything thing in main loop except for QThread class and objects. QThread class and objects will be executed in a seperate thread which has lower priority than main thread. If QThread class and objects has conflict with main thread (e.g. during calling methods in main loop/ outside QTHread class), the event (being in a computation loop) in the main thread will be executed first. 
 

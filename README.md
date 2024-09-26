This repository contains the files of the research project titled **"Prototypical Realization and Evaluation of the Data Organizaton and Management for Heterogeneous Data"**


The file **"Poster_Sarath.pdf"** contains the poster created as part of the research project. This is to gives a brief understanding of the system.

The video **"working_system.mp4**" shows the final working of the system. 



In the _src_ folder all the the necessary codes required for the execution of the system are available.

For the implementation of a network file system, I had used virtual machines. The user need to create atleast 2 virtual machines, one as conroller and other as active node. It is better to have 3 VMs, such that there are controller node, active node and a passive node.

The files from the _src_ should be executed in the _controller_ node. One the foler in the order of their naming. Folder that begins with "1_..." should be used first then "2...". Since the system was supposed to be made as modular and extensible, multiple docker files needs to be executed. All the commands needed are specified in the respective folders.

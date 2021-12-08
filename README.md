## CS655 Image Recognition Application

Project Demo:


### Set up instructions: 
First, create the required GENI environment by using the Rspec provided in the rep. Then, you need to clone the repo in the home directory in both your worker and server nodes. Once that done, please follow the relevant instructions below: 

#### Server Setup: 

From the main repo dir, run: 

```console
$ chmod +x install_requirements.sh 
$ ./install_requirements.sh 
$ cd server 
$ ./install_service.sh 
```

The service is now running in the background. To check on its status, run: 

```console
$ sudo systemctl status image_pred.service
```

Then please modify the workers.txt file in server to properly set your workers ip/port values. 

#### Worker Setup: 

From the main repo dir, run: 

```console
$ chmod +x install_requirements.sh 
$ ./install_requirements.sh 
$ cd worker
$ ./install_service.sh 
```

The service is now running in the background. To check on its status, run: 

```console
$ sudo systemctl status worker.service
```




 

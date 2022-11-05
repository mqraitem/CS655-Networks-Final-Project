## CS655 Image Recognition Application

A server implementation in python that receives and distributes Deep Learning based image classification requests to actively running workers. 

### Application Set up: 
First, create the required GENI environment by using the Rspec provided in the repo. Then, clone the repo in the home directory in both your worker and server nodes. Once that done, please follow the relevant instructions below: 

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

### Testing Setup: 

For Testing, clone the repo on your personal machine and then run: 

```console
$ chmod +x install_requirements.sh 
$ ./install_requirements.sh 
$ cd tools
```
In order to use the browser automation tool Selenium, you will need to install [chromedriver](https://chromedriver.chromium.org/downloads). Please install the one that matches your machine chrome browser version. Then run: 


```console
$ wget [chromedriver link]
$ unzip [chromedriver file]
$ sudo mv [chromedriver file] /usr/bin
```

Finally, please modify the url in the script to match your setup url. Now, you should be able to run the test_script_freq.py. Feel free to modify the simulation parameters inside the script. 


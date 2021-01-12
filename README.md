# cml2 lab operation

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/masanobu48154/cml2_lab_operation)

## Overview

Cisco Modeling Labs is a tool for building virtual network simulations (or labs) for you to test out new topologies, protocols, and config changes; automate network tests via CI/CD pipeline integration; and learn new things about the cool world of networking.

With this demo you can deploy a docker containers to control multiple CML2s.

- breakout_tool container :  This container provides a telnet connection to the node in CML2.This container will be deployed as many as your CML2 number.
- python(API server) container : This container has the following two functions.
  1. Import, start, stop, wipe and delete the lab of CML2.
  2. Configure the breakout tool with the selenium library so that you can telnet to the cml2 node.
- controller container : This container provides UI that controls multiple CML2s. Please use it as a reference for creating a controller, which is your job.
- selenium-hub container : Pull and use docker image that can use selenium grid. This container is the hub of the selenium grid that distributes the processing to the chrome clients.
- selenium-chrome container : Pull and use docker image that can use selenium grid. This container is the client of the selenium grid that has a chrome browser operating the breakout tool web ui.

## The OS on which this software was tested
- Ubuntu 20.04.1 LTS (Focal Fossa) with docker and python3 installed.

## Installation

### 1. Clone the repository
```
git clone https://github.com/masanobu48154/cml2_lab_operation.git
```

### 2. Go into the CML2 directory
```
cd cml2_lab_operation/
```

### 3. Edit env.py for your environment.
```
vi env.py
```

Define variables for your environment.
The environment when testing CML2 with 10 units is as follows.

```
$ cat env.py
#!user/bin/python

class MyEnv:
    """
    Define variables for your environment.

    key
    ---
    your_username:
        Username with administrator privileges for cml2 rest API.
    your_password:
        Password for "your_username".
    subnet
        The subnet to which the docker host server belongs.
        This subnet is required to reach the internet.
        Controllers, API servers, selenium hubs and selenium chromes need to
        belong to this subnet.
    gateway
        Docker host subnet gateway.
    cml2_
        Address of CML2 built in your environment.
    api_server
        Address of api_server.
        The API server is automatically deployed as a docker container.
    selenium_hub
        Address of selenium_hub.
        The selenium_hub is automatically deployed as a docker container.
    selenium_chrome01
        Address of selenium_chrome01.
        The selenium_chrome01 is automatically deployed as a docker container.
    selenium_chrome02
        Address of selenium_chrome02.
        The selenium_chrome02 is automatically deployed as a docker container.
    breakout_tool
        Address of breakout_tool0.
        The breakout_tool0 is automatically deployed as a docker container.
    controller
        Address of controller.
        The controller is automatically deployed as a docker container.
        This controller provides only minimal functionality.
         1.Stop the existing lab, wipe it, and delete it.
         2.Start lab from the yaml file.
         3.Make it possible to operate the nodes in lab with telnet via
           breakout_tool.
        It is your job to make a controller, so please refer to this form to
        make it.
    phsical_nic
        NIC name of docker host.
    """
    def __init__(self):
        self.my_env = {
            "your_username": "testuser",
            "your_password": "testpassword",
            "subnet": "172.16.1.0/24",
            "gateway": "172.16.1.1",
            "cml2_0": "172.16.1.200",
            "cml2_1": "172.16.1.201",
            "cml2_2": "172.16.1.202",
            "cml2_3": "172.16.1.203",
            "cml2_4": "172.16.1.204",
            "cml2_5": "172.16.1.205",
            "cml2_6": "172.16.1.206",
            "cml2_7": "172.16.1.207",
            "cml2_8": "172.16.1.208",
            "cml2_9": "172.16.1.209",
            "api_server": "172.16.1.254",
            "selenium_hub": "172.16.1.150",
            "selenium_chrome01": "172.16.1.151",
            "selenium_chrome02": "172.16.1.152",
            "breakout_tool0": "172.16.1.180",
            "breakout_tool1": "172.16.1.181",
            "breakout_tool2": "172.16.1.182",
            "breakout_tool3": "172.16.1.183",
            "breakout_tool4": "172.16.1.184",
            "breakout_tool5": "172.16.1.185",
            "breakout_tool6": "172.16.1.186",
            "breakout_tool7": "172.16.1.187",
            "breakout_tool8": "172.16.1.188",
            "breakout_tool9": "172.16.1.189",
            "controller": "172.16.1.250",
            "num_cml2": "10",
            "phsical_nic": "ens160"
        }
```

### 4. Store yaml file
Store the yaml file that defines the lab configuration in the virl_data directory. You can download this yaml file from the lab defined in CML2.

## Usage

### 1. Creates html files for the controller
```
sudo python3 create_controller.py
```
This script creates html files for the controller.

### 2. Build and run containers
```
sudo python3 docker_start.py
```
This script build and run breakout tool containers, python container, controller container, selenium-hub container and selenium-chrome containers.

> The details of the container runned by this script are as follows.
>
> 1. breakout_tool containers :  
>    - Pulled image == ubuntu:20.04
>    - Software installed when built == nothing
> 2. python(API server) container :
>    - Pulled image == ubuntu:20.04
>    - Software installed when built == python3, python3-pip, apache2, vim, requests, selenium
> 3. controller container :
>    - Pulled image == ubuntu:20.04
>    - Software installed when built == apache2, vim
> 4. selenium-hub container :
>    - Pulled image == selenium/hub:3.14.0-helium
>    - Software installed when built == nothing
> 5. selenium-chrome container :
>    - Pulled image == selenium/node-chrome-debug:3.14.0-helium
>    - Software installed when built == nothing

### 3. Operate CML2s
1. Access the controller's ip address via http in your browser.
2. Click the link of the CML2 you want to operate.
3. Select the lab name you want to start and click run.
4. Drink coffee and wait for all nodes to start.
5. After all nodes have started, you can access telnet by clicking the link. It may be necessary to specify the telnet client on the browser side.

## Uninstall
```
sudo python3 remove_all_container.py
```
Delete all docker containers and delete the built image as well.

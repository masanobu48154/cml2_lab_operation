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
        Controllers, API servers, selenium hubs and seleniumi chromes need to
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
        The sselenium_chrome01 is automatically deployed as a docker container.
    selenium_chrome02
        Address of selenium_chrome02.
        The sselenium_chrome02 is automatically deployed as a docker container.
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
            "your_username": "your_username",
            "your_password": "your_password",
            "subnet": "<your_lab_subnet/mask>",
            "gateway": "<your_lab_gateway_ip_address>",
            "cml2_0": "<cml_ip_address>",
            "cml2_1": "<cml_ip_address>",
            "cml2_2": "<cml_ip_address>",
            "cml2_3": "<cml_ip_address>",
            "cml2_4": "<cml_ip_address>",
            "cml2_5": "<cml_ip_address>",
            "cml2_6": "<cml_ip_address>",
            "cml2_7": "<cml_ip_address>",
            "cml2_8": "<cml_ip_address>",
            "cml2_9": "<cml_ip_address>",
            "api_server": "<python_container_ip_address>",
            "selenium_hub": "<selenium_hub_container_ip_address>",
            "selenium_chrome01": "<selenium_chrome01_container_ip_address>",
            "selenium_chrome02": "<selenium_chrome02_container_ip_address>",
            "breakout_tool0": "<breakout_tool_ip_address>",
            "breakout_tool1": "<breakout_tool_ip_address>",
            "breakout_tool2": "<breakout_tool_ip_address>",
            "breakout_tool3": "<breakout_tool_ip_address>3",
            "breakout_tool4": "<breakout_tool_ip_address>4",
            "breakout_tool5": "<breakout_tool_ip_address>",
            "breakout_tool6": "<breakout_tool_ip_address>",
            "breakout_tool7": "<breakout_tool_ip_address>",
            "breakout_tool8": "<breakout_tool_ip_address>",
            "breakout_tool9": "<breakout_tool_ip_address>",
            "controller": "<controller_tool_ip_address>",
            "num_cml2": "<Number of CML2s to control>",
            "phsical_nic": "<NIC name of docker host>"
        }

#!user/bin/python

import os
import subprocess
import time
import env

env_object = env.MyEnv()

cmd_create_macvlan = [
    "docker", "network", "create", "-d", "macvlan",
    "--subnet={0}".format(env_object.my_env["subnet"]),
    "--gateway={0}".format(env_object.my_env["gateway"]),
    "-o", "parent={0}".format(env_object.my_env["phsical_nic"]),
    "macvlan"
]
copy_env_file = [
    "cp", "env.py", "./docker_file/python/cgi-bin/"
]
tar_cml2s_index = [
    "tar", "-zcvf", "./docker_file/controller/html/cml2s.tar.gz",
    "cml2s/"
]
copy_html_file = [
    "cp", "index.html", "./docker_file/controller/html/"
]
tar_virl_data_file = [
    "tar", "-zcvf", "./docker_file/python/cgi-bin/virl_data.tar.gz",
    "virl_data/"
]
download_break_out_tool = [
    "wget", "--no-check-certificate",
    "https://{0}/breakout/breakout-linux-x86_amd64".format(
        env_object.my_env["cml2_0"])
]
cmd_build_api_container = [
    "docker", "build", "-t", "py", "."
]
cmd_build_controller_container = [
    "docker", "build", "-t", "ctl", "."
]
cmd_build_breakout_container = [
    "docker", "build", "-t", "br", "."
]
cmd_run_api_container = [
    "docker", "run", "-it", "-d", "--name", "py", "--network", "macvlan",
    "--ip", env_object.my_env["api_server"], "-p", "80:80", "py"
]
cmd_run_controller_container = [
    "docker", "run", "-it", "-d", "--name", "ctl", "--network", "macvlan",
    "--ip", env_object.my_env["controller"], "-p", "80:80", "ctl"
]
cmd_run_selenium_hub_container = [
    "docker", "run", "-it", "-d", "--name", "selenium-hub", "--network",
    "macvlan", "--ip", env_object.my_env["selenium_hub"], "-p", "4444:4444",
    "-e", "GRID_BROWSER_TIMEOUT=120", "-e", "GRID_TIMEOUT=150", "-e",
    "GRID_MAX_SESSION=30", "selenium/hub:3.14.0-helium"
]
cmd_run_chrome0_container = [
    "docker", "run", "-it", "-d", "--name", "chrome0", "--network", "macvlan",
    "--ip", env_object.my_env["selenium_chrome01"], "-p", "5900:5900", "-p",
    "5555:5555", "-e", "NODE_MAX_INSTANCES=5", "-e", "NODE_MAX_SESSION=5", "-e",
    "HUB_PORT_4444_TCP_ADDR={0}".format(env_object.my_env["selenium_hub"]),
    "-e", "HUB_PORT_4444_TCP_PORT=4444", "-e",
    'REMOTE_HOST="http://{0}:5555"'.format(
        env_object.my_env["selenium_chrome01"]),
    "selenium/node-chrome-debug:3.14.0-helium"
]
cmd_run_chrome1_container = [
    "docker", "run", "-it", "-d", "--name", "chrome1", "--network", "macvlan",
    "--ip", env_object.my_env["selenium_chrome02"], "-p", "5900:5900", "-p",
    "5555:5555", "-e", "NODE_MAX_INSTANCES=5", "-e", "NODE_MAX_SESSION=5", "-e",
    "HUB_PORT_4444_TCP_ADDR={0}".format(env_object.my_env["selenium_hub"]),
    "-e", "HUB_PORT_4444_TCP_PORT=4444", "-e",
    'REMOTE_HOST="http://{0}:5555"'.format(
        env_object.my_env["selenium_chrome02"]),
    "selenium/node-chrome-debug:3.14.0-helium"
]

python_containaer_path = './docker_file/python/'
breakout_tool_containaer_path = './docker_file/breakout_tool/'
controller_container_path = './docker_file/controller/'
root_path = '../../'
index_file_path = './index.html'

subprocess.run(cmd_create_macvlan)
subprocess.run(copy_env_file)
if os.path.isfile(index_file_path) is True:
    subprocess.run(tar_cml2s_index)
    subprocess.run(copy_html_file)
    os.chdir(controller_container_path)
    subprocess.run(cmd_build_controller_container)
    os.chdir(root_path)
else:
    subprocess.run(["echo", "Index files is nothing!!"])
subprocess.run(tar_virl_data_file)
os.chdir(python_containaer_path)
subprocess.run(cmd_build_api_container)
os.chdir(root_path)
os.chdir(breakout_tool_containaer_path)
subprocess.run(download_break_out_tool)
subprocess.run(cmd_build_breakout_container)
os.chdir(root_path)
subprocess.run(cmd_run_api_container)
if os.path.isfile(index_file_path) is True:
    subprocess.run(cmd_run_controller_container)
else:
    subprocess.run(["echo", "Index files is nothing!!"])
subprocess.run(cmd_run_selenium_hub_container)
subprocess.run(cmd_run_chrome0_container)
subprocess.run(cmd_run_chrome1_container)
for num in range(int(env_object.my_env["num_cml2"])):
    cmd_run_breakout_container = [
        "docker", "run", "-it", "-d", "--name", "br{0}".format(num),
        "--network", "macvlan", "--ip",
        env_object.my_env["breakout_tool{0}".format(num)], "-p", "8080:8080",
        "br"
    ]
    cmd_exec_breakout_container = [
        "docker", "exec", "-it", "-d", "br{0}".format(num),
        "/opt/breakout-linux-x86_amd64", "-listen",
        env_object.my_env["breakout_tool{0}".format(num)], "ui"
    ]

    subprocess.run(cmd_run_breakout_container)
    time.sleep(5)
    subprocess.run(cmd_exec_breakout_container)

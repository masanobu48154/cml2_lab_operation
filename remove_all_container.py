#!user/bin/python

import os
import subprocess
import env

env_object = env.MyEnv()
cmd_rm_api_container = [
    'docker', 'rm', '-f', 'py'
]
cmd_rm_ctl_container = [
    'docker', 'rm', '-f', 'ctl'
]
cmd_rm_chrome0_container = [
    'docker', 'rm', '-f', 'chrome0'
]
cmd_rm_chrome1_container = [
    'docker', 'rm', '-f', 'chrome1'
]
cmd_rm_selenium_hub_container = [
    'docker', 'rm', '-f', 'selenium-hub'
]
cmd_rmi_api_image = [
    'docker', 'rmi', 'py'
]
cmd_rmi_ctl_image = [
    'docker', 'rmi', 'ctl'
]
cmd_rmi_breakout_tool_image = [
    'docker', 'rmi', 'br'
]
cmd_rmi_selenium_chrome_image = [
    'docker', 'rmi', 'selenium/node-chrome-debug:3.14.0-helium'
]
cmd_rmi_selenium_hub_image = [
    'docker', 'rmi', 'selenium/hub:3.14.0-helium'
]
cmd_rm_macvlan_network = [
    'docker', 'network', 'rm', 'macvlan'
]
rm_break_out_tool = [
    "rm", "breakout-linux-x86_amd64"
]
rm_virl_data = [
    "rm", "virl_data.tar.gz"
]
rm_env = [
    "rm", "env.py"
]
rm_html_file = [
    "rm", "index.html"
]
rm_cml2s_tar = [
    "rm", "cml2s.tar.gz"
]
rm_cml2s_dir = [
    "rm", "-r", "cml2s"
]

breakout_containaer_path = './docker_file/breakout_tool/'
python_containaer_cgi_path = './docker_file/python/cgi-bin/'
controller_containaer_html_path = './docker_file/controller/html/'
root_path = '../../'
root_path2 = '../../../'

subprocess.run(cmd_rm_api_container)
subprocess.run(cmd_rm_ctl_container)

for num in range(int(env_object.my_env["num_cml2"])):
    cmd_rm_breakout_tool_container = [
        'docker', 'rm', '-f', 'br{0}'.format(num)
    ]
    subprocess.run(cmd_rm_breakout_tool_container)


subprocess.run(cmd_rm_chrome0_container)
subprocess.run(cmd_rm_chrome1_container)
subprocess.run(cmd_rm_selenium_hub_container)
subprocess.run(cmd_rmi_api_image)
subprocess.run(cmd_rmi_ctl_image)
subprocess.run(cmd_rmi_breakout_tool_image)
subprocess.run(cmd_rmi_selenium_chrome_image)
subprocess.run(cmd_rmi_selenium_hub_image)
subprocess.run(cmd_rm_macvlan_network)
os.chdir(breakout_containaer_path)
subprocess.run(rm_break_out_tool)
os.chdir(root_path)
os.chdir(python_containaer_cgi_path)
subprocess.run(rm_virl_data)
subprocess.run(rm_env)
os.chdir(root_path2)
subprocess.run(rm_html_file)
subprocess.run(rm_cml2s_dir)
os.chdir(controller_containaer_html_path)
subprocess.run(rm_html_file)
subprocess.run(rm_cml2s_tar)

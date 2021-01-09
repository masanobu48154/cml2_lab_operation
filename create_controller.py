#!user/bin/python

import glob
import os
import env
import textwrap


def get_labs_list():
    """
    A function that lists the names of lab configuration yaml files stored in
    virl_data.

    Returns
    -------
    list
        List of names of yaml files that define the lab configuration.
    """
    yaml_files = []
    files = glob.glob("./virl_data/*")
    for file in files:
        yaml_files.append(os.path.split(file)[1].replace(".yaml", ""))
    return yaml_files


def get_cml2s_list(env_object):
    """
    A function that names all of the CML2s you have.

    Parameters
    ----------
    env_object : objest
        Objest of env.MyEnv()

    Returns
    -------
    list
        List of names of CML2s
    """
    cms2s_list = ["cml2_{0}".format(cml2s) for cml2s in range(
        int(env_object.my_env["num_cml2"]))]
    return cms2s_list


def create_root_index(ctl_addr, cml2_name_list):
    """
    A function that creates an index file for the root directory.
    You can select the cml2 you want to control.

    Parameters
    ----------
    ctl_addr : str
        Address of Controller
    cml2_name_list : list
        list of CML2 name
    """
    root_index_path = "./index.html"
    root_index = textwrap.dedent('''\
        <Content-type: text/html>

        <html>
    ''')
    for cmlist in cml2_name_list:
        root_index += textwrap.dedent('''\
            <a href="http://{0}/cml2s/{1}"><i>{1}</i></a><br>
        '''.format(ctl_addr, cmlist))
    root_index += '</html>'
    with open(root_index_path, "w") as f:
        f.write(root_index)


def create_index(
    cml2_name, cml2_addr, breakout_addr, env_object, telnet_port_list
):
    """
    This function creates an index file that provides the ability to build
    a lab in CML2 and connect to a node in CML2 via a breakout tool.
    CML2 and breakout tools must be paired.

    Parameters
    ----------
    cml2_name : str
        Name of CML2
    cml2_addr : str
        Address of CML2
    breakout_addr : str
        Address of Breakout tool
    env_object : object
        Objest of env.MyEnv()
    telnet_port_list : list
        List of telnet port for connecting to nodes in CML2
    """
    os.makedirs("./cml2s/{0}".format(cml2_name))
    index_path = "./cml2s/{0}/index.html".format(cml2_name)
    index = textwrap.dedent('''\
        <Content-type: text/html>

        <html>
    ''')
    index += textwrap.dedent('''\
        <form action="http://{0}/cgi-bin/cml2_rest_api.py" method="post">
    '''.format(env_object.my_env["api_server"]))
    for tech in get_labs_list():
        index += textwrap.dedent('''\
            <input type="radio" name="host" value="lab_{0}_{1}"><i>RESTART_{1}\
            </i><br><br>
        '''.format(cml2_addr, tech))
    index += textwrap.dedent('''\
        <input type="radio" name="host" value="break_{0}_{1}"><i>BREAKOUT Tool\
        </i><br><br>
        <input type="submit" value="RUN">
        </form>
    '''.format(cml2_addr, breakout_addr))
    for node_number, node_port in enumerate(telnet_port_list):
        index += textwrap.dedent('''\
            <a href="telnet://{0}:{1}"><i>node {2}</i></a><br>
        '''.format(breakout_addr, node_port, node_number))
    index += '</html>'
    with open(index_path, "w") as f:
        f.write(index)


env_object = env.MyEnv()

for num, i in enumerate(get_cml2s_list(env_object)):
    create_index(
        i,
        env_object.my_env[i],
        env_object.my_env["breakout_tool{}".format(num)],
        env_object,
        [port for port in range(9000, 9040, 2)]
    )

create_root_index(env_object.my_env["controller"], get_cml2s_list(env_object))

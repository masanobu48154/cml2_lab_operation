#!user/bin/python

import requests
import time
import urllib3
import env
import json
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)


class Cml2:
    """
    A class that imports and starts a new lab
    after deleting all the labs running on CML2.

    How to call:
        1. Create a object with the CML2 lab address.
        2. Execute delete_labs function and start_lab.
    """

    def __init__(self, host):
        """
        Parameters
        ----------
        host : str
            CML2 lab address or FQDN
        """
        env_object = env.MyEnv()
        login_data_dic = {
            "username": env_object.my_env["your_username"],
            "password": env_object.my_env["your_password"]
        }
        self.host = host
        self.login_data = json.dumps(login_data_dic)
        self.yaml_path = './virl_data/{0}.yaml'

    def get_bearer(self):
        """
        Function to get Authentication token.
        This function requires a JSON object that holds authentication data.

        Returns
        -------
        str
            Authentication token
        """
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "accept": "application/json"}
        login_url = "https://{0}/api/v0/authenticate".format(self.host)
        s = requests.session()
        res_post_login = s.post(
            login_url, data=self.login_data, headers=headers, verify=False)
        return res_post_login.json()

    def import_lab(self, bearer, tech):
        """
        Function to import lab.
        This function requires a yaml file that defines the lab configuration.

        Parameters
        ----------
        bearer : str
            Authentication token
        tech : str
            The name of the yaml file.
            The location of this yaml file must be defined in 'self.yaml_path'.

        Returns
        -------
        str
            Imported lab ID
        """
        create_urlv1 = "https://{0}/api/v0/import?title={1}".format(
            self.host, tech)
        headers = {"Content-type": "text/xml", "accept": "application/json",
                   "Authorization": "Bearer {0}".format(bearer)}
        with open(self.yaml_path.format(tech), 'rb') as f:
            virl_data = f.read()
        s = requests.session()
        res_post_virlv1 = s.post(
            create_urlv1, headers=headers, data=virl_data, verify=False)
        import_lab_dic = res_post_virlv1.json()
        return import_lab_dic["id"]

    def start_lab(self, tech):
        """
        Function to import and start lab.
        This function requires a yaml file that defines the lab configuration.

        Parameters
        ----------
        tech : str
            The name of the yaml file.
            The location of this yaml file must be defined in 'self.yaml_path'.
        """
        bearer = self.get_bearer()
        lab_id = self.import_lab(bearer, tech)
        time.sleep(10)
        start_url = "https://{0}/api/v0/labs/{1}/start".format(
            self.host, lab_id)
        headers = {"Content-type": "application/json",
                   "accept": "application/json",
                   "Authorization": "Bearer {0}".format(bearer)}
        s = requests.session()
        res_put_start = s.put(start_url, headers=headers, verify=False)
        return res_put_start.json()

    def get_labid(self, bearer):
        """
        Function to get the lab id of the running labs.

        Parameters
        ----------
        bearer : str
            Authentication token

        Returns
        -------
        str
            Runing lab ID
        """
        get_labs_url = "https://{0}/api/v0/labs".format(self.host)
        headers = {"accept": "application/json",
                   "Authorization": "Bearer {0}".format(bearer)}
        s = requests.session()
        res_get_labs = s.get(get_labs_url, headers=headers, verify=False)
        return res_get_labs.json()

    def stop_labs(self, bearer):
        """
        Function to stop all labs.

        Parameters
        ----------
        bearer : str
            Authentication token

        Returns
        -------
        dictionary
            Key = Lab ID, Value = API Status
        """
        stop_labs_dic = {}
        for i in self.get_labid(bearer):
            stop_url = "https://{0}/api/v0/labs/{1}/stop".format(self.host, i)
            headers = {"Content-type": "application/json",
                       "accept": "application/json",
                       "Authorization": "Bearer {0}".format(bearer)}
            s = requests.session()
            res_put_stop = s.put(stop_url, headers=headers, verify=False)
            time.sleep(20)
            stop_labs_dic[i] = res_put_stop.json()
        return stop_labs_dic

    def wipe_labs(self, bearer):
        """
        Function to stop and wipe all labs.

        Parameters
        ----------
        bearer : str
            Authentication token

        Returns
        -------
        dictionary
            Key = Lab ID, Value = API Status
        """
        wipe_labs_dic = {}
        self.stop_labs(bearer)
        for i in self.get_labid(bearer):
            wipe_url = "https://{0}/api/v0/labs/{1}/wipe?force=true".format(
                self.host, i)
            headers = {"Content-type": "application/json",
                       "accept": "application/json",
                       "Authorization": "Bearer {0}".format(bearer)}
            s = requests.session()
            res_put_wipe = s.put(wipe_url, headers=headers, verify=False)
            time.sleep(5)
            wipe_labs_dic[i] = res_put_wipe.json()
        return wipe_labs_dic

    def delete_labs(self):
        """
        Function to stop, wipe and delete all labs.

        Returns
        -------
        dictionary
            Key = Lab ID, Value = API Status
        """
        delete_labs_dic = {}
        bearer = self.get_bearer()
        self.wipe_labs(bearer)
        for i in self.get_labid(bearer):
            delete_labs_url = "https://{0}/api/v0/labs/{1}".format(
                self.host, i)
            headers = {"accept": "application/json",
                       "Authorization": "Bearer {0}".format(bearer)}
            s = requests.session()
            res_delete_labs = s.delete(
                delete_labs_url, headers=headers, verify=False)
            delete_labs_dic[i] = res_delete_labs
        return delete_labs_dic

    def get_node(self):
        """
        Function to extract nodes placed in lab.
        """
        lab_nodes_dic = {}
        bearer = self.get_bearer()
        for i in self.get_labid(bearer):
            getnodes_url = "https://{0}/api/v0/labs/{1}/nodes".format(
                self.host, i)
            headers = {"Content-type": "application/json",
                       "accept": "application/json",
                       "Authorization": "Bearer {0}".format(bearer)}
            s = requests.session()
            RES_GET_NODES = s.get(getnodes_url, headers=headers, verify=False)
            # return  RES_GET_NODES.json()
            lab_nodes_dic[i] = RES_GET_NODES.json()
        return lab_nodes_dic

    def check_converged(self):
        """
        Function to check if lab converged.
        """
        bearer = self.get_bearer()
        for i in self.get_labid(bearer):
            check_url = "https://{0}/api/v0/labs/{1}/check_if_converged".format(
                self.host, i)
            headers = {"Content-type": "application/json",
                       "accept": "application/json",
                       "Authorization": "Bearer {0}".format(bearer)}
            s = requests.session()
            RES_CHECK = s.get(getnodes_url, headers=headers, verify=False)
            # return  RES_GET_NODES.json()
        return RES_CHECK

if __name__ == '__main__':
    method = input("Start(s) or Stop(p) or Get Nodes(g): ")
    if method == "s":
        host = input("Target CML Address : ")
        tech = input("Import Technology : ")
        ob = Cml2(host)
        print(ob.start_lab(tech))
    elif method == "p":
        host = input("Target CML Address : ")
        ob = Cml2(host)
        print(ob.delete_labs())
    elif method == "g":
        host = input("Target CML Address : ")
        ob = Cml2(host)
        print(ob.get_node())
    elif method == "c":
        host = input("Target CML Address : ")
        ob = Cml2(host)
        print(ob.check_converged())
    else:
        print("Input 'S' or 'p' or 'g'!!")

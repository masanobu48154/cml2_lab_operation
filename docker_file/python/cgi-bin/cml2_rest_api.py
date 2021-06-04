#!/usr/bin/python3

from urllib3.exceptions import InsecureRequestWarning
import textwrap
import urllib3
import apple
import breakout
import cgi
import cgitb
cgitb.enable()
urllib3.disable_warnings(InsecureRequestWarning)

form = cgi.FieldStorage()
tech = form.getvalue('host', '')
tech_split = tech.split("_")
tech_operation = tech_split[0]
tech_host = tech_split[1]
html_response = textwrap.dedent('''\
    Status: 200 OK
    Content-type: text/html

    <HTML>
     <HEAD>
      <TITLE>Python Device Setting</TITLE>
     </HEAD>
     <BODY>
      <H1>Status {0}</H1>
      <a href="#" onclick="javascript:window.history.back(-1);return false;">\
        Back to previous page and Wait a few minutes...</a>
      <br>
     </BODY>
    </HTML>
''')

if tech_operation == "break":
    breakhost = tech_split[2]
    ob = breakout.BreakOut(tech_host, breakhost)
    BREAK_RES = ob.breakout()
    print(html_response.format(BREAK_RES))
elif tech_operation == "lab":
    tech_labid = tech_split[2]
    ob = apple.Cml2(tech_host)
    ob.delete_labs()
    ob.start_lab(tech_labid)
    print(html_response.format(tech))

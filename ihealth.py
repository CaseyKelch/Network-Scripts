import requests
import json
import glob
import os
import time


sess = requests.session()


def ihealth_auth(health_user, health_pass):

    # Creates session object for authentication and future iHealth API calls.
    url = "https://api.f5.com/auth/pub/sso/login/ihealth-api"
    json_auth = json.dumps({
        "user_id": health_user,
        "user_secret": health_pass
    })

    sess.get(url, proxies=proxy_dict)
    req = sess.post(url="https://api.f5.com/auth/pub/sso/login/ihealth-api", data=json_auth)
    print("Authentication Granted: {0}".format(req.text))


def download_diag(diag_dir):

    # Download Diagnostics PDF from ihealth API.
    qkview_data = sess.get("https://ihealth-api.f5.com/qkview-analyzer/api/qkviews.json")
    data = json.loads(qkview_data.text)
    for val in data['id']:
        diag_data = sess.get("https://ihealth-api.f5.com/qkview-analyzer/api/qkviews/{0}/diagnostics.json"
                             .format(val))
        hostname = json.loads(diag_data.text)
        print("Downloading PDF for " + hostname["system_information"]["hostname"])

        qkview_pdf = sess.get("https://ihealth-api.f5.com/qkview-analyzer/api/qkviews/{0}/diagnostics.pdf"
                              .format(val))
        with open(diag_dir + hostname["system_information"]["hostname"] + ".pdf", 'wb') \
                as f:
            for chunk in qkview_pdf.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)


def upload_qkview(file_name):
    # Upload .qkview files from local directory.
    files = {'qkview': open(file_name, 'rb')}
    values = {'visible_in_gui': 'True'}

    print("Uploading {0} to iHealth...".format(file_name))
    # Upload qkview
    post_qkview = sess.post("https://ihealth-api.f5.com/qkview-analyzer/api/qkviews",
                            files=files, data=values)
    print(post_qkview)

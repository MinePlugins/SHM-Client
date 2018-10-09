#! /usr/bin/python
# -*- coding:utf-8 -*-

# License MIT

import datetime
import hashlib
import json
import os
import platform
import subprocess
import time
from threading import Thread

import psutil
import requests
from flask import Flask, flash
from flask import render_template, session, redirect, url_for, request, json

#
#  Variable systeme PATH
#

PATH_MONITORING = 'static/data/monitoring.json'
PATH_DATA = 'static/data/data.json'
PATH_LOG = '../log/log.txt'
PATH_FOLDER = 'static/data'
DEFAULT_CONFIG = '{ \"config\": { \"autorestart\": null,' \
                 ' \"bname\": \"Default\", \"debug\": null,' \
                 ' \"ext\": \"http://google.fr\", \"id\": \"1\",' \
                 ' \"ip\": \"0.0.0.0\", \"password\": \"\",' \
                 ' \"port\": \"5000\", \"refreshtime\": \"30\",' \
                 ' \"sysloghost\": \"172.16.196.133\",' \
                 ' \"syslogport\": \"3000\", \"uid\": \"\", ' \
                 '\"isinstall\": false, \"passphrase\": \"\", \"version\": \"1.1\",' \
                 ' \"username\": \"\"}}'

DEFAULT_MONITORING = '{  \"process\":  {  }}'
#
# Detection de la plateforme
#

if platform.uname()[1] == 'raspberrypi':
    osn = "RPI"
elif platform.uname()[1] == 'tinkerboard':
    osn = "TB"
elif platform.uname()[0] == "Windows":
    osn = "Win"
else:
    osn = "Other"

app = Flask(__name__, static_folder='static', static_url_path='/static')

data = list
monitoring = []
flashs = []
stopped = False
ping = None
pingext = None


def logger(msg, type="info"):
    x = datetime.datetime.now()
    f = open(PATH_LOG, "a+", encoding='utf-8')
    f.write(str("[" + str(x.year) + "-" + str(x.month) + "-" + str(x.day) + "][" + str(x.hour) + ":" + str(
        x.minute) + ":" + str(x.second) + "] [" + type + "] " + msg + "\n"))
    tsyslog.logger(type, msg)
    f.close()


def startup():
    global data
    global monitoring
    if osn == "TB":
        bashCommand = "sudo chmod 777 /sys/class/thermal/thermal_zone0/temp"
        bashCommand2 = "sudo chmod 777 /sys/class/thermal/thermal_zone1/temp"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        process.communicate()
        process2 = subprocess.Popen(bashCommand2.split(), stdout=subprocess.PIPE)
        process2.communicate()

    if not os.path.exists(PATH_FOLDER):
        os.makedirs(PATH_FOLDER)

    if not os.path.exists(PATH_MONITORING):
        with open(PATH_MONITORING, 'w', encoding='utf-8'):
            pass
        monitoring = json.loads(DEFAULT_MONITORING)
    else:
        try:
            monitoring = json.load(open(PATH_MONITORING))
        except:
            monitoring = json.loads(DEFAULT_MONITORING)

    if not os.path.exists(PATH_LOG):
        with open(PATH_LOG, 'w', encoding='utf-8'):
            pass
    else:
        open(PATH_LOG, 'w').close()
    if not os.path.exists(PATH_DATA):
        with open(PATH_DATA, 'w', encoding='utf-8'):
            pass
        data = json.loads(DEFAULT_CONFIG)
    else:
        try:
            data = json.load(open(PATH_DATA))
        except:
            data = json.loads(DEFAULT_CONFIG)


def encrypt_string(text):
    sha_signature = \
        hashlib.sha256(text.encode()).hexdigest()
    return sha_signature

def datawrite():
    global data
    tsyslog.sendUpdate()
    logger("Modification des données", "warning")
    with open(PATH_DATA, 'w') as outfile:
        json.dump(data, outfile)

def monitoringwrite():
    global monitoring
    logger("Modification des monitorings", "warning")
    with open(PATH_MONITORING, 'w') as outfile:
        print(monitoring)
        json.dump(monitoring, outfile)

def measure_temps():
    if osn == "TB":
        tempcpu = open("/sys/class/thermal/thermal_zone0/temp", "r+").readline()
        tempgpu = open("/sys/class/thermal/thermal_zone1/temp", "r+").readline()
        tempcpu = int(tempcpu) / 1000
        tempgpu = int(tempgpu) / 1000
    else:
        tempgpu = 0
        tempcpu = 0
    return [tempcpu, tempgpu]


@app.route('/success')
def success():
    datawrite()
    return render_template('success.html', titre="SHM")


@app.route('/reboot')
def reboot():
    try:
        if 'username' in session:
            bashCommand = "sudo reboot"
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            process.communicate()
            return render_template('index.html', username=session['username'], titre="SHM",
                                   id=data['config']['id'])
    except:
        return render_template('login.html', titre="SHM")
    return render_template('index.html', titre="SHM")


@app.route('/install', methods=['GET', 'POST'])
def install():
    if request.method == 'POST':
        data['config']['password'] = encrypt_string(request.form.get('password'))
        data['config']['username'] = request.form.get('username')
        return redirect(url_for('install2'))
    else:
        return render_template('install.html', titre="SHM")


@app.route('/install2', methods=['GET', 'POST'])
def install2():
    if request.method == 'POST':
        data['config']['ip'] = request.form.get('ipp')
        data['config']['port'] = request.form.get('portp')
        data['config']['debug'] = request.form.get('debug')
        data['config']['sysloghost'] = request.form.get('sysloghost')
        data['config']['syslogport'] = request.form.get('syslogport')
        data['config']['refreshtime'] = request.form.get('refreshtime')
        data['config']['ext'] = request.form.get('ext')
        data['config']['bname'] = request.form.get('name')
        data['config']['passphrase'] = request.form.get('passphrase')
        app.secret_key = data['config']['passphrase']
        data['config']['isinstall'] = True
        return redirect(url_for('success'))
    else:
        return render_template('install2.html', titre="SHM")


@app.route('/config', methods=['GET', 'POST'])
def config():
    if not data['config']['isinstall']:
        return redirect(url_for('install'))
    if data['config']['debug']:
        logger("Accés à la page config", "debug")
    if 'username' in session:
        if request.method == 'POST':
            data['config']['ip'] = request.form.get('ipp')
            data['config']['port'] = request.form.get('portp')
            if request.form.get('password'):
                data['config']['password'] = encrypt_string(request.form.get('password'))
            else:
                data['config']['password'] = data['config']['password']
            data['config']['debug'] = request.form.get('debug')
            data['config']['sysloghost'] = request.form.get('sysloghost')
            data['config']['syslogport'] = request.form.get('syslogport')
            data['config']['refreshtime'] = request.form.get('refreshtime')
            data['config']['ext'] = request.form.get('ext')
            data['config']['bname'] = request.form.get('name')
            data['config']['passphrase'] = request.form.get('passphrase')

            datawrite()
            return render_template('config.html', titre="SHM", debug=data['config']['debug'],
                                   ipp=data['config']['ip'], portp=data['config']['port'],
                                   sysloghost=data['config']['sysloghost'], syslogport=data['config']['syslogport'],
                                   uid=data['config']['uid'], refreshtime=data['config']['refreshtime'],
                                   name=data['config']['bname'], ext=data['config']['ext'])
        else:
            return render_template('config.html', titre="SHM", debug=data['config']['debug'],
                                   ipp=data['config']['ip'], portp=data['config']['port'],
                                   sysloghost=data['config']['sysloghost'], syslogport=data['config']['syslogport'],
                                   uid=data['config']['uid'], refreshtime=data['config']['refreshtime'],
                                   name=data['config']['bname'], ext=data['config']['ext'])
    else:
        return render_template('login.html', titre="SHM")


@app.route('/pid/<int:pid>')
def kill_pid(pid):
    if not data['config']['isinstall']:
        return redirect(url_for('install'))
    if data['config']['debug']:
        logger("Accés à la page kill_pid", "debug")
    if 'username' in session:
        if psutil.pid_exists(pid):
            logger("Kill du processus" + str(psutil.Process(pid).name()) + " (PID: " + str(pid) + ")", "warning")
            psutil.Process(pid).kill()
        return redirect(url_for('pid'))
    else:
        return render_template('login.html', titre="SHM")


@app.route('/pid')
def pid():
    global osn
    global monitoring
    if not data['config']['isinstall']:
        return redirect(url_for('install'))
    if data['config']['debug']:
        logger("Accés à la page pid", "debug")
    if 'username' in session:
        try:
            tab = []
            for i in psutil.pids():
                try:
                    if psutil.Process(i).name() in monitoring['process']:
                        tab.append([psutil.Process(i), True])
                    else:
                        tab.append([psutil.Process(i), False])
                except Exception as e:
                    continue
            return render_template('pids.html', pid=tab, titre="SHM", plateforme=osn, username=session['username'])

        except Exception as e:
            flash(str(e))

            return redirect(url_for('pid'))

    else:
        return render_template('login.html', titre="SHM")


@app.route('/pidmonitor/<string:name>')
def pidmonitoradd(name):
    global osn
    global monitoring
    if data['config']['debug']:
        logger("Accés à la page pid", "debug")
    if 'username' in session:
        try:
            for i in psutil.pids():
                if psutil.Process(i).name() == name:
                    monitoring['process'][name] = {"pid": psutil.Process(i).ppid()}
                    monitoringwrite()
                    return render_template('pidmonitor.html', i=psutil.Process(i), titre="SHM", plateforme=osn,
                                           username=session['username'])

        except Exception as e:
            flash(str(e))

            return redirect(url_for('pid'))

    else:
        return render_template('login.html', titre="SHM")


@app.route('/pidmonitor')
def pidmonitor():
    global osn
    if not data['config']['isinstall']:
        return redirect(url_for('install'))
    if data['config']['debug']:
        logger("Accés à la page pid", "debug")
    if 'username' in session:
        try:
            tab = []
            for i in psutil.pids():
                tab.append(psutil.Process(i))
            return render_template('pids.html', pid=tab, titre="SHM", plateforme=osn, username=session['username'])

        except Exception as e:
            flash(str(e))

            return redirect(url_for('pidmonitor'))

    else:
        return render_template('login.html', titre="SHM")

@app.route('/log')
def log():
    if not data['config']['isinstall']:
        return redirect(url_for('install'))
    if data['config']['debug']:
        logger("Accés à la page log", "debug")
    if 'username' in session:
        with open(PATH_LOG) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        content.reverse()
        return render_template('log.html', log=content, titre="SHM", username=session['username'])
    else:
        return render_template('login.html', titre="SHM")


@app.route('/status')
def status():
    if not data['config']['isinstall']:
        return redirect(url_for('install'))
    if data['config']['debug']:
        logger("Accés à la page status", "debug")
    if 'username' in session:
        temp = measure_temps()
        return render_template('status.html', titre="Genius-hello", username=session['username'],
                               cpu=psutil.cpu_percent(), ram=psutil.virtual_memory().percent,
                               disk=psutil.disk_usage('/').percent, temp=temp, platform=platform.uname(),
                               id=data['config']['id'], uid=data['config']['uid'], name=data['config']['bname'])
    else:
        return render_template('login.html', titre="SHM")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if not data['config']['isinstall']:
        return redirect(url_for('install'))
    if data['config']['debug']:
        logger("Accés à la page login", "debug")
    if request.method == 'POST':
        password = encrypt_string(request.form['password'])

        if password.lower() == data['config']['password'].lower() and request.form['username'].lower() == \
                data['config'][
            'username'].lower():
            session['username'] = request.form['username']
            print("logged in")
            flash("Connexion réussi")
            return render_template('index.html', titre="Genius-Hello", username=session['username'],
                                   id=data['config']['id'])
        else:
            flash("Mot de passe ou identifiant incorrect")

            return render_template('login.html', titre="Genius-Hello")

    else:
        flash("Merci de bien vouloir vous connecté")
        return render_template('login.html', titre="Genius-Hello")


@app.route('/logout')
def logout():
    if not data['config']['isinstall']:
        return redirect(url_for('install'))
    if data['config']['debug']:
        logger("Deconnection", "debug")
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/')
def index():
    if not data['config']['isinstall']:
        return redirect(url_for('install'))
    if data['config']['debug']:
        logger("Accés à la page Accueil", "debug")
    try:
        if 'username' in session:
            return render_template('index.html', username=session['username'], titre="SHM",
                                   id=data['config']['id'])
    except:
        return render_template('login.html', titre="SHM")
    else:
        return render_template('login.html', titre="SHM")


class syslog(Thread):
    def __init__(self):
        global data
        Thread.__init__(self)
        self.platform = platform.uname()
        self.ip = data['config']['sysloghost']
        self.port = data['config']['syslogport']
        self.headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache",
        }

    def run(self):
        global ping
        global pingext
        if len(data['config']['uid']) < 5 and data['config']['uid'] == None:
            self.first()
        else:
            while True:
                url = "http://" + str(self.ip) + ":" + str(self.port) + "/state/" + str(data['config']['uid'])

                try:
                    r = requests.post(url, data={'cpu': psutil.cpu_percent(), 'ram': psutil.virtual_memory().percent,
                                                 'disk': psutil.disk_usage('/').percent, 'tempCpu': measure_temps()[0],
                                                 'tempGpu': measure_temps()[1], 'pingSys': ping, 'pingExt': pingext,
                                                 'refreshTime': data['config']['refreshtime']},
                                      headers=self.headers)
                    ping = r.elapsed.microseconds / 1000
                    if data['config']['debug']:
                        logger('Reponse de l\'envoie de l\'etat ' + str(r.status_code), "debug")

                    r = requests.get(data['config']['ext'], headers=self.headers)
                    pingext = r.elapsed.microseconds / 1000
                    if data['config']['debug']:
                        logger('Ping SysLog : ' + str(ping) + "ms | Ping Ext : " + str(pingext) + "ms", "debug")
                        logger('Reponse de l\'envoie de l\'etat ' + str(r.status_code), "debug")
                except Exception as e:

                    logger('Erreur lors de l\'envoie de state avec le serveur de log. Erreur : ' + str(e))
                time.sleep(int(data['config']['refreshtime']))

    def logger(self, type="info", msg="None"):
        url = "http://" + str(self.ip) + ":" + str(self.port) + "/log/" + str(data['config']['uid'])

        try:
            r = requests.post(url, data={'type': type, 'msg': msg}, headers=self.headers)
        except Exception as e:
            print('Erreur lors de l\'envoie de log avec le serveur de log. Erreur : ' + str(e))

    def first(self):
        try:
            url = "http://" + str(self.ip) + ":" + str(self.port) + "/devices"
            r = requests.post(url,
                              data={'system': self.platform.system, 'cpu': self.platform.processor,
                                    'arch': self.platform.machine,
                                    'version': self.platform.version, 'release': self.platform.release,
                                    'hardware': self.platform.node, 'name': data['config']['bname'],
                                    'refreshTime': data['config']['refreshtime'],
                                    'uid': data['config']['id']}, headers=self.headers)
            data['config']['uid'] = json.loads(r.content)['_id']
            datawrite()
            if data['config']['debug']:
                logger('Récupération de l\'UID : ' + str(data['config']['uid']), "debug")
                logger('Reponse de l\'envoie de l\'initialisation ' + str(r.status_code), "debug")

        except Exception as e:
            logger('Erreur lors de l\'inititalisation avec le serveur de log. Erreur : ' + str(e), "erreur")
        self.run()

    def sendUpdate(self):
        try:
            url = "http://" + str(self.ip) + ":" + str(self.port) + "/devices/" + str(data['config']['uid'])
            r = requests.put(url,
                             data={'system': self.platform.system, 'cpu': self.platform.processor,
                                   'arch': self.platform.machine,
                                   'version': self.platform.version, 'release': self.platform.release,
                                   'hardware': self.platform.node, 'name': data['config']['bname'],
                                   'refreshTime': data['config']['refreshtime'],
                                   'port': data['config']['port'],
                                   'ip': data['config']['ip']}, headers=self.headers)
            if data['config']['debug']:
                logger('Reponse de l\'envoie de l\'initialisation ' + str(r.status_code), "debug")
        except Exception as e:
            logger('Erreur lors de l\'inititalisation avec le serveur de log. Erreur : ' + str(e), "erreur")


if __name__ == '__main__':
    startup()
    if data['config']['isinstall']:
        app.secret_key = data['config']['passphrase']
    tsyslog = syslog()
    tsyslog.start()
    app.run(host=data['config']['ip'], port=data['config']['port'], debug=data['config']['debug'])
    tsyslog.join()

import os
import re
from threading import Thread
import time
import frida
import time
import timeout_decorator
import sys
from func_timeout import func_set_timeout



def get_activit():
    res = os.popen('adb shell dumpsys activity top')
    count = 200
    activity = []
    try:
        for i in res:
            if count == 0:
                break
            else:
                count -= 1
            temp = str(i)
            try:
                res = re.search('ACTIVITY (.*?) (.*?) pid=', temp)
                print(res.group(1))
                activity.append(res.group(1))
            except Exception as e:
                pass
    except Exception as e:
        print(str(e))
    return activity


def active_activity():
    print('active')
    start_ac = []
    for actiity in get_activit():
        if "com.miui" in actiity or "com.android.mms" in actiity:
            continue
        cmd = "adb shell am start -n {}".format(actiity)
        res = os.popen(cmd)
        for i in res:
            print(i)
        start_ac.append(actiity)
    return start_ac


def kill_activity(start_ac):
    for actiity in start_ac:
        if "com.miui" in actiity or "com.android.mms" in actiity:
            continue
        pkg, ac = actiity.split('/')
        cmd = "adb shell am force-stop {}".format(pkg)
        res = os.popen(cmd)
        print('kill', pkg)

def kill_by_actiity_name(activity_name):
    print('kill',activity_name)
    pkg,ac = activity_name.split('/')
    cmd = "adb shell am force-stop {}".format(pkg)
    res = os.popen(cmd)
    for i in res:
        print(i)
    time.sleep(2)


def active_by_activity_name(activity_name):
   # kill_by_actiity_name(activity_name)
    print('start',activity_name)
    cmd = "adb shell am start -n {}".format(activity_name)
    res = os.popen(cmd)
    for i in res:
        print(i)


def hook_by_method(activity,method_name):
    pkg, ac = activity.split('/')
    activity = activity.replace('/','')
    js_code = """
    Java.perform(
    setTimeout(function(){
    var hookClass = Java.use('%s')
    console.log('HookClass',hookClass)
    hookClass.%s.implementation = function(args){
        send('crack successful',%s)
        console.log('入参',args)
        return this.%s(args)
    }

},1000)
    );
    """%(activity,method_name,method_name,method_name)
    print(js_code)

    process = frida.get_remote_device().attach(pkg)
    script = process.create_script(js_code)
    def on_message(message, data):
        if message['type'] == 'send':
            print("[*] {0}".format(message['payload']))
        else:
            print(message)

    script.on('message', on_message)
    print('开始hook')
    script.load()
    sys.stdin.read()

def hook_by_file(file,pkg):

    import random
    with open(file,'r') as f:
        js_code = f.read()
    print(js_code)
    process = frida.get_remote_device().attach(pkg)
    script = process.create_script(js_code)
    def on_message(message, data):
        if message['type'] == 'send':
            print("[*] {0}".format(message['payload']))
        else:
            print(message)

    script.on('message', on_message)
    print('开始hook')
    script.load()

    return script


get_activit()

if __name__ == '__main__':

    # get_activit()
    # kill_by_actiity_name('com.zuiai.hh/.MainActivity')

    # pkg_name = "com.tencent.mm/.ui.LauncherUI"
    # pkg_name = get_activit()[-1]
    # active_by_activity_name(pkg_name)
    # method_name="String"
    # time.sleep(2)
    #hook_by_method(pkg_name,method_name)
    # hook_by_file('huihe.js','com.zuiai.hh')




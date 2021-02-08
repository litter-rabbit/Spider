import frida, sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

jscode = """
Java.perform(function () {
  // Function to hook is defined here
  var MainActivity = Java.use('com.example.seccon2015.rock_paper_scissors.MainActivity');

  // Whenever button is clicked
  var onClick = MainActivity.onClick;
  onClick.implementation = function (v) {
    // Show a message to know that the function got called
    send('onClick');

    // Call the original onClick handler
    onClick.call(this, v);

    // Set our values after running the original onClick handler
    this.m.value = 0;
    this.n.value = 1;
    this.cnt.value = 999;

    // Log to the console that it's done, and we should have the flag!
    console.log('Done:' + JSON.stringify(this.cnt));
  };
});
"""

idel_fish_code="""
Java.perform(function () {
    var SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
    SwitchConfig.zC.overload().implementation = function () {
        
        return false;
    }
});
"""

#process = frida.get_remote_device().attach('com.example.seccon2015.rock_paper_scissors')
process = frida.get_remote_device().attach('com.taobao.idlefish')
script = process.create_script(idel_fish_code)
script.on('message', on_message)
print('[*] Running CTF')
script.load()
sys.stdin.read()
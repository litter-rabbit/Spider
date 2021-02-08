import frida, sys




"""
var string_class = Java.use("java.lang.String")
var my_string = string_class.$new("My TeSt String#####"); 
"""

choose_code ="""
Java.choose("com.yaotong.crackme" , {
  onMatch : function(instance){ //This function will be called for every instance found by frida
    console.log("Found instance: "+instance);
    console.log("Result of secret func: " + instance.securityCheck());
  },
  onComplete:function(){}

});

"""

js_code = """
Java.perform(function () {


    var mac = Java.use('com.yaotong.crackme.MainActivity')
    if(mac == null){
        console.log('未找到',mac)
        
    }

    mac.securityCheck.overload("java.lang.String").implementation = function(x){
        send('crack successful')
        console.log(x)
        return true;
    }
    
});
"""

process = frida.get_remote_device().attach('com.yaotong.crackme')
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
import frida
import sys
rdev=frida.get_remote_device()
session=rdev.attach("包名")
scr="""
send("get in jscode")
Java.perform(function(){
var pointer = Module.findExportByName("libcore.so" , "JNI_OnLoad");
console.log("pointer: "+pointer);//                     用ida查看JNI_OnLoad 在so中的IDA      未导出函数sub_22F4
var hookpointer = '0x' +parseInt(parseInt(pointer) - parseInt('0x1AD0') + parseInt('0x22F4')).toString(16).toUpperCase();
console.log("hookpointer: "+hookpointer);
var nativePointer = new NativePointer(hookpointer);
console.log("net native pointers:"+nativePointer);
Interceptor.attach(nativePointer, {
      onEnter: function(args) {
      console.log("args: " + Memory.readCString (args[1]));
     },
     onLeave:function(retval){
}
});
})
"""
script = session.create_script(scr)
def on_message(message ,data):
    file=open(r'C:\Users\Administrator\Desktop\log.txt', 'a')
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
        file.writelines(str(message['payload'])+"\n")
        file.close()
    else:
        file.writelines(str(message)+"\n")
        file.close()
        print (message)
script.on("message" , on_message)
script.load()
sys.stdin.read()
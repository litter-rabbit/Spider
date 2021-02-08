from __future__ import print_function
import frida
import sys


def on_message(message, data):
    if message['payload']['chatroomvxid'] == None:
        print('[个人消息]: ' + message['payload']['wxid'] + ': ' + message['payload']['text'])
    else:
        print('[群消息]: ' + message['payload']['wxid'] + ': ' + message['payload']['chatroomvxid'] + ': ' +
              message['payload']['text'])


def main(target_process):
    session = frida.attach(target_process)
    script = session.create_script("""
    var ModAddress=Process.findModuleByName('wechatwin.dll');
    //console.log('ModAdress:' + ModAddress.base);
    var hookAddress=ModAddress.base.add('0x3CCB75')
    //console.log('hookAdress' + hookAddress.base)
    Interceptor.attach(hookAddress,{
        onEnter:function(args) {
            //console.log(JSON.stringify(this.context));
            var edi=this.context.edi;
            //console.log('edi:' + Memory.readPointer(edi));
            var edi1=Memory.readPointer(edi)
            var wxid=Memory.readUtf16String(Memory.readPointer(edi1.add('0x40')));
            var text=Memory.readUtf16String(Memory.readPointer(edi1.add('0x68')));
            var chatroomvxid=Memory.readUtf16String(Memory.readPointer(edi1.add('0x164')));
            send({'wxid':wxid,'text':text,'chatroomvxid':chatroomvxid})
            //console.log(wxid + ':' + text);
        }
    })
""")
    script.on('message', on_message)
    script.load()
    print("[!] Ctrl+D on UNIX, Ctrl+Z on Windows/cmd.exe to detach from instrumented program.\n\n")
    sys.stdin.read()
    session.detach()


if __name__ == '__main__':
    main('wechat.exe')
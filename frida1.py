import frida
import sys


jscode = """
Java.perform(function(){
    var vvvvv = Java.use("com.kanxue.pediy1.VVVVV");
    vvvvv.VVVV.implemention = function(){
        send("Hook Start !");
        return true;
    }
});

"""
def on_message(message, data):
    if message['type']=='send':
        print('[*] {0}'.format(message['payload']))
    else:
        print(message)


process = frida.get_remote_device().attach("com.kanxue.pediy1")
script = process.create_script(jscode)
script.on('message', on_message)
script.load()
sys.stdin.read()
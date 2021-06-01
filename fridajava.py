import frida
import sys


jscode = """
Java.perform(function(){
    var MainActivity = Java.use('com.example.testfrida.MainActivity');
    MainActivity.testFrida.implementation = function(){
        send('Statr! hook!')
        return 'Change String!'
    }
});
"""



def on_message(message, data):
    if message['type']=='send':
        print(' {0}'.format(message['payload']))
    else:
        print(message)

process=frida.get_remote_device().attach('com.example.testfrida')
script = process.create_script(jscode)
script.on('message', on_message)
script.load()
sys.stdin.read()



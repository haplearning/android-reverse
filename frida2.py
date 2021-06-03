import frida
import sys


jscode = """

"""



def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


process = frida.get_remote_device().attach('')
script = process.create_script(jscode)
script.on('message', on_message)
script.load()
sys.stdin.read()
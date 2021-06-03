import frida
import sys


jscode = """
Java.perform(function(){
    var flag = null;
    var enc1 = Java.use("java.lang.String").$new("6f452303f18605510aac694b0f5736beebf110bf");
    console.log(enc1);
    var res = null;
    for (var i1=48;i1<58;i1++)
        for (var i2 = 48;i2 < 58; i2++)
                for (var i3 = 48;i3 < 58; i3++)
                    for (var i4 = 48;i4 < 58; i4++)
                        for (var i5 = 48;i5 < 58; i5++){
                            var flag = String.fromCharCode(i1,i2,i3,i4,i5);
                            res =Java.use("java.lang.String").$new(Java.use('com.kanxue.pediy1.VVVVV').eeeee(flag));
                            if (enc1.equals(res)){
                                console.log("flag is success", flag);
                                return;
                            }
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
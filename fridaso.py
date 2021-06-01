import frida
import sys
from frida.core import Script



jscode = """
Java.perform(function(){
    //指定要Hook的so文件名和要Hook的函数名，函数名就是上面IDA导出表中显示的那个函数名
    Interceptor.attach(Module.findExportByName("libfridaso.so","Java_com_example_fridaso_FridaSoDefine_FridaSo"),{
        //进入该函数前要执行的代码，其中args是传入的参数，一般so层函数第一个参数都是JniEnv，第二个参数是jclass，从第三个参数开始才是我们java层传入的参数
        onEnter:function(args){
            send("Hook start");
            send("args[2]="+args[2]);
            send("args[3]="+args[3]);
        },
        //该函数执行结束要执行的代码，其中retval参数即是返回值
        onLeave:function(retval){
            send("return:"+retval); 
            retval.replace(0);
        }
    });
});
"""

def on_message(message, data):
    if message['type']=='send':
        print(' {0}'.format(message['payload']))
    else:
        print(message)

process=frida.get_remote_device().attach('com.example.fridaso')
script = process.create_script(jscode)
script.on('message', on_message)
script.load()
sys.stdin.read()


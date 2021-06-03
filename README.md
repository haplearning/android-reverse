# android-reverse

Some examples of android reverse



## 1、Adb 环境配置

### 1.1 、Adb 常见命令

- adb 启动和停止

  - `adb start-server`
  - `adb kill-server`

- adb 查看最顶端应用的包名和 activity 名

  - `adb shell dumpsys window | grep mCurrentFocus`

- adb 输入字符串

  - `adb shell input text "<String>"`

- adb 模拟按键

  - `adb shell input keyevent <Int>` [按键参考](https://www.huaweicloud.com/articles/aaab7697baca07f9d37854a69631a11d.html)

- adb 安装 apk 指定 32 位和 64 位

  ```
  BASH
  adb install --abi armeabi-v7a <apk path>  # 32位下运行
  adb install --abi arm64-v8a <apk path>    # 64位下运行
  ```

- adb 查看连接设备

  - `adb devices`

- adb 指定连接设备

  - `adb -s cf12345f shell`

- adb 安装应用

  - `adb install -r demo.apk`

- adb 卸载应用

  - `adb uninstall <包名>`

- adb 列出手机安装的所有 app 的包名

  - `adb shell pm list packages`

- adb 列出除了系统应用之外的第三方应用

  - `adb shell pm list package -3`

- adb 清除应用数据和缓存

  - `adb shell pm clear <包名>`

- adb 强制停止应用

  - `adb shell am force-stop com.tencent.mm`

- adb 启动 activity

  - `adb shell am start com.tencent.mm/com.tencent.mm.ui.LauncherUI` 配合adb 查看最顶端应用的包名和 activity 名使用

- adb 取出安装的 apk

  1. `adb shell pm list package`
  2. `adb shell pm path com.tence01.mm` 获取apk的位置
  3. `adb pull /data/app/com.tence01.mm-1.apk ~/apks` 拉取到本地

- 获取系统版本：
  - adb shell getprop ro.build.version.release

- 获取系统api版本：
  - adb shell getprop ro.build.version.sdk

- 获取手机相关制造商信息：
  - adb shell getprop | grep "model\|version.sdk\|manufacturer\|hardware\|platform\|revision\|serialno\|product.name\|brand"


- 获取手机系统信息（ CPU，厂商名称等）
  - adb shell "cat /system/build.prop | grep "product""

- 获取手机系统版本
  - adb shell getprop ro.build.version.release

- 获取手机系统api版本
  - adb shell getprop ro.build.version.sdk

- 获取手机设备型号
  - adb -d shell getprop ro.product.model

- 获取手机厂商名称
  - adb -d shell getprop ro.product.brand
  - 
    获取手机的序列号,有两种方式
    adb get-serialno
    adb shell getprop ro.serialno
  
- 获取手机的IMEI,有三种方式，由于手机和系统的限制，不一定获取到
  - adb shell dumpsys iphonesubinfo，其中Device ID即为IMEI号
  - adb shell getprop gsm.baseband.imei
  - service call iphonesubinfo 1 此种方式，需要自己处理获取的信息得到

- 获取手机mac地址
  - adb shell cat /sys/class/net/wlan0/address

- 获取手机内存信息
  - adb shell cat /proc/meminfo

- 获取手机存储信息
  - adb shell df

- 获取手机内部存储信息：
  - 魅族手机： adb shell df /mnt/shell/emulated
  - 其他： adb shell df /data

- 获取sdcard存储信息：
  - adb shell df /storage/sdcard

- 获取手机分辨率
  - adb shell "dumpsys window | grep mUnrestrictedScreen"

- 获取手机物理密度
  - adb shell wm density


## 2、Android 7.0 以上安装 Fiddler 系统级证书

Android 7.0 以上，系统不再新人用户级的证书，只信任系统级证书，要实现 https 的抓包，就需要将用户证书修改为系统证书

### 2.1、工具：

- Fiddler/Charles 证书
- openssl

下载地址：

- Fiddler/Charles 设置好代理后，访问代理 ip:port 下载
- [OpenSSL官方下载 - 码客 (oomake.com)](https://oomake.com/download/openssl)

### 2.2、步骤：

1. 将抓包程序证书导出，一班为 `.cer` 或 `.pem` 格式

2. 使用 `openssl` 的 `x509` 指令进行 `.cer` 证书转 `.pem` 证书：

   > openssl x509 -inform DER -in xxx.cer -out cacert.pem 

3.  用 `md5` 方式显示 `pem` 证书的 `hash` 值

 > openssl x509 -inform PEM -subject_hash_old -in cacert.pem	//v>1.0
 > openssl x509 -inform PEM -subject_hash -in cacert.pem //v<1.0

4. 将 `.pem` 证书重命名为 3 步查出来的值（`.0`结尾）
5. 将新证书放到手机系统目录：`/system/etc/security/cacerts`(需root)



## 3、Frida

frida 是一款基于 `python + javascript` 的 `hook` 框架，可运行在 `android/ios/linux/win/osx` 等各平台，主要使用动态二进制插桩技术。

### 3.1、插桩技术

插桩技术是指将额外的代码注入程序中以收集运行时的信息，可分两种：

- 源代码插桩 [Source Code Instrumentation(SCI)]：额外代码注入到程序源代码中。
- 二进制插桩 [Binary Instrumentation]：额外代码注入到二进制可执行文件中。
  - 静态二进制插桩 [Static Binary Instrumentation(SBI)]：在程序执行前插入额外的代码和数据，生成一个永久改变的可执行文件。
  - 动态二进制插桩 [Dynamic Binary Instrumentation(DBI)]：在程序运行时实时地插入额外代码和数据，对可执行文件没有任何永久改变。

### 3.2、Frida DBI 能做什么

- 访问进程的内存
- 在应用程序运行时覆盖一些功能
- 从导入的类中调用函数
- 在堆上查找对象实例并使用这些对象实例
- Hook，跟踪和拦截函数等等

### 3.3、Frida  安装

#### frida CLI

环境要求：

- 系统环境：windows/mac/linux
- Python：3.x 版本

安装：pip install frida / pip install frida -v 版本号

#### frida server

frida-server 可在 https://github.com/frida/frida/releases 下载

需对应 frida CLI 版本

- 查看 Frida 版本：frida -version
- 查看 Android 版本：`adb shell getprop ro.product.cpu.abi`
  - armeabiv-v7a： 第7代及以上的 ARM 处理器。2011年15月以后的生产的大部分Android设备都使用它.
  - arm64-v8a： 第8代、64位ARM处理器，很少设备。
  - x86：平板、模拟器用得比较多。
  - x86_64：64位的平板。

这里 windows frida 版本是 14.2.18，Android 端用的 夜神模拟器，frida-server 选择的是 `frida-server-14.2.18-android-x86.xz`

解压后启动命令行，将 frida-server push 到 Android 设备的 /data/local/tmp 中
> adb push ./frida-server-14.2.18-android-x86 /data/local/tmp

启动 adb shell
> adb shell
> su
> cd /data/local/tmp
> mv ./frida-server-14.2.18-android-x86  ./frida-server

设置权限
> chmod 777 frida-server

启动服务
> ./frida-server

端口转发
> adb  forward tcp:27042 tcp:27042
> adb  forward tcp:27042 tcp:27042

另开命令行查看进程
> frida-ps -U

### 3.4、客户端命令

#### 将脚本注册到 Android 目标进程

`frida -U -l mybook.js com.xxx.xxxx`

参数解释：

- -U 指定对USB设备操作
- -l 指定加载一个Javascript脚本
- 最后指定一个进程名，如果想指定进程pid,用`-p`选项。正在运行的进程可以用`frida-ps -U`命令查看

#### 重启一个 Android 进程并注入脚本

`frida -U -l myhook.js -f com.xxx.xxxx --no-pause`

参数解释：

- -f 指定一个进程，重启它并注入脚本
- --no-pause 自动运行程序

这种注入脚本的方法，常用于hook在App就启动期就执行的函数。

> frida运行过程中，执行`%resume`重新注入，执行`%reload`来重新加载脚本；执行`exit`结束脚本注入

### 3.5、Hook Java 方法

#### 载入类：

`Java.use` 方法用于加载一个 Java 类，相当于 Java 的 `Class.forname()`

例如加载一个 String 类：

`var StringClass = Java.use("java.lang.String");`

加载内部类：

`var MyClass_InnerClass = Java.use("com.xxx.xxxx.MyClassInnerClass");`

#### 修改函数实现：

##### 函数参数类型表示：

###### 基本类型：

对于基本类型，直接用在 java 中的表示方法就可以，不用改变，如：int、short、char、byte、boolean、float、double、long

###### 基本类型数组：

基本类型数组，用左中括号接上基本类型的缩写，如 `[B` 表示 byte 数组

缩写对照表

| 基本类型 | 缩写 |
| -------- | ---- |
| boolean  | Z    |
| byte     | B    |
| char     | C    |
| double   | D    |
| float    | F    |
| int      | I    |
| long     | J    |
| short    | S    |

###### 任意类：

任意类可直接写完整类名：`java.lang.String`

###### 对象数组：

对象数组，用左中括号接上完整类名再接上分号：`[java.lang.String;`

##### 带参构造函数：

修改参数为 byte[] 类型的构造函数的实现

```js 
ClassName.$init.overload("[B").implementation=function(param){
    //do something
}
```

> 注：ClassName 是使用 Java.use 定义的类；param 是函数体中访问的参数

修改多参数的构造函数的实现

```js
ClassName.$init.overload('[B','int','int').implementation=function(param1,param2,param3){
    //do something
}
```

##### 无参数构造函数：

```js
ClassName.$init.overload().implementation=function(){
    //do something
}
```

调用原构造函数

```js
ClassName.$init.overload().implementation=function(){
    this.$init();
    //do something
}
```

> 注意：当构造函数(函数)有多种重载形式，比如一个类中有两个形式的func：`void func()`和`void func(int)`，要加上overload来对函数进行重载，否则可以省略overload

##### 一般函数：

修改函数名为 func ，参数为 byte[] 类型的函数的实现

```js
ClassName.func.overload('[B').implementation=function(param){
    //do somethint
}
```

##### 无参数函数：

```js
ClassName.func.overload().implementation=function(){
    //do something
}
```

> 注： 在修改函数实现时，如果原函数有返回值，那么我们在实现时也要返回合适的值

```js
ClassName.func.overload().implementation=function(){
    //do something
    return this.func();
}
```

#### 调用函数：

和Java一样，创建类实例就是调用构造函数，而在这里用`$new`表示一个构造函数。

```js
var ClassName=Java.use("com.luoye.test.ClassName");
var instance = ClassName.$new();
```

实例化以后调用其他函数

```js
var ClassName=Java.use("com.luoye.test.ClassName");
var instance = ClassName.$new();
instance.func();
```

#### 字段操作：

字段赋值和读取要在字段名后加`.value`，假设有这样的一个类：

```js
package com.luoyesiqiu.app;
public class Person{
    private String name;
    private int age;
}
```

写个脚本操作Person类的name字段和age字段：

```js
var person_class = Java.use("com.luoyesiqiu.app.Person");
//实例化Person类
var person_class_instance = person_class.$new();
//给name字段赋值
person_class_instance.name.value = "luoyesiqiu";
//给age字段赋值
person_class_instance.age.value = 18;
//输出name字段和age字段的值
console.log("name = ",person_class_instance.name.value, "," ,"age = " ,person_class_instance.age.value);
```

输出：

```
name =  luoyesiqiu , age =  18
```

#### 类型转换

用`Java.cast`方法来对一个对象进行类型转换，如将`variable`转换成`java.lang.String`：

```js
var StringClass=Java.use("java.lang.String");
var NewTypeClass=Java.cast(variable,StringClass);
```

#### Java.available字段

这个字段标记Java虚拟机（例如： Dalvik 或者 ART）是否已加载, 操作Java任何东西之前，要确认这个值是否为true

#### Java.perform方法

Java.perform(fn)在Javascript代码成功被附加到目标进程时调用，我们核心的代码要在里面写。格式：

```js
Java.perform(function(){
//do something...
});
```

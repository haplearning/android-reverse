# android-reverse

[TOC]



## 

# 基本环境配置

## Adb 

### 环境配置

### Adb 常见命令

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
  - `adb shell getprop ro.build.version.release`

- 获取系统api版本：
  - `adb shell getprop ro.build.version.sdk`

- 获取手机相关制造商信息：
  - `adb shell getprop | grep model\|version.sdk\|manufacturer\|hardware\|platform\|revision\|serialno\|product.name\|brand`


- 获取手机系统信息（ CPU，厂商名称等）
  - `adb shell "cat /system/build.prop | grep "product""`

- 获取手机系统版本
  - `adb shell getprop ro.build.version.release`

- 获取手机系统api版本
  - `adb shell getprop ro.build.version.sdk`

- 获取手机设备型号
  - `adb -d shell getprop ro.product.model`

- 获取手机厂商名称
  - `adb -d shell getprop ro.product.brand`
  - 获取手机的序列号,有两种方式
    `adb get-serialno`
    `adb shell getprop ro.serialno`
  
- 获取手机的IMEI,有三种方式，由于手机和系统的限制，不一定获取到
  - `adb shell dumpsys iphonesubinfo`，其中Device ID即为IMEI号
  - `adb shell getprop gsm.baseband.imei`
  - `service call iphonesubinfo 1` 此种方式，需要自己处理获取的信息得到

- 获取手机mac地址
  - `adb shell cat /sys/class/net/wlan0/address`

- 获取手机内存信息
  - `adb shell cat /proc/meminfo`

- 获取手机存储信息
  - `adb shell df`

- 获取手机内部存储信息：
  - 魅族手机： `adb shell df /mnt/shell/emulated`
  - 其他： `adb shell df /data`

- 获取sdcard存储信息：
  - `adb shell df /storage/sdcard`

- 获取手机分辨率
  - `adb shell "dumpsys window | grep mUnrestrictedScreen"`

- 获取手机物理密度
  - `adb shell wm density`


## Android 7.0 系统级证书

Android 7.0 以上，系统不再新人用户级的证书，只信任系统级证书，要实现 https 的抓包，就需要将用户证书修改为系统证书

### 环境配置

- Fiddler/Charles 证书
- openssl

下载地址：

- Fiddler/Charles 设置好代理后，访问代理 ip:port 下载
- [OpenSSL官方下载 - 码客 (oomake.com)](https://oomake.com/download/openssl)，安装完毕后配置环境变量

### 配置步骤

1. 将抓包程序证书导出，一班为 `.cer` 或 `.pem` 格式

2. 使用 `openssl` 的 `x509` 指令进行 `.cer` 证书转 `.pem` 证书：

   > openssl x509 -inform DER -in xxx.cer -out cacert.pem 

3.  用 `md5` 方式显示 `pem` 证书的 `hash` 值

 > openssl x509 -inform PEM -subject_hash_old -in cacert.pem	//v>1.0
 > openssl x509 -inform PEM -subject_hash -in cacert.pem //v<1.0

4. 将 `.pem` 证书重命名为 3 步查出来的值（`.0`结尾）
5. 将新证书放到手机系统目录：`/system/etc/security/cacerts`(需root)



## Frida

frida 是一款基于 `python + javascript` 的 `hook` 框架，可运行在 `android/ios/linux/win/osx` 等各平台，主要使用动态二进制插桩技术。

### 插桩技术

插桩技术是指将额外的代码注入程序中以收集运行时的信息，可分两种：

- 源代码插桩 [Source Code Instrumentation(SCI)]：额外代码注入到程序源代码中。
- 二进制插桩 [Binary Instrumentation]：额外代码注入到二进制可执行文件中。
  - 静态二进制插桩 [Static Binary Instrumentation(SBI)]：在程序执行前插入额外的代码和数据，生成一个永久改变的可执行文件。
  - 动态二进制插桩 [Dynamic Binary Instrumentation(DBI)]：在程序运行时实时地插入额外代码和数据，对可执行文件没有任何永久改变。

### Frida DBI 作用

- 访问进程的内存
- 在应用程序运行时覆盖一些功能
- 从导入的类中调用函数
- 在堆上查找对象实例并使用这些对象实例
- Hook，跟踪和拦截函数等等

### Frida  安装

#### frida CLI

环境要求：

- 系统环境：windows/mac/linux
- Python：3.x 版本

安装：`pip install frida` / `pip install frida -v <版本号>`

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
> adb  forward tcp:27043 tcp:27043
> adb  forward tcp:27042 tcp:27042

另开命令行查看进程
> frida-ps -U

### 客户端命令

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

### Hook Java 方法

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

# 反编译：

### Apktool 

#### 环境配置：

安装教程参考：[Apktool - How to Install (ibotpeaches.github.io)](https://ibotpeaches.github.io/Apktool/install/)

版本支持：

- 至少安装 java 1.8
- 命令行`java -version` 返回 1.8 或更高 
- 安装 `Java 8+` 并设置环境变量

windows 安装：

- 下载或浏览器保存链接 [wrapper script](https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/windows/apktool.bat) 为 `apktool.bat`
- 下载 `apktool.jar`，下载地址：[apktool.jar]([iBotPeaches / Apktool / Downloads — Bitbucket](https://bitbucket.org/iBotPeaches/apktool/downloads/))
- 将下载的 `apktool_x.x.x.jar` 重命名为 `apktool.jar`
- 将 `apktool.jar` 和 `apktool.bat` 放到同一目录下（如 `apktool/`），并配置环境变量
- 执行 `apktool` 命令查看是否配置成功

安装步骤截图

![image-20210608234148676](https://github.com/haplearning/android-reverse/blob/main/images/image-20210608234148676.png)

![image-20210608234749900](https://github.com/haplearning/android-reverse/blob/main/images/image-20210608234749900.png)

![image-20210608235301440](https://github.com/haplearning/android-reverse/blob/main/images/image-20210608235301440.png)

![image-20210608235401335](https://github.com/haplearning/android-reverse/blob/main/images/image-20210608235401335.png)



#### 常用命令

- `apktool d <.apk> [-o apk]`：反编译 apk ，默认输出当前目录，可指定输出目录
- `apktool b <apk> [-o <.apk>]`：回编译 apk，默认输出当前目录，可指定输出目录
- `apktool -b <apk> -p <frameworkdir> [-o <out.apk>`：`-p` 指定 `framework` 文件；空 `framework` 文件夹可忽略回编译时的 `'compileSdkVersion'/'compileSdkVersionCodename'/'appComponentFactory'` 错误

**注意：回编译后的 apk 文件需经过 签名 后才能够被安装**



![image-20210609003024658](https://github.com/haplearning/android-reverse/blob/main/images/image-20210609003024658.png)

![image-20210609002542971](https://github.com/haplearning/android-reverse/blob/main/images/image-20210609002542971.png)

### APK Easy Tool 



# 回编译：待补充



# 签名

Android 签名原理可参考知乎这篇文章：[都到2020年了，Android 签名机制 v1、v2、v3你懂什么意思嘛！ - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/130394904)

目前 Android 应用的签名工具有两种，其签名算法没有什么区别，主要是签名使用的文件不同：

- jarsigner：Java jdk 自带的签名工具，可以对 `jar` 进行签名。使用 `keystore`  文件进行签名。生成的签名文件默认使用 `keystore` 的别名命名
- apksigner：Android sdk 提供的专门用于 Android 应用的签名工具。使用 `pk8`、`x509.pem` 文件进行签名。其中 `pk8` 是私钥文件，`x509.pem` 是含有公钥的文件。生成的签名文件统一使用 `CERT` 命名。

其中 Android studio 默认签名保存在系统用户文件夹下的 `.android` 目录下的 `debug.keystore` 文件，别名为：`androiddebugkey` ，密码为 `android` 

### 环境配置

- Java： jdk-16.0.1
- Android_SDK：build-tools\30.0.3

### Jarsigner 签名

`jarsigner` 签名需要用到 Java 安装目录 `./jdk-16.0.0.1/bin` 下的 `keytool.exe` 和 `jarsigner.exe` 工具，这两个工具是 Java 自带的，配置了 Java 的环境目录后可以直接使用

查看签名：`keytool -v -list -keystore debug.keystore`

![image-20210608111921362](https://github.com/haplearning/android-reverse/blob/main/images/image-20210608111921362.png)

查看 apk 的签名信息：

- `jarsigner -verify -verbose -certs <.apk>` 
-  `keytool -printcert -jarfile <.apk>` 只支持v1签名校验

![image-20210608112303471](https://github.com/haplearning/android-reverse/blob/main/images/image-20210608112303471.png)

创建签名文件：

命令行输入：`keytool -genkey -alias key.keystore -keyalg RSA -validity 30000 -keystore key.keystore`

依次输入口令密码和签名信息，最后输入 `y` 确认签名，就会在当前目录下生成签名文件 `key.ketstore`

![image-20210608114718865](https://github.com/haplearning/android-reverse/blob/main/images/image-20210608114718865.png)

查看签名：keytool -v -list -keystore key.keystore

![image-20210608115016123](https://github.com/haplearning/android-reverse/blob/main/images/image-20210608115016123.png)

Keytool 常见选项：

|选项|描述|
|-|-|
|-genkey|产生一个键值对（公钥和私钥）|
|-v|允许动作输出|
|-alias|键的别名。只有前八位字符有效|
|-keyalg|产生键的加密算法。支持 DSA 和 RSA|
|-validity|密钥对得有效期（单位：天）|
|-keysize|产生键的长度。未提供时keytool默认值为1024bits，通常用2048bits或更长的|
|-dname|专有名称，描述谁创建的密钥。该值被用作自签名证书的颁发者和主题字段。|
|-keypass|键的密码，未提供时keytool会提示输入|
|-keystore|指定用于存储私钥的文件|
|-storepass|私钥存储文件的密码。未提供时keytool会提示输入且该密码不会存储在 shell 历史记录中|
|-delete|删除一条密钥|

用 jarsigner 给 apk 签名：

命令行输入：`jarsigner -verbose -keystore key.keystore -signedjar signed_app-debug.apk  app-debug.apk  key.keystore`

![image-20210608170250494](https://github.com/haplearning/android-reverse/blob/main/images/image-20210608170250494.png)

![image-20210608171055683](https://github.com/haplearning/android-reverse/blob/main/images/image-20210608171055683.png)

签名完成，拖进模拟器就可以安装了

Jarsigner 常见选项

| 选项 | 描述 |
| ---- | ---- |
|-keystore|keystore 包含你私钥的存储文件|
|-verbose|显示输出动作。|
|-signedjar|后街签名后的apk名称 和 待签名的apk|
|-sigalg|签名算法，用 SHA1withRSA.|
|-digestalg|消息摘要算法，用 SHA1.|
|-storepass|存储文件的密码。 主要为了安全起见，如果没提供，jarsigner会提示你输入。|
|-keypass|私钥的密码。 主要为了安全起见，如果没提供，jarsigner会提示你输入。这个密码不会存储在你的shell历史记录中。|



### Apksigner 签名：待补充

Apksigner 是 Android_SDK 提供的签名方式，Android 现在已支持三种应用签名方案：

- v1 方案：基于 JAR 签名
- v2 方案：APK 签名方案 v2，在 Android 7.0 引入
- v3 方案：APK 签名方案 v3，在 Android 9.0 引入



# Android studio 动态调试 smali

### 安装 smalidea 插件：

参考文章：[ 解决新版Android Studio 4.0+无法断点调试smali问题_逍遥阁-CSDN博客](https://blog.csdn.net/qq_43278826/article/details/108377201)

版本支持：

- Android studio 4.2.1
- smalidea 0.06

`smalidea ` git 地址：[https://github.com/JesusFreke/smalidea](https://github.com/JesusFreke/smalidea)，实测从 git 版本库中 0.06版本安装失败，可以从这个网站下载：[https://bitbucket.org/JesusFreke/smalidea/downloads/](https://bitbucket.org/JesusFreke/smalidea/downloads/)

安装：

Android studio 依次点击 `File-Setting-Plugins` 

![image-20210607180508680](https://github.com/haplearning/android-reverse/blob/main/images/image-20210607180508680.png)

安装后重启 Android studio，然后将处理 `*.smali` 的插件设置为 smalidea

![image-20210607180933369](https://github.com/haplearning/android-reverse/blob/main/images/image-20210607180933369.png)

### 调试 smali

打开夜神模拟器连接设备：`adb devices`

查看包或第三方包：`adb shell pm list packages [-3]`

命令行启动调试模式：`adb shell am start -D -n <packagename>/<.MainActivity>` 

查看进程号：`adb shell ps | findstr <packagename>`

端口映射：`adb forward tcp:8900 jdwp:12618`

Android studio 以 `Profile or Debug APK`  打开 apk（在主目录下`/ApkProjects/` 下创建apk的副本），并创建 `remote `调试，设置端口为 `8900`

![image-20210608222712303](https://github.com/haplearning/android-reverse/blob/main/images/image-20210608222712303.png)

![image-20210607211527616](https://github.com/haplearning/android-reverse/blob/main/images/image-20210607211527616.png)![image-20210607211717435](https://github.com/haplearning/android-reverse/blob/main/images/image-20210607211717435.png)

![image-20210607211951445](https://github.com/haplearning/android-reverse/blob/main/images/image-20210607211951445.png)



然后打开 smali 代码断点，启动调试，选择进程

![image-20210608223533226](https://github.com/haplearning/android-reverse/blob/main/images/image-20210608223533226.png)

![image-20210608223647690](https://github.com/haplearning/android-reverse/blob/main/images/image-20210608223647690.png)



然后就进入调试了



![image-20210608223800443](https://github.com/haplearning/android-reverse/blob/main/images/image-20210608223800443.png)



模拟器输入账号、密码，点击登录自动进入调试



![image-20210608223854885](https://github.com/haplearning/android-reverse/blob/main/images/image-20210608223854885.png)

![image-20210608224002233](https://github.com/haplearning/android-reverse/blob/main/images/image-20210608224002233.png)



#  在 Smali 中插入日志



Android studio 以 `Profile or Debug APK`  打开 apk（在主目录下`/ApkProjects/` 下创建apk的副本）

![image-20210615173747426](https://github.com/haplearning/android-reverse/blob/main/images/image-20210615173747426.png)

![image-20210615174541638](https://github.com/haplearning/android-reverse/blob/main/images/image-20210615174541638.png)

开启或重启设备

![image-20210615174801334](https://github.com/haplearning/android-reverse/blob/main/images/image-20210615174801334.png)

打开 app 后会出现包名，且自动输出 app 日志

![image-20210615175429956](https://github.com/haplearning/android-reverse/blob/main/images/image-20210615175429956.png)


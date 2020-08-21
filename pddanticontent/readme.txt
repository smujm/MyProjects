本项目是解决拼多多商家登录需要的anticontent参数

main.05108fe9.js  文件为pdd商家网页版的源js文件，这个只做参考不是运行必须
anticontent.js 为逆向+扣main.05108fe9.js 生成anticontent的代码，运行需要node环境，node需要安装jsdom+express模块

直接运行 node  anticontent.js

运行成功后，通过http请求：  http://127.0.0.1:8000/get_anti_content 会返回anticontent内容

注意pdd的main.05108fe9.js会不定期的更换文件名和文件内容，如发现失效需要重新逆向新的main.xxx.js文件
# gmgard_checkin
用于hoshinobot的gmgard签到插件

使用前请修改gmgard.json文件:
  URL_GMGARD = 'https://gmgard.com' #这项不出意外不需要修改
  USER中保存了cookies，请自行登陆后打开 https://gmgard.com 获取cookie中".AspNetCore.Identity.Application"的值进行手动录入，支持多个账号，文件中已经写入了例子请自行修改，登录单账号的话把USER2删除掉即可。
  推荐将USER中key名改为账号昵称，方便在签到后查看签到情况（例如：USER1改为Romuuu后，签到完成会提示 用户:Romuuu）
  
  需要三方库：selenium
  webdriver配置方法请自行检索~
  
  指令为："g签到" 

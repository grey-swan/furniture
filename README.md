# furniture
家具小程序后端，包括如下两部分内容：
1. 用户、权限、角色、用户登录和注销，数据存储在本地mysql中，只用于用户登录和权限管理；
2. 业务模块，数据存储在微信云开发数据库中，数据库操作均是通过调用云函数方式进行，所以重写了一下模块。

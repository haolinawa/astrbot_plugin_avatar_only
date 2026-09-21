# AstrBotのQQ头像修改

这是一个只用于修改 NapCat QQ Bot 自身头像的 AstrBot 插件

## 如何使用

Tips:仅 AstrBot 管理员可以使用：

- “/换头像” + 图片
- 引用一张图片后发送 `/换头像`
- “/头像” + 图片
- “/set_avatar” + 图片 URL

例如：

1. 在 QQ 中发送一张猫猫沙沙的图片
2. 引用这张图片发送 “/换头像”
3. NapCat就会调用 `set_qq_avatar` 修改 Bot 自身头像

## 要求

- AstrBot
- OneBot v11 / aiocqhttp
- NapCat

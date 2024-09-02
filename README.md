# 使用手册
## 环境变量说明
- REFRESH_TOKEN_LIST：为 阿里云盘的刷新token，多个帐号使用，进行分割
- PUSHPLUS_TOKEN： 为 PUSHPLUS的通知token

## 本地运行
1. 安装
```shell
export REFRESH_TOKEN_LIST=xxx,xxx PUSHPLUS_TOKEN=xxx
pip install -r requirements.txt
```

2. 运行
```shell
python checkin.py
```
## github action
在项目仓库`settings->Security->Secrets and variables -> Actions`的Repository secrets 中添加
`REFRESH_TOKEN_LIST`和`PUSHPLUS_TOKEN`的环境变量。
暂定北京时间的6：30跑，若需修改，可以修改`.github/workflows/auto.yml`中的cron的值



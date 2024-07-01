
# 介绍

Automatically tally WeChat group chat information, Discord various channel information to CSV

# 环境

```python
conda create -n auto_static python=3.10 -y
conda activate auto_static
pip install -r requirements.txt
```

# Discord数据统计
- 更新`client.run`内的token，才能有权限访问读取所有频道的历史信息
- 目前这个机器人是我的账户创建的，你可以自己创建一个机器人，然后把赋予相应的读取权限让诺拉进去，然后替换token
```python
python discord_statistic.py
```

# 微信数据统计
- 修改代码中args相应的信息为你自己的，要保证你自己已经加入到01的五个微信群里，后续如果还有更多的群，可以在sql语句中添加
- 当前args的信息：
args = {
    "mobile": "15258388747",  # 手机号
    "name": "易二三.",  # 微信昵称
    "account": "ygf15258388747",  # 微信账号
    "version_list_path": "version_list.json",  # 微信版本偏移文件路径（可选）
    "key": None,  # 密钥（可选）
    "db_path": None,  # 微信文件夹路径（可选）
}
```python
python wx_statistics.py
```

- 上述两个脚本代码都不长，遇到问题可以跟一下代码debug一下。
# Acknowledgments

This code is based on [PyWxDump](https://github.com/xaoyaoo/PyWxDump)
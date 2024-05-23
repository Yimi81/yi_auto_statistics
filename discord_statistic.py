import discord
import csv
from discord.ext import commands
from datetime import datetime, timedelta

# 初始化bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')
    # 指定需要抓取的频道ID列表
    channel_ids = [1197807921979985925, 1197807921979985927, 1215251476750925845, 1215251872810672138, 1215252321899122728, 1215327344659529789, 1197820943385501726, 1216039017028649071, 1220699450113130576]  # 替换为实际的频道ID
    for channel_id in channel_ids:
        channel = client.get_channel(channel_id)
        if channel:
            # 打开或创建CSV文件，准备写入数据
            with open(f'{channel.name}_messages.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Author", "Content", "Timestamp"])

                # 获取频道消息
                start_date = datetime.today() - timedelta(days=7)
                async for message in channel.history(after=start_date):  # 可以根据需要调整limit参数
                    writer.writerow([message.author.display_name, message.content, message.created_at])
            
            print(f"Messages from {channel.name} have been saved to CSV.")
        else:
            print(f"Channel {channel_id} not found or bot does not have access.")

    return
# 替换Bot Token
client.run('')

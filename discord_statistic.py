import discord
import csv
from discord.ext import commands
from datetime import datetime, timedelta
import pandas as pd


# 初始化bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)


def convert_df(path, group):
    df = pd.read_csv(path)
    df["group"] = group
    return df


@client.event
async def on_ready():
    print(f"Logged in as {client.user}!")
    # 指定需要抓取的频道ID列表
    channel_ids = [
        1197807921979985925,
        1197807921979985927,
        1215251476750925845,
        1215251872810672138,
        1215252321899122728,
        1215327344659529789,
        1197820943385501726,
        1216039017028649071,
        1220699450113130576,
    ]  # 替换为实际的频道ID
    total_count_last_week = 0
    all_export_path = []
    export_group_order = []

    for channel_id in channel_ids:
        channel = client.get_channel(channel_id)
        if channel:
            # 打开或创建CSV文件，准备写入数据
            with open(
                f"./export/discord/{channel.name}_messages.csv",
                "w",
                newline="",
                encoding="utf-8",
            ) as file:
                writer = csv.writer(file)
                writer.writerow(["Author", "Content", "Timestamp"])

                # 获取频道消息
                start_date = datetime.today() - timedelta(days=7)
                async for message in channel.history(
                    after=start_date
                ):  # 可以根据需要调整limit参数
                    writer.writerow(
                        [
                            message.author.display_name,
                            message.content,
                            message.created_at,
                        ]
                    )

            print(f"Messages from {channel.name} have been saved to CSV.")
            all_export_path.append(f"./export/discord/{channel.name}_messages.csv")
            export_group_order.append(channel.name)
            df = pd.read_csv(f"./export/discord/{channel.name}_messages.csv")
            total_count_last_week += len(df) - 1
        else:
            print(f"Channel {channel_id} not found or bot does not have access.")

    print(f"上周Discord各个频道技术讨论量: {total_count_last_week}")
    all_new_df = [
        convert_df(path, export_group_order[idx])
        for idx, path in enumerate(all_export_path)
    ]

    merged_df = pd.concat(
        all_new_df,
        ignore_index=True,
    )
    end_date = datetime.now().date()
    merged_df.to_csv(rf"./export/discord/{end_date}_discord_merged_file.csv", index=False)
    # 记录特定人聊天记录
    talker_ids = ["我", "Nuo Ma @01.ai"]  # 当前记录：易国峰，马诺
    filtered_df = merged_df.loc[merged_df["Author"].isin(talker_ids)]
    print(f"总解决问题：{len(filtered_df)}")
    return


# 替换Bot Token
client.run("MTIzNDQwNjEwOTc1MDc1NTM1OQ.GxDdNu.uoiJvGxAqc7GdzFFjVZ_dwuwnxTESb0xWaQtmk")

import os
import pandas as pd
from pywxdump import (
    BiasAddr,
    read_info,
    get_wechat_db,
    batch_decrypt,
    get_core_db,
    merge_real_time_db,
    DBPool,
)
from pywxdump.analyzer.utils import execute_sql
from pywxdump.dbpreprocess import (
    wxid2userinfo,
    ParsingMSG,
    get_user_list,
    get_recent_user_list,
    ParsingMediaMSG,
    download_file,
    export_csv,
    export_json,
)
from datetime import datetime
import argparse


# 获取微信基址偏移
args = {
    "mobile": "15258388747",  # 手机号
    "name": "易二三.",  # 微信昵称
    "account": "ygf15258388747",  # 微信账号
    "version_list_path": "version_list.json",  # 微信版本偏移文件路径（可选）
    "key": None,  # 密钥（可选）
    "db_path": None,  # 微信文件夹路径（可选）
}

bias_addr = BiasAddr(
    args["account"], args["mobile"], args["name"], args["key"], args["db_path"]
)
result = bias_addr.run(True, args["version_list_path"])

# 获取微信信息
wx_info = read_info(result, True)

args["key"] = wx_info[0]["key"]
args["wx_files"] = wx_info[0]["filePath"]
args["wxid"] = wx_info[0]["wxid"]
args["require_list"] = "all"

# 获取微信文件夹路径
user_dirs = get_wechat_db(args["require_list"], args["wx_files"], args["wxid"], True)

args["db_path"] = rf"{wx_info[0]['filePath']}\Msg"
args["out_path"] = "./decrypted"

# 解密微信数据库
# result = batch_decrypt(args["key"], args["db_path"], args["out_path"], True)

args.update(
    {
        "outpath": r"./export",  # 导出路径
        "msg_path": r"./decrypted/Multi/de_MSG0.db",  # 解密后的 MSG.db 的路径
        "micro_path": r"./decrypted/de_MicroMsg.db",  # 解密后的 MicroMsg.db 的路径
        "media_path": r"./decrypted/Multi/de_MediaMSG0.db",  # 解密后的 MediaMSG.db 的路径
        "filestorage_path": rf"{wx_info[0]['filePath']}\FileStorage",  # 文件夹 FileStorage 的路径（用于显示图片）
    }
)
# print(get_core_db(args["wx_files"],["MSG", "MediaMSG", "MicroMsg"]))

# 获取五个微信群聊的username, 即id
yi_chat_room = None
with DBPool(args["micro_path"]) as db:
    sql = "SELECT UserName, NickName FROM Contact WHERE NickName IN ('Yi User Group 中文社区', 'Yi-VL User Group', '零一万物大模型开放平台API', '零一万物大模型开放平台社区')"
    yi_chat_room = execute_sql(db, sql)
    print(yi_chat_room)

# 记录所有Yi相关群自今天开始过去一周所有聊天记录
all_export_path = []
export_group_order = []


total_count_last_week = 0


def convert_df(path, group):
    df = pd.read_csv(path)
    df["group"] = group
    return df


if yi_chat_room:
    for idx, value in enumerate(yi_chat_room):
        user_name = value[0]  # id
        nick_name = value[1]
        export_group_order.append(nick_name)

        is_success, export_path, chatCount = export_csv(
            user_name, args["outpath"], args["msg_path"], last_week=True
        )
        if is_success:
            print(f"导出成功: {export_path}, Count: {chatCount}")
            all_export_path.append(export_path)
            total_count_last_week += chatCount
        else:
            print(f"过去七天{nick_name}无记录：{export_path}")

    print("=" * 10 + "最终结果" + "=" * 10)
    print(f"上周技术讨论量: {total_count_last_week}")

    all_new_df = [
        convert_df(path, export_group_order[idx])
        for idx, path in enumerate(all_export_path)
    ]

    merged_df = pd.concat(
        all_new_df,
        ignore_index=True,
    )

    result_output_path = f"{args['outpath']}/result"
    if not os.path.exists(result_output_path):
        os.makedirs(result_output_path)

    end_date = datetime.now().date()
    merged_df.to_csv(rf"{result_output_path}/{end_date}_wx_merged_file.csv", index=False)

    # 记录特定人聊天记录
    talker_ids = ["我", "xmafile"]  # 当前记录：易国峰，马诺

    filtered_df = merged_df.loc[merged_df["talker"].isin(["我", "xmafile"])]
    filtered_df.loc[filtered_df["talker"] == "我", "talker"] = "易国峰"
    filtered_df.loc[filtered_df["talker"] == "xmafile", "talker"] = "马诺"
    print(f"总解决问题：{len(filtered_df)}")

    selected_columns_df = filtered_df[
        ["type_name", "talker", "content", "CreateTime", "group"]
    ]

    # 对数据进行排序：group 升序，CreateTime 降序
    solved_sorted_df = selected_columns_df.sort_values(
        by=["group", "CreateTime"], ascending=[True, False]
    )

    # 保存到 CSV 文件
    solved_sorted_df.to_csv(
        f"{result_output_path}/{end_date}_solved_sorted_messages.csv", index=False
    )

    # @TODO 利用飞书APIhttps://github.com/larksuite/oapi-sdk-python/blob/v2_main/README.md，获取文档，将数据写入文档，csv文件上传至文档，自动更新
    
# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         exportCSV.py
# Description:  
# Author:       xaoyaoo
# Date:         2024/04/20
# -------------------------------------------------------------------------------
import csv
import json
import os
from datetime import datetime
from ..parsingMSG import ParsingMSG


def export_csv(wxid, outpath, msg_path, page_size=50000, last_week=False):
    if not os.path.exists(outpath):
        os.makedirs(outpath)

    pmsg = ParsingMSG(msg_path)

    count = pmsg.msg_count(wxid, last_week)
    chatCount = count.get(wxid, 0)
    if chatCount == 0:
        return False, "没有聊天记录", chatCount

    if page_size > chatCount:
        page_size = chatCount + 1

    for i in range(0, chatCount, page_size):
        start_index = i
        data, wxid_list = pmsg.msg_list(wxid, start_index, page_size, last_week)

        if len(data) == 0:
            return False, "没有聊天记录", chatCount

        save_path = os.path.join(outpath, f"{datetime.now().date()}_{wxid}_{i}_{i + page_size}.csv")

        with open(save_path, "w", encoding="utf-8", newline='') as f:
            csv_writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)

            csv_writer.writerow(["id", "MsgSvrID", "type_name", "is_sender", "talker", "room_name", "content",
                                 "CreateTime"])
            for row in data:
                id = row.get("id", "")
                MsgSvrID = row.get("MsgSvrID", "")
                type_name = row.get("type_name", "")
                is_sender = row.get("is_sender", "")
                talker = row.get("talker", "")
                room_name = row.get("room_name", "")
                content = row.get("content", "")
                CreateTime = row.get("CreateTime", "")
                
                content = json.dumps(content, ensure_ascii=False)
                csv_writer.writerow([id, MsgSvrID, type_name, is_sender, talker, room_name, content, CreateTime])

    return True, save_path, chatCount


if __name__ == '__main__':
    pass

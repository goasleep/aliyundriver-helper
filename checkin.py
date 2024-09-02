import json
import os

import requests
import urllib3

urllib3.disable_warnings()


class AliYun:
    name = "阿里云盘"

    def __init__(self, check_item: dict):
        self.check_item = check_item

    def update_token(self, refresh_token):
        url = "https://auth.aliyundrive.com/v2/account/token"
        data = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        response = requests.post(url=url, json=data).json()
        access_token = response.get("access_token")
        return access_token

    def sign(self, access_token):
        url = "https://member.aliyundrive.com/v1/activity/sign_in_list"
        headers = {"Authorization": access_token, "Content-Type": "application/json"}
        result = requests.post(url=url, headers=headers, json={}).json()
        sign_days = result["result"]["signInCount"]
        data = {"signInDay": sign_days}
        url_reward = "https://member.aliyundrive.com/v1/activity/sign_in_reward"
        requests.post(url=url_reward, headers=headers, data=json.dumps(data))
        if "success" in result:
            print("签到成功")
            for i, j in enumerate(result["result"]["signInLogs"]):
                if j["status"] == "miss":
                    day_json = result["result"]["signInLogs"][i - 1]
                    if not day_json["isReward"]:
                        msg = [
                            {
                                "name": "阿里云盘",
                                "value": "签到成功，今日未获得奖励",
                            }
                        ]
                    else:
                        msg = [
                            {
                                "name": "累计签到",
                                "value": result["result"]["signInCount"],
                            },
                            {
                                "name": "阿里云盘",
                                "value": "获得奖励：{}{}".format(
                                    day_json["reward"]["name"],
                                    day_json["reward"]["description"],
                                ),
                            },
                        ]

                    return msg

    def push_to_pushplus(self, content):
        data = {
            "token": self.check_item["pushplus_token"],
            "title": "阿里云盘每日签到",
            "content": content.replace("\n", "<br>"),
            "template": "json",
        }
        requests.post(url="http://www.pushplus.plus/send", data=json.dumps(data))
        return

    def main(self):
        refresh_tokens = self.check_item.get("refresh_token")
        msgs = []
        for index, refresh_token in enumerate(refresh_tokens):
            access_token = self.update_token(refresh_token)
            if not access_token:
                return [{"name": "阿里云盘", "value": "token 过期"}]
            msg = self.sign(access_token)
            msg = f"第{index + 1}帐号:" + "\n".join(
                [f"{one.get('name')}: {one.get('value')}" for one in msg]
            )
            msgs.append(msg)
        if self.check_item.get("pushplus_token"):
            self.push_to_pushplus("\n".join(msgs))
        return msg


if __name__ == "__main__":
    import os

    # 从环境变量中读取列表
    refresh_token_list = os.getenv('REFRESH_TOKEN_LIST', "")  # 默认为空列表
    pushplus_token = os.getenv('PUSHPLUS_TOKEN')
    _check_item = {
        "refresh_token": refresh_token_list.split(","),
        "pushplus_token": pushplus_token,
    }
    print(AliYun(check_item=_check_item).main())

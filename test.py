import json
import os



if __name__ == "__main__":
    import os

    # 从环境变量中读取列表
    list_venv = os.getenv("LIST_ENV", [])
    print(list_venv)
    print(type(list_venv))

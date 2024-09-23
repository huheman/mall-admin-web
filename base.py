import subprocess
import os

# 执行命令函数
def modify_config(env:str, base_api:str):
    config_file_path = './config/prod.env.js'

    # 使用提供的 env 和 base_api 替换字符串中的固定值
    config_content = (
        "'use strict'\n"
        f"module.exports = {{  NODE_ENV: '\"{env}\"',  BASE_API: '\"{base_api}\"'}}\n"
    )

    # 将修改后的内容写入文件
    with open(config_file_path, 'w', encoding='utf-8') as file:
        file.write(config_content)


# 执行命令函数
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(command,' ok')
    except subprocess.CalledProcessError as e:
        print(f"{command}命令执行出错: {e.stderr.decode()}")
        raise

def publish(env:str,base_api:str,ip:str):
    modify_config(env,base_api)
    # 定义要执行的 SSH 和 SCP 命令
    commands = [
      "npm run build",
        f"ssh root@{ip} \"rm -fr /root/env_dev/nginx/html/mall-admin-new\"",
        f"scp -r ./dist/ root@{ip}:/root/env_dev/nginx/html/mall-admin-new/",
        f"ssh root@{ip} \"mv /root/env_dev/nginx/html/mall-admin /root/env_dev/nginx/html/mall-admin-old\"",
        f"ssh root@{ip} \"mv /root/env_dev/nginx/html/mall-admin-new /root/env_dev/nginx/html/mall-admin\"",
        f"ssh root@{ip} \"rm -fr /root/env_dev/nginx/html/mall-admin-old\""
    ]

    # 遍历并执行命令
    for command in commands:
        run_command(command)

    modify_config('development','http://localhost:8201/mall-admin')

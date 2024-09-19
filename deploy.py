import subprocess
import os

# 执行命令函数
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(command,' ok')
    except subprocess.CalledProcessError as e:
        print(f"命令执行出错: {e.stderr.decode()}")
        raise

def main():
    # 打印 'hello'
    run_command("echo 'hello'")

    # 发布 H5 平台
    run_command("npm run build")

    # 远程删除文件夹下的内容，如果文件夹存在
    ssh_rm_command = "ssh root@192.168.1.34 \"rm -fr /root/env_dev/nginx/html/mall-admin-new\""
    run_command(ssh_rm_command)

    # 使用 SCP 上传文件
    scp_command = "scp -r ./dist/ root@192.168.1.34:/root/env_dev/nginx/html/mall-admin-new/"
    run_command(scp_command)

    scp_command = "ssh root@192.168.1.34 \"mv /root/env_dev/nginx/html/mall-admin /root/env_dev/nginx/html/mall-admin-old\""
    run_command(scp_command)

    scp_command = "ssh root@192.168.1.34 \"mv /root/env_dev/nginx/html/mall-admin-new /root/env_dev/nginx/html/mall-admin\""
    run_command(scp_command)

    # 远程删除文件夹下的内容，如果文件夹存在
    ssh_rm_command = "ssh root@192.168.1.34 \"rm -fr /root/env_dev/nginx/html/mall-admin-old\""
    run_command(ssh_rm_command)



    print("部署完成！")

if __name__ == "__main__":
    main()

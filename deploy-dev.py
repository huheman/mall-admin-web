from base import publish

ip = '192.168.1.34'
env='development'
base_api='https://www.huhp.cc/api/mall-admin'


def main():
    publish(env,base_api,ip)

    print("部署dev完成！")

if __name__ == "__main__":
    main()

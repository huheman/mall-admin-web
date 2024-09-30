from base import publish


ip = '106.52.76.28'
env='production'
base_api='https://www.jikenow.cn/api/mall-admin'

def main():
    publish(env,base_api,ip)

    print("部署prd完成！")

if __name__ == "__main__":
    main()

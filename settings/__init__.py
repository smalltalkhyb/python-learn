import os

from settings.dev_config import get_dev_settings
from settings.prod_config import get_prod_settings

# 获取环境变量
profile = os.getenv("PROFILE", "prod")  # 使用os.getenv获取环境变量PROFILE，如果没有设置则默认为"prod"
if profile == "prod":
    # 如果有虚拟环境 则是 生产环境
    print("生产环境启动--->>")  # 打印提示信息，表示正在启动生产环境
    settings = get_prod_settings()  # 调用get_prod_settings函数获取生产环境配置

else:
    # 没有则是开发环境
    print("开发环境启动--->>")  # 打印提示信息，表示正在启动开发环境
    settings = get_dev_settings()  # 调用get_dev_settings函数获取开发环境配置



import os
from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    __doc__ = "生产环境配置"

    # ---------------- apps 配置 ----------------
    API_V1_STR: str = "/api/v1/coderepo"
    API_V2_STR: str = "/api/v2/coderepo"
    APP_NAME: str = "sthg_code_repository"
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 日志目录
    LOG_PATH: str = os.path.join(BASE_DIR, "logs")
    # 静态文件目录
    STATIC_PATH: str = os.path.join(BASE_DIR, "static")

    # --------------- 跨域配置 ------------------
    # 跨域设置 验证 list包含任意http url
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['http://localhost']

    # --------------- 数据库配置 ---------
    DB_DRIVE = os.getenv('DB_DRIVE', 'mysql+pymysql')
    DB_HOST = os.environ.get('DB_HOST', "192.168.1.171")
    DB_PORT = int(os.environ.get('DB_PORT', "9030"))
    DB_USER = os.environ.get('DB_USER', "dev_user")
    DB_PWD = os.environ.get('DB_PWD', "Dev@02891")
    DB_SCHEAMA = os.environ.get('DB_SCHEAMA', "")
    # --------------- 数据库配置 ------------------
    DB_DATABASE = os.environ.get('DB_DATABASE', "ontology_test_db")

    # --------------- 数据集配置 ------------------
    DB_DATASET_DATABASE = os.environ.get('DB_DATASET_DATABASE', "ontology_data_source_test")

    # --------------- 数据集配置 ------------------

    # ----------------- Gitlab 配置 ----------------
    QUEUE_TYPE: str = os.getenv("QUEUE_TYPE", "redis")
    GIT_LOCAL: str = os.path.join(BASE_DIR, "gitlocal")
    GIT_LOCAL_BAK: str = os.getenv('GIT_LOCAL', "/data/stonehg/data/opt/tiangong/gitlocal")
    GITLAB_IP_PORT: str = os.getenv('GITLAB_IP_PORT', "http://192.168.1.240:8082")
    GITLAB_PRIVATE_TOKEN: str = os.getenv('GITLAB_PRIVATE_TOKEN', "SP7yEh1PZxZSp8w_Zyoj")
    GITLAB_PUBLIC_GROUP_ID: int = os.getenv('GITLAB_PUBLIC_GROUP_ID', 2079)
    GITLAB_PUBLIC_FORK_PROJECT_ID: int = os.getenv('GITLAB_PUBLIC_FORK_PROJECT_ID', 424)
    GITLAB_LUBN_USER_ID: int = os.getenv('GITLAB_LUBN_USER_ID', 3)
    GITLAB_PUBLIC_GROUP_TOKEN: str = os.getenv('GITLAB_PUBLIC_GROUP_TOKEN', "pfvPqxZgTHoWR7sda1zX")
    GITLAB_PUBLIC_GIT_PROJECT_ID: str = os.getenv('GITLAB_PUBLIC_GIT_PROJECT_ID', 744)
    # ----------------- 不同服务之间的互相调用 ----------------
    ONTOLOGY_MANAGER_URL: str = os.getenv("ONTOLOGY_MANAGER_URL", "http://192.168.1.128:31176")
    GIT_PROJECT_PARENT_PATH: str = os.getenv('GIT_PROJECT_PARENT_PATH', "/tiangong")
    GIT_PROJECT_APP_PATH: str =  os.getenv('GIT_PROJECT_APP_PATH', "app.py")


    # redis配置
    REDIS_HOST: str = os.environ.get('REDIS_HOST', '192.168.1.241')
    REDIS_PORT: int = os.environ.get('REDIS_PORT', 6399)
    REDIS_PASSWORD: str = os.environ.get('REDIS_PASSWORD', '123456')
    REDIS_DEFAULT_DB: int = int(os.environ.get('REDIS_DEFAULT_DB', 6))


    # 用户中心配置
    TOKEN_USER_ID_URL = os.getenv("TOKEN_USER_ID_URL", "http://192.168.1.124:31018/api/user/userInfoByToken")

@lru_cache()
def get_prod_settings():
    """"
    即使加载.env文件，pydantic 依然选择先加载环境变量配置
    """
    return Settings(
        _env_file=os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "settings", "env_config"),
        _env_file_encoding="utf-8")

"""
@Author: huyanbing
@Date: 2025/5/10
@Description: 
"""
import os

from apps.api.v1.router import api_router as api_v1
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.staticfiles import StaticFiles

from settings import settings


def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url='https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui-bundle.js',
        swagger_css_url='https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui.css'
    )


def create_app():
    app = FastAPI(
        openapi='3.0.0',
        title="本体代码仓库",
        version="0.1.1",
        docs_url=None,  # 完全禁用默认/docs
        redoc_url=None,  # 如果需要也禁用redoc
        openapi_url="/api/openapi.json",
    )

    # 挂载静态文件
    workdir = os.getcwd()
    print("工作目录", workdir)

    if os.path.exists('static'):
        app.mount('/static', StaticFiles(directory=os.path.join(workdir, 'static')), name='静态文件')
    else:
        app.mount('/static', StaticFiles(directory=os.path.join(workdir, '../../static')), name='静态文件')

    @app.get("/api/docs", include_in_schema=False)
    def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/static/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui.css",
            swagger_favicon_url="/static/favicon.png"
            # swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
            # swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
            # swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
        )

    # 导入路由, 前缀设置
    app.include_router(
        api_v1,
        prefix=settings.API_V1_STR,
    )


    return app

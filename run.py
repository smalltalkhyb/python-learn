import uvicorn
from apps import create_app

# 创建FastAPI应用实例
app = create_app()

if __name__ == '__main__':
    uvicorn.run('run:app', port=7090, host='0.0.0.0', proxy_headers=False,
                timeout_keep_alive=300)

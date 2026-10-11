fastapi+同步sqlalchemy+jwt登陆

使用test.http中接口进行测试


my_fastapi.service

[Unit]
Description=我自己的fastapi服务

After=network.target

[Service]
WorkingDirectory=/home/kenan/document/my_fastapi
# 启动命令
ExecStart=/home/kenan/.local/bin/uv run main.py
# 环境变量
Environment=PATH=/usr/local/bin:/home/kenan/document/green/uv-python/bin/uv
# 自动重启
Restart=always
RestartSec=5
# 日志标准输出
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
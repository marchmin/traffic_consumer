#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""统一启动入口，支持 CLI 与 Web UI。"""

import sys

from app.cli import parse_args, run_cli


def main():
    """根据参数选择 CLI 或 Web UI 启动方式"""
    args = parse_args()

    # 命令行模式包含配置/统计相关命令与 --no-gui
    is_cli_mode = any(
        flag in sys.argv
        for flag in ["--list-configs", "--delete-config", "--show-stats", "--save-config", "--no-gui"]
    ) or args.no_gui

    if is_cli_mode:
        run_cli(args)
        return

    try:
        from web_ui import app, socketio
        print("启动 Web UI, 访问 http://0.0.0.0:5001")
        from web_ui import launch_auto_start_configs
        launch_auto_start_configs()
        socketio.run(app, 
                     host='0.0.0.0',  # 允许外部访问
                     port=5001,       # 指定端口
                     allow_unsafe_werkzeug=True)
    except ImportError:
        print("错误: 无法导入web_ui。请确保Flask和Flask-SocketIO已安装。")
        print("运行 'pip install Flask Flask-SocketIO' 来安装。")


if __name__ == "__main__":
    main()

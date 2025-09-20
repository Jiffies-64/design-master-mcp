#!/usr/bin/env python3
"""
启动脚本，同时启动主Web服务和MCP服务
支持多种传输方式：STDIO、SSE、StreamableHTTP
"""

import subprocess
import sys
import time
import argparse
import os

def start_main_web_service():
    """启动主Web服务"""
    print("正在启动主Web服务...")
    web_process = subprocess.Popen([sys.executable, "app.py"], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE,
                                  text=True)
    return web_process

def start_mcp_service(transport="stdio", host="127.0.0.1", port=8000):
    """启动MCP服务"""
    print(f"正在启动MCP服务 (传输方式: {transport})...")
    
    # 设置环境变量，让Web应用知道当前的MCP配置
    env = os.environ.copy()
    env['MCP_TRANSPORT'] = transport
    env['MCP_HOST'] = host
    env['MCP_PORT'] = str(port)
    env['WEB_PORT'] = '5000'  # 默认Web端口
    
    # 构建命令参数
    cmd = [sys.executable, "mcp_service.py"]
    
    if transport == "sse":
        cmd.extend(["--sse", "--host", host, "--port", str(port)])
    elif transport == "http":
        cmd.extend(["--http", "--host", host, "--port", str(port)])
    elif transport == "streamable-http":
        cmd.extend(["--streamable-http", "--host", host, "--port", str(port)])
    # stdio模式不需要额外参数
    
    mcp_process = subprocess.Popen(cmd,
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE,
                                  text=True,
                                  env=env)
    return mcp_process

def main():
    parser = argparse.ArgumentParser(description="启动DesignMaster服务")
    parser.add_argument("--mcp-transport", choices=["stdio", "sse", "http", "streamable-http"], 
                       default="stdio", help="MCP服务传输方式 (默认: stdio)")
    parser.add_argument("--mcp-host", default="127.0.0.1", help="MCP服务主机地址 (默认: 127.0.0.1)")
    parser.add_argument("--mcp-port", type=int, default=8000, help="MCP服务端口 (默认: 8000)")
    parser.add_argument("--no-web", action="store_true", help="不启动主Web服务")
    parser.add_argument("--no-mcp", action="store_true", help="不启动MCP服务")
    
    args = parser.parse_args()
    
    # 设置环境变量，让Web应用知道当前的MCP配置
    os.environ['MCP_TRANSPORT'] = args.mcp_transport
    os.environ['MCP_HOST'] = args.mcp_host
    os.environ['MCP_PORT'] = str(args.mcp_port)
    os.environ['WEB_PORT'] = '5000'  # 默认Web端口
    
    print("=" * 50)
    print("DesignMaster 服务启动器")
    print("=" * 50)
    
    processes = []
    
    # 启动主Web服务
    if not args.no_web:
        try:
            web_process = start_main_web_service()
            processes.append(("主Web服务", web_process))
            print("✓ 主Web服务已启动")
        except Exception as e:
            print(f"✗ 启动主Web服务失败: {e}")
    
    # 启动MCP服务
    if not args.no_mcp:
        try:
            mcp_process = start_mcp_service(args.mcp_transport, args.mcp_host, args.mcp_port)
            processes.append(("MCP服务", mcp_process))
            print(f"✓ MCP服务已启动 (传输方式: {args.mcp_transport})")
        except Exception as e:
            print(f"✗ 启动MCP服务失败: {e}")
    
    if not processes:
        print("没有启动任何服务")
        return
    
    print("\n" + "=" * 50)
    print("服务信息:")
    print("=" * 50)
    
    if not args.no_web:
        print("主Web服务:")
        print("  地址: http://localhost:5000")
        print("  功能: Web界面、用户管理、模板市场")
        print()
    
    if not args.no_mcp:
        print("MCP服务:")
        if args.mcp_transport == "stdio":
            print("  传输方式: STDIO")
            print("  功能: 通过STDIO与IDE通信")
        else:
            print(f"  传输方式: {args.mcp_transport.upper()}")
            print(f"  地址: http://{args.mcp_host}:{args.mcp_port}")
            print("  功能: 通过HTTP/SSE与IDE通信")
        print()
    
    print("按 Ctrl+C 停止所有服务")
    print("=" * 50)
    
    try:
        # 等待任意进程结束
        while True:
            time.sleep(1)
            # 检查进程是否仍在运行
            for name, process in processes:
                if process.poll() is not None:
                    print(f"\n{name} 已停止")
                    # 终止所有其他进程
                    for other_name, other_process in processes:
                        if other_process != process and other_process.poll() is None:
                            other_process.terminate()
                    return
                    
    except KeyboardInterrupt:
        print("\n\n正在停止所有服务...")
        # 终止所有进程
        for name, process in processes:
            if process.poll() is None:  # 如果进程仍在运行
                process.terminate()
                print(f"已发送终止信号给 {name}")
        
        # 等待进程结束
        for name, process in processes:
            try:
                process.wait(timeout=5)
                print(f"{name} 已停止")
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"{name} 已强制终止")
        
        print("所有服务已停止")

if __name__ == "__main__":
    main()
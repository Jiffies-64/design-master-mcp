# MCP连接问题排查指南

## 问题描述
当在IDE中配置MCP时，出现以下错误：
```
failed to create MCP client for DesignMaster: timeout waiting for endpoint
```

## 可能的原因和解决方案

### 1. 服务器未运行
**问题**：MCP服务器未启动或已崩溃
**解决方案**：
1. 确保服务器正在运行：
   ```bash
   python app.py
   ```
2. 检查服务器是否在监听5000端口：
   ```bash
   netstat -ano | findstr :5000
   ```

### 2. 防火墙或安全软件阻止连接
**问题**：Windows防火墙或杀毒软件阻止了连接
**解决方案**：
1. 在Windows防火墙中添加例外：
   - 打开"Windows Defender 防火墙"
   - 点击"允许应用或功能通过Windows Defender防火墙"
   - 添加Python可执行文件或允许端口5000
2. 临时禁用杀毒软件测试连接

### 3. IDE配置错误
**问题**：MCP配置不正确
**解决方案**：
1. 确保使用正确的配置格式：
   ```json
   {
     "DesignMaster": {
       "url": "http://127.0.0.1:5000",
       "headers": {
         "Authorization": "Bearer your-actual-token-here"
       }
     }
   }
   ```
2. 从MCP服务器获取最新的配置：
   - 访问 `http://127.0.0.1:5000`
   - 登录后点击"获取MCP配置"
   - 复制生成的配置到IDE中

### 4. 网络配置问题
**问题**：服务器绑定到错误的网络接口
**解决方案**：
1. 确保服务器绑定到正确的地址：
   ```python
   if __name__ == '__main__':
       app.run(debug=True, host='0.0.0.0', port=5000)
   ```
2. 使用 `0.0.0.0` 绑定到所有网络接口以允许外部访问
3. 如果仍然无法连接，可以尝试使用 `127.0.0.1` 或本地IP地址

### 5. 认证问题
**问题**：认证令牌无效或过期
**解决方案**：
1. 重新生成认证令牌：
   - 重新登录MCP服务器
   - 重新获取MCP配置
2. 确保在请求头中正确传递令牌：
   ```
   Authorization: Bearer your-actual-token-here
   ```

## 测试连接
可以使用以下命令测试服务器连接：
```bash
# 测试健康检查端点
curl http://127.0.0.1:5000/health

# 测试MCP工具端点
curl -X POST http://127.0.0.1:5000/mcp/start_document -H "Content-Type: application/json" -d "{}"
```

## 其他注意事项
1. 确保没有其他程序占用5000端口
2. 如果使用虚拟环境，确保在正确的环境中运行服务器
3. 检查服务器日志以获取更多错误信息
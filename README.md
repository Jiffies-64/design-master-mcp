# MCP Design Document Generator

This is a MCP tool for generating design documents with the following components:

1. **Templates**: Store user-configured design document templates with placeholders
2. **Prompts**: Define steps for creating design documents, bound to templates
3. **Model Calls**: Handle AI IDE calls (like Cursor) with parameter refinement
4. **Storage**: Store resources for different users

## Features

- Web interface for configuring templates and prompts
- API for IDE integration
- User authentication and resource management
- Support for PlantUML diagrams in Markdown templates
- Template marketplace for sharing templates
- User registration and login system
- Global MCP configuration generation for IDE integration

## Installation

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Initialize the database with sample data:
   ```
   python init_sample_data.py
   ```

3. Add sample templates to the public market:
   ```
   python add_sample_templates.py
   ```

## Usage

### Web Interface

1. Start the main web server:
   ```
   python app.py
   ```

2. Open your browser and navigate to `http://localhost:5000`

3. Login with the sample user:
   - Username: testuser
   - Password: password123

4. Get the MCP configuration for your IDE:
   - Click on "获取MCP配置" in the template market
   - Copy the configuration JSON
   - Paste it into your IDE's MCP configuration

5. Browse templates in the marketplace or create your own

### MCP Service (FastMCP)

1. Install the MCP service using FastMCP CLI:
   ```
   fastmcp install mcp_service.py
   ```

2. If the `fastmcp` command is not available, run the service directly:
   ```
   python mcp_service.py
   ```

3. The MCP service will run as a STDIO-based server that can be connected to your IDE

4. Configure your IDE with the following MCP configuration:
   ```json
   {
     "mcpServers": [
       {
         "name": "DesignMaster",
         "command": "python",
         "args": ["mcp_service.py"]
       }
     ]
   }
   ```

## Project Structure

- `app.py`: Main application file
- `mcp_service.py`: FastMCP service implementation
- `models/`: Database models
- `web_templates/`: Web interface templates (HTML files)
- `templates/`: Template management Python code
- `prompts/`: Prompt management
- `storage/`: User resource storage
- `mcp_tools/`: MCP tool implementations

## API Endpoints

### Web Interface Endpoints
- `GET /` - Redirects to login or templates market
- `GET /login` - User login page
- `POST /login` - Process login
- `GET /register` - User registration page
- `POST /register` - Process registration
- `GET /templates/market` - Template marketplace
- `GET /templates/create` - Create new template page
- `POST /templates/create` - Process template creation
- `GET /templates/<id>` - View template details
- `GET /mcp/config` - Get global MCP configuration

### MCP Standard Endpoints
- `GET /mcp/capabilities` - MCP capabilities endpoint
- `POST /mcp/tools` - MCP tools endpoint
- `GET /mcp/sse` - MCP Server-Sent Events endpoint
- `GET /health` - Health check endpoint

## Sample Templates

The system includes the following sample templates in the public market:

1. **Web应用设计模板** - For web application design documents
2. **微服务架构模板** - For microservices architecture design
3. **移动应用模板** - For mobile application design

These templates provide a starting point for creating design documents and can be used as examples for creating your own templates.

## MCP Configuration

The system now supports generating a global MCP configuration for IDE integration with the following format:

```json
{
  "DesignMaster": {
    "url": "http://127.0.0.1:5000",
    "headers": {
      "Authorization": "Bearer user-auth-token"
    }
  }
}
```

To get the MCP configuration:
1. Visit the template market
2. Click on "获取MCP配置"
3. Copy the configuration JSON
4. Paste it into your IDE's MCP configuration

This single configuration allows your IDE to access all MCP tools provided by the server.

## Troubleshooting Connection Issues

If you encounter connection issues with the error message:
```
failed to create MCP client for DesignMaster: timeout waiting for endpoint
```

Please refer to the [MCP_CONNECTION_TROUBLESHOOTING.md](MCP_CONNECTION_TROUBLESHOOTING.md) file for detailed troubleshooting steps.

## Testing MCP Connection

You can use the provided test scripts to verify MCP connection:

```
# Test legacy endpoints
python test_mcp_connection.py

# Test standard MCP endpoints
python test_mcp_standard.py

# Test FastMCP service
python test_fastmcp.py
```

These scripts will test:
1. Health check endpoint
2. Authentication requirements
3. MCP tool endpoints with proper authentication
4. Standard MCP initialization endpoint
5. Standard MCP JSON-RPC endpoint
6. FastMCP service functionality
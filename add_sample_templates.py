from app import app
from models.models import db, User, Template, Placeholder, Prompt
from werkzeug.security import generate_password_hash

def add_sample_templates():
    """Add sample templates to the public market"""
    with app.app_context():
        # Check if we already have the sample templates
        existing_templates = Template.query.filter_by(name="Web应用设计模板").all()
        if existing_templates:
            print("Sample templates already exist")
            return
        
        # Get the first user (testuser) or create one if doesn't exist
        user = User.query.filter_by(username="testuser").first()
        if not user:
            # Create a sample user with hashed password
            hashed_password = generate_password_hash("password123")
            user = User(username="testuser", email="test@example.com", password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
        
        # Create a web application design template
        web_template_content = """# {{project_name}} Web应用设计文档

## 1. 项目概述
{{project_overview}}

## 2. 技术架构
{{tech_architecture}}

## 3. 数据库设计
```plantuml
{{database_schema}}
```

## 4. API接口设计
{{api_design}}

## 5. 前端设计
{{frontend_design}}

## 6. 安全设计
{{security_design}}

## 7. 部署方案
{{deployment_plan}}

## 8. 项目进度
{{project_timeline}}
"""
        
        web_template = Template(
            name="Web应用设计模板",
            content=web_template_content,
            description="适用于Web应用程序的设计文档模板，包含完整的架构设计和开发规范",
            user_id=user.id,
            is_public=True
        )
        db.session.add(web_template)
        db.session.commit()
        
        # Create placeholders for web template
        web_placeholders = [
            ("project_name", "项目名称", "任务管理系统"),
            ("project_overview", "项目概述", "一个基于Web的任务管理系统，用于团队协作和任务跟踪"),
            ("tech_architecture", "技术架构", "前端：React + Redux\n后端：Node.js + Express\n数据库：MongoDB\n部署：Docker + Kubernetes"),
            ("database_schema", "数据库设计图", "@startuml\nentity User {\n  id: ObjectId\n  username: String\n  email: String\n}\nentity Task {\n  id: ObjectId\n  title: String\n  description: String\n  status: String\n  assigned_to: ObjectId\n}\nUser ||--o{ Task\n@enduml"),
            ("api_design", "API接口设计", "GET /api/tasks - 获取所有任务\nPOST /api/tasks - 创建新任务\nPUT /api/tasks/:id - 更新任务\nDELETE /api/tasks/:id - 删除任务"),
            ("frontend_design", "前端设计", "使用React组件化开发，采用Ant Design组件库，响应式设计支持移动端"),
            ("security_design", "安全设计", "JWT身份验证\n密码加密存储\nCSRF防护\nXSS防护"),
            ("deployment_plan", "部署方案", "使用Docker容器化部署，通过Kubernetes进行编排，Nginx反向代理"),
            ("project_timeline", "项目进度", "需求分析：1周\n技术选型：3天\n原型设计：1周\n开发阶段：4周\n测试阶段：2周\n部署上线：3天")
        ]
        
        for name, description, example in web_placeholders:
            placeholder = Placeholder(
                name=name,
                description=description,
                example=example,
                template_id=web_template.id
            )
            db.session.add(placeholder)
        
        # Create prompts for web template
        web_prompts = [
            "请提供项目名称和简要概述",
            "请描述技术架构，包括前端、后端、数据库和部署技术",
            "请使用PlantUML设计数据库模式",
            "请设计API接口，包括HTTP方法、路径和参数",
            "请描述前端设计方案，包括技术栈和UI框架",
            "请说明安全设计方案，包括身份验证和防护措施",
            "请制定部署方案，包括服务器环境和部署流程",
            "请制定项目进度计划，包括各阶段的时间安排"
        ]
        
        for i, content in enumerate(web_prompts):
            prompt = Prompt(
                order=i,
                content=content,
                template_id=web_template.id
            )
            db.session.add(prompt)
        
        # Create a microservices design template
        microservices_template_content = """# {{project_name}} 微服务架构设计文档

## 1. 项目背景
{{project_background}}

## 2. 架构设计原则
{{design_principles}}

## 3. 微服务拆分
{{service_split}}

## 4. 服务间通信
{{service_communication}}

## 5. 数据管理策略
{{data_management}}

## 6. 安全策略
{{security_strategy}}

## 7. 监控与日志
{{monitoring_logging}}

## 8. 部署架构
{{deployment_architecture}}

## 9. 容错与恢复
{{fault_tolerance}}

## 10. 性能优化
{{performance_optimization}}
"""
        
        microservices_template = Template(
            name="微服务架构模板",
            content=microservices_template_content,
            description="适用于微服务架构系统的设计文档模板，包含服务拆分、通信和部署等关键内容",
            user_id=user.id,
            is_public=True
        )
        db.session.add(microservices_template)
        db.session.commit()
        
        # Create placeholders for microservices template
        microservices_placeholders = [
            ("project_name", "项目名称", "电商平台"),
            ("project_background", "项目背景", "一个B2C电商平台，支持商品浏览、购物车、订单管理等功能"),
            ("design_principles", "设计原则", "单一职责原则\n高内聚低耦合\n无状态服务\n容错性设计"),
            ("service_split", "微服务拆分", "用户服务：负责用户注册、登录、权限管理\n商品服务：负责商品信息管理\n订单服务：负责订单创建、支付、发货\n支付服务：负责支付处理\n库存服务：负责库存管理"),
            ("service_communication", "服务间通信", "同步通信：RESTful API\n异步通信：消息队列（RabbitMQ）\n服务发现：Consul\n负载均衡：Nginx"),
            ("data_management", "数据管理策略", "每个服务独立数据库\n分布式事务：Saga模式\n数据一致性：最终一致性\n数据备份：每日定时备份"),
            ("security_strategy", "安全策略", "API网关统一认证\nJWT Token\n服务间通信加密\n数据传输加密（HTTPS）"),
            ("monitoring_logging", "监控与日志", "Prometheus + Grafana监控\nELK日志收集分析\n分布式链路追踪：Zipkin\n告警机制：邮件+短信"),
            ("deployment_architecture", "部署架构", "Docker容器化\nKubernetes编排\nHelm包管理\n蓝绿部署策略"),
            ("fault_tolerance", "容错与恢复", "熔断机制：Hystrix\n限流策略：令牌桶算法\n降级策略：返回缓存数据\n自动恢复：健康检查+自动重启"),
            ("performance_optimization", "性能优化", "缓存策略：Redis多级缓存\n数据库优化：索引优化+读写分离\nCDN加速：静态资源\n异步处理：消息队列解耦")
        ]
        
        for name, description, example in microservices_placeholders:
            placeholder = Placeholder(
                name=name,
                description=description,
                example=example,
                template_id=microservices_template.id
            )
            db.session.add(placeholder)
        
        # Create prompts for microservices template
        microservices_prompts = [
            "请提供项目名称和背景介绍",
            "请说明架构设计原则和考虑因素",
            "请详细描述微服务的拆分方案",
            "请说明服务间的通信机制",
            "请制定数据管理策略",
            "请设计安全策略",
            "请制定监控和日志方案",
            "请设计部署架构",
            "请说明容错和恢复机制",
            "请制定性能优化方案"
        ]
        
        for i, content in enumerate(microservices_prompts):
            prompt = Prompt(
                order=i,
                content=content,
                template_id=microservices_template.id
            )
            db.session.add(prompt)
        
        # Create a mobile app design template
        mobile_template_content = """# {{project_name}} 移动应用设计文档

## 1. 应用概述
{{app_overview}}

## 2. 技术选型
{{tech_stack}}

## 3. 功能模块设计
{{feature_modules}}

## 4. UI/UX设计
{{ui_ux_design}}

## 5. 数据存储设计
{{data_storage}}

## 6. 网络通信设计
{{network_communication}}

## 7. 性能优化方案
{{performance_optimization}}

## 8. 安全方案
{{security_plan}}

## 9. 测试策略
{{testing_strategy}}

## 10. 发布计划
{{release_plan}}
"""
        
        mobile_template = Template(
            name="移动应用模板",
            content=mobile_template_content,
            description="适用于移动应用的设计文档模板，包含UI设计、性能优化和发布计划等",
            user_id=user.id,
            is_public=True
        )
        db.session.add(mobile_template)
        db.session.commit()
        
        # Create placeholders for mobile template
        mobile_placeholders = [
            ("project_name", "项目名称", "健康助手App"),
            ("app_overview", "应用概述", "一款健康管理应用，提供运动记录、饮食建议、健康数据监测等功能"),
            ("tech_stack", "技术选型", "前端：React Native\n状态管理：Redux\n后端：Node.js + Express\n数据库：MongoDB\n推送服务：Firebase Cloud Messaging"),
            ("feature_modules", "功能模块设计", "1. 用户模块：注册登录、个人资料\n2. 运动模块：运动记录、数据分析\n3. 饮食模块：饮食记录、营养分析\n4. 健康模块：数据监测、健康报告\n5. 社交模块：好友互动、分享"),
            ("ui_ux_design", "UI/UX设计", "设计风格：Material Design\n色彩方案：蓝绿色主题\n交互设计：手势操作、动画效果\n适配方案：响应式布局支持不同屏幕尺寸"),
            ("data_storage", "数据存储设计", "本地存储：AsyncStorage缓存用户偏好\n远程存储：MongoDB存储用户数据\n文件存储：Firebase Storage存储图片\n数据同步：WebSocket实时同步"),
            ("network_communication", "网络通信设计", "RESTful API与后端通信\nGraphQL查询优化\n图片上传下载\n离线数据同步"),
            ("performance_optimization", "性能优化方案", "图片懒加载\n列表虚拟化\n代码分割\n内存泄漏检测"),
            ("security_plan", "安全方案", "数据传输加密（HTTPS）\n本地数据加密\n生物识别认证\n权限控制"),
            ("testing_strategy", "测试策略", "单元测试：Jest\nUI测试：Detox\n性能测试：React Native Performance\n自动化测试：Appium"),
            ("release_plan", "发布计划", "Alpha测试：内部测试\nBeta测试：邀请用户测试\n正式发布：应用商店上线\n版本迭代：每两周一个小版本")
        ]
        
        for name, description, example in mobile_placeholders:
            placeholder = Placeholder(
                name=name,
                description=description,
                example=example,
                template_id=mobile_template.id
            )
            db.session.add(placeholder)
        
        # Create prompts for mobile template
        mobile_prompts = [
            "请提供应用名称和概述",
            "请说明技术选型和考虑因素",
            "请详细描述功能模块设计",
            "请设计UI/UX方案",
            "请制定数据存储方案",
            "请设计网络通信机制",
            "请制定性能优化方案",
            "请设计安全方案",
            "请制定测试策略",
            "请制定发布计划"
        ]
        
        for i, content in enumerate(mobile_prompts):
            prompt = Prompt(
                order=i,
                content=content,
                template_id=mobile_template.id
            )
            db.session.add(prompt)
        
        db.session.commit()
        
        print("Sample templates added successfully!")

if __name__ == "__main__":
    add_sample_templates()
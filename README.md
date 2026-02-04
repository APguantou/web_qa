# Web开发项目配置说明

### 第1步：下载python包
将下面的命令复制到pycharm的命令行（terminal）中执行
```bash
pip install flask
pip install flask_migrate
pip install flask_mail
pip install wtforms
pip install flask_sqlalchemy
pip install datetime
pip install email_validator
```

### 配置文件修改
修改当前目录`config.py`文件中的配置项

| 配置项                           | 说明                     |
|--------------------------------|------------------------|
| [SECRET_KEY](config.py)        | 应用密钥 - 设置一个安全的密码       |
| [PASSWORD](config.py)          | 数据库密码 - 替换为实际的数据库root密码 |
| [MAIL_SERVER](config.py)       | 邮箱服务器 - 填入邮箱服务器地址（默认QQ邮箱）|
| [MAIL_USERNAME](config.py)     | 邮箱账号 - 使用的实际邮箱地址      |
| [MAIL_PASSWORD](config.py)     | 邮箱授权码 - 邮箱的授权码（非登录密码）  |
| [MAIL_DEFAULT_SENDER](config.py)| 默认发件人 - 与邮箱账号保持一致     |


### 数据库设置
将下面的命令复制到navicat查询控制台中执行，注意修改表名
```sql
CREATE DATABASE webnew;
USE webnew;

CREATE TABLE IF NOT EXISTS user_02 (
    id INTEGER PRIMARY KEY auto_increment,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(400) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    join_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    post_count INTEGER DEFAULT 0,
    points INTEGER DEFAULT 0,
    level INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS email_captcha_02 (
    id INTEGER PRIMARY KEY auto_increment,
    email VARCHAR(100) NOT NULL,
    captcha VARCHAR(200) NOT NULL
);
CREATE TABLE IF NOT EXISTS question_02 (
    id INTEGER PRIMARY KEY auto_increment,
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    author_id INTEGER,
    view_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    favorite_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    FOREIGN KEY (author_id) REFERENCES user_02(id)
);
CREATE TABLE IF NOT EXISTS question_favorites_02 (
    favorite_id INTEGER PRIMARY KEY auto_increment,
    user_id INTEGER NOT NULL,
    ques_id INTEGER NOT NULL,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_02(id),
    FOREIGN KEY (ques_id) REFERENCES question_02(id)
);
CREATE TABLE IF NOT EXISTS question_likes_02 (
    like_id INTEGER PRIMARY KEY auto_increment,
    user_id INTEGER NOT NULL,
    ques_id INTEGER NOT NULL,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_02(id),
    FOREIGN KEY (ques_id) REFERENCES question_02(id)
);
CREATE TABLE IF NOT EXISTS question_comments_02 (
    comment_id INTEGER PRIMARY KEY auto_increment,
    user_id INTEGER NOT NULL,
    ques_id INTEGER NOT NULL,
    comment_content TEXT NOT NULL,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_02(id),
    FOREIGN KEY (ques_id) REFERENCES question_02(id)
);

INSERT INTO user_02 (username, password, email, post_count, points, level) VALUES
('张三', 'pbkdf2:sha256:260000$...', 'zhangsan@example.com', 0, 0, 0),
('李四', 'pbkdf2:sha256:260000$...', 'lisi@example.com', 0, 0, 0),
('王五', 'pbkdf2:sha256:260000$...', 'wangwu@example.com', 0, 0, 0),
('赵六', 'pbkdf2:sha256:260000$...', 'zhaoliu@example.com', 0, 0, 0),
('钱七', 'pbkdf2:sha256:260000$...', 'qianqi@example.com', 0, 0, 0),
('孙八', 'pbkdf2:sha256:260000$...', 'sunba@example.com', 0, 0, 0),
('周九', 'pbkdf2:sha256:260000$...', 'zhoujiu@example.com', 0, 0, 0),
('吴十', 'pbkdf2:sha256:260000$...', 'wushi@example.com', 0, 0, 0),
('郑十一', 'pbkdf2:sha256:260000$...', 'zhengshiyi@example.com', 0, 0, 0),
('陈十二', 'pbkdf2:sha256:260000$...', 'chenshier@example.com', 0, 0, 0);

INSERT INTO question_02 (title, content, author_id, view_count, like_count, favorite_count, comment_count) VALUES
('Python中的装饰器如何工作？', '我对Python装饰器的概念感到困惑，希望能得到详细的解释', 1, 0, 0, 0, 0),
('Flask框架的路由机制详解', '如何在Flask中设置复杂的路由规则？', 2, 0, 0, 0, 0),
('数据库索引优化策略', '什么样的情况下应该创建索引？有哪些优化技巧？', 3, 0, 0, 0, 0),
('JavaScript异步编程最佳实践', '关于Promise和async/await的使用场景和最佳实践', 4, 0, 0, 0, 0),
('CSS Grid布局完全指南', 'Grid布局与Flexbox的区别以及使用场景', 5, 0, 0, 0, 0),
('机器学习中的过拟合问题', '如何识别和解决模型的过拟合问题？', 6, 0, 0, 0, 0),
('Docker容器编排最佳实践', '使用Docker Compose进行多容器应用管理', 7, 0, 0, 0, 0),
('React Hooks使用技巧', '如何自定义Hooks以及常见陷阱', 8, 0, 0, 0, 0),
('网络安全基础概念', 'Web应用常见的安全漏洞及防护措施', 9, 0, 0, 0, 0),
('Python多线程编程', 'threading和multiprocessing模块的使用区别', 10, 0, 0, 0, 0),
('RESTful API设计原则', '如何设计符合REST规范的API接口', 1, 0, 0, 0, 0),
('Vue.js响应式系统原理', 'Vue3中的Proxy和Vue2中的Object.defineProperty的区别', 2, 0, 0, 0, 0),
('SQL查询性能优化', 'EXPLAIN命令解读和查询优化技巧', 3, 0, 0, 0, 0),
('微服务架构设计模式', '服务拆分原则和通信机制选择', 4, 0, 0, 0, 0),
('Node.js事件循环机制', '事件循环、任务队列和宏任务微任务详解', 5, 0, 0, 0, 0),
('深度学习基础概念', '神经网络的基本构成和训练过程', 6, 0, 0, 0, 0),
('Git版本控制高级技巧', '分支管理和冲突解决最佳实践', 7, 0, 0, 0, 0),
('前端性能优化策略', '页面加载速度和运行性能优化方法', 8, 0, 0, 0, 0),
('Linux系统管理基础', '常用命令和系统监控工具', 9, 0, 0, 0, 0),
('移动端开发技术选型', '原生开发、混合开发和跨平台框架对比', 10, 0, 0, 0, 0),
('云原生架构实践', '容器化、服务网格和Serverless技术应用', 1, 0, 0, 0, 0),
('TypeScript类型系统', '泛型、接口和类型推断的高级用法', 2, 0, 0, 0, 0),
('消息队列应用场景', 'RabbitMQ和Kafka的特点及使用场景', 3, 0, 0, 0, 0),
('缓存策略设计', 'Redis和Memcached的使用场景对比', 4, 0, 0, 0, 0),
('API网关设计与实现', '服务聚合和流量管控机制', 5, 0, 0, 0, 0),
('DevOps自动化流程', 'CI/CD流水线搭建和部署策略', 6, 0, 0, 0, 0),
('大数据处理框架对比', 'Hadoop和Spark框架特点分析', 7, 0, 0, 0, 0),
('区块链技术基础', '共识算法和加密机制详解', 8, 0, 0, 0, 0),
('GraphQL vs REST', '两种API设计方式的优缺点对比', 9, 0, 0, 0, 0),
('Web安全渗透测试', '常见的安全测试方法和工具', 10, 0, 0, 0, 0);
```

### 功能简介
##### 1、主页
* **导航栏**：包含天气信息、搜索框、用户名称信息、学校官网链接、发布问答链接、热门榜单链接、登录按钮、注册按钮、登出按钮 
* **问答列表**：包含问答标题、作者、发布时间、浏览量、点赞数、收藏数、评论数
* **分页按钮**：每页显示10个问答，显示页码按钮
* **搜索框**：根据输入的内容筛选问答标题，展示搜索结果

##### 2、发布问答页面
包含标题输入框、内容输入框、发布按钮

##### 3、热门榜单页面
* **帖子列表**：根据问答浏览量排序，展示浏览量最高的10个问答，包含问答标题、作者、发布时间、浏览量、点赞数、收藏数、评论数 
* **创作者列表**：根据作者积分排序，展示积分最高的10个作者，包含问答作者、积分

##### 4、用户信息页面
* **导航栏**：包含返回首页、注销账户、登出（退出登陆）
* **用户信息**：展示用户名称、邮箱、注册时间、问答数量、积分、用户等级
* **用户积分**：根据评论数量、发帖收缩的点赞数、收藏数计算积分
* **用户等级**：根据用户积分计算等级，每50积分一个等级，超过500分均为Lv10
* **用户内容**：分别展示用户发布的问答、用户点赞的问答、用户收藏的问答、用户评论的问答

##### 5、登录/注册页面
* **登录页面**：输入邮箱和密码登录
* **注册页面**：输入邮箱、验证码、用户名、密码注册
* **找回密码页面**：输入邮箱、验证码、重置密码
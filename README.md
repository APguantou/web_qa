# Web开发项目配置说明

### 需要下载的python包
| 包名               | 作用        |
|--------------------|-------------|
| flask              | 创建Web应用  |
| flask_migrate      | 数据库迁移   |
| flask_mail         | 邮件发送     |
| wtforms            | 创建表单     |
| flask_sqlalchemy   | 数据库操作   |
| datetime           | 表示时间     |
| email_validator    | Email验证器  |


下载命令如下：
```bash
pip install flask
pip install flask_migrate
pip install flask_mail
pip install wtforms
pip install flask_sqlalchemy
pip install datetime
pip install email_validator
```

### 数据库设置

```sql
CREATE DATABASE webnew;
USE webnew;
    
create table alembic_version
(
    version_num varchar(32) not null
        primary key
);

create table email_captcha_02
(
    id      int auto_increment
        primary key,
    email   varchar(100) not null,
    captcha varchar(200) not null
);

-- auto-generated definition
create table question_02
(
    id             int auto_increment
        primary key,
    title          varchar(100)                       not null,
    content        text                               not null,
    create_time    datetime default CURRENT_TIMESTAMP null,
    author_id      int                                null,
    view_count     int                                null,
    like_count     int                                null,
    favorite_count int                                null,
    comment_count  int                                null,
    constraint question_02_ibfk_1
        foreign key (author_id) references user_02 (id)
);

create index author_id
    on question_02 (author_id);

-- auto-generated definition
create table question_comments_02
(
    comment_id      int auto_increment
        primary key,
    user_id         int      not null,
    ques_id         int      not null,
    comment_content text     not null,
    create_time     datetime null,
    constraint question_comments_02_ibfk_1
        foreign key (ques_id) references question_02 (id),
    constraint question_comments_02_ibfk_2
        foreign key (user_id) references user_02 (id)
);

create index ques_id
    on question_comments_02 (ques_id);

create index user_id
    on question_comments_02 (user_id);

-- auto-generated definition
create table question_favorites_02
(
    favorite_id int auto_increment
        primary key,
    user_id     int      not null,
    ques_id     int      not null,
    create_time datetime null,
    constraint question_favorites_02_ibfk_1
        foreign key (ques_id) references question_02 (id),
    constraint question_favorites_02_ibfk_2
        foreign key (user_id) references user_02 (id)
);

create index ques_id
    on question_favorites_02 (ques_id);

create index user_id
    on question_favorites_02 (user_id);

-- auto-generated definition
create table question_likes_02
(
    like_id     int auto_increment
        primary key,
    user_id     int      not null,
    ques_id     int      not null,
    create_time datetime null,
    constraint question_likes_02_ibfk_1
        foreign key (ques_id) references question_02 (id),
    constraint question_likes_02_ibfk_2
        foreign key (user_id) references user_02 (id)
);

create index ques_id
    on question_likes_02 (ques_id);

create index user_id
    on question_likes_02 (user_id);

-- auto-generated definition
create table user_02
(
    id         int auto_increment
        primary key,
    username   varchar(100)                       not null,
    password   varchar(400)                       not null,
    email      varchar(100)                       not null,
    join_time  datetime default CURRENT_TIMESTAMP null,
    post_count int                                null,
    points     int                                null,
    level      int                                null,
    constraint email
        unique (email)
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
('Python中的装饰器如何工作？', '我对Python装饰器的概念感到困惑，希望能得到详细的解释', 21, 0, 0, 0, 0),
('Flask框架的路由机制详解', '如何在Flask中设置复杂的路由规则？', 22, 0, 0, 0, 0),
('数据库索引优化策略', '什么样的情况下应该创建索引？有哪些优化技巧？', 23, 0, 0, 0, 0),
('JavaScript异步编程最佳实践', '关于Promise和async/await的使用场景和最佳实践', 24, 0, 0, 0, 0),
('CSS Grid布局完全指南', 'Grid布局与Flexbox的区别以及使用场景', 25, 0, 0, 0, 0),
('机器学习中的过拟合问题', '如何识别和解决模型的过拟合问题？', 26, 0, 0, 0, 0),
('Docker容器编排最佳实践', '使用Docker Compose进行多容器应用管理', 27, 0, 0, 0, 0),
('React Hooks使用技巧', '如何自定义Hooks以及常见陷阱', 28, 0, 0, 0, 0),
('网络安全基础概念', 'Web应用常见的安全漏洞及防护措施', 29, 0, 0, 0, 0),
('Python多线程编程', 'threading和multiprocessing模块的使用区别', 30, 0, 0, 0, 0),
('RESTful API设计原则', '如何设计符合REST规范的API接口', 21, 0, 0, 0, 0),
('Vue.js响应式系统原理', 'Vue3中的Proxy和Vue2中的Object.defineProperty的区别', 22, 0, 0, 0, 0),
('SQL查询性能优化', 'EXPLAIN命令解读和查询优化技巧', 23, 0, 0, 0, 0),
('微服务架构设计模式', '服务拆分原则和通信机制选择', 24, 0, 0, 0, 0),
('Node.js事件循环机制', '事件循环、任务队列和宏任务微任务详解', 25, 0, 0, 0, 0),
('深度学习基础概念', '神经网络的基本构成和训练过程', 26, 0, 0, 0, 0),
('Git版本控制高级技巧', '分支管理和冲突解决最佳实践', 27, 0, 0, 0, 0),
('前端性能优化策略', '页面加载速度和运行性能优化方法', 28, 0, 0, 0, 0),
('Linux系统管理基础', '常用命令和系统监控工具', 29, 0, 0, 0, 0),
('移动端开发技术选型', '原生开发、混合开发和跨平台框架对比', 30, 0, 0, 0, 0),
('云原生架构实践', '容器化、服务网格和Serverless技术应用', 21, 0, 0, 0, 0),
('TypeScript类型系统', '泛型、接口和类型推断的高级用法', 22, 0, 0, 0, 0),
('消息队列应用场景', 'RabbitMQ和Kafka的特点及使用场景', 23, 0, 0, 0, 0),
('缓存策略设计', 'Redis和Memcached的使用场景对比', 24, 0, 0, 0, 0),
('API网关设计与实现', '服务聚合和流量管控机制', 25, 0, 0, 0, 0),
('DevOps自动化流程', 'CI/CD流水线搭建和部署策略', 26, 0, 0, 0, 0),
('大数据处理框架对比', 'Hadoop和Spark框架特点分析', 27, 0, 0, 0, 0),
('区块链技术基础', '共识算法和加密机制详解', 28, 0, 0, 0, 0),
('GraphQL vs REST', '两种API设计方式的优缺点对比', 29, 0, 0, 0, 0),
('Web安全渗透测试', '常见的安全测试方法和工具', 30, 0, 0, 0, 0);

```


### 配置文件修改
修改`config.py`文件和`auth.py`中的配置项

| 配置项                           | 说明                     |
|--------------------------------|------------------------|
| [SECRET_KEY](config.py)        | 应用密钥 - 设置一个安全的密码       |
| [PASSWORD](config.py)          | 数据库密码 - 替换为实际的数据库root密码 |
| [MAIL_SERVER](config.py)       | 邮箱服务器 - 填入邮箱服务器地址（默认QQ邮箱）|
| [MAIL_USERNAME](config.py)     | 邮箱账号 - 使用的实际邮箱地址      |
| [MAIL_PASSWORD](config.py)     | 邮箱授权码 - 邮箱的授权码（非登录密码）  |
| [MAIL_DEFAULT_SENDER](config.py)| 默认发件人 - 与邮箱账号保持一致     |
| [mail_test函数的测试邮箱](auth.py)| 测试邮箱 - 与邮箱账号保持一致      |


### 项目文件结构一览
```
           
```

### 项目运行步骤

### 核心文件说明

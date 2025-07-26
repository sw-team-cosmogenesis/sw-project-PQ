# 项目名称（例如：AI演讲互动系统）

## 📚 项目简介
一个简单的，供演讲者和听众使用的平台。演讲者可以创建演讲并上传材料，而后通过将材料发给 AI 来自动生成题目，而后推送给观众作答，以测试观众的注意力是否集中于演讲。

## 🚀 技术栈

| 层级 | 技术        |
|------|-------------|
| 前端 | Vue3, Vue Router, Axios, |
| 构建工具 | Vite |
| 后端 | Django, Django REST framework |
| 数据库 | PostgreSQL |
| AI支持 |  通义千问 |
| 其他 | 阿里云 OSS（图床）, CORS, JWT  |

## 📁 项目结构

```bash
├── frontend/
    ├── \---src
    |   App.vue
    |   main.ts
    |   
    +---assets   
    +---components
    |       LeftSideNavBar.vue
    |       PresentationDropdownMenu.vue
    |       PresenterLeftSidebar.vue
    |       ProfileBox.vue
    |       QuizCard.vue
    |       TopNavBar.vue
    |       
    +---router
    |       index.ts
    |       
    +---utils
    |       api.ts
    |       request.ts
    |       
    \---views
            EditView.vue
            Home.vue
            LoginPage.vue
            PresentationsPage.vue
            PresentationsView.vue
            PresenterPage.vue
            QuizPage.vue
            RegisterPage.vue
+---djangoback
|   manage.py
|   requirements.txt
|   structure.txt
|   +---djangoback
|   |   .env
|   |   admin.py
|   |   asgi.py
|   |   models.py
|   |   serializers.py
|   |   settings.py
|   |   urls.py
|   |   utils.py
|   |   views.py
|   |   wsgi.py
|   |   __init__.py
|   |   
|   +---migrations
+---poppler-24.08.0
├── README.md
└── requirements.txt   # 后端依赖

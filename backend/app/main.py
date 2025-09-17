from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, class_management, assignment, submission

app = FastAPI()

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # 前端开发服务器地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(class_management.router)
app.include_router(assignment.router)
app.include_router(submission.router)

@app.get("/")
def root():
    return {"message": "welcome to APRP(automated paper review platform)"}





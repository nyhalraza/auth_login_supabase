import os
from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

app = FastAPI()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}


# from fastapi import FastAPI, Path, HTTPException, Response
# from typing import Optional
# from pydantic import BaseModel
# import storage

# app = FastAPI()


# class Task(BaseModel):
#     title: str
#     done: bool = False


# class UpdateTask(BaseModel):
#     title: Optional[str] = None
#     done: Optional[bool] = None


# @app.get("/")
# def index():
#     return {
#         "name": "Task API",
#         "version": "2.0",
#         "storage": "Postgres",
#         "endpoints": ["/tasks", "/tasks/{id}"]
#     }


# @app.get("/health")
# def health():
#     return {"status": "ok"}


# @app.get("/tasks")
# def get_all_tasks():
#     return storage.list_tasks()


# @app.get("/tasks/{task_id}")
# def get_task_by_id(task_id: int = Path(..., gt=0, description="Task ID")):
#     task = storage.get_task(task_id)
#     if task is None:
#         raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
#     return task


# @app.post("/tasks", status_code=201)
# def create_task(task: Task):
#     title = task.title.strip()
#     if not title:
#         raise HTTPException(status_code=400, detail="Title cannot be empty")
#     return storage.create_task(title, task.done)


# @app.put("/tasks/{task_id}")
# def update_task(task_id: int, task: UpdateTask):
#     title = task.title
#     if title is not None:
#         title = title.strip()
#         if not title:
#             raise HTTPException(status_code=400, detail="Title cannot be empty")
#     updated = storage.update_task(task_id, title, task.done)
#     if updated is None:
#         raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
#     return updated


# @app.delete("/tasks/{task_id}", status_code=204)
# def delete_task(task_id: int):
#     if not storage.delete_task(task_id):
#         raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
#     return Response(status_code=204)
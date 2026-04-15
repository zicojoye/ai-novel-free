#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的应用测试
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI(title="AI Novel Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "AI Novel Platform API", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/api/projects")
async def get_projects():
    return {"projects": [], "total": 0}


if __name__ == "__main__":
    print("AI Novel Platform Starting...")
    uvicorn.run("test_app:app", host="0.0.0.0", port=8000, reload=True)

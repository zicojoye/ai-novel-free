# 多阶段构建 - 后端

# 阶段1: 构建阶段
FROM python:3.11-slim AS builder

WORKDIR /app

# 安装构建依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY backend/requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir --user -r requirements.txt

# 阶段2: 生产阶段
FROM python:3.11-slim AS production

WORKDIR /app

# 安装运行时依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        && rm -rf /var/lib/apt/lists/*

# 复制构建产物
COPY --from=builder /root/.local /root/.local

# 确保脚本在PATH中
ENV PATH=/root/.local/bin:$PATH

# 复制应用代码
COPY backend/ ./app/

# 创建数据目录
RUN mkdir -p /app/data/uploads \
    /app/data/logs \
    /app/data/db \
    /app/data/cache

# 创建非root用户
RUN groupadd -r appuser && \
    useradd -r -g appuser -u 1001 appuser && \
    chown -R appuser:appuser /app

# 切换到非root用户
USER appuser

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动应用
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

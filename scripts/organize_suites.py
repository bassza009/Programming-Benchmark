#!/usr/bin/env python3
import os

BASE_DIR = r"D:\github\Programming-Benchmark\main_web_benchmark"
SUITES = [
    (os.path.join(BASE_DIR, "GET", "get_no_index"), "get-no-index"),
    (os.path.join(BASE_DIR, "GET", "get_with_index"), "get-with-index"),
    (os.path.join(BASE_DIR, "POST"), "post")
]

compose_template = """version: '3.8'

services:
  server-python:
    build:
      context: frameworks/python/fastapi
      dockerfile: Dockerfile
    container_name: server-python-{slug}
    ports:
      - "8001:8001"
    extra_hosts:
      - "host.docker.internal:host-gateway"
    environment:
      DB_HOST: host.docker.internal
      DB_PORT: 3306
      DB_USER: admin
      DB_PASS: secret
      DB_NAME: benchmark_db
    ulimits:
      nofile:
        soft: 65535
        hard: 65535

  server-node:
    build:
      context: frameworks/nodejs/fastify
      dockerfile: Dockerfile
    container_name: server-node-{slug}
    ports:
      - "8002:8002"
    extra_hosts:
      - "host.docker.internal:host-gateway"
    environment:
      DB_HOST: host.docker.internal
      DB_PORT: 3306
      DB_USER: admin
      DB_PASS: secret
      DB_NAME: benchmark_db
    ulimits:
      nofile:
        soft: 65535
        hard: 65535

  server-php:
    build:
      context: frameworks/php/swoole
      dockerfile: Dockerfile
    container_name: server-php-{slug}
    ports:
      - "8003:8003"
    extra_hosts:
      - "host.docker.internal:host-gateway"
    environment:
      DB_HOST: host.docker.internal
      DB_PORT: 3306
      DB_USER: admin
      DB_PASS: secret
      DB_NAME: benchmark_db
    ulimits:
      nofile:
        soft: 65535
        hard: 65535

  server-go:
    build:
      context: frameworks/go/fiber
      dockerfile: Dockerfile
    container_name: server-go-{slug}
    ports:
      - "8004:8004"
    extra_hosts:
      - "host.docker.internal:host-gateway"
    environment:
      DB_HOST: host.docker.internal
      DB_PORT: 3306
      DB_USER: admin
      DB_PASS: secret
      DB_NAME: benchmark_db
    ulimits:
      nofile:
        soft: 65535
        hard: 65535

  server-java:
    build:
      context: frameworks/java/springboot
      dockerfile: Dockerfile
    container_name: server-java-{slug}
    ports:
      - "8005:8005"
    extra_hosts:
      - "host.docker.internal:host-gateway"
    environment:
      DB_HOST: host.docker.internal
      DB_PORT: 3306
      DB_USER: admin
      DB_PASS: secret
      DB_NAME: benchmark_db
    ulimits:
      nofile:
        soft: 65535
        hard: 65535
"""

for suite_dir, slug in SUITES:
    # 1. Update docker-compose.yml
    compose_path = os.path.join(suite_dir, "docker-compose.yml")
    with open(compose_path, "w", encoding="utf-8") as f:
        f.write(compose_template.format(slug=slug))
    print(f"Updated {compose_path}")

    # 2. Update run_bme_wrk.py
    bme_path = os.path.join(suite_dir, "run_bme_wrk.py")
    if os.path.exists(bme_path):
        with open(bme_path, "r", encoding="utf-8") as f:
            content = f.read()

        old_langs = """LANGUAGES = [
    {"name": "Python", "port": 8001, "cmd": ["python3", "server.py"]},
    {"name": "Node.js", "port": 8002, "cmd": ["node", "server.js"]},
    {"name": "PHP", "port": 8003, "cmd": ["php", "server.php"]},
    {"name": "Go", "port": 8004, "cmd": ["./server"]},
    {"name": "Java", "port": 8005, "cmd": ["java", "-jar", "app.jar"]}
]"""

        new_langs = """SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

LANGUAGES = [
    {"name": "Python", "port": 8001, "cmd": ["python3", "server.py"], "cwd": os.path.join(SCRIPT_DIR, "frameworks", "python", "fastapi")},
    {"name": "Node.js", "port": 8002, "cmd": ["node", "server.js"], "cwd": os.path.join(SCRIPT_DIR, "frameworks", "nodejs", "fastify")},
    {"name": "PHP", "port": 8003, "cmd": ["php", "server.php"], "cwd": os.path.join(SCRIPT_DIR, "frameworks", "php", "swoole")},
    {"name": "Go", "port": 8004, "cmd": ["./server"], "cwd": os.path.join(SCRIPT_DIR, "frameworks", "go", "fiber")},
    {"name": "Java", "port": 8005, "cmd": ["java", "-jar", "app.jar"], "cwd": os.path.join(SCRIPT_DIR, "frameworks", "java", "springboot")}
]"""

        if old_langs in content:
            content = content.replace(old_langs, new_langs)

        content = content.replace(
            'proc = subprocess.Popen(lang["cmd"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)',
            'proc = subprocess.Popen(lang["cmd"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=lang.get("cwd"))'
        )

        with open(bme_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {bme_path}")

print("All suite configs updated successfully!")

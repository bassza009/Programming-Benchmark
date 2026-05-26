#!/bin/bash

# Makefile-like script for common GET benchmark tasks

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

case "${1:-help}" in
    help)
        echo "GET Benchmark Helper"
        echo "==================="
        echo ""
        echo "Usage: ./manage.sh [command] [options]"
        echo ""
        echo "Commands:"
        echo "  start              Start all Docker containers"
        echo "  stop               Stop all Docker containers"
        echo "  restart            Restart all containers"
        echo "  status             Show container status"
        echo "  build              Build Docker images"
        echo "  clean              Remove containers and images"
        echo "  logs [service]     Show logs (optional: service name)"
        echo "  benchmark          Run benchmark (alias for run.sh)"
        echo "  shell [service]    Open shell in container"
        echo ""
        echo "Examples:"
        echo "  ./manage.sh start"
        echo "  ./manage.sh benchmark"
        echo "  ./manage.sh shell python_server"
        ;;
    
    start)
        echo "Starting Docker containers..."
        docker-compose up -d
        sleep 5
        ./manage.sh status
        ;;
    
    stop)
        echo "Stopping Docker containers..."
        docker-compose down
        ;;
    
    restart)
        echo "Restarting Docker containers..."
        docker-compose restart
        ./manage.sh status
        ;;
    
    status)
        echo "Container Status:"
        docker-compose ps
        ;;
    
    build)
        echo "Building Docker images..."
        docker-compose build
        ;;
    
    clean)
        echo "Cleaning up containers and images..."
        docker-compose down --rmi all
        echo "Cleaned!"
        ;;
    
    logs)
        if [ -z "$2" ]; then
            docker-compose logs -f
        else
            docker-compose logs -f "$2"
        fi
        ;;
    
    shell)
        if [ -z "$2" ]; then
            echo "Error: Service name required"
            echo "Available services: python_server, nodejs_server, php_server, go_server, java_server"
            exit 1
        fi
        docker-compose exec "$2" /bin/sh
        ;;
    
    benchmark)
        ./run.sh "${@:2}"
        ;;
    
    *)
        echo "Unknown command: $1"
        echo "Run './manage.sh help' for usage"
        exit 1
        ;;
esac

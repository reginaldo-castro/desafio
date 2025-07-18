#!/bin/bash
set -e

DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}

echo "🟦 Aguardando o banco de dados em $DB_HOST:$DB_PORT..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "✅ Banco de dados disponível!"

if [ ! -d "gerenciador_emprestimo" ]; then
    echo "🚀 Criando o projeto Django..."
    django-admin startproject gerenciador_emprestimo .
else
    echo "📁 Projeto Django já existe. Pulando criação."
fi

echo "⚙️ Aplicando migrações..."
python manage.py migrate --noinput

if [ -d "gerenciador_emprestimo/static" ]; then
  echo "📦 Coletando arquivos estáticos..."
  python manage.py collectstatic --noinput || echo "⚠️ Erro ignorado no collectstatic"
else
  echo "⏭️ Pasta 'static' não encontrada. Pulando collectstatic."
fi

echo "🔐 Corrigindo permissões de arquivos..."
chown -R 1000:1000 /app

echo "🚀 Iniciando servidor na porta 8000..."
python manage.py runserver 0.0.0.0:8000

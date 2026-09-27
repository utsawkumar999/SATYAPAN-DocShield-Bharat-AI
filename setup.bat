@echo off
cd /d e:\SIH
mkdir docs
mkdir backend\app
mkdir database

echo # DocShield AI X Master Plan > docs\implementation_plan.md
echo fastapi > backend\requirements.txt
echo uvicorn >> backend\requirements.txt
echo easyocr >> backend\requirements.txt
echo opencv-python-headless >> backend\requirements.txt
echo networkx >> backend\requirements.txt

echo from fastapi import FastAPI > backend\app\main.py
echo app = FastAPI() >> backend\app\main.py

echo CREATE TABLE IF NOT EXISTS verifications (id UUID PRIMARY KEY, risk_score INT); > database\schema.sql

echo.
echo ========================================================
echo  SUCCESS! ALL DOCSHIELD AI X FILES CREATED IN E:\SIH!
echo ========================================================
echo.
pause
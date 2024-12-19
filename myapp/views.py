import os
from django.shortcuts import render
from django.http import JsonResponse
from neo4j import GraphDatabase
from .utils.chatgpt import get_chatgpt_response  # 確保 utils.chatgpt.py 存在且正確
import logging
import json  
from openai import OpenAIError
from dotenv import load_dotenv

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()
# 初始化 Neo4j
NEO4J_URL = os.getenv("NEO4J_URL")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

try:
    driver = GraphDatabase.driver(NEO4J_URL, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    logger.info("成功連接 Neo4j 資料庫")
except Exception as e:
    logger.error(f"無法連接 Neo4j: {e}")
    driver = None

# 主頁
def index(request):
    return render(request, 'myapp/index.html')

# 處理檔案上傳
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            logger.info(f"收到文件上傳：{file.name}")
            return JsonResponse({'message': '文件上傳成功！'})
        return JsonResponse({'error': '沒有上傳文件'}, status=400)
    return JsonResponse({'error': '無效的請求方法'}, status=400)

# 處理網址
def process_url(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if url:
            logger.info(f"處理的 URL: {url}")
            return JsonResponse({"message": f"成功處理網址：{url}"})
    return JsonResponse({"error": "無效請求"}, status=400)

# AI 聊天功能
def chat_with_ai(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question')
            if question:
                # 呼叫 ChatGPT API
                ai_response = get_chatgpt_response(question)
                return JsonResponse({"result": str(ai_response)}, status=200)
            else:
                return JsonResponse({"error": "未提供問題"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"處理問題時發生錯誤: {str(e)}"}, status=500)
    return JsonResponse({"error": "不支援的請求方法"}, status=405)
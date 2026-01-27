import os
import sys

from dotenv import load_dotenv
from openai import AsyncOpenAI

# --- AI & Notification Configuration ---
load_dotenv()

# --- File Paths & Directories ---
STATE_FILE = "xianyu_state.json"
IMAGE_SAVE_DIR = "images"
CONFIG_FILE = "config.json"
os.makedirs(IMAGE_SAVE_DIR, exist_ok=True)

# 任务隔离的临时图片目录前缀
TASK_IMAGE_DIR_PREFIX = "task_images_"

# --- API URL Patterns ---
API_URL_PATTERN = "h5api.m.goofish.com/h5/mtop.taobao.idlemtopsearch.pc.search"
DETAIL_API_URL_PATTERN = "h5api.m.goofish.com/h5/mtop.taobao.idle.pc.detail"

# --- Environment Variables ---
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")
PROXY_URL = os.getenv("PROXY_URL")
NOTIFIER_URL = os.getenv("NOTIFIER_URL")
NTFY_TOPIC_URL = os.getenv("NTFY_TOPIC_URL")
GOTIFY_URL = os.getenv("GOTIFY_URL")
GOTIFY_TOKEN = os.getenv("GOTIFY_TOKEN")
BARK_URL = os.getenv("BARK_URL")
WX_BOT_URL = os.getenv("WX_BOT_URL")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_METHOD = os.getenv("WEBHOOK_METHOD", "POST").upper()
WEBHOOK_HEADERS = os.getenv("WEBHOOK_HEADERS")
WEBHOOK_CONTENT_TYPE = os.getenv("WEBHOOK_CONTENT_TYPE", "JSON").upper()
WEBHOOK_QUERY_PARAMETERS = os.getenv("WEBHOOK_QUERY_PARAMETERS")
WEBHOOK_BODY = os.getenv("WEBHOOK_BODY")
PCURL_TO_MOBILE = os.getenv("PCURL_TO_MOBILE", "false").lower() == "true"
RUN_HEADLESS = os.getenv("RUN_HEADLESS", "true").lower() != "false"
LOGIN_IS_EDGE = os.getenv("LOGIN_IS_EDGE", "false").lower() == "true"
RUNNING_IN_DOCKER = os.getenv("RUNNING_IN_DOCKER", "false").lower() == "true"
AI_DEBUG_MODE = os.getenv("AI_DEBUG_MODE", "false").lower() == "true"
SKIP_AI_ANALYSIS = os.getenv("SKIP_AI_ANALYSIS", "false").lower() == "true"
ENABLE_THINKING = os.getenv("ENABLE_THINKING", "false").lower() == "true"
ENABLE_RESPONSE_FORMAT = os.getenv("ENABLE_RESPONSE_FORMAT", "true").lower() == "true"

# --- Headers ---
IMAGE_DOWNLOAD_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# --- Client Initialization ---
# 检查配置是否齐全
if not all([BASE_URL, MODEL_NAME]):
    print("警告：未在 .env 文件中完整设置 OPENAI_BASE_URL 和 OPENAI_MODEL_NAME。AI相关功能可能无法使用。")
    client = None
else:
    try:
        if PROXY_URL:
            print(f"正在为AI请求使用HTTP/S代理: {PROXY_URL}")
            # httpx 会自动从环境变量中读取代理设置
            os.environ['HTTP_PROXY'] = PROXY_URL
            os.environ['HTTPS_PROXY'] = PROXY_URL

        # openai 客户端内部的 httpx 会自动从环境变量中获取代理配置
        client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL)
    except Exception as e:
        print(f"初始化 OpenAI 客户端时出错: {e}")
        client = None

# 检查AI客户端是否成功初始化
if not client:
    # 在 prompt_generator.py 中，如果 client 为 None，会直接报错退出
    # 在 spider_v2.py 中，AI分析会跳过
    # 为了保持一致性，这里只打印警告，具体逻辑由调用方处理
    pass

# 检查关键配置
if not all([BASE_URL, MODEL_NAME]) and 'prompt_generator.py' in sys.argv[0]:
    sys.exit("错误：请确保在 .env 文件中完整设置了 OPENAI_BASE_URL 和 OPENAI_MODEL_NAME。(OPENAI_API_KEY 对于某些服务是可选的)")

def get_ai_request_params(**kwargs):
    """
    构建AI请求参数，根据ENABLE_THINKING和ENABLE_RESPONSE_FORMAT环境变量决定是否添加相应参数
    """
    params = kwargs.copy()
    
    if ENABLE_THINKING:
        params["extra_body"] = {"enable_thinking": False}
    
    # 注意：在 ai_handler.py 中已经手动处理了 response_format，
    # 并且针对 gpt-4o-mini 等模型做了特殊处理。
    # 这里如果重复添加，可能会覆盖掉 ai_handler.py 中的逻辑，或者造成冲突。
    # 最安全的做法是：如果 kwargs 中已经有了，就不覆盖；如果没有，才根据环境变量添加。
    # if ENABLE_RESPONSE_FORMAT and "response_format" not in params:
    #    params["response_format"] = {"type": "json_object"}
    
    # 如果有代理设置
    if PROXY_URL:
        import httpx
        params["http_client"] = httpx.AsyncClient(proxy=PROXY_URL)
    
    # 过滤掉不支持的参数
    if "http_client" in params:
        del params["http_client"]

    # 针对 Gemini 等模型，如果不支持 response_format="json_object"，则移除该参数
    # 或者如果 response_format 导致 400 错误，可以在这里进行特殊处理
    # 目前 gemai.cc 的 [福利]gemini-3-flash-preview 是支持 json_object 的，但为了稳妥，
    # 我们可以通过 MODEL_NAME 来判断是否需要移除某些特定参数。
    # 这里暂时保持原样，因为测试脚本通过了。
    
    return params

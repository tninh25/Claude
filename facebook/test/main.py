import os
import requests
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

FB_APP_ID = os.getenv("FB_APP_ID")
FB_APP_SECRET = os.getenv("FB_APP_SECRET")
FB_REDIRECT_URI = os.getenv("FB_REDIRECT_URI")


# ================================
# 1. NÚT / LINK KẾT NỐI FACEBOOK
# ================================
@app.get("/connect-facebook")
def connect_facebook():
    scope = "email"
    oauth_url = (
        f"https://www.facebook.com/v24.0/dialog/oauth"
        f"?client_id={FB_APP_ID}"
        f"&redirect_uri={FB_REDIRECT_URI}"
        f"&scope={scope}"
    )
    return RedirectResponse(oauth_url)


# ================================
# 2. CALLBACK FACEBOOK
# ================================
@app.get("/facebook/callback")
def facebook_callback(code: str):
    # ----------------------------------
    # BƯỚC 1: ĐỔI CODE → USER TOKEN
    # ----------------------------------
    token_url = "https://graph.facebook.com/v24.0/oauth/access_token"
    token_params = {
        "client_id": FB_APP_ID,
        "redirect_uri": FB_REDIRECT_URI,
        "client_secret": FB_APP_SECRET,
        "code": code,
    }

    token_res = requests.get(token_url, params=token_params).json()

    if "access_token" not in token_res:
        return {
            "error": "Không lấy được User Access Token",
            "detail": token_res,
        }

    user_access_token = token_res["access_token"]

    # ----------------------------------
    # BƯỚC 2: LẤY PAGE ACCESS TOKEN
    # ----------------------------------
    pages_url = "https://graph.facebook.com/v24.0/me/accounts"
    pages_res = requests.get(
        pages_url, params={"access_token": user_access_token}
    ).json()

    if "data" not in pages_res or len(pages_res["data"]) == 0:
        return {
            "error": "Không tìm thấy fanpage",
            "detail": pages_res,
        }

    page = pages_res["data"][0]  # lấy fanpage đầu tiên
    page_id = page["id"]
    page_access_token = page["access_token"]

    # ----------------------------------
    # BƯỚC 3: ĐĂNG BÀI TEST
    # ----------------------------------
    post_url = f"https://graph.facebook.com/v24.0/{page_id}/feed"
    post_data = {
        "message": "✅ Bài test được đăng tự động từ FastAPI + OAuth Facebook",
        "access_token": page_access_token,
    }

    post_res = requests.post(post_url, data=post_data).json()

    if "id" not in post_res:
        return {
            "error": "Đăng bài thất bại",
            "detail": post_res,
        }

    return {
        "success": True,
        "page_name": page.get("name"),
        "page_id": page_id,
        "post_id": post_res["id"],
    }

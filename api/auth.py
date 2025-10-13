from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


from api.client import client_id, client, get_access_token, secret
from utils.helpers import update_env_file


# Express server
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Connection-Id",
    ],
)


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/hosted-link-destination")
async def webhook_callback(request: Request):
    payload = await request.json()

    if (
        payload.get("webhook_code") == "SESSION_FINISHED"
        and payload.get("status") == "success"
    ):
        public_tokens = payload.get("public_tokens", [])
        public_token = None if len(public_tokens) == 0 else public_tokens[0]

        if public_token != None:
            access_token = get_access_token(public_token=public_token)
            update_env_file(key="ACCESS_TOKEN", value=access_token)

        return {"received_token": public_token}

    return {"error": "Unable to process hosted link"}

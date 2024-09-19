import logging.config

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, PlainTextResponse

from configs import DEBUG, LOGGING_CONFIG, BASE_URL, REDIRECT_PATH
from db import async_session_maker
from models import ShortUrl, Click

logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI(debug=DEBUG)


@app.get("/generate", response_class=PlainTextResponse)
async def generate_short_url(url: str, request: Request) -> PlainTextResponse:
    meta = dict(request.query_params)
    meta.pop("url")
    async with async_session_maker() as db_session, db_session.begin():
        short_path = await ShortUrl.generate(db_session, url, meta)
        short_url = f"{BASE_URL}/{REDIRECT_PATH}/{short_path}"

        return PlainTextResponse(status_code=200, content=short_url)


@app.get(f"/{REDIRECT_PATH}/{{path}}")
async def redirect(path: str, request: Request):
    async with async_session_maker() as db_session, db_session.begin():
        short_url = await ShortUrl.get_full_url(db_session, path)

        click = Click(
            short_path=path,
            headers=dict(request.headers),
            cookies=request.cookies,
            success=short_url is not None
        )
        db_session.add(click)

    if short_url is None:
        raise HTTPException(status_code=404)

    return RedirectResponse(short_url.full_url, status_code=308)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8090, log_level="info")

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from googletrans import Translator
from pathlib import Path

app = FastAPI()

# Get the absolute path of the APP directory
BASE_DIR = Path(__file__).resolve().parent

# Mount static and templates folders correctly
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Initialize the Google Translator client
translator = Translator()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/translate", response_class=HTMLResponse)
async def translate_text(request: Request, text: str = Form(...), target_language: str = Form(...)):
    try:
        result = translator.translate(text, dest=target_language)
        translated_text = result.text
        return templates.TemplateResponse("index.html", {"request": request, "translated_text": translated_text, "text": text, "target_language": target_language})
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from datetime import date, datetime
import os

from image_generator import generate_progress_image

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/goal")
async def goal_image(
    goal: str = Query(..., description="Name of the goal"),
    start_date: date = Query(..., description="Start date of the goal"),
    goal_date: date = Query(..., description="Target date of the goal"),
    height: int = Query(2340, description="Height of the image"),
    width: int = Query(1080, description="Width of the image"),
    fill_color: str = Query("#ff6b35", description="Hex color for the dots")
):
    # For matching context precisely
    current_date = datetime.now().date()
    
    img_bytes = generate_progress_image(
        goal=goal,
        start_date=start_date,
        goal_date=goal_date,
        current_date=current_date,
        width=width,
        height=height,
        fill_color=fill_color
    )
    return Response(content=img_bytes, media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

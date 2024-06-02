import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from BlogAgent import blog_writer  # Assuming blog_writer is in a module named BlogAgent

# Initialize logging
logging.basicConfig(level=logging.INFO)
word_limit = 1000
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Allow CORS for local development (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProcessRequest(BaseModel):
    blog_topic: str
    audience: str
    tone: str
    specifications: str

@app.post("/process") 
async def process_input(request: ProcessRequest):
    blog_topic = request.blog_topic
    audience = request.audience
    tone = request.tone
    specifications = request.specifications 

    logging.info(f"Received blog_topic: {blog_topic}, audience: {audience}, tone:{tone}, specifications: {specifications}")
    
    try:
        # Call the blog_writer function
        processed_text = blog_writer(blog_topic, audience, tone, word_limit, specifications)
        logging.info(f"Processed text: {processed_text}")
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
    return {"processed_text": processed_text}
'''
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
'''
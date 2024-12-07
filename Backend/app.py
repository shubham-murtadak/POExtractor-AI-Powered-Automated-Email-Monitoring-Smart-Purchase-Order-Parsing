import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to fetch data
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your React app's URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/project-info")
async def get_project_info():
    return {
        "title": "POExtractor - Smart Purchase Order Parsing",
        "description": (
            "An AI-powered tool to classify and process purchase orders effortlessly! "
            "Automatically monitor emails, classify purchase orders, handle attachments, "
            "and extract critical data using Fine Tuned advanced Multimodal LLM models like LLaMA 3.2 and LLAVA"
        ),
        "features": [
            "Automatic email monitoring and classification",
            "Attachment handling (PDFs, Images, Excel, and more)",
            "AI-powered data extraction",
            "User-friendly interface for data review and corrections",
        ],
    }


if __name__ == '__main__':
    # Run the FastAPI app using `uvicorn` when running directly
    uvicorn.run(app, host="0.0.0.0", port=8000)

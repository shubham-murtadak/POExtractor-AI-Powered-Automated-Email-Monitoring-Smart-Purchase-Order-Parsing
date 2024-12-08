import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Source.email_read import read_email_from_email
import nest_asyncio
nest_asyncio.apply()


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
    """
    * method: get_project_info
    * description: FastAPI endpoint to fetch and return project-related email data by calling `read_email_from_email`.
    * return: JSON response containing parsed email data.
    *
    * who             when           version  change (include bug# if apply)
    * ----------      -----------    -------  ------------------------------
    * Shubham M      07-DEC-2024        1.0      initial creation
    *
    * Parameters
    *   None
    """

    return read_email_from_email()

if __name__ == '__main__':
    # Run the FastAPI app using `uvicorn` when running directly
    uvicorn.run(app, host="0.0.0.0", port=8000)

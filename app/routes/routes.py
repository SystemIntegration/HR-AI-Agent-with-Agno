# app/routes/routes.py
from fastapi import APIRouter,Request
from fastapi.responses import FileResponse,JSONResponse
from pydantic import BaseModel
import os
from fastapi import HTTPException
from app.agents.multi_agent_team import multi_agent_team
from app.configurations.logger import logger

router = APIRouter()


@router.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    index_path = os.path.join("./frontend/dist", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend build not found"}


class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
async def ask_question(question_request: QuestionRequest,request: Request):
    try:

        user_query = question_request.question

        # multi_agent_team.print_response(
        #     user_query, stream=True
        # )

        # This should route to the stock_searcher
        response = await multi_agent_team.arun(user_query)
        final_answer = response.content


        # Print the assistant’s response
        print("\n=== Assistant’s Response ===")
        print(final_answer)
        print("============================\n")

        return {"answer": final_answer}

    except Exception as e:
        error_message = str(e)

        # Log the actual exception
        logger.error(f"{error_message} WHICH_API = {request.url.path}", exc_info=True)
        
        if "429" in error_message or "503" in error_message or "Too Many Requests" in error_message:
            return JSONResponse(status_code=429, content={"error": "Too many requests. Please try again later"})

        if "400" in error_message or "INVALID_ARGUMENT" in error_message:
            return JSONResponse(status_code=400, content={"error": "Something went wrong. If this issue persists please contact us through our help center."})
        

        # return JSONResponse(status_code=500, content={"error": f"An error occurred: {error_message}"})
        return JSONResponse(status_code=500, content={"error": "Sorry! I’m having trouble thinking right now. My brain (AI server) might be on a short break. Let’s try again soon!"})

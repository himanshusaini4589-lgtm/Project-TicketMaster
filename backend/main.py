from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.agent import build_agent
from backend.memory import make_checkpointer, thread_config
from backend.runtime import start_turn, resume_turn

app = FastAPI(title="Ticketmaster AI Agent API")

# Shared singletons in memory
checkpointer = make_checkpointer()
agent = build_agent(checkpointer=checkpointer)

class ChatRequest(BaseModel):
    message: str
    session_id: str

class ApprovalRequest(BaseModel):
    session_id: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    config = thread_config(request.session_id)
    try:
        turn_result = start_turn(agent, request.message, config)
        
        if turn_result.pending_interrupt:
            return {
                "status": "pending_approval",
                "session_id": request.session_id,
                "interrupt_details": turn_result.pending_interrupt,
                "response": "Action requires human approval. Proceed to purchase tickets?"
            }

        return {
            "status": "ok",
            "session_id": request.session_id,
            "response": turn_result.text,
            "summary": turn_result.structured.model_dump() if turn_result.structured else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/approve")
async def approve_endpoint(request: ApprovalRequest):
    config = thread_config(request.session_id)
    decisions = [{"type": "approve"}]
    
    turn_result = resume_turn(agent, decisions, config)
    return {
        "status": "ok",
        "session_id": request.session_id,
        "response": turn_result.text
    }

@app.post("/reject")
async def reject_endpoint(request: ApprovalRequest):
    config = thread_config(request.session_id)
    decisions = [{
        "type": "reject",
        "message": "User declined booking action. Explain and ask how to assist further."
    }]
    
    turn_result = resume_turn(agent, decisions, config)
    return {
        "status": "rejected",
        "session_id": request.session_id,
        "response": turn_result.text
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
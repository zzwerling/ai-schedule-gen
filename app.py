from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware


from utils import get_fixed_tasks, get_unfixed_tasks
from scheduler import construct_prompt, get_schedule

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:5173"] for specific frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FixedTask(BaseModel):
    name: str
    time: str

class UnfixedTask(BaseModel):
    name: str
    duration: int

class ScheduleRequest(BaseModel):
    wakeTime: str
    sleepTime: str
    fixedTasks: Optional[List[FixedTask]]
    unfixedTasks: List[UnfixedTask]

@app.post("/schedule")
def generate_schedule(req: ScheduleRequest):
    prompt = construct_prompt(
        req.wakeTime,
        req.sleepTime,
        req.fixedTasks,
        req.unfixedTasks
    )
    schedule = get_schedule(prompt)
    return {"schedule": schedule}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
"""
def main():
    print("Welcome to ai-schedule-gen")
    
    wake_time = input("What time do you plan on waking up? ").strip()
    sleep_time = input("What time do you go to sleep? ").strip()
    
    print("Enter your fixed tasks one by one (e.g. '5PM Doctor'). ")
    print("Press Enter with no input when you're done. \n")
    fixed_tasks = get_fixed_tasks()
    print("Enter your unfixed tasks one by one (e.g. 'gym' or 'meditation'). ")
    print("Press Enter with no input when you're done. \n")
    unfixed_tasks = get_unfixed_tasks()
    
    prompt = construct_prompt(wake_time, sleep_time, fixed_tasks, unfixed_tasks)
    
    schedule = get_schedule(prompt)
    print("\n🗓️ Your Generated Schedule:\n")
    print(schedule)
"""    
    
   
    
    
    
    
    
    
    
   




from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def construct_prompt(wake_time, sleep_time, fixed_tasks, unfixed_tasks):
    fixed_tasks_joined = ", ".join(f"{task.name} {task.time}" for task in fixed_tasks)
    unfixed_tasks_joined = ", ".join(f"{task.name} {task.duration} min" if task.duration is not None else task.name
    for task in unfixed_tasks)   
    
    prompt = (
    f"You are helping someone build a realistic daily schedule.\n"
    f"- Wake time: {wake_time}\n"
    f"- Sleep time: {sleep_time}\n"
    f"- Fixed tasks: {fixed_tasks_joined}\n"
    f"- Unfixed tasks: {unfixed_tasks_joined}\n"
    f"Make it practical and time-efficient. Do not deviate from the fixed tasks. The time for those is non-negotiable."
    f"Add styling tags in the response using tailwind CSS to make it pretty. There should be no extra junk in it. The whole answer should be directly renderable."
)
    
    return prompt

def get_schedule(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert productivity coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        print("❌ Error calling OpenAI:", e)
        return "⚠️ Error generating schedule."
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_unfixed_tasks():
    tasks = []
    while True:
        task = input("➤ Unfixed task: ").strip()
        
        if task:
            tasks.append(task)
        
        if not task and len(tasks) > 0:
            break
        elif not task and len(tasks) == 0:
            print("You need to enter at least one unfixed task.")

    
    
    print("\n✅ Got the following tasks:")
    for i, t in enumerate(tasks, 1):
        print(f"{i}. {t}")

    amt_tasks = len(tasks)
    print(f"\nProceeding with {amt_tasks} unfixed tasks.")
    
    return tasks

def get_fixed_tasks():
    tasks = []
    while True:
        task = input("➤ Fixed task: ").strip()
        
        if not task:
            break
        
        if len(task.split()) < 2:
            print("⚠️  Please include a time and a task (e.g. '5PM Doctor'). Try again.")
            continue

        tasks.append(task)
    
    if tasks:
        print("\n✅ Got the following fixed tasks:")
        for i, t in enumerate(tasks, 1):
            print(f"{i}. {t}")
    else:
        print("\nProceeding with 0 fixed tasks.")
    
    return tasks

def construct_prompt(wake_time, sleep_time, fixed_tasks, unfixed_tasks):
    unfixed_tasks_joined = ", ".join(unfixed_tasks)
    fixed_tasks_joined = ", ".join(fixed_tasks)
    prompt = (
    f"You are helping someone build a realistic daily schedule.\n"
    f"- Wake time: {wake_time}\n"
    f"- Sleep time: {sleep_time}\n"
    f"- Fixed tasks: {fixed_tasks_joined}\n"
    f"- Unfixed tasks: {unfixed_tasks_joined}\n"
    f"Make it practical and time-efficient. Do not deviate from the fixed tasks. The time for those is non-negotiable."
)
    
    return prompt

def get_schedule(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert productivity coach."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content


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
    
    
   
    
    
    
    
    
    
    
   




if __name__ == "__main__":
    main()
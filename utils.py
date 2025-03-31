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
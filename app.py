import heapq
from datetime import datetime, timedelta

class Task:
    def __init__(self, description, deadline, priority):
        self.description = description
        self.deadline = deadline
        self.priority = priority

    def __lt__(self, other):
        # Compare based on deadline time first
        if self.deadline.time() != other.deadline.time():
            return self.deadline.time() < other.deadline.time()
        # If the deadline time is the same, use priority
        else:
            return self.priority < other.priority

class TaskScheduler:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        heapq.heappush(self.tasks, task)

    def get_next_task(self):
        if self.tasks:
            return heapq.heappop(self.tasks)
        else:
            return None

def get_task_input():
    description = input("Enter task description: ")

    # Prompt for the time only
    deadline_time_str = input("Enter task deadline time (HH:MM): ")
    deadline_time = datetime.strptime(deadline_time_str, "%H:%M").time()

    # Combine time with the current date to create the deadline
    current_date = datetime.now().date()
    deadline = datetime.combine(current_date, deadline_time)

    priority = int(input("Enter task priority (1-3, where 1 is the highest): "))

    return Task(description, deadline, priority)

def main():
    scheduler = TaskScheduler()

    while True:
        add_more_tasks = input("Do you want to add a new task? (yes/no): ").lower()
        if add_more_tasks != 'yes':
            break
        task = get_task_input()
        scheduler.add_task(task)

    print("\nTask Order:")
    while True:
        next_task = scheduler.get_next_task()
        if next_task:
            print(f"{next_task.description} - Deadline: {next_task.deadline} - Priority: {next_task.priority}")
        else:
            print("No more tasks.")
            break

if __name__ == "__main__":
    main()

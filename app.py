import heapq
from datetime import datetime, timedelta

class Task:
    def __init__(self, description, deadline, priority):
        self.description = description
        self.deadline = deadline
        self.priority = priority

    def __lt__(self, other):
        # Compare based on deadline date first (ignoring the year)
        if (self.deadline.month, self.deadline.day) != (other.deadline.month, other.deadline.day):
            return (self.deadline.month, self.deadline.day) < (other.deadline.month, other.deadline.day)
        # If the deadline date is the same, use priority
        else:
            return self.priority < other.priority

class TaskScheduler:
    def __init__(self):
        self.tasks_by_date = {}

    def add_task(self, task):
        date_key = task.deadline.date()
        if date_key not in self.tasks_by_date:
            self.tasks_by_date[date_key] = []
        heapq.heappush(self.tasks_by_date[date_key], task)

    def get_next_task(self):
        next_task = None
        min_date = min(self.tasks_by_date.keys()) if self.tasks_by_date else None
        if min_date is not None:
            next_task = heapq.heappop(self.tasks_by_date[min_date])
            if not self.tasks_by_date[min_date]:  # Remove the date entry if no tasks are left for that date
                del self.tasks_by_date[min_date]
        return next_task

    def print_tasks_by_date(self):
        for date, tasks in sorted(self.tasks_by_date.items()):
            print(f"\nTasks for {date.month}-{date.day}:")
            for task in tasks:
                print(f"{task.description} - Deadline: {task.deadline.strftime('%H:%M')} - Priority: {task.priority}")

def get_task_input():
    description = input("Enter task description: ")

    deadline_date_str = input("Enter task deadline date (MM-DD): ")
    deadline_date = datetime.strptime(deadline_date_str, "%m-%d").date()

    deadline_time_str = input("Enter task deadline time (HH:MM): ")
    deadline_time = datetime.strptime(deadline_time_str, "%H:%M").time()

    deadline = datetime.combine(deadline_date, deadline_time)

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

    scheduler.print_tasks_by_date()

if __name__ == "__main__":
    main()

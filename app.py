import heapq
from datetime import datetime
import wx
import wx.adv
import wx.lib.calendar

# Constants for task priority
LOW_PRIORITY = 1
MEDIUM_PRIORITY = 2
HIGH_PRIORITY = 3


class Task:
    """Class representing a task with description, deadline, and priority."""

    def __init__(self, description, deadline, priority):
        """Initialize a Task object."""
        self.description = description
        self.deadline = deadline
        self.priority = priority

    def __lt__(self, other):
        """Compare tasks based on deadline and priority."""
        if (self.deadline.month, self.deadline.day) != (other.deadline.month, other.deadline.day):
            return (self.deadline.month, self.deadline.day) < (other.deadline.month, other.deadline.day)
        else:
            return self.priority < other.priority


class TaskScheduler:
    """Class for managing and scheduling tasks."""

    def __init__(self):
        """Initialize a TaskScheduler object."""
        self.tasks_by_date = {}

    def add_task(self, task):
        """Add a task to the scheduler."""
        date_key = task.deadline.date()
        if date_key not in self.tasks_by_date:
            self.tasks_by_date[date_key] = []
        heapq.heappush(self.tasks_by_date[date_key], task)

    def get_next_task(self):
        """Get the next scheduled task."""
        next_task = None
        min_date = min(self.tasks_by_date.keys()) if self.tasks_by_date else None
        if min_date is not None:
            next_task = heapq.heappop(self.tasks_by_date[min_date])
            if not self.tasks_by_date[min_date]:
                del self.tasks_by_date[min_date]
        return next_task

    def print_tasks_by_date(self):
        """Print tasks grouped by date."""
        output = ""
        for date, tasks in sorted(self.tasks_by_date.items()):
            output += f"\nTasks for {date.strftime('%B %d')}:"
            for task in tasks:
                output += f"\n{task.description} - Deadline: {task.deadline.strftime('%I:%M %p')} - Priority: {task.priority}"
        return output


class TaskApp(wx.App):
    """Class for creating a wxPython app for task scheduling."""

    def __init__(self):
        """Initialize a TaskApp object."""
        super().__init__()
        self.scheduler = TaskScheduler()
        self.main_frame = wx.Frame(None, title="Task Scheduler", size=(800, 600))
        self.main_panel = wx.Panel(self.main_frame)
        self.create_widgets()
        self.main_frame.Show()

    def create_widgets(self):
        """Create widgets for the app."""
        self.description_label = wx.StaticText(self.main_panel, label="Task Description:")
        self.description_text = wx.TextCtrl(self.main_panel, style=wx.TE_MULTILINE)

        self.deadline_date_label = wx.StaticText(self.main_panel, label="Task Deadline Date:")
        self.deadline_date_picker = wx.adv.DatePickerCtrl(self.main_panel, style=wx.adv.DP_DEFAULT)

        self.deadline_time_label = wx.StaticText(self.main_panel, label="Task Deadline Time:")
        self.deadline_time_picker = wx.adv.TimePickerCtrl(self.main_panel, style=wx.adv.DP_DEFAULT)

        self.priority_label = wx.StaticText(self.main_panel, label="Task Priority (1-3):")
        self.priority_text = wx.TextCtrl(self.main_panel)

        self.add_button = wx.Button(self.main_panel, label="Add Task")
        self.add_button.Bind(wx.EVT_BUTTON, self.on_add_button)

        self.next_button = wx.Button(self.main_panel, label="Get Next Task")
        self.next_button.Bind(wx.EVT_BUTTON, self.on_next_button)

        self.list_button = wx.Button(self.main_panel, label="List All Tasks")
        self.list_button.Bind(wx.EVT_BUTTON, self.on_list_button)

        self.output_text = wx.TextCtrl(self.main_panel, style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.calendar = wx.lib.calendar.Calendar(self.main_panel, pos=(400, 35), size=(200, 180))

        self.setup_layout()

    def setup_layout(self):
        """Set up the layout of widgets."""
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer = wx.GridBagSizer(10, 10)

        grid_sizer.Add(self.description_label, pos=(0, 0), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        grid_sizer.Add(self.description_text, pos=(0, 1), span=(1, 3), flag=wx.ALL | wx.EXPAND, border=5)

        grid_sizer.Add(self.deadline_date_label, pos=(1, 0), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        grid_sizer.Add(self.deadline_date_picker, pos=(1, 1), flag=wx.ALL, border=5)

        grid_sizer.Add(self.deadline_time_label, pos=(2, 0), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        grid_sizer.Add(self.deadline_time_picker, pos=(2, 1), flag=wx.ALL, border=5)

        grid_sizer.Add(self.priority_label, pos=(3, 0), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        grid_sizer.Add(self.priority_text, pos=(3, 1), flag=wx.ALL, border=5)

        grid_sizer.Add(self.add_button, pos=(3, 2), flag=wx.ALL, border=5)
        grid_sizer.Add(self.next_button, pos=(3, 3), flag=wx.ALL, border=5)

        grid_sizer.Add(self.list_button, pos=(4, 0), flag=wx.ALL, border=5)
        grid_sizer.Add(self.output_text, pos=(4, 1), span=(4, 3), flag=wx.ALL | wx.EXPAND, border=5)

        grid_sizer.Add(self.calendar, pos=(0, 4), span=(4, 1), flag=wx.ALL, border=5)

        main_sizer.Add(grid_sizer, proportion=1, flag=wx.EXPAND)

        self.main_panel.SetSizer(main_sizer)

    def on_add_button(self, event):
        """Handle the add button click event."""
        try:
            description = self.description_text.GetValue()
            deadline_date = self.deadline_date_picker.GetValue().Format("%Y-%m-%d")
            deadline_time = self.deadline_time_picker.GetValue().Format("%H:%M")
            deadline = datetime.strptime(f"{deadline_date} {deadline_time}", "%Y-%m-%d %H:%M")
            priority = int(self.priority_text.GetValue())
            if priority not in [LOW_PRIORITY, MEDIUM_PRIORITY, HIGH_PRIORITY]:
                raise ValueError("Priority must be in the range 1-3.")
            task = Task(description, deadline, priority)
            self.scheduler.add_task(task)
            self.output_text.AppendText(f"Task added: {task.description}\n")
            self.calendar.AddSelect([deadline.day], 'red', 'white')
            self.calendar.Refresh()
        except ValueError as e:
            self.output_text.AppendText(f"Error: {e}. Please enter valid input.\n")

    def on_next_button(self, event):
        """Handle the next button click event."""
        next_task = self.scheduler.get_next_task()
        if next_task is not None:
            self.output_text.AppendText(
                f"Next task: {next_task.description} - Deadline: {next_task.deadline.strftime('%I:%M %p')} - Priority: {next_task.priority}\n")
        else:
            self.output_text.AppendText("No more tasks.\n")

    def on_list_button(self, event):
        """Handle the list button click event."""
        self.output_text.Clear()
        output = self.scheduler.print_tasks_by_date()
        self.output_text.AppendText(output)


def main():
    """Main function to run the wxPython app."""
    app = TaskApp()
    app.MainLoop()


if __name__ == "__main__":
    main()

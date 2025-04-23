#!/usr/bin/env python3
"""
AD_DEV_ChronCLI - A terminal-based calendar and task scheduler
"""

import curses
import datetime
import os
import json
import sys
import time
from curses import panel

# Constants
CONFIG_DIR = os.path.expanduser("~/.ad_dev_chroncli")
DATA_FILE = os.path.join(CONFIG_DIR, "tasks.json")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
VERSION = "1.0.0"

ASCII_BANNER = """
                                                                                                   
                                      .                                                             
                                       =                                                            
                                        :                                                           
                                        =                                                           
                                         -                                                          
                                         #                                                          
                                         #                                                          
                                         -                                                          
                                       #                                                            
                                     **                                                             
                                    #                                                               
                                   #                                                                
                                 . %                                                                
                                 - #                                                                
            .                    : #                                                                
             -----.               .                                                                 
         @@########@@-=-          #                                                                 
       #-            .##@--: .     #                                                                
     #:   @@@@@@@     @:.+*@ -  .   #      @@@@@ @@@@@@@*       @@@@@@@@@@+@@@@@:    @@@@@@         
  . #    @@@@@@@@     @@@@@@+#@ -    #.   @@@@@* @@@@@@@@@@@    @@@@@@@@@@@ @@@@@    @@@@@          
    #    @@@@@@@@     @@@@@@@@@ @ --  #@  @@@@@  @@@@@@@@@@@@   @@@@@@@@@@@ @@@@@    @@@@@          
   =     @@@@@@@@.    @@@@@   @@@-#@ - =# @@@@@  @@@@@   @@@@@  @@@@@       @@@@@    @@@@@          
   # .   @@@@@@@@@    @@@@@   @@@@@ #@ -- #@@@*  @@@@@   @@@@@  @@@@@       @@@@@    @@@@+          
   # .  @@@@@-@@@@    @@@@@   @@@@@   #@#-: @@   @@@@@   @@@@@  @@@@@        @@@@   .@@@@           
   .    @@@@@ @@@@    @@@@@   @@@@@      @@ -    @@@@@   @@@@@  @@@@@        @@@@@  @@@@@           
    *   @@@@@ @@@@=   @   #=* @@@@@    @#@-#@ -  @@@@@   @@@@@  @@@@@        @@@@@  @@@@@           
        @@@@@ @@@@@   @@@@@   @ @@@  @# @@@@@#@*:  @@@   @@@@@  @@@@@@@@@@   @@@@@  @@@@@ .         
        @@@@. @@@@@   @@@@@   @@=  @%   @@@@@  #@@ : @   @@@@@  @@@@@@@@@@ . @@@:+                  
       @@@@@  @@@@@   @@@@@   @  @@     @@@@%    ##@ -   @@@@@  @@@@@:...#   +  *#:*@@%@*#@@-       
       @@@@@  @@@@@   @@@@@    =@#@ *  @@@@@     @@@#@ :-             *#* .-. @@@@ .@@@@    #@-     
       @@@@@   @@@@@  @@@@@   @#@@@  # @@@@@          #@@ - %@@@@@@@@=---     @@@@ @@@@@      #     
       @@@@@@@@@@@@@  @@@@@  @@@@@@      @@     @@@##@   #@  -  @@@@@ *#@@--  @@@@ @@@@         @ . 
      @@@@@@@@@@@@@@  @@@@  @ @@@@@   @@    @@@% @@@@@   @@*#@  -  @@     # .  @@@ @@@@     .  @@ . 
      @@@@@@@@@@@@@@  @@@@ #@ @@@@@      @@@.    @@@@@   @@@@@-#@-  -  .    @  @@@@@@@@  .    @#    
      @@@@@    @@@@@  @@@@.  :@@@    :@##@+  #@@ @@@@@@@@@@@@#  @##%@..:--  .  =           @@#      
      @@@@@    @@@@@@ @@@@@*@    %@@#%@@@@     . **     +@@@#   @@@@@.*#@@@@@#-.  .@@@@@%##         
     =@@@@@     @@@@@ @@@@@@@@%##:   @@@@@       @@@@@####*=*@@+.  .@@@##@@ =##%@@@@@@   .          
                                     @@@@@                  ..:-=-:                                 
                                    @@@@@                                                           
                                                                                                    
"""

class Task:
    """Task object representing a scheduled task"""
    
    def __init__(self, name, start_time, end_time=None, completed=False):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.completed = completed
        
    def to_dict(self):
        """Convert task to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "completed": self.completed
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create task from dictionary"""
        return cls(
            name=data["name"],
            start_time=datetime.datetime.fromisoformat(data["start_time"]),
            end_time=datetime.datetime.fromisoformat(data["end_time"]) if data["end_time"] else None,
            completed=data["completed"]
        )


class TaskManager:
    """Manages task data and persistence"""
    
    def __init__(self):
        self.tasks = []
        self.load_tasks()
        
    def add_task(self, task):
        """Add a new task and save"""
        self.tasks.append(task)
        self.sort_tasks()
        self.save_tasks()
        
    def delete_task(self, task_index):
        """Delete a task by index"""
        if 0 <= task_index < len(self.tasks):
            del self.tasks[task_index]
            self.save_tasks()
            return True
        return False
    
    def toggle_task_completion(self, task_index):
        """Toggle task completion status"""
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].completed = not self.tasks[task_index].completed
            self.save_tasks()
            return True
        return False
    
    def sort_tasks(self):
        """Sort tasks by start time"""
        self.tasks.sort(key=lambda x: x.start_time)
    
    def get_tasks_for_date(self, date):
        """Get all tasks for a specific date"""
        return [task for task in self.tasks if task.start_time.date() == date]
        
    def save_tasks(self):
        """Save tasks to JSON file"""
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)
            
        with open(DATA_FILE, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f)
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    tasks_data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in tasks_data]
                    self.sort_tasks()
            except (json.JSONDecodeError, KeyError):
                self.tasks = []
                print("Error loading tasks, starting with empty task list")


class CalendarView:
    """Calendar visualization component"""
    
    def __init__(self, window, task_manager):
        self.window = window
        self.task_manager = task_manager
        self.current_date = datetime.date.today()
        self.panel = panel.new_panel(window)
        
    def draw(self):
        """Draw the calendar view"""
        self.window.clear()
        height, width = self.window.getmaxyx()
        
        # Draw calendar header
        month_year = self.current_date.strftime("%B %Y")
        self.window.addstr(1, (width - len(month_year)) // 2, month_year, curses.A_BOLD)
        
        # Draw weekday headers
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        day_width = width // 7
        
        for i, day in enumerate(weekdays):
            x = i * day_width + (day_width - len(day)) // 2
            self.window.addstr(3, x, day)
        
        # Calculate first day of month and number of days
        first_day = datetime.date(self.current_date.year, self.current_date.month, 1)
        last_day = (datetime.date(self.current_date.year, self.current_date.month % 12 + 1, 1) 
                    if self.current_date.month < 12 
                    else datetime.date(self.current_date.year + 1, 1, 1)) - datetime.timedelta(days=1)
        
        # Calculate offset (0 = Monday, 6 = Sunday)
        offset = first_day.weekday()
        
        # Draw days
        day = 1
        for week in range(6):  # Max 6 weeks in a month
            for weekday in range(7):
                x = weekday * day_width + 2
                y = week * 3 + 5
                
                if (week == 0 and weekday < offset) or day > last_day.day:
                    # Empty cell
                    pass
                else:
                    # Draw day number
                    day_str = str(day)
                    if day == self.current_date.day and self.current_date.month == datetime.date.today().month:
                        self.window.addstr(y, x, day_str, curses.A_REVERSE)
                    else:
                        self.window.addstr(y, x, day_str)
                    
                    # Check for tasks on this day
                    day_date = datetime.date(self.current_date.year, self.current_date.month, day)
                    day_tasks = self.task_manager.get_tasks_for_date(day_date)
                    
                    if day_tasks:
                        task_indicator = f"[{len(day_tasks)}]"
                        self.window.addstr(y, x + len(day_str) + 1, task_indicator, 
                                          curses.A_BOLD if len(day_tasks) > 0 else 0)
                    
                    day += 1
        
        # Draw navigation instructions
        nav_text = "< Prev [p] | Next [n] >"
        self.window.addstr(height - 2, (width - len(nav_text)) // 2, nav_text)
        
        self.window.box()
        self.window.refresh()
    
    def next_month(self):
        """Move to next month"""
        if self.current_date.month == 12:
            self.current_date = datetime.date(self.current_date.year + 1, 1, self.current_date.day)
        else:
            self.current_date = datetime.date(self.current_date.year, self.current_date.month + 1, 
                                             min(self.current_date.day, 
                                                 self._days_in_month(self.current_date.year, self.current_date.month + 1)))
        self.draw()
    
    def prev_month(self):
        """Move to previous month"""
        if self.current_date.month == 1:
            self.current_date = datetime.date(self.current_date.year - 1, 12, self.current_date.day)
        else:
            self.current_date = datetime.date(self.current_date.year, self.current_date.month - 1, 
                                             min(self.current_date.day, 
                                                 self._days_in_month(self.current_date.year, self.current_date.month - 1)))
        self.draw()
    
    def _days_in_month(self, year, month):
        """Helper method to get the number of days in a month"""
        if month == 12:
            return 31
        return (datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)).day


class TaskListView:
    """Task list and task entry component"""
    
    def __init__(self, window, task_manager):
        self.window = window
        self.task_manager = task_manager
        self.panel = panel.new_panel(window)
        self.selected_index = 0
        self.offset = 0  # For scrolling
        self.mode = "list"  # "list" or "entry"
        
        # Task entry fields
        self.task_name = ""
        self.task_date = datetime.date.today().strftime("%Y-%m-%d")
        self.task_time = datetime.datetime.now().strftime("%H:%M")
        self.end_time = ""
        self.entry_field = 0  # 0: name, 1: date, 2: time, 3: end time
        
    def draw(self):
        """Draw the task list view"""
        self.window.clear()
        height, width = self.window.getmaxyx()
        
        # Draw header
        header = "Task List"
        self.window.addstr(1, (width - len(header)) // 2, header, curses.A_BOLD)
        
        # Draw tasks
        if self.mode == "list":
            tasks_per_page = height - 10
            
            if self.task_manager.tasks:
                for i in range(min(tasks_per_page, len(self.task_manager.tasks) - self.offset)):
                    task_idx = i + self.offset
                    task = self.task_manager.tasks[task_idx]
                    
                    # Format task display
                    checkbox = "[X]" if task.completed else "[ ]"
                    date_str = task.start_time.strftime("%Y-%m-%d")
                    time_str = task.start_time.strftime("%H:%M")
                    
                    # Truncate task name if needed
                    max_name_len = width - 25
                    task_name = task.name[:max_name_len] + "..." if len(task.name) > max_name_len else task.name
                    
                    task_display = f"{checkbox} {date_str} {time_str} {task_name}"
                    
                    # Highlight selected task
                    attr = curses.A_REVERSE if task_idx == self.selected_index else 0
                    self.window.addstr(3 + i, 2, task_display, attr)
            else:
                self.window.addstr(3, 2, "No tasks. Press 'a' to add a task.")
            
            # Draw controls
            controls = "[a]dd | [d]elete | [Space] toggle | [↑/↓] navigate"
            self.window.addstr(height - 6, (width - len(controls)) // 2, controls)
            
        # Draw task entry form
        elif self.mode == "entry":
            self.window.addstr(3, 2, "Task Name:")
            self.window.addstr(4, 4, self.task_name)
            
            self.window.addstr(6, 2, "Date (YYYY-MM-DD):")
            self.window.addstr(7, 4, self.task_date)
            
            self.window.addstr(9, 2, "Time (HH:MM):")
            self.window.addstr(10, 4, self.task_time)
            
            self.window.addstr(12, 2, "End Time (HH:MM, optional):")
            self.window.addstr(13, 4, self.end_time)
            
            # Highlight current field
            y_positions = [4, 7, 10, 13]
            self.window.addstr(y_positions[self.entry_field], 2, ">")
            
            # Draw controls
            controls = "[Enter] next field | [Esc] cancel | [Tab] save"
            self.window.addstr(height - 6, (width - len(controls)) // 2, controls)
        
        self.window.box()
        self.window.refresh()
    
    def handle_key(self, key):
        """Handle key presses"""
        if self.mode == "list":
            return self._handle_list_key(key)
        elif self.mode == "entry":
            return self._handle_entry_key(key)
    
    def _handle_list_key(self, key):
        """Handle keys in list mode"""
        if key == ord('a'):
            self.mode = "entry"
            self.task_name = ""
            self.task_date = datetime.date.today().strftime("%Y-%m-%d")
            self.task_time = datetime.datetime.now().strftime("%H:%M")
            self.end_time = ""
            self.entry_field = 0
            self.draw()
            return True
        
        elif key == ord('d'):
            if self.task_manager.tasks:
                self.task_manager.delete_task(self.selected_index)
                if self.selected_index >= len(self.task_manager.tasks) and self.selected_index > 0:
                    self.selected_index -= 1
                self.draw()
            return True
        
        elif key == ord(' '):
            if self.task_manager.tasks:
                self.task_manager.toggle_task_completion(self.selected_index)
                self.draw()
            return True
        
        elif key == curses.KEY_UP:
            if self.task_manager.tasks and self.selected_index > 0:
                self.selected_index -= 1
                # Adjust offset for scrolling
                if self.selected_index < self.offset:
                    self.offset = self.selected_index
                self.draw()
            return True
        
        elif key == curses.KEY_DOWN:
            if self.task_manager.tasks and self.selected_index < len(self.task_manager.tasks) - 1:
                self.selected_index += 1
                # Adjust offset for scrolling
                height = self.window.getmaxyx()[0]
                if self.selected_index >= self.offset + (height - 10):
                    self.offset += 1
                self.draw()
            return True
        
        return False
    
    def _handle_entry_key(self, key):
        """Handle keys in entry mode"""
        height, width = self.window.getmaxyx()
        
        if key == 27:  # Escape
            self.mode = "list"
            self.draw()
            return True
        
        elif key == 9:  # Tab - save task
            try:
                # Validate date and time
                start_datetime = datetime.datetime.strptime(f"{self.task_date} {self.task_time}", "%Y-%m-%d %H:%M")
                end_datetime = None
                
                if self.end_time:
                    end_datetime = datetime.datetime.strptime(f"{self.task_date} {self.end_time}", "%Y-%m-%d %H:%M")
                    if end_datetime <= start_datetime:
                        self.window.addstr(height - 4, 2, "Error: End time must be after start time", curses.A_BOLD)
                        self.window.refresh()
                        time.sleep(2)
                        return True
                
                # Create and save task
                task = Task(self.task_name, start_datetime, end_datetime)
                self.task_manager.add_task(task)
                
                # Reset and go back to list mode
                self.mode = "list"
                self.draw()
                
            except ValueError:
                self.window.addstr(height - 4, 2, "Error: Invalid date or time format", curses.A_BOLD)
                self.window.refresh()
                time.sleep(2)
                
            return True
        
        elif key == 10:  # Enter - move to next field
            self.entry_field = (self.entry_field + 1) % 4
            self.draw()
            return True
        
        elif key == curses.KEY_BACKSPACE or key == 127:  # Handle backspace
            if self.entry_field == 0 and self.task_name:
                self.task_name = self.task_name[:-1]
            elif self.entry_field == 1 and self.task_date:
                self.task_date = self.task_date[:-1]
            elif self.entry_field == 2 and self.task_time:
                self.task_time = self.task_time[:-1]
            elif self.entry_field == 3 and self.end_time:
                self.end_time = self.end_time[:-1]
            self.draw()
            return True
        
        # Handle typing
        if 32 <= key <= 126:  # Printable characters
            char = chr(key)
            if self.entry_field == 0:
                self.task_name += char
            elif self.entry_field == 1:
                self.task_date += char
            elif self.entry_field == 2:
                self.task_time += char
            elif self.entry_field == 3:
                self.end_time += char
            self.draw()
            return True
        
        return False


class ChronCLI:
    """Main application class"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.task_manager = TaskManager()
        
        # Initialize colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        
        # Hide cursor
        curses.curs_set(0)
        
        # Create windows
        height, width = stdscr.getmaxyx()
        
        # Split screen horizontally
        task_list_height = height
        task_list_width = width // 2
        calendar_height = height
        calendar_width = width - task_list_width
        
        # Create windows
        self.task_list_win = curses.newwin(task_list_height, task_list_width, 0, 0)
        self.calendar_win = curses.newwin(calendar_height, calendar_width, 0, task_list_width)
        
        # Create views
        self.task_list_view = TaskListView(self.task_list_win, self.task_manager)
        self.calendar_view = CalendarView(self.calendar_win, self.task_manager)
        
    def draw_banner(self):
        """Draw the AD DEV banner"""
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        
        # Display banner
        banner_lines = ASCII_BANNER.strip().split('\n')
        for i, line in enumerate(banner_lines):
            if i < height:
                self.stdscr.addstr(i, max(0, (width - len(line)) // 2), line)
        
        self.stdscr.refresh()
        time.sleep(1.5)  # Show banner for 1.5 seconds
    
    def run(self):
        """Run the main application loop"""
        self.draw_banner()
        
        # Draw initial views
        self.task_list_view.draw()
        self.calendar_view.draw()
        
        # Main event loop
        while True:
            key = self.stdscr.getch()
            
            # Global quit
            if key == ord('q'):
                break
            
            # Task list handling
            if self.task_list_view.handle_key(key):
                self.calendar_view.draw()  # Refresh calendar if task list changes
                continue
            
            # Calendar navigation
            if key == ord('p'):  # Previous month
                self.calendar_view.prev_month()
            elif key == ord('n'):  # Next month
                self.calendar_view.next_month()


def main():
    """Entry point"""
    # Create config directory if it doesn't exist
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    
    # Run the application
    curses.wrapper(lambda stdscr: ChronCLI(stdscr).run())


if __name__ == "__main__":
    main()

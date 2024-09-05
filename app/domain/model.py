from __future__ import annotations
from datetime import datetime, timedelta, time
from enum import Enum
from dataclasses import dataclass, field


class TaskStatus(Enum):
    ASSIGNET = 0
    IN_PROGRESS = 1
    PAUSED = 2
    COMPLITED = 3

# @dataclass
# class TaskTimeData:
#     date_of_finish: datetime
#     planned_time_to_finish: datetime = field(default=date_of_finish)
#     time_of_creation: datetime = field(default_factory=datetime.now)
#     actual_time_to_finish: datetime = field(default=None)


class Task:
    def __init__(
            self,
            task_name: str,
            workers: str,
            finish_date: datetime,
            task_description: str = ' ',
            parent_task: Task = None,
            task_status: TaskStatus = TaskStatus.ASSIGNET
            ):
        self._time_of_creation = datetime.now()
        self._task_id = 0  #func for gen uuid
        self.task_name = task_name
        self.workers = workers
        self.task_description = task_description
        self.task_status = task_status
        self.parent_task = parent_task
        self.finish_date = finish_date
        self._planned_time_to_finish = finish_date - self._time_of_creation
        self._actual_time_to_finish = None
        self._child_tasks = []

    def add_subtask(self, subtask: Task):
        self._child_tasks.append(subtask)
        subtask.parent_task = self
        self._update_planned_ttf()

    def delete_subtask(self, subtask: Task):
        self._child_tasks.remove(subtask)
        subtask.parent_task = None
        self._update_planned_ttf()

    def update_task(self, new_task: Task):
        self.task_name = new_task.task_name
        self.workers = new_task.workers
        self.task_description = new_task.task_description
        self.task_status = new_task.task_status
        self.finish_date = new_task.finish_date

    def get_planned_ttf(self):
        return self._planned_time_to_finish

    def _update_planned_ttf(self):
        cur_task = self
        while cur_task:
            new_ttf = None
            if cur_task._child_tasks:
                for task in cur_task._child_tasks:
                    if new_ttf:
                        new_ttf += task._planned_time_to_finish
                    else:
                        new_ttf = task._planned_time_to_finish
                cur_task._planned_time_to_finish = new_ttf
            else:
                cur_task._planned_time_to_finish = cur_task.finish_date - \
                                                cur_task._time_of_creation
            cur_task = cur_task.parent_task

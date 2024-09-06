from __future__ import annotations
from datetime import datetime, timedelta, time
from enum import Enum
from dataclasses import dataclass, field
from queue import Queue


class TaskStatus(Enum):
    ASSIGNMENT = 0
    IN_PROGRESS = 1
    PAUSED = 2
    COMPLITED = 3


class Error(Exception):
    pass

# @dataclass
# class TaskTimeData:
#     date_of_finish: datetime
#     planned_time_to_finish: datetime = field(default=date_of_finish)
#     time_of_creation: datetime = field(default_factory=datetime.now)
#     actual_time_to_finish: datetime = field(default=None)


class Task:
    def __init__(
            self,
            name: str,
            workers: str,
            finish_date: datetime,
            description: str = ' ',
            parent_task: Task = None,
            status: TaskStatus = TaskStatus.ASSIGNMENT
            ):
        self._time_of_creation = datetime.now()
        #self._task_id = 0  #func for gen uuid
        self.name = name
        self.workers = workers
        self.description = description
        self.status = status
        self.parent_task = parent_task
        self.finish_date = finish_date
        self._planned_time_to_finish = finish_date - self._time_of_creation
        self._actual_time_to_finish = None
        self._child_tasks = []

    def add_subtask(self, subtask: Task):
        '''
        Simple realization of adding subtask
        '''
        self._child_tasks.append(subtask)
        subtask.parent_task = self
        self._update_planned_ttf()

    def delete_task(self):
        '''
        Realization of delete task
        With cheking if task terminated
        '''
        if not self._child_tasks:
            p_task = self.parent_task
            p_task._child_tasks.remove(self)
        else:
            raise Error('This task has subtusks')

    def update_task(self, new_task: Task) -> bool:
        '''
        Update task data with cheking: is
        change task status needed and possible
        '''
        try:
            if self.status != new_task.status:
                self._change_status(new_task.status)
            self.name = new_task.name
            self.workers = new_task.workers
            self.description = new_task.description
            self.finish_date = new_task.finish_date
            return 0
        except Error:
            return 1

    def get_planned_ttf(self):
        return self._planned_time_to_finish

    def _update_planned_ttf(self):
        '''
        Private func with realization of auto changing
        _planned_time_to_finish attr iteration while moving to the head of
        the tree
        '''
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

    def _change_status(self, new_status: TaskStatus):
        '''
        Private func with realization of changing status logic
        '''
        if new_status == TaskStatus.COMPLITED:
            if self._change_status_if_subtasks_can_be_complited():
                self._actual_time_to_finish = self._planned_time_to_finish - \
                                                self._time_of_creation
            else:
                raise Error("Can't change status of task on Complited")
        elif new_status == TaskStatus.PAUSED:
            if self.status != TaskStatus.IN_PROGRESS:
                raise Error("Can't change status on Paused")
            self.status = new_status
        else:
            self.status = new_status

    def _change_status_if_subtasks_can_be_complited(self) -> bool:
        '''
        Private func to check if the task can be completed
        and if so, chaged task and all its subtasks status
        to Complited
        '''
        que = Queue()
        to_change = []
        que.put(self)

        while not que.empty():
            cur_task = que.get()
            if cur_task.status == TaskStatus.ASSIGNMENT:
                return False
            to_change.append(cur_task)
            for task in cur_task._child_tasks:
                que.put(task)

        for task in to_change:
            task.status = TaskStatus.COMPLITED

        return True
import sys
import os
sys.path.append(os.path.join(sys.path[0], '../../'))
from app.domain.model import TaskStatus, Task
from datetime import datetime
import pytest


def test_add_subtask_to_task():
    task = Task('test', 'Julia', datetime(2024, 9, 20))
    sub_task = Task('test2', 'Mark', datetime(2024, 9, 21))

    task.add_subtask(sub_task)

    assert len(task._child_tasks) == 1
    assert sub_task.parent_task == task


def test_task_delete():
    task = Task('test', 'Julia', datetime(2024, 9, 20))
    sub_task = Task('test2', 'Mark', datetime(2024, 9, 21))

    task.add_subtask(sub_task)
    assert len(task._child_tasks) == 1

    sub_task.delete_task()

    assert len(task._child_tasks) == 0


def test_task_update():
    task = Task('test', 'Julia', datetime(2024, 9, 20))
    new_task = Task('test2', 'Julia2', datetime(2024, 9, 21),
                    description='new task',
                    status=TaskStatus.IN_PROGRESS)
    task.update_task(new_task)

    assert task.name == new_task.name
    assert task.workers == new_task.workers
    assert task.finish_date == new_task.finish_date
    assert task.description == new_task.description
    assert task.status == new_task.status


def test_auto_calculated_planed_time_to_finish_by_the_time_of_subtasks():
    task = Task('test1', 'Julia1', datetime(2024, 9, 5))
    sub_task1 = Task('test2', 'Julia2', datetime(2024, 9, 20))
    sub_task2 = Task('test3', 'Julia3', datetime(2024, 9, 10))
    sub_task3 = Task('test4', 'Julia4', datetime(2024, 9, 5))
    sub_task4 = Task('test5', 'Julia5', datetime(2024, 9, 26))

    task.add_subtask(sub_task1)
    task.add_subtask(sub_task2)
    sub_task1.add_subtask(sub_task3)
    sub_task1.add_subtask(sub_task4)

    assert task.get_planned_ttf() == sub_task1.get_planned_ttf() + \
                                        sub_task2.get_planned_ttf()
    assert sub_task1.get_planned_ttf() == sub_task3.get_planned_ttf() + \
                                            sub_task4.get_planned_ttf()

# def test_auto_calculated_planed_time_to_finish_by_the_time_of_subtasks():
#     task = Task()
#     sub_task1 = Task()
#     sub_task2 = Task()

#     task.add_subtask(sub_task1)
#     task.add_subtask(sub_task2)
    
#     assert task.get_planed_ttf() ==  sub_task1.get_palned_ttf() + sub_task2.get_planed_ttf()
 
# def test_auto_calculated_actual_time_to_finish_by_the_time_of_subtasks():
#     pass

# def test_show_all_tasks():
#     pass

# def test_task_change_status_complited_only_after_in_progress():
#     pass

# def test_task_status_change_to_finish_also_finished_subtusk():
#     pass


if __name__ == '__main__':
    test_add_subtask_to_task()
    # test_delete_subtask_form_task()
    test_task_delete()
    test_task_update()
    test_auto_calculated_planed_time_to_finish_by_the_time_of_subtasks()

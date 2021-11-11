# from controller import *
# from models import *
from mongodblab3 import MongoDB
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk

# створення графічного інтерфейсу адмінки CRUD
root = Tk()
mainf = Frame()
mainf.pack(side=TOP, padx=10)
f = Frame(mainf)
f.pack(side=LEFT, padx=10)
db = MongoDB()

# таблиця в яку будуть виводитися результати запитів до таблиці tasks

entryname = Entry(f)
entryid = Entry(f)
entrystat = Entry(f)
Label(f, text='Enter new task name:').grid(row=2, column=0, columnspan=2)
entryname.grid(row=3, column=0)
Label(f, text='Enter new task employee id:').grid(row=4, column=0, columnspan=2)
entryid.grid(row=5, column=0)
Label(f, text='Enter new task status:').grid(row=6, column=0, columnspan=2)
entrystat.grid(row=7, column=0)

Button(f, text="Add", command=lambda: db.add_employee(entryid.get(), entryname.get(), entrystat.get())).grid(row=8,
                                                                                                             column=0)

f6 = Frame(mainf)
f6.pack(side=LEFT, padx=10)
tasks_id1 = Entry(f6)
team_id1 = Entry(f6)
Label(f6, text='Enter new team id').grid(row=2, column=0, columnspan=2)
team_id1.grid(row=3, column=0)
Label(f6, text="Enter task id's").grid(row=4, column=0, columnspan=2)
tasks_id1.grid(row=5, column=0)

Button(f6, text="ADD", command=lambda: db.add_team(team_id1.get(), tasks_id1.get())).grid(row=6, column=0)  #

f2 = Frame(mainf)
f2.pack(side=LEFT, padx=10)
taskid = Entry(f2)
new_status = Entry(f2)
Label(f2, text='Enter task id to update status:').grid(row=2, column=0, columnspan=2)
taskid.grid(row=3, column=0)
Label(f2, text='Enter new status:').grid(row=4, column=0, columnspan=2)
new_status.grid(row=5, column=0)

Button(f2, text="refresh", command=lambda: db.edit_task(taskid.get(), new_status.get())).grid(row=6, column=0)

f3 = Frame(mainf)
f3.pack(side=LEFT, padx=10)
team_id = Entry(f3)
Label(f3, text='Enter team id to Delete team:').grid(row=2, column=0, columnspan=2)
team_id.grid(row=3, column=0)

Button(f3, text="Delete", command=lambda: db.delete_team_by_id(team_id.get())).grid(row=6, column=0)  #

f4 = Frame(mainf)
f4.pack(side=LEFT, padx=10)
taskidel = Entry(f4)
Label(f4, text='Enter task id to delete task:').grid(row=2, column=0, columnspan=2)
taskidel.grid(row=3, column=0)

Button(f4, text="Delete", command=lambda: db.delete_task_by_id(taskidel.get())).grid(row=6, column=0)  #

f5 = Frame()
f5.pack(side=TOP, pady=20)
Button(f5, text="Refresh table", command=lambda: add_()).grid(row=6, column=0)


def item_selected(event):
    for selected_item in table_task.selection():
        table_task.delete(selected_item)


columns = ('#1', '#2', '#3')
table_task = ttk.Treeview(show="headings", columns=columns)
table_task.heading("#1", text="TaskId")
table_task.heading("#2", text="TaskName")
table_task.heading("#3", text="Task status")
table_task.pack(side=LEFT, pady=10)
table_task.bind('<<TreeviewSelect>>', item_selected)

table_teams = ttk.Treeview(show="headings", columns=columns)
table_teams.heading("#1", text="Team id")
table_teams.heading("#2", text="Team task id's")
table_teams.heading("#3", text="Team status")
table_teams.pack(side=LEFT, pady=10)


def add_():
    table_task.delete(*table_task.get_children())
    table_teams.delete(*table_teams.get_children())
    ls_task = list(db.collection_tasks.aggregate([{"$group": {"_id": ["$id", "$Task", "$status"]}}]))
    ls_team = list(db.collection_teams.aggregate([{"$group": {"_id": ["$id", "$Team_squad", "$status"]}}]))
    ls_task.sort(key=lambda i: int(i['_id'][0]))
    ls_team.sort(key=lambda i: int(i['_id'][0]))

    for i in ls_task:
        task = (i['_id'][0], i['_id'][1], i['_id'][2])
        table_task.insert('', tk.END, values=task)
    for i in ls_team:
        task = (i['_id'][0], str(i['_id'][1]), db.refresh_team_status(i['_id'][0]))
        table_teams.insert('', tk.END, values=task)


add_()
root.mainloop()

from sqlalchemy import Table, select, insert, update, delete, create_engine, MetaData, Integer, String, Column, ForeignKey
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy.sql.schema import ForeignKey, MetaData

from tkinter import *
import tkinter.ttk as ttk
import json


# створює базу даних  postgree_db
def create_postgre_db():
    conn = psycopg2.connect(
        user="postgres",
        password="1111",
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute('create database postgree_db')
    cursor.close()
    conn.close()

# створює зєднання з базами даних sqlite i postgresql, якщо цих баз не існує то створює ці бази


def connect_to_dbs():
    try:
        pgengine = create_engine(
            "postgresql+psycopg2://postgres:1111@localhost/postgree_db")
        pgcon = pgengine.connect()
    except:
        create_postgre_db()
        pgengine = create_engine(
            "postgresql+psycopg2://postgres:1111@localhost/postgree_db")
        pgcon = pgengine.connect()
    litengine = create_engine('sqlite:///sqlite3.db')
    litecon = litengine.connect()
    return pgengine, pgcon, litengine, litecon


# створює таблиці в обох базах даних та їх представлення
def create_table(pgengine, pgcon, litengine, litecon, metadata):
    departament = Table('departament', metadata,
                        Column('departamentid',  Integer(
                        ), autoincrement=True, primary_key=True),
                        Column(
                            'name',  String(200)),
                        Column('responsible_for',
                               String(100))
                        )

    employee = Table('employee', metadata,
                     Column('employeeid',  Integer(
                     ), autoincrement=True, primary_key=True),
                     Column('name',  String(200)),
                     Column(
                         'position',  String(200)),
                     Column('departamentid',  Integer(
                     ), ForeignKey("departament.departamentid"))
                     )

    tasks = Table('tasks', metadata,
                  Column('taskid', Integer(
                  ), autoincrement=True, primary_key=True),
                  Column(
                      'taskname',  String(200)),
                  Column(
                      'status',  String(200)),
                  Column('employeeid',  Integer(
                  ), ForeignKey("employee.employeeid"))
                  )
    metadata.drop_all(pgengine)
    metadata.create_all(litengine)
    metadata.drop_all(pgengine)
    metadata.create_all(pgengine)
    return departament, employee, tasks


# вставляє нового працівника в таблицю employee
def employee_insert(con, employee, entities):
    empl = employee.insert().values(
        name=entities[0], position=entities[1], departamentid=entities[2])
    con.execute(empl)

# вставлення нового департаменту


def depart_insert(con, departament, entities):
    empl = departament.insert().values(
        name=entities[0], responsible_for=entities[1])
    con.execute(empl)

# вставлення нового завдання і виклик функції tasks_fetch для показу оновленої таблиці в графічному інтерфейсі


def task_insert(con, tasks, table, entryname, entryid, entrystat):
    empl = tasks.insert().values(taskname=entryname.get(),
                                 employeeid=entryid.get(), status=entrystat.get())
    con.execute(empl)
    tasks_fetch(con, tasks, table)

# оновлення статусу завдання по ід і виклик функції tasks_fetch для показу оновленої таблиці в графічному інтерфейсі


def task_status_update(con, tasks, table, taskid, new_value=None):
    print(taskid)
    if int(taskid) == -1:
        u = update(tasks).where(True).values(status="done")
    else:
        u = update(tasks).where(tasks.c.taskid ==
                                taskid).values(status=new_value)
        con.execute(u)
    tasks_fetch(con, tasks, table)

# вивід всієї таблиці tasks в графічний інтерфейс якщо не вказаний ід або конкретного записа якщо вказаний ід


def tasks_fetch(con, tasks, table, id=None):
    # очищаємо таблицю графічного інтерфейса
    for i in table.get_children():
        table.delete(i)
    if not id:
        s = select([tasks])
    else:
        s = select([tasks]).where(tasks.c.taskid == id)
    r = con.execute(s)
    rows = r.fetchall()
    for row in rows:
        print(row)
        table.insert("", END, values=list(row))

# видалення завдання по ід і виклик функції tasks_fetch для показу оновленої таблиці в графічному інтерфейсі


def tasks_delete(con, tasks, table, taskid):
    con.execute(delete(tasks).where(tasks.c.taskid == taskid))
    tasks_fetch(con, tasks, table)

# експорт в базу даних postgreesql з бази даних sqlite


def export_to_db2(litecon, pgcon, departament, employee, tasks, table):
    pgcon.execute(delete(tasks))
    task_s = select([tasks])
    r = litecon.execute(task_s)
    tasksrows = r.fetchall()
    employee_s = select([employee])
    r = litecon.execute(employee_s)
    employeerows = r.fetchall()
    departament_s = select([departament])
    r = litecon.execute(departament_s)
    departamentrows = r.fetchall()
    for i in departamentrows:
        pgcon.execute(departament.insert().values(
            name=i[1], responsible_for=i[2]))
    for j in employeerows:
        pgcon.execute(employee.insert().values(
            name=j[1], position=j[2], departamentid=j[3]))
    for k in tasksrows:
        pgcon.execute(tasks.insert().values(
            taskname=k[1], employeeid=k[3], status=k[2]))
    print('success export to db2')
    pgcon.execute(update(tasks).where(True).values(status="done"))
    tasks_fetch(pgcon, tasks, table)
    a = pgcon.execute(select([tasks]))
    print(a.fetchall())


# Запис даних з postgreesql в json
def write_json(pgcon, tasks, departament, employee):
    task_s = select([tasks])
    r = pgcon.execute(task_s)
    tasksrows = r.fetchall()
    employee_s = select([employee])
    r = pgcon.execute(employee_s)
    employeerows = r.fetchall()
    departament_s = select([departament])
    r = pgcon.execute(departament_s)
    departamentrows = r.fetchall()
    tasks_data = {}
    for i in tasksrows:
        tasks_data[i[0]] = {'taskid': i[0], 'taskname': i[1],
                            'status': i[2], 'employeeid': i[3]}
    employee_data = {}
    for i in employeerows:
        employee_data[i[0]] = {
            'employeeid': i[0], 'name': i[1], 'position': i[2], 'departamentid': i[3]}
    departament_data = {}
    for i in departamentrows:
        departament_data[i[0]] = {'departamentid': i[0],
                                  'name': i[1], 'responcible_for': i[2]}
    with open('tasks.json', 'w') as f:
        json.dump(tasks_data, f)
    with open('departament.json', 'w') as f:
        json.dump(departament_data, f)
    with open('employee.json', 'w') as f:
        json.dump(employee_data, f)
    print("Succes export to json")


# графічний інтерфейс
def ui(pgcon,  litecon, departament, employee, tasks):
    root = Tk()
    mainf = Frame()
    mainf.pack(side=TOP, padx=10)
    f = Frame(mainf)
    f.pack(side=LEFT, padx=10)

# таблиця в яку будуть виводитися результати запитів до таблиці tasks
    columns = ('#1', '#2', '#3', '#4')
    table = ttk.Treeview(show="headings", columns=columns)

    entryname = Entry(f)
    entryid = Entry(f)
    entrystat = Entry(f)
    Label(f, text='Enter new task name:').grid(row=2, column=0, columnspan=2)
    entryname.grid(row=3, column=0)
    Label(f, text='Enter new task employee id:').grid(
        row=4, column=0, columnspan=2)
    entryid.grid(row=5, column=0)
    Label(f, text='Enter new task status:').grid(row=6, column=0, columnspan=2)
    entrystat.grid(row=7, column=0)
    Button(f, text="Add", command=lambda: task_insert(litecon, tasks,
           table, entryname, entryid, entrystat)).grid(row=8, column=0)

    f2 = Frame(mainf)
    f2.pack(side=LEFT, padx=10)
    taskid = Entry(f2)
    new_status = Entry(f2)
    Label(f2, text='Enter task id to update status or -1 to set "done" to all tasks:').grid(row=2,
                                                                                            column=0, columnspan=2)
    taskid.grid(row=3, column=0)
    Label(f2, text='Enter new status:').grid(row=4, column=0, columnspan=2)
    new_status.grid(row=5, column=0)
    Button(f2, text="Change", command=lambda: task_status_update(
        litecon, tasks, table, taskid.get(), new_status.get())).grid(row=6, column=0)

    f3 = Frame(mainf)
    f3.pack(side=LEFT, padx=10)
    taskidselect = Entry(f3)
    Label(f3, text='Enter task id to select task or nothing to select all tasks:').grid(
        row=2, column=0, columnspan=2)
    taskidselect.grid(row=3, column=0)
    Button(f3, text="Select", command=lambda: tasks_fetch(
        litecon, tasks, table, taskidselect.get())).grid(row=6, column=0)

    f4 = Frame(mainf)
    f4.pack(side=LEFT, padx=10)
    taskidel = Entry(f4)
    Label(f4, text='Enter task id to delete task:').grid(
        row=2, column=0, columnspan=2)
    taskidel.grid(row=3, column=0)
    Button(f4, text="Delete", command=lambda: tasks_delete(
        litecon, tasks, table, taskidel.get())).grid(row=6, column=0)

    f5 = Frame()
    f5.pack(side=TOP, pady=20)
    columns = ('#1', '#2', '#3', '#4')
    table.heading("#1", text="TaskId")
    table.heading("#2", text="TaskName")
    table.heading("#3", text="status")
    table.heading("#4", text="EmployeeId")
    table.pack(side=TOP, pady=10)
    Button(f5, text="Export to database_2(postges)", command=lambda: export_to_db2(
        litecon, pgcon, departament, employee, tasks, table)).pack(side=TOP, pady=10)
    Button(f5, text="Export to json", command=lambda: write_json(
        pgcon, tasks, departament, employee)).pack(side=TOP, pady=10)
    root.mainloop()


# головний застосунок, створює підключення до баз даних, обєкт контейнер MetaData,
# який містить представлення таблиць, створює таблиці в обох базах даних, вставляє деякі початкові дані
#  в базу даних sqlite та ініціалізує графічний інтерфейс для подальших операцій з базами даних
def main():
    pgengine, pgcon, litengine, litecon = connect_to_dbs()
    print(pgengine)
    print(litengine)
    metadata = MetaData()
    departament, employee, tasks = create_table(
        pgengine, pgcon, litengine, litecon, metadata)
    depart_insert(litecon, departament, ("loafers2", "do nothing"))
    depart_insert(litecon, departament, ("loafers3", "do nothing"))
    employee_insert(litecon, employee, ("Nameless", "another nobody", 2))
    employee_insert(litecon, employee, ("TestExport", "tester", 1))
    ui(pgcon,  litecon,
        departament, employee, tasks)


main()

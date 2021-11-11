import pymongo
import json


class MongoDB:
    def __init__(self):
        # connecting to MongoDB
        self.db_client = pymongo.MongoClient("mongodb://localhost:27017/")
        # connecting to the "mongo_db" Data Base or creating one if it does not exist
        self.current_db = self.db_client["mongo_db"]
        # getting the collection "technique" from our Data Base or creating one if it does not exist
        self.collection_tasks = self.current_db["Employees"]
        # getting the collection "specs" from our Data Base or creating one if it does not exist
        self.collection_teams = self.current_db["Teams"]
        self.team_status = 'in progress'

    def add_employee(self, id_task, task_name, employee_status):
        if id_task != "" and employee_status != "":
            if employee_status == "":
                employee_status = "in progress"
            # creating new technique object
            new_task = {
                'id': id_task,
                'Task': task_name,
                'status': employee_status,
            }

            self.collection_tasks.insert_one(new_task)
            print(self.collection_tasks.find_one({'id': id_task}))
            print("Complete")
        else:
            print("Enter task id and task name")

    def add_team(self, id_team, tasks_id):
        if id_team != "":
            tasks_id = tasks_id.split(" ")
            try:
                for i in tasks_id:
                    self.collection_tasks.find_one({'id': i})
            except:
                print("NO task with this id")

            new_team = {
                'id': id_team,
                'Team_squad': [*tasks_id],
                'status': self.team_status,
            }
            self.collection_teams.insert_one(new_team)
            print(self.collection_teams.find_one({'id': id_team}))
            print("Complete")
        else:
            print("You mast write id team")

    def edit_task(self, id_task_is, employee_status):
        self.collection_tasks.update_one({'id': id_task_is}, {'$set': {
            'status': employee_status,
        }})
        print("Complete")

    def refresh_team_status(self, id_team):

        for i in self.collection_teams.find_one({'id': str(id_team)})['Team_squad']:

            if self.collection_tasks.find_one({'id': i})['status'] == "done":
                self.team_status = "done"

            else:
                self.team_status = 'in progress'
                return 'in progress'

        self.collection_teams.update_one({'id': id_team}, {'$set': {
            'status': self.team_status,
        }})
        self.team_status = 'in progress'
        return "done"

    def edit_team(self, id_team, tasks_id):
        self.refresh_team_status(tasks_id)
        self.collection_teams.update_one({'id': id_team}, {'$set': {
            'Team_squad': {*tasks_id},
            'status': self.team_status,
        }})
        self.team_status = 'in progress'
        print("Complete")

    def delete_team_by_id(self, id_team):
        self.collection_teams.delete_one({'id': id_team})
        print("Complete")

    def delete_task_by_id(self, id_employee):
        self.collection_tasks.delete_one({'id': id_employee})
        print("Complete")

# def get_all_records(self):
#     # return [self.collection_teams.find_one({'id': 10})]
#     # self.collection_tasks.find_one({'id': 6})
#     return [list(self.collection_tasks.aggregate([
#         {"$group": {"_id": ["$id", "$Task", "$status"]}}
#     ])), list(self.collection_teams.aggregate([
#         {"$group": {"_id": ["$id", "$Team_squad", "$status"]}}
#     ]))]

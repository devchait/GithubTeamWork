from stores import *
import json


class Converter:
    def __init__(self, child):
        if child:
            self.child = child
        else:
            raise "Child can't be empty"

    def __to_dict(self, obj=None):
        current_obj = None
        new_dict = {}
        if obj and isinstance(obj, Store):
            current_obj = obj
        elif isinstance(self.child, Store):
            current_obj = self.child
        else:
            raise "Wrong Object"
        if current_obj:
            # print(current_obj.variable_value_dict)
            for k, v in current_obj.variable_value_dict.items():

                if k:
                    if isinstance(v, Store):
                        new_dict[k] = self.__to_dict(v)
                        # print(new_dict)
                    elif v is not None:
                        # print(k + " :elif " + str(v))
                        new_dict[k] = v
                        # print(new_dict)
                    else:
                        # print(k + " :el " + str(v))
                        new_dict[k] = ""
                        # print(new_dict)
            return new_dict
        else:
            return " "

    def to_json(self, obj=None):
        return self.__to_dict(obj)


class Gh_Issues_Tmw_Taskv1(Converter):
    def __init__(self, identity):
        self.issue = None
        self.identity = identity
        self.to_do_v1 = TeamworkToDoItem(self.identity)
        self.task = TeamworkTaskv1(self.identity)
        self.task.setValue("todo-item", self.to_do_v1)
        super().__init__(self.task)

    def convert(self, gh_issue):
        if isinstance(gh_issue, Issue):
            self.__set_default_values()
            self.issue = gh_issue
            self.__set_task_details()
            self.child = self.task
            return self.task
        else:
            raise "Wrong Object Initialization"

    def __set_default_values(self):
        self.to_do_v1.setValue("tasklistId", 2605642)
        self.to_do_v1.setValue("use-defaults", False)
        self.to_do_v1.setValue("completed", False)
        self.to_do_v1.setValue("creator-id", 0)
        self.to_do_v1.setValue("priority", "medium")
        self.to_do_v1.setValue("parentTaskId", 0)
        self.to_do_v1.setValue("everyone-must-do", False)
        self.to_do_v1.setValue("estimated-minutes", 200)
        self.to_do_v1.setValue("responsible-party-id", 0)
        self.to_do_v1.setValue("progress", 0)
        self.to_do_v1.setValue("tagIds", 1)
        self.to_do_v1.setValue("columnId", 0)
        self.to_do_v1.setValue("notify", False)

    def __set_milestone_tag(self):
        mile_stone = TeamworkTaskTags(0)
        gh_milestone = self.issue.getValue("milestone")
        # currently we are considering the color of tag to receive from the milestone's description
        # We could also have desription in some - formatted to get description and other info
        mile_stone.setValue("color", gh_milestone.getValue("description"))
        mile_stone.setValue("name", gh_milestone.getValue("title"))
        mile_stone.setValue("projectId", "")

    def __set_assignees(self):
        assignees = self.issue.getValue("assignees")
        if assignees and isinstance(assignees, list):
            pass
        else:
            pass
        # self.to_do_v1.setValue("creator-id")

    def __set_dates(self, creation_date=None, due_date=None):
        self.to_do_v1.setValue("start-date", creation_date)
        self.to_do_v1.setValue("due-date", due_date)

    def __set_estimated_time(self, time=None):
        print(time)
        if time:
            ele = time.split()
            if len(ele) == 2:
                if ele[1].upper() == "HRS":
                    mins = int(ele[0]) * 60
                    self.to_do_v1.setValue("estimated-minutes", mins)
                else:
                    self.to_do_v1.setValue("estimated-minutes", ele[0])
            else:
                self.to_do_v1.setValue("estimated-minutes", 80)
                # raise "Wrong Time Information"

    def __set_tags(self, tagIds=None):
        self.to_do_v1.setValue("tagIds", tagIds)

    def __set_task_details(self):

        body = self.issue.getValue("body")
        description = (
            body.getValue("Name")
            + body.getValue("Description")
            + body.getValue("Details")
            + body.getValue("Additional_Context")
            + body.getValue("Extra_Material")
        )
        self.__set_estimated_time(body.getValue("Estimated_Time"))
        self.__set_dates(
            creation_date=body.getValue("Expected_Start_Date"),
            due_date=body.getValue("Expected_End_Date"),
        )
        self.to_do_v1.setValue("content", self.issue.getValue("title"))
        self.to_do_v1.setValue("description", description)
        if body.getValue("SubTasksList"):
            self.__set_sub_task_details(body.getValue("SubTasksList"))

    def __set_sub_task_details(self, subtaskDetails=None):
        pass


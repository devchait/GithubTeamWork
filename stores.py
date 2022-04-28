imp_key_map = {
    "issue_url": "url",
    "labels_url": "lables_url",
    "issue_number": "number",
    "issue_title": "title",
    "assignee": "assignee",
    "color": "color",
    "login_id": "login",
    "description": "description",
    "milestone": "milestone",
    "state": "state",
    "created_at": "created_at",
    "updated_at": "updated_at",
    "due_on": "due_on",
    "closed_at": "closed_at",
    "body": "body",
    "labels": "labels",
    "assignee": "assignee",
    "assignees": "assignees",
}


def parse_multi_line(value, variables, value_dict, imp_key=None):
    # print("Value is: " + value)
    if value:
        new_line = "\n"
        begin = False
        topic = False
        earlier_word = None
        unknown_lines = []
        for line in value.splitlines():
            if line:
                words = line.strip().split(" ")
                begin = True
                # print("first word:: " + words[0])
                proper_word = (
                    words[0][:-1] if words[0] and words[0][-1] == ":" else words[0]
                )
                # print("ppw: " + proper_word)
                new_line = new_line + "\n"
                if proper_word in variables:
                    # print(
                    #     "ppw True earlierwr:" + str(earlier_word) + " : " + str(imp_key)
                    # )
                    earlier_word = proper_word
                    topic = True
                    begin = False
                    for word in words[1:]:
                        new_line = new_line + word

                    if earlier_word and earlier_word != imp_key:
                        value_dict[earlier_word] = new_line
                        new_line = "\n"
                    elif earlier_word and earlier_word == imp_key:
                        subTaskObj = Store.getStoreByKey(imp_key, 1)
                        # print("SubTaskList bdy:" + new_line)
                        subTaskObj.setValue(Body, new_line)
                        value_dict[imp_key] = subTaskObj
                    else:
                        pass

                elif begin and topic:
                    # print("@@@: " + words)
                    for word in words:

                        if word != "-" or word != "[ ]":
                            new_line = new_line + word + " "
                else:
                    unknown_lines.append(line)
        if len(unknown_lines) > 0:
            for l in unknown_lines:
                value_dict["unknown_comment"] = (
                    l
                    if not "unknown_comment" in value_dict.keys()
                    else value_dict["unknown_comment"] + l
                )


class Store:

    __registered_class__ = {}

    def __init__(self, variables):
        if isinstance(variables, list):
            self.variables = variables
        else:
            self.variables = [variables]
        self.variable_value_dict = {}

    def getValue(self, variable):

        if variable in self.variable_value_dict.keys():
            return self.variable_value_dict[variable]
        else:
            return ""

    def setValue(self, variable, value):
        if variable in self.variables:
            if variable in self.variable_value_dict.keys():
                if isinstance(self.variable_value_dict[variable], list):
                    self.variable_value_dict[variable].append(value)
                else:
                    self.variable_value_dict[variable] = [
                        self.variable_value_dict[variable],
                        value,
                    ]
            else:
                self.variable_value_dict[variable] = value

    def __str__(self):
        str_repr = " "
        for k, v in self.variable_value_dict.items():
            str_repr = str_repr + k
            if isinstance(v, list):
                str_repr = str_repr + " [ "
                for item in v:
                    str_repr = str_repr + " : " + str(item)
                str_repr = str_repr + " ]\n "
            else:
                str_repr = str_repr + " : " + str(v) + " , "
        return str_repr

    @staticmethod
    def register_class(class_key, class_name):
        Store.__registered_class__[class_key] = class_name

    @staticmethod
    def getStoreByKey(key, param):
        if key in Store.__registered_class__.keys():
            return Store.__registered_class__[key](param)


class Issue(Store):
    def __init__(self, identity):
        self.identity = identity
        print(identity)
        self.subTasks = []
        self.has_attribute = False
        super().__init__(
            [
                "number",
                "state",
                "title",
                "body",
                "labels",
                "assignees",
                "milestone",
                "pull_request",
                "closed_at",
                "created_at",
                "updated_at",
            ]
        )


class Comment(Store):
    def __init__(self, identity):
        self.identity = identity
        self.st_time = 0
        self.et_time = 0
        self._am_pm = 0
        super().__init__(["body", "html_url", "user", "created_at", "updated_at"])

    def setValue(self, variable, value):
        if variable == "body":
            # b = self.getValue("body")

            self.__extract_time_info(value.getValue("unknown_comment"))
            self.variable_value_dict["start-time"] = self.st_time
            self.variable_value_dict["end-time"] = self.et_time
            self.variable_value_dict["AM_PM"] = self._am_pm
        super().setValue(variable, value)

    def __extract_time_info(self, comment_data):
        print("@@ : " + comment_data)
        if comment_data:
            words = comment_data.split(" ")
            for w in words:

                if w[0] == "/" and w[-1] == "/":

                    time_infos = w[1:-1].split("-")
                    # print(time_infos)
                    self.st_time = time_infos[0]
                    self.et_time = time_infos[1]
                    self._am_pm = 0 if time_infos[2].upper() == "AM" else 1
                    # print(self.st + " : " + self.et)


class ComUser(Store):
    def __init__(self, identity):
        self.identity = identity
        super().__init__(["login"])


class Lable(Store):
    def __init__(self, identity):
        self.identity = identity
        super().__init__(["name", "color", "description"])


class Milestone(Store):
    def __init__(self, identity):
        self.identity = identity
        super().__init__(
            [
                "title",
                "number",
                "state",
                "description",
                "closed_issues",
                "created_at",
                "updated_at",
                "closed_at",
                "due_on",
            ]
        )


class Assignee(Store):
    def __init__(self, identity):
        self.identity = identity
        super().__init__(["login", "type"])


class Body(Store):
    def __init__(self, identity):
        self.identity = identity
        super().__init__(
            [
                "Type",
                "Name",
                "Number",
                "Description",
                "Details",
                "Additional_Context",
                "Extra_Material",
                "SubTasksList",
                "Parent_Task",
                "Previous_Task_Number",
                "Estimated_Time",
                "Expected_Start_Date",
                "Expected_End_Date",
            ]
        )

    def setValue(self, variable, value):
        if value:
            parse_multi_line(
                value, variable, self.variable_value_dict, imp_key="SubTasksList"
            )


class SubTask(Store):
    def __init__(self, identity):
        self.identity = identity
        super().__init__(
            ["-Number", "-Estimated_Time", "-Previous_Task", "-Description"]
        )

    def setValue(self, variable, value):
        if value:
            parse_multi_line(value, self.variables, self.variable_value_dict)


class TeamworkTaskContainer(Store):
    def __init__(self, identity):
        self.identity = identity
        super().__init__(
            [
                "attachmentOptions",
                "attachments",
                "card",
                "predecessors",
                "tags",
                "task",
                "taskOptions",
            ]
        )


class TeamworkTask(Store):
    def __init__(self, identity):
        self.identity = identity
        super().__init__(
            [
                "assignees",
                "attachmentIds",
                "changeFollowers",
                "commentFollowers",
                "completedAt",
                "completedBy",
                "createdAt",
                "createdBy",
                "crmDealIds",
                "customFields",
                "description",
                "dueAt",
                "estimatedMinutes",
                "grantAccessTo",
                "hasDeskTickets",
                "name",
                "parentTaskId",
                "priority",
                "private",
                "progress",
                "reminders",
                "repeatOptions",
                "startAt",
                "status",
                "tagIds",
                "tasklistId",
                "templateRoleName",
                "ticketId",
            ]
        )


class TeamworkTaskOptions(Store):
    def __init__(self, identity):
        self.identity = identity
        super().__init__(
            [
                "appendAssignees",
                "checkInvalidusers",
                "everyoneMustDo",
                "fireWebhook",
                "isTemplate",
                "logActivity",
                "notify",
                "parseInlineTags",
                "positionAfterTaskId",
                "shiftProjectDates",
                "useDefaults",
                "useNotifyViaTWIM",
            ]
        )


class TeamworkTaskAttachmentOptions(Store):
    def __init__(self, identity):
        self.identity = identity
        super().__init__(["removeOtherFiles"])


class TeamworkTaskAttachments(Store):
    def __init__(self, identity):
        self.identity = identity
        super().__init__(["files", "pendingFiles"])


class TeamworkTaskCard(Store):
    def __init__(self, identity):
        self.identity = identity
        super().__init__(["columnId"])


class TeamworkTaskPredecessor(Store):
    def __init__(self, identity):
        self.identity = identity
        super().__init__(["id", "type"])


class TeamworkTaskTags(Store):
    def __init__(self, identity):
        self.identity = identity
        super().__init__(["color", "name", "projectId"])


class TeamworkGeneralIds(Store):
    def __init__(self, identity):
        self.identity = identity
        super().__init__(["Null", "Set", "Value"])


class TeamworkTaskv1(Store):
    def __init__(self, identity):
        self.identity = identity
        super().__init__(["todo-item"])


class TeamworkToDoItem(Store):
    def __init__(self, identity):
        self.identity = identity
        super().__init__(
            [
                "use-defaults",
                "completed",
                "content",
                "tasklistId",
                "creator-id",
                "notify",
                "responsible-party-id",
                "start-date",
                "due-date",
                "description",
                "priority",
                "progress",
                "parentTaskId",
                "tagIds",
                "everyone-must-do",
                "predecessors",
                "reminders",
                "columnId",
                "commentFollowerIds",
                "changeFollowerIds",
                "grant-access-to",
                "private",
                "estimated-minutes",
                "pendingFileAttachments",
                "updateFiles",
                "attachments",
                "removeOtherFiles",
                "attachmentsCategoryIds",
                "pendingFileAttachmentsCategoryIds",
                "repeatOptions",
            ]
        )


Store.register_class("tmwrkTaskv1", TeamworkTaskv1)
Store.register_class("tmwrkTaskToDov1", TeamworkToDoItem)
Store.register_class("tmwrkTaskContainer", TeamworkTaskContainer)
Store.register_class("tmwrkGeneralIds", TeamworkGeneralIds)
Store.register_class("tmwrkTaskTags", TeamworkTaskTags)
Store.register_class("tmwrkTaskPredecessor", TeamworkTaskPredecessor)
Store.register_class("tmwrkTaskCards", TeamworkTaskCard)
Store.register_class("tmwrkTaskAttachment", TeamworkTaskAttachments)
Store.register_class("tmwrkTaskAttachmentOption", TeamworkTaskAttachmentOptions)
Store.register_class("tmwrkTask", TeamworkTask)
Store.register_class("tmwrkTaskOption", TeamworkTaskOptions)
Store.register_class("issue", Issue)
Store.register_class("body", Body)
Store.register_class("SubTasksList", SubTask)
Store.register_class("labels", Lable)
Store.register_class("milestone", Milestone)
Store.register_class("assignees", Assignee)
Store.register_class("comment", Comment)
Store.register_class("user", ComUser)


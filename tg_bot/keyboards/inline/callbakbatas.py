from aiogram.utils.callback_data import CallbackData

adding_task_calllback = CallbackData("adding", "type_task", "task")
tasks_list_callback = CallbackData("tasks", "task_id", "text", "my_task")
edit_callback = CallbackData("edit", "field")
cancel_callback = CallbackData("cancel", "trigger")

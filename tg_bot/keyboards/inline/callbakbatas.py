from aiogram.utils.callback_data import CallbackData

adding_task_callback = CallbackData("adding", "type_task", "task")
tasks_list_callback = CallbackData("tasks", "task_id", "text", "scheduler_id", "my_task")
edit_callback = CallbackData("edit", "field")
cancel_callback = CallbackData("cancel", "trigger")
notify_callback = CallbackData("notify", "ans")

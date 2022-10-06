from aiogram.utils.callback_data import CallbackData

notify_callback = CallbackData("notify", "add")
tasks_list_call = CallbackData("task_list", "task_id", "task")
paginator_call = CallbackData("paginator", "next", "offset", "pager")
edit_task_call = CallbackData("edit", "edit_task", "attr")

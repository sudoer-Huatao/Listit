import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title="Listit", width=600, height=600)
num = 0  # Number of to-dos.
dict_num = 0  # Iterator for dictionary
example_tasks = [
    "Write some code",
    "Do my homework",
    "Read a good book",
    "Do my chores",
    "Read the daily news",
    "Play my favorite video game",
    "Go to the movies",
    "Buy Mom a gift",
]
tasks = []  # List for storing tasks
task = 0


def make_new(todo: str, done: bool):
    global task, num, nums
    with dpg.group(tag=str(num), horizontal=True, parent="main"):
        if done != None:
            dpg.add_checkbox(
                label="Done?",
                tag="done" + str(num),
                default_value=done,
                callback=store_done,
            )
        else:
            dpg.add_checkbox(
                label="Done?",
                tag="done" + str(num),
                default_value=done,
                callback=store_done,
            )
        if todo == "add":
            dpg.add_input_text(
                hint="Idea: "
                + example_tasks[task % 7],  # Circulate through example to-dos.
                tag="todo" + str(num),
                callback=store_task,
            )
        else:
            dpg.add_input_text(
                default_value=todo,
                tag="todo" + str(num),
                callback=store_task,
            )

        dpg.add_button(
            label="Remove to-do",
            tag="delete_todo" + str(num),
            callback=remove_row,
            user_data=str(num),
        )

    num += 1
    task += 1
    dpg.delete_item(nums)
    nums = dpg.add_text("Number of to-do's: " + str(num), parent="main", before="add")


def remove_row(user_data: str):
    global num, nums
    num -= 1
    dpg.delete_item(nums)
    nums = dpg.add_text("Number of to-do's: " + str(num), parent="main", before="add")
    dpg.delete_item(user_data.lstrip("delete_todo"))


def store_task(user_data: str):
    tasks.append([dpg.get_value(user_data), False])


def store_done(user_data: str):
    user_data = int(user_data.lstrip("done"))
    tasks[user_data][1] = not (tasks[user_data][1])  # Reverse done/not done


def save_list():
    f = open("tasks.txt", "w")
    f.seek(0)
    f.truncate()
    for todo in tasks:
        f.write(todo[0] + " " + str(todo[1]) + "\n")
    f.close()


def load_list():
    global num
    f = open("tasks.txt", "r")
    for i in range(num):
        dpg.delete_item(i)  # Delete current list todo-list

    num = 0
    tasks.clear()

    for line in f.readlines():
        todo, done = line.split()
        make_new(todo, bool(done))  # Load each todo from save file


def change_color():
    pass


with dpg.viewport_menu_bar():
    with dpg.menu(label="My Todo-list"):
        dpg.add_menu_item(label="Save", callback=save_list)
        dpg.add_menu_item(label="Load a to-do list", callback=load_list)

    with dpg.menu(label="Settings"):
        dpg.add_menu_item(label="Change color theme", callback=change_color)

with dpg.window(label="Listit", tag="main", width=600, height=600):
    global nums
    dpg.add_text("Listit: Your own to-do list.\n\nIf you can list it, you can do it.\n")
    dpg.add_button(label="Add new to-do", callback=make_new, tag="add")
    nums = dpg.add_text("Number of to-do's: " + str(num), before="add")


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

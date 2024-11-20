import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title="Listit", width=600, height=600)
num = 0  # Number of to-dos.
example_tasks = [
    "Write some code",
    "Finish homework",
    "Read a good book",
    "Do my chores",
    "Read the daily news",
    "Play a video game",
    "Go to the movies",
    "Buy Mom a gift",
    "Practice music instruments",
]
fonts = ["Aptos-Display.ttf", "ProggyClean.otf"]
tasks = {}  # List for storing tasks
task = 0


def make_new(todo: str, done: bool):
    # Make a new todo
    global task, num, nums
    num += 1
    with dpg.group(tag=str(num), horizontal=True, parent="main"):
        if done == None:
            dpg.add_checkbox(
                label="Done?",
                tag="done" + str(num),
                callback=store_done,
            )
        else:
            dpg.add_checkbox(
                label="Done?",
                default_value=done,
                tag="done" + str(num),
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

    task += 1
    dpg.delete_item(nums)
    nums = dpg.add_text("Number of to-do's: " + str(num), parent="main", before="add")


def remove_row(user_data: str):
    # Remove a todo
    global num, nums
    num -= 1
    dpg.delete_item(nums)
    nums = dpg.add_text("Number of to-do's: " + str(num), parent="main", before="add")
    dpg.delete_item(user_data.lstrip("delete_todo"))


def store_task(user_data: str):
    # Store to-do in dict
    tasks[int(user_data.lstrip("todo"))] = [dpg.get_value(user_data), False]


def store_done(user_data: str):
    # Update whether todo is done in dict
    user_data = int(user_data.lstrip("done"))
    try:
        (tasks[user_data])[1] = not ((tasks[user_data])[1])  # Reverse done/not done
    except KeyError:
        print("Warning: No todo to check!")


def save_list():
    # Save to-dos into file
    f = open("tasks.txt", "w")
    f.seek(0)
    f.truncate()
    for key, val in tasks.items():
        f.write(val[0] + " " + str(val[1]) + "\n")
    f.close()


def load_list():
    # Load to-do list
    global num

    f = open("tasks.txt", "r")
    for i in range(num):
        dpg.delete_item(str(i))  # Delete current list todo-list

    num = 0
    tasks.clear()

    for line in f.readlines():
        if line != "\n":
            todo, done = line.split()
            make_new(todo, eval(done))  # Load each todo from save file


def change_color():
    dpg.show_style_editor()


def change_font():
    dpg.show_font_manager()


with dpg.theme() as global_theme:  # Color themes
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(
            dpg.mvThemeCol_WindowBg, (200, 200, 50), category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_style(
            dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_Text, (10, 10, 10), category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_MenuBarBg, (220, 170, 0), category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_TitleBg, (220, 170, 0), category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_style(
            dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_Button, (220, 190, 0), category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_CheckMark, (220, 170, 0), category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_FrameBg, (230, 200, 0), category=dpg.mvThemeCat_Core
        )
        dpg.add_theme_color(
            dpg.mvThemeCol_PopupBg, (220, 170, 0), category=dpg.mvThemeCat_Core
        )

dpg.bind_theme(global_theme)

with dpg.font_registry():  # Default font is Sans
    dpg.add_font("Aptos-Display.ttf", 20)

with dpg.viewport_menu_bar():
    with dpg.menu(label="My Todo-list"):
        dpg.add_menu_item(label="Save", callback=save_list)
        dpg.add_menu_item(label="Load a to-do list", callback=load_list)

    with dpg.menu(label="Settings"):
        dpg.add_menu_item(label="Change font", callback=change_font)
        dpg.add_menu_item(label="Change color theme", callback=change_color)

with dpg.window(label="Listit", tag="main", width=600, height=600):
    global nums
    dpg.add_text("Listit: Your own to-do list.\n\nIf you can list it, you can do it.\n")
    dpg.add_button(label="Add new to-do", callback=make_new, tag="add")
    nums = dpg.add_text("Number of to-do's: " + str(num), before="add")

dpg.set_viewport_large_icon("icon.ico")
dpg.set_viewport_small_icon("icon.ico")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

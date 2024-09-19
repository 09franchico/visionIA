import dearpygui.dearpygui as dpg
import dearpygui_grid as dpg_grid

dpg.create_context()
dpg.setup_dearpygui()
dpg.create_viewport()
dpg.show_viewport()

window = dpg.add_window(width=400, height=400, no_scrollbar=True, no_title_bar=True)

grid = dpg_grid.Grid(3, 3, window)

grid.push(dpg.add_button(parent=window), 0, 1) # middle col, top row
# grid.push(dpg.add_button(parent=window), 0, 1)  # left col, middle row
# grid.push(dpg.add_button(parent=window), 1, 1)  # middle col, middle row
# grid.push(dpg.add_button(parent=window), 2, 1)  # right col, middle row
# grid.push(dpg.add_button(parent=window), 1, 2)  # middle col, bottom row

with dpg.item_handler_registry() as window_hr:
    dpg.add_item_visible_handler(callback=grid)
dpg.bind_item_handler_registry(window, window_hr)

dpg.start_dearpygui()




# import dearpygui.dearpygui as dpg
# import dearpygui.demo as demo

# dpg.create_context()
# dpg.create_viewport(title='Custom Title', width=600, height=600)

# demo.show_demo()

# dpg.setup_dearpygui()
# dpg.show_viewport()
# dpg.start_dearpygui()
# dpg.destroy_context()
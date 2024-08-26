import dearpygui.dearpygui as dpg


with dpg.theme() as global_theme:
    
    with dpg.theme_component(dpg.mvAll):
        
        # Styles
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 4, 4, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 4, 4, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 4, 4, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4, 4, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0.1, category=dpg.mvThemeCat_Core)

        # Colors
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (33, 33, 33), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (48, 48, 48), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (200, 200, 200), category=dpg.mvThemeCat_Core)
        
        
with dpg.theme() as item_theme_result:
    with dpg.theme_component(dpg.mvChildWindow):
         dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255, 0, 0))


with dpg.theme() as disabled_theme:
    
    with dpg.theme_component(dpg.mvAll):
        # Styles

        # Colors
        dpg.add_theme_color(dpg.mvThemeCol_Text, (100, 100, 100), category=dpg.mvThemeCat_Core)
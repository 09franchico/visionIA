import dearpygui.dearpygui as dpg


import dearpygui.dearpygui as dpg

class ThemeManager:
    def __init__(self):
        
        self.global_theme = None
        self.item_theme_result = None
        self.disabled_theme = None
        self.main_font_registry = None
        
        #Fontes
        self.regular_font = None
        self.bold_font = None
        self.score_font = None
        self.score_font_result = None
        
        self.create_themes()

    def create_themes(self):
        
        with dpg.theme() as self.global_theme:
            
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 4, 4, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 4, 4, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 4, 4, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4, 4, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0.1, category=dpg.mvThemeCat_Core)

                # Cores
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (33, 33, 33), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (48, 48, 48), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Text, (200, 200, 200), category=dpg.mvThemeCat_Core)

        with dpg.theme() as self.item_theme_result:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255, 0, 0))



        with dpg.theme() as self.disabled_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (100, 100, 100), category=dpg.mvThemeCat_Core)
                
             
    def font(self):
        with dpg.font_registry() as self.main_font_registry:
            try:
                self.regular_font = dpg.add_font('fonts/Roboto/Roboto-Regular.ttf', 16)
                self.bold_font = dpg.add_font('fonts/Roboto/Roboto-Bold.ttf', 21)
                self.score_font = dpg.add_font('fonts/ARCADE.ttf', 35)
                self.score_font_result = dpg.add_font('fonts/ARCADE.ttf', 50)
            except Exception as e:
                print(f"Erro ao carregar a fonte: {e}")

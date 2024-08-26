import dearpygui.dearpygui as dpg

def setup_font():
    with dpg.font_registry():
        font = dpg.add_font("path_to_your_font.ttf", size=24)  # Ajuste o tamanho da fonte aqui
    return font

def display_text_with_font():
    font = setup_font()
    
    with dpg.window(label="Font Example"):
        with dpg.group():
            with dpg.font(font):
                dpg.add_text("REPROVADO")

dpg.create_context()
dpg.create_viewport(title='Font Example', width=600, height=400)
dpg.setup_dearpygui()

display_text_with_font()

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

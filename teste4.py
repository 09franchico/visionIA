import dearpygui.dearpygui as dpg

dpg.create_context()

# Variáveis globais para armazenar as coordenadas iniciais e finais
start_pos = [0, 0]
end_pos = [0, 0]

def start_drawing_rect(sender, app_data):
    global start_pos
    start_pos = dpg.get_mouse_pos()

def update_rect(sender, app_data):
    global end_pos
    end_pos = dpg.get_mouse_pos()
    dpg.configure_item("rectangle", pmin=start_pos, pmax=end_pos)

def stop_drawing_rect(sender, app_data):
    global start_pos, end_pos
    # Aqui você pode adicionar lógica para "fixar" o retângulo, se necessário.
    pass

with dpg.handler_registry():
    dpg.add_mouse_click_handler(callback=start_drawing_rect)  # Inicia o desenho
    dpg.add_mouse_drag_handler(callback=update_rect)  # Atualiza o retângulo
    dpg.add_mouse_release_handler(callback=stop_drawing_rect)  # Finaliza o desenho

with dpg.window(width=500, height=300, tag="teste"):
    dpg.add_text("Clique e arraste para desenhar um retângulo", tag="text_item")
    dpg.add_drawlist(width=500, height=300)  # Local onde será desenhado
    dpg.draw_rectangle([0, 0], [0, 0], color=[255, 0, 0, 255], tag="rectangle")  # Retângulo inicial

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()



# import dearpygui.dearpygui as dpg
# import dearpygui.demo as demo

# dpg.create_context()
# dpg.create_viewport(title='Custom Title', width=600, height=600)

# demo.show_demo()

# dpg.setup_dearpygui()
# dpg.show_viewport()
# dpg.start_dearpygui()
# dpg.destroy_context()
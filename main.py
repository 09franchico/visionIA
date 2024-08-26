import dearpygui.dearpygui as dpg
import uuid
import cv2 as cv
import numpy as np



# Contexto principal
dpg.create_context()
from theme_settings import *


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
    pass

with dpg.handler_registry():
    dpg.add_mouse_click_handler(callback=start_drawing_rect) 
    dpg.add_mouse_drag_handler(callback=update_rect)
    dpg.add_mouse_release_handler(callback=stop_drawing_rect)


def query(sender, app_data, user_data):
        
    x1, y1, x2, y2 = app_data
    
    if dpg.does_item_exist("teste"):
        dpg.delete_item("teste")
        
    
    dpg.draw_rectangle(
        pmin=[x1, x2],  
        pmax=[y1, y2], 
        thickness=5,
        color=[58,239,45],
        fill=None,
        parent=sender,
        tag="teste"
    )


def set_image_plot(path):
    try:  
        
        if dpg.does_item_exist("imagem_id"):
            dpg.delete_item("imagem_id")
                    
        if dpg.does_item_exist("y_axis_image_id"):
           return
        else:
            width, height, channels, data = dpg.load_image(path)
                
            with dpg.texture_registry():
                dpg.add_static_texture(width, height, data, tag="imagem_id")

            dpg.add_image_series("imagem_id", [0, 0], [width, height], parent="y_axis", tag="y_axis_image_id")
        
        
        
    except Exception as e:
      print(f"Erro set_image: {e}")  
    
    
def set_image_drawing_tela(path):
    
    if dpg.does_item_exist("imagem_id_draw"):
            dpg.delete_item("imagem_id_draw")
                    
    if dpg.does_item_exist("draw_id"):
        return
    
    else:
        
        width, height, channels, data = dpg.load_image(path)
        
        with dpg.texture_registry():
            dpg.add_static_texture(width, height, data, tag="imagem_id_draw")
            
        dpg.draw_image("imagem_id_draw", (0, 0), (800, 1200), uv_min=(0, 0), uv_max=(1, 1),parent="draw_image",tag="draw_id")
        
    

def callback(sender, app_data, user_data):
    global path
    path = app_data["file_path_name"]
    
    try:
        set_image_plot(path)
    except Exception as e:
        print(f"Erro no callback do diálogo de arquivos: {e}")
        
    
def thema():
    dpg.bind_theme(disabled_theme)
    

def set_image_drawing(sender, app_data,user_data):
    global path  # Declaração da variável global para acessar seu valor
    
    print(sender)
    print(app_data)
    print(user_data)
    # print(user_data)
    try:
        if app_data == 66:
           set_image_drawing_tela(path)  # Chama a função correta para definir a imagem
    except Exception as e:
        print(f"Erro ao definir imagem: {e}")
        
        
#-------------------------------------------------------------------GUI------------------------------------------------------------------------
    
with dpg.file_dialog(directory_selector=False, show=False, callback=callback, id="file_dialog_id", width=700 ,height=400):
    dpg.add_file_extension(".bmp")
    dpg.add_file_extension(".jpeg", color=(150, 255, 150, 255))
    dpg.add_file_extension("Source files (*.cpp *.h *.hpp){.cpp,.h,.hpp}", color=(0, 255, 255, 255))
    dpg.add_file_extension(".h", color=(255, 0, 255, 255), custom_text="[header]")
    dpg.add_file_extension(".py", color=(0, 255, 0, 255), custom_text="[Python]")



with dpg.window(tag="Primary Window") as app:
    
    with dpg.child_window(height=90, autosize_x=True):
            dpg.add_spacer(height=20)
            with dpg.group(horizontal=True):
                dpg.add_spacer(width=10)
                score = dpg.add_text(default_value="VISIONIA")
                dpg.bind_item_font(item=score, font=score_font)
            
                
    with dpg.group(horizontal=True):
        
            with dpg.child_window(width=800,border=True):
                
                with dpg.tab_bar(callback=set_image_drawing):
                    
                    with dpg.tab(label="Plotar imagem",tag="tab1_plot_image"):
                        with dpg.plot(query=True,width=800,height=620,crosshairs=True,callback=query,tag="plot_imagem"):
                                dpg.add_plot_legend()
                                dpg.add_plot_axis(dpg.mvXAxis, label="",tag="x_axis")
                                dpg.add_plot_axis(dpg.mvYAxis, label="", tag="y_axis")
                                
                    with dpg.tab(label="Desenhar imagem",tag="tab2_plot_image"):
                        
                           with dpg.drawlist(width=1200, height=600,tag="draw_image"):  # or you could use dpg.add_drawlist and set parents manually
                               pass
                                

            
            with dpg.child_window(autosize_x=True, autosize_y=True):

                with dpg.group():
                    with dpg.child_window(height=380,border=False):
                        dpg.add_spacer(height=200)
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=10)
                            dpg.add_button(label="ANEXA IMAGEM",width=150,height=30,callback=lambda: dpg.show_item("file_dialog_id"))
                            dpg.add_spacer(width=20)
                            dpg.add_button(label="START",width=150,height=30)
                               
                    with dpg.child_window(height=265) as aprov:
                        dpg.add_spacer(height=110)
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=60)
                            text = dpg.add_text(default_value="REPROVADO")
                            dpg.bind_item_font(item=text, font=score_font_result)
                        
                         
                                                      
dpg.create_viewport(title='VISONIA', width=1200, height=800)
dpg.set_viewport_max_height(800)
dpg.set_viewport_max_width(1200)

dpg.bind_theme(global_theme)
dpg.bind_font(regular_font)
dpg.bind_item_theme(aprov, item_theme_result) 


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
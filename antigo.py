import dearpygui.dearpygui as dpg
import uuid
import cv2 as cv
import numpy as np
import json
import os



# Contexto principal
dpg.create_context()
from theme_settings.theme_registry import *

circle_data = []
image_path = None

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
    global image_path
    image_path = path
    
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
    try:
        if app_data == 66:
           set_image_drawing_tela(path)  # Chama a função correta para definir a imagem
    except Exception as e:
        print(f"Erro ao definir imagem: {e}")
        
        
def plot_mouse_click():
    x, y = dpg.get_plot_mouse_pos()
    # Ajuste o raio de acordo com a escala
    radius = 4500 * 0.01
    
    tag = f"circle_{len(circle_data)}" 
    dpg.draw_circle(center=[x, y], radius=radius, color=(219, 73, 255), parent=draw_node,thickness=2,tag=tag)
    
    circle_data.append({"tag": tag, "center": (x, y), "radius": radius})
    print(f"Círculo desenhado em: ({x}, {y})")
    
    
def save_value_plot():

    file_path = os.path.join(os.getcwd(), 'circle_data.json')
    
    with open(file_path, 'w') as file:
        json.dump(circle_data, file, indent=4)
    
    print(f"Dados salvos em: {file_path}")
    for data in circle_data:
        print(f"Tag: {data['tag']}, Coordenadas: {data['center']}, Raio: {data['radius']}")
    
def delete_item_circle():
    circle_data.clear()
    dpg.delete_item(draw_node,children_only=True)

    
def set_cor():
    for data in circle_data:
        dpg.configure_item(data["tag"], color=(255,0,0))
        

def crop_image_circle():
    global image_path
    if image_path is None or not circle_data:
        print("Imagem não carregada ou nenhum círculo desenhado.")
        return
    
    image = cv.imread(image_path)
    
    for idx, circle in enumerate(circle_data):
        
        center, radius = circle["center"], circle["radius"]
        center = (int(center[0]), int(center[1]))
        radius = int(radius)
        
        # Calcula a área do retângulo que envolve o círculo
        x_start, y_start = int(center[0] - radius), int(center[1] - radius)
        x_end, y_end = int(center[0] + radius), int(center[1] + radius)
        
        cropped_result = image[y_start:y_end, x_start:x_end]
        
        output_path = os.path.join(os.getcwd(), f'cropped_circle_image_{idx}.png')
        cv.imwrite(output_path, cropped_result)
        print(f"Imagem recortada salva em: {output_path}")
            

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
                score = dpg.add_text(default_value="APRENDENDO DEARPYGUI")
                dpg.bind_item_font(item=score, font=score_font)
            
                
    with dpg.group(horizontal=True):
        
            with dpg.child_window(width=800,border=True):
                
                with dpg.tab_bar(callback=set_image_drawing):
                    
                    with dpg.tab(label="Plotar imagem",tag="tab1_plot_image"):
                        with dpg.plot(query=True,width=800,height=620,crosshairs=True,tag="plot_imagem",no_box_select=True,no_menus=True) as plot:
                                dpg.add_plot_legend()
                                xaxis = dpg.add_plot_axis(dpg.mvXAxis, label="",tag="x_axis")
                                yaxis = dpg.add_plot_axis(dpg.mvYAxis, label="", tag="y_axis")
                                
                                draw_node = dpg.add_draw_node(parent=plot)
                                
                    with dpg.tab(label="Desenhar imagem",tag="tab2_plot_image"):
                           with dpg.drawlist(width=1200, height=600,tag="draw_image"):  # or you could use dpg.add_drawlist and set parents manually
                               pass
                                
            
            with dpg.child_window(autosize_x=True, autosize_y=True):

                with dpg.group():
                    with dpg.child_window(height=380,border=False):
                        with dpg.group():
                            dpg.add_spacer(width=10)
                            dpg.add_button(label="ANEXA IMAGEM",width=150,height=30,callback=lambda: dpg.show_item("file_dialog_id"))
                            dpg.add_spacer(width=20)
                            dpg.add_button(label="START",width=150,height=30)
                            dpg.add_spacer(width=20)
                            dpg.add_button(label="DELETE",width=150,height=30,callback=delete_item_circle)
                            dpg.add_button(label="SALVAR",width=150,height=30,callback=save_value_plot)
                            dpg.add_button(label="MUDAR COR",width=150,height=30,callback=set_cor)
                            dpg.add_button(label="FOTO",width=150,height=30,callback=crop_image_circle)
                               
                    with dpg.child_window(height=265) as aprov:
                        dpg.add_spacer(height=110)
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=60)
                            text = dpg.add_text(default_value="REPROVADO")
                            dpg.bind_item_font(item=text, font=score_font_result)
                    
                        
with dpg.item_handler_registry() as registry:
    dpg.add_item_clicked_handler(button=dpg.mvMouseButton_Right,callback=plot_mouse_click)
dpg.bind_item_handler_registry(plot,registry)

                 
                                                      
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
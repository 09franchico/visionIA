import dearpygui.dearpygui as dpg
from theme_settings.theme_registry import *
import json
import os
import cv2 as cv2
import numpy as np


class ExampleApp:
    
    def __init__(self):
        self.circle_data = []
        self.image_path = None
        self.setup()
        
    
    def setup(self):
        
        dpg.create_context()
        self.theme_manager = ThemeManager()
        self.theme_manager.font()
        
        dpg.create_viewport(title='VISONIA', width=1200, height=800)
        dpg.set_viewport_max_height(800)
        dpg.set_viewport_max_width(1200)
        dpg.bind_theme(self.theme_manager.global_theme)
        dpg.bind_font(self.theme_manager.regular_font)
        
        self.create_window()
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Primary Window", True)
        dpg.start_dearpygui()
        dpg.destroy_context()


    def create_window(self):
            
        with dpg.window(tag="Primary Window") as app:
    
            with dpg.child_window(height=90, autosize_x=True):
                    dpg.add_spacer(height=20)
                    with dpg.group(horizontal=True):
                        dpg.add_spacer(width=10)
                        score = dpg.add_text(default_value="APRENDENDO DEARPYGUI")
                        dpg.bind_item_font(item=score, font=self.theme_manager.score_font)
                    
                        
            with dpg.group(horizontal=True):
                
                    with dpg.child_window(width=800,border=True):
                        
                        with dpg.tab_bar():
                            
                            with dpg.tab(label="Plotar imagem",tag="tab1_plot_image"):
                                with dpg.plot(query=True,width=-1,height=-1,crosshairs=True,tag="plot_imagem",no_box_select=True,no_menus=True) as plot:
                                        dpg.add_plot_legend()
                                        dpg.add_plot_axis(dpg.mvXAxis, label="",tag="x_axis")
                                        dpg.add_plot_axis(dpg.mvYAxis, label="", tag="y_axis")
                                        dpg.add_draw_node(parent=plot,tag="draw_node")
                                        
                            with dpg.tab(label="Desenhar imagem",tag="tab2_plot_image"):
                                 with dpg.node_editor(callback=self.link_callback, delink_callback=self.delink_callback,tag="node_id"):
                                     
                                    with dpg.node(label="Francisco"):
                                        with dpg.node_attribute(label="Node A1"):
                                            dpg.add_input_float(label="F1", width=150)

                                        with dpg.node_attribute(label="Node A2", attribute_type=dpg.mvNode_Attr_Output):
                                            dpg.add_input_float(label="F2", width=150)

                                    with dpg.node(label="Santos"):
                                        with dpg.node_attribute(label="Node A3"):
                                            dpg.add_input_float(label="F3", width=200)

                                        with dpg.node_attribute(label="Node A4", attribute_type=dpg.mvNode_Attr_Output):
                                            dpg.add_input_float(label="F4", width=200)
                                            
                    
                    with dpg.child_window(autosize_x=True, autosize_y=True):
                        with dpg.group():
                            with dpg.child_window(height=380,border=False):
                                with dpg.group():
                                    dpg.add_spacer(width=10)
                                    dpg.add_button(label="ANEXA IMAGEM",width=150,height=30,callback=lambda: dpg.show_item("file_dialog_id"))
                                    dpg.add_spacer(width=20)
                                    dpg.add_button(label="START",width=150,height=30,callback=self.on_save)
                                    dpg.add_spacer(width=20)
                                    dpg.add_button(label="DELETE",width=150,height=30,callback=self.delete_item_circle)
                                    dpg.add_button(label="MUDAR COR",width=150,height=30,callback=self.set_cor)
                                    dpg.add_button(label="ANEXAR JSON",width=150,height=30,callback=lambda: dpg.show_item("file_json_id"))
                                    dpg.add_button(label="NODE",width=150,height=30,callback=self.mostrar_node)
                                    
                            with dpg.child_window(height=265) as aprov:
                                dpg.add_spacer(height=110)
                                with dpg.group(horizontal=True):
                                    dpg.add_spacer(width=60)
                                    text = dpg.add_text(default_value="REPROVADO")
                                    dpg.bind_item_font(item=text, font=self.theme_manager.score_font_result)
                                    dpg.bind_item_theme(aprov, self.theme_manager.item_theme_result) 
                                    
        #MODAL de arquivos do sistema                          
        with dpg.file_dialog(directory_selector=False, show=False, callback=self.find_file_system, id="file_dialog_id", width=700 ,height=400):
            dpg.add_file_extension(".bmp")
            dpg.add_file_extension(".jpeg", color=(150, 255, 150, 255))
            dpg.add_file_extension("Source files (*.cpp *.h *.hpp){.cpp,.h,.hpp}", color=(0, 255, 255, 255))
            dpg.add_file_extension(".h", color=(255, 0, 255, 255), custom_text="[header]")
            dpg.add_file_extension(".py", color=(0, 255, 0, 255), custom_text="[Python]")
            
        #MODAL JSON                       
        with dpg.file_dialog(directory_selector=False, show=False, callback=self.set_json_image, id="file_json_id", width=700 ,height=400):
            dpg.add_file_extension(".json")
        
            
        
        with dpg.item_handler_registry() as registry:
             dpg.add_item_clicked_handler(button=dpg.mvMouseButton_Right,callback=self.plot_mouse_click)
        dpg.bind_item_handler_registry(plot,registry)
        
        
    def mostrar_node(self):
        teste = dpg.get_item_configuration("node_id")
        print(teste)
        
    def link_callback(self,sender, app_data):
        dpg.add_node_link(app_data[0], app_data[1], parent=sender)
      
    def delink_callback(self,sender, app_data):
        dpg.delete_item(app_data)
            


    def set_json_image(self,sender, app_data, user_data):
        
        try:
            file_path = app_data["file_path_name"]
        
            if not file_path:
                print("Nenhum arquivo JSON selecionado")
                return
            with open(file_path, 'r') as file:
                data = json.load(file)
            dpg.delete_item("draw_node", children_only=True)
            
            self.circle_data = data
            for item in data:
                if 'circle' in item.get('tag', ''):
                    x, y = item['center']
                    radius = item['radius']
                    dpg.draw_circle(center=[x, y], radius=radius, color=(255, 255, 0), parent="draw_node", thickness=2, tag=item['tag'])
        except Exception as e:
            print("Erro em set_json_imagem: ",e)
        
        

            
    def on_save(self, sender, app_data):
        # Salva os dados dos círculos
        file_path = os.path.join(os.getcwd(), 'circle_data.json')
        with open(file_path, 'w') as file:
            json.dump(self.circle_data, file, indent=4)
        
        img = cv2.imread(self.image_path)
        img_height, img_width, _ = img.shape
        
        
        print(f"Imagem original - Largura: {img_width}, Altura: {img_height}")
        
        for i, data in enumerate(self.circle_data):
            x = int(data['center'][0])
            y = int(data['center'][1])
            radius = int(data['radius'])
            
                
            print(f"Posicao x: {x}")
            print(f"Posicao y: {y}")
            print(f"Raio: {radius}")
            
            # Definir os limites do recorte
            x_start = max(0, x - radius)
            x_end = min(img_width, x + radius)
            y_start = max(0, y - radius)
            y_end = min(img_height, y + radius)
            
            # Recortar a imagem na região especificada
            cropped_img = img[y_start:y_end, x_start:x_end]
            
            # Salvar a imagem recortada
            cropped_image_path = os.path.join(os.getcwd(), f'cropped_circle_{i}.png')
            cv2.imwrite(cropped_image_path, cropped_img)
            
            print(f"Imagem recortada salva em: {cropped_image_path}")
            
        

        
        
    def set_image_plot(self,path):
        self.image_path = path
        try:  
            if dpg.does_item_exist(""):
                dpg.delete_item("imagem_id")   
            if dpg.does_item_exist("y_axis_image_id"):
               return
            else:
                width, height, channels, data = dpg.load_image(path)
                with dpg.texture_registry():
                    dpg.add_dynamic_texture(width, height, data, tag="imagem_id")
                dpg.add_image_series("imagem_id", [0, 0], [width, height], parent="y_axis", tag="y_axis_image_id")  
        except Exception as e:
             print(f"Erro set_image: {e}")  
        
    
    def find_file_system(self,sender, app_data, user_data):
        path = app_data["file_path_name"]
        self.set_image_plot(path)
    
        
    def plot_mouse_click(self,sender, app_data, user_data):
        x, y = dpg.get_plot_mouse_pos()
        tag = f"circle_{len(self.circle_data)}" 
        radius = 4608 * 0.01
        dpg.draw_circle(center=[x, y], radius=radius, color=(219, 73, 255), parent="draw_node",thickness=2,tag=tag)
        self.circle_data.append({"tag": tag, "center": (x, y), "radius": radius})
        
        
    def delete_item_circle(self):
        self.circle_data.clear()
        dpg.delete_item("draw_node",children_only=True)
    
    
    def set_cor(self):
        for data in self.circle_data:
            dpg.configure_item(data["tag"], color=(255,0,0))
        



if __name__ == "__main__":
    ExampleApp()

import dearpygui.dearpygui as dpg
import cv2 as cv
import numpy as np

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=600, height=800)
dpg.setup_dearpygui()

vid = cv.VideoCapture(0)

if not vid.isOpened():
    print("Erro ao abrir a câmera.")
    dpg.destroy_context()
    exit()
    
ret, frame = vid.read()


data = np.flip(frame, 2)  # because the camera data comes in as BGR and we need RGB
data = data.ravel()  # flatten camera data to a 1 d stricture
data = np.asarray(data, dtype='f')  # change data type to 32bit floats
texture_data = np.true_divide(data, 255.0)  # normalize image data to prepare for GPU



with dpg.texture_registry(show=True):
    dpg.add_raw_texture(frame.shape[1], frame.shape[0], texture_data, tag="texture_tag", format=dpg.mvFormat_Float_rgb)

with dpg.window(label="Example Window"):
    dpg.add_text("Hello, world")
    dpg.add_image("texture_tag")

dpg.show_metrics()
dpg.show_viewport()

while dpg.is_dearpygui_running():

    # updating the texture in a while loop the frame rate will be limited to the camera frame rate.
    # commenting out the "ret, frame = vid.read()" line will show the full speed that operations and updating a texture can run at
    
    ret, frame = vid.read()
    data = np.flip(frame, 2)
    data = data.ravel()
    data = np.asarray(data, dtype='f')
    texture_data = np.true_divide(data, 255.0)
    dpg.set_value("texture_tag", texture_data)

    # to compare to the base example in the open cv tutorials uncomment below
    #cv.imshow('frame', frame)
    dpg.render_dearpygui_frame()

vid.release()

dpg.destroy_context()
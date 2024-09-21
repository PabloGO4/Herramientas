import os 
from pywinauto import Desktop
from pywinauto.keyboard import send_keys
class Word():
    def save(nombre_doc): 
        
        access = True
        while access:
            try:
                print("abrir word")
                app = Desktop(backend="uia").window(title_re=".*Word")
                # Seleccionar la ventana principal de Word
                app.set_focus()
                send_keys('{F12}')
                send_keys(nombre_doc)
                send_keys('^L')
                ruta = os.path.join(os.path.join(os.environ['USERPROFILE']), 'downloads')
                send_keys(ruta)

                for i in range(4):
                    send_keys('{ENTER}')
                app.close()
                access = False
                return  os.path.join(ruta, nombre_doc)
            except Exception as a:
                access = True 
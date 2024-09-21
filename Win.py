import re
import time
import unicodedata
import pywinauto
import pyautogui
from pywinauto import Desktop, application, mouse
from pywinauto.application import Application
from pywinauto.timings import wait_until


_TIME_OUT_FIND_WINDOW = 30
_TIME_TO_FIND = 3
_SECS_BETWEEN_KEY = 0.2

class Win:

    def __init__(self, exePath, windowName=None):

        if windowName:
            self._window = Desktop(backend="uia").window(title=windowName)
            self._app = Application(backend='uia').connect(path=exePath, visible_only=False)

        else:
            self._app = Application(backend='uia').start(exePath)
            self._window = None

        self._specialCharacters = [ '~' ]

    def startWindow(self, name):

        self._window = Desktop(backend="uia")[name] 
        window = self.__findWindowByName(self._app, name)
        
        return window
    
    @staticmethod
    def __findWindowByName(autoApp, name):
        funcFindWindow = lambda: pywinauto.findwindows.find_windows(title=name)[0]
        dialog = pywinauto.timings.wait_until_passes(_TIME_OUT_FIND_WINDOW, _TIME_TO_FIND, funcFindWindow)
        window = autoApp.window(handle=dialog, top_level_only=False)
        window.set_focus()
        
        return window
    

    @staticmethod
    def findWindow(self, name):
        windowName = []
        windows = Desktop(backend="uia").windows()
        for w in windows:
            windowName.append(w.window_text())
        for win in windowName:
            if name in win:
                self._window = Desktop(backend='uia')[win]

                return win

    def clickButton(self, windowName, buttonName):
        self._window = self._app.window(title=windowName)
        button = self._window.child_window(title=buttonName, control_type="Button")
        button.click()

        
    def printIdentifiersInWindow(self, window_name):
        self.startWindow(window_name)
        window = Desktop(backend='uia').window(title=window_name)
        window.print_control_identifiers()    


    def clickButtonByButtonClassName(self, window_name, class_name):
        window = pywinauto.findwindows.find_windows(title=window_name)[0]
        button = window.child_window(class_name=class_name, control_type="Button")

        if button.exists():
            button.click()
        else:
            raise pywinauto.ElementNotFoundError(f"Button with class name '{class_name}' not found")

    def isWindowOpenByTitle(self,window_title):
        try:
            # Check if any window with the title exists
            windows = pywinauto.findwindows.find_windows(title=window_title)
            for window in windows:
                if window.is_active:
                    return True  # Found an active window with the title

            return False  # No active window found with the title

        except pywinauto.ElementNotFoundError:
            return False  # No window with the title found

    def clickButtonByWindowClass(self, windowClass, buttonName):
        try:
            handle = pywinauto.findwindows.find_windows(class_name=windowClass)[0]
            self._window = self._app.window(handle=handle, top_level_only=False)
            self._window.set_focus()
            button = self._window.child_window(title=buttonName, control_type="Button")
            button.click()
            return True
        except Exception as e:
            return False

    def writeText(self, text):

        for sc in self._specialCharacters:
            if sc in text:
                text = text.replace(sc, '{' + sc +'}')

        self._window.type_keys(text, with_spaces=True)

    def pressTab(self):
        self._window.type_keys('{TAB}')

    def pressEnter(self):
        self._window.type_keys('{ENTER}')
    
    def pressAlt(self):
        self._window.type_keys('%')

    def pressDown(self):
        self._window.type_keys('{DOWN}')

    def pressDelete(self):
        self._window.type_keys('{BACKSPACE}')

    def pressLeft(self):
        self._window.type_keys('{LEFT}')    

    def clickTextElement(self, text):
        try:
            self._window[text].click_input()
        except Exception as e:
            print('Excepcion click text element', e)

    def getElementByLevels(self, levels):
        element = self._window

        for level in levels:
            element = element.children()[level]

        return element
    
    def existElement(self, elementName):
        
        exists = False
        children = self._window.children()
        # children = self._window.wrapper_object().children()

        for child in children:
            if elementName in str(child):
                exists = True

        return exists

    def writeTextByAutomationId(self, window, autoId, text):
        self._window = Desktop(backend="uia")[window] 
        self._window.window(auto_id=autoId).type_keys(text, with_spaces = True)

    def clickByAutomationId(self, window, autoId):
        self._window = Desktop(backend="uia")[window] 
        self._window.window(auto_id=autoId).click_input()

    def clearTextByAutomationId(self, window, autoId):
        self._window = Desktop(backend="uia")[window]
        self._window.window(auto_id=autoId).type_keys('^a')
        self._window.window(auto_id=autoId).type_keys('{BACKSPACE}')

    def sendKeysWithSpace(self, text):
        # self._window.type_keys('^A')
        # self._window.type_keys('{BACKSPACE}')
        self._window.send_keys(text, with_spaces=True)

    def writeTextByLevelsWithSpaces(self, text, levels):
        win = self._window

        for level in levels:
            win = win.children()[level]

        # win.type_keys('^A')
        # win.type_keys('{BACKSPACE}')

        words = text.split(" ")
        for word in words:
            win.type_keys(word)
            if word != words[-1]:
                win.type_keys('{SPACE}')

        return win

    def clickElementByLevels(self, levels):
        win = self._window

        for level in levels:
            win = win.children()[level]

        win.click_input()

        return win
    

    def clickElementByCoordinates(self, x, y):
        mouse.click(button='left', coords=(x, y))

    def findWindowByClass(self, className):
        accesed = True
        while accesed:
            try:
                handle = pywinauto.findwindows.find_windows(class_name=className)[0]
                self._window = self._app.window(handle=handle, top_level_only=False)
                self._window.set_focus()

                name = self._window.window_text()
                accesed = False
                return name
            except Exception as a:
                accesed = True
                print("warning al acceder a la ventana")        
    @staticmethod
    def allWondowsOpen():
        windows = Desktop(backend="uia").windows()
        for window in windows:
            print(window.window_text()) 
    
    def printControlIdentifiers(self, name):
        """Printa por consola los identificadores de la ventana que le pasamos por parametro"""

        self._window = Desktop(backend="uia")[name] 
        window = self.__findWindowByName(self._app, name)
        
        print(window.print_control_identifiers())
    
    @staticmethod
    def buscar(ventana, name):
        ventana.print_control_identifiers(filename=f'{name}.txt')
        child_windows = ventana.children()
        index = 0
        for child_window in child_windows:
                
            if index > 0 :        
                time.sleep(1)
                print(index)
                print(child_window.window_text())
                print(child_window.control_id())
                rectangulo = child_window.rectangle()
                posicion = rectangulo.mid_point()
                pyautogui.moveTo(posicion.x, posicion.y)
                #pyautogui.click(button='right')
            index+=1   
    
    @staticmethod
    def match_window(self, name):
        title_pattern = re.compile(f"{name}.*")

        desktop = Desktop(backend="win32")
        found_window = None
        for win in desktop.windows():
            if title_pattern.match(win.window_text()):
                win.set_focus()
                window_text = win.window_text()
                normalized_text = unicodedata.normalize('NFC', window_text)
                return normalized_text

        return None
    
    @staticmethod
    def check_checkbox(checkbox):
            if checkbox.get_toggle_state() != 1:
                checkbox.click_input()
    
    @staticmethod
    def uncheck_checkbox(checkbox):
        if checkbox.get_toggle_state() == 1:
            checkbox.click_input()

    @staticmethod
    def check_checkbox_win32(checkbox):
        if checkbox.get_check_state() != 1:
            checkbox.click_input()

    @staticmethod
    def uncheck_checkbox_win32(checkbox):
        if checkbox.get_check_state() == 1:
            checkbox.click_input()
    
    def clickMenuItem(self, name):
        self._window.child_window(title=name, control_type="MenuItem").click_input()



    def startWindowByBestMatch(self, name):
     
        window = Desktop(backend="uia").window(best_match = name)
        self._window = window
        self._window.set_focus()
        return window
        

        
    
    @staticmethod
    def waitTillWindowOpens(nameByBestMatch,timeToWait):
        notExistWindow = True
        count = 0
        while notExistWindow:
            if count <= timeToWait:
                try:
                    time.sleep(1)
                    Desktop(backend="uia").window(best_match=nameByBestMatch).set_focus()
                    notExistWindow = False
                except:
                   
                    count += 1


    @staticmethod
    def waitTillWindowOpensby(by, name,timeToWait):
        notExistWindow = True
        count = 0
        while notExistWindow:
            if count <= timeToWait:
                try:
                    time.sleep(1)
                    
                    Desktop(backend="uia").window(by = name).set_focus()
                    notExistWindow = False
                except:
                    count += 1


   
    def waitTillObjectAppears(self,by,description,timeToWait):
        notExistWindow = True
        count = 0
        while notExistWindow:
            if count <= timeToWait:
                try:
                    time.sleep(1)
                    self._window.child_window(by = description)
                    notExistWindow = False
                except:
                    count += 1

    @staticmethod
    def findWindowByBestMatch(name):
        windows = Desktop(backend='uia').windows()

        for win in windows:

            if name in win.get_properties()['texts'][0]:

                return win.window_text()
            


    @staticmethod
    def waitWindowToOpen(name, timeToWait):
        
        exit = False
        count = 0
        while not exit:
            windows = Desktop(backend='uia').windows()
            for i in windows:
                
                if count <= timeToWait:
                    
                    if name in i.get_properties()['texts'][0]:
                        exit = True
                        return i.window_text()
                    else:
                        
                        count += 1
                else:
                    exit = True
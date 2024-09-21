import glob
import os
import shutil
import time

from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from Herramientas.OCR import OCR

from Herramientas.Win import Win


class UiPathAssistant:
    
    @staticmethod
    def login(exePath, user, password):
        logger.info('Iniciando sesión en UiPath Assistant')
        
        win = Win(exePath)
        win.startWindow('UiPath Assistant')
        time.sleep(10)

        if win.existElement('Inicie sesión en su cuenta'):
            win.clickTextElement('Iniciar sesión')
            time.sleep(3)

            chromeWin = win.findWindow('Google Chrome')
            # win.startWindow(chromeWin)

            win.pressTab()
            win.writeText(password)
            time.sleep(2)
            win.clickTextElement('Sign In')
            time.sleep(5)

        win.startWindow('UiPath Assistant')
        time.sleep(3)

        return win
    
    @staticmethod
    def searchRobot(win, robotName):
        logger.info(f'Buscando robot {robotName}')
        
        time.sleep(1)
        win.startWindow('UiPath Assistant')
        time.sleep(3)
        win.writeTextByAutomationId('UiPath Assistant', 'mat-input-0', robotName)
        time.sleep(3)
        
        win.clickTextElement(robotName)
        time.sleep(3)

    @staticmethod
    def executeRobot(win, robotName):
        logger.info(f'Ejecutando robot {robotName}')

        win.startWindow('UiPath Assistant')
        time.sleep(1)

        win.clickTextElement('Iniciar')

        finished = False
        while(not finished):
            if win.existElement('Completado'):
                finished = True

        # runtime = win.getElementByLevels([0,13]).element_info.name

        objects = win.getElementByLevels([0]).children()
        for idx, child in enumerate(objects):
            if 'Estado' in child.element_info.name:
                runtime = objects[idx+1].element_info.name

            if 'Instalando el paquete' in child.element_info.name:
                startDate = child.element_info.name.split('...')[1].replace('[', '').replace(']', '').strip()

            if 'Completado' in child.element_info.name:
                finishDate = child.element_info.name.split('Completado')[1].split(': ')[0].replace('[', '').replace(']', '').strip()

        # ocr = OCR()
        # text = ocr.extractTextFromScreenshot()

        # for line in text:
        #     if 'Estado (' in line:
        #         status = line.split('(')[1].split(')')[0].strip()
        #         break
        status = None

        time.sleep(3)
        win.clickTextElement('Cerrar detalles de automatización')
        time.sleep(3)
        win.clickTextElement('Cerrar')


        return status, startDate, finishDate, runtime


    @staticmethod
    def logout(win):
        logger.info('Cerrando sesión en UiPath Assistant')

        win.clickTextElement('LR')
        time.sleep(2)
        win.clickTextElement('Cerrar sesión')
        time.sleep(3)

        if win.existElement('¿Cerrar sesión'):
            win.clickTextElement('Sí')
            time.sleep(3)

            chromeWin = win.findWindow('Google Chrome')
            win.clickTextElement('Log out')
            time.sleep(3)






        

        
















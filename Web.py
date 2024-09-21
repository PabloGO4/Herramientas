import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager



class Web:

    def __init__(self, default_download_folder = os.path.join(os.path.join(os.environ['USERPROFILE']), 'downloads')):
        
        chromeProfile = webdriver.ChromeOptions()
        chromeProfile.add_argument("--start-maximized")
        chromeProfile.add_experimental_option('excludeSwitches', ['enable-logging'])
        

        self._prefs = {   'download.default_directory' : default_download_folder,
                    'profile.default_content_setting_values.automatic_downloads': 1,
                    'download.prompt_for_download': False,
                    "plugins.always_open_pdf_externally": True,
                    'excludeSwitches': ['enable-logging'],
                    "default_search_provider_data":{"template_url_data":{"alternate_urls":[],"choice_location":0,"contextual_search_url":"","created_by_policy":0,"created_from_play_api":'false',"date_created":"0","doodle_url":"","enforced_by_policy":'false',"favicon_url":"https://duckduckgo.com/favicon.ico","featured_by_policy":'false',"id":"5","image_search_branding_label":"","image_translate_source_language_param_key":"","image_translate_target_language_param_key":"","image_translate_url":"","image_url":"","image_url_post_params":"","input_encodings":["UTF-8"],"is_active":0,"keyword":"duckduckgo.com","last_modified":"13366453669908977","last_visited":"0","logo_url":"","new_tab_url":"https://duckduckgo.com/chrome_newtab","originating_url":"","preconnect_to_search_url":'false',"prefetch_likely_navigations":'false',"prepopulate_id":92,"safe_for_autoreplace":'true',"search_intent_params":[],"search_url_post_params":"","short_name":"DuckDuckGo","side_image_search_param":"","side_search_param":"","starter_pack_id":0,"suggestions_url":"https://duckduckgo.com/ac/?q={searchTerms}&type=list","suggestions_url_post_params":"","synced_guid":"485bf7d3-0215-45af-87dc-538868000092","url":"https://duckduckgo.com/?q={searchTerms}","usage_count":0}}

        
                }
       
        chromeProfile.add_experimental_option("prefs", self._prefs)
        service = Service(executable_path=ChromeDriverManager().install())
        self._driver = webdriver.Chrome(options=chromeProfile)  # fallo en service: self._driver = webdriver.Chrome(service=service, options=chromeProfile)
        

    def __getDownloadPath(self):
        """Returns the default downloads path for linux or windows"""
        if os.name == 'nt':
            import winreg
            sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                location = winreg.QueryValueEx(key, downloads_guid)[0]
            return location
        else:
            return os.path.join(os.path.expanduser('~'), 'downloads')
    
    def open(self, url):
        self._driver.get(url)

        time.sleep(2)

    def connectToBrowser(self):
        url = self._driver.command_executor._url
        sessionId = self._driver.session_id

        options = Options()
        cloud_options = {}
        options.set_capability('cloud:options', cloud_options)

        self._driver = webdriver.Remote(command_executor=url, options=options)
        # self._driver.close()   # this prevents the dummy browser
        self._driver.session_id = sessionId

    def writeTextById(self, id, text):
        element = self._driver.find_element('id', id)
        element.send_keys(text)

        time.sleep(1)

    def writeTextByName(self, name, text):
        element = self._driver.find_element('name', name)
        element.send_keys(text)

        time.sleep(1)

    def clickElementByName(self, elementName, log=False):
        element = self._driver.find_element('name', elementName)
        if log:
                print(f'antes Clicked 1 ')

        element.click()
        if log:
                print(f'despues Clicked 1 ')
        time.sleep(1)

    def clickElementById(self, id):
        element = self._driver.find_element('id', id)
        element.click()

        time.sleep(1)

    def getElementByAttribute(self, attr, value):

        strXPath = f'//*[@{attr}="{value}"]'
        element = self._driver.find_element('xpath', strXPath)

        time.sleep(1)

        return element
    
    def getChildrenByTag(self, element, tag):

        return element.find_elements(By.TAG_NAME, tag)
    
    def clickElementByAttribute(self, attr, value):

        strXPath = f'//*[@{attr}="{value}"]'
        element = self._driver.find_element('xpath', strXPath)
        element.click()

        time.sleep(1)
    
    def clickElementByXPath(self, strXPath):

        element = self._driver.find_element('xpath', strXPath)
        element.click()

    def getElementByXPath(self, strXPath):

        element = self._driver.find_element('xpath', strXPath)
        return element

    def clickLinkByText(self, text):

        link = self._driver.find_element(By.LINK_TEXT, text)
        link.click()

    def existsText(self, text):
        return text in self._driver.page_source
    
    def clickElementByText(self, text):
        self._driver.find_element(By.XPATH,f"//*[text()='{text}']").click()



    def selectComboboxByText(self, text):

        strXPath = "//*[contains(text(), '{0}')]".format(text)
        element = self._driver.find_element('xpath', strXPath)
        element.click()

    def selectComboboxByNameAndText(self, name, text):
        select = Select(self._driver.find_element(By.NAME, name))
        select.select_by_visible_text(text)

    def switchWindow(self, indx):
        
        handles = self._driver.window_handles[indx]
        self._driver.switch_to.window(handles)
        self._driver.maximize_window()

    def switchToIFrame(self, pathFrame):
        
        splitNames = pathFrame.split("/")
        
        for name in splitNames:
            self._driver.switch_to.frame(name)

    def endIFrame(self):
        self._driver.switch_to.default_content()

    def clickElementByValue(self,text):
        self._driver.find_element(By.XPATH, f'//input[@value=\"{text}\"]')

    
    





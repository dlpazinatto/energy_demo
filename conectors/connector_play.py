from playwright.sync_api import sync_playwright
import os
import shutil
from cryptography.fernet import Fernet

def decrypt_password(key, encrypted_password):
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password

class ConnectorPlay:
    def __init__(self,key):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context(
            accept_downloads=True
        )
        self.page = self.browser.new_page()
        self.download_dir = os.path.join(os.getcwd(), 'downloads')
        os.makedirs(self.download_dir, exist_ok=True)
        self.downloaded_file_path = None
        self.user = 'dlpazinatto@gmail.com'
        self.key = key
        self.password = decrypt_password(key, 'gAAAAABmz2R-kWyfoO8O9fqA9DFOhZ_eFWjKVKKNtAgIhurLGqc7z0BXRVk3JDCLiT-tJ97stGOTP1Qk_GVB4d2IYWJxpPMR5Q==')
        self.page.on('download', self.handle_download)

    def handle_download(self, download):
        self.downloaded_file_path = os.path.join(self.download_dir, download.suggested_filename)
        download.save_as(self.downloaded_file_path)

    def get_page(self, url):
        print("Getting page: ", url)
        self.page.goto(url)

        self.page.wait_for_load_state('load')

        self.page.wait_for_timeout(5000)

        element_locator = self.page.locator('text="Já tenho o novo cadastro"')
        element_present = element_locator.count()

        if element_present > 0:
            self.page.click('text="Já tenho o novo cadastro"')
            self.page.wait_for_load_state('load')
        else:
            print("Element not found")

        user_input_selector = 'body > celesc-root > div.router-wrapper.no-scroll > celesc-login > div > div > div.main-login-options-wrapper > div.content > form > ui-celesc-input > div > input'
        pass_input_selector = 'body > celesc-root > div.router-wrapper.no-scroll > celesc-login > div > div > div.main-login-options-wrapper > div.content > form > ui-celesc-input-password > div > input'
        
        self.page.locator(user_input_selector).fill(self.user)
        self.page.locator(pass_input_selector).fill(self.password)

        self.page.wait_for_timeout(1000)

        try:
            self.page.locator('button.default[type="button"]').click()
        except:
            self.page.locator('text="Entrar"').click()

        self.page.wait_for_load_state('load')

        self.page.locator('//button[span[text()=" Selecionar unidade "]]').click()

        self.page.wait_for_load_state('load')

        download_button_locator = self.page.locator('button:has-text("2ª via de conta Comprovante de residência")')
        download_button_locator.click()

        self.page.wait_for_timeout(10000)

        if self.downloaded_file_path:
            target_path = os.path.join(os.getcwd(), 'fatura.pdf')
            shutil.move(self.downloaded_file_path, target_path)
            print(f"Arquivo PDF movido para: {target_path}")
        else:
            print("Nenhum arquivo foi baixado.")

        self.page.wait_for_timeout(5000)

        self.browser.close()

    def close(self):
        self.browser.close()

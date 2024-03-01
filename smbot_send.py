import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import os
import dotenv


async def send_meta():
    
    async with async_playwright() as p:
        browser = await p.firefox.launch(
            headless=False
        )
        resultado = Path('resultado_dia.txt')
        with open(resultado, 'r', encoding='utf-8') as file:
            atualização = file.readlines()
        page = await browser.new_page()
        await page.goto('https://www.smsolucoesdigital.com.br/index.html#/bots/bot')
        await page.wait_for_selector('#email')
        await page.locator('#email').fill(os.getenv('SMBOT_USERNAME'))
        await page.locator('#password').fill(os.getenv('SMBOT_PASSWORD'))
        await page.locator('button[ng-click="onLogin()"]').click()
        await page.wait_for_selector('button[ng-click="close()"]')
        await page.locator('button[ng-click="close()"]').click()
        await page.locator('button[ng-click="closeMegaZapNotification()"]').click()
        await page.locator('div[title="Alexandre Ferreira dos Santos"]').click()
        for line in atualização:
            await page.locator('textarea[ng-show="chatInterno.arquivos.length === 0 && !disableChatGrupo()"]').fill(line)
            await page.locator('div[ng-click="enviarMensagem()"]').click()
            await asyncio.sleep(1)
        
     

if __name__ == '__main__':
    dotenv.load_dotenv()
    def init_async():
        asyncio.run(send_meta())
    init_async()
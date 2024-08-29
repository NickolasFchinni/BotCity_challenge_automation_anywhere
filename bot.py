from botcity.web import WebBot, Browser, By
from botcity.web.util import element_as_select
from botcity.maestro import *
import pandas

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()

    bot.headless = False
    bot.browser = Browser.CHROME
    bot.driver_path = r"C:\Users\nickolas.faquini\Documents\python_projects\chromedriver\chromedriver.exe"

    var_challengeUrlPath = "https://pathfinder.automationanywhere.com/challenges/automationanywherelabs-customeronboarding.html?_gl=1*1os70bz*_gcl_au*MTkzOTg1MzgyNC4xNzIxMTUzOTkw*_ga*MTA2MzU3MjcyNS4xNzIxMTUzOTkx*_ga_DG1BTLENXK*MTcyNDg3NjQ1MS42LjAuMTcyNDg3NjQ1My41OC4wLjA."
    var_arrLoginCredentials = ["nulleyson@gmail.com", "Nickolas1001-"]
    var_dtCustomerUnboarding = pandas.read_csv('customer-onboarding-challenge.csv')

    # Abre o site do Automation Anywhere
    bot.browse(var_challengeUrlPath)
    bot.maximize_window()

    var_buttonCookies = bot.find_element('//*[@id="onetrust-accept-btn-handler"]', By.XPATH)
    var_buttonCookies.click()

    var_btnCommunityLogin = bot.find_element('//button[@aria-label="Community login"]', By.XPATH)
    var_btnCommunityLogin.click()

    inserindo_credenciais_para_efetuar_login(bot, var_arrLoginCredentials)

    inserindo_dados_nos_inputs(bot,var_dtCustomerUnboarding)

    bot.wait(10000)
    bot.stop_browser()

    maestro.finish_task(
        task_id=execution.task_id,
        status=AutomationTaskFinishStatus.SUCCESS,
        message="Task Finished OK."
    )

def inserindo_credenciais_para_efetuar_login(bot, credentials):
    # Preencher Login e clicar em next
    var_loginInput = bot.find_element('//*[@placeholder="*Email"]', By.XPATH)
    var_loginInput.send_keys(credentials[0])

    var_buttonNext = bot.find_element('//*[@class="slds-button slds-button_brand button"]', By.XPATH)
    var_buttonNext.click()

    # Preencher senha e efetuar login
    var_passwordInput = bot.find_element('//*[@type="password"]', By.XPATH)
    var_passwordInput.send_keys(credentials[1])

    var_buttonLogin = bot.find_element('//*[@class="slds-button slds-button_brand button"]', By.XPATH)
    var_buttonLogin.click()

def inserindo_dados_nos_inputs(bot, table):
    var_state = element_as_select(bot.find_element("//select[@name='state']", By.XPATH))
    # Loop para buscar e inserir dados
    for _,row in table.iterrows():
        bot.find_element('//input[@name="customerName"]', By.XPATH).send_keys(row['Company Name'])
        bot.find_element('//input[@name="customerID "]', By.XPATH).send_keys(row['Customer ID'])
        bot.find_element('//input[@name="contact "]', By.XPATH).send_keys(row['Primary Contact'])
        bot.find_element('//input[@name="street "]', By.XPATH).send_keys(row['Street Address'])
        bot.find_element('//input[@name="city "]', By.XPATH).send_keys(row['City'])
        bot.find_element('//input[@name="zip "]', By.XPATH).send_keys(row['Zip'])
        bot.find_element('//input[@name="email"]', By.XPATH).send_keys(row['Email Address'])
        var_state.select_by_value(row['State'])

        if row['Offers Discounts'] == "YES":
            bot.find_element('//input[@id="activeDiscountYes"]', By.XPATH).click()  
        elif row['Offers Discounts'] == "NO":
            bot.find_element('//input[@id="activeDiscountNo"]', By.XPATH).click()

        if row['Non-Disclosure On File'] == "YES":
            bot.find_element('//input[@id="NDA"]', By.XPATH).click()
        
        var_btnRegister = bot.find_element('//button[@id="submit_button"]', By.XPATH)
        var_btnRegister.click()

def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()

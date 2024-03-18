import config
import time
import logging
import datetime
from SGTAMProdTask import SGTAMProd
from config import SGTAM_log_config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import cv2


if __name__ == '__main__':
    # setup logging
    logging.basicConfig(
      filename= f"log\{datetime.datetime.now().strftime('%Y%m%d%H%M')}_EPOPEScreenshots.log",
      format='%(asctime)s %(levelname)s %(message)s',
      level=logging.INFO
    )

    s = SGTAMProd()
    config.SGTAM_log_config['statusFlag'], config.SGTAM_log_config['logID']  = s.insert_tlog(**config.SGTAM_log_config)

    logging.info("EPO PE Screenshots Started")

    #Your script here
    try: 
        #EPO Login Url
        EPO_login_url = 'http://10.86.137.60/public/#/actions/login'

        # set up chrome driver
        logging.info("Setting up the selenium driver")
        chrome_options = Options()
        #chrome_options.add_argument("--headless") #to run Chrome in background, comment it if want to see chrome opened,
        
        #driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options) #Always update chrome driver if outdated
        
        ## temporary solution for chrome driver
        #driver = webdriver.Chrome(executable_path=r"D:\05. Data Production\Project\EPOPEScreenshots\temp_storage_ChromeDrivers\chromedriver-win64\chromedriver.exe", options=chrome_options)
        driver = webdriver.Chrome(executable_path=r"D:\05. Data Production\Project\EPOPEScreenshots\temp_storage_ChromeDrivers\chromedriver-win64_121\chromedriver.exe")


        driver.maximize_window() #Set Chrome to fullscreen
        
        logging.info("Go to EPO login page")
        driver.get(EPO_login_url) #navigate to EPO login page
        
        logging.info("Wait max 10s until 'username' field section is fully loaded/detected.")
        #Wait max 10s until the username part is loaded on chrome, else throw exception
        wait = WebDriverWait(driver, 10)
        wait_element_username = wait.until(EC.visibility_of_element_located((By.ID,"username")))
        logging.info("username field is detected")
        
        logging.info("Send keys to login EPO")
        #send username and password to the fields for login
        username_input = driver.find_element(By.ID, 'username')
        username_input.send_keys("snchat")
        username_password = driver.find_element(By.ID, 'password')
        username_password.send_keys("Summer@0705")
        username_btn = driver.find_element(By.XPATH, '//*[@id="login"]/div[3]/div/button').click()

        #Go to different EPO sections and take screenshots
        time.sleep(2)
        logging.info("Navigate to related EPO sections to screenshot")
        for i in config.GENERAL_CHECK_URL_LIST:
            if(i[1]=='SgpExportFinal'):#if is SgpExportFinal, will need to wait for some element to be fully loaded first then set the driver to scroll to that element before screenshot
                logging.info(f"Navigate to {i[1]}")
                driver.get(i[0])
                logging.info("Wait max 10s for SgpExportFinal text to be detected else throw timedout exception.")
                wait_element_username = wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div[17]/div/div[1]/h5')))
                logging.info("Element found.")
                element_SgpExportFinal = driver.find_element(By.XPATH,'/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div[17]/div/div[1]/h5')
                driver.execute_script("arguments[0].scrollIntoView();", element_SgpExportFinal)
                logging.info(f"Scrolled down to the text element of {i[1]}")
                time.sleep(2)
                driver.save_screenshot('screenshots/'+i[1]+'.jpg')
                logging.info(f"{i[1]} screenshot saved.")
            else:#if not Sgp ExportFinal, just take screenshot as per normal
                logging.info(f"Navigate to {i[1]}")
                driver.get(i[0])
                time.sleep(2)
                driver.save_screenshot('screenshots/'+i[1]+'.jpg')
                logging.info(f"{i[1]} screenshot saved.")
        
        #This part go to different CPS url and take screenshots
        logging.info(f"Navigate to CPSs sections.")
        for i in config.CPS_URL:
            logging.info(f"Navigate to {i[1]}")
            driver.get(i[0])
            time.sleep(2)
            driver.save_screenshot('screenshots/'+i[1]+'.jpg')
            logging.info(f"{i[1]} screenshot saved.")
        
        logging.info(f"Closing driver.")
        driver.close() #close driver once done
        logging.info(f"Driver closed.")
        logging.info(f"Process done, updating tLog and email settings.")
        
        config.SGTAM_log_config['logMsg'] = "Process ended successfully."
        #Add screenshots to the email body
        screenshots = [
           'screenshots/SgpExportFinal.jpg',
           'screenshots/DnxWorkflow.jpg',
           'screenshots/CpsTree.jpg',
           'screenshots/SgpMasterInGermany.jpg',
           'screenshots/SgpMasterInSgp.jpg',
           'screenshots/SgpMasterForCustomers.jpg',
           'screenshots/SgpMasterFedAuth.jpg',
           'screenshots/SgpMasterInAws.jpg',
           'screenshots/ConnectedDevices.jpg',
           'screenshots/ConnectedDevicesByProvider.jpg',
           'screenshots/CorrelationInformation.jpg',
           'screenshots/BllServer.jpg'
           ]
        finalImage = cv2.imread("screenshots/SgpExportFinal.jpg")
        
        for screenshot in screenshots:
            if(screenshot != 'screenshots/SgpExportFinal.jpg'):
                img = cv2.imread(screenshot)
                finalImage = cv2.vconcat([finalImage,img])
        cv2.imwrite("screenshots/FinalScreenshots.jpg", finalImage, [cv2.IMWRITE_JPEG_QUALITY, 15]) #combine all screenshots vertically and resize to 15% quality
        
        config.email['filename'] = ['screenshots/FinalScreenshots.jpg'] #have to send as array/list, as edited the module to take in array/list instead of str.
        config.email['subject'] = 'EPO PE Screenshots'
        config.email['body'] = 'Please find the screenshots for the daily morning routine EPO check.\n You may need to zoom in to have a better view.\n*This is an auto generated email, do not reply to it.'
        
        
    except Exception as e:
        config.SGTAM_log_config['statusFlag'] = 2
        config.SGTAM_log_config['logMsg'] = "There is/are exception(s), please check."
        config.email['subject'] = "[ERROR] EPO PE Screenshots"
        config.email['body'] = f"{config.SGTAM_log_config['logMsg']}\n{e}\n*This is an auto generated email, do not reply to it."
        logging.error(config.SGTAM_log_config['logMsg'])
        logging.error(e)

    finally:
        if config.SGTAM_log_config['statusFlag'] in [2]:
            s.send_email(**config.email)
            logging.info('Email sent.')
            s.update_tlog(**config.SGTAM_log_config)
            logging.info('SGTAM log updated.')
        else:
            s.send_email(**config.email)
            logging.info('Email sent.')
            s.update_tlog(**config.SGTAM_log_config)
            logging.info('SGTAM log updated.')
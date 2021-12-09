

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import multiprocessing as mp
from multiprocessing import Pool


def get_response(final_html):
    soup = BeautifulSoup(final_html, "html.parser")
    resp = soup.findAll('p')
        
    if len(resp) > 1: 
        resp = [element.get_text() for element in resp]
        response_time = resp[2].split(':')[1].strip('\n') 
        worker_idx = resp[3].split(':')[1].strip() 
        return response_time, worker_idx
    else: 
        return -1, -1 

def execute_process(url): 
    options = Options()
    options.add_argument("--headless")
    ser = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=ser, options=options)

    start = time.time() 
    driver.get(url)

    driver.find_element(By.ID, "upload_proc").send_keys(os.getcwd() + '/sample.jpg')
    button_element = driver.find_element(By.ID, 'submit_proc')
    button_element.click()

    
    WebDriverWait(driver, 100000).until(EC.url_changes(url))
    final_html = driver.page_source
    end = time.time() 
    total_time = end - start
    return final_html, total_time

def con_req_pool(con_req, url_list, success_count, avg_time):

    pool = Pool(processes=con_req)
    ret = pool.map(execute_process, url_list)
    for final_html, total_time in ret:
        avg_time.value += total_time
        response_time, worker_idx = get_response(final_html)
        print('Model Inference time: %s' % response_time)
        print('Assigned Worker: %s' % worker_idx)
        if response_time != -1:
            success_count.value += 1


if __name__ == "__main__":   

    total_req_seq = 3
    con_req = 3
    freq_time = 2
    
    url = "http://pcvm4-3.instageni.colorado.edu:8080/"
    url_list = [url] * con_req
        
    success_count = mp.Value('d', 0.0)
    avg_time = mp.Value('d', 0.0)
    seq = 0
    last_time = time.time() - freq_time

    process_list = []
    for i in range(total_req_seq):
        process_list.append(mp.Process(target=con_req_pool, args=(con_req, url_list, success_count, avg_time, )))

    while seq < total_req_seq:
        p = process_list[seq]
        if time.time() - last_time > freq_time:
            p.start()
            print('new process!')
            last_time = time.time()
            seq += 1
    for p in process_list:
        p.join()

    print('Delay: %.3f' % avg_time.value)
    print('Average Delay: %.3f'%(avg_time.value/(con_req*total_req_seq)))
    print('Sucess Rate: %.3f'%(success_count.value/(con_req*total_req_seq)))



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

def save_title(browser):
    
    print "Starting crawling questions..."
    
    status = browser.find_elements_by_class_name('TopicQuestionsStatsRow')
    question_num = int(status[0].find_element_by_tag_name('strong').text)
    question_url = status[0].get_attribute("href")
    
    print "Detected total question number:", question_num, "under url:", question_url
    
    print "Starting saving questions..."
    
    browser.get(question_url)
    
    # prevent infinite loop, if five times the number stay the same then stop reload
    count = 0
    prev_q_num = 0
    
    while 1:
        all_questions = browser.find_elements_by_class_name('pagedlist_item')
        
        print "Saving",len(all_questions), "questions..."
        
        if len(all_questions) == prev_q_num:
            count = count + 1
        else:
            count = 0
            
        prev_q_num = len(all_questions)
        
        # scrolling down until loading all the page
        if len(all_questions) == question_num or count == 5:
            break
        
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # for emulator to scrolling down
        sleep(0.5)
        
    link_list = [ question.find_elements_by_class_name("question_link")[0].get_attribute('href') for question in all_questions]
    question_list = [ question.find_elements_by_class_name("question_link")[0].text for question in all_questions]      
        
    print "Saving",len(question_list),"questions of total", question_num, "questions."
    print "Finished Crawling!Excited"
    return question_list, link_list

def save_answers(browser,link):
    
    print "Starting crawling answers on url:", link
    
    browser.get(link)

    if browser.find_elements_by_class_name('answer_count') == []:
        print "No answer for this question."
        return ['NA']
    
    answer_num = int(browser.find_elements_by_class_name('answer_count')[0].text.split(' ')[0])
    
    print "Detected total answer number:", answer_num, "under url:", link
    
    print "Starting saving answers..."
    
    # prevent infinite loop, if five times the number stay the same then stop reload
    count = 0
    prev_a_num = 0
    
    while 1:
        all_answers = browser.find_elements_by_class_name('AnswerBase')
        
        print "Saving",len(all_answers), "answers..."
        
        if len(all_answers) == prev_a_num:
            count = count + 1
        else:
            count = 0
            
        prev_a_num = len(all_answers)
        
        # scrolling down until loading all the page
        if len(all_answers) == answer_num or count == 5:
            break
        
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # for emulator to scrolling down
        sleep(0.5)
        
    answer_list = [ answer.find_elements_by_class_name('rendered_qtext')[-1].text for answer in all_answers]
        
    print "Saving",len(answer_list),"answers of total", answer_num, "answers."

    sleep(0.5)

    return answer_list

url = 'https://www.quora.com/topic/Ann-Arbor-MI'

print "Emulate webdriver with phantomJS..."

# binary = FirefoxBinary('path/to/binary')
browser = webdriver.PhantomJS()
browser.get(url)

question_list,link_list = save_title(browser)


#saving data to csv file
import csv
with open('quora_qa.csv', 'wb') as csvfile:
    qawriter = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)

    count = 0

    qawriter.writerow(["Questions","Answers"])
    for i in range(len(link_list)):
        print "########",count
        if count == 10:
            print "restarting browser..."
            browser.quit()
            browser = webdriver.PhantomJS()
            count = 0

        ans_list = save_answers(browser,link_list[i])
        count = count + 1
        sleep(0.1)
        for ans in ans_list:
            qawriter.writerow([unicode(question_list[i]).encode("utf-8"), unicode(ans).encode("utf-8")])

browser.quit()
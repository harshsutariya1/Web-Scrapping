# Data Scraper for Google Forms
# ----------------------------------
# This script retrieves form questions and options from a Google Form.

import requests
from bs4 import BeautifulSoup

def get_quiz_data(google_form_link):
    quiz_data = []
    question_container_tag = {'div':'geS5n'}
    question_tag = {'span':'M7eMe'}
    options_list_tag = {'div':'SG0AAe'}
    option_tag = {'div':'ulDsOb'}
    short_ans_input_tag  = {'div':'Xb9hP'}
    
    try:
        form_url = google_form_link
        response = requests.get(form_url)
        print(f"Status code: {response.status_code}")

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Checking the div classes where questions and options are located.
            questions_containers = soup.find_all('div', class_=question_container_tag['div'])
            print(f"Questions found: {len(questions_containers)}")

            for index, question_container in enumerate(questions_containers):
                try:
                    print(f"\nProcessing question {index + 1}...")
                    
                    # print(question_container.text.__contains__(short_ans_input_tag['div']))
                    # Extract question
                    question:str = question_container.find('span', class_=question_tag['span']).text.strip()
                    if question:
                        print("Question:", question)
                    else:
                        print("Question not found.")
                        continue
                    
                    # Extract list of options
                    options:list[str] = []
                    
                    try:
                        options_div = question_container.find('div', class_=options_list_tag['div']) 
                        if options_div:
                            options_list = options_div.find_all('div', class_=option_tag['div'])
                            if options_list:
                                for option in options_list:
                                    print("Option:", option.text.strip(),)
                                    options.append(option.text.strip())
                                print(options)
                            else:
                                print("Options list not found.")
                        else:
                            print("Options div Not found.")
                    except Exception as error:
                        print("An error occured while getting options:",error)
                            
                    quiz_data.append({
                        'question': question,
                        'options': options
                    })
                
                except Exception as error:
                    print("An error occurred while looping through question container:", error)
                    continue
                
        else:
            print("Failed to retrieve the form. Status code:", response.status_code)

    except Exception as error:
        print("An error occurred:", error)

    return quiz_data


def main():
    google_form_link = 'https:///forms/d/e/1FAIpQLSeRrwWEMf9W2-XHmgWSOaJrn3zZ98QdTbDT7TGhMJKCHZUHOA/viewform?usp=sf_link/'
    # google_form_link = 'https://forms.gle/9G5JXTE3SFDmht6N8'
    if (google_form_link.__contains__('docs.google.com') or google_form_link.__contains__('forms.gle')):
        quizData = get_quiz_data(google_form_link)
    else:
        print("Given URL is not Google form link...")
    
    print('_____________________________________________________________________\n')
    print(quizData)
    print('_____________________________________________________________________\n')



if __name__ == "__main__":
    main()
else:
    print("main function not found")
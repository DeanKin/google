from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

print("🚀 Starting Google Forms automation...")
options = Options()
# Temporarily disable headless mode to see what's happening
# options.add_argument("--headless=new")
print("⚙️  Initializing Chrome driver (visible mode for debugging)...")
driver = webdriver.Chrome(options=options)
driver.maximize_window()  # Make window larger to see form better
print("✓ Chrome driver initialized successfully")
# Initialize Chrome driver (Make sure chromedriver is installed and in path)


try:
    url = "https://docs.google.com/forms/d/e/1FAIpQLSdceHYFsB9rB9-U9lc1Q2o98p11dN97M4yNkAP6ent5DNkAhg/viewform?usp=dialog"
    print("Loading Google Form...")
    driver.get(url)
    print("✓ Form loaded successfully")

    wait = WebDriverWait(driver, 10)

    # 1. Click NEXT button on 1st page
    print("📄 Page 1: Looking for Next button (下一個 or 繼續)...")
    try:
        # Try "下一個" first
        next_button_1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='下一個']")))
    except:
        # If not found, try "繼續"
        next_button_1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='繼續']")))
    next_button_1.click()
    print("✓ Page 1: Next button clicked, moving to page 2")

    time.sleep(2)  # Wait for 2nd page to load

    # 2. On 2nd page: randomly select one answer for each of 5 questions
    # These are demographic questions like Gender, Age, Education, etc.
    print("📄 Page 2: Loading questions...")
    questions_2nd_page = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='listitem']")))
    # Usually, Google Forms groups questions, adjust selector as needed for exact questions
    print(f"📄 Page 2: Found {len(questions_2nd_page)} question elements")

    count_selected = 0
    for i, question in enumerate(questions_2nd_page, 1):
        # Try to get question title/text
        question_title = ""
        try:
            title_element = question.find_element(By.CSS_SELECTOR, "div[role='heading'], .freebirdFormviewerViewItemsItemItemTitle, h2, h3")
            question_title = title_element.text.strip()
        except:
            question_title = f"Question {i}"
        
        print(f"\n📋 Page 2: Processing Question {i}")
        print(f"   Title: {question_title}")
        
        # Find all selectable options for the question
        options = question.find_elements(By.CSS_SELECTOR, "div[role='radio']")
        if not options:
            options = question.find_elements(By.CSS_SELECTOR, "div[role='radio'], div[role='listitem'] div[role='option']")
        if not options:
            options = question.find_elements(By.CSS_SELECTOR, "div[role='option']")
        if not options:
            # Try more generic selectors
            options = question.find_elements(By.CSS_SELECTOR, "label, .freebirdFormviewerViewItemsRadioOption")
            
        if options:
            print(f"   Available options: {len(options)}")
            
            # Get option texts for display
            option_texts = []
            for opt in options:
                try:
                    text = opt.text.strip()
                    if text:
                        option_texts.append(text)
                    else:
                        option_texts.append("(No text)")
                except:
                    option_texts.append("(Unable to read)")
            
            # Randomly select one option
            option_to_select = random.choice(options)
            selected_index = options.index(option_to_select)
            selected_text = option_texts[selected_index] if selected_index < len(option_texts) else "Unknown option"
            
            driver.execute_script("arguments[0].scrollIntoView(true);", option_to_select)
            time.sleep(0.5)  # Small delay to ensure element is ready
            try:
                option_to_select.click()
            except:
                # If regular click fails, try JavaScript click
                driver.execute_script("arguments[0].click();", option_to_select)
            count_selected += 1
            
            print(f"   ✓ Selected: {selected_text}")
            print(f"✓ Page 2: Question {count_selected} completed")
            
            if count_selected == 5:
                break
        else:
            print(f"   ❌ No selectable options found for question {i}")

    print(f"\n✓ Page 2: Completed {count_selected} questions total")
    time.sleep(2)  # Wait for selections to register

    # Click Next button to go to 3rd page
    print("📄 Page 2: Looking for Next button to go to page 3 (下一個 or 繼續)...")
    try:
        # Try "下一個" first
        next_button_2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='下一個']")))
    except:
        # If not found, try "繼續"
        next_button_2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='繼續']")))
    next_button_2.click()
    print("✓ Page 2: Next button clicked, moving to page 3")

    time.sleep(2)  # Wait for 3rd page to load

    # 3. On 3rd page: total 15 questions, for each randomly select 4 or 5 options (checkboxes)
    print("📄 Page 3: Loading questions...")
    questions_3rd_page = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='listitem']")))
    selected_questions = questions_3rd_page[:15]  # Ensure only first 15 questions are handled
    print(f"📄 Page 3: Found {len(questions_3rd_page)} question elements, processing first 15")
    
    for i, question in enumerate(selected_questions, 1):
        # Try to get question title/text
        question_title = ""
        try:
            title_element = question.find_element(By.CSS_SELECTOR, "div[role='heading'], .freebirdFormviewerViewItemsItemItemTitle, h2, h3")
            question_title = title_element.text.strip()
        except:
            question_title = f"Question {i}"
        
        print(f"\n📋 Page 3: Processing Question {i}")
        print(f"   Title: {question_title}")
        
        # Try different selectors for options
        options = question.find_elements(By.CSS_SELECTOR, "div[role='checkbox']")
        question_type = "checkbox"
        
        if not options:
            options = question.find_elements(By.CSS_SELECTOR, "div[role='radio']")
            question_type = "radio"
            
        if not options:
            options = question.find_elements(By.CSS_SELECTOR, "div[role='option']")
            question_type = "option"
            
        if not options:
            # Try more generic selectors
            options = question.find_elements(By.CSS_SELECTOR, "label, .freebirdFormviewerViewItemsRadioOption, .freebirdFormviewerViewItemsCheckboxOption")
            question_type = "generic"
        
        print(f"   Question type detected: {question_type}")
        
        if options:
            print(f"   Available options: {len(options)}")
            
            # Get option texts for display
            option_texts = []
            for opt in options:
                try:
                    text = opt.text.strip()
                    if text:
                        option_texts.append(text)
                    else:
                        option_texts.append("(No text)")
                except:
                    option_texts.append("(Unable to read)")
            
            # Handle selection logic based on question type
            if question_type == "radio":
                # For radio buttons (like Likert scale), we can only select one
                # But if you want 4-5 selections, this might be a different type of question
                print("   ⚠️  Radio button detected - can only select 1 option")
                num_to_select = 1
                options_to_click = [random.choice(options)]
            else:
                # For checkboxes, select based on question number
                if i <= 10:
                    # First 10 questions: select exactly 4 options
                    if len(options) >= 4:
                        num_to_select = 4
                        print(f"   Target selections: {num_to_select} (first 10 questions - fixed at 4)")
                    else:
                        num_to_select = len(options)  # Select all available if less than 4
                        print(f"   Target selections: {num_to_select} (all available, less than 4)")
                else:
                    # Questions 11-15: randomly select 4 or 5 options
                    if len(options) >= 5:
                        num_to_select = random.choice([4, 5])
                    elif len(options) >= 4:
                        num_to_select = 4
                    else:
                        num_to_select = len(options)  # Select all available if less than 4
                    print(f"   Target selections: {num_to_select} (questions 11-15 - random 4 or 5)")
                
                # Filter out options 1, 2, 3 (only select from 4, 5 and higher)
                # Assume options are in order, so exclude first 3 options
                if len(options) > 3:
                    available_options = options[3:]  # Skip first 3 options (1, 2, 3)
                    print(f"   Excluding options 1, 2, 3. Available for selection: {len(available_options)} options")
                else:
                    available_options = options  # If less than 4 options total, use all
                    print(f"   Warning: Less than 4 options total, using all {len(available_options)} options")
                
                # Adjust num_to_select if we don't have enough available options
                if num_to_select > len(available_options):
                    num_to_select = len(available_options)
                    print(f"   Adjusted target selections to: {num_to_select} (based on available options)")
                
                # Randomly select from available options (4, 5, etc.)
                options_to_click = random.sample(available_options, num_to_select)
            
            selected_texts = []
            for j, opt in enumerate(options_to_click):
                driver.execute_script("arguments[0].scrollIntoView(true);", opt)
                time.sleep(0.3)  # Small delay to ensure element is ready
                try:
                    opt.click()
                except:
                    # If regular click fails, try JavaScript click
                    driver.execute_script("arguments[0].click();", opt)
                
                # Get the text of selected option
                selected_index = options.index(opt)  # Find index in original options list
                if selected_index < len(option_texts):
                    selected_texts.append(option_texts[selected_index])
                    # Show which option number was selected (1-based indexing)
                    option_number = selected_index + 1
                    print(f"     → Selected option {option_number}: {option_texts[selected_index]}")
                
                # Small delay between clicks to ensure registration
                time.sleep(0.2)
            
            print(f"   ✓ Selected {len(options_to_click)} out of {len(options)} options:")
            for text in selected_texts:
                print(f"     • {text}")
        else:
            print(f"   ❌ No selectable options found for question {i}")

    print("✓ Page 3: All 15 questions completed")
    
    # Navigate to form elements using TAB keys
    body = driver.find_element(By.TAG_NAME, "body")
    
    # Initial TAB navigation to reach form elements
    for _ in range(12):
        body.send_keys(Keys.TAB)
    
    # Process form questions using TAB and arrow keys
    for _ in range(20):
        # Press TAB twice to move between questions
        body.send_keys(Keys.TAB)
        body.send_keys(Keys.TAB)
        
        # Randomly press RIGHT 3 or 4 times to select options
        presses = random.choice([3, 4])
        for _ in range(presses):
            body.send_keys(Keys.ARROW_RIGHT)
        
        # Small delay to allow the selection to register before next loop
        time.sleep(0.3)
    
    print("✓ Page 3: All 20 questions completed")
    
    # Submit the form
    print("📤 Looking for Submit button...")
    try:
        # Try different submit button texts
        submit_button = None
        submit_texts = ["Submit", "提交", "送出", "確定"]
        
        for submit_text in submit_texts:
            try:
                submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text()='{submit_text}']")))
                print(f"✓ Found Submit button: '{submit_text}'")
                break
            except:
                continue
        
        if not submit_button:
            # Try generic submit button selectors
            submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='button'][aria-label*='submit'], div[role='button'][aria-label*='Submit'], input[type='submit'], button[type='submit']")))
            print("✓ Found Submit button using generic selector")
        
        if submit_button:
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            time.sleep(1)
            submit_button.click()
            print("✅ Form submitted successfully!")
            
            # Wait for confirmation page
            time.sleep(3)
            print("⏳ Waiting for submission confirmation...")
            
        else:
            print("❌ Could not find Submit button")
            
    except Exception as e:
        print(f"❌ Error submitting form: {str(e)}")
        print("📝 Form responses may not have been recorded")

    # Keep the browser open for a while to review
    print("🎉 Form automation completed!")
    print("Waiting 5 seconds before closing...")
    time.sleep(5)

except Exception as e:
    print(f"❌ Error occurred: {str(e)}")
    print("📍 Script execution failed")
finally:
    print("🔚 Closing browser...")
    driver.quit()
    print("✓ Browser closed successfully")

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
    url = "https://docs.google.com/forms/u/1/d/e/1FAIpQLSe_mpKKLm_xmx99IuksKSNWL-wcz6gbNUUg29uTR-aQAAE5pg/viewform?pli=1&pli=1"
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
    body = driver.find_element(By.TAG_NAME, "body")
 body.send_keys(Keys.TAB)
for _ in range(20):
    # Press TAB twice
    body.send_keys(Keys.TAB)
    body.send_keys(Keys.TAB)
    
    # Randomly press RIGHT 3 or 4 times
    presses = random.choice([3, 4])
    for _ in range(presses):
        body.send_keys(Keys.ARROW_RIGHT)

    # Small delay to allow the selection to register before next loop
    time.sleep(0.3)
    print("✓ Page 3: All 15 questions completed")
    
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
            time.sleep(5)
            print("⏳ Waiting for submission confirmation...")
            
        else:
            print("❌ Could not find Submit button")
            
    except Exception as e:
        print(f"❌ Error submitting form: {str(e)}")
        print("📝 Form responses may not have been recorded")

    # Keep the browser open for a while to review
    print("🎉 Form automation completed!")
    print("Waiting 5 seconds before closing...")
    time.sleep(1)

except Exception as e:
    print(f"❌ Error occurred: {str(e)}")
    print("📍 Script execution failed")
finally:
    print("🔚 Closing browser...")
    driver.quit()
    print("✓ Browser closed successfully")


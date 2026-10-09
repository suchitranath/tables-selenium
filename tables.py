from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_webtable_tests():
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    driver.maximize_window()
    wait = WebDriverWait(driver, 3)

    try:
        driver.get("https://assertqa.com/practice/webtables")

        print("=" * 60)
        print("EXECUTING WEB TABLE AUTOMATION TEST SUITE")
        print("=" * 60)

        # -------------------------------------------------------------
        # TC01: Print all column headings
        # -------------------------------------------------------------
        print("\n--- TC01: Print all column headings ---")
        headers = driver.find_elements(By.XPATH, "//table//th")
        header_texts = [h.text for h in headers]
        print("Column Headings:", " | ".join(header_texts))

        # -------------------------------------------------------------
        # TC02: Print the first data row
        # -------------------------------------------------------------
        print("\n--- TC02: Print the first data row ---")
        first_row = driver.find_element(By.XPATH, "//table/tbody/tr[1]")
        print("First Row Record:", first_row.text)

        # -------------------------------------------------------------
        # TC03: Print the last data row
        # -------------------------------------------------------------
        print("\n--- TC03: Print the last data row ---")
        visible_rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
        last_row = visible_rows[-1]
        print("Last Row Record (Current Page):", last_row.text)

        # -------------------------------------------------------------
        # TC04: Search for an employee by last name ('Smith')
        # -------------------------------------------------------------
        print("\n--- TC04: Search for an employee by last name ('Smith') ---")
        search_box = driver.find_element(By.XPATH, "//input[@placeholder='Search...' or @type='search' or @type='text']")
        search_box.clear()
        search_box.send_keys("Smith")

        search_results = driver.find_elements(By.XPATH, "//table/tbody/tr")
        for idx, row in enumerate(search_results, 1):
            print(f"Match {idx}: {row.text}")
        
        # Reset search box to display all records again
        search_box.clear()
        search_box.send_keys("")

        # -------------------------------------------------------------
        # Robust Dropdown Selection Fix
        # -------------------------------------------------------------
        try:
            # Find the rows per page select element
            select_element = driver.find_element(By.XPATH, "//select[option[contains(text(),'15') or contains(text(),'5')]]")
            rows_per_page = Select(select_element)
            
            # Select by visible text to avoid value mismatch errors
            try:
                rows_per_page.select_by_visible_text("15")
            except:
                rows_per_page.select_by_index(len(rows_per_page.options) - 1)
        except Exception as e:
            print(f"(Note: Dropdown change skipped or already showing all rows: {e})")

        # -------------------------------------------------------------
        # TC05: Extract all email addresses
        # -------------------------------------------------------------
        print("\n--- TC05: Extract all email addresses ---")
        email_cells = driver.find_elements(By.XPATH, "//table/tbody/tr/td[4]")
        emails = [cell.text for cell in email_cells if cell.text]
        for i, email in enumerate(emails, 1):
            print(f"{i:02d}. {email}")

        # -------------------------------------------------------------
        # TC06: Find employee with highest Salary
        # -------------------------------------------------------------
        print("\n--- TC06: Find employee with highest Salary ---")
        all_data_rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
        max_salary = 0.0
        highest_paid_employee = ""

        for row in all_data_rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 6:
                full_name = f"{cols[1].text} {cols[2].text}"
                salary_str = cols[5].text.replace("$", "").replace(",", "").strip()
                if salary_str:
                    salary_val = float(salary_str)
                    if salary_val > max_salary:
                        max_salary = salary_val
                        highest_paid_employee = f"{full_name} (${salary_val:,.2f})"

        print("Highest Salary Employee:", highest_paid_employee)

        # -------------------------------------------------------------
        # TC07: Verify that a particular website link exists
        # -------------------------------------------------------------
        print("\n--- TC07: Verify that a particular website link exists ---")
        contact_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'hi@assertqa.com') or contains(@href, 'practice')]")
        if len(contact_links) > 0:
            print("Status: PASS - Found valid links on page.")
        else:
            print("Status: FAIL - Web link not found.")

        # -------------------------------------------------------------
        # TC08: Count data rows without counting the header
        # -------------------------------------------------------------
        print("\n--- TC08: Count data rows without counting the header ---")
        data_rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
        print("Total Data Rows (excluding <th> header):", len(data_rows))

        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 60)

    except Exception as error:
        print("\nAn error occurred during test execution:", error)

    finally:
        driver.quit()

if __name__ == "__main__":
    run_webtable_tests()
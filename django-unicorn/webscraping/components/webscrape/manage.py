from django_unicorn.components import UnicornView, QuerySetType
from django.conf import settings

from datetime import date, datetime
from webscraping.models import Webscrape


from .webscrapes import MessageStatus


class ManageView(UnicornView):
    """
        src: https://www.bugbytes.io/posts/django-unicorn-an-introduction/
    """
    webscrape: Webscrape = None


    website_url: str = ''
    title: str = ''
    first_name: str = ''
    last_name: str = ''
    middle_name: str = ''
    middle_initials: str = ''
    age: int = None
    city: str = ''
    state: str = ''
    country: str = '' 

    us_states = None
    countries = None

    new_media_base64 = None
    new_media_file_name = None

    webscrapes: QuerySetType[Webscrape] = Webscrape.objects.all()

    def setTitle(self, value):
        self.title = value

    def mount(self):
        self.countries = self.parent.countries
        self.us_states = self.parent.us_states

        # For testing...
        # --------------
        if settings.DEBUG:
            self.webscrape = Webscrape.objects.first()

        # @ToDo: Auto set fields - check
        # ----------------------
        # self.fields = [f.name for f in Webscrape._meta.get_fields()]
        # for val in ('id', 'created_on', 'last_modified'):
        #     self.fields.remove(val)

        # for field in self.fields:
        #     self.__dict__[field] = None


    def add(self):

        print('------------------ | ----------------', str(self.title), str(self.age))
        Webscrape.objects.create(
            website_url = self.website_url,
            title = self.title,
            first_name = self.first_name,
            last_name = self.last_name,
            middle_name = self.middle_name,
            middle_initials = self.middle_initials,
            age = self.age,
            city = self.city,
            state = self.state,
        )
        self.clear_fields()
        return self.parent.load_table(force_render=True)

    def scrape(self):
        self.add()

        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        # Initialize WebDriver (e.g., Chrome)
        driver = webdriver.Chrome() 

        # Navigate to TruthFinder website (replace with the actual URL)
        driver.get("https://www.truthfinder.com") 

        # Example: Find an element by name 
        try:
            # Wait for the element to be clickable (adjust timeout as needed)
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "username_or_email")) 
            ) 

            # Interact with the element (e.g., send keys)
            element.send_keys("your_username_or_email") 

        except Exception as e:
            print(f"Error locating or interacting with element: {e}")

        # ... (Continue with other actions, such as finding and interacting with other elements) ...

        # Close the browser
        driver.quit()

    def update_list(self):
        self.parent.load_table(force_render=True)


    def clear_fields(self):
        self.title = ''
        self.first_name = ''
        self.last_name = ''
        self.middle_name = ''
        self.middle_initials = ''
        self.last_name = ''
        self.age = ''
        self.city = ''
        self.state = ''



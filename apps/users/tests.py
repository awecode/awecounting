from droozal.tests import snapshot_on_error, TestCaseOnPhantom
from .models import User


class UserTest(TestCaseOnPhantom):
    def test_create_user(self):
        self.create_user()

    def test_create_superuser_and_login(self):
        self.superuser_login()

    @snapshot_on_error
    def test_create_new_user(self):
        self.superuser_login()
        self.open('/admin/users/user/add/')
        # Fill the create user form with username and password
        random_username = self.random_string()
        random_email = self.random_string() + '@' + self.random_string() + '.com'
        self.browser.find_element_by_id("id_username").send_keys(random_username)
        self.browser.find_element_by_id("id_email").send_keys(random_email)
        self.browser.find_element_by_id("id_password1").send_keys("testpassword")
        self.browser.find_element_by_id("id_password2").send_keys("testpassword")

        # Forms can be submitted directly by calling its method submit
        self.browser.find_element_by_id("user_form").submit()
        # the following gives error if the above procedure failed, otherwise test has been passed
        User.objects.get(username=random_username, email=random_email)

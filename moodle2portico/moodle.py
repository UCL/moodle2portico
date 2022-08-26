import mechanize
import getpass

def init_browser():
    """Get browser object with settings so that Moodle won't block access."""
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [("User-agent","Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0")]
    return br

browser = init_browser()  # TODO: Can we avoid using a global variable for this?

def download_gradebook(url_course):
    """Download full gradebook from given course as CSV, returning a string."""
    select_grade_download_form(url_course)
    grades = download_data()
    return grades

def login(url_course):
    """Fill in login form on Moodle site."""
    response = browser.open(url_course)
    browser.select_form(predicate=is_login_form)
    login_form = browser.form
    username = input("Enter username for Moodle login: ")
    password = getpass.getpass("Enter password for Moodle login: ")
    login_form["username"] = username
    login_form["password"] = password
    browser.submit()
    if not logged_in_to_moodle():
        raise Exception("Not logged in")

def is_login_form(form):
    """Check if given form has expected username and password
    controls."""
    try:
        form.find_control(name='username',type='text')
        form.find_control(name='password',type='password')
        return True
    except mechanize.ControlNotFoundError:
        return False

def is_download_form(form):
    """Check if given form has expected download control."""
    try:
        submit = form.find_control(name='submitbutton',type='submit')
        label  = submit.get_labels()[0]
        return "Download" == label.text
    except mechanize.ControlNotFoundError:
        return False

def logged_in_to_moodle():
    """Check if we are logged in to Moodle so can see 'My courses'."""
    try:
        browser.find_link(text="My courses")
        return True
    except mechanize.LinkNotFoundError:
        return False

def select_grade_download_form(url_course):
    """Select form to download grades as plain text (CSV)."""
    browser.open(url_course)
    browser.follow_link(text="Gradebook setup")
    browser.follow_link(text="Export")
    browser.follow_link(text="Plain text file")
    browser.select_form(predicate=is_download_form)

def download_data():
    """Submit form and retrieve data."""
    download_response = browser.submit(name="submitbutton")
    data = download_response.get_data()
    string_data = data.decode()
    return string_data

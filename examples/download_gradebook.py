import moodle2portico as m2p

url_course = 'https://moodle.ucl.ac.uk/course/view.php?id=10648'
m2p.moodle.login(url_course)
grades = m2p.moodle.download_gradebook(url_course)
m2p.save_string_as_file(grades,'grades_original.csv')

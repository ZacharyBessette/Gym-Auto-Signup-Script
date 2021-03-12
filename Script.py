from selenium import webdriver
import datetime
from tkinter import *
import time

''' #Todo/improvements
-More variety and descriptive error messages
-Create and exe. for ease of setup (for reservation txt document and scheduled file running
-Backup booking dates, in case one is taken (possible although very unlikely to happen)
-Nice UI and presentation for reservations
'''

user_email_address = "zacharybessette1619@gmail.com"
user_password = "Command7"
reservation_directory_path = "D:/Documents/Fit 4 Less Auto Signup/Gym reservations.txt"


# Finds date 2 days in the future, in year-month-day format (without showing the time of day)
reservation_date = datetime.datetime.today() + datetime.timedelta(days=2)
reservation_date_2 = "date_" + str(reservation_date)[0:10] #Takes only the string yy/mm/dd component of the date

alert_list = ("ERROR:", "Unknown error, reservation could not be completed successfully", "")

#Copied code from internet, displays a pop-up window indicating whether gym appointment was successfully book for the time slot or not
def alert_popup(title, message, path):
    """Generate a pop-up window for special messages."""
    root = Tk()
    root.title(title)
    w = 400     # popup window width
    h = 200     # popup window height
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w)/2
    y = (sh - h)/2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    m = message
    m += '\n'
    m += path
    w = Label(root, text=m, width=120, height=10)
    w.pack()
    b = Button(root, text="OK", command=root.destroy, width=10)
    b.pack()
    mainloop()



booking_date = str(reservation_date)[0:10]

#Read predefined gym reservations from a text file
gym_slots = open(reservation_directory_path, 'r')
file_text_lines = gym_slots.readlines()
index = 0

if any(booking_date in word for word in file_text_lines): #Checks if a valid date is present in the text document
    for i in range(len(file_text_lines)): #Checks the whole length of the file, line by line
        if booking_date in file_text_lines[i]: #Checks if the booking date is found in the given file line
            index = i
    booking_date_occurrence_index = file_text_lines[index].find(booking_date) #Finds index of the start of the reservation date string in the file line

    given_date = file_text_lines[index][booking_date_occurrence_index + 10:].replace(" ", "").replace('\n', "") #Removes any blank spaces on the given resveration date line and looks for the time, given after the yy/mm/dd element

    #Dictionary with the given gym timeslots available, each assigned to a number
    time_slot_numbers = {
        '7:00am': 0,
        '8:30am': 1,
        '10:00am': 2,
        '11:30am': 3,
        '1:00pm': 4,
        '2:30pm': 5,
        '4:00pm': 6,
        '5:30pm': 7,
        '7:00pm': 8,
        '8:30pm': 9
    }
    alert_list = ("Success!:", "Reservation successfully booked for:", booking_date + ", at: " + given_date)
    #Changes alert if gym reservation was able to be read


# Creates a web-browser and has the web-browser open said url
browser = webdriver.Chrome('D:/Documents/Fit 4 Less Auto Signup/chromedriver.exe')
browser.get('https://myfit4less.gymmanager.com/portal/login.asp')
browser.maximize_window()

# Login stuff
email = browser.find_element_by_name('emailaddress')
password = browser.find_element_by_name('password')

email.click()
email.send_keys(user_email_address)

password.click()
password.send_keys(user_password)

browser.find_element_by_id('loginButton').click()


# Clicks the reservation button based on date given on first couple lines
# Date only valid for today, tomorrow and the day after tomorrow
browser.find_element_by_id('btn_date_select').click()

#Clicks the button for the given reservation date yy/mm/dd given in the file
browser.find_element_by_id(reservation_date_2).click()
#Scroll down function used as future button elements have to be on screen for the selenium functions to properly work
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#Forgot what this does, 99% sure its useless, but program works fine with it so going to keep it in
button_list = browser.find_elements_by_class_name('available-slots').__getitem__(1)

#Clicks on the timeslot button using the website's button name
button_list = button_list.find_elements_by_class_name('time-slot')

#Clicks the gym reservation corresponding to the given time in the text document
button_list.__getitem__(time_slot_numbers[given_date]).click()

#Clicks the reservation confirmation button
browser.find_element_by_id('dialog_book_yes').click()

#Displays alert to screen and closes the webdriver
alert_popup(alert_list[0], alert_list[1], alert_list[2])
exit()

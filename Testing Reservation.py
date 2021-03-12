import datetime
from tkinter import *
reservation_date = datetime.datetime.today() + datetime.timedelta(days=2)
reservation_date_2 = "date_" + str(reservation_date)[0:10]


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


def reservation():
    booking_date = str(reservation_date)[0:10]

    gym_slots = open('Gym reservations.txt', 'r')
    file_text_lines = gym_slots.readlines()

    if any(booking_date in word for word in file_text_lines):
        for i in range(len(file_text_lines)):
            if booking_date in file_text_lines[i]:
                index = i
        booking_date_occurrence_index = file_text_lines[index].find(booking_date)

        given_date = file_text_lines[index][booking_date_occurrence_index + 10:].replace(" ", "").replace('\n', "")
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
        alert_popup("Success!:", "Reservation will successfully be booked for:", booking_date + ", at: " + given_date)
        return time_slot_numbers[given_date]

    else:
        alert_popup("ERROR:", "Unknown error, reservation not successfully setup", "")
        return 0


reservation()

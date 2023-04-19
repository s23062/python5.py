import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#slownik do przechowywania danych
students = {}

#wczytywanie danych z pliku csv i zapisywanie ich do słownika
def load_data(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            email = row[0]
            first_name = row[1]
            last_name = row[2]
            points = int(row[3])
            grade = row[4] if len(row) >= 5 else ''
            status = row[5] if len(row) >= 6 else ''
            students[email] = {'first_name': first_name, 'last_name': last_name, 'points': points, 'grade': grade, 'status': status}

#zapisywanie danych do pliku csv
def save_data(file_path):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for email, data in students.items():
            writer.writerow([email, data['first_name'], data['last_name'], data['points'], data['grade'], data['status']])

#automatyczne wystawianie oceny
def grade_students():
    for email, data in students.items():
        if data['status'] not in ['GRADED', 'MAILED']:
            points = data['points']
            if points <= 50:
                grade = 2
            elif points <= 60:
                grade = 3
            elif points <= 70:
                grade = 3.5
            elif points <= 80:
                grade = 4
            elif points <= 90:
                grade = 4.5
            else:
                grade = 5
            students[email]['grade'] = grade
            students[email]['status'] = 'GRADED'

#dodawanie nowego studenta
def add_student(email, first_name, last_name, points):
    if email in students:
        print('Student with email {} already exists.'.format(email))
    else:
        students[email] = {'first_name': first_name, 'last_name': last_name, 'points': points, 'grade': '', 'status': ''}
        save_data('students.csv')
        print('Student added successfully.')

#usuwanie studenta
def remove_student(email):
    if email in students:
        del students[email]
        save_data('students.csv')
        print('Student removed successfully.')
    else:
        print('Student with email {} does not exist.'.format(email))

#wyswietlenie studentow z pliku
#def show_students():
    #with open('students.csv', mode='r') as file:
       #reader = csv.DictReader(file)
        #for row in reader:
           #print(f"{row['first_name']} {row['last_name']} - {row['email']} - {row['points']} pkt - {row['grade']} - {row['status']}")

#wysyłanie emaili
def send_emails(email_address, email_password, email_subject, email_message):
    for email, data in students.items():
        if data['status'] != 'MAILED':
            first_name = data['first_name']
            last_name = data['last_name']
            grade = data['grade']
            message = email_message.format(first_name, last_name, grade)
            msg = MIMEMultipart()
            msg['From'] = email_address
            msg['To'] = email
            msg['Subject'] = email_subject
            msg.attach(MIMEText(message, 'plain'))
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(email_address, email_password)
                server.sendmail(email_address, email, msg.as_string())
                server.quit()
                students[email]['status'] = 'MAILED'
                save_data('students.csv')
                print('Email sent successfully to {}.'.format(email))
            except Exception as e:
                print('Failed to send email to {}. Error message: {}'.format(email, str(e)))

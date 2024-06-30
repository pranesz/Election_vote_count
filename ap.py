from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pr@24!74",
    database="election_count"
)

mycursor = mydb.cursor()

# Define the email sending function
def send_email(to_email, voter_name):
    from_email = "praneshpranesh648@gmail.com"
    password = "qoaa vssn sxoo rptq"

    subject = "Thanks for Voting"
    body = f"Dear {voter_name},\n\nThank you for voting!\n\nBest regards,\nElection Committee"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:  
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

@app.route('/')
def get_user_details():
    return render_template('login.html')

@app.route('/front', methods=['GET', 'POST'])
def show_data():
    if request.method == 'POST':
        voter_name = request.form.get('voter_name')
        voter_email = request.form.get('voter_email')

 
        with open('voter_details.txt', 'a') as file:
            file.write(f'Name: {voter_name}, Email: {voter_email}\n')

 
        mycursor.execute("SELECT id, candidate_name FROM election_count")
        candidates = mycursor.fetchall()
        return render_template("front.html", candidates=candidates, voter_name=voter_name, voter_email=voter_email)

    return redirect(url_for('get_user_details'))

@app.route('/vote', methods=['POST'])
def vote():
    candidate_id = request.form['candidate_id']
    voter_name = request.form['voter_name']
    voter_email = request.form['voter_email']

    mycursor.execute('UPDATE election_count SET votes = votes + 1 WHERE id = %s', (candidate_id,))
    mydb.commit()

    send_email(voter_email, voter_name)

    return redirect(url_for('show_data'))

if __name__ == "__main__":
    app.run(debug=True)

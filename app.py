from flask import Flask,render_template,request,redirect,url_for
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Pr@24!74",
    database = "election_count"
    
)
mycursor = mydb.cursor()



def send_mail(to_mail,voter_name):
    from_email="praneshpranesh648@gmail.com"
    password = "qoaa vssn sxoo rptq"

    subject = "Thanks For Voting"
    body = f"Dear {voter_name},\n\n Thanks you for Voting!\n\n Best Regards,\nElection Committee"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_mail
    msg['Subject'] = subject
    msg.attach(MIMEText(body,"plain"))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:  
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_mail, msg.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")



@app.route('/')
def get_user_details():
    return render_template('login.html')



@app.route('/front',methods=['GET','POST'])
def show_data():
    if request.method == 'POST':
        voter_name = request.form.get('voter_name')
        voter_email = request.form.get('voter_email')
        with open("Voter_details.txt","a") as file:
            file.write(f"Username: {voter_name} Email: {voter_email}\n")

        mycursor.execute("select id, candidate_name from election_count")
        candidates = mycursor.fetchall()
        print("Fetch Candidates",candidates)
        return render_template("front.html",candidates=candidates,voter_name=voter_name,voter_email=voter_email)
    return redirect(url_for('get_user_details'))


 
@app.route('/vote',methods=['POST'])
def vote():
    candidate_id = request.form['candidate_id']
    voter_name = request.form['voter_name']
    voter_email = request.form['voter_email']
    mycursor.execute('UPDATE election_count SET votes = votes + 1 WHERE id = %s',(candidate_id,))
    mydb.commit()

    send_mail(voter_name,voter_email)

    return redirect(url_for('results'))

@app.route('/results')
def results():
    mycursor.execute("SELECT candidate_name, votes FROM election_count ORDER BY votes DESC")
    results = mycursor.fetchall()

    with open('Winner.txt','a') as file:
        for candidate in results:
            file.write(f"{candidate[0],{candidate[1]}}")
    
    if results:
        highest_votes = results[0][1]
        tied_candidates = [candidate[0] for candidate in results if candidate[1] == highest_votes]
    else:
        tied_candidates = []

    return render_template('results.html', tied_candidates=tied_candidates)

if __name__ == "__main__":
    app.run(debug=True)
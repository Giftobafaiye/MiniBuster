import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from sklearn.ensemble import IsolationForest  # ✅ this is key
import smtplib
from email.mime.text import MIMEText

import requests  # If not already imported

def send_slack_alert(webhook_url, anomalies_count):
    message = {
        "text": f"🚨 *MiniBuster* detected *{anomalies_count}* anomalies in logs!"
    }
    requests.post(webhook_url, json=message)

def send_email_alert(to_email, anomalies_count):
    sender = "giftobafaiye@gmail.com"
    password = "oaed cuor gqgi mqlw"  # <-- App password from Google
    subject = "🚨 MiniBuster Alert: Anomalies Detected"
    body = f"MiniBuster detected {anomalies_count} suspicious log entries."

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, to_email, msg.as_string())

import requests

def send_slack_alert(webhook_url, anomalies_count):
    message = {
        "text": f"🚨 *MiniBuster* detected *{anomalies_count}* anomalies in logs!"
    }
    requests.post("https://hooks.slack.com/services/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", json=message)


anomalies = df[df['anomaly'] == -1]
st.subheader("🚨 Detected Anomalies")
st.dataframe(anomalies)

if not anomalies.empty:
    send_email_alert("giftobafaiye@gmail.com", len(anomalies))
    send_slack_alert("https://hooks.slack.com/services/your/full/webhook", len(anomalies))

st.set_page_config(page_title="MiniBuster Dashboard", layout="centered")

credentials = {
    "usernames": {
        "admin": {
            "name": "Admin",
            "password": "$2b$12$CnLg6Ld9OdQ815a5IDAodu37gJocaMl8r6q.79VsJFtYF8hKsP4fG"  # your hashed password
        }
    }
}

authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name='minibuster',
    key='abcdef',
    cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login(form_name='Login', location='main')

if authentication_status:
    authenticator.logout('Logout', 'sidebar')
    st.success(f'Welcome {name} 👋')

    # 👇 Everything below must be indented inside this block
    st.title("🛡️ MiniBuster: Ransomware Anomaly Detector")

    uploaded_file = st.file_uploader("📁 Upload system_logs.csv", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.subheader("📊 Preview of Uploaded Logs")
        st.dataframe(df)

        # Run Isolation Forest
        contamination = st.slider("Sensitivity (Contamination %)", 0.01, 0.5, 0.2)
        model = IsolationForest(contamination=contamination)
        model.fit(df)
        df['anomaly'] = model.predict(df)

        anomalies = df[df['anomaly'] == -1]
        st.subheader("🚨 Detected Anomalies")
        st.dataframe(anomalies)

        # Charts
        st.line_chart(df['cpu_usage'])
        st.line_chart(df['memory_usage'])
        st.line_chart(df['disk_usage'])
        st.line_chart(df['network_in'])

        # Download
        st.download_button("⬇️ Download Report", df.to_csv(index=False), file_name="report.csv")
    else:
        st.info("Please upload a CSV file to get started.")

elif authentication_status is False:
    st.error("Incorrect username or password")
elif authentication_status is None:
    st.warning("Please enter your credentials")









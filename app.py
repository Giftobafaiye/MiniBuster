import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from sklearn.ensemble import IsolationForest
import smtplib
import requests
from email.mime.text import MIMEText

# -----------------------------
# Email Alert Function
# -----------------------------
def send_email_alert(to_email, anomalies_count):
    sender = st.secrets["email"]["sender"]
    password = st.secrets["email"]["app_password"]
    subject = "🚨 MiniBuster Alert: Anomalies Detected"
    body = f"MiniBuster detected {anomalies_count} suspicious log entries."

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, to_email, msg.as_string())

# -----------------------------
# Slack Alert Function
# -----------------------------
def send_slack_alert(anomalies_count):
    webhook = st.secrets["slack"]["webhook"]
    message = {
        "text": f"🚨 *MiniBuster* detected *{anomalies_count}* anomalies in logs!"
    }
    requests.post(webhook, json=message)

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(page_title="MiniBuster Dashboard", layout="centered")

# -----------------------------
# Authenticator Config
# -----------------------------
credentials = {
    "usernames": {
        "admin": {
            "name": "Admin",
            "password": "$2b$12$CnLg6Ld9OdQ815a5IDAodu37gJocaMl8r6q.79VsJFtYF8hKsP4fG"
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

# -----------------------------
# If Logged In
# -----------------------------
if authentication_status:
    authenticator.logout('Logout', 'sidebar')
    st.success(f'Welcome {name} 👋')
    st.title("🛡️ MiniBuster: Ransomware Anomaly Detector")

    uploaded_file = st.file_uploader("📁 Upload system_logs.csv", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.subheader("📊 Preview of Uploaded Logs")
        st.dataframe(df)

        # Anomaly Detection
        contamination = st.slider("Sensitivity (Contamination %)", 0.01, 0.5, 0.2)
        model = IsolationForest(contamination=contamination)
        model.fit(df)
        df['anomaly'] = model.predict(df)

        anomalies = df[df['anomaly'] == -1]
        st.subheader("🚨 Detected Anomalies")
        st.dataframe(anomalies)

        # Alerts
        if not anomalies.empty:
            send_email_alert("your-email@gmail.com", len(anomalies))
            send_slack_alert(len(anomalies))

        # Visualizations
        st.subheader("📈 CPU Usage Over Time")
        st.line_chart(df['cpu_usage'])

        st.subheader("📈 Memory Usage Over Time")
        st.line_chart(df['memory_usage'])

        st.subheader("📈 Disk Usage Over Time")
        st.line_chart(df['disk_usage'])

        st.subheader("📈 Network Inbound Over Time")
        st.line_chart(df['network_in'])

        # Download
        st.download_button("⬇️ Download Full Report", df.to_csv(index=False), file_name="minibuster_report.csv")

    else:
        st.info("Please upload a CSV file to begin.")

# -----------------------------
# If Login Failed
# -----------------------------
elif authentication_status == False:
    st.error("Incorrect username or password")
elif authentication_status is None:
    st.warning("Please enter your credentials")

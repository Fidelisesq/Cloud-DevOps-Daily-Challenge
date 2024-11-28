import os
import psutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import time

def check_disk_usage():
    """Check and display disk usage."""
    try:
        usage = psutil.disk_usage('/')
        print("\nDisk Usage:")
        print(f"Total: {usage.total // (1024 ** 3)} GB")
        print(f"Used: {usage.used // (1024 ** 3)} GB")
        print(f"Free: {usage.free // (1024 ** 3)} GB")
        print(f"Percentage: {usage.percent}%")
    except Exception as e:
        print(f"Error checking disk usage: {e}")

def monitor_running_services():
    """Monitor running services."""
    try:
        print("\nRunning Services:")
        for process in psutil.process_iter(['pid', 'name', 'status']):
            if process.info['status'] == psutil.STATUS_RUNNING:
                print(f"PID: {process.info['pid']} - Name: {process.info['name']}")
    except Exception as e:
        print(f"Error monitoring running services: {e}")

def assess_memory_usage():
    """Assess and display memory usage."""
    try:
        memory = psutil.virtual_memory()
        print("\nMemory Usage:")
        print(f"Total: {memory.total // (1024 ** 3)} GB")
        print(f"Available: {memory.available // (1024 ** 3)} GB")
        print(f"Used: {memory.used // (1024 ** 3)} GB")
        print(f"Percentage: {memory.percent}%")
    except Exception as e:
        print(f"Error assessing memory usage: {e}")

def evaluate_cpu_usage():
    """Evaluate and display CPU usage."""
    try:
        print("\nCPU Usage:")
        print(f"CPU Utilization: {psutil.cpu_percent(interval=1)}%")
    except Exception as e:
        print(f"Error evaluating CPU usage: {e}")

def send_email_report():
    """Send a comprehensive system health report via email."""
    try:
        # Generate the report
        now = datetime.now()
        report = f"System Health Report - {now.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        usage = psutil.disk_usage('/')
        memory = psutil.virtual_memory()

        report += f"Disk Usage:\n"
        report += f"Total: {usage.total // (1024 ** 3)} GB\n"
        report += f"Used: {usage.used // (1024 ** 3)} GB\n"
        report += f"Free: {usage.free // (1024 ** 3)} GB\n"
        report += f"Percentage: {usage.percent}%\n\n"

        report += f"Memory Usage:\n"
        report += f"Total: {memory.total // (1024 ** 3)} GB\n"
        report += f"Available: {memory.available // (1024 ** 3)} GB\n"
        report += f"Used: {memory.used // (1024 ** 3)} GB\n"
        report += f"Percentage: {memory.percent}%\n\n"

        report += f"CPU Usage:\n"
        report += f"CPU Utilization: {psutil.cpu_percent(interval=1)}%\n\n"

        # Email configuration
        sender_email = os.getenv("SENDER_EMAIL")
        receiver_email = os.getenv("RECEIVER_EMAIL")
        email_password = os.getenv("EMAIL_PASSWORD")

        if not sender_email or not receiver_email or not email_password:
            raise ValueError("One or more email environment variables are not set!")

        # Create the email
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = "System Health Report"
        msg.attach(MIMEText(report, "plain"))

        # Send the email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        print("\nReport sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def main():
    """Main menu for system health checks."""
    while True:
        print("\n--- System Health Check Menu ---")
        print("1. Check Disk Usage")
        print("2. Monitor Running Services")
        print("3. Assess Memory Usage")
        print("4. Evaluate CPU Usage")
        print("5. Send Comprehensive Report via Email")
        print("6. Exit")
        try:
            choice = int(input("Enter an integer corresponding to your choice: "))
            if choice == 1:
                check_disk_usage()
            elif choice == 2:
                monitor_running_services()
            elif choice == 3:
                assess_memory_usage()
            elif choice == 4:
                evaluate_cpu_usage()
            elif choice == 5:
                send_email_report()
            elif choice == 6:
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

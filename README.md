# SMS Massive - Polyline Constructora

A Python application built with Flet for sending mass emails with customizable templates, attachments, and HTML support.

## Features
- **Simple Emails**: Send plain text emails with a subject and message.
- **Complex Emails**: Include attachments with your emails.
- **HTML Emails**: Send emails with custom HTML templates.
- **Bulk Sending**: Send emails to multiple recipients from a CSV file.
- **Progress Tracking**: Monitor the progress of email sending with a progress bar and logs.


<img src="https://github.com/R3D4L1T/massEmails/blob/main/img1.jpg">
<img src="https://github.com/R3D4L1T/massEmails/blob/main/img2.jpg">
<img src="https://github.com/R3D4L1T/massEmails/blob/main/img3.jpg">




## Prerequisites
- Python 3.8 or higher
- Flet library (`pip install flet`)
- SMTP credentials (e.g., Gmail)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/smsMassive.git
   cd smsMassive
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```bash
   python src/main.py
   ```
2. Follow the on-screen instructions to compose and send emails.

## Configuration
- **SMTP Settings**: Update the `emailAddress` and `passwordAddress` fields in the app with your SMTP credentials.
- **CSV File**: Ensure your CSV file has a `correo` column for recipient emails.



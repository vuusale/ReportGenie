# 🧞‍♂️ ReportGenie: Your Wish, My Report!

<img src="https://github.com/user-attachments/assets/dc2b166c-097d-4bd5-b402-23e9dd190a60" alt="drawing" width="1000"/>

👋 Welcome to ReportGenie, where a little magic (and code) goes a long way in generating professional pentest reports!

Tired of endlessly formatting pentest findings, wrangling with Word docs, or stressing over getting that perfect structure? Fear not! ReportGenie is here to grant your report-writing wishes. You tell the Genie what vulnerabilities you found, and POOF!—you’ve got a neatly formatted penetration test report, all through a simple web interface.

### 🌟 What is ReportGenie?

ReportGenie is a Flask-based web app designed to make penetration testers’ lives easier. With just a few clicks, you can input the details of your findings, and ReportGenie will handle the heavy lifting of generating a professional report.

Think of ReportGenie as your trusty assistant who never misses a detail, formats with precision, and doesn’t ask for vacation days. (Though it might take a coffee break if you forget to install Flask 😉).

### 🧙‍♂️ How It Works

1. **Summon the Genie**: Open the web app (with Flask running), and fill in your project details and any custom fields you've defined..
2. **Add Your Findings**: For each vulnerability, add details like title, description, severity, impact, and remediation. 
4. **Manage Projects**: Edit or delete past projects as needed, and set up default settings for future reports.
5. **Generate Reports**: Hit the Generate Report button, and let ReportGenie compile your pentest report in an instant.
6. **Download & Share**: Download your reports anytime from past projects, ready to deliver to your client or team.

### 🚀 Setup

1. Clone this repo:
```bash
git clone https://github.com/vuusale/ReportGenie.git
cd ReportGenie
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the Flask app:
```bash
flask run
```
4. Open the app: Navigate to `http://localhost:8000` in your browser.

Now you’re ready to enter your findings and let the Genie do the rest!

### Docker installation

You can also pull the docker image to testify Genie's capabilities! Just execute `docker run -p 8000:8000 vuusale/reportgenie:latest` command to awaken the genie. 

> [!WARNING]  
> **Please keep in mind that all data will be gone when you terminate the container. So I recommend cloning the repository to get the full out of this tool.**

### 📖 Usage Guide

1. Start by telling the Genie details about the project you’re working on such as start and end dates, executive summary, etc.
2. Describe Vulnerabilities: For each vulnerability:
  - Provide a title (e.g., “SQL Injection in Login Form”).
  - Select the severity (Low, Medium, High, or Critical).
  - Indicate URL or vulnerable component
  - Write a clear and concise description.
  - Add the potential impact (so your client knows why it’s a big deal).
  - Provide remediation steps (so they know how to fix it).
3. With everything entered, click the Generate Report button and let ReportGenie do its thing. 
4. Click Download Report button to get a polished report, ready to deliver to your client. 

When opening the docx file every time, you will encounter a popup like the following:

<img src="https://github.com/user-attachments/assets/8372f4b9-d779-4563-9d83-64d7c1102c82" width="1000" />

This is for updating the Table of Contents, so click "Yes", then "OK". After that, I recommend saving the file as DOCX or PDF to avoid seeing a popup every time.

### ✨ Features

- **Vulnerability Input Forms**: Tell the Genie what you’ve uncovered—vulnerabilities, impact, remediation—it handles the rest.
- **Add Unlimited Vulnerabilities**: Easily add as many vulnerabilities as you need without any hassle.
- **Rich Text Editing**: The text fields support rich text formatting, allowing you to enhance your content with various styling options.
- **Store Project Details**: Save all your pentest project information securely within the app. No more scattered notes or lost details.
- **Professional Report**: Generate clean, professionally formatted reports ready to impress your clients or boss.
- **Edit and Delete Past Projects**: Need to update a report or remove an old project? The Genie allows you to do everything effortlessly.
- **Download Reports Anytime**: Download reports of your past projects whenever you need them. Your reports are just a click away.
- **Define Custom Fields**: Need to add specific sections unique to your project? Define custom fields in settings for complete flexibility. 
- **Fast & Simple**: No more hours lost to formatting—just wish for a report, and it’s done.

> [!WARNING]  
> **There migth be certain formatting issues in the resulting document, such as an empty page or some HTML elements not rendering. That's because reportGenie cannot entirely replace humans 😊**

### 🛡️ Why Use ReportGenie?

- **Time Saver**: Spend less time formatting and more time finding vulnerabilities.
- **Customizable**: Define default settings and custom fields to tailor reports to your needs.
- **Organized**: Store, edit, and manage all your pentest projects in one place.
- **Standardized Format**: All reports are consistently formatted and look professional.
- **User-Friendly**: An intuitive interface that makes report generation a breeze.
- **Scalable**: Handle any number of vulnerabilities without extra work.

### 📫 Contributing

If you have any cool feature ideas, bug fixes, or enhancements, feel free to submit a pull request! The Genie loves to learn new tricks.

So, what are you waiting for? Make a wish, summon the Genie, and let it handle the reports while you focus on the real hacking! 🧞‍♂️✨

Happy Pentesting! 🎩🐍

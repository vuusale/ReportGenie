🧞‍♂️ ReportGenie: Your Wish, My Report!

<img src="https://github.com/user-attachments/assets/b2b0fbc3-7722-4c3a-8ec3-2e05e741d07a" alt="drawing" width="500"/>

👋 Welcome to ReportGenie, where a little magic (and code) goes a long way in generating professional pentest reports!

Tired of endlessly formatting pentest findings, wrangling with Word docs, or stressing over getting that perfect structure? Fear not! ReportGenie is here to grant your report-writing wishes. You tell the Genie what vulnerabilities you found, and POOF!—you’ve got a neatly formatted penetration test report, all through a simple web interface.

### 🌟 What is ReportGenie?

ReportGenie is a Flask-based web app designed to make penetration testers’ lives easier. With just a few clicks, you can input the details of your findings, and ReportGenie will handle the heavy lifting of generating a professional report.

Think of ReportGenie as your trusty assistant who never misses a detail, formats with precision, and doesn’t ask for vacation days. (Though it might take a coffee break if you forget to install Flask 😉).

### 🧙‍♂️ How It Works

- Summon the Genie: Open the web app (with Flask running), and fill in your project details.
- Add Your Findings: For each vulnerability, add the title, description, severity, impact, and remediation steps. You can even provide references if you’re feeling extra thorough.
- Wish Granted: Hit the Generate Report button and let ReportGenie conjure your pentest report in an instant. Magic, right?

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
4. Open the app: Navigate to `http://localhost` in your browser.

Now you’re ready to enter your findings and let the Genie do the rest!

### ✨ Features

- Vulnerability Input Forms: Tell the Genie what you’ve uncovered—vulnerabilities, impact, remediation—it handles the rest.
- Add as Many Vulnerabilities as You Want: Need more space? Click "Add Vulnerability," and voilà! A new form appears as if by magic.
- Clean, Professional Report Output: Genie delivers a formatted, professional pentest report ready to impress your client or boss.
- Client & Project Info: Input details like the project name, client name, and date to customize your report.
- Fast & Simple: No more hours lost to formatting—just wish for a report, and it’s done.


> [!WARNING]  
> **Pro tip: Don’t ask the Genie for infinite wishes. It’s a pentest reporting tool, not a loophole in magical contracts.**


### 🛠️ Tech stack

- Framework: Flask (Python)
- Front-End: Bootstrap for sleek and responsive forms.
- Docx Templates: Custom templates for each report generated.
- Dynamic Form Handling: Add multiple vulnerabilities dynamically without refreshing the page.

### 📖 Usage Guide

1. Enter Project Details: Start by telling the Genie what project you’re working on and who it’s for.
2. Describe Vulnerabilities: For each vulnerability:
  - Provide a title (e.g., “SQL Injection in Login Form”).
  - Select the severity (Low, Medium, High, or Critical).
  - Write a clear and concise description.
  - Add the potential impact (so your client knows why it’s a big deal).
  - Provide remediation steps (so they know how to fix it).
  -  Optionally, add references (e.g., OWASP guidelines).
3. Generate the Report: With everything entered, click the Generate Report button and let ReportGenie do its thing. You’ll get a polished report, ready to deliver.

### 🧞‍♂️ Meet the Genie

ReportGenie is more than just a tool—it’s your new digital sidekick. Unlike other reporting tools, this Genie has personality:

- Fast: The Genie doesn’t mess around. Input your findings and let it instantly whip up a professional report for you.
- Accurate: Not only does it format your findings beautifully, but it also ensures no typo sneaks past!
- Friendly: No confusing settings, no technical headaches—just you, the Genie, and a well-organized report.

### 🛡️ Why Use ReportGenie?

- Time Saver: Spend less time formatting and more time finding vulnerabilities.
- Standardized Format: All reports are consistently formatted and look professional.
- Scalable: Handle any number of vulnerabilities without extra work.

### 📫 Contributing

If you have any cool feature ideas, bug fixes, or enhancements, feel free to submit a pull request! The Genie loves to learn new tricks.

So, what are you waiting for? Make a wish, summon the Genie, and let it handle the reports while you focus on the real hacking! 🧞‍♂️✨

Happy Pentesting! 🎩🐍

Feel free to adjust or add to this as you see fit! The goal is to maintain a light-hearted tone while still providing all the necessary details about the project.

# Pet Health Tracker
## Table of Contents
- [Description](#description)
- [Languages and Technologies Used](#languages-and-technologies-used)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Description
Pet Health Tracker is a console-based application built to help pet owners manage their pets' health information in one place. It covers user registration and login, storing details for multiple pets per owner, logging health records and vaccinations, and scheduling veterinary appointments. The goal is to give pet owners a simple, centralized way to stay on top of their pets' care and build better habits around preventive healthcare.

## Languages and Technologies Used
- Python
- File I/O (`users.txt`, `data.json`) for persistent storage

## Features
1. **User Accounts:**
   - Register a new account with a username and password
   - Log in to access saved pet data
   - User data automatically loaded and saved between sessions (`users.txt`)
2. **Pet Management:**
   - Add pets with name, breed, age, weight, and vaccination status
   - Display detailed information for each registered pet
3. **Health Tracking:**
   - Add health records with dates and descriptions
   - Log vaccination events per pet
4. **Appointment Scheduling:**
   - Record veterinary visits
   - Automatically calculate the next recommended appointment date
5. **Usability:**
   - Simple main menu loop for navigating all features
   - Clean exit option
   - Error handling and feedback guide the user through invalid input

## Installation
No installation is required beyond having Python installed. Clone the repository and run the main script:
```bash
git clone https://github.com/FarisKarkelja/pet-health-tracker.git
cd pet-health-tracker/project
python main.py
```

## Usage
Run the program and follow the on-screen menu to:
1. Register or log in to an account
2. Add one or more pets to your profile
3. Add health records and vaccinations for each pet
4. Schedule a veterinary appointment; the app calculates the next recommended visit
5. View a full summary of each pet's details at any time

User data persists automatically between sessions via `users.txt`.

## Contributing
If you'd like to contribute to this project, please follow these guidelines:
1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request

## License
This project is not licensed.

## Acknowledgements
- [Python Documentation](https://docs.python.org/3/)
- [Stack Overflow](https://stackoverflow.com/)
- University materials and resources

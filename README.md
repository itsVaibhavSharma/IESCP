# Influencer Sponsor Platform

[![Flask](https://img.shields.io/badge/Flask-v2.0-blue)](https://flask.palletsprojects.com/) [![Python](https://img.shields.io/badge/Python-v3.9-yellow)](https://www.python.org/) [![Jinja2](https://img.shields.io/badge/Jinja2-v3.1.2-green)](https://jinja.palletsprojects.com/) [![SQLite](https://img.shields.io/badge/SQLite-v3.39.4-blue)](https://www.sqlite.org/) [![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-v1.4.27-orange)](https://www.sqlalchemy.org/) [![HTML](https://img.shields.io/badge/HTML-v5-red)](https://developer.mozilla.org/en-US/docs/Web/HTML) [![CSS](https://img.shields.io/badge/CSS-v3-blue)](https://developer.mozilla.org/en-US/docs/Web/CSS) [![Bootstrap](https://img.shields.io/badge/Bootstrap-v5.1.3-purple)](https://getbootstrap.com/) [![JavaScript](https://img.shields.io/badge/JavaScript-vES6-yellowgreen)](https://developer.mozilla.org/en-US/docs/Web/JavaScript) [![AJAX](https://img.shields.io/badge/AJAX-v1.0-blue)](https://developer.mozilla.org/en-US/docs/Web/Guide/AJAX) [![Matplotlib](https://img.shields.io/badge/Matplotlib-v3.4.3-red)](https://matplotlib.org/) [![Git](https://img.shields.io/badge/Git-v2.30.1-orange)](https://git-scm.com/) [![Charts.js](https://img.shields.io/badge/Charts.js-v3.7.0-green)](https://www.chartjs.org/) [![Calendar](https://img.shields.io/badge/Calendar-v1.1.0-lightgrey)](https://pypi.org/project/calendar/) [![Datetime](https://img.shields.io/badge/Datetime-v4.3.1-lightblue)](https://docs.python.org/3/library/datetime.html)

A web application built using **Python**, **Flask**, and **SQLite** that connects **Sponsors** and **Influencers** for advertising campaigns. Sponsors can create campaigns, view influencer profiles, and manage advertising requests. Influencers can explore public campaigns and submit their ad requests. The platform offers an easy-to-use dashboard with features for both Sponsors and Influencers.

## Features

- **User Authentication** for both Sponsors and Influencers.
- **Sponsors Dashboard**: Create, manage, and flag campaigns, view ad requests, filter influencers by category.
- **Influencers Dashboard**: Explore public campaigns, submit ad requests, manage profiles.
- **Admin Panel**: Manage sponsors, influencers, campaigns, and ad requests with flagging/unflagging options.
- **Campaign and Ad Request Management**: Create public/private campaigns, accept/reject ad requests.
- **Statistics Dashboard**: View graphs and statistics on campaigns, ad requests, and users.
- **Responsive Design**: User-friendly interface built with **HTML**, **CSS**, **Bootstrap**.
- **Data Visualization**: Graphs rendered using **Matplotlib** and **Charts.js**.
- **AJAX** for interactive elements without reloading pages.
- **Calendar** and **Datetime** features for scheduling campaigns.

## Technologies Used

- **Backend**: Python, Flask, Jinja2, SQLite, SQLAlchemy
- **Frontend**: HTML, CSS, Bootstrap, JavaScript, AJAX
- **Visualization**: Matplotlib, Charts.js
- **Other Tools**: Git, Calendar, Datetime

## Screenshots

_Add screenshots of your platform here to visually showcase your project._

#### Home

![HOME](screenshots/home.png)

### Sponsor Registration

![Sponsor Registration](screenshots/sponsor_reg.png)

### Influencer Registration

![Influencer Registration](screenshots/influencer_reg.png)

### User Login

![User Login](screenshots/userLogin.png)

### Sponsor Dashboard

![Sponsor Dashboard](screenshots/SponDashboard.png)

### Sponsor Dashboard: Campaigns

![Sponsor Campaigns](screenshots/sponCampaigns.png)

![Sponsor Campaigns2](screenshots/sponCamp2.png)

### Sponsor Dashboard: Add Campaign

![Add Campaigns](screenshots/addCamp.png)

#### Select Influencer for private campaign

![Sponsor Registration](screenshots/selectInfCreateCamp.png)

### Sponsor Dashboard: Search

![Search Campaigns](screenshots/sponSearch.png)

### Sponsor Dashboard: Statistics

![Statistics](screenshots/sponStat.png)

#### Influencer Dasboard

![Influencer Dashboard](screenshots/infDashboard.png)

##### Edit Profile

![Influencer Edit Profile](screenshots/infeditprof.png)

### Influencer Dashboard: Public Campaign

![Public Campaigns](screenshots/infdashpubcamp.png)

![Public Campaigns -details](screenshots/infcamppubreq.png)

![Public Campaigns -details](screenshots/infdashpubdetails.png)

### Influencer Dashboard: Search

![Search Campaigns](screenshots/infdashSearch.png)

### Influencer Dashboard: Statistics

![Influencer Statistics](screenshots/infdashstats.png)

### Admin Dashboard

![Stats](screenshots/adminDash1.png)

![Stats2](screenshots/adminDash2.png)

![Stats3](screenshots/adminDash3.png)

### Admin Dashboard: Sponsors

![Sponsors](screenshots/adminSpon.png)

### Admin Dashboard: Influencer

![Influencer](screenshots/adminInf.png)

![FlaggedInfluencer](screenshots/flaggedUser.png)

### Admin Dashboard: Campaigns

![Campaign](screenshots/admincamps.png)

### Admin Dashboard: AdRequests

![Adrequests](screenshots/adminAdreq.png)

## Demo

You can check the live demo of the platform here: **[Live Demo Link](#)**  
_(Link will be updated after deployment)_

## Installation

To run this project locally, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/itsVaibhavSharma/IESCP.git
   cd IESCP
   ```

2. **Create a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**:
   Initialize the SQLite database and tables by running:

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. **Run the application**:

   ```bash
   flask run
   ```

6. **Access the app**:
   Open your browser and go to `http://127.0.0.1:5000/`.

## Usage

1. **Sponsor**: Register and log in as a Sponsor to create, edit, update and view campaigns, view influencers, manage ad requests, search and check statistics.
2. **Influencer**: Sign up as an Influencer to explore public campaigns and submit ad requests, accept, view and delete adrequests for private campaigns, search and view statistics.
3. **Admin**: Log in as an Admin to monitor activities (statistics), flag users, and manage campaigns and adrequests.

## Database Schema

| **Table Name** | **Description**                                                                                                               | **Columns**                                                                                                                                         |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Admin`        | Stores admin information such as name, email, and password.                                                                   | `id`, `name`, `email`, `password`                                                                                                                   |
| `Influencer`   | Stores influencer details including name, email, category, niche, reach, balance, and flagged status.                         | `id`, `name`, `email`, `password`, `category`, `niche`, `reach`, `balance`, `flagged`                                                               |
| `Sponsor`      | Stores sponsor details like name, email, budget, industry, age, and flagged status.                                           | `id`, `name`, `email`, `password`, `budget`, `industry`, `age`, `flagged`                                                                           |
| `Campaign`     | Stores campaign details such as name, description, budget, start date, end date, goals, visibility, and sponsor relationship. | `id`, `name`, `description`, `start_date`, `end_date`, `budget`, `visibility`, `goals`, `sponsor_id`, `progress`, `stat`, `flagged`                 |
| `AdRequest`    | Stores ad requests made by influencers, including message, requirements, payment amount, and request status.                  | `id`, `campaign_id`, `influencer_id`, `message`, `requirements`, `payment_amount`, `status`, `negotiation`, `negotiation_amt`, `for_who`, `flagged` |

### ER Diagram

![ER](screenshots/dbschema.png)

## Deployment

The application will be deployed to **[Platform Name]** soon. Stay tuned for the link!

## Future Enhancements

- **Real-time Notifications**: Email or SMS notifications for new campaigns and ad requests.
- **Enhanced Reporting**: Advanced data analytics for better campaign insights.
- **Payment Integration**: Integrate payment gateways for campaign funding.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request. For major changes, open an issue first to discuss what you'd like to change.

## Contact

If you have any questions or feedback, feel free to reach out:

- **Vaibhav Sharma**  
  Email: [itsVaibhavSharma007@gmail.com](mailto:itsVaibhavSharma007@gmail.com)
  GitHub: [@itsVaibhavSharma](https://github.com/itsVaibhavSharma)

# Project Documentation
#### Luke Morton ####
#### 10621189 ####
#### September 2023 ####

## Introduction
The aim of this project was to develop an Information System for a particular area of interest. In my case, I chose to build an IS that could be used by freelancers to log and track their incoming jobs.

The project was built using the following technologies: Flask, Python, SQLite, HTML, CSS, and JavaScript. Towards the end of the project, it was also deployed into Azure App Service.

## Requirements
The requirements for the project were as follows:
* The system can use any back end
* The system can use any front end
* The system can use any programming language
* The system must include at least two user types
* Data can be searched, sorted, entered, updated, validated
* Reports can be generated
* The system must be documented and tested
* The code and documentation must be stored in a version control system such as GitHub
* Code must be attributed and licences used correctly
* A presentation must be delivered at the end of the semester

## Database Design
Different database solutions were considered at the planning stage of the project however I decided to go with SQLite for a few reasons. Firstly it's familiar, having worked with it in previous modules and having an understanding of SQL. 

Secondly, SQLite is incredibly lightweight and is perfect for a small-scale application such as this.

The database entity relationship diagram was first planned and designed using Lucid. I then created the schema and database initialisation files in my project.

![B8IT150 ERD](https://github.com/LukeM94/B8IT150-CA/assets/1420218/bd34e5e6-201d-488d-ae0f-8ee787892c3c)


## Architecture
The front end uses HTML templates. I was able to create a base HTML template that included foundation page components including the nav bar and footer. The other pages such as login, then inherit the base template.

I also made extensive use of Bootstrap for the front end. Bootstrap is an extremely powerful system that allowed me to use components that are responsive and professional-looking.

The back end uses Flask which is a Python web framework. Flask uses routes to create the URL endpoints and handles the requests for those endpoints. I chose to use Flask as I've worked with C# and ASP.NET in a previous module and wanted to learn some new skills.

The application was deployed to Azure App Service. When configuring Azure App Service, I took advantage of the code being stored in GitHub to add a GitHub Action that would deploy the latest version of my project was changes were pushed to the repo.

## Testing

The below test cases were created to ensure the system meets the requirements mentioned above. 

| Test ID | Test Description | Expected Result | Actual Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| 1 | User can register an account | User is registered and redirected to login page | User is registered and redirected to login page | PASS |
| 2 | User can log in | User is logged in and redirected to profile | User is logged in and redirected to profile | PASS |
| 3 | User can log out | User is logged out and redirected to the homepage | User is logged out and redirected to the homepage | PASS |
| 4 | Any user can view the homepage | Homepage is displayed | Homepage is displayed | PASS |
| 5 | Any user can view the about page | About page is displayed | About page is displayed | PASS |
| 6 | Any user can view the register page | Register page is displayed | Register page is displayed | PASS |
| 7 | Any user can view the login page | Login page is displayed | Login page is displayed | PASS |
| 8 | Only an authenticated user can view the jobs page | Jobs page displayed only when logged in | Jobs page is displayed | PASS |
| 9 | Only an authenticated user can view the search page | Search page displayed only when logged in | Search page is displayed | PASS |
| 10 | Only an authenticated user can view the create job page | Create job page displayed only when logged in | Create job page is displayed | PASS |
| 11 | Only an authenticated user can view the calendar page | Calendar page displayed only when logged in | Calendar page is displayed | PASS |
| 12 | Only an authenticated user can view the profile page | Profile page displayed only when logged in | Profile page is displayed | PASS |
| 13 | Only an authenticated admin user can view the admin page | Admin page displayed only when logged in as an admin | Admin page is displayed | PASS |
| 14 | A user can create a job via the create job page  | Job is created and the user is redirected to the jobs page | Redirected to the jobs page and the newly created job is visible in the table | PASS |
| 15 | A job report can be generated with a list of the current users jobs | A PDF job report opens with every job created by the current user | PDF report is generated and contains a list of the expected jobs | PASS |
| 16 | A user can modify a job via the jobs page | Modified job data is saved and appears on the job details page | Redirected to the jobs page and the modified data is saved | PASS |
| 16 | A user can delete a job via the jobs page | Job is deleted from the system and no longer visible | Redirected to the jobs page and deleted job is not visible in the table | PASS |
| 17 | A user can search for a job via the search page | Only jobs matching the search term are returned | Jobs matching the search term are displayed in the table | PASS |
| 18 | A user can sort jobs by title, description, or status | Jobs are sorted in ascending or descending order | Jobs are sorted correctly based on the sort options clicked on the table headings | PASS |
| 19 | A user can view their jobs on the calendar | Jobs appear on the calendar based on their deadline date | Jobs appear on the calendar on the day that they are due | PASS |


## Conclusion
If I had more time to spend on the project there are a number of features I'd like to implement. One of these would be a payment function where customers of freelancers could pay their invoices. A payment system could be built from scratch however there are many considerations, especially around security. A more straightforward solution if I was to develop this would be to integrate a third-party service like Stripe or PayPal.

Another learning experience was using Overleaf to write the documentation in LATEX. I hadn't used LATEX before and found that while it's an incredibly powerful tool, it's also complex and I did struggle with things like table formatting. I decided to switch to Markdown for the documentation. The added bonus of using Markdown was the ability to work on my docs directly in VS Code where I was already writing code.

## References

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

## Architecture
The front end uses HTML templates. I was able to create a base HTML template that included foundation page components including the nav bar and footer. The other pages such as login, then inherit the base template.

I also made extensive use of Bootstrap for the front end. Bootstrap is an extremely powerful system that allowed me to use components that are responsive and professional-looking.

The back end uses Flask which is a Python web framework. Flask uses routes to create the URL endpoints and handles the requests for those endpoints.

The application was deployed to Azure App Service. When configuring Azure App Service, I took advantage of  the code being stored in GitHub to add a GitHub Action that would deploy the latest version of my project was changes were pushed to the repo.

## Testing

| Test ID | Test Description | Expected Result | Actual Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| 1 | User can register an account | User is registered and redirected to login page | User is registered and redirected to login page |  |
| 2 | User can log in | User is logged in and redirected to profile | User is logged in and redirected to profile |  |
| 3 | User can log out | User is logged out and redirected to the homepage | User is logged out and redirected to the homepage |  |

## Conclusion
If I had more time to spend on the project there are a number of features I'd like to implement. One of these would be a payment function where customers of freelancers could pay their invoices. A payment system could be built from scratch however there are many considerations, especially around security. A more straightforward solution if I was to develop this would be to integrate a third-party service like Stripe or PayPal.

Another learning experience was using Overleaf to write the documentation in LATEX. I hadn't used LATEX before and found that while it's an incredibly powerful tool, it's also complex and I did struggle with things like table formatting. I decided to switch to Markdown for the documentation. The added bonus of using Markdown was the ability to work on my docs directly in VS Code where I was already writing code.

## References
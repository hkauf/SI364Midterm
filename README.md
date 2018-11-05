My app is an opentable app that allows you to search restaurants by name or search by location and price range. 
The name search output will provide you with restaurants with the name that you searched or will contain that name within a larger name, the address (street, city, state), the open table reservation link, and the price range that open table provides on a scale of 1-4.
The location search will provides you with restaurants in that area, their address (street, city, and state), and the open table reservation link

**Note some of the opentable links will not work due to the fact that the restaurants are no longer on OpenTable**

Requirements:
**-Ensure that the SI364midterm.py file has all the setup (app.config values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on http://localhost:5000 (and the other routes you set up)**
**-Ensure that all templates in the application inherit (using template inheritance, with extends) from base.html and include at least one additional block.**
**-Include at least 2 additional template .html files we did not provide.
At least one additional template with a Jinja template for loop and at least one additional template with a Jinja template conditional.**
**-These could be in the same template, and could be 1 of the 2 additional template files.**
**-At least one errorhandler for a 404 error and a corresponding template.**
**-At least one request to a REST API that is based on data submitted in a WTForm.**
-At least one additional (not provided) WTForm that sends data with a GET request to a new page.
**-At least one additional (not provided) WTForm that sends data with a POST request to the same page.**)
**-At least one custom validator for a field in a WTForm.**
**-At least 2 additional model classes.**
**-Have a one:many relationship that works properly built between 2 of your models.**
**-Successfully save data to each table.**
**-Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for).**
**-Query data using an .all() method in at least one view function and send the results of that query to a template.**
**-Include at least one use of redirect. (HINT: This should probably happen in the view function where data is posted...)**
**-Include at least one use of url_for. (HINT: This could happen where you render a form...)**
**-Have at least 3 view functions that are not included with the code we have provided. (But you may have more! Make sure you include ALL view functions in the app in the documentation and ALL pages in the app in the navigation links of base.html.)**
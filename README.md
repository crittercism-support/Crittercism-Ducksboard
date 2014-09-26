Crittercism-Ducksboard Integration
======================

This serves as a sample proof of concept to show some of the things the Crittercism API can do when combined with another BI tool. A screenshot of the dashboard can be seen here: [Click Me!](http://i.imgur.com/BK6bxH1.png). This isn't the best code, feel free to refine it, or add more features that suit your needs.

This script utilizes the unirest library http://unirest.io/python.html. 

Please note: widgets/charts/graphs will first need to be generated via the Ducksboard portal, then you can push data using this script to each widget/chart/graph. Within the script you'll see notes on what type of widget/chart/graph will need to be generated ahead of time. Please e-mail me at ajohal@crittercism.com if you have any questions.


Upcoming Fixes
======================
* Dynamic generation of Crittercism Access Token upon expiration.
* Adjust code to populate past data, currently data starts from the first day this script is run, meaning it can take some days/weeks for certain charts to fill up.
* Possibly add widget/chart/graph creation as a part of this script, so that you never need to manually create a new widget unless need be.

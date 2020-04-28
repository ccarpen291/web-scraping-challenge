# web-scraping-challenge

This is a web tool that literally goes to mars, retreives data and publishes it to the internet

We are using a few different websites to gather the data. The most important ones I find interesting are the daily twitter feed.

This was a little hard to scrape on the internet because you have to use an xpath and that does not always work for individual users.
It is still not clear why my xpath would not copy the full xpath on my computer but I had to end up using the path of an individual who's it would work
I will have to figure this out in the future but for now it works just fine

Additionally, we pull some fun facts using pandas.  This was interesting because pandas pulls all the tables on a webpage and returns them as a list
So this basically lets you call the tables and use numbers to call the tables.  Luckily, the fun facts we wanted to pull about Mars
Was on the first table, so we just had to call table 0 as it was the first table in a list.

Finally, we pulled a few different images and really just saved the html of those images where the image is being saved on the website
and we are just using our website as a repeater



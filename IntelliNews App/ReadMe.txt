Instructions for the Backend

First install requirements.txt, next you will likely need to adjust the transformers device in "condenser.py". Currently, the device is "mps" which will likely work on all M-series Apple computers, but if you are not using that hardware you will need to determine the device on your machine. Now the program should be ready to run, if you wish to run the process once, run "main.py", if you wish to schedule it to run every 24 hours, run "scheduler.py". If you wish to run the summary through external models, you must get an api key for groq cloud.

The entire process will take a few hours to run depending on your hardware


Instructions for the Frontend

Open terminal and navigate to the "intellinews-client" folder. Use the command "npm ci" to install dependencies, then execute "npm run dev", this will launch the webpage on the local host. Finally, enter the address in a web-browser to view the news summaries.
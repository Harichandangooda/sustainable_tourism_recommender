# sustainable_tourism_recommender
Travel Smart: Developing a Recommendation System for Promoting Sustainable Tourism

Team Number: 19

Team Member 1  
Name: Hari Chandan Gooda  
UBIT: 50614165
Question: Predicting Rating Classification Using Decision Tree

Code Location : Phase_3_Notebook.ipynb 13th-14th cell

Analysis Location : 3rd Question in Analysis.pdf

Team Member 2  
Name: Pramila Yadav  
UBIT: 50613803

Question: Popular Times Classification for Each Hour Using KNN

Code Location : Phase_3_Notebook.ipynb 10th cell

Analysis Location : 4th Question in Analysis.pdf

Team Member 3  
Name: Keshav Narayan Srinivasan  
UBIT: 50610509  

Question: Predicting Working Hours from Popular Times Data using Random Forest

Code Location : Phase_3_Notebook.ipynb 6th-9th cell

Analysis Location : 1st Question in Analysis.pdf

Team Member 4  
Name: Tharunnesh Ramamoorthy  
UBIT: 50611344

Question: Closest 5 Places for Each Place Using BallTree

Code Location : Phase_3_Notebook.ipynb 11th cell

Analysis Location : 2nd Question in Analysis.pdf

Folder Structure Information:
The app data is contained within the app folder (/app) and Phase 1 and Phase 2 files are stored in the exp folder respectively(/exp/Phase_1 and /exp/Phase_2).

The app folder contains the app code and the Python Notebook consisting of running of Models used for phase 3 in the Phase_3_Notebook.ipynb file. It also contains the csv files that are required to run the application. There is also a subfolder named pages which is a streamlit method to have a multipage app.

Instructions to run the application:

Kindly install the following libraries using the following commands if needed:
pip install streamlit
pip install psycopg2
pip install sqlalchemy
pip install folium
(Use Python 3.12 if possible)

Open the app folder in vscode and use the following command:
python -m streamlit run Database.py.

You can see the video attached in the ublearns submission to understand how our app works and what it does (Since Github restricted files to 20mb we uploaded it in the zip file).
Kindly Note: We have used Google Cloud SQL to store the csv as a table in our PostgreSQL database, so we have not included the Host address and Password in the GitHub code for safety reasons. The UBLearns submission code has the host address and Password included to run the code :)

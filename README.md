# AUT-VIRTUAL-INTERNSHIP
WEBSITE DEVELOPMENT FOR YESENERGY BACKEND PART
***********************************
>CALCULATING RMSE FOR SELECTED INTERVAL
***********************************
>DISPLAYING GRAPH
***********************************
*************CREATE VIRTUAL ENVIORNMENT***************
***********************************
conda create --name energy_dashboard python=3.8
***********************************
conda activate energy_dashboard
***********************************
***********MAKE NECESSARY FILES***********
***********************************
mkdir energy_dashboard
***********************************
cd energy_dashboard
***********************************
mkdir app data
***********************************
notepad app\__init__.py
***********************************
notepad app\routes.py
***********************************
notepad run.py
***********************************
notepad data\forecasts.csv
***********************************
notepad requirements.txt
***********************************
*******JSON FILES*******
***********************************
filter_data.json
***********************************
graph_data.json  ****dispaly actual timeseries*****
***********************************
rmse_data.json ********set the rmse data range ,out of given range will be displayed****
***********************************
rsme_graph_data.json ******graph of rmse data selected*****

***********************************
*************CREATE ACTUAL PRICE*************
***********************************
generate_sctual_prices.py
***********************************
********INSTALL DEPENDENCIES********
***********************************
pip install -r requirements.txt
***********************************
**********RUN THE APPLICATION****************
***********************************
python run.py
***********************************
***********GET REQUEST IN ANOTHER BASE ENVIRONMENT*********
***********************************
cd path\to\your\energy_dashboard
***********************************
curl -X POST -H "Content-Type: application/json" -d @filter_data.json http://127.0.0.1:5000/filtered_data
***********************************
curl -X POST -H "Content-Type: application/json" -d @rmse_data.json http://127.0.0.1:5000/filtered_statistics
***********************************
*******TO DISPLAY GRAPH********
***********************************
curl -X POST -H "Content-Type: application/json" -d @graph_data.json http://127.0.0.1:5000/graph --output graph.png
***********************************
curl -X POST -H "Content-Type: application/json" -d @rmse_graph_data.json http://127.0.0.1:5000/rmse_graph --output rmse_graph.png
***********************************
This will save the RMSE graph image as rmse_graph.png.

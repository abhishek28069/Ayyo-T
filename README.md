## How to run?
1. install the requirements in requirements.txt
        `pip3 install -r ./requirements.txt`
2. go to in-cse file and run
        `./start.sh`        
   for running the onem2m server (localhost:5089/webpage)
3. go to sensor_manager/onem2m_interface and run
        `python3 onem2mapi.py`
        `python3 onem2mDatawarehouse.py`
   to run our flask api (localhost:8069)
4. go to `./sensor_manager/sensor_query` and run
        python3 query_server.py
5. go to `./ui/sensormanager_frontend` and run
         `npm install`
         `npm run dev`
   to open the frontend (localhost:5173)

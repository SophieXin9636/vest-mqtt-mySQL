# Intelligent Chest Care Vest with MQTT & Database

## Environment
* Ubuntu 18.04 (or 20.04)
* python3

## Intall the dependencies
```
pip3 install -r requirements.txt
```

## Usage

Step1. Establish a Database
Step2. Create Subsciber
Step3. After Receiving Force Data, it will store data into the Database

### Establish a Database
```sh
python3 init_DB.py
```

### Create Subscriber and API Handler

* API Handler
	* Project Database
		* Connect MySQL Database
		* Execute Query
	* Force Data Handler
		* Add data into list
		* Calculate Average Force
		* Statistic patting level (soft, medium, hard)
		* Add SQL Query
		* Receive sound file and json data (using socket)
		* Store data into Project Database
		* Split sound into Frames
		* Create Spectrogram
		* Sound Recognition

```sh
python3 api_handler.py
```
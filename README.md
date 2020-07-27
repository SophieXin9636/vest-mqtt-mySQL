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

### Create Subscriber
```sh
python3 mqtt_sub_data.py
```
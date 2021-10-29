# Challenge Python L1 - Prueba Tecnica ZINOBE

This repository contains the development of the application requested for the backend python technical test of the company ZINOBE.

## Installation

1. Create a python virtual environment to install the dependencies.
2. Activate the virtual environment created in step 1.
3. Execute the following which installs the necessary dependencies for the execution of the application found in the file requirements.txt

  ```bash
     python3 -m venv venv
     pip install -r requirements.txt
  ```

## Usage
 ```
Once the installation steps have been completed, proceed to execute the python file "app.py" which contains the application.
```

## Testing
 ```
Once the installation steps have been completed, proceed to execute the python file "test.py" which contains the test cases suite for the application.
```

## Description

1. The "regions" table is created in the sqlite database to store the calculated execution times of the dataframe.
2. The application makes a request via api rest to the endpoint "https://restcountries.com/" which will obtain the regions, and languages of the countries provided there.
3. Once the country, region and language have been obtained, the country's speech language is encrypted using the sha-1 function.
4. We proceed to create the row in the dataframe and calculate the time it takes to create it.
5. Once the table with the required information has been created, the total time, average time, minimum time and maximum execution time are calculated.
6. Once the times have been calculated, they are inserted into the sqlite database in the regions table, previously created in step 1.
7. The dataframe created is exported in a .json file which contains the name data.json and will be stored in the path "exports"

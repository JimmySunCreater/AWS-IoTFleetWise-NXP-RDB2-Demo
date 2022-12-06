# Deploying Amazon Managed Grafana incl. sample dashboards.

This repository contains guidelines for quickly setting up Amazon Managed Grafana dashboards to demonstrate analysis of data stored in Amazon Timestream by AWS IoT FleetWise service. 



## Before you start

Please note that the guidelines in this repository assume that you already have Amazon Timestream table with the vehicle data ingested by AWS IoT FleetWise. If you not at that point yet, you can consider the following options:
- **Simulation approach**: can use the following AWS internal guidelines: [https://w.amazon.com/bin/view/AWS_Automotive/Kaleidoscope/Developers/Trainings/](https://w.amazon.com/bin/view/AWS_Automotive/Kaleidoscope/Developers/Trainings/).
- Connect physical vehicle to AWS IoT FleetWise

**Big red warning: dashboard models in this repository assume that your Timestream database is called `FleetWiseDatabase` and your Timerstream tabel is called `VehicleDataTable`.  So you have 2 options: either change the Timestream resource naming, or search/replace in the JSON files with dashboard models to the Timestream database and table names you use.** 


## Deployment instructions

### Step 1: Configure SSO

1. **Activate SSO**
    If SSO is not activated yet in your account, do so via [https://console.aws.amazon.com/singlesignon/home](https://console.aws.amazon.com/singlesignon).

2. **Add groups**
    Add SSO groups "Demo_Admins" and "Demo_Viewers":
    - **Demo_Admins** will be able to add and edit AMG dashboards 
    - **Demo_Viewers** will be only able to view dashboards
  
3. **Add users**
    Add SSO users via [https://us-east-1.console.aws.amazon.com/singlesignon/identity/home?region=us-east-1#!/users](https://us-east-1.console.aws.amazon.com/singlesignon/identity/home?region=us-east-1#!/users). Adjust region if necessary. **You can have SSO service and AMG in different regions!**

4. **Add users to groups**
    Now add SSO users to SSO groups "Demo_Admins" and "Demo_Viewers".


### Step 2: Deploy AMG workspace

``` shell
# Change region if required
AWS_REGION=eu-west-1
# If you dont have it yet
npm install -g aws-cdk    
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cdk bootstrap
cdk deploy
```

### Step 3: Configure SSO

**Skip this step if you have previously configured SSO in this account**
 
1. Open your workspace by navigating to [https://console.aws.amazon.com/grafana/home?#/workspaces/](https://console.aws.amazon.com/grafana/home?#/workspaces/)

2. Navigate to "SSO Configuration", "Configure users and user groups", "Assigned user groups".

3. Click on "Assign user group" button , navigate to "Groups" 

4. Checkbox Demo_Admins

5. Click "Assign users and groups"

### Step 4: Log in to AMG workspace 

Open your AMG workspace by clicking on your workspace URL (you can retrieve it via AMG console by navigation to the workspace)

### Step 5: Add Timestream Data source

![](images/Amazon_Timestream__Settings_-_Amazon_Managed_Grafana.png)

1. Go to "Configuration" , Data Sources and click on "Add Data Source"

2. Add Timestream Data source

3. Go to Timestream Data source configuration

4. Set the name to "Amazon Timestream FleetWise". **Big Read Warning: you MUST use exactly this name of the data source, as the dashboard models refer to it**.

5. Set "Default region" to the region where your Timestream database resides.

6. **Dont be worried if your database is not listed under "Select database".**

7. Click on "Save and test", you should see "Connection success"

### Step 6: Import dashboards

![](images/Import__Import_-_Amazon_Managed_Grafana.png)


1. Locate one of the following files in your file system (see folder `dashboardmodels` of this repo):
   1. usecase1-issuedetect-dashboard.json
   2. usecase2-overheatanalysis-dashboard.json
   3. usecase3-adhocsnapshot-dashboard.json


2. Click on "+" symbol on the left pane and then on "Import"

3. You should see the dashboard now. If you face problems, please see "Troubleshooting" section.

4. Questions or need help? Slack me at svirida@


## Troubleshooting

**I added dashboards but they dont show data or show errors**

- **Check 1.** Dashboard models in this repository assume that your Timestream database is called `FleetWiseDatabase` and your Timerstream tabel is called `VehicleDataTable`. So you have 2 options: either change the Timestream resource naming, or search/replace in the JSON files with dashboard models to the Timestream database and table names you use. 
   
- **Check 2**: Did you set the name of Timestream data source to "Amazon Timestream FleetWise"? you MUST use exactly this name of the data source, as the dashboard models refer to it. 
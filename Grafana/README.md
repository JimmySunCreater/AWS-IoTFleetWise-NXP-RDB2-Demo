# Introduction of Amazon Managed Grafana Deplpy and Run
This section describes how to quickly setting up Amazon Managed Grafana dashboards to demonstrate analysis of data stored in Amazon Timestream by AWS IoT FleetWise service.
## Prerequisites
Amazon Timestream table with the vehicle data ingested by AWS IoT FleetWise should be created ahead, if not, please refer to Introduction of Amazon IoTFleetwise Deploy and Run.
## Deploy and Run
Step 1: Configure SSO

1. Activate SSO
If SSO is not activated yet in your account, do so via [https://console.aws.amazon.com/singlesignon/home](https://console.aws.amazon.com/singlesignon).
2. Add groups
Add SSO groups "Demo_Admins" and "Demo_Viewers":
Demo_Admins will be able to add and edit AMG dashboards
Demo_Viewers will be only able to view dashboards
3. Add users
Add SSO users via [https://us-east-1.console.aws.amazon.com/singlesignon/identity/home?region=us-east-1#!/users](https://us-east-1.console.aws.amazon.com/singlesignon/identity/home?region=us-east-1#!/users). Adjust region if necessary. You can have SSO service and AMG in different regions!
4. Add users to groups
Now add SSO users to SSO groups "Demo_Admins" and "Demo_Viewers".
Step 2: Deploy Amazon Managed Grafana workspace
Download AmazonManagedGrafanaDeploy and run the following commands
```
cd <path to AmazonManagedGrafanaDeploy>
AWS_REGION=us-east-1
npm install -g aws-cdk    
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cdk bootstrap
cdk deploy
```

Step 3: Configure SSO
Skip this step if you have previously configured SSO in this account

1. Open your workspace by navigating to [https://console.aws.amazon.com/grafana/home?#/workspaces/](https://console.aws.amazon.com/grafana/home?#/workspaces/)
2. Navigate to "SSO Configuration", "Configure users and user groups", "Assigned user groups".
3. Click on "Assign user group" button , navigate to "Groups"
4. Checkbox Demo_Admins
5. Click "Assign users and groups"

Step 4: Log in to AMG workspace
Open your AMG workspace by clicking on your workspace URL (you can retrieve it via AMG console by navigation to the workspace)

Step 5: Add Timestream Data source

1. Go to "Configuration" , Data Sources and click on "Add Data Source"
2. Add Timestream Data source
3. Go to Timestream Data source configuration
4. Set the name to "Amazon Timestream FleetWise". 
5. Set "Default region" to the region where your Timestream database resides.
6. Dont be worried if your database is not listed under "Select database".
7. Click on "Save and test", you should see "Connection success"

Step 6: Import dashboards
Click on "+" symbol on the left pane and then on "Import"
Choose AWS IoT FleetWise RDB2 - Signal overview.json to import json configuration.

Now it's ready to use.
>Note: Some of the configurations come from svirida@, thank you for your contribute.
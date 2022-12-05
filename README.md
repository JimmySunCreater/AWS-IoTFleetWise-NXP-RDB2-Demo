# Brief of AWS IoT Fleetwise Demo Guide
AWS IoT FleetWise is a managed service that allows automakers or car rental companies to collect vehicle data, transform it, and then transfer it to the cloud to gain insights about  fleet(s) of vehicles. Automakers can use the data transferred by AWS IoT FleetWise to analyze vehicle fleet health to quickly identify potential maintenance issues, make in-vehicle infotainment systems smarter, or use analytics and machine learning (ML) to improve models for autonomous driving and advanced driver assistance systems (ADAS).Car rental companies can use it to monitor the vehicle status to provide refined vehicle maintenance and customer assistant services.

AWS IoT FleetWise removes the complexities of collecting data from vehicle fleets at scale. Using virtual vehicle modeling, users can create a common data format across vehicle brands, models, and components, allowing for streamlined fleet-wide data analysis in the cloud.

AWS IoT FleetWise also helps users more intelligently collect vehicle data, which provides users access to more useful data in the cloud. Users can improve data relevance by creating time- and event-based data collection campaigns that send the exact data you need to the cloud.

This guide is intended to demonstrate the  features of AWS IoT FleetWise by building AWS IoT FleetWise Edge Agent and running it on NXP-S32G-VNP-RDB2 as vehicle gateway,by using CARLA to simulate vehicle ECU data,by deploying a time-based campaign in AWS IoT FleetWise to collect data from the virtual vehicle,by data visiualization using Amazon Managed Grafana.
## Prerequisites
It's assumed that you have got aws account and config aws cli with administrator rights.
>Note: AWS IoT FleetWise is currently available in US East (N. Virginia) and Europe (Frankfurt).
# Architecture
![IoTFleetwise%20RDB2_02.png](https://github.com/JimmySunCreater/AWS-IoTFleetwise-NXP-RDB2-Demo/blob/main/IoTFleetwise%20RDB2%20Architecture.png)
## Models/Services and usage
* [Carla](http://carla.org/)

  CARLA is an open-source autonomous driving simulator. It was built from scratch to serve as a modular and flexible API to address a range of tasks involved in the problem of autonomous driving.This demo use carla to simulate ECUs in the vehicle and send encoded data to the signal collecter(NXP-S32G-VNP-RDB2)in format of CANBus.
* [NXP-S32G-VNP-RDB2](https://www.nxp.com/design/designs/s32g2-vehicle-networking-reference-design:S32G-VNP-RDB2)

  The S32G-VNP-RDB2 is a compact, highly optimized and integrated board engineering for vehicle service-oriented gateway (SoG), domain control applications, high-performance processing, safety and security applications. This demo use S32G-VNP-RDB2 as vehicle gateway. It receives CAN data from CARLA by interface CAN0,on the other hand, IoT Fleetwise edge agent is deployed to inspect and upload following the campaign schema from FleetWise.
* [AWS IoT FleetWise](https://aws.amazon.com/iot-fleetwise/)

  IoT Fleetwise is used for virtual vehicle modeling,signal decoder creation and campaign deploy in the demo.
* [Amazon Timestream](https://aws.amazon.com/timestream/)
  
  Amazon Timestream is a fast, scalable, and serverless time series database service for IoT and operational applications that makes it easy to store and analyze trillions of events per day up to 1,000 times faster and at as little as 1/10th the cost of relational databases. The payload will be decoded by IoT service and stored by memory store or magnetic store.
* [AWS IoT Core](https://aws.amazon.com/iot-core/)

  AWS IoT Core is a managed cloud platform that lets connected devices easily and securely interact with cloud applications and other devices. This demo use IoT Core to establish a secure connection to the device through a certificate, data exchange via MQTT with low latency and with low overhead, filter, transform, and route the data to Timestream for further processing and analytics.
* [Amazon S3](https://aws.amazon.com/s3/)

  Amazon S3 is object storage built to store and retrieve any amount of data from anywhere.This demo us it to store decoded vehicle data from Timestream for persistent storage.
* [Amazon Managed Grafana](https://aws.amazon.com/grafana/)

  Amazon Managed Grafana is a fully managed service with rich, interactive data visualizations to help customers analyze, monitor, and alarm on metrics, logs, and traces across multiple data sources. This demo use AMG to visualize near-realtime data such as vehicle speed,gear and perform statistical analysis such as collision time and collision severity.
## Environment and Dashboard
Environment
![Environment.png](https://github.com/JimmySunCreater/AWS-IoTFleetwise-NXP-RDB2-Demo/blob/main/Environment.png)

Grafana Dashboard
![GrafanaDashboard](https://github.com/JimmySunCreater/AWS-IoTFleetwise-NXP-RDB2-Demo/blob/main/Grafana/Grafana%20Gauge.png)

# Deploy and Run
The procedures to deploy and run the demo are as follows while please refer to the git folders for detailed configuration.
* * *
**1. Model vehicle and create campaign**

A virtral vehicle model need to be created in IoT FleetWise to perform data signal creation and decode manifest by using .dbc file. A virtual vehicle linking with the vehicle model and decode manifest is also required. This virtual vehicle is attached in IoT Core which represents the RDB2. Campaigns will be deployed to the RDB2 once it is approved. Campaigns give the Edge Agent software instructions on how to select, collect, and transfer data to the cloud. 
* * *
**2. Campaign approval and release**

The compaign will be deployed once user approved the campaign. If you want to pause collecting data from vehicles connected to the campaign, on the Campaign summary page, choose Suspend. To resume collecting data from vehicles connected to the campaign, choose Resume.
>Detailed configuration for step 1 and 2 can be reached at <u>[/Fleetwise/README.md](https://github.com/JimmySunCreater/AWS-IoTFleetwise-NXP-RDB2-Demo/blob/main/Fleetwise/README.md)</u>
* * *
**3. Vehicle Authentication**

The RDB2 is used as vehicle gateway to upload data, IoT FleetWise Edge Agent need to be deployed in RDB2 as application and a certification is also needed for authentication to perform legal communication with IoT Core. 
>Detailed configuration can be reached at [/NXP-VNP-RDB2/README.md](https://github.com/JimmySunCreater/AWS-IoTFleetwise-NXP-RDB2-Demo/blob/main/NXP-VNP-RDB2/README.md)
* * *
**4. Deploy data collection schema**

Data Collection Schemes describes what and how to collect signal, it is generated at step 1, once it is approved at step2, the scheme will be deployed to IoT FleetWise Edge Agent automatically.
* * *
**5. Data encode using canbus dbc file**

The DBC file(CAN database files)is a simple text file that consists of information for decoding raw CAN bus data to physical values in human readable form or encoding physical values to CAN bus data. DBC file is used as shared schema for data exchange from the car and cloud in this demo. Python code is used to convert CARLA physical values(decimal) to ECU CAN bus values（hexadecimal）and ingest to RDB2.
* * *
**6. Data ingestion**
Since CARLA is install in a server, a usb to CAN converter is used to transfer the digital data into CAN bus logic level signal. CAN high/low are connected to FLEX_CAN0_H/L.
>Detailed configuration for step 5 and 6 can be reached at [/CARLA/README.md](https://github.com/JimmySunCreater/AWS-IoTFleetwise-NXP-RDB2-Demo/blob/main/CARLA/README.md)
* * *
**7. Inspect canbus data and package**
The IoT FleetWise Edge Agent will specify what data to collect and which collection triggers to inspect data following rules of Data Collection Schemes. 
* * *
**8. Upload data payload**
The data will be packed and send to IoT Core by IoT FleetWise Edge Agent.
* * *
**9. Store vehicle data**
The data will be stored at Amazon Timestream.
>Detailed configuration for Timestream can be reached at [Fleetwise/README.md](https://github.com/JimmySunCreater/AWS-IoTFleetwise-NXP-RDB2-Demo/blob/main/Fleetwise/README.md)
* * *
**10. Config visualization specification**

* * *
**11. Query data and process**
* * *
**12. Data visualization**
* * *
**13. Persistent storage**
The vehicle data can be stored to Amazon s3 for persistent, low-cost storage.

# Getting Help
It's welcome to contact if you have any technical questions about the demo.
# Resources
The following documents are used for reference for the construction of this demo,appreciate the efforts of the authors.
* [AWS IoT FleetWise Developer Guide](https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/what-is-iotfleetwise.html) provides key concepts and instructions for using AWS IoT FleetWise service.
* [AWS IoT FleetWise Edge Agent Developer Guide](https://github.com/aws/aws-iot-fleetwise-edge/blob/main/docs/dev-guide/edge-agent-dev-guide.md) provides step-by-step instructions for building and running Edge Agent Reference Implementation for AWS IoT FleetWise.
* [AWS IoT FleetWise API Reference](https://docs.aws.amazon.com/iot-fleetwise/latest/APIReference/Welcome.html) describes all the API operations for FleetWise.
* [Demo-Auto-Aws IoT Fleetwise](https://github.com/aws4embeddedlinux/demo-auto-aws-iotfleetwise) provides a demo using AWS Graviton and RDB2+carla to simulate vehicle.
* [AWS IoT FleetWise demo kit](https://gitlab.aws.dev/emea-iot-specialist-sa/aws-iot-fleetwise-demokit/-/tree/main/grafana_dashboards) contains guidelines for quickly setting up Amazon Managed Grafana dashboards to demonstrate analysis of data stored in Amazon Timestream.

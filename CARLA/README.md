# Introduction of CARLA Deploy and Run
This section describes how to deploy and run CARLA to act as a simulated vehicle and send CAN data to RDB2.
## Requirements of CARLA
The following [requirements](https://CARLA.readthedocs.io/en/latest/start_quickstart/) should be fulfilled before installing CARLA:

* System requirements. CARLA is built for Windows and Linux systems. Ubuntu20.04 used in the demo.
* An adequate GPU. CARLA aims for realistic simulations, so the server needs at least a 6 GB GPU although we would recommend 8 GB. A dedicated GPU is highly recommended for machine learning.
* Disk space. CARLA will use about 20 GB of space.
* Python. Python is the main scripting language in CARLA.Python>=3.7 recommanded.
* Pip. Some installation methods of the CARLA client library require pip or pip3 (depending on your Python version) version 20.3 or higher. To check your pip version:
```
 pip3 -V
```
If you need to upgrade:
```
 pip3 install --upgrade pip
```
## CARLA Installation
### Dependencies
CARLA requires some Python dependencies. 
```
cd <path to requirements.txt>
pip3 install -r requirements.txt
```
IDE:Pycharm or VSCode
###  Quick installation
1. Download CARLA package from [CARLA Repository](https://github.com/CARLA-simulator/CARLA/blob/master/Docs/download.md)

* [CARLA 0.9.13](https://github.com/CARLA-simulator/CARLA/releases/tag/0.9.13/) is used in the demo.
* Download [Ubuntu] CARLA_0.9.13.tar.gz (6.2GB) for CARLA
* Download [Ubuntu] AdditionalMaps_0.9.13.tar.gz (3.2GB) for additional map
2. CARLA Install
The package is a compressed file, extract the release file. It contains a precompiled version of the simulator, the Python API module and some scripts to be used as examples. Copy AdditionalMaps_0.9.13 to CARLA_0.9.13 and choose REPLACE to merge maps.
3. Import additional assets
Each release has it's own additional package of extra assets and maps. This additional package includes the maps Town06, Town07, and Town10. These are stored separately to reduce the size of the build, so they can only be imported after the main package has been installed.
Run the following script to extract the contents:
```
cd <path to CARLA root> #(for example: /home/usr/CARLA_0.9.13)
./ImportAssets.sh
```
4. Downloadable Python package for CARLA
The CARLA client library can be downloaded from PyPi. This library is compatible with Python versions 2.7, 3.6, 3.7, and 3.8. To install it you will need pip/pip3 version 20.3 or above. See the Before you begin section for how to check the version and upgrade pip/pip3.
It is recommended to install the CARLA client library in a virtual environment to avoid conflicts when working with multiple versions.
To install the client library from PyPi, run the following command:
```
 # Python 3
 pip3 install CARLA
```
4.Running CARLA
```
cd path/to/CARLA/root #(for example: /home/usr/CARLA_0.9.13)
./CARLAUE4.sh
```
A window containing a view over the city will pop up. This is the spectator view. To fly around the city use the mouse and WASD keys, holding down the right mouse button to control the direction.This is the server simulator which is now running and waiting for a client to connect and interact with the world.
## Demo Run
The CARLA simulator consists of a scalable client-server architecture.
The server is responsible for everything related with the simulation itself: sensor rendering, computation of physics, updates on the world-state and its actors and much more. As it aims for realistic results, the best fit would be running the server with a dedicated GPU, especially when dealing with machine learning.
The client side consists of a sum of client modules controlling the logic of actors on scene and setting world conditions. This is achieved by leveraging the CARLA API (in Python or C++), a layer that mediates between server and client that is constantly evolving to provide new functionalities.
![CARLA API](https://github.com/JimmySunCreater/AWS-IoTFleetwise-NXP-RDB2-Demo/blob/main/CARLA/carla_modules.png)
Demo code using Python to start the virtual vehicle.
Download [IoTFleetwiseRDB2DemoCode\(manual_control\).py](https://github.com/JimmySunCreater/AWS-IoTFleetwise-NXP-RDB2-Demo/blob/main/CARLA/IoTFleetwiseRDB2DemoCode%28manual_control%29.py) file and run:
```
cd <path to the python file>
python3 IoTFleetwiseRDB2DemoCode(manual_control).py
```
## Code Deepdive 
The vehicle value can be accessed using [CARLA PythonAPI](https://CARLA.readthedocs.io/en/latest/python_api/) including Cameras (RGB, depth and semantic segmentation),Collision detector,GNSS ,IMU sensor,Lane invasion,LIDAR,Obstacle,Radar. All the data is decimal, it can't be used directly in the real vehicle. 
Normally, the data transfer within the vehicle using CANBus. CAN is a message oriented protocol for quick serial data exchange between electronic control units (ECU) in automotive and automation industry as well as in other industries. 
IoTFleetwise and Edge Agent following the CAN protocals.The DBC file(CAN database files)is a simple text file that consists of information for decoding raw CAN bus data to physical values in human readable form or encoding physical values to CAN bus data. DBC file is used as shared schema for data exchange from the car and cloud in this demo. Python code is used to convert CARLA physical values(decimal) to ECU CAN bus values（hexadecimal）and ingest to RDB2.

* [CANTools](https://cantools.readthedocs.io/en/latest/#) is a python plugin used for CAN message encoding and decoding.
[Python-can](https://python-can.readthedocs.io/) library provides Controller Area Network support for Python, providing common abstractions to different hardware devices, and a suite of utilities for sending and receiving messages on a CAN bus.

USB interface init and database init for CARLA is defined by global parameter.
```
db_CAN = cantools.database.load_file('<path to hscan.dbc>)
can_bus = can.interface.Bus(bustype='canalystii', bitrate=500000, channel=0)
```
>The hardware of USB2CAN in the demo is CANalyst-II.CANalyst-II is a USB to CAN Analyzer device produced by Chuangxin Technology, so bustype='canalystii'.Choose the right [bustype](https://python-can.readthedocs.io/en/master/interfaces.html) and channel by the hardware.

* class CAN() is defined to init and define data send function. It can be echo by the other code in main. Data sending example code is as follows.

```
def send_Engine(self, ThrottlePosition):  
        if ((time.time()-self.Engine_time)>=self.CollectionInterval):
            self.Engine_time=time.time()
            message = db_CAN.get_message_by_name('Engine')
            data = message.encode({'ThrottlePosition': ThrottlePosition})
            encodedata = can.Message(arbitration_id=message.frame_id, data=data, is_extended_id=False)
            can_bus.send(encodedata)
```
>self.CollectionInterval is the interval time of data collection, it's configurable.

## Hot keys
Welcome to CARLA manual control.
Use ARROWS or WASD keys for control.

    W            : throttle
    S            : brake
    A/D          : steer left/right
    Q            : toggle reverse
    Space        : hand-brake
    P            : toggle autopilot
    M            : toggle manual transmission
    ,/.          : gear up/down
    CTRL + W     : toggle constant velocity mode at 60 km/h
    L            : toggle next light type
    SHIFT + L    : toggle high beam
    Z            : toggle double blinker
    I            : toggle interior light
    TAB          : change sensor position
    ` or N       : next sensor
    [1-9]        : change to sensor [1-9]
    G            : toggle radar visualization
    C            : change weather (Shift+C reverse)
    Backspace    : change vehicle
    O            : open/close Front Left Door
    CTRL + O     : open/close Front Right Door
    K            : open/close Rear Left Door
    CTRL + K     : open/close Rear Right Door
    T            : toggle vehicle's telemetry
    V            : Select next map layer (Shift+V reverse)
    B            : Load current selected map layer (Shift+B to unload)
    R            : toggle recording images to disk
    CTRL + R     : toggle recording of simulation (replacing any previous)
    CTRL + P     : start replaying last recorded simulation
    CTRL + +     : increments the start time of the replay by 1 second (+SHIFT = 10 seconds)
    CTRL + -     : decrements the start time of the replay by 1 second (+SHIFT = 10 seconds)
    F1           : toggle HUD
    H/?          : toggle help
    ESC          : quit

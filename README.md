# BFMC - Brain Project

The project contains all the provided code for the RPi, more precisely:
- Firmware for communicating with the Nucleo and control the robot movements (Speed with constant current consumption, speed with constant speed, braking, moving and steering);
- Firmware for gathering data from the sensors (IMU and Camera);
- API's for communicating with the environmental servers at Bosch location;
- Simulated servers for the API's.

## The documentation is available in more details here:
[Documentation](https://bosch-future-mobility-challenge-documentation.readthedocs-hosted.com/)



Installation on RPi 5(RPios Lite Version 12 (bookworm) 64-bit)

Step 1: Install git
```sh
sudo apt-get install git
```
Step 2: Clone the repository
```sh
git clone https://github.com/ECC-BFMC/Brain 
cd Brain
```
Step 3: Install the python venv
```sh
sudo apt-get install python3-venv
python3 -m venv venv
source venv/bin/activate
```

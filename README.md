# LocalShare

## V1

## About

I created this application, called LocalShare, which allows users to share files between two devices over the same local network. This project makes use of FastAPI and includes security checks to ensure that files can only be accessed through an allowed path.

The reason behind this project is quite simple: I always wanted to become someone who solves problems. One day, I had to transfer files between my phone and laptop. I didn't have access to a cable, and Bluetooth wasn't working for some reason. That is when I came across LocalSend.

I found myself fascinated by the concept and thought, why not make something like this myself?

And so began my journey of making LocalShare.

This is the first application that I have built myself. Through this project, I have learned about TCP sockets, networking, HTTP, FastAPI, file handling, and the process of turning an idea into something that actually works across multiple devices.

LocalShare V1 currently supports uploading, listing, and downloading files between devices on the same local network. I plan to continue improving it as I learn more.

## Features

### File Transfer

* Users can upload and download files between devices.

### File Discovery

* Devices can view files that are available for download.

### File Handling

* Handles filename collisions by automatically generating a new filename when a file with the same name already exists.
* Deletes partially transferred files if an upload fails before completion.

### Networking

* Allows different devices on the same local network to access the server.

### Security

* Uses path validation to prevent requested file paths from escaping the allowed Downloads directory.

### API

* Uses FastAPI to provide HTTP endpoints for uploading, listing, and downloading files.

## Setup / Usage

* Clone or download the repository onto your local machine.
* Ensure all the devices are on the same network.
* Open the terminal in the project directory and run: py -m uvicorn main:app --host 0.0.0.0 --port 8000.
* On the other device, open up "http://<LAPTOP_LOCAL_IP>:8000/docs" in the browser.
* To get the Laptop Local IP, navigate to Windows PowerShell and copy the IPv4 address of the network you're      connected to. Ensure both devices are on the same network.
* This will open the Swagger UI, where you can test LocalShare's API endpoints to upload, list, and download files.

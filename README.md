# HL7/MLLP load testing with locust

This project aims to show a small proof of concept on how to load test an HL7 server using [locust](https://locust.io/).

## HL7 mock server

In order to test this on your local, there's a dummy tcp server within the repo that is mocking an HL7 server.

Note that it will always answer with the same message. That's why is dummy.

In order to start the server, run the following command:

```bash
python mockHL7server.py
```

This will start the mock server in port `13370`.

## Runnin locust

Also within the project you can find a `locustfile.py`. This file contains the proof of concept.

It will send the same message over and over and expect an ACK from the HL7 server.

In order to run locust, standing on the project's root folder, you should run the following command in a bash console :

```bash
locust
```

_Note that you need to have [python and locust installed](https://docs.locust.io/en/stable/installation.html) in your computer first._

This will start a server in `localhost:8089` that will allow you to load test the target hl7 server.

After some time, you should get some stats like this one:

![image](https://user-images.githubusercontent.com/3678598/113576098-4d386600-95f5-11eb-839c-145416d1e66a.png)

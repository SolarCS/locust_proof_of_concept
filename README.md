# HL7/MLLP load testing with locust

This project aims to show a small proof of concept on how to load test an HL7 server using [locust](https://locust.io/).

## HL7 server

In order to test this on your local, there's a dummy tcp server within the repo that is mocking an HL7 server.

Note that it will always answer with the same message. That's why is dummy.

In order to start the server, run the following command:

```bash
python mockHL7server.py
```

This will start the mock server in port `13370`.

## Locustfile

Also within the project you can find a `locustfile.py`. This file contains the proof of concept.

It will send the same message over and over and expect an ACK from the HL7 server.
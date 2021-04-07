import time
import string
import random
import logging

# from socket import socket, AF_INET, SOCK_STREAM
import socket
from locust import User, TaskSet, events, task

# author: Max.Bai
# date: 2017-04

class MllpClient(socket.socket):

    # locust tcp client
    # author: Max.Bai@2017
    def __init__(self, af_inet, socket_type):
        super(MllpClient, self).__init__(af_inet, socket_type)

    def connect(self, addr):
        return super(MllpClient, self).connect(addr)

    def send(self, msg):
        msg = b"\x0b" + msg.replace("\n", "\r").encode('ascii') + b"\x1c\x0d"
        return super(MllpClient, self).send(msg)

    def recv(self, bufsize):
        return super(MllpClient, self).recv(bufsize).decode()

    def close(self):
        return super(MllpClient, self).close()


class TcpUser(User):
    """
    This is the abstract Locust class which should be subclassed. It provides an TCP socket client
    that can be used to make TCP socket requests that will be tracked in Locust's statistics.
    author: Max.bai@2017
    """

    abstract = True
    user_id_gen = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.new_connection()
        TcpUser.user_id_gen += 1
        self.user_id = TcpUser.user_id_gen

    def new_connection(self):
        self.client = MllpClient(socket.AF_INET, socket.SOCK_STREAM)
        ADDR = (self.host, self.port)
        self.client.connect(ADDR)
        self.message_count = 0

class TestUser(TcpUser):

    min_wait = 100
    max_wait = 1000
    host = "192.168.198.2"
    port = 2575

    hl7_message = """MSH||EPIC|UCSF|CIPHERHEALTH|UCSF|20210312165235||ADT^A01|87326|P|2.3
EVN||20210227031434
PID|1||1237||Elfo^Oscuro||19970315|M||White|1 Exchange Place^^Jersey City^NJ^61571||(309)999-999|(309)999-999|ENG|||63713440||||||||||||N
PD1||||21194^SMITH^JOHN^L
PV1||I|35NU^3418-01^^UCSF|EL|||67397^DAVOLIO^NANCY|||SUR||||1|||67397^DAVOLIO^NANCY||193167550|||||||||||||||||||||||||20201229084300
DG1||||Description0
DG1||||Description1
IN1||||UNITED MEDICAL RESOURCES INC"""

    @task
    def send_message(self):
        if self.message_count < 90:
            print(f'{self.user_id}: port {self.client.getsockname()[1]}')
            start_time = time.time()
            try:
                self.client.send(self.hl7_message)
                data = self.client.recv(2048)
                if 'ACK' not in data:
                    raise Exception(f'ACK not found in message: {data}')
                self.message_count += 1
                total_time = int((time.time() - start_time) * 1000)
                self.environment.events.request_success.fire(request_type="test_user", name="send_message", response_time=total_time, response_length=0)
            except Exception as e:
                total_time = int((time.time() - start_time) * 1000)
                self.environment.events.request_failure.fire(request_type="test_user", name="send_message", response_time=total_time, response_length=0, exception=e)
        else:
            # Reset connection
            self.client.close()
            time.sleep(1) # sleep 1 second
            self.new_connection()

# Exit code should depend on some pre established performance baseline
@events.quitting.add_listener
def _(environment, **kw):
    if environment.stats.total.fail_ratio > 0.01:
        logging.error("Test failed due to failure ratio > 1%")
        environment.process_exit_code = 1
    elif environment.stats.total.avg_response_time > 200:
        logging.error("Test failed due to average response time ratio > 200 ms")
        environment.process_exit_code = 1
    elif environment.stats.total.get_response_time_percentile(0.95) > 800:
        logging.error("Test failed due to 95th percentile response time > 800 ms")
        environment.process_exit_code = 1
    else:
        environment.process_exit_code = 0

if __name__ == "__main__":
    user = TestUser()
    user.run()

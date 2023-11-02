import time
import socket

import gunicorn.http as http

class Config:
    limit_request_line = 4094
    is_ssl = False
    limit_request_fields = 100
    limit_request_field_size = 8190
    proxy_protocol = False
    forwarded_allow_ips = "127.0.0.1"
    secure_scheme_headers = {
        "X-FORWARDED-PROTOCOL": "ssl",
        "X-FORWARDED-PROTO": "https",
        "X-FORWARDED-SSL": "on"
    }
    strip_header_spaces = False

addr = ("127.0.0.2", 8080)
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
with socket.socket(socket.AF_INET, socket.SOCK_STREAM | socket.SOCK_NONBLOCK) as sock:
    sock.bind(addr)
    sock.listen(1)

    while True:
        try:
            conn, addr = sock.accept()
        except BlockingIOError:
            time.sleep(0.1)
            continue
        with conn:
            print("Connected by", addr)
            # while True:
            config = Config()
            try:
                parser = http.RequestParser(config, conn, addr)
                req = next(parser)
                print(req.__dict__)
                # data = conn.recv(1024)
                # header_str, body = data.split(b"\r\n\r\n")
                # method, path, http_version = header_str.split(b"\r\n")[0].split(b" ")
                # headers = dict(map(lambda x: x.decode().split(": "), header_str.split(b"\r\n")[1:]))
                # print("Data received: ", data)
                # print("method, path,  http_version", method, path,  http_version)
                # print("headers", headers)
                # if not data:
                    # break
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    + "Server: gunicorn\r\n"
                    + "Date: Fri, 27 Oct 2023 09:00:22 GMT\r\n"
                    + "Connection: close\r\n"
                    + "Content-Type: text/html; charset=utf-8\r\n\r\n"
                ).encode()
                response = response+b"Pong!"
                print("Sending response: \n", response)
                conn.sendall(response)
            except Exception as e:
                print("Error", str(e))
            conn.close()

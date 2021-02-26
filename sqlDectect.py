import connect
import sqliPayload

class sqlDetect:
    error_msg = ["You have an error in your SQL syntax", "Warning: mysql_fetch_array()", "sql test"]
    def unionDetect(self, url, method, params):
        from sqliPayload import sqliPayload

        payloads = sqliPayload.generator_union_sql()
        connect(payloads, url, params, "union")

    def boleanDetect(self, url, method, params):
        from sqliPayload import sqliPayload
        payloads = sqliPayload.generator_blind_sql()
        connect(payloads, url, params, "bolean")

    def connect(self, payloads, url, params,typeSQLI):
        from connect import connect
        import datetime
        conn = connect()
        if method == "post":
            for payload in payloads:
                for param in params:
                    a = datetime.datetime.now()
                    resp = conn.normal_POST(url,param, payload)
                    b = datetime.datetime.now()
                    c = b - a
                    if c.seconds >= 5:
                        print( "Sqli                Type: time-base SLQI "\
                                   "\n                  Method: POST"\
                                   "\n                  Url: " + url+\
                                   "\n                  Payload: " + payload)
                    for err in error_msg:
                        if err in resp.text:
                            print( "Sqli                Type: " + typeSQLI\
                                   "\n                  Method: POST"\
                                   "\n                  Url: " + url+\
                                   "\n                  Payload: " + payload)
            pass
        elif method == "get":
            for payload in payloads:
                for param in params:
                    a = datetime.datetime.now()
                    resp = conn.normal_GET(url,param, payload)
                    b = datetime.datetime.now()
                    c = b - a
                    if c.seconds >= 5:
                        print( "Sqli                Type: time-base SLQI "\
                                   "\n                  Method: POST"\
                                   "\n                  Url: " + url+\
                                   "\n                  Payload: " + payload)
                    for err in error_msg:
                        if err in resp.text:
                            print( "Sqli                Type: " + typeSQLI\
                                   "\n                  Method: GET"\
                                   "\n                  Url: " + url+\
                                   "\n                  Payload: " + payload)
            pass
        


        



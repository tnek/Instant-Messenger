#!/usr/bin/python3
class HTTPObject(object):
    def __init__(self, version):
        self.version = version
        self.headers = {}
        self.data = ""
    def export_headers(self):
        data_len = len(self.data)
        if data_len > 0:
            self.headers["Content-Length"] = [str(data_len)]

        header_resp = []

        for header in self.headers:
            header_val = "".join(self.headers[header])
            header_resp.append("%s: %s\r\n" %(header, header_val))

        header_resp.append("\r\n")
        return "".join(header_resp) 


class HTTPResponse(HTTPObject):
    """

    From the rfc2616:

           After receiving and interpreting a request message, a server responds
       with an HTTP response message.

           Response      = Status-Line               ; Section 6.1
                           *(( general-header        ; Section 4.5
                            | response-header        ; Section 6.2
                            | entity-header ) CRLF)  ; Section 7.1
                           CRLF
                           [ message-body ]          ; Section 7.2

    """
    def __init__(self, status_code, reason_phrase, version="HTTP/1.1", data=""):
        super().__init__(version)
        self.status_code = status_code
        self.reason_phrase = reason_phrase
        self.data = data

    def status_line(self):
        """
            BNF is as follows: 
                Status-Line = HTTP-Version SP Status-Code SP Reason-Phrase CRLF
        """

        return "%s %s %s\r\n" %(self.version, self.status_code, self.reason_phrase)


    def serialize(self):
        """
            Build HTTP response string
        """
        resp = [self.status_line(), self.export_headers(), self.data, "\r\n"]
        print(resp)
        return "".join(resp)


valid_methods = {"OPTIONS", "GET", "HEAD", "POST", "PUT", "DELETE", "TRACE", "CONNECT" }

class HTTPRequest(HTTPObject):
    def __init__(self, method, uri, version):
        super().__init__(version)
        if method not in valid_methods:
            raise ValueError("Malformed HTTP Request Method")

        self.method = method
        self.uri = uri
import zerorpc

c = zerorpc.Client()
c.connect("tcp://127.0.0.1:4001")

c.websiteHandler("beans.com")

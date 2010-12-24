import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.template
import tornado.websocket

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    l = tornado.template.Loader('./')
    self.write(l.load('pad.html').generate())

class PadWebSocket(tornado.websocket.WebSocketHandler):
  instances = []

  def open(self, *args, **kwargs):
    PadWebSocket.instances.append(self)

  def on_close(self):
    PadWebSocket.instances.remove(self)

  def on_message(self, message):
    for instance in PadWebSocket.instances:
      if instance is not self:
        instance.write_message('Anonymous said: ' + message)
      else:
        instance.write_message('You said: ' + message)


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/websocket", PadWebSocket),
], static_path = './static')

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.template
import tornado.websocket

import json

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    l = tornado.template.Loader('./')
    self.write(l.load('pad.html').generate())

class PadWebSocket(tornado.websocket.WebSocketHandler):
  instances = []
  message = ''

  # Types of Messages
  # * update - clobber the entire contents of the channel with "body"
  # * insert - insert body at pos
  # * delete - remove from start to end
  # * replace - remove from start to end and insert body in its stead

  def open(self, *args, **kwargs):
    PadWebSocket.instances.append(self)
    self.write_message(json.dumps({
          'action': 'update',
          'body': PadWebSocket.message,
    }))

  def on_close(self):
    PadWebSocket.instances.remove(self)

  def on_message(self, message):

    # Update the global state
    recv = json.loads(message)    
    if recv['action'] == 'insert':
      PadWebSocket.message = \
        PadWebSocket.message[:recv['pos']] + \
        recv['body'] + \
        PadWebSocket.message[recv['pos']:]

    elif recv['action'] == 'delete':
      PadWebSocket.message = \
        PadWebSocket.message[:recv['start']] + \
        PadWebSocket.message[recv['end']:]

    elif recv['action'] == 'replace':
      PadWebSocket.message = \
        PadWebSocket.message[:recv['start']] + \
        recv['body'] + \
        PadWebSocket.message[recv['end']:]

    # Re-broadcast to the others
    for instance in PadWebSocket.instances:
      if instance is not self:
        # just write the raw message back out
        instance.write_message(message)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/websocket", PadWebSocket),
], static_path = './static')

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


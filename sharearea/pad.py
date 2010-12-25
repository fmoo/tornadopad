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

  def on_insert_message(msg):
    PadWebSocket.message = \
      PadWebSocket.message[:msg['pos']] + \
      msg['body'] + \
      PadWebSocket.message[msg['pos']:]

  def on_delete_message(msg):
    PadWebSocket.message = \
      PadWebSocket.message[:msg['start']] + \
      PadWebSocket.message[msg['end']:]

  def on_replace_message(msg):
      PadWebSocket.message = \
        PadWebSocket.message[:msg['start']] + \
        msg['body'] + \
        PadWebSocket.message[msg['end']:]

  __ACTIONMAP__ = {
    'insert': on_insert_message,
    'delete': on_delete_message,
    'replace': on_replace_message,
  }

  def on_message(self, message):
    # Update the global state
    recv = json.loads(message)
    action = self.__ACTIONMAP__.get(recv.get('action'))
    if action:
      action(recv)

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


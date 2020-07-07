import socket
import kivy
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

kivy.require('1.0.6')  # replace with your current kivy version !
__version__ = "1.0.3"

host = 'localhost'  # The server's hostname or IP address
port = 12345  # The port used by the server


class MainWindow(BoxLayout):
    input_text = ObjectProperty()
    status = ObjectProperty()
    port_data = ObjectProperty()
    host_data = ObjectProperty()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def light_led(self):
        print(self.input_text.text)
        message = self.input_text.text
        self.client.send(message.encode())

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Trying to connect to the server")

        try:
            if self.port_data.text != "" and self.host_data.text != "":
                self.client.connect((self.host_data.text, int(self.port_data.text)))
            else:
                self.client.connect((host, port))
            print("Connection successful!")
            self.status.text = "Connected"
        except socket.error as exc:
            print("Caught exception socket.error : %s" % exc)
            self.status.text = str(exc)

    def disconnect(self):
        self.status.text = "Disconnected"
        print("Disconnecting from the server")
        self.client.close()


class MainApp(App):

    def build(self):
        Window.bind(on_request_close=self.on_request_close)
        return MainWindow()

    def on_request_close(self, *args):
        print("goodbye")
        MainWindow.client.close()
        self.stop()
        return True


if __name__ == '__main__':
    MainApp().run()

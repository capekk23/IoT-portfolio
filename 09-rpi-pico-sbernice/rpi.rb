# Raspberry Pi: I2C controller. The button (or the dashboard) toggles the LED on the Pico,
# the LED state is read back from the Pico over the same bus.
require "socket"

PICO = 0x42          # I2C address of the Pico
I2C_SLAVE = 0x0703   # Linux ioctl that selects the target address
BUTTON = 17          # BCM GPIO number, physical pin 11

i2c = File.open("/dev/i2c-1", "r+b")
i2c.ioctl(I2C_SLAVE, PICO)
bus = Mutex.new      # The button and the web share one bus, one at a time.
presses = 0

toggle = lambda do
  bus.synchronize { i2c.syswrite("T") }
  presses += 1
end

led = lambda do
  bus.synchronize { i2c.sysread(1).ord }
end

# gpiomon prints one line for every press (falling edge, pull-up, 30 ms debounce).
Thread.new do
  IO.popen(["gpiomon", "-c", "gpiochip0", "-b", "pull-up", "-e", "falling", "-p", "30ms", BUTTON.to_s]) do |events|
    events.each_line do
      toggle.call
      puts "Button: toggle sent"
    end
  end
end

# GET /stav returns the state as JSON, POST /tlacitko is the logical button.
server = TCPServer.new("0.0.0.0", 8009)
loop do
  client = server.accept
  request = client.gets.to_s
  while (line = client.gets) && line != "\r\n"
  end

  toggle.call if request.start_with?("POST /tlacitko")
  sleep 0.02 if request.start_with?("POST")  # Give the Pico time to toggle.

  json = "{\"led\":#{led.call},\"stisky\":#{presses}}"
  client.write "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n" \
               "Access-Control-Allow-Origin: *\r\nContent-Length: #{json.size}\r\n" \
               "Connection: close\r\n\r\n#{json}"
  client.close
end

from pyscript import document, window, when
import wave
import gc

device_LUT = {512: 'single motor', 513: 'dual motor', 514:'color', 515:'joystick'}

class hubs():
    def __init__(self, num, myPlot = None, verbose = False):
        self.num = num
        self.myPlot = myPlot
        self.verbose =  verbose
        self.reply = None
        self.value = None
        self.info = None
        self.hub = wave.Hub(num, verbose)
        self.hub.callback(self.callback)
        self.final_callback = None
        
        self.name = document.getElementById(f'name{num}')
        self.id = document.getElementById(f'sync{num}')
        self.rate = document.getElementById(f'rate{num}')
        self.data_btn = document.getElementById(f'data{num}')
        self.val = document.getElementById(f'value{num}')
        #self.beep_btn = document.getElementById(f'beep{num}')
        self.off_btn = document.getElementById(f'stop{num}')
        self.dropdown_menu = document.getElementById(f'dd{num}')
        self.id.onclick = self.ask
        self.data_btn.onclick = self.start_data_feed
        #self.beep_btn.onclick = self.beep
        #self.off_btn.onclick = self.motor_stop
        self.list_update = False
        
    def callback(self, data):
        gc.collect()
        if self.hub.verbose:
            window.console.log(' callback in main.py/hub ',data)
        try:
            data = [d for d in data]
            self.reply = self.hub.parse(data)
            #window.console.log(' parsed ',self.reply)
            if self.reply:
                update = False
                #window.console.log(self.hub.info['device'])
                if not self.list_update and not 'Firmware' in self.reply:
                    window.console.log(' getting list ')
                    myList = list(self.reply.keys())
                    window.console.log('my list is ',myList)
                    self.list_update = True
                    for i,attribute in enumerate(myList):
                        option = document.createElement("option")
                        option.value = attribute
                        option.text = attribute
                        self.dropdown_menu.appendChild(option)
                    return
                if 'Firmware' in self.reply:
                    self.name.innerHTML = f'{device_LUT[self.reply['device']]} ({self.reply['Firmware']['major']}.{self.reply['Firmware']['minor']}b{self.reply['Firmware']['build']})'
                    update = False                    
                elif self.hub.info['device'] == 514: 
                    self.value = self.reply[self.dropdown_menu.value]
                    self.val.innerHTML = self.value
                    if self.num == 1:
                        value1_copy = document.getElementById("value1_copy")
                        if value1_copy:
                            value1_copy.innerHTML = self.value
                    if self.num == 2:
                        value2_copy = document.getElementById("value2_copy")
                        if value2_copy:
                            value2_copy.innerHTML = self.value
                    # update = self.myPlot.addPoints(self.num, [self.value])
                elif self.hub.info['device'] == 515:
                    self.value = self.reply[self.dropdown_menu.value] #(self.reply['leftAngle'],self.reply['rightAngle'])
                    self.val.innerHTML = self.value
                    if self.num == 1:
                        value1_copy = document.getElementById("value1_copy")
                        if value1_copy:
                            value1_copy.innerHTML = self.value
                    if self.num == 2:
                        value2_copy = document.getElementById("value2_copy")
                        if value2_copy:
                            value2_copy.innerHTML = self.value
                    # update = self.myPlot.addPoints(self.num, [self.value])
                elif self.hub.info['device'] == 513:
                    self.value = self.reply[self.dropdown_menu.value] #(self.reply['position1'],self.reply['position2'])
                    self.val.innerHTML = self.value
                    if self.num == 1:
                        value1_copy = document.getElementById("value1_copy")
                        if value1_copy:
                            value1_copy.innerHTML = self.value
                    if self.num == 2:
                        value2_copy = document.getElementById("value2_copy")
                        if value2_copy:
                            value2_copy.innerHTML = self.value
                    # update = self.myPlot.addPoints(self.num, [self.value])
                elif self.hub.info['device'] == 512:
                    self.value = self.reply[self.dropdown_menu.value]  #self.dropdown.value
                    self.val.innerHTML = self.value
                    if self.num == 1:
                        value1_copy = document.getElementById("value1_copy")
                        if value1_copy:
                            value1_copy.innerHTML = self.value
                    if self.num == 2:
                        value2_copy = document.getElementById("value2_copy")
                        if value2_copy:
                            value2_copy.innerHTML = self.value
                    # update = self.myPlot.addPoints(self.num, [self.value])
                else:
                    window.console.log('unrecognized device ',self.hub.info['device'])
                    update = False
                #await channel.post('/coral', self.value)
                if update:
                    choice = int(document.getElementById('dropdown').value)
                    if self.num == choice:
                        self.myPlot.updatePlot(update)
        except Exception as e:
            window.console.log('error ', e)
        if self.final_callback:
            await self.final_callback(self.reply)
    
    async def ask(self, event):
        if self.id.innerHTML == 'Connect':
            self.list_update = False
            await self.hub.connect()
            self.id.innerHTML = 'Disconnect'
            window.console.log('connected')
        else:
            self.id.innerHTML = 'Connect'
            self.hub.disconnect()
            window.console.log('disconnected')
            self.name.innerHTML = 'Connection'
            self.list_update = False
            self.dropdown_menu.options.length = 0

    async def start_data_feed(self, event):
        rate = int(1000 / float(self.rate.value))
        await self.hub.write(self.hub.feed(rate))

    async def motor_speed(self, port = 1, speed = 50):
        await self.hub.write(self.hub.motor_speed(port,speed))

    async def left_angle(self, angle = 20):
        await self.hub.write(self.hub.motor_angle(1, angle, 2))
        
    async def right_angle(self, angle = 20):
        await self.hub.write(self.hub.motor_angle(2, angle, 2))

    async def left_abs_pos(self, pos = 30, direction = 2):
        await self.hub.write(self.hub.motor_abs_pos(1, pos,direction))

    async def right_abs_pos(self, pos = 30, direction = 2):
        await self.hub.write(self.hub.motor_abs_pos(2,pos,direction))

    async def motor_stop(self, event):
        await self.hub.write(self.hub.motor_stop(3,0))

    async def motor_run(self, port = 3, dir = 2):
        await self.hub.write(self.hub.motor_run(port, dir))

    async def beep(self, event):
        await self.hub.write(self.hub.beep(440,1000))

    async def animate_light(self, pattern = 1, red = 255, green = 255, blue = 255, repeat = 1, speed = 1, intensity = 100):
        await self.hub.write(self.hub.animate_light(pattern,red, green,blue, repeat, speed, intensity))
        
    async def display_image(self, image = 0, timeout = 1000):
        await self.hub.write(self.hub.display_image(image, timeout))
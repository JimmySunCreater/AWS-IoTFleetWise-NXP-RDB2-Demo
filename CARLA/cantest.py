import cantools
import can
# Init CAN(DBC file, CAN configuration) CAN1 Send
db_CAN = cantools.database.load_file('/home/usr/CARLA_0.9.13/PythonAPI/examples/CSS-Electronics-OBD2-v1.4.dbc')
can_bus = can.interface.Bus(bustype='canalystii', bitrate=500000, channel=1)


message = db_CAN.get_message_by_name('OBD2')
data = message.encode({'S1_PID_0C_EngineRPM': 200, 'S1_PID_0D_VehicleSpeed': 89, 'S1_PID_46_AmbientAirTemp': 90,
                       'S1_PID_67_EngineCoolantTemp':200, 'S1_PID_45_RelThrottlePos':80,'S1_PID_2F_FuelTankLevel':92})
encodedata = can.Message(arbitration_id=message.frame_id, data=data)
print(encodedata)
can_bus.send(encodedata)


can_bus.shutdown()

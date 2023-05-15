''' Information:
This code will save voltage and current vs. time to CSV file.

Voltage is sensed using a Precision Voltage Sensor (Device ID = 1135_0B)

The current is sensed using a ACS712 current sensor module
Acs712 is available in market in three ratings:
    ACS712ELCTR-05B-T -- Sensitivity = 185 mV/A
    ACS712ELCTR-20A-T -- Sensitivity = 100 mV/A
    ACS712ELCTR-30A-T -- Sensitivity = 66 mV/A

    Current = (AcsOffset - measured_analog_reading) / Sensitivity
    Where:
        * AcsOffset is normal voltage output at Viout pin when no current is flowing through the circuit.
        * measured_analog_reading is the analog signal value read and converted to actual voltage from the analog channel
          to which acs712 output is connected.
        * Sensitivity is Acs712 change in voltage representing 1 A current change as given above.

    Note: The above formula gives the current the basic calculation, but we will modify to use Phidget's voltage ratio
'''

#region Imports ---------------------------------------------------------------------------------------------------------
from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
from Phidget22.Devices.VoltageRatioInput import *
import traceback
import time
#endregion End Imports --------------------------------------------------------------------------------------------------

endMainSuccess = False

#region Main Function ---------------------------------------------------------------------------------------------------
def main():
    global endMainSuccess
    print('Start of main function')
    # Set up Input Sensors
    # Create channels for voltage and current sensors
    voltageInput0 = VoltageInput()
    currentInput1 = VoltageRatioInput() # more on this later

    # Set addressing parameters
    voltageInput0.setIsHubPortDevice(True)
    voltageInput0.setHubPort(0)

    # Open your Phidgets and wait for attachment
    try:
        voltageInput0.openWaitForAttachment(5000)
    except PhidgetException as ex:
        traceback.print_exc()
        print("")
        print("PhidgetException " + str(ex.code) + " (" + ex.description + "): " + ex.details)
        return

    #Set the sensor type to match the analog sensor you are using after opening the Phidget
    voltageInput0.setSensorType(VoltageSensorType.SENSOR_TYPE_1135)

    # Start Main Loop
    print('Starting Main Loop: Press "Ctrl+C" to stop')
    try:
        while True:
            # Read latest values
            # Print latest values to terminal output
            # Save latest values to CSV file

            # Sleep for 1 seconds before iterating the loop
            time.sleep(1) 
    except (Exception, KeyboardInterrupt):
        pass
    print('Ending Main Loop')
    endMainSuccess = True
#endregion Main Function ------------------------------------------------------------------------------------------------

# Call main function
if __name__ == "__main__":
    main()
    if not endMainSuccess:
        print('Main function terminated prematurely!')

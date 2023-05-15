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
# from Phidget22.Devices.VoltageRatioInput import *
import traceback
from datetime import datetime, timedelta
import time as t
import csv
#endregion End Imports --------------------------------------------------------------------------------------------------


#region Global Delegations ----------------------------------------------------------------------------------------------
V_OFFSET = 2.5 # This value needs to be calibrated by reading the open circuit voltage
SENSITIVITY = 185.0 / 1000
SAMPLE_RATE = 1 # This is the number of seconds between each reading
endMainSuccess = False
#endregion Global Delegations -------------------------------------------------------------------------------------------


#region Main Function ---------------------------------------------------------------------------------------------------
def main():
    global endMainSuccess
    print('Start of main function')
    # Set up Input Sensors
    # Create channels for voltage and current sensors
    voltageInput0 = VoltageInput()
    currentInput1 = VoltageInput()

    # Set addressing parameters
    voltageInput0.setIsHubPortDevice(True)
    voltageInput0.setHubPort(0)

    currentInput1.setIsHubPortDevice(True)
    currentInput1.setHubPort(1)

    # Open your Phidgets and wait for attachment
    try:
        voltageInput0.openWaitForAttachment(5000)
        currentInput1.openWaitForAttachment(5000)
        print('Sensors successfully attached!')
    except PhidgetException as ex:
        traceback.print_exc()
        print("")
        print("PhidgetException " + str(ex.code) + " (" + ex.description + "): " + ex.details)
        return

    #Set the sensor type to match the analog sensor you are using after opening the Phidget
    voltageInput0.setSensorType(VoltageSensorType.SENSOR_TYPE_1135)

    # Create CSV file for this run data
    log_file_name = datetime.now().strftime('Voltage Log -- %Y-%m-%d %H.%M.%S.csv')
    # Start Main Loop
    print('Starting Main Loop: Press "Ctrl+C" to stop')
    START_TIME = None # datetime.now()
    try:
        with open(log_file_name, mode='w', newline='') as log_file:
            writer = csv.DictWriter(log_file, delimiter=',', fieldnames=['Time', 'Duration', 'Voltage', 'Current'])
            writer.writeheader()
            while True:
                # Read latest values
                voltage = voltageInput0.getVoltage()
                current = (V_OFFSET - currentInput1.getVoltage()) / SENSITIVITY
                last_read_time = datetime.now()
                if START_TIME == None:
                    START_TIME = last_read_time

                # Print latest values to terminal output
                print_str = f'{last_read_time:%H:%M:%S}, {(last_read_time - START_TIME).total_seconds():.2f}, {voltage:.3f}, {current:.3f}'

                print(print_str)
                
                # Save latest values to CSV file
                writer.writerow({
                    'Time':f'{last_read_time:%H:%M:%S}',
                    'Duration':f'{(last_read_time - START_TIME).total_seconds():.2f}',
                    'Voltage':f'{voltage:.3f}',
                    'Current':f'{current:.3f}' 
                    })

                # Sleep for 1 seconds before iterating the loop
                t.sleep(SAMPLE_RATE) 
    except KeyboardInterrupt:
        pass
    print('Ending Main Loop')
    endMainSuccess = True
#endregion Main Function ------------------------------------------------------------------------------------------------


# Call main function
if __name__ == "__main__":
    main()
    if not endMainSuccess:
        print('Main function terminated prematurely!')

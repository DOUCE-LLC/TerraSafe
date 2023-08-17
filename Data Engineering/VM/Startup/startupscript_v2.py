import subprocess
import logging

# File log config
logging.basicConfig(filename='/home/santiagomartearena6/startupscript.log', level=logging.DEBUG)  

# Uso del registro en el código
#logging.debug('Este es un mensaje de debug')
#logging.info('Este es un mensaje informativo')
#logging.warning('Este es un mensaje de advertencia')
#logging.error('Este es un mensaje de error')




# Function to execute a Python script in background
def run_script(script_path):
    subprocess.Popen(["python3", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logging.debug('Iniciando %s', script_path)

if __name__ == "__main__":
    # Scripts file path 
    script1_path = "/home/santiagomartearena6/NOAA_API_Task_v2.py"
    script2_path = "/home/santiagomartearena6/NOAA_ETL_Task_v1.1.py"
    script3_path = "/home/santiagomartearena6/USGS-CHI_API_Task_v2.py"
    script4_path = "/home/santiagomartearena6/USGS-JPN_API_Task_v2.py"
    script5_path = "/home/santiagomartearena6/USGS-USA_API_Task_v2.py"
    script6_path = "/home/santiagomartearena6/USGS-CHI_ETL_Task_v1.py"
    script7_path = "/home/santiagomartearena6/USGS-JPN_ETL_Task_v1.py"
    script8_path = "/home/santiagomartearena6/USGS-USA_ETL_Task_v1.py"
    
    
    # Execute scripts in background
    run_script(script1_path)
    run_script(script2_path)
    run_script(script3_path)
    run_script(script4_path)
    run_script(script5_path)
    run_script(script6_path)
    run_script(script7_path)
    run_script(script8_path)
import os
import difflib
def main():
    print("BEGIN Tests")
    # Test file1
    # Test config 1
    # Test Expected Output
    #Check for Stats only
    print("Check Statistics")
    cmd = "python ..\HttpLogMonitor.py --input_file .\TestLogsConfigs\logs1.txt --config_file .\TestLogsConfigs\config1.json > temp"
    returned_value = os.system(cmd)  # returns the exit code in unix
    text1 = open(".\TestLogsConfigs\expected_output1.txt").readlines()
    text2 = open("temp").readlines()
    noError=True
    for line in difflib.unified_diff(text1, text2):
        noError=False
        print(line)
    if noError == False:
        print(f'Statistics check test Failed')
    else:
        print(f'Statistics check test Succeeded')
    # Test file2
    # Test config 2
    # Test Expected Output
    #Check for Stats only
    print("Check Alerts")
    cmd = "python ..\HttpLogMonitor.py --input_file .\TestLogsConfigs\logs2.txt --config_file .\TestLogsConfigs\config2.json > temp"
    returned_value = os.system(cmd)  # returns the exit code in unix
    text1 = open(".\TestLogsConfigs\expected_output2.txt").readlines()
    text2 = open("temp").readlines()
    noError=True
    for line in difflib.unified_diff(text1, text2):
        noError=False
        print(line)
    if noError == False:
        print(f'Alert check test Failed')
    else:
        print(f'Alert check Succeeded')

    print("Check Invalid Arguments")
    cmd = "python ..\HttpLogMonitor.py --input_file .\TestLogsConfigs\invalid_path.txt --config_file .\TestLogsConfigs\config2.json"
    returned_value = os.system(cmd)  # returns the exit code in unix
    if returned_value !=1 :
        print("Test Failed")
    else:
        print("Test was a Success")

    print('END Tests')
    return
if __name__ == "__main__":
        main()

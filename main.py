from SharePoint import Sharepoint_Connector
import time
import config
import os

#-------------------Environment Variable Here----------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------
domain = "https://*.sharepoint.com/sites/RFPAutomation"
username = ""
pwd = ""

Refernece_folder_url = "/sites/RFPAutomation/Shared Documents/General/RFP"
local_directory_Input = "C://Users/sagarkumar4/Documents/AutomationHubPoc/RFP Usecase/TestDocs"
local_directory_Output = "C://Users/sagarkumar4/Documents/AutomationHubPoc/RFP Usecase/Output"

Target_Archive_Folder = "/sites/RFPAutomation/Shared Documents/General/RFP/Archive"
Target_Output_Upload_Folder = "/sites/RFPAutomation/Shared Documents/General/RFP/Output"

#--------------------------------------------Execute The Solution---------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------
#Establish Connection with Sharepoint
sharepointdownloader = Sharepoint_Connector(Domain=domain, UserName=username,Password=pwd)
while True:
    #Download Files if there are any on the Sharepoint
    source_Path = Sharepoint_Connector.check_folders_recursively(sharepointdownloader, root_folder_url= os.path.join(Refernece_folder_url,"Input"),TargetPath=local_directory_Input)

    #wait for the files to download
    time.sleep(30)

    #Check if There are one ore more downloaded Files in local directory
    if len(os.listdir(local_directory_Input))>0:
        print("RFP Files available for analysing are : "+str(os.listdir(local_directory_Input)))

        #Execute the GenAI Script
        with open("RFP_Analysis_Final.py") as file:
            exec(file.read())

        #move the Input Files on sharepoint to Archive Folder
        Sharepoint_Connector.Move_To_Archive(sharepointdownloader,SourceFolder=os.path.join(Refernece_folder_url,"Input",source_Path),TargetArchiveFolder=Target_Archive_Folder)

        #Wait for some time for the files to get moved
        time.sleep(10)

        #Check For Output/Generated Files in the local directory
        OutputFileList = os.listdir(local_directory_Output)

        for file in OutputFileList:
            #Upload the Generated Response to SharePoint
            Sharepoint_Connector.Upload_File(sharepointdownloader,os.path.join(local_directory_Output,file),Target_Output_Upload_Folder)

            #Remove the local Version of File
            os.remove(os.path.join(local_directory_Output,file))

        #Remove the Downloaded Input Files also from local directory
        InputFileList = os.listdir(local_directory_Input)
        for file in InputFileList:
            os.remove(os.path.join(local_directory_Input,file))

        #Wait some time to again start checking for new RFP Files on SharePoint
        time.sleep(30)

    else:

        print("No File Downloaded")

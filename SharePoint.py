import time
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
import os

#----------------------------------------------------------------------------------------------------------------
#-------------Python Class to connect with SharePoint------------------------------------------------------------
#---------------Download_Files Function will Download the files from Sharepoint to a specified folder/location---
#---------------

class Sharepoint_Connector():
    def __init__(self,Domain,UserName,Password) -> None:
        ctx_auth = AuthenticationContext(url=Domain)
        if ctx_auth.acquire_token_for_user(UserName, Password):
            self.ctx = ClientContext(Domain, ctx_auth)
            print("Connected to SharePoint successfully")
        else:
            print("Failed to authenticate to SharePoint")

        pass

    def Download_Files(self,SourceRefernecePath, TargetPath) -> str:
        downloaded_files = []
        root_folder = self.ctx.web.get_folder_by_server_relative_url(SourceRefernecePath)
        self.ctx.load(root_folder)
        try:
            self.ctx.execute_query()
        except:
            print("execute query suspended due to exception")

        #--------------------------------------------------------------
        folder = self.ctx.web.get_folder_by_server_relative_url(SourceRefernecePath)
        self.ctx.load(folder)
        self.ctx.execute_query()
 
        folder_files = folder.files
        self.ctx.load(folder_files)
        self.ctx.execute_query()
        print(SourceRefernecePath)
        if len(folder_files) > 0:
            print(str(len(folder_files))+" : Files Found in folder:", SourceRefernecePath)
            for file in folder_files:
                print(f"- {file.properties['Name']}")
            try:
                # Get the folder
                folder = self.ctx.web.get_folder_by_server_relative_path(SourceRefernecePath)
                self.ctx.load(folder)
                self.ctx.execute_query()
                print("Folder loaded successfully")
 
            # Get files in the folder
                files = folder.files
                self.ctx.load(files)
                self.ctx.execute_query()
                print("Files loaded successfully")

                #Load Web
                web = self.ctx.web
                self.ctx.load(web)
                self.ctx.execute_query()
 
                # Iterate through each file and download it
                for file in files:
                    file_name = file.properties["Name"]
                    print(file_name)
                    file_url = file.properties["ServerRelativeUrl"]
                    file_path = os.path.join(TargetPath, file_name).replace("\\","//")
                    file = File.open_binary(self.ctx, file_url)
 
                # Download file content
                    with open(file_path, "wb") as local_file:
                        local_file.write(file.content)
                # Add file name to the list
                    downloaded_files.append(file_name)
                    print("File '{}' downloaded to '{}'".format(file_name, file_path))
            except Exception as ex:
                print("Error:", ex)

            #return str(SourceRefernecePath)
 
        else:
            print("No Files in the Defined SharePoint Folder")
        #--------------------------------------------------------------
        #check_folder_for_files(SourceRefernecePath)
        #sub_folders = root_folder.folders
        #self.ctx.load(sub_folders)
        #for folder in sub_folders:
            #print("Name is : "+ str(folder.properties['Name']))
            #self.Download_Files(folder.properties['ServerRelativeUrl'])
        return str(SourceRefernecePath)

    def check_folders_recursively(self,root_folder_url,TargetPath) -> str:
        root_folder = self.ctx.web.get_folder_by_server_relative_url(root_folder_url)
        self.ctx.load(root_folder)
        try:
            self.ctx.execute_query()
        except:
            print("execute query suspended due to exception")
        source_path = self.Download_Files(root_folder_url,TargetPath)
        sub_folders = root_folder.folders
        self.ctx.load(sub_folders)
        try:
            self.ctx.execute_query()
        except:
            print("execute query suspended due to exception")
        folder_name = ""
        for folder in sub_folders:
            print("Name is : "+ str(folder.properties['Name']))
            folder_name = str(folder.properties['Name'])
            self.check_folders_recursively(root_folder_url= folder.properties['ServerRelativeUrl'],TargetPath = TargetPath)
        
        return folder_name

    def Move_To_Archive(self,SourceFolder,TargetArchiveFolder) -> None:
        # Get the source folder
        source_folder = self.ctx.web.get_folder_by_server_relative_url(SourceFolder)
        print(source_folder)
        self.ctx.load(source_folder)
        try:
            self.ctx.execute_query()
        except:
            print("Execute Query Command Failed due to Internal Exception")

        # Get the destination folder
        destination_folder = self.ctx.web.get_folder_by_server_relative_url(TargetArchiveFolder)
        self.ctx.load(destination_folder)
        try:
            self.ctx.execute_query()
        except:
            print("Execute Query Command Failed due to Internal Exception")

        # Move the source folder to the destination folder
        source_folder.move_to(TargetArchiveFolder + "//" + source_folder.properties["Name"])
        print("Folder Moved To Archive")
        try:
            self.ctx.execute_query()
        except:
            print("Execute Query Command Failed due to Internal Exception")

        pass

    def Upload_File(self,Source_File,TargetPath) -> None:
        web = self.ctx.web
        self.ctx.load(web)
        self.ctx.execute_query()
 
        # Get the folder where you want to upload the file
        folder = self.ctx.web.get_folder_by_server_relative_url(TargetPath)
        self.ctx.load(folder)
        self.ctx.execute_query()
 
        # Prepare file path and name
        filename = os.path.basename(Source_File)
 
        # Upload the file
        with open(Source_File, 'rb') as file_content:
            uploaded_file = folder.upload_file(filename, file_content)
            self.ctx.execute_query()
 
        print(f"File uploaded successfully to SharePoint: {uploaded_file.serverRelativeUrl}")
        pass
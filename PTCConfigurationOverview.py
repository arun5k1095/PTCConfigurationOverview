#################################################################
# Handcrafted at ZF -TCI, Hyderabad
# Authors : Kiran Reddy, Arun Kumar
ToolName = 'PTCConfigurationOverview'
ToolRev = "1.4.4"
LastUpdatedOn = "31st August,2021 "
#Last Evolution : 30th Jul 2021
#################################################################




import tkinter
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import pandas as pd
from pandastable import Table
import copy
import pickle
import sys
import os
import subprocess as CommandWin
from tkinter import scrolledtext
from datetime import datetime
import xlrd
import xml.etree.ElementTree as ET
from ttkwidgets import CheckboxTreeview


ProjectsList_stored = []
EPBFuncDetails = []
ProjectAndParamFileNAmes = []
percentage = 0
FuncConfigVerdict = []
ConnectionAttempt = 0
ProjectsToAssess = []






filterKeywordsInputMemory ="KeyWord_1,KeyWord_2,"
filterDropDown_w_wo = "Without"
filterKeywordsInputMemoryDevpthProjRev = "KeyWord_1,KeyWord_2,"
filterDropDown_w_wo_DevProjRevs = "Without"
Memory1_Proj2BanlysedWith = ""
Memory1_Proj2BanlysedWithList = [""]
Memory1_Proj2BanlysedWithOut = ""
Memory1_Proj2BanlysedWithOutList = [""]
MemoryCheckBoxNolabel = 0


#ProjCatFoldrStruct = ['/EPB/ProductDevelopment/EPBi/project.pj','08_Software','PBC_APPL','Application_PBC','ParkBrakeApplication']

ProjCatFoldrStruct_Database = {

    "EPBi PBC System (PBC and SSM PB Application)": ['/EPB/ProductDevelopment/EPBi/project.pj', '08_Software',
                                                     'PBC_APPL', 'Application_PBC', 'ParkBrakeApplication'],
    "PBC Application Only": ['/EPB/ProductDevelopment/EPBi/project.pj', '08_Software', 'PBC_APPL', 'Application_PBC',
                             'ParkBrakeApplication'],
    "SSM_PB Application Only": ['/EPB/CustomerDevelopment/VW/MEB/project.pj', '08_Software', 'SSM_PB_APPL', 'Application_SSM_PB',
                                'SSM'],
    "EPB5 (MMC Application)": ['/EPB/ProductDevelopment/EPBi/project.pj', '08_Software', 'MMC_APPL', 'Application',
                                'ParkBrakeApplication'],
    "EPB4 and Uncategorised": ['/EPB/ProductDevelopment/EPBi/project.pj', '08_Software', 'PBC_APPL', 'Application_PBC',
                               'ParkBrakeApplication'],
    "EPB Redundant": ['/EPB/ProductDevelopment/EPBi/project.pj', '08_Software', 'PBC_APPL', 'Application_PBC',
                      'ParkBrakeApplication'],

}



Categories_Proj_Wrapper2 = {
                            "PBC":"PBC Application Only",
                            "SSM":"SSM_PB Application Only",
                            "MMC":"EPB5 (MMC Application)",
                            "EPB4":"EPB4 and Uncategorised",
                            "EPB_R":"EPB Redundant",
                            }




Categories_Proj_Wrapper = {"CAT1_Full_EPBi":"EPBi PBC System (PBC and SSM PB Application)",
                 "CAT2_PBC_APPL":"PBC Application Only",
                 "CAT3_SSM_PB_APPL":"SSM_PB Application Only",
                 "CAT4_MMC_APPL":"EPB5 (MMC Application)",
                 "CAT5_EPB4_and_Uncategorised":"EPB4 and Uncategorised",
                 "CAT6_EPB_Redundant":"EPB Redundant",
                   }

FuncAnlsDB_ProjCatFoldrStruct = {

    "CAT1_Full_EPBi": {"XML_FILEPTH":["08_Software/PBC_PARA/02_Architecture_Design/project.pj"] ,
                       "INTERFCE_FILEPTH" : ["08_Software/PBC_APPL/Application_PBC/ParkBrakeApplication/PBAInterface/02_Sources/project.pj"],
                       "XML_FILENAME": "Parameter_List.xml",
                       "INTERFCE_FILENAME": "PBAInterface_Sub.h"  },
    "CAT2_PBC_APPL":     {"XML_FILEPTH":["08_Software/PBC_PARA/02_Architecture_Design/project.pj"] ,
                          "INTERFCE_FILEPTH" : ["08_Software/PBC_APPL/Application_PBC/ParkBrakeApplication/PBAInterface/02_Sources/project.pj"],
                          "XML_FILENAME": "Parameter_List.xml",
                          "INTERFCE_FILENAME": "PBAInterface_Sub.h"
                          },
    "CAT3_SSM_PB_APPL": {"XML_FILEPTH":["08_Software/SSM_PB_PARA/02_Architecture_Design/project.pj"] ,
                         "INTERFCE_FILEPTH" : ["08_Software/SSM_PB_APPL/Application_SSM_PB/SSM/SSMInterface/02_Sources/project.pj"],
                         "XML_FILENAME": "Parameter_List.xml",
                         "INTERFCE_FILENAME": "SSMInterface_sub.h"
                         },
    "CAT4_MMC_APPL": {"XML_FILEPTH":["08_Software/MMC_PARA/02_Architecture_Design/project.pj"] ,
                      "INTERFCE_FILEPTH" : ["08_Software/MMC_APPL/Application/ParkBrakeApplication/PBAInterface/02_Sources/project.pj"],
                      "XML_FILENAME": "Parameter_List.xml",
                      "INTERFCE_FILENAME": "PBAInterface_Sub.h"
                      },
    "CAT5_EPB4_and_Uncategorised": {"XML_FILEPTH":["TBD"] ,
                                    "INTERFCE_FILEPTH" : ["TBD"],
                                    "XML_FILENAME": "TBD",
                                    "INTERFCE_FILENAME": "TBD"
                                    },
    "CAT6_EPB_Redundant":           {"XML_FILEPTH":["TBD"] ,
                                     "INTERFCE_FILEPTH" : ["TBD"],
                                     "XML_FILENAME": "TBD",
                                     "INTERFCE_FILENAME": "TBD"
                                     }

}



def ErrorPrompt(ErrorType, message):
    messagebox.showwarning(ErrorType, message)

def resource_path(relative_path):

   try:
        base_path = sys._MEIPASS
   except Exception:
        base_path = os.path.abspath(".")

   return os.path.join(base_path, relative_path)

IconFilepath = resource_path("ZF_logo.ico")


GUITopFrame = tkinter.Tk()
GUITopFrame.config(bg="Dodgerblue4")
GUITopFrame.title(ToolName)
GUITopFrame.resizable(True, True)
GUITopFrame.minsize(800,500)
GUITopFrame.state("zoomed")
ParameterFileParsedStatus = 0

try:
    GUITopFrame.iconbitmap(IconFilepath)
except:
    pass


ServerName_IntegrityClient = "skobde-mks-im.kobde.trw.com"
PortName_IntegrityClient = 7001
ServerName_WorkFlow_and_Doc = "skobde-mks-im.kobde.trw.com"
PortName_WorkFlow_and_Doc = 7001
ServerName_ConfigMgmt = "skobde-mks.kobde.trw.com"
PortName_ConfigMgmt = 7001
UserCredentialID = 'Z0083520'
UserCredentialIPswd = 'Zf1234567890.'


EntryVar_IntegrityClient = StringVar(GUITopFrame,value=ServerName_IntegrityClient)
EntryVar_WorkFlow_and_Doc = StringVar(GUITopFrame,value=ServerName_WorkFlow_and_Doc)
EntryVar_ConfigMgmt = StringVar(GUITopFrame,value=ServerName_ConfigMgmt)
EntryVar_UserCredID = StringVar(GUITopFrame,value=UserCredentialID)
EntryVar_UserCredPswd = StringVar(GUITopFrame,value=UserCredentialIPswd)
EntryVar_PortNumIntegrityClient = IntVar(GUITopFrame,value=PortName_IntegrityClient)
EntryVar_PortNumWorkFlow_and_Doc = IntVar(GUITopFrame,value=PortName_WorkFlow_and_Doc)
EntryVar_PortNumConfigMgmt = IntVar(GUITopFrame,value=PortName_ConfigMgmt)



IconFilepath_ServerSynch = PhotoImage(file=resource_path("ServerSynch_Icon.png"))
IconFilepath_DataBase= PhotoImage(file=resource_path("DB_Icon.png"))
IconFilepath_ServConfig= PhotoImage(file=resource_path("Server_Icon.png"))
IconFilepath_FetchIcon= PhotoImage(file=resource_path("Fetch_Icon.png"))
IconFilepath_FilterIcon= PhotoImage(file=resource_path("Icon_Filter.png"))
IconFilepath_AboutIcon= PhotoImage(file=resource_path("Icon_About.png"))
IconFilepath_Connectivity= PhotoImage(file=resource_path("Icon_Connectivty.png"))
IconFilepath_LogoScreenZF= PhotoImage(file=resource_path("Icon_ScreenLogoZF.png"))







notebook = ttk.Notebook(GUITopFrame)
notebook.pack(expand = 1,fill=BOTH)
noteStyle = ttk.Style(GUITopFrame)
noteStyle.configure("TNotebook", background="Dodgerblue4" , borderwidth=3)
#noteStyle.theme_use('default')
noteStyle.configure('TNotebook.Tab', background="white")
noteStyle.map("TNotebook", background= [("selected", "green3")])


Notebook_frame1 = tkinter.Frame(notebook,bd=0,bg="Dodgerblue4")
Notebook_frame2 = tkinter.Frame(notebook,bd=0,bg="Dodgerblue4")

Notebook_frame1.pack(fill='both', expand=1)
Notebook_frame2.pack(fill='both', expand=1)

notebook.add(Notebook_frame1, text='  Process  ')
notebook.add(Notebook_frame2, text='  Output  ')







def ServerConfig():
    ServerConfig_GUI = Toplevel(GUITopFrame)
    ServerConfig_GUI.config(bg="white")
    ServerConfig_GUI.title("Server Connection Configuration")
    ServerConfig_GUI.resizable(False, False)  # x,y resizabling disabled
    #EDIT_Filter_3_DevPathsProjectCheckPts.minsize(500, 200)
    try:
        ServerConfig_GUI.iconbitmap(IconFilepath)
    except:
        pass

    #img = ImageTk.PhotoImage(Image.open(IconFilepath_Connectivity))

    ServerConfig_GUI.grab_set()

    panel = Label(ServerConfig_GUI, image=IconFilepath_Connectivity,relief='flat',bd=0,activebackground='white')
    panel.grid(column=0, row=4, padx=5, pady=10,rowspan = 10)


    Label(ServerConfig_GUI, font=("Segoe UI", 9),
                                      text="Server: Integrity Client",bg="white").grid(column=0, row=0, padx=5, pady=10,
                                                                                sticky='W')


    Entry(ServerConfig_GUI, width=30, textvariable=EntryVar_IntegrityClient,bg="ghost white").grid(row=0, column=1,
                                                                         columnspan=1,
                                                                         sticky='W',
                                                                         padx=5,
                                                                         pady=5, ipadx=5, ipady=2)

    Label(ServerConfig_GUI, font=("Segoe UI", 9),
                                      text="Port number ",bg="white").grid(column=2, row=0, padx=5, pady=10,
                                                                                sticky='W')


    Entry(ServerConfig_GUI, width=30, textvariable=EntryVar_PortNumIntegrityClient,bg="ghost white").grid(row=0, column=3,
                                                                         columnspan=5,
                                                                         sticky='W',
                                                                         padx=5,
                                                                         pady=5, ipadx=5, ipady=2)



    Label(ServerConfig_GUI, font=("Segoe UI", 9),
                                      text="Server: Workflows and Docs",bg="white").grid(column=0, row=1, padx=5, pady=10,
                                                                                sticky='W')


    Entry(ServerConfig_GUI, width=30, textvariable=EntryVar_WorkFlow_and_Doc,bg="ghost white").grid(row=1, column=1,
                                                                         columnspan=1,
                                                                         sticky='W',
                                                                         padx=5,
                                                                         pady=5, ipadx=5, ipady=2)

    Label(ServerConfig_GUI, font=("Segoe UI", 9),
                                      text="Port number ",bg="white").grid(column=2, row=1, padx=5, pady=10,
                                                                                sticky='W')


    Entry(ServerConfig_GUI, width=30, textvariable=EntryVar_PortNumWorkFlow_and_Doc,bg="ghost white").grid(row=1, column=3,
                                                                         columnspan=5,
                                                                         sticky='W',
                                                                         padx=5,
                                                                         pady=5, ipadx=5, ipady=2)






    Label(ServerConfig_GUI, font=("Segoe UI", 9),
                                      text="Server: Configuration management",bg="white").grid(column=0, row=2, padx=5, pady=10,
                                                                                sticky='W')


    Entry(ServerConfig_GUI, width=30, textvariable=EntryVar_ConfigMgmt,bg="ghost white").grid(row=2, column=1,
                                                                         columnspan=1,
                                                                         sticky='W',
                                                                         padx=5,
                                                                         pady=5, ipadx=5, ipady=2)

    Label(ServerConfig_GUI, font=("Segoe UI", 9),
                                      text="Port number ",bg="white").grid(column=2, row=2, padx=5, pady=10,
                                                                                sticky='W')


    Entry(ServerConfig_GUI, width=30, textvariable=EntryVar_PortNumConfigMgmt,bg="ghost white").grid(row=2, column=3,
                                                                         columnspan=5,
                                                                         sticky='W',
                                                                         padx=5,
                                                                         pady=5, ipadx=5, ipady=2)






    Label(ServerConfig_GUI, font=("Segoe UI", 9),
                                      text="User Integrity Login ID",bg="white").grid(column=0, row=3, padx=5, pady=10,
                                                                                sticky='W')


    Entry(ServerConfig_GUI, width=30, textvariable=EntryVar_UserCredID,bg="ghost white").grid(row=3, column=1,
                                                                         columnspan=1,
                                                                         sticky='W',
                                                                         padx=5,
                                                                         pady=5, ipadx=5, ipady=2)

    Label(ServerConfig_GUI, font=("Segoe UI", 9),
                                      text="User Password",bg="white").grid(column=2, row=3, padx=5, pady=10,
                                                                                sticky='W')


    Entry(ServerConfig_GUI, width=30, textvariable=EntryVar_UserCredPswd,bg="ghost white", show="*").grid(row=3, column=3,
                                                                         columnspan=5,
                                                                         sticky='W',
                                                                         padx=5,
                                                                         pady=5, ipadx=5, ipady=2)







    def ConnectToServers():
        if ((EstablishServerConnection("im",EntryVar_IntegrityClient.get().strip(),str(EntryVar_PortNumIntegrityClient.get()).strip(),\
                                  EntryVar_UserCredID.get().strip(),EntryVar_UserCredPswd.get().strip())) and \

            (EstablishServerConnection("im",EntryVar_WorkFlow_and_Doc.get().strip(), str(EntryVar_PortNumWorkFlow_and_Doc.get()).strip(), \
                                  EntryVar_UserCredID.get().strip(), EntryVar_UserCredPswd.get().strip())) and \

            (EstablishServerConnection("si",EntryVar_ConfigMgmt.get().strip(), str(EntryVar_PortNumConfigMgmt.get()).strip(), \
                                  EntryVar_UserCredID.get().strip(), EntryVar_UserCredPswd.get().strip()))) :

            EstablishServerConnectionButton.config(bg="green")
            EstablishServerConnectionButton.config(text="Connected")
        else :

            EstablishServerConnectionButton.config(bg="red")



    EstablishServerConnectionButton = Button(ServerConfig_GUI, font=("Segoe UI", 9),
                                             text="Connect     ", fg="white", bg="Dodgerblue4",
                                             relief="raised", command=ConnectToServers)
    EstablishServerConnectionButton.grid(row=6, column=1,
                                         columnspan=5,
                                         sticky='W',
                                         padx=5,
                                         pady=5, ipadx=5, ipady=3)

    #EstablishServerConnectionButtonGUI = Button(ServerConfig_GUI, font=("Segoe UI", 9),
    #                                            text="Connect via Integrity ↹", fg="white", bg="Dodgerblue4",
    #                                            relief="raised", command=EstablishServerConnectionViaIntegrity)
    #EstablishServerConnectionButtonGUI.grid(row=7, column=1,
    #                                        columnspan=5,
    #                                        sticky='W',
    #                                        padx=5,
    #                                        pady=5, ipadx=5, ipady=3)

    def DisConnectFrmServer():
        EstablishServerConnectionButton.config(bg="Dodgerblue4")
        EstablishServerConnectionButton.config(text="Connect     ")
        DisconnectfromServer()
    DisconnectButton = Button(ServerConfig_GUI, font=("Segoe UI", 9),
                                                text="Disconnect", fg="white", bg="Dodgerblue4",
                                                relief="raised", command=DisConnectFrmServer)
    DisconnectButton.grid(row=7, column=1,
                                         columnspan=5,
                                         sticky='W',
                                         padx=5,
                                         pady=5, ipadx=5, ipady=3)
    def Close():
        ServerConfig_GUI.destroy()
    CloseButton = Button(ServerConfig_GUI, font=("Segoe UI", 9),
                              text="  Close  ", fg="white", bg="Dodgerblue4",
                              relief="raised", command=Close)
    CloseButton.grid(row=7, column=7,
                          columnspan=5,
                          sticky='W',
                          padx=15,
                          pady=15, ipadx=5, ipady=3)


def DisconnectfromServer():
    global CLI_Window_ServerConn, ConnectionAttempt, EstablishServerConnectionButton

    Command = "si disconnect --yes"

    try:
        response = CommandWin.Popen(Command, stdout=CommandWin.PIPE, stderr=CommandWin.PIPE)
        stdout, stderr = response.communicate(timeout=15)
        MessagesLog(stderr.decode())
    except Exception as error:
        MessagesLog(error)
        #MessagesLog("str(error)")



def EstablishServerConnectionViaIntegrity():
    global CLI_Window_ServerConn,ConnectionAttempt,EstablishServerConnectionButton
    Command = "si connect --yes --gui"
    try:
        response = CommandWin.Popen(Command, stdout=CommandWin.PIPE, stderr=CommandWin.PIPE)
    except Exception as error:
        MessagesLog(error)



def EstablishServerConnection(IM_SI,ServerName , PortNum , UserID , UserPaswd):
    Command = "{} connect --yes --hostname={} --port={} --user={} --password={} ".format(str(IM_SI),ServerName , PortNum , UserID , UserPaswd)

    try:
        response = CommandWin.Popen(Command, shell=True,stdout=CommandWin.PIPE, stderr=CommandWin.PIPE)
        stdout, stderr = response.communicate(timeout=15)

        if len(str(stdout.decode()).strip()) == 0 and len(str(stderr.decode()).strip()) == 0:
            Command = "si servers"
            response = CommandWin.Popen(Command, stdout=CommandWin.PIPE, stderr=CommandWin.PIPE)
            stdout, stderr = response.communicate()
            MessagesLog("Connected- Servers :"+str(stdout.decode()))
            return 1
        else:
            MessagesLog("Error" + str(stderr.decode()))
            return 0

    except Exception as exception:
        MessagesLog(exception)
        return 0









def UpdateProgressStatus(MaxVal, Currprogress):
    global percentage
    ProgressStatus["maximum"] = MaxVal
    ProgressStatus["value"] = Currprogress
    try:
        percentage = round(Currprogress / MaxVal * 100)
    except:
        percentage = 0
    ProgressBarstyle.configure('text.Horizontal.TProgressbar', text="Progress: " + str(percentage) + '%')
    FrameLeft_Notebook_frame1R_1.update()




def EPBProjDetailsParse():

    global ProjectsList_stored,EPBFuncDetails,ProjectAndParamFileNAmes,FetchAllProjectsfromServerBtn,FetchAllProjectsfromDBBtn

    EPBFuncDetails.clear()
   # ProjectsList_stored.clear()
    EPBProjDetails_Path = "EPBProjDetails.xlsx"
    try:
        Workbook = xlrd.open_workbook(EPBProjDetails_Path)

        ProjectsList_stored.clear()
        for proj in Projects_Categorised_DB:
            ProjectsList_stored.append(proj["ProjectPath"])

        WorkbookSheet_EPB_EPB_FunctionDetails = Workbook.sheet_by_name("EPB_FunctionDetails")  # first sheet in workbook
        for row in range(WorkbookSheet_EPB_EPB_FunctionDetails.nrows):
            for col in range(WorkbookSheet_EPB_EPB_FunctionDetails.ncols):
                if WorkbookSheet_EPB_EPB_FunctionDetails.cell_value(row, col) == 'FUNCTIONALITY':
                    FUNCTIONALITYCol = col
                    EPB_FunctionDetailsHeaderRow = row
                if WorkbookSheet_EPB_EPB_FunctionDetails.cell_value(row, col) == 'COMPILESWITCH':
                    COMPILESWITCHCol = col
                if WorkbookSheet_EPB_EPB_FunctionDetails.cell_value(row, col) == 'PARAMETER':
                    PARAMETERCol = col
                if WorkbookSheet_EPB_EPB_FunctionDetails.cell_value(row, col) == 'SOURCECODEFILE':
                    SOURCECODEFILECol = col
                if WorkbookSheet_EPB_EPB_FunctionDetails.cell_value(row, col) == 'BRIEFDESCRIPTION':
                    BRIEFDESCRIPTIONCol = col
                if WorkbookSheet_EPB_EPB_FunctionDetails.cell_value(row, col) == '#MarkerEOD#':
                    break

        for row in range(WorkbookSheet_EPB_EPB_FunctionDetails.nrows):
                if WorkbookSheet_EPB_EPB_FunctionDetails.cell_value(row, 0) == '#MarkerEOD#':
                    EODEPB_FunctionDetailsRow = row

        for row in range(1,EODEPB_FunctionDetailsRow):
            EPBFuncDetails.append({ "FUNCTIONALITY":str(WorkbookSheet_EPB_EPB_FunctionDetails.cell_value(row, FUNCTIONALITYCol)),
              "COMPILESWITCH":str(WorkbookSheet_EPB_EPB_FunctionDetails.cell_value(row, COMPILESWITCHCol)),
              "PARAMETER":str(WorkbookSheet_EPB_EPB_FunctionDetails.cell_value(row, PARAMETERCol)),
              "SOURCECODEFILE":str(WorkbookSheet_EPB_EPB_FunctionDetails.cell_value(row, SOURCECODEFILECol)),
              "BRIEFDESCRIPTION":str(WorkbookSheet_EPB_EPB_FunctionDetails.cell_value(row, BRIEFDESCRIPTIONCol))}
            )
        UpdateProjects()
        FetchAllProjectsfromServerBtn.config(bg="white")
        FetchAllProjectsfromDBBtn.config(bg="white")
        ProjectRevisions_FunctionProjMode_3("")
        ProjectFuncConfig_FunctionProjMode("")

    except Exception as exception:
        #print(str(exception))
        FetchAllProjectsfromServerBtn.config(bg="white")
        FetchAllProjectsfromDBBtn.config(bg="red")
        MessagesLog(str(exception))


def DWnld_XM_and_IntefaceFiles(project,xmlFilePath,InterfaceFilePath,xmfileNAme,InterfaceFileNAme):

        ProjectTobeAssessed_Interface = str(project).replace("project.pj",
                                                             InterfaceFilePath)
        ProjectTobeAssessed_XML = str(project).replace(r"project.pj",
                                                       xmlFilePath)

        FiletobeSavedAt_interface = str(r'''"C:\Users\Z0083520\Desktop\PTC_Integrity_Scan\Downloads\{}"'''.format(
            str(str(project.split("/")[-3]) + "_" + str(project.split("/")[-2])) + ".h"))
        FiletobeSavedAt_paramXML = str(r"C:\Users\Z0083520\Desktop\PTC_Integrity_Scan\Downloads\{}".format(
            str(str(project.split("/")[-3]) + "_" + str(project.split("/")[-2])) + ".xml"))
        MACROfileCommand = r'''si projectco --nolock --yes  --project={} --targetFile={} "{}" '''.format(
            ProjectTobeAssessed_Interface, FiletobeSavedAt_interface,InterfaceFileNAme)
        PARAMETERfileCommand = r'''si projectco  --yes --nolock --project={} --targetFile={} "{}" '''.format(
            ProjectTobeAssessed_XML, FiletobeSavedAt_paramXML,xmfileNAme)

        print(PARAMETERfileCommand)

        ProjecNametemp = str(str(str(project.split("/")[-3]) + "_" + str(project.split("/")[-2]))).split("/")[-1]
        ProjectAndParamFileNAmes.append({"Projpath": str(project), "FuncFile": copy.deepcopy(ProjecNametemp)})

        AnalyseServereturnError = CommandWin.Popen(MACROfileCommand, shell=True, stdout=CommandWin.PIPE,
                                                   stderr=CommandWin.PIPE)
        subprocess_return = AnalyseServereturnError.stderr.read().decode()
        if len(str(subprocess_return).strip()) > 1:
            MessagesLog(str(subprocess_return))

        AnalyseServereturnError = CommandWin.Popen(PARAMETERfileCommand, shell=True, stdout=CommandWin.PIPE,
                                                   stderr=CommandWin.PIPE)
        subprocess_return = AnalyseServereturnError.stderr.read().decode()
        if len(str(subprocess_return).strip()) > 1:
            MessagesLog(str(subprocess_return))

        responseMACRO = CommandWin.Popen(MACROfileCommand, stdout=CommandWin.PIPE, stderr=CommandWin.PIPE)
        stdout, stderr = responseMACRO.communicate(timeout=15)
        response1 = str(stdout.decode()) + str(stderr.decode())

        responseXML = CommandWin.Popen(PARAMETERfileCommand, stdout=CommandWin.PIPE, stderr=CommandWin.PIPE)
        stdout, stderr = responseXML.communicate(timeout=15)
        response2 = str(stdout.decode()) + str(stderr.decode())




def ProjectCTGR_1(project):
    try:
        for proj in Projects_Categorised_DB:
            try:
                if project == proj["ProjectPath"]:
                    return FuncAnlsDB_ProjCatFoldrStruct[str(proj["ProjectCategory"])]["XML_FILEPTH"], \
                           FuncAnlsDB_ProjCatFoldrStruct[str(proj["ProjectCategory"])]["INTERFCE_FILEPTH"], \
                           FuncAnlsDB_ProjCatFoldrStruct[str(proj["ProjectCategory"])]["XML_FILENAME"], \
                           FuncAnlsDB_ProjCatFoldrStruct[str(proj["ProjectCategory"])]["INTERFCE_FILENAME"]

            except Exception as error:
                MessagesLog(error)
        return ["TBD"],["TBD"],"TBD","TBD"
    except Exception as error:
        MessagesLog(str(error))

def downloadFuncConfigFiles():
    #print(ProjectClassification_Db)

    global ProjectsToAssess, EPBFuncDetails, ProjectAndParamFileNAmes,FuncConfigVerdict

    ProjectAndParamFileNAmes.clear()
    FuncConfigVerdict.clear()
    if (Filter_ProjectsToAssess()) == 1:
        pass
    else:
        return
    ProjectCount = 0
    #print(ProjectsToAssess)
    ProjectCount = 0
    for project in ProjectsToAssess:
        try:
            xmlFilePath , InterfaceFilePath ,xmfileNAme,InterfaceFileNAme= ProjectCTGR_1(project)
           # print(xmlFilePath,InterfaceFilePath,xmfileNAme,InterfaceFileNAme)
            if ((xmlFilePath[0] == "TBD") or(InterfaceFilePath[0]== "TBD")or\
                    (xmfileNAme == "TBD") or(InterfaceFileNAme== "TBD")):
                ProjectCount += 1
                UpdateProgressStatus(len(ProjectsToAssess), ProjectCount)
                ErrorPrompt("Development Error","Certain Project/Category are not yet enabled in Tool for analysis, Those would be ignored in analysis")
                ProjectCount += 1
                UpdateProgressStatus(len(ProjectsToAssess), ProjectCount)
                continue
            if len(xmlFilePath)>1:
                #print(len(xmlFilePath))

                DWnld_XM_and_IntefaceFiles(project, xmlFilePath[0], InterfaceFilePath[0], xmfileNAme, InterfaceFileNAme)
                DWnld_XM_and_IntefaceFiles(project, xmlFilePath[1], InterfaceFilePath[1], xmfileNAme, InterfaceFileNAme)

            else:

                DWnld_XM_and_IntefaceFiles(project,xmlFilePath[0],InterfaceFilePath[0],xmfileNAme,InterfaceFileNAme)
            ProjectCount += 1
            UpdateProgressStatus(len(ProjectsToAssess), ProjectCount)
        except Exception as error:
            ProjectCount += 1
            UpdateProgressStatus(len(ProjectsToAssess), ProjectCount)
            MessagesLog(str(error))
    AssesFunEnablDisable()

def AssesFunEnablDisable():

    global FuncConfigVerdict
    if (Filter_ProjectsToAssess()) == 1:
        pass
    else:
        return
    FuncConfig_MACRO_XML = []
    FuncStatusAssessed = []
    ConfigAnalyse = {}


    for project in ProjectAndParamFileNAmes:

        ConfigAnalyse.clear()

        for i in range(len(EPBFuncDetails)):
            FuncStatusAssessed.append(["MACRO : NA","PARAM : NA"])

        for func in EPBFuncDetails:
            datatemp1 = { 'Function': func['FUNCTIONALITY'] ,'MacroConfig' :0,'ParameterConfig' :0}
            FuncConfig_MACRO_XML.append(datatemp1)
        FiletobeSavedAt_interface = str(
            r"C:\Users\Z0083520\Desktop\PTC_Integrity_Scan\Downloads\{}".format(str(project["FuncFile"]) + ".h"))
        FiletobeSavedAt_paramXML = str(
            r"C:\Users\Z0083520\Desktop\PTC_Integrity_Scan\Downloads\{}".format(str(project["FuncFile"]) + ".xml"))
        #print(FiletobeSavedAt_paramXML)
        try:
            try:
                with open(str(FiletobeSavedAt_interface)) as file_in:
                    #MACRO check
                    for line in file_in:
                        FuncStatusAssessedIndex = 0
                        for function in EPBFuncDetails:
                            if (function["COMPILESWITCH"] in line) and ((("*") in line) or (("//") in line)):
                                FuncStatusAssessed[FuncStatusAssessedIndex][0] = "MACRO : Commented"
                            if (function["COMPILESWITCH"] in line) and ((("*") not in line) and (("//") not in line)):
                                FuncStatusAssessed[FuncStatusAssessedIndex][0] = "MACRO : Defined"
                            FuncStatusAssessedIndex +=1

                    tree = ET.parse(FiletobeSavedAt_paramXML)
                    parameters = tree.getroot()
                    FuncStatusAssessedIndex = 0
                    for function in EPBFuncDetails:
                        if function["PARAMETER"] == "NA":
                            FuncStatusAssessed[FuncStatusAssessedIndex][1] = "PARAM : NA"
                        for param in parameters:
                            elem = param.attrib
                            if (str(elem.get("name")).upper() == str(function["PARAMETER"]).upper().strip()):
                                for variant in param:
                                    if (variant.get("variant") == "default"):
                                        for value in variant:
                                            if (str(value.attrib['value']) == "1"):
                                                FuncStatusAssessed[FuncStatusAssessedIndex][1] = "PARAM : Enabled"
                                            else : FuncStatusAssessed[FuncStatusAssessedIndex][1] = "PARAM : Disabled"
                        FuncStatusAssessedIndex += 1

                ConfigAnalyse['Project_Name'] = project["Projpath"]
                for i,function in enumerate(EPBFuncDetails):
                    ConfigAnalyse[str(function["FUNCTIONALITY"])] = FuncStatusAssessed[i]
                tempdata = copy.deepcopy(ConfigAnalyse)
                FuncConfigVerdict.append(copy.deepcopy(tempdata))


            except Exception as exception:
                MessagesLog(str("Project Analysis Ignored : "+ str(project["Projpath"])))

        except Exception as exception:
                #print(exception)
                MessagesLog(str(exception))

    #print(FuncConfigVerdict)
    UpdateVisualTable(FuncConfigVerdict)



FrameLeft_Notebook_frame1R= LabelFrame(Notebook_frame1,
                         fg="black",bg="Dodgerblue4",bd=0,relief = "groove")
FrameLeft_Notebook_frame1R.pack(fill=BOTH,side = "right",expand = 1)

FrameLeft_Notebook_frame1L= LabelFrame(Notebook_frame1,
                         fg="black",bg="Dodgerblue4",bd=0,relief = "groove")
FrameLeft_Notebook_frame1L.pack(fill=BOTH,side = "left",expand = 0)


FrameLeft_Notebook_frame_01= LabelFrame(FrameLeft_Notebook_frame1L, text="",
                         fg="black",bg="Dodgerblue4",bd=0,relief = "flat")
FrameLeft_Notebook_frame_01.pack(fill=BOTH,side = "top")



FrameLeft_Notebook_frame_02= LabelFrame(FrameLeft_Notebook_frame1L,text="Projects hierarchy ..", font=("Segoe UI",10),
                         fg="white",bg="Dodgerblue4",bd=0,relief = "flat")
FrameLeft_Notebook_frame_02.pack(fill=BOTH,side = "top",expand = 1)

FrameLeft_Notebook_frame_01T= LabelFrame(FrameLeft_Notebook_frame1L,text="",
                         fg="white",bg="Dodgerblue4",bd=0,relief = "flat")
FrameLeft_Notebook_frame_01T.pack(fill=BOTH,side = "top")






FrameLeft_Notebook_frame_03= LabelFrame(FrameLeft_Notebook_frame1L, text="",
                         fg="black",bg="Dodgerblue4",bd=0,relief = "flat")
FrameLeft_Notebook_frame_03.pack(fill=BOTH,side = "top")

MessagesLogCounter = 0
def MessagesLog(message):
    global MessageWindow,MessagesLogCounter
    MessagesLogCounter+=1
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    MessageWindow.configure(state='normal')
    MessageWindow.insert(1.0, "\n>> MSG_LOG_"+str(MessagesLogCounter)+"  "+str(dt_string)+" : \n"+str(message)+"\n")
    MessageWindow.configure(state='disabled')

MessageWindow = scrolledtext.ScrolledText(FrameLeft_Notebook_frame_03,
                                      wrap=tkinter.WORD,

                                      height = 12,
                                      font=("Segoe UI",
                                            10),background = "Dodgerblue4",foreground='white')
scrolledtext.ScrolledText()
MessageWindow.pack(fill=BOTH,expand = 0,side = "top")
MessagesLog("Invoked PTCConfigurationOverview Tool Rev : " + str(ToolRev))
MessageWindow.focus()

#FrameLeft_Notebook_frame1R_2= LabelFrame(FrameLeft_Notebook_frame1R, text="Reserved", fg="black")
#FrameLeft_Notebook_frame1R_2.pack(fill=BOTH,side = "top",expand = 1)
FrameLeft_Notebook_frame1R_1= LabelFrame(FrameLeft_Notebook_frame1R, text="",
                         fg="black",bg="white",bd=1,relief = "groove")
FrameLeft_Notebook_frame1R_1.pack(fill=BOTH,side = "top",expand = 1)









ProgressStatus = ttk.Progressbar(FrameLeft_Notebook_frame1R_1, style='text.Horizontal.TProgressbar',  \
                                 cursor='exchange', mode="determinate", orient=tkinter.HORIZONTAL)
ProgressStatus.pack(fill = "x" ,side = "bottom")


FrameLeft_Notebook_frame1R_1_0 = LabelFrame(FrameLeft_Notebook_frame1R_1, text="1. Functions Configurations ➠",
                         fg="black",bg="white",bd=1,relief = "groove")
FrameLeft_Notebook_frame1R_1_0.pack(fill=BOTH,expand=1,side = "top")

FrameLeft_Notebook_frame1R_1_1 = LabelFrame(FrameLeft_Notebook_frame1R_1, text="2. Functions Usages ➠",
                         fg="black",bg="white",bd=1,relief = "groove")
FrameLeft_Notebook_frame1R_1_1.pack(fill=BOTH,expand=1,side = "top")

FrameLeft_Notebook_frame1R_1_2 = LabelFrame(FrameLeft_Notebook_frame1R_1, text="3. Functions checkpoint configurations ➠",
                         fg="black",bg="white",bd=1,relief = "groove")
FrameLeft_Notebook_frame1R_1_2.pack(fill=BOTH,expand=1,side = "top")







def FetchProjects():
    global ProjectsList_stored,FetchAllProjectsfromServerBtn,FetchAllProjectsfromDBBtn
    Command = "im projects"
    try:
        response = CommandWin.Popen(Command, stdout=CommandWin.PIPE, stderr=CommandWin.PIPE)
        #print(response.stdout.read())
        stdout, stderr = response.communicate(timeout=15)
        ProjectsONServer = stdout.decode().split()
        ProjectsList_stored.clear()
        for project in ProjectsONServer:
            if ("/EPB/CustomerDevelopment/" in project) or (("/BRK/Customer/" in project)and ("/EPB" in project )):
                if (project.count("/") != 3):
                    ProjectsList_stored.append(str(project)+"/project.pj")
        #print(ProjectsList_stored)

        for proj in ProjectsList_stored:
            if proj not in [proj["ProjectPath"] for proj in Projects_Categorised_DB]:
                DownloadProjects_DirStructure(str(proj))
        UpdateProjects()
        if len(ProjectsONServer) ==0:
            FetchAllProjectsfromServerBtn.config(bg="red")
            ErrorPrompt("Server Error","No Valid response from server, Please ensure IM server connectivity")
            return
        FetchAllProjectsfromServerBtn.config(bg="green")
        #FetchAllProjectsfromDBBtn.config(bg="Dodgerblue4")


    except Exception as exception:
        MessagesLog(str(exception))
        FetchAllProjectsfromServerBtn.config(bg="red")
        FetchAllProjectsfromDBBtn.config(bg="white")

    #ErrorPrompt("Invalid Operation" , "This functionality is pending implimentation")

FetchAllProjectsfromServerBtn = Button(FrameLeft_Notebook_frame_01,image = IconFilepath_ServerSynch,text=" Re-Synch Projects ",compound= LEFT, fg="black", bg="white",
                      relief="raised",command = FetchProjects,bd=1,activebackground='white')
FetchAllProjectsfromServerBtn.grid(row=0, column=0,
                                                                               columnspan=1,
                                                                               sticky='W',
                                                                               padx=5,
                                                                               pady=5)
FetchAllProjectsfromDBBtn = Button(FrameLeft_Notebook_frame_01,font=("Segoe UI",9),image = IconFilepath_DataBase,compound= LEFT,text="Database ", fg="black", bg="white",
                      relief="raised",command = EPBProjDetailsParse,bd=1,activebackground='white')
FetchAllProjectsfromDBBtn.grid(row=0, column=1,
                                                                               columnspan=1,
                                                                               sticky='W',
                                                                               padx=5,
                                                                               pady=5)

ServerConfig = Button(FrameLeft_Notebook_frame_01,font=("Segoe UI",9),image = IconFilepath_ServConfig,compound= LEFT,text="Server Config ", fg="black", bg="white",
                      relief="raised",command = ServerConfig,bd=1,activebackground='white')
ServerConfig.grid(row=0, column=2,
                                                                               columnspan=1,
                                                                               sticky='W',
                                                                               padx=5,
                                                                               pady=5)





ProgressBarstyle = ttk.Style(FrameLeft_Notebook_frame1R_1)
#ProgressBarstyle.theme_use('alt')
ProgressBarstyle.layout('text.Horizontal.TProgressbar',
             [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar',
                              {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'}),
              ('Horizontal.Progressbar.label', {'sticky': ''})])
#ProgressBarstyle.configure('text.Horizontal.TProgressbar',background="black")
UpdateProgressStatus(100, 0)
#ProgressBarstyle.configure('TProgressbar', background='green', troughcolor='black')
#ProgressBarstyle.configure('text.Horizontal.TProgressbar', thickness=2000, pbarrelief='flat')


def Filter_ProjectsToAssess():
    global ProjectsToAssess

    if len(ct.get_checked()) == 0:
        ErrorPrompt("Invalid Input","Please select minimum 1 project from project tree for analysis.")
        return 0
    else:pass
    ProjectsToAssess.clear()
    ProjectsToAssess=ct.get_checked()
    #print(ProjectsToAssess)
    return 1

def AboutTool():
    AboutTool_GUI = Toplevel(GUITopFrame)
    AboutTool_GUI.config(bg="white")
    AboutTool_GUI.title("Developlment information")
    AboutTool_GUI.resizable(False, False)  # x,y resizabling disabled
    #EDIT_Filter_3_DevPathsProjectCheckPts.minsize(500, 200)

    try:
        AboutTool_GUI.iconbitmap(IconFilepath)
    except:
        pass
    MessageInfo = "\n\n\n"+"PTCConfigurationOverview Tool\n" \
                  "Version "+ToolRev+"  Last Updated : "+LastUpdatedOn+"\n" \
                  "Copyright @ ZF TCI, Hyderabad, India "+\
                  "\n\n\n"
    AboutTool_GUI.grab_set()


    def exitToolInfo():
        AboutTool_GUI.destroy()

    Button(AboutTool_GUI, font=("Segoe UI",10),text= MessageInfo,image=IconFilepath_LogoScreenZF, fg="black", bg="white",
                      relief="sunken",compound= LEFT,state = "normal",command = exitToolInfo,activebackground='white',bd=1).pack(fill=BOTH, expand=1)




AboutBtn = Button(FrameLeft_Notebook_frame_01,image = IconFilepath_AboutIcon, fg="black", bg="white",
                      relief="raised",command = AboutTool,bd=1,activebackground='white').grid(row=0, column=5,
                                                                               columnspan=1,
                                                                               sticky='W',
                                                                               ipadx=2,
                                                                               ipady=2)


###############################################
#Kiran Code 1#Function 2
TempFileSavePath = r"C:\Users\Z0083520\Desktop\PTC_Integrity_Scan\Downloads\Temp.txt"

def LocateFunctionUsages():

    if len(str(FuncRevisionsDropDownUserEntered.get()).strip()) == 0:
        ErrorPrompt("Invalid Input" , "Please provide valid functionality revision number")
        return
    # a_file = open(TempFileSavePath, "w")
    # a_file.close()
    # Start_RevThreshHoldIndx = FunctionalityRevisions.index(str(FuncRevisionsDropDownUserEntered.get()).strip())
    #
    #
    # RevisionFilter = ""
    # if RevperationDropDownBtn.get() == "Same as":
    #     RevisionFilter = ''' /C:"({})"'''.format(str(FuncRevisionsDropDownUserEntered.get()).strip())
    # elif RevperationDropDownBtn.get() == "Lesser than":
    #     if Start_RevThreshHoldIndx == len(FunctionalityRevisions)-1:
    #         ErrorPrompt("Invalid Input" , "Invalid Filter criteria provided.\nLowest revision selected - To be parsed for Lesser revisions.")
    #         return
    #     else:
    #         RevisionToAssess = FunctionalityRevisions[Start_RevThreshHoldIndx:]
    #         for revision in RevisionToAssess:
    #             RevisionFilter += ''' /C:"({})"'''.format(revision)
    #
    # elif RevperationDropDownBtn.get() == "Greater than":
    #
    #     if Start_RevThreshHoldIndx == 0:
    #         ErrorPrompt("Invalid Input" , "Invalid Filter criteria provided.\nHighest revision selected - To be parsed for higher revisions")
    #         return
    #     else:
    #         RevisionToAssess = FunctionalityRevisions[:Start_RevThreshHoldIndx]
    #         for revision in RevisionToAssess:
    #             RevisionFilter += ''' /C:"({})"'''.format(revision)
    # elif RevperationDropDownBtn.get() == "Within range":
    #     End_RevThreshHoldIndx = FunctionalityRevisions.index(str(FuncRevisionsDropDownUserEnteredThreshHold.get()).strip())
    #     RevisionToAssess = FunctionalityRevisions[End_RevThreshHoldIndx:Start_RevThreshHoldIndx]
    #     for revision in RevisionToAssess:
    #         RevisionFilter += ''' /C:"({})"'''.format(revision)


    try:
        UpdateProgressStatus(100, 0)
        SWUnitsList = []
        SWUnitsFinalList = []
        ProjectRevisionsRangeFinalList = []
        Start_Rev = ""
        End_Rev = ""

        if RevperationDropDownBtn.get() == "Same as":
            ProjectRevisionsRangeFinalList.append(str(FuncRevisionsDropDownUserEntered.get()).strip())

        elif RevperationDropDownBtn.get() == "Lesser than":

            End_Rev = str(FuncRevisionsDropDownUserEntered.get()).strip()

        elif RevperationDropDownBtn.get() == "Greater than":

            Start_Rev = str(FuncRevisionsDropDownUserEntered.get()).strip()

        elif RevperationDropDownBtn.get() == "Within range":

            Start_Rev = str(FuncRevisionsDropDownUserEntered.get()).strip()
            End_Rev = str(FuncRevisionsDropDownUserEnteredThreshHold.get()).strip()

        print("Start_Rev", Start_Rev, "End_Rev", End_Rev)

        prjpath = "/EPB/ProductDevelopment/EPBi/08_Software/PBC_APPL/Application_PBC/ParkBrakeApplication/" + str(
            FunctionsDropDownopions.get()).strip() + "/project.pj"

        if RevperationDropDownBtn.get() != "Same as":
            ProjectRevisionsRangeFinalList = GetProjectRevisionsRangeinProject(prjpath, Start_Rev, End_Rev)

        RevisionsOrginalList = GetProjectRevisionsLabelsinProject(
            "/EPB/ProductDevelopment/EPBi/08_Software/project.pj", "NA")

        RevisionsList = FilterOutProj2BAnalysed(RevisionsOrginalList)
        print(RevisionsList)

        Count = 0
        for Revision in RevisionsList:



            UnitRevisionsDict = dict.fromkeys(["ProjectRevision", "Label", "SWUnitRevision"])
            UnitRevisionsDict["ProjectRevision"] = Revision.split("(", 1)[0]

            if "(" in Revision:
                start = Revision.find("(") + len("(")
                end = Revision.find(")")
                UnitRevisionsDict["Label"] = Revision[start:end]
            else:
                UnitRevisionsDict["Label"] = "NA"




            ParentRevision = GetSubProjectRevisionsLevelN(ProjCatFoldrStruct_Database[Categories_Proj_Wrapper2[ProjCategories_2_Dropdown.get()]], UnitRevisionsDict["ProjectRevision"])
            ProjectDir = GetPojectDirLevelN(ProjCatFoldrStruct_Database[Categories_Proj_Wrapper2[ProjCategories_2_Dropdown.get()]])
            SWUnitRevision = GetSubprojectRevision(ProjectDir, ParentRevision, str(FunctionsDropDownopions.get()).strip())
            #SWUnitRevision = GetSubprojectRevision(ProjectDir, ParentRevision, str('RWU'))

            UnitRevisionsDict["SWUnitRevision"] = SWUnitRevision

            SWUnitsList.append(copy.deepcopy(UnitRevisionsDict))
            Count += 1
            UpdateProgressStatus(len(RevisionsList),Count)


        for SWUnitDict in SWUnitsList:
            if (SWUnitDict["SWUnitRevision"] in ProjectRevisionsRangeFinalList):
                SWUnitsFinalList.append(copy.deepcopy(SWUnitDict))

        UpdateVisualTable(SWUnitsFinalList)

    except Exception as exception:
        MessagesLog(str(exception))


def ClearRevision(event):
    global FunctionalityRevisions
    FunctionalityRevisions.clear()
    UpdateFUNCRevisionsinUserInputs()


FunctionsDropDown =  ["ActuatorStateEnhancement","AM","AMS","AutoAdjust","BrakeHandler","BrakeModule","Ca_Pbc","CascadeControl","CFC","DemandArbitrator",\
                      "DSD","FunctionManager","GDA","GSP_Pbc","HPS","HUFunc","MCCA","OutOfSpecMessage_Pbc","ParkRequest","PBA","PBAInterface",\
                      "PBDH","PBFH","PR","PRD","RC","RCC","Reclamp","RWU","SP","TemperatureModel","Vehicle_Pbc" ]

FunctionsDropDownopions = ttk.Combobox(FrameLeft_Notebook_frame1R_1_1, values=sorted(FunctionsDropDown) , width = 25,state="readonly" )
FunctionsDropDownopions.grid(row=1, column=1,
                                                                               columnspan=1,
                                                                               sticky='W',
                                                                               padx=5,
                                                                               pady=5, ipadx=5, ipady=3)
FunctionsDropDownopions.current(0)
FunctionsDropDownopions.bind("<<ComboboxSelected>>", ClearRevision)




def UpdateFuncDropDown_2():
    pass



Label(FrameLeft_Notebook_frame1R_1_1,font=("Segoe UI",9), text="Projects Category",bg="white").grid(column=0,row=0,padx=5,pady=10,sticky='W',columnspan = 5)
ProjCatg_2_DropDownList = ["PBC" , "SSM" , "MMC"]
ProjCategories_2_Dropdown = ttk.Combobox(FrameLeft_Notebook_frame1R_1_1, values=ProjCatg_2_DropDownList , width = 25,state="readonly" )
ProjCategories_2_Dropdown.grid(row=0, column=1,
                                                                               columnspan=1,
                                                                               sticky='W',
                                                                               padx=5,
                                                                               pady=5, ipadx=5, ipady=3)
ProjCategories_2_Dropdown.current(0)
ProjCategories_2_Dropdown.bind("<<ComboboxSelected>>", UpdateFuncDropDown_2)









Label(FrameLeft_Notebook_frame1R_1_1,font=("Segoe UI",9), text="Select Function",bg="white").grid(column=0,row=1,padx=5,pady=10,sticky='W',columnspan = 5)

FuncRevision = StringVar(FrameLeft_Notebook_frame1R_1_1, value='1.46')

Label(FrameLeft_Notebook_frame1R_1_1,font=("Segoe UI",9), text="Function revision",bg="white").grid(column=0,row=2,padx=5,pady=10,sticky='W')
#Entry(FrameLeft_Notebook_frame1R_1_1, width=20,textvariable=FuncRevision).grid(row=1, column=2,
#                                                                               columnspan=1,
#                                                                              sticky='W',
#                                                                               padx=10,
#                                                                              pady=5, ipadx=5, ipady=3)

def FuncRevisionsDropDownUserEnteredUpdated():
    pass

FunctionalityRevisions = [""]

FuncRevisionsDropDownUserEntered = ttk.Combobox(FrameLeft_Notebook_frame1R_1_1,values=FunctionalityRevisions , width = 25 , state="readonly" )
FuncRevisionsDropDownUserEntered.grid(row=2, column=2,
                                                                               columnspan=1,
                                                                               sticky='W',
                                                                               padx=10,
                                                                               pady=5, ipadx=5, ipady=3)

FuncRevisionsDropDownUserEntered.current(0)
#FuncRevisionsDropDownUserEntered.bind("<<ComboboxSelected>>", FuncRevisionsDropDownUserEnteredUpdated)





#ThreshHoldRev = StringVar(FrameLeft_Notebook_frame1R_1_1, value='')
#ThreshHoldRevEntry= Entry(FrameLeft_Notebook_frame1R_1_1, width=20,textvariable=ThreshHoldRev,state="disabled")
#ThreshHoldRevEntry.grid(row=1, column=3,
   #                                                                            columnspan=1,
  #                                                                             sticky='W',
 #                                                                              padx=10,
#                                                                               pady=5, ipadx=5, ipady=3)

FuncRevisionsDropDownUserEnteredThreshHold = ttk.Combobox(FrameLeft_Notebook_frame1R_1_1,values=FunctionalityRevisions , width = 25 , state="disabled" )
FuncRevisionsDropDownUserEnteredThreshHold.grid(row=2, column=3,
                                                                               columnspan=1,
                                                                               sticky='W',
                                                                               padx=10,
                                                                               pady=5, ipadx=5, ipady=3)

FuncRevisionsDropDownUserEnteredThreshHold.current(0)
#FuncRevisionsDropDownUserEnteredThreshHold.bind("<<ComboboxSelected>>", FuncRevisionsDropDownUserEntered)
def UpdateFUNCRevisionsinUserInputs():
    global FuncRevisionsDropDownUserEntered,FuncRevisionsDropDownUserEnteredThreshHold
    if len(FunctionalityRevisions) > 1:
        FuncRevisionsDropDownUserEntered.config(values=FunctionalityRevisions)
        FuncRevisionsDropDownUserEntered.current(0)
        if RevperationDropDownBtn.get() == "Within range" :
            FuncRevisionsDropDownUserEnteredThreshHold.config(values=FunctionalityRevisions)
            FuncRevisionsDropDownUserEnteredThreshHold.current(0)
        else:
            FuncRevisionsDropDownUserEnteredThreshHold.config(values=[""])
            FuncRevisionsDropDownUserEnteredThreshHold.current(0)
    else:

        FuncRevisionsDropDownUserEntered.config(values=[""])
        FuncRevisionsDropDownUserEntered.current(0)

        FuncRevisionsDropDownUserEnteredThreshHold.config(values=[""])
        FuncRevisionsDropDownUserEnteredThreshHold.current(0)



def FetchRevisionsFuncRev():
    global FunctionalityRevisions
    FunctionalityRevisions.clear()

    Command = "si viewprojecthistory --project=/EPB/SoftwareDevelopment/APPL/SW_Modules/{}/project.pj --fields=revision".format(FunctionsDropDownopions.get())

    try:
        response = CommandWin.Popen(Command, stdout=CommandWin.PIPE, stderr=CommandWin.PIPE)
        stdout, stderr = response.communicate(timeout=15)
        FunctionalityRevisions = list(stdout.decode().split()[1:])
        UpdateFUNCRevisionsinUserInputs()


    except Exception as error:
        MessagesLog("Error Fetching revisions -  "+str(error))


    pass
Button(FrameLeft_Notebook_frame1R_1_1,font=("Segoe UI",9),text="Fetch ",image = IconFilepath_FetchIcon ,compound= LEFT,command = FetchRevisionsFuncRev, fg="Dodgerblue4", bg="white",
                      relief="raised",bd=1,activebackground='white').grid(row=2, column=4,
                                                                               columnspan=1,
                                                                               sticky='W',
                                                                               padx=10,
                                                                               pady=5, ipadx=5, ipady=3)


RevisionOperationChosen = "Same as"
def RevisionOperationUpdated(event):
    global RevisionOperationChosen,FuncRevisionsDropDownUserEnteredThreshHold

    if RevperationDropDownBtn.get() == "Same as" :
        RevisionOperationChosen = str(RevperationDropDownBtn.get())
        FuncRevisionsDropDownUserEnteredThreshHold.config(state="disabled")
        #ThreshHoldRev.set("")
    elif RevperationDropDownBtn.get() == "Lesser than" :
        RevisionOperationChosen = str(RevperationDropDownBtn.get())
        FuncRevisionsDropDownUserEnteredThreshHold.config(state="disabled")
    elif RevperationDropDownBtn.get() == "Greater than" :
        RevisionOperationChosen = str(RevperationDropDownBtn.get())
        FuncRevisionsDropDownUserEnteredThreshHold.config(state="disabled")
    elif RevperationDropDownBtn.get() == "Within range" :
        RevisionOperationChosen = str(RevperationDropDownBtn.get())
        FuncRevisionsDropDownUserEnteredThreshHold.config(state="readonly")
    UpdateFUNCRevisionsinUserInputs()




RevperationDropDownBtn = ttk.Combobox(FrameLeft_Notebook_frame1R_1_1,values=["Same as", "Lesser than", "Greater than", "Within range"] , width = 25 , state="readonly" )
RevperationDropDownBtn.grid(row=2, column=1,
                                                                               columnspan=1,
                                                                               sticky='W',
                                                                               padx=5,
                                                                               pady=5, ipadx=5, ipady=3)

RevperationDropDownBtn.current(0)
RevperationDropDownBtn.bind("<<ComboboxSelected>>", RevisionOperationUpdated)


Label(FrameLeft_Notebook_frame1R_1_1,font=("Segoe UI",9), text="Function Usages in projects ",bg="white").grid(column=0,row=3,padx=5,pady=10,sticky='W')
LocateBtn = Button(FrameLeft_Notebook_frame1R_1_1,font=("Segoe UI",9),text=" Locate  ",command = LocateFunctionUsages, fg="white", bg="Dodgerblue4",
                      relief="raised")
LocateBtn.grid(row=3, column=1,
                                                                               columnspan=5,
                                                                               sticky='W',
                                                                               padx=5,
                                                                               pady=5, ipadx=5, ipady=3)





#$$$$$$$$$$$$$$$$$$$$$$$$$$


def FilterOutProj2BAnalysed(inputList) :
    TempData = []


    if len(Memory1_Proj2BanlysedWithList) >= 1:
        for revision in inputList:
            for withElem in Memory1_Proj2BanlysedWithList:
                if (withElem.upper().replace(" ","") in revision.upper().replace(" ",""))and (revision not in TempData):
                    TempData.append(revision)
    else: TempData = copy.deepcopy(inputList)

    TempData2 = []


    if len(Memory1_Proj2BanlysedWithOutList) >= 1:
        for revision in TempData:
            ToBeCopiedFlag = 0
            for withOutElem in Memory1_Proj2BanlysedWithOutList:
                if withOutElem != "":
                    if (withOutElem.upper().replace(" ","") in revision.upper().replace(" ","")) :
                        ToBeCopiedFlag = 1
                else:
                    if (revision not in TempData2):
                        TempData2.append(revision)
                        ToBeCopiedFlag = 1
            if ToBeCopiedFlag == 0:
                TempData2.append(revision)
    else : TempData2 = copy.deepcopy(TempData)

    TempData3 = []

    if MemoryCheckBoxNolabel == 1:
        for rev in TempData2:
            if "(" in rev :
                TempData3.append(rev)
    else : TempData3 = copy.deepcopy(TempData2)

    return TempData3

def Filter_2_Prj2Anlys ():
    global Memory1_Proj2BanlysedWith,Memory1_Proj2BanlysedWithOut
    EDIT_Filter_2_Projs2Banalysed = Toplevel(GUITopFrame)
    EDIT_Filter_2_Projs2Banalysed.config(bg="white")
    EDIT_Filter_2_Projs2Banalysed.title("Filter Projects to be analysed")
    EDIT_Filter_2_Projs2Banalysed.resizable(False, False)  # x,y resizabling disabled
    #EDIT_Filter_2_Projs2Banalysed.minsize(500, 200)

    try:
        EDIT_Filter_2_Projs2Banalysed.iconbitmap(IconFilepath)
    except:
        pass



    EDIT_Filter_2_Projs2Banalysed.grab_set()


    Label(EDIT_Filter_2_Projs2Banalysed, font=("Segoe UI", 9),bg= "white" ,text="Include project labels\n WITH keywords").grid(column=0, row=1,
                                                                                                       padx=5, pady=10,
                                                                                                       sticky='W')



    KeyWordsInputPane = scrolledtext.ScrolledText(EDIT_Filter_2_Projs2Banalysed,
                                              wrap=tkinter.WORD,

                                              height=4,width =40,
                                              font=("Segoe UI",
                                                    10), background="white", foreground='grey17')
    #KeyWordsInputPane.ScrolledText()
    KeyWordsInputPane.grid(column=1, row=1,padx=5, pady=10,sticky='W',columnspan = 4)
    KeyWordsInputPane.focus()
    KeyWordsInputPane.insert(tkinter.INSERT, Memory1_Proj2BanlysedWith.replace("\n", ""))

    Label(EDIT_Filter_2_Projs2Banalysed, font=("Segoe UI", 9), bg="white",
          text="Include project labels\n WITHOUT keywords").grid(column=0, row=2,
                                                                 padx=5, pady=10,
                                                                 sticky='W')
    KeyWordsInputPaneWithout = scrolledtext.ScrolledText(EDIT_Filter_2_Projs2Banalysed,
                                              wrap=tkinter.WORD,

                                              height=4,width =40,
                                              font=("Segoe UI",
                                                    10), background="white", foreground='grey17')
    #KeyWordsInputPane.ScrolledText()
    KeyWordsInputPaneWithout.grid(column=1, row=2,padx=5, pady=10,sticky='W',columnspan = 4)
    KeyWordsInputPaneWithout.focus()
    KeyWordsInputPaneWithout.insert(tkinter.INSERT, Memory1_Proj2BanlysedWithOut.replace("\n", ""))

    var1 = tkinter.IntVar()

    def checkboxTriggered():
        pass
    c1 = tkinter.Checkbutton(EDIT_Filter_2_Projs2Banalysed,bg="white", text='Exclude project checkpoints with empty Labels', \
                        variable=var1, onvalue=1, offvalue=0, command=checkboxTriggered,relief = "groove",bd=0)
    c1.grid(column=2, row=0,
                                                                     padx=5, pady=10,
                                                                        sticky='W')
    var1.set(MemoryCheckBoxNolabel)


    def Apply_Filter_2():

        global Memory1_Proj2BanlysedWith,Memory1_Proj2BanlysedWithOut,\
            Memory1_Proj2BanlysedWithList,Memory1_Proj2BanlysedWithOutList,MemoryCheckBoxNolabel

        Memory1_Proj2BanlysedWithList = str(KeyWordsInputPane.get("1.0", tkinter.END)).replace(" ","").replace("\n","").split(",")
        Memory1_Proj2BanlysedWithOutList = str(KeyWordsInputPaneWithout.get("1.0", tkinter.END)).replace(" ","").replace("\n","").split(",")

        Memory1_Proj2BanlysedWith = str(KeyWordsInputPane.get("1.0", tkinter.END))
        Memory1_Proj2BanlysedWithOut = str(KeyWordsInputPaneWithout.get("1.0", tkinter.END))
        MemoryCheckBoxNolabel = var1.get()
        EDIT_Filter_2_Projs2Banalysed.destroy()


    Button(EDIT_Filter_2_Projs2Banalysed, font=("Segoe UI", 9), text="     Save     ", command=Apply_Filter_2,
           fg="white", bg="Dodgerblue4",activebackground='white',
           relief="raised").grid(column=2, row=3,padx=110, pady=10,sticky='W',columnspan = 1)


    def Reset():
        global Memory1_Proj2BanlysedWith,Memory1_Proj2BanlysedWithOut,\
            Memory1_Proj2BanlysedWithOutList,Memory1_Proj2BanlysedWithList,MemoryCheckBoxNolabel
        KeyWordsInputPane.delete('0.0', END)
        KeyWordsInputPaneWithout.delete('0.0', END)
        MemoryCheckBoxNolabel = 0
        var1.set(MemoryCheckBoxNolabel)
        Memory1_Proj2BanlysedWithList.clear()
        Memory1_Proj2BanlysedWithOutList.clear()
        Memory1_Proj2BanlysedWith = str(KeyWordsInputPane.get("1.0", tkinter.END))
        Memory1_Proj2BanlysedWithOut = str(KeyWordsInputPaneWithout.get("1.0", tkinter.END))
        #filterDropDown_w_wo_DevProjRevs = FilterDropDown_3_WWO.get()
        #Update_3_DevPathsDropDown(ProjectCheckPointsList_3)

    Button(EDIT_Filter_2_Projs2Banalysed, font=("Segoe UI", 9), text=" Reset Fields ", command=Reset,
           fg="white", bg="Dodgerblue4",activebackground='white',
           relief="raised").grid(column=2, row=3, padx=5, pady=10, sticky='W', columnspan=1)




#$$$$$$$$$$$$$$$$$$$$$$$$$$




FilterProjectsToAnlysButton = Button(FrameLeft_Notebook_frame1R_1_1,font=("Segoe UI",9),text="Filter ",command = Filter_2_Prj2Anlys, image = IconFilepath_FilterIcon ,compound= LEFT,fg="black", bg="white",
                      relief="raised",activebackground='white')
FilterProjectsToAnlysButton.grid(row=3, column=1,
                                                                               columnspan=2,
                                                                               sticky='W',
                                                                               padx=80,
                                                                               pady=5)












###############################################
#Kiran Code 2 #Function 3

def GetProjFunctionsRevisions():
    global ProjectsToAssess
    if FunctionsCheckpointDropDownFuncMode.get() == "Single":
        ProjCatFoldrStruct = ProjCatFoldrStruct_Database[ProjectCategoriesDropDown_3.get()]
        #print(ProjCatFoldrStruct)
        ProjectsToAssess.clear()
        ProjectsToAssess.append(
            str(ProjCatFoldrStruct[0]).replace("project.pj", '/'.join(ProjCatFoldrStruct[1:]) + "/project.pj"))
        Revision = str(ProjCheckPoints_3_DropDown.get()).split("(")[0]
        #print(ProjCatFoldrStruct)
        #print(Revision)

        Project_3_CheckPoint = GetSubProjectRevisionsLevelN(ProjCatFoldrStruct,Revision)
        #print("Project_3_CheckPoint",Project_3_CheckPoint)

    else:

        Project_3_CheckPoint = ""
        if (Filter_ProjectsToAssess()) == 1:
            pass
        else:
            return
    Datadisplay = []
    projectToAnalyzeCounter = 0
    Datadisplay.clear()
    ListofPBCUnits = ["Project","ActuatorStateEnhancement","AM","AMS","AutoAdjust","BrakeHandler",
                                   "BrakeModule","Ca_Pbc","CascadeControl","CFC","DemandArbitrator","DSD",
                                   "FunctionManager","GDA","GSP_Pbc","HPS","HUFunc","MCCA","OutOfSpecMessage_Pbc",
                                    "ParkRequest","PBA","PBAInterface","PBDH","PBFH","PR","PRD","RC","RCC","Reclamp",
                                   "RWU","SP","TemperatureModel","Vehicle_Pbc"]
    FunctionsAvailable = []
    for projectToAnalyze in ProjectsToAssess:
        #print(projectToAnalyze)
        #print(ProjCatFoldrStruct_Database)
        for proj in Projects_Categorised_DB:
            if (proj['ProjectPath'] == str(projectToAnalyze)) :
                ProjCatFoldrStruct = ProjCatFoldrStruct_Database[
                    Categories_Proj_Wrapper[proj['ProjectCategory']]]
                break


        if (FunctionsCheckpointDropDownFuncMode.get() == "Multiple")  :
            projTemp12 = str(projectToAnalyze).replace("project.pj",
                                                                  '/'.join(ProjCatFoldrStruct[1:]) + "/project.pj")
        else :
            projTemp12 = projectToAnalyze

        projectToAnalyzeCounter +=1
        FunctionsAvailable.clear()
        #project1 = projectToAnalyze
        #print(projectToAnalyze,Project_3_CheckPoint,TempFileSavePath)
        SubProjectRevisionsNotUpdated = GetSubProjectRevisionsToFile(projTemp12,Project_3_CheckPoint,TempFileSavePath)
        if SubProjectRevisionsNotUpdated == 1:
            continue

        #cmd = 'cmd /c "{}"'.format(Command)
        #Value = str(os.system(cmd))


        a1_file = open(TempFileSavePath, "r")
        Linenum = 0

        for line in (a1_file):
            #print(line)
            if "shared-build-subproject" in line:
                FunctionsAvailable.append(line)
        #print(FunctionsAvailable)


        #for Linenum, line in enumerate(a1_file, 1):
        #    if "shared-build-subproject" in line:
        #        break


        SWUnitsDict = dict.fromkeys(ListofPBCUnits)

        SWUnitsDict["Project"] = projectToAnalyze


        for line in FunctionsAvailable:
            Cleaned_line1 = line.strip()
            Cleaned_line1 = " ".join(Cleaned_line1.split())
            start = Cleaned_line1.find("(") + len("(")
            end = Cleaned_line1.find(")")
            Revision1 = Cleaned_line1[start:end]
            SWUnit1 = Cleaned_line1.split('/project.pj')[0]
            SWUnitsDict[SWUnit1]=Revision1

        Datadisplay.append(copy.deepcopy(SWUnitsDict))
        #print("Datadisplay",str(Datadisplay))

        a1_file.close()
        UpdateProgressStatus(len(ProjectsToAssess), projectToAnalyzeCounter)
    UpdateProgressStatus(len(ProjectsToAssess), projectToAnalyzeCounter)
    UpdateVisualTable(Datadisplay)

def ProjectRevisions_FunctionProjMode_3(Mode):
    global Project_Categories_3_DropDown,ProjectCategoriesDropDown_3,FilterDevPathsButton1,ProjCheckPoints_3_DropDown,\
        DropDown3_DevPathOptions,FunctionsCheckpointDropDownFuncMode,ProjectRevRevision,DevPaths_3_FetchBtn1, \
        DevPaths_3_FetchBtn2_ProjCheckPoints, FilterDevPathsButton2
    if FunctionsCheckpointDropDownFuncMode.get() == "Single":
        if(len(ProjectsList_stored)) == 0 :
            ErrorPrompt("Input Missing" , "Please Load the Projects from either Database/Server.")
            FunctionsCheckpointDropDownFuncMode.current(1)
            return
        Project_Categories_3_DropDown = copy.deepcopy(ProjectsList_stored)
        #ProjectCategoriesDropDown_3.config(values=Project_Categories_3_DropDown)
        #ProjectCategoriesDropDown_3.current(0)
        ProjectCategoriesDropDown_3.config(state="readonly")
        DevPaths_3_FetchBtn1.config(state="normal")
        DevPaths_3_FetchBtn2_ProjCheckPoints.config(state="normal")
        FilterDevPathsButton1.config(state="normal")
        FilterDevPathsButton2.config(state="normal")
        DropDown3_DevPathOptions.config(state="readonly")
        DropDown3_DevPathOptions.config(state="readonly")
        ProjCheckPoints_3_DropDown.config(state="readonly")

    else:
        #ProjectCategoriesDropDown_3.config(values=[""])
        #ProjectCategoriesDropDown_3.current(0)
        ProjectCategoriesDropDown_3.config(state="disabled")
        DevPaths_3_FetchBtn1.config(state="disabled")
        DevPaths_3_FetchBtn2_ProjCheckPoints.config(state="disabled")
        FilterDevPathsButton1.config(state="disabled")
        FilterDevPathsButton2.config(state="disabled")
        DropDown3_DevPathOptions.config(state="disabled")
        ProjCheckPoints_3_DropDown.config(state="disabled")
        ProjectRevRevision.set("")


def ProjectFuncConfig_FunctionProjMode(Mode):
    global Project_Categories_3_DropDown,FunctionsConfigDropDownopions,\
        FunctionsConfigEntry,FunctionsConfigDropDownFuncMode
    if FunctionsConfigDropDownFuncMode.get() == "Single":
        if(len(ProjectsList_stored)) == 0 :
            ErrorPrompt("Input Missing" , "Please Load the Projects from either Database/Server.")
            FunctionsConfigDropDownFuncMode.current(1)
            return
        Project_Categories_3_DropDown = copy.deepcopy(ProjectsList_stored)
        FunctionsConfigDropDownopions.config(values=Project_Categories_3_DropDown)
        FunctionsConfigDropDownopions.current(0)
        FunctionsConfigDropDownopions.config(state="readonly")
        FunctionsConfigEntry.config(state="normal")
    else:

        FunctionsConfigDropDownopions.config(state="disabled")
        FunctionsConfigEntry.config(state="disabled")




Project_Categories_3_DropDown = ["EPBi PBC System (PBC and SSM PB Application)",
                                "PBC Application Only",
                                "SSM_PB Application Only",
                                "EPB5 (MMC Application)"]

ProjectCategoriesDropDown_3 = ttk.Combobox(FrameLeft_Notebook_frame1R_1_2, values=Project_Categories_3_DropDown , width = 50 , state="disabled" )
ProjectCategoriesDropDown_3.grid(row=0, column=4,
                                                                               columnspan=20,
                                                                               sticky='W',
                                                                               padx=5,
                                                                               pady=5, ipadx=5, ipady=3)
ProjectCategoriesDropDown_3.current(0)
ProjectCategoriesDropDown_3.config(state = "disabled")



Label(FrameLeft_Notebook_frame1R_1_2,font=("Segoe UI",9), text="Project Category",bg="white").grid(column=2,row=0,padx=5,pady=10,sticky='W')
Label(FrameLeft_Notebook_frame1R_1_2,font=("Segoe UI",9), text="Development Paths",bg="white").grid(column=0,row=2,padx=5,pady=10,sticky='W')
ProjectRevRevision = StringVar(FrameLeft_Notebook_frame1R_1_2)
ProjectRevRevision.set("")


List_3_DevPathsAvailable = [""]
DropDown3_DevPathOptions = ttk.Combobox(FrameLeft_Notebook_frame1R_1_2,values=List_3_DevPathsAvailable , width = 45 , state="disabled" )
DropDown3_DevPathOptions.grid(row=2, column=1,
                                                                               columnspan=10,
                                                                               sticky='W',
                                                                               padx=5,
                                                                               pady=5, ipadx=5, ipady=3)
DropDown3_DevPathOptions.current(0)



def Update_3_DevPathsDropDown(devpaths):
    global DropDown3_DevPathOptions
    if len(devpaths) >=1:
        DropDown3_DevPathOptions.config(value = devpaths)
        DropDown3_DevPathOptions.config( state="readonly")
        DropDown3_DevPathOptions.current((0))
    else:
        DropDown3_DevPathOptions.config(value=[""])
        DropDown3_DevPathOptions.current((0))
        DropDown3_DevPathOptions.config(state="readonly")


def FetchDevPaths_3():
    global List_3_DevPathsAvailable
    List_3_DevPathsAvailable.clear()
    try:
        projPath = str(ProjCatFoldrStruct_Database[str(ProjectCategoriesDropDown_3.get())][0]).replace("project.pj",str(ProjCatFoldrStruct_Database[str(ProjectCategoriesDropDown_3.get())][1])+"/project.pj")
        List_3_DevPathsAvailable = GetDevpathsinProject(projPath)
    except Exception as exception :
        MessagesLog(str(exception))

    Update_3_DevPathsDropDown(List_3_DevPathsAvailable)




def Filter_3_DevPaths ():
    global filterKeywordsInputMemory

    if len(List_3_DevPathsAvailable) <=1 and (List_3_DevPathsAvailable[0] ==""):
        ErrorPrompt("Input Error" , "Please Fetch Development paths from the Server before this operation")
        return

    EDIT_Filter_3_DevPaths = Toplevel(GUITopFrame)
    EDIT_Filter_3_DevPaths.config(bg="white")
    EDIT_Filter_3_DevPaths.title("Filter Development Paths")
    EDIT_Filter_3_DevPaths.resizable(False, False)  # x,y resizabling disabled
    #EDIT_Filter_3_DevPaths.minsize(500, 200)

    try:
        EDIT_Filter_3_DevPaths.iconbitmap(IconFilepath)
    except:
        pass


    EDIT_Filter_3_DevPaths.grab_set()

    Label(EDIT_Filter_3_DevPaths, font=("Segoe UI", 9),bg= "white" ,text="Include Development paths").grid(column=0, row=0,
                                                                                                       padx=5, pady=10,
                                                                                                       sticky='W')
    FilterDropdown_w_WO = ["With", "Without"]
    FilterDropDown_3_WWO = ttk.Combobox(EDIT_Filter_3_DevPaths, values=FilterDropdown_w_WO, width=10, state="readonly")
    FilterDropDown_3_WWO.grid(column=1, row=0,

                                                                                                       sticky='W')
    FilterDropDown_3_WWO.current(FilterDropdown_w_WO.index(filterDropDown_w_wo))
    Label(EDIT_Filter_3_DevPaths, font=("Segoe UI", 9), bg="white", text="keywords :").grid(column=2,
                                                                                                           row=0,

                                                                                                           pady=10,
                                                                                                           sticky='W')
    KeyWordsInputPane = scrolledtext.ScrolledText(EDIT_Filter_3_DevPaths,
                                              wrap=tkinter.WORD,

                                              height=5,width =40,
                                              font=("Segoe UI",
                                                    10), background="white", foreground='grey17')
    #KeyWordsInputPane.ScrolledText()
    KeyWordsInputPane.grid(column=0, row=1,padx=5, pady=10,sticky='W',columnspan = 4)
    KeyWordsInputPane.focus()

    KeyWordsInputPane.insert(tkinter.INSERT,filterKeywordsInputMemory.replace("\n",""))


    def Apply_Filter():
        global filterKeywordsInputMemory,filterDropDown_w_wo
        FilterKeywords = str(KeyWordsInputPane.get("1.0", tkinter.END)).replace(" ","").replace("\n","").split(",")
        #print(FilterKeywords)
        TempDevPaths = []
        TempDevPaths.clear()
        if FilterDropDown_3_WWO.get() == "With":
            for Filter_3_Keyword  in FilterKeywords:
                for DevPath in List_3_DevPathsAvailable:
                        if (str(Filter_3_Keyword).upper().strip().replace(" ", "") in str(DevPath).upper().strip().replace(
                            " ", "")) and  (DevPath not in TempDevPaths):
                            TempDevPaths.append(DevPath)
            filterKeywordsInputMemory = str(KeyWordsInputPane.get("1.0", tkinter.END))
            filterDropDown_w_wo = FilterDropDown_3_WWO.get()
        else:
            TempDevPaths = copy.deepcopy(List_3_DevPathsAvailable)
            #print(TempDevPaths)
            for DevPath in List_3_DevPathsAvailable:
                for Filter_3_Keyword in FilterKeywords:
                        if (str(Filter_3_Keyword).upper().strip().replace(" ", "")  in str(
                            DevPath).upper().strip().replace(" ", "")) and (len(Filter_3_Keyword)>1) :
                            try:TempDevPaths.remove(DevPath)
                            except:pass
            filterKeywordsInputMemory = str(KeyWordsInputPane.get("1.0", tkinter.END))
            filterDropDown_w_wo = FilterDropDown_3_WWO.get()

        #List_3_DevPathsAvailable = copy.deepcopy(TempDevPaths)
        #print(List_3_DevPathsAvailable)
        Update_3_DevPathsDropDown(TempDevPaths)

        EDIT_Filter_3_DevPaths.destroy()




    Button(EDIT_Filter_3_DevPaths, font=("Segoe UI", 9), text=" Apply Filter ", command=Apply_Filter,
           fg="white", bg="Dodgerblue4",activebackground='white',
           relief="raised").grid(column=2, row=2,padx=5, pady=10,sticky='W',columnspan = 1)

    def cancel() : EDIT_Filter_3_DevPaths.destroy()
    Button(EDIT_Filter_3_DevPaths, font=("Segoe UI", 9), text="  Close  ", command=cancel,
           fg="white", bg="Dodgerblue4",activebackground='white',
           relief="raised").grid(column=3, row=2,padx=5, pady=10,sticky='W',columnspan = 1)
    def Reset():
        global filterDropDown_w_wo,filterKeywordsInputMemory
        KeyWordsInputPane.delete('0.0', END)
        filterKeywordsInputMemory = str(KeyWordsInputPane.get("1.0", tkinter.END))
        filterDropDown_w_wo = FilterDropDown_3_WWO.get()
        Update_3_DevPathsDropDown(List_3_DevPathsAvailable)

    Button(EDIT_Filter_3_DevPaths, font=("Segoe UI", 9), text=" Reset  ", command=Reset,
           fg="white", bg="Dodgerblue4",activebackground='white',
           relief="raised").grid(column=1, row=2, padx=5, pady=10, sticky='W', columnspan=1)



Label(FrameLeft_Notebook_frame1R_1_2,font=("Segoe UI",9), text="Project checkpoints",bg="white").grid(column=0,row=3,padx=5,pady=10,sticky='W')





ProjectCheckPointsList_3 = [""]
ProjCheckPoints_3_DropDown = ttk.Combobox(FrameLeft_Notebook_frame1R_1_2, values=ProjectCheckPointsList_3 , width = 45,state="disabled"  )
ProjCheckPoints_3_DropDown.grid(row=3, column=1,
                                                                               columnspan=10,
                                                                               sticky='W',
                                                                               padx=5,
                                                                               pady=5, ipadx=5, ipady=3)
ProjCheckPoints_3_DropDown.current(0)




Label(FrameLeft_Notebook_frame1R_1_2,font=("Segoe UI",9), text="Functions Checkpointed at",bg="white").grid(column=0,row=4,padx=5,pady=10,sticky='W')
Analyse_3_Btn = Button(FrameLeft_Notebook_frame1R_1_2,font=("Segoe UI",9),text="Analyse ",command = GetProjFunctionsRevisions, fg="white", bg="Dodgerblue4",
                      relief="raised")
Analyse_3_Btn.grid(row=4, column=1,
                                                                               columnspan=5,
                                                                               sticky='W',
                                                                               padx=5,
                                                                               pady=5, ipadx=5, ipady=3)
DevPaths_3_FetchBtn1 = Button(FrameLeft_Notebook_frame1R_1_2,font=("Segoe UI",9),text="Fetch ",command = FetchDevPaths_3, image = IconFilepath_FetchIcon ,compound= LEFT,fg="black", bg="white",
                      relief="raised",state = "disabled",bd=1,activebackground='white')
DevPaths_3_FetchBtn1.grid(row=2, column=11,
                                                                               columnspan=1,
                                                                               sticky='W',
                                                                               padx=5,
                                                                               pady=5)



ZFIconScreen = Label(FrameLeft_Notebook_frame1R_1_2, image=IconFilepath_LogoScreenZF,relief='flat',bd=0,activebackground='white')
ZFIconScreen.grid(column=48, row=6, padx=5, pady=10,rowspan = 10)



def updateProjCheckpoints_3_Dropdown(DropdownList):
    global ProjCheckPoints_3_DropDown
    #print(DropdownList)
    ProjCheckPoints_3_DropDown.config(values =DropdownList)
    ProjCheckPoints_3_DropDown.current(0)


def FetchProjCheckpoints_3():

    global ProjectCheckPointsList_3

    if len(DropDown3_DevPathOptions.get()) <2:
        ErrorPrompt("Input Error" , "Please Select appropriate Development path first.")
        return

    projPath = str(ProjCatFoldrStruct_Database[str(ProjectCategoriesDropDown_3.get())][0]).replace("project.pj", str(
        ProjCatFoldrStruct_Database[str(ProjectCategoriesDropDown_3.get())][1]) + "/project.pj")

    rev = str(str(DropDown3_DevPathOptions.get()).split("(")[0]).strip()
    #print(rev)
    #print(projPath)
    try:
        ProjectCheckPointsList_3 = GetProjectRevisionsLabelsinProject(projPath,rev)
        #ProjectCheckPointsList_3)
    except Exception as exception:
        MessagesLog(str(exception))
    updateProjCheckpoints_3_Dropdown(ProjectCheckPointsList_3)



def Filter_3_DevPathsProjectCheckPts ():
    global filterKeywordsInputMemoryDevpthProjRev

    if len(ProjectCheckPointsList_3) <1:
        ErrorPrompt("Input Error" , "Please Fetch Development paths from the Server before this operation")
        return

    EDIT_Filter_3_DevPathsProjectCheckPts = Toplevel(GUITopFrame)
    EDIT_Filter_3_DevPathsProjectCheckPts.config(bg="white")
    EDIT_Filter_3_DevPathsProjectCheckPts.title("Filter Project Checkpoints")
    EDIT_Filter_3_DevPathsProjectCheckPts.resizable(False, False)  # x,y resizabling disabled
    #EDIT_Filter_3_DevPathsProjectCheckPts.minsize(500, 200)

    try:
        EDIT_Filter_3_DevPathsProjectCheckPts.iconbitmap(IconFilepath)
    except:
        pass


    EDIT_Filter_3_DevPathsProjectCheckPts.grab_set()

    Label(EDIT_Filter_3_DevPathsProjectCheckPts, font=("Segoe UI", 9),bg= "white" ,text="Include Project checkpoints").grid(column=0, row=0,
                                                                                                       padx=5, pady=10,
                                                                                                       sticky='W')
    FilterDropdown_w_WO = ["With", "Without"]
    FilterDropDown_3_WWO = ttk.Combobox(EDIT_Filter_3_DevPathsProjectCheckPts, values=FilterDropdown_w_WO, width=10, state="readonly")
    FilterDropDown_3_WWO.grid(column=1, row=0,

                                                                                                       sticky='W')
    FilterDropDown_3_WWO.current(FilterDropdown_w_WO.index(filterDropDown_w_wo_DevProjRevs))
    Label(EDIT_Filter_3_DevPathsProjectCheckPts, font=("Segoe UI", 9), bg="white", text="keywords :").grid(column=2,
                                                                                                           row=0,

                                                                                                           pady=10,
                                                                                                           sticky='W')
    KeyWordsInputPane = scrolledtext.ScrolledText(EDIT_Filter_3_DevPathsProjectCheckPts,
                                              wrap=tkinter.WORD,

                                              height=5,width =40,
                                              font=("Segoe UI",
                                                    10), background="white", foreground='grey17')
    #KeyWordsInputPane.ScrolledText()
    KeyWordsInputPane.grid(column=0, row=1,padx=5, pady=10,sticky='W',columnspan = 4)
    KeyWordsInputPane.focus()

    KeyWordsInputPane.insert(tkinter.INSERT,filterKeywordsInputMemoryDevpthProjRev.replace("\n",""))


    def Apply_Filter():
        global filterKeywordsInputMemoryDevpthProjRev,filterDropDown_w_wo_DevProjRevs
        FilterKeywords = str(KeyWordsInputPane.get("1.0", tkinter.END)).replace(" ","").replace("\n","").split(",")
        #print(FilterKeywords)
        TempDevPaths = []
        TempDevPaths.clear()
        if FilterDropDown_3_WWO.get() == "With":
            for Filter_3_Keyword  in FilterKeywords:
                for DevPath in ProjectCheckPointsList_3:
                        if (str(Filter_3_Keyword).upper().strip().replace(" ", "") in str(DevPath).upper().strip().replace(
                            " ", "")) and  (DevPath not in TempDevPaths):
                            TempDevPaths.append(DevPath)
            filterKeywordsInputMemoryDevpthProjRev = str(KeyWordsInputPane.get("1.0", tkinter.END))
            filterDropDown_w_wo_DevProjRevs = FilterDropDown_3_WWO.get()
        else:
            TempDevPaths = copy.deepcopy(ProjectCheckPointsList_3)
            #print(TempDevPaths)
            for DevPath in ProjectCheckPointsList_3:
                for Filter_3_Keyword in FilterKeywords:
                        if (str(Filter_3_Keyword).upper().strip().replace(" ", "")  in str(
                            DevPath).upper().strip().replace(" ", "")) and (len(Filter_3_Keyword)>1) :
                            try:TempDevPaths.remove(DevPath)
                            except:pass
            filterKeywordsInputMemoryDevpthProjRev = str(KeyWordsInputPane.get("1.0", tkinter.END))
            filterDropDown_w_wo_DevProjRevs = FilterDropDown_3_WWO.get()

        #ProjectCheckPointsList_3 = copy.deepcopy(TempDevPaths)
        #print(ProjectCheckPointsList_3)
        updateProjCheckpoints_3_Dropdown(TempDevPaths)

        EDIT_Filter_3_DevPathsProjectCheckPts.destroy()




    Button(EDIT_Filter_3_DevPathsProjectCheckPts, font=("Segoe UI", 9), text=" Apply Filter ", command=Apply_Filter,
           fg="white", bg="Dodgerblue4",activebackground='white',
           relief="raised").grid(column=2, row=2,padx=5, pady=10,sticky='W',columnspan = 1)

    def cancel() : EDIT_Filter_3_DevPathsProjectCheckPts.destroy()
    Button(EDIT_Filter_3_DevPathsProjectCheckPts, font=("Segoe UI", 9), text="  Close  ", command=cancel,
           fg="white", bg="Dodgerblue4",activebackground='white',
           relief="raised").grid(column=3, row=2,padx=5, pady=10,sticky='W',columnspan = 1)
    def Reset():
        global filterDropDown_w_wo_DevProjRevs,filterKeywordsInputMemoryDevpthProjRev
        KeyWordsInputPane.delete('0.0', END)
        filterKeywordsInputMemoryDevpthProjRev = str(KeyWordsInputPane.get("1.0", tkinter.END))
        filterDropDown_w_wo_DevProjRevs = FilterDropDown_3_WWO.get()
        Update_3_DevPathsDropDown(ProjectCheckPointsList_3)

    Button(EDIT_Filter_3_DevPathsProjectCheckPts, font=("Segoe UI", 9), text=" Reset  ", command=Reset,
           fg="white", bg="Dodgerblue4",activebackground='white',
           relief="raised").grid(column=1, row=2, padx=5, pady=10, sticky='W', columnspan=1)





DevPaths_3_FetchBtn2_ProjCheckPoints = Button(FrameLeft_Notebook_frame1R_1_2,font=("Segoe UI",9),text="Fetch ",command = FetchProjCheckpoints_3, image = IconFilepath_FetchIcon ,compound= LEFT,fg="black", bg="white",
                      relief="raised",state = "disabled",bd=1,activebackground='white')
DevPaths_3_FetchBtn2_ProjCheckPoints.grid(row=3, column=11,
                                                                               columnspan=1,
                                                                               sticky='W',
                                                                               padx=5,
                                                                               pady=5)

FilterDevPathsButton1 = Button(FrameLeft_Notebook_frame1R_1_2,font=("Segoe UI",9),text="Filter ",command = Filter_3_DevPaths, image = IconFilepath_FilterIcon ,compound= LEFT,fg="black", bg="white",
                      relief="raised",state = "disabled",activebackground='white')
FilterDevPathsButton1.grid(row=2, column=12,
                                                                               columnspan=1,
                                                                               sticky='W',
                                                                               padx=5,
                                                                               pady=5)
FilterDevPathsButton2 = Button(FrameLeft_Notebook_frame1R_1_2,font=("Segoe UI",9),text="Filter ",command = Filter_3_DevPathsProjectCheckPts, image = IconFilepath_FilterIcon ,compound= LEFT,fg="black", bg="white",
                      relief="raised",state = "disabled",activebackground='white')
FilterDevPathsButton2.grid(row=3, column=12,
                                                                               columnspan=1,
                                                                               sticky='W',
                                                                               padx=5,
                                                                               pady=5)


Label(FrameLeft_Notebook_frame1R_1_2,font=("Segoe UI",9), text="Project(s) to Evaluate ",bg="white").grid(column=0,row=0,padx=5,pady=10,sticky='W')

FunctionsCheckpointDropDownFuncMode = ttk.Combobox(FrameLeft_Notebook_frame1R_1_2, values=["Single","Multiple"] , width = 15,state="readonly"  )
FunctionsCheckpointDropDownFuncMode.grid(row=0, column=1,
                                                                               columnspan=1,
                                                                               sticky='W',
                                                                               padx=5,
                                                                               pady=5, ipadx=5, ipady=3)
FunctionsCheckpointDropDownFuncMode.current(1)
FunctionsCheckpointDropDownFuncMode.bind("<<ComboboxSelected>>", ProjectRevisions_FunctionProjMode_3)



Label(FrameLeft_Notebook_frame1R_1_0,font=("Segoe UI",9), text="Project(s) to Evaluate ",bg="white").grid(column=0,row=0,padx=5,pady=10,sticky='W')
FunctionsConfigDropDownFuncMode = ttk.Combobox(FrameLeft_Notebook_frame1R_1_0, values=["Single","Multiple"] , width = 25,state="readonly"  )
FunctionsConfigDropDownFuncMode.grid(row=0, column=1,
                                                                               columnspan=1,
                                                                               sticky='W',
                                                                               padx=5,
                                                                               pady=5, ipadx=5, ipady=3)
FunctionsConfigDropDownFuncMode.current(1)
FunctionsConfigDropDownFuncMode.bind("<<ComboboxSelected>>", ProjectFuncConfig_FunctionProjMode)

Label(FrameLeft_Notebook_frame1R_1_0,font=("Segoe UI",9), text="Project Category",bg="white").grid(column=0,row=1,padx=5,pady=10,sticky='W')

FunctionsConfigDropDownopions = ttk.Combobox(FrameLeft_Notebook_frame1R_1_0, values=sorted(Project_Categories_3_DropDown) , width = 90 , state="disabled" )
FunctionsConfigDropDownopions.grid(row=1, column=1,
                                                                               columnspan=3,
                                                                               sticky='W',
                                                                               padx=5,
                                                                               pady=5, ipadx=5, ipady=3)
FunctionsConfigDropDownopions.current(0)
FunctionsConfigDropDownopions.config(state = "disabled")


Label(FrameLeft_Notebook_frame1R_1_0,font=("Segoe UI",9), text="Project Revision",bg="white").grid(column=0,row=2,padx=5,pady=10,sticky='W')
FunctionsConfigRevisionEntryVar = StringVar(FrameLeft_Notebook_frame1R_1_0)
FunctionsConfigRevisionEntryVar.set("")
FunctionsConfigEntry = Entry(FrameLeft_Notebook_frame1R_1_0, width=28,textvariable=FunctionsConfigRevisionEntryVar)
FunctionsConfigEntry.grid(row=2, column=1,
                                                                               columnspan=1,
                                                                               sticky='W',
                                                                               padx=5,
                                                                               pady=5, ipadx=5, ipady=3)
FunctionsConfigEntry.config(state="disabled")


Label(FrameLeft_Notebook_frame1R_1_0,font=("Segoe UI",9), text="Functions (Enabled/Disabled)",bg="white").grid(column=0,row=3,padx=5,pady=10,sticky='W')
ValidateDetailsBtn = Button(FrameLeft_Notebook_frame1R_1_0,font=("Segoe UI",9),text="Evaluate",command = downloadFuncConfigFiles, fg="white", bg="Dodgerblue4",
                      relief="raised")
ValidateDetailsBtn.grid(row=3, column=1,
                                                                               columnspan=5,
                                                                               sticky='W',
                                                                               padx=5,
                                                                               pady=5, ipadx=5, ipady=3)
###############################################
#Library functions:


def GetSubprojectRevision(Project,ProjectRevision,Subproject):

    SubprojectRevision = ""
    Command = "si viewproject -N --project={} --projectRevision={} {}/project.pj".format(Project,ProjectRevision,Subproject)
    #print("GetSubprojectRevision" , Command)
    try:
        response = CommandWin.Popen(Command, stdout=CommandWin.PIPE, stderr=CommandWin.PIPE)
        stdout, stderr = response.communicate(timeout=15)
        SubprojectRevision = str(stdout)
        SubprojectNotFound = "The file {}/project.pj is not a current or destined or pending member or a subproject of {}.".format(Subproject,Project)

        if stdout == SubprojectNotFound:
            SubprojectRevision = "NotFound"
        else:
            start = SubprojectRevision.find("/project.pj (") + len("/project.pj (")
            end = SubprojectRevision.find(")")
            SubprojectRevision = SubprojectRevision[start:end]

    except Exception as error:
        MessagesLog("Error Fetching Subprojectrevision -  "+str(error))

    return SubprojectRevision

def GetSubProjectRevisionsToFile(Project,ProjectRevision,Filepath):
    SubProjectRevisionsNotUpdated = 0

    a_file = open(Filepath, "w")
    a_file.close()
    Command = '''si viewproject -N --project={} --projectRevision={} >> {}'''.format(Project, ProjectRevision,
                                                                                     Filepath)
    #print(Command)
    AnalyseServereturnError = CommandWin.Popen(Command, shell=True, stdout=CommandWin.PIPE, stderr=CommandWin.PIPE)
    subprocess_return = AnalyseServereturnError.stderr.read().decode()

    if len(str(subprocess_return).strip()) > 1:
        MessagesLog("Project Analysis Ignored - " + "Server/Project Directory Error : \n" + str(subprocess_return))
        SubProjectRevisionsNotUpdated = 1;

    return SubProjectRevisionsNotUpdated


def GetSubProjectRevisionsLevelN(ProjCatFoldrStruct,ProjectRevision):

    Project = ProjCatFoldrStruct[0]

    for i in range(1,len(ProjCatFoldrStruct)-1):

        Project = Project.replace("project.pj", ProjCatFoldrStruct[i] + "/project.pj")
        #print("GetSubProjectRevisionsLevelN",Project, ProjectRevision, ProjCatFoldrStruct[i+1])
        SubprojectRevision = GetSubprojectRevision(Project, ProjectRevision, ProjCatFoldrStruct[i+1])
        ProjectRevision = SubprojectRevision
        #print("ProjectRevision = SubprojectRevision",ProjectRevision)

    return SubprojectRevision

def GetDevpathsinProject(Projectt):
    Command = "si projectinfo --project={} --noacl --noattributes --noshowCheckpointDescription --noassociatedIssues".format(
        Projectt)

    DevpathsList=[]

    try:
        response = CommandWin.Popen(Command, stdout=CommandWin.PIPE, stderr=CommandWin.PIPE)
        stdout, stderr = response.communicate(timeout=15)
        DevpathsList = stdout.splitlines()
        DevpathsList = [x.decode().strip() for x in DevpathsList]

        target_index = DevpathsList.index('Development Paths:')
        DevpathsList = DevpathsList[target_index + 1:]
        DevpathsList.insert(0,":mainline")

    except Exception as error:
        MessagesLog("Error Fetching Devpaths -  " + str(error))

    return DevpathsList

def GetProjectRevisionsLabelsinProject(Projectt, Devpath):
    if Devpath == "NA":
        Command = "si viewprojecthistory --project={} --fields=revision,labels".format(Projectt)
    else:
        Command = "si viewprojecthistory --project={} --fields=revision,labels --rfilter=devpath:{}".format(
            Projectt, Devpath)


    ProjectRevisionsList=[]
    ProjectRevisionsFinalList = []
    try:
        response = CommandWin.Popen(Command, stdout=CommandWin.PIPE, stderr=CommandWin.PIPE)
        stdout, stderr = response.communicate(timeout=15)
        ProjectRevisionsLabelList = stdout.splitlines()
        ProjectRevisionsLabelList = ProjectRevisionsLabelList[1:]
        #print(ProjectRevisionsLabelList)
        for x in ProjectRevisionsLabelList:
            x = x.decode().strip()
            if "\t" in x:
                x = x.replace("\t", "(") + ")"
            if (x != ""):
                ProjectRevisionsFinalList.append(x)
        #print(ProjectRevisionsLabelList)
    except Exception as error:
        MessagesLog("Error Fetching ProjectRevisionsLabel -  " + str(error))
    return ProjectRevisionsFinalList

def RemoveListItemsWithKeywords(Listt, KeywordList):

    FilteredList=[]

    FilteredList= [x for x in Listt if any(word in x for word in KeywordList)]

    return FilteredList

def GetPojectDirLevelN(ProjectDir):

    ProjectString = '/'.join(ProjectDir[1:])
    ProjectString = ProjectDir[0].replace("project.pj", ProjectString + "/project.pj")

    return ProjectString

def GetProjectRevisionsRangeinProject(Projectt,LowerRevision,HigherRevision):
    Command = "si viewprojecthistory --project={} --fields=revision --rFilter=branchrange:{}-{}".format(
        Projectt, LowerRevision, HigherRevision)

    ProjectRevisionsRangeList = []
    ProjectRevisionsRangeFinalList = []

    try:
        response = CommandWin.Popen(Command, stdout=CommandWin.PIPE, stderr=CommandWin.PIPE)
        stdout, stderr = response.communicate(timeout=15)
        ProjectRevisionsRangeList = stdout.splitlines()
        ProjectRevisionsRangeList = ProjectRevisionsRangeList[1:]

        for x in ProjectRevisionsRangeList:
            x = x.decode().strip()
            if (x != ""):
                ProjectRevisionsRangeFinalList.append(x)

    except Exception as error:
        MessagesLog("Error Fetching ProjectRevisions In Range -  " + str(error))
    return ProjectRevisionsRangeFinalList


def DownloadProjects_DirStructure(Projectpath):
        #global ProjectClassification

        if "/BRK/Customer/" in Projectpath :
            FilName = str(Projectpath.split("/")[-4]) + "_" + str(Projectpath.split("/")[-3])+ "_" + str(Projectpath.split("/")[-2])+".txt"
            TempfileTobeSavedas = r"C:\Users\Z0083520\OneDrive - ZF Friedrichshafen AG\Desktop\PTC_Integrity_Scan\Downloads\{}".format(FilName)

            f = open(TempfileTobeSavedas, "w")
            f.write("ProjectAssessed="+str(Projectpath)+"\n")
            f.close()

            path = str(Projectpath).replace("/BRK/Customer/","#/BRK#Customer/").replace("/project.pj","/08_Software/project.pj")
            Command = '''si viewproject --project={} -N --filter=attribute:label=project.pj >> "{}"'''.format(path,TempfileTobeSavedas)
            #print(Command)

        elif "/EPB/CustomerDevelopment" in  Projectpath:
            FilName = str(Projectpath.split("/")[-3]) + "_" + str(Projectpath.split("/")[-2])+".txt"
            TempfileTobeSavedas = r"C:\Users\Z0083520\OneDrive - ZF Friedrichshafen AG\Desktop\PTC_Integrity_Scan\Downloads\{}".format(FilName)

            f = open(TempfileTobeSavedas, "w")
            f.write("ProjectAssessed="+str(Projectpath)+"\n")
            f.close()


            path = str(Projectpath).replace("/EPB/CustomerDevelopment", "#/EPB#CustomerDevelopment").replace("/project.pj","/08_Software/project.pj")
            Command = '''si viewproject --project={} -N --filter=attribute:label=project.pj >> "{}"'''.format(path,
                                                                                                              TempfileTobeSavedas)

        try:
            ServerResp = os.system(Command)
        except Exception as exception:
            MessagesLog(exception)
        #print(Status)
        if ServerResp == 0 : pass
        else:

            if "/BRK/Customer/" in Projectpath:
                FilName = str(Projectpath.split("/")[-4]) + "_" + str(Projectpath.split("/")[-3]) + "_" + str(
                    Projectpath.split("/")[-2]) + ".txt"
                TempfileTobeSavedas = r"C:\Users\Z0083520\OneDrive - ZF Friedrichshafen AG\Desktop\PTC_Integrity_Scan\Downloads\{}".format(
                    FilName)

                f = open(TempfileTobeSavedas, "w")
                f.write("ProjectAssessed=" + str(Projectpath) + "\n")
                f.close()

                path = str(Projectpath).replace("/BRK/Customer/", "#/BRK#Customer/")
                Command = '''si viewproject --project={} -N --filter=attribute:label=project.pj >> "{}"'''.format(path,
                                                                                                                  TempfileTobeSavedas)
                #print(Command)

            elif "/EPB/CustomerDevelopment" in Projectpath:
                FilName = str(Projectpath.split("/")[-3]) + "_" + str(Projectpath.split("/")[-2]) + ".txt"
                TempfileTobeSavedas = r"C:\Users\Z0083520\OneDrive - ZF Friedrichshafen AG\Desktop\PTC_Integrity_Scan\Downloads\{}".format(
                    FilName)

                f = open(TempfileTobeSavedas, "w")
                f.write("ProjectAssessed=" + str(Projectpath)+"\n")
                f.close()

                path = str(Projectpath).replace("/EPB/CustomerDevelopment", "#/EPB#CustomerDevelopment")
                Command = '''si viewproject --project={} -N --filter=attribute:label=project.pj >> "{}"'''.format(path,
                                                                                                                  TempfileTobeSavedas)

            try:
                AnalyseServereturnError = CommandWin.Popen(Command, shell=True, stdout=CommandWin.PIPE,
                                                           stderr=CommandWin.PIPE)
                subprocess_return = AnalyseServereturnError.stderr.read().decode()
                if len(str(subprocess_return).strip()) > 1:
                    MessagesLog("Server Project Ignored : "+str(Projectpath)+"\n"+str(subprocess_return))

                ServerResp = os.system(Command)
            except Exception as exception:
                MessagesLog(exception)
            #print(ServerResp)



def Projects_Categorisation():
    global ProjectClassification,Projects_Categorised_DB
    ListofFiles = os.listdir(r'C:\Users\Z0083520\OneDrive - ZF Friedrichshafen AG\Desktop\PTC_Integrity_Scan\Downloads')
    for file in ListofFiles:
        try:

            FilePath = str("C:\\Users\\Z0083520\\OneDrive - ZF Friedrichshafen AG\\Desktop\\PTC_Integrity_Scan\\Downloads")
            FilePath += "\\"+file
            #print(FilePath)
            projanalyzed = []
            data = {}
            with open(FilePath,"r") as file_in:

                for line in file_in:
                    projanalyzed.append(line.replace("\n",""))

            #print(lines)
            if len(projanalyzed)<=1:
                #print("Not analyzed" + str(projanalyzed))
                if "ProjectAssessed" in projanalyzed[0]:
                    # print("Not analyzed" + str(projanalyzed))
                    pass
                else:
                    continue

            else :
                data = {"ProjectPath": str(projanalyzed[0]).replace("ProjectAssessed=", ""),
                        "ProjectCategory": "CAT5_EPB4_and_Uncategorised"}
                projStructure = ""
                for projStructurefolder in projanalyzed:
                    projStructure +=(str(projStructurefolder)+"***")

                if ("PBC_APPL" in projStructure) and ("SSM_PB_APPL" in projStructure):
                        #data = {"ProjectPath" : str(projanalyzed[0]).replace("ProjectAssessed=","") , "ProjectCategory" : "Full_EPBi"}
                        data["ProjectCategory"] = "CAT1_Full_EPBi"

                elif ("PBC_APPL" in projStructure) and ("SSM_PB_APPL" not in projStructure) and ("MMC_APPL" not in projStructure):
                        #data = {"ProjectPath" : str(projanalyzed[0]).replace("ProjectAssessed=","") , "ProjectCategory" : "PBC_APPL"}
                        data["ProjectCategory"] = "CAT2_PBC_APPL"

                elif ("SSM_PB_APPL" in projStructure) and ("PBC_APPL" not in projStructure)and ("MMC_APPL" not in projStructure):
                        #data = {"ProjectPath" : str(projanalyzed[0]).replace("ProjectAssessed=","") , "ProjectCategory" : "SSM_PB_APPL"}
                        data["ProjectCategory"] = "CAT3_SSM_PB_APPL"

                elif ("MMC_APPL" in projStructure) and ("PBC_APPL" not in projStructure)and ("SSM_PB_APPL" not in projStructure):
                        #data = {"ProjectPath" : str(projanalyzed[0]).replace("ProjectAssessed=","") , "ProjectCategory" : "MMC_APPL"}
                        data["ProjectCategory"] = "CAT4_MMC_APPL"

                elif ("APPL_Redundant" in projStructure) and ("PBC_APPL" not in projStructure)and ("SSM_PB_APPL" not in projStructure):
                        #data = {"ProjectPath" : str(projanalyzed[0]).replace("ProjectAssessed=","") , "ProjectCategory" : "MMC_APPL"}
                        data["ProjectCategory"] = "CAT4_MMC_APPL"

            if len(projanalyzed)>1:
                #print(data)
                if data["ProjectPath"] not in [projpath["ProjectPath"] for projpath in ProjectClassification ]:
                    ProjectClassification.append(data)



        except Exception as exception:
            print(exception)
            return
    pickle.dump(ProjectClassification, open("DataBase.p", "wb"))
    Projects_Categorised_DB = pickle.load(open("DataBase.p", "rb"))




#Project Tree Development
ct = CheckboxTreeview(FrameLeft_Notebook_frame_02, show='tree')
ct.pack(fill=BOTH, side="left", expand=1)
ct.insert('', 'end', "PBC", text="EPBi PBC System (PBC and SSM PB Application)")
ct.insert('', 'end', "PBC_Only", text="PBC Application Only")
ct.insert('', 'end', "SSM_Only", text="SSM_PB Application Only")
ct.insert('', 'end', "EPB5", text="EPB5 (MMC Application)")
ct.insert('', 'end', "EPB4_O", text="EPB4 and Uncategorised")
ct.insert('', 'end', "CAT6_EPB_Redundant", text="EPB Redundant")
#ct.insert('', 'end', "SSM_PB", text="SSM_PBC Projects")
# ----Vertical scrollbar----------
vbar = tkinter.Scrollbar(FrameLeft_Notebook_frame_02, orient=VERTICAL, command=ct.yview,relief="flat")
vbar.pack(side = "right" , fill=Y)
# ----horizontal scrollbar----------
hbar = tkinter.Scrollbar(FrameLeft_Notebook_frame_01T, orient=HORIZONTAL, command=ct.xview,relief="flat")
hbar.pack(side = "bottom", fill=X)

ct.configure(xscrollcommand=hbar.set,yscrollcommand=vbar.set)


def UpdateProjects():
    global ct
    ct.delete(*ct.get_children())
    ct.insert('', 'end', "CAT1_Full_EPBi", text="EPBi PBC System (PBC and SSM PB Application)")
    ct.insert('', 'end', "CAT2_PBC_APPL", text="PBC Application Only")
    ct.insert('', 'end', "CAT3_SSM_PB_APPL", text="SSM_PB Application Only")
    ct.insert('', 'end', "CAT4_MMC_APPL", text="EPB5 (MMC Application)")
    ct.insert('', 'end', "CAT5_EPB4_and_Uncategorised", text="EPB4 and Uncategorised")
    ct.insert('', 'end', "CAT6_EPB_Redundant", text="EPB Redundant")
    FrameLeft_Notebook_frame_02.update()

    for proj in Projects_Categorised_DB:
        if str(proj["ProjectCategory"]) == "CAT1_Full_EPBi":
            ct.insert("CAT1_Full_EPBi", 'end',str(proj["ProjectPath"]), text=str(proj["ProjectPath"]))
        if str(proj["ProjectCategory"]) == "CAT2_PBC_APPL":
            ct.insert("CAT2_PBC_APPL", 'end',str(proj["ProjectPath"]), text=str(proj["ProjectPath"]))
        if str(proj["ProjectCategory"]) == "CAT3_SSM_PB_APPL":
            ct.insert("CAT3_SSM_PB_APPL", 'end',str(proj["ProjectPath"]), text=str(proj["ProjectPath"]))
        if str(proj["ProjectCategory"]) == "CAT4_MMC_APPL":
            ct.insert("CAT4_MMC_APPL", 'end',str(proj["ProjectPath"]), text=str(proj["ProjectPath"]))
        if str(proj["ProjectCategory"]) == "CAT5_EPB4_and_Uncategorised":
            ct.insert("CAT5_EPB4_and_Uncategorised", 'end',str(proj["ProjectPath"]), text=str(proj["ProjectPath"]))
        if str(proj["ProjectCategory"]) == "CAT6_EPB_Redundant":
            ct.insert("CAT6_EPB_Redundant", 'end',str(proj["ProjectPath"]), text=str(proj["ProjectPath"]))




def UpdateVisualTable(filtereddata):
    global DataFrame
    #Notebook_frame2.destroy()
    DataFrame.destroy()
    DataFrame = LabelFrame(Notebook_frame2, text="", bg="white",
                             fg="black")
    DataFrame.pack(fill=BOTH, expand=1)

    frame = tkinter.Frame(DataFrame)
    frame.pack(fill=BOTH, expand=1)
    df = pd.DataFrame(filtereddata)
    PandasTable = Table(frame, dataframe=df, showtoolbar=False, showstatusbar=True)
    PandasTable.show()




DataFrame = tkinter.Frame(Notebook_frame2)
DataFrame.pack(fill=BOTH, expand=1)
df = pd.DataFrame(index=['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], \
                      columns=['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
PandasTable = Table(DataFrame, dataframe=df, showtoolbar=False, showstatusbar=True)
PandasTable.show()


try:
    Projects_Categorised_DB = pickle.load(open("DataBase.p", "rb"))
    #print(Projects_Categorised_DB)

    #print(str(ProjectClassification_Db))
except Exception as exception :
    ErrorPrompt("File Missing" , "DataBase.p is missing/corrupted at current directory."+"\n"+str(exception))
EPBProjDetailsParse()

#print(FuncAnlsDB_ProjCatFoldrStruct[ProjectCategoriesDropDown_3.get()]["XML_FILEPTH"][0])
GUITopFrame.mainloop()

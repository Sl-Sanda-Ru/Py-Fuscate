
from pystyle import Colors, Colorate
import ctypes
import random
import string
import pymem
import time
import re
import os
import psutil

p = psutil.Process(os.getpid())
p.nice(psutil.HIGH_PRIORITY_CLASS)
import requests
def CloseRBLX():
    roblox_processes = ChaoSpolit.YieldForProgram("RobloxPlayerBeta.exe")
    if roblox_processes:
        os.system("taskkill /im RobloxPlayerBeta.exe")

    if not roblox_processes:
        print("/\RobloxPlayerBeta.exe was not found")
        exit()

os.system("cls" if os.name == "nt" else "clear")

# This is a flag that the thread will check to see if it should stop
stop_thread = False

def undetectname():# silly bypass
    global stop_thread
    while not stop_thread:
        letters = string.ascii_lowercase
        appname = ''.join(random.choice(letters) for _ in range(20))
        ctypes.windll.kernel32.SetConsoleTitleW(appname)
        time.sleep(1)


def init():
    """# docs by tabnine
    This function is used to check for updates and display them to the user.
    """
    url = "https://capi-3ns5.onrender.com/latestversion"# i am dumb
    req = requests.get(url=url)
    #convert the output : [1] into only the number in it
    res = req.text[1:-1]
    # print(res)# debug [purposes]
    if res == "1":
        print(Colorate.Horizontal(Colors.purple_to_red, f"Latest Version : {res}..."))
        print(Colorate.Horizontal(Colors.purple_to_red, "Discord: https://discord.gg/chaosploit...", 1))
        pass
    else:
        print(Colorate.Horizontal(Colors.purple_to_red, "Update Soon Please Join: https://discord.gg/chaosploit...", 1))
        exit()
        

init()        
        
        
print(Colorate.Horizontal(Colors.purple_to_red, "Init...", 1))

class ChaoSpolit:
    def __init__(self, program_name):
        self.program_name = program_name

    def SimpleGetProcesses(self):
        return [proc.name() for proc in psutil.process_iter(["name"])]
    
    def SetParent(self, Instance, Parent, parentOffset):
        ChaoSpolit.Pymem.write_longlong(Instance + parentOffset, Parent)

    def __init__(self, ProgramName=None):# init
        self.ProgramName = ProgramName
        self.Pymem = pymem.Pymem()
        self.Addresses = {}
        self.Handle = None
        self.is64bit = True
        self.ProcessID = None
        self.PID = self.ProcessID
        if type(ProgramName) == str:
            self.Pymem = pymem.Pymem(ProgramName)
            self.Handle = self.Pymem.process_handle
            self.is64bit = pymem.process.is_64_bit(self.Handle)
            self.ProcessID = self.Pymem.process_id
            self.PID = self.ProcessID
        elif type(ProgramName) == int:
            self.Pymem.open_process_from_id(ProgramName)
            self.Handle = self.Pymem.process_handle
            self.is64bit = pymem.process.is_64_bit(self.Handle)
            self.ProcessID = self.Pymem.process_id
            self.PID = self.ProcessID

    def h2d(self, hz: str, bit: int = 16) -> int:
        if type(hz) == int:
            return hz
        return int(hz, bit)

    def d2h(self, dc: int, UseAuto=None) -> str:
        if type(dc) == str:
            return dc
        if UseAuto:
            if UseAuto == 32:
                dc = hex(dc & (2**32 - 1)).replace("0x", "")
            else:
                dc = hex(dc & (2**64 - 1)).replace("0x", "")
        else:
            if abs(dc) > 4294967295:
                dc = hex(dc & (2**64 - 1)).replace("0x", "")
            else:
                dc = hex(dc & (2**32 - 1)).replace("0x", "")
        if len(dc) > 8:
            while len(dc) < 16:
                dc = "0" + dc
        if len(dc) < 8:
            while len(dc) < 8:
                dc = "0" + dc
        return dc

    def PLAT(self, aob: str):
        if type(aob) == bytes:
            return aob
        trueB = bytearray(b"")
        aob = aob.replace(" ", "")
        PLATlist = []
        for i in range(0, len(aob), 2):
            PLATlist.append(aob[i : i + 2])
        for i in PLATlist:
            if "?" in i:
                trueB.extend(b".")
            if "?" not in i:
                trueB.extend(re.escape(bytes.fromhex(i)))
        return bytes(trueB)

    def AOBSCANALL(self, AOB_HexArray, xreturn_multiple=False):
        """
        Searches for a given AOB (Address-Of-Buffer) pattern in the currently opened process.

        Parameters:
        AOB_HexArray (str): The AOB pattern to search for, represented as a hex string.
        xreturn_multiple (bool): Whether to return all matches or only the first match.

        Returns:
        A list of addresses where the AOB pattern was found, or None if the pattern was not found.
        """
        try:
            # Open the process with the appropriate access rights
            ChaoSpolit.Pymem.process_handle = ctypes.windll.kernel32.OpenProcess(
                0x1F0FFF,  # PROCESS_ALL_ACCESS
                False,  # False = do not inherit handles
                ChaoSpolit.Pymem.process_id,
            )

            # Define necessary ChaoSpolit functions
            PAGE_EXECUTE_READWRITE = 0x40
            ntdll = ctypes.windll.ntdll
            NtProtectVirtualMemory = ntdll.NtProtectVirtualMemory
            NtProtectVirtualMemory.restype = ctypes.c_long

            # Get the base address of the process
            base_address = ctypes.windll.kernel32.GetModuleHandleW(None)

            # Remove read/write protection from the process memory
            old_protect = ctypes.c_ulong()
            size = ctypes.c_size_t(0x1000)
            NtProtectVirtualMemory(
                ChaoSpolit.Pymem.process_handle,
                ctypes.byref(ctypes.c_void_p(base_address)),
                ctypes.byref(size),
                PAGE_EXECUTE_READWRITE,
                ctypes.byref(old_protect),
            )

            # Get the base address of the process again (after removing read/write protection)
            base_address = ctypes.windll.kernel32.GetModuleHandleW(None)

            # Re-enable read/write protection for the process memory
            NtProtectVirtualMemory(
                ChaoSpolit.Pymem.process_handle,
                ctypes.byref(ctypes.c_void_p(base_address)),
                ctypes.byref(size),
                old_protect,
                ctypes.byref(ctypes.c_ulong()),
            )

            # Now attempt the pattern scan
            return pymem.pattern.pattern_scan_all(
                self.Pymem.process_handle,
                self.PLAT(AOB_HexArray),
                return_multiple=xreturn_multiple,
            )
        except Exception as e:
            print(f"WinAPI Error: {e}")
            # Let's try bypassing read/write protection first.
            try:
                ChaoSpolit.Pymem.process_handle = ctypes.windll.kernel32.OpenProcess(
                    0x1F0FFF,  # PROCESS_ALL_ACCESS
                    False,  # False = do not inherit handles
                    ChaoSpolit.Pymem.process_id,
                )

                # Define necessary ChaoSpolit functions
                PAGE_EXECUTE_READWRITE = 0x40
                ntdll = ctypes.windll.ntdll
                NtProtectVirtualMemory = ntdll.NtProtectVirtualMemory
                NtProtectVirtualMemory.restype = ctypes.c_long

                # Get the base address of the process
                base_address = ctypes.windll.kernel32.GetModuleHandleW(None)

                # Remove read/write protection from the process memory
                old_protect = ctypes.c_ulong()
                size = ctypes.c_size_t(0x1000)
                NtProtectVirtualMemory(
                    ChaoSpolit.Pymem.process_handle,
                    ctypes.byref(ctypes.c_void_p(base_address)),
                    ctypes.byref(size),
                    PAGE_EXECUTE_READWRITE,
                    ctypes.byref(old_protect),
                )

                # Get the base address of the process again (after removing read/write protection)
                base_address = ctypes.windll.kernel32.GetModuleHandleW(None)

                # Re-enable read/write protection for the process memory
                NtProtectVirtualMemory(
                    ChaoSpolit.Pymem.process_handle,
                    ctypes.byref(ctypes.c_void_p(base_address)),
                    ctypes.byref(size),
                    old_protect,
                    ctypes.byref(ctypes.c_ulong()),
                )

                # Now attempt the pattern scan
                return pymem.pattern.pattern_scan_all(
                    self.Pymem.process_handle,
                    self.PLAT(AOB_HexArray),
                    return_multiple=xreturn_multiple,
                )
            except WindowsError as we:
                if we.winerror == 5:
                    ChaoSpolit.Pymem.process_handle = ctypes.windll.kernel32.OpenProcess(
                        0x1F0FFF,  # PROCESS_ALL_ACCESS
                        False,  # False = do not inherit handles
                        ChaoSpolit.Pymem.process_id,
                    )

                # Define necessary ChaoSpolit functions
                PAGE_EXECUTE_READWRITE = 0x40
                ntdll = ctypes.windll.ntdll
                NtProtectVirtualMemory = ntdll.NtProtectVirtualMemory
                NtProtectVirtualMemory.restype = ctypes.c_long

                # Get the base address of the process
                base_address = ctypes.windll.kernel32.GetModuleHandleW(None)

                # Remove read/write protection from the process memory
                old_protect = ctypes.c_ulong()
                size = ctypes.c_size_t(0x1000)
                NtProtectVirtualMemory(
                    ChaoSpolit.Pymem.process_handle,
                    ctypes.byref(ctypes.c_void_p(base_address)),
                    ctypes.byref(size),
                    PAGE_EXECUTE_READWRITE,
                    ctypes.byref(old_protect),
                )

                # Get the base address of the process again (after removing read/write protection)
                base_address = ctypes.windll.kernel32.GetModuleHandleW(None)

                # Re-enable read/write protection for the process memory
                NtProtectVirtualMemory(
                    ChaoSpolit.Pymem.process_handle,
                    ctypes.byref(ctypes.c_void_p(base_address)),
                    ctypes.byref(size),
                    old_protect,
                    ctypes.byref(ctypes.c_ulong()),
                )

                # Now attempt the pattern scan
                return pymem.pattern.pattern_scan_all(
                    self.Pymem.process_handle,
                    self.PLAT(AOB_HexArray),
                    return_multiple=xreturn_multiple,
                )
            except Exception as e:
                print(f"Unknown error: ")
    def gethexc(self, hex: str):
        hex = hex.replace(" ", "")
        hxlist = []
        for i in range(0, len(hex), 2):
            hxlist.append(hex[i : i + 2])
        return len(hxlist)

    def hex2le(self, hex: str):
        lehex = hex.replace(" ", "")
        lelist = []
        if len(lehex) > 8:
            while len(lehex) < 16:
                lehex = "0" + lehex
            for i in range(0, len(lehex), 2):
                lelist.append(lehex[i : i + 2])
            lelist.reverse()
            return "".join(lelist)
        if len(lehex) < 9:
            while len(lehex) < 8:
                lehex = "0" + lehex
            for i in range(0, len(lehex), 2):
                lelist.append(lehex[i : i + 2])
            lelist.reverse()
            return "".join(lelist)

    def calcjmpop(self, des, cur):
        jmpopc = (self.h2d(des) - self.h2d(cur)) - 5
        jmpopc = hex(jmpopc & (2**32 - 1)).replace("0x", "")
        if len(jmpopc) % 2 != 0:
            jmpopc = "0" + str(jmpopc)
        return jmpopc

    def isProgramGameActive(self):
        try:
            self.Pymem.read_char(self.Pymem.base_address)
            return True
        except:
            return False

    def DRP(self, Address: int, is64Bit: bool = None) -> int:
        Address = Address
        if type(Address) == str:
            Address = self.h2d(Address)
        if is64Bit:
            return int.from_bytes(self.Pymem.read_bytes(Address, 8), "little")
        if self.is64bit:
            return int.from_bytes(self.Pymem.read_bytes(Address, 8), "little")
        return int.from_bytes(self.Pymem.read_bytes(Address, 4), "little")

    def isValidPointer(self, Address: int, is64Bit: bool = None) -> bool:
        try:
            if type(Address) == str:
                Address = self.h2d(Address)
            self.Pymem.read_bytes(self.DRP(Address, is64Bit), 1)
            return True
        except:
            return False

    def GetModules(self) -> list:
        return list(self.Pymem.list_modules())

    def getAddressFromName(self, Address: str) -> int:
        if type(Address) == int:
            return Address
        AddressBase = 0
        AddressOffset = 0
        for i in self.GetModules():
            if i.name in Address:
                AddressBase = i.lpBaseOfDll
                AddressOffset = self.h2d(Address.replace(i.name + "+", ""))
                AddressNamed = AddressBase + AddressOffset
                return AddressNamed
            print("\033[91mAdress failed: \033[0m" + Address + " Line Rsp1")
            exit() 

        return Address

    def getNameFromAddress(self, Address: int) -> str:
        memoryInfo = pymem.memory.virtual_query(self.Pymem.process_handle, Address)
        BaseAddress = memoryInfo.BaseAddress
        NameOfDLL = ""
        AddressOffset = 0
        for i in self.GetModules():
            if i.lpBaseOfDll == BaseAddress:
                NameOfDLL = i.name
                AddressOffset = Address - BaseAddress
                break
        if NameOfDLL == "":
            return Address
        NameOfAddress = NameOfDLL + "+" + self.d2h(AddressOffset)
        return NameOfAddress

    def getRawProcesses(self):
        toreturn = []
        for i in pymem.process.list_processes():
            toreturn.append(
                [
                    i.cntThreads,
                    i.cntUsage,
                    i.dwFlags,
                    i.dwSize,
                    i.pcPriClassBase,
                    i.szExeFile,
                    i.th32DefaultHeapID,
                    i.th32ModuleID,
                    i.th32ParentProcessID,
                    i.th32ProcessID,
                ]
            )
        return toreturn

    def SimpleGetProcesses(self):
        toreturn = []
        for i in self.getRawProcesses():
            toreturn.append({"Name": i[5].decode(), "Threads": i[0], "ProcessId": i[9]})
        return toreturn

    def YieldForProgram(self, programName, AutoOpen: bool = False, Limit=1):
        Count = 0
        while True:
            if Count >= Limit:
                return False
            ProcessesList = self.SimpleGetProcesses()
            for i in ProcessesList:
                if i["Name"] == programName:

                    if AutoOpen:
                        self.Pymem.open_process_from_id(i["ProcessId"])
                        self.ProgramName = programName
                        self.Handle = self.Pymem.process_handle
                        self.is64bit = pymem.process.is_64_bit(self.Handle)
                        self.ProcessID = self.Pymem.process_id
                        self.PID = self.ProcessID
                    return True
            time.sleep(1)
            Count += 1

    def ReadPointer(
        self, BaseAddress: int, Offsets_L2R: list, is64Bit: bool = None
    ) -> int:
        x = self.DRP(BaseAddress, is64Bit)
        y = Offsets_L2R
        z = x
        if y == None or len(y) == 0:
            return z
        count = 0
        for i in y:
            try:
                print(self.d2h(x + i))
                print(self.d2h(i))
                z = self.DRP(z + i, is64Bit)
                count += 1
                print(self.d2h(z))
            except:
                print("\033[91mNo index offset: \033[0m" + str(count) + " Rsp2")
                exit()  
        
            return z
        return z


    def GetMemoryInfo(self, Address: int, Handle: int = None):
        if Handle:
            return pymem.memory.virtual_query(Handle, Address)
        else:
            return pymem.memory.virtual_query(self.Handle, Address)

    def MemoryInfoToDictionary(self, MemoryInfo):
        return {
            "BaseAddress": MemoryInfo.BaseAddress,
            "AllocationBase": MemoryInfo.AllocationBase,
            "AllocationProtect": MemoryInfo.AllocationProtect,
            "RegionSize": MemoryInfo.RegionSize,
            "State": MemoryInfo.State,
            "Protect": MemoryInfo.Protect,
            "Type": MemoryInfo.Type,
        }

    def SetProtection(
        self,
        Address: int,
        ProtectionType=0x40,
        Size: int = 4,
        OldProtect=ctypes.c_ulong(0),
    ):
        pymem.ressources.kernel32.VirtualProtectEx(
            self.Pymem.process_handle,
            Address,
            Size,
            ProtectionType,
            ctypes.byref(OldProtect),
        )
        return OldProtect

    def ChangeProtection(
        self,
        Address: int,
        ProtectionType=0x40,
        Size: int = 4,
        OldProtect=ctypes.c_ulong(0),
    ):
        return self.SetProtection(Address, ProtectionType, Size, OldProtect)

    def GetProtection(self, Address: int):
        return self.GetMemoryInfo(Address).Protect

    def KnowProtection(self, Protection):
        if Protection == 0x10:
            return "PAGE_EXECUTE"
        if Protection == 0x20:
            return "PAGE_EXECUTE_READ"
        if Protection == 0x40:
            return "PAGE_EXECUTE_READWRITE"
        if Protection == 0x80:
            return "PAGE_EXECUTE_WRITECOPY"
        if Protection == 0x01:
            return "PAGE_NOACCESS"
        if Protection == 0x02:
            return "PAGE_READONLY"
        if Protection == 0x04:
            return "PAGE_READWRITE"
        if Protection == 0x08:
            return "PAGE_WRITECOPY"
        if Protection == 0x100:
            return "PAGE_GUARD"
        if Protection == 0x200:
            return "PAGE_NOCACHE"
        if Protection == 0x400:
            return "PAGE_WRITECOMBINE"
        if Protection in ["PAGE_EXECUTE", "execute", "e"]:
            return 0x10
        if Protection in [
            "PAGE_EXECUTE_READ",
            "execute read",
            "read execute",
            "execute_read",
            "read_execute",
            "er",
            "re",
        ]:
            return 0x20
        if Protection in [
            "PAGE_EXECUTE_READWRITE",
            "execute read write",
            "execute write read",
            "write execute read",
            "write read execute",
            "read write execute",
            "read execute write",
            "erw",
            "ewr",
            "wre",
            "wer",
            "rew",
            "rwe",
        ]:
            return 0x40
        if Protection in [
            "PAGE_EXECUTE_WRITECOPY",
            "execute copy write",
            "execute write copy",
            "write execute copy",
            "write copy execute",
            "copy write execute",
            "copy execute write",
            "ecw",
            "ewc",
            "wce",
            "wec",
            "cew",
            "cwe",
        ]:
            return 0x80
        if Protection in ["PAGE_NOACCESS", "noaccess", "na", "n"]:
            return 0x01
        if Protection in ["PAGE_READONLY", "readonly", "ro", "r"]:
            return 0x02
        if Protection in ["PAGE_READWRITE", "read write", "write read", "wr", "rw"]:
            return 0x04
        if Protection in ["PAGE_WRITECOPY", "write copy", "copy write", "wc", "cw"]:
            return 0x08
        if Protection in ["PAGE_GUARD", "pg", "guard", "g"]:
            return 0x100
        if Protection in ["PAGE_NOCACHE", "nc", "nocache"]:
            return 0x200
        if Protection in ["PAGE_WRITECOMBINE", "write combine", "combine write"]:
            return 0x400
        return Protection

    def Suspend(self, pid: int = None):
        kernel32 = ctypes.WinDLL("kernel32.dll")
        if pid:
            kernel32.DebugActiveProcess(pid)
        if self.PID:
            kernel32.DebugActiveProcess(self.PID)

    def Resume(self, pid: int = None):
        kernel32 = ctypes.WinDLL("kernel32.dll")
        if pid:
            kernel32.DebugActiveProcessStop(pid)
        if self.PID:
            kernel32.DebugActiveProcessStop(self.PID)

ChaoSpolit = ChaoSpolit()



print(Colorate.Horizontal(Colors.purple_to_red, "Loaded", 1))
print(Colorate.Horizontal(Colors.purple_to_red, "Waiting for RobloxPlayerBeta.exe", 1))
while True:
    if ChaoSpolit.YieldForProgram("RobloxPlayerBeta.exe", True, 15):
        break
print(Colorate.Horizontal(Colors.purple_to_red, "Found Process", 1))      


                

def ReadRobloxString(ExpectedAddress: int) -> str:
        try:
            StringCount = ChaoSpolit.Pymem.read_int(ExpectedAddress + 0x10)
            if StringCount > 15:
                return ChaoSpolit.Pymem.read_string(ChaoSpolit.DRP(ExpectedAddress), StringCount)
            return ChaoSpolit.Pymem.read_string(ExpectedAddress, StringCount)
        except TypeError as e:
            print(f"TypeError: {e} \n" + "Rsp3")
            exit()

def GetClassName(Instance: int) -> str:
    ExpectedAddress = ChaoSpolit.DRP(ChaoSpolit.DRP(Instance + 0x18) + 8)
    return ReadRobloxString(ExpectedAddress)

def setParent(Instance, Parent, parentOffset, childrenOffset):
    ChaoSpolit.Pymem.process_handle = ctypes.windll.kernel32.OpenProcess(
                    0x1F0FFF,  # PROCESS_ALL_ACCESS
                    False,  # False = do not inherit handles
                    ChaoSpolit.Pymem.process_id,
                )

                # Define necessary ChaoSpolit functions
    PAGE_EXECUTE_READWRITE = 0x40
    ntdll = ctypes.windll.ntdll
    NtProtectVirtualMemory = ntdll.NtProtectVirtualMemory
    NtProtectVirtualMemory.restype = ctypes.c_long

                # Get the base address of the process
    base_address = ctypes.windll.kernel32.GetModuleHandleW(None)

                # Remove read/write protection from the process memory
    old_protect = ctypes.c_ulong()
    size = ctypes.c_size_t(0x1000)
    NtProtectVirtualMemory(
        ChaoSpolit.Pymem.process_handle,
        ctypes.byref(ctypes.c_void_p(base_address)),
        ctypes.byref(size),
        PAGE_EXECUTE_READWRITE,
        ctypes.byref(old_protect),
    )

                # Get the base address of the process again (after removing read/write protection)
    base_address = ctypes.windll.kernel32.GetModuleHandleW(None)

                # Re-enable read/write protection for the process memory
    NtProtectVirtualMemory(
                    ChaoSpolit.Pymem.process_handle,
                    ctypes.byref(ctypes.c_void_p(base_address)),
                    ctypes.byref(size),
                    old_protect,
                    ctypes.byref(ctypes.c_ulong()),
    )
    
    ChaoSpolit.Pymem.write_longlong(Instance + parentOffset, Parent)
    newChildren = ChaoSpolit.Pymem.allocate(0x400)
    ChaoSpolit.Pymem.write_longlong(newChildren + 0, newChildren + 0x40)

    ptr = ChaoSpolit.Pymem.read_longlong(Parent + childrenOffset)
    childrenStart = ChaoSpolit.Pymem.read_longlong(ptr)
    childrenEnd = ChaoSpolit.Pymem.read_longlong(ptr + 8)

    if childrenStart == 0 or childrenEnd == 0 or childrenEnd <= childrenStart:
        print("\033[91mError: Invalid children range. Line: Rsp16\033[0m")
        exit()

    length = childrenEnd - childrenStart
    if length < 0:
        print("\033[91mError: Negative length for children array. Line: Rsp17\033[0m")
        exit()

    b = ChaoSpolit.Pymem.read_bytes(childrenStart, length)
    ChaoSpolit.Pymem.write_bytes(newChildren + 0x40, b, len(b))
    e = newChildren + 0x40 + length
    ChaoSpolit.Pymem.write_longlong(e, Instance)
    ChaoSpolit.Pymem.write_longlong(e + 8, ChaoSpolit.Pymem.read_longlong(Instance + 0x10))
    e = e + 0x10
    ChaoSpolit.Pymem.write_longlong(newChildren + 0x8, e)
    ChaoSpolit.Pymem.write_longlong(newChildren + 0x10, e)

def inject():
    nameOffset = 72
    parentOffset = 96
    childrenOffset = 80 

    def GetDataModel() -> int:# lua and cipher
        guiroot_pattern = b"\\x47\\x75\\x69\\x52\\x6F\\x6F\\x74\\x00\\x47\\x75\\x69\\x49\\x74\\x65\\x6D"
        guiroot_address = ChaoSpolit.AOBSCANALL(guiroot_pattern, xreturn_multiple=False)
        if guiroot_address != 0:
            RawDataModel = ChaoSpolit.DRP(guiroot_address + 0x38)
            DataModel = RawDataModel + 0x150
            return DataModel - 0x8
        else:
            print("Critical Error please restart the program")
            exit()  
    dataModel = GetDataModel()
    print(GetClassName(dataModel)) # this will print app cuz its actual datamodel
    for i in range(0x10, 0x200 + 8, 8):
        ptr = ChaoSpolit.Pymem.read_longlong(dataModel + i)
        if ptr:
            try:
                childrenStart = ChaoSpolit.Pymem.read_longlong(ptr)
                childrenEnd = ChaoSpolit.Pymem.read_longlong(ptr + 8)
                if childrenStart and childrenEnd:
                    diff = childrenEnd - childrenStart
                    if diff > 1 and diff < 0x1000:
                        childrenOffset = i
                        break
            except:
                pass
    print(Colorate.Horizontal(Colors.purple_to_red, "Done", 1))

    def GetNameAddress(Instance: int) -> int:
        try:
        
                ExpectedAddress = ChaoSpolit.DRP(Instance + nameOffset, True)


                return ExpectedAddress
        except TypeError as e:
            print(f"TypeError: {e} \n" + "Line: Rsp8")
            exit() 

        

    def GetName(Instance: int) -> str:
        ExpectedAddress = GetNameAddress(Instance)
        return ReadRobloxString(ExpectedAddress)

    def GetChildren(Instance: int) -> str:
        ChaoSpolit.Pymem.process_handle = ctypes.windll.kernel32.OpenProcess(
                    0x1F0FFF,  # PROCESS_ALL_ACCESS
                    False,  # False = do not inherit handles
                    ChaoSpolit.Pymem.process_id,
                )

                # Define necessary ChaoSpolit functions
        PAGE_EXECUTE_READWRITE = 0x40
        ntdll = ctypes.windll.ntdll
        NtProtectVirtualMemory = ntdll.NtProtectVirtualMemory
        NtProtectVirtualMemory.restype = ctypes.c_long

                    # Get the base address of the process
        base_address = ctypes.windll.kernel32.GetModuleHandleW(None)

                    # Remove read/write protection from the process memory
        old_protect = ctypes.c_ulong()
        size = ctypes.c_size_t(0x1000)
        NtProtectVirtualMemory(
            ChaoSpolit.Pymem.process_handle,
            ctypes.byref(ctypes.c_void_p(base_address)),
            ctypes.byref(size),
            PAGE_EXECUTE_READWRITE,
            ctypes.byref(old_protect),
        )

                    # Get the base address of the process again (after removing read/write protection)
        base_address = ctypes.windll.kernel32.GetModuleHandleW(None)

                    # Re-enable read/write protection for the process memory
        NtProtectVirtualMemory(
                        ChaoSpolit.Pymem.process_handle,
                        ctypes.byref(ctypes.c_void_p(base_address)),
                        ctypes.byref(size),
                        old_protect,
                        ctypes.byref(ctypes.c_ulong()),
        )
        ChildrenInstance = []
        InstanceAddress = Instance
        if not InstanceAddress:
            return False
        ChildrenStart = ChaoSpolit.DRP(InstanceAddress + childrenOffset, True)
        if ChildrenStart == 0:
            return []
        ChildrenEnd = ChaoSpolit.DRP(ChildrenStart + 8, True)
        OffsetAddressPerChild = 0x10
        CurrentChildAddress = ChaoSpolit.DRP(ChildrenStart, True)
        try:
            for i in range(0, 9000):
                if i == 8999:
                    raise ValueError("Invalid children please rerun the program! Line: Rsp9")

                if CurrentChildAddress == ChildrenEnd:
                    break
                ChildrenInstance.append(ChaoSpolit.Pymem.read_longlong(CurrentChildAddress))
                CurrentChildAddress += OffsetAddressPerChild
            return ChildrenInstance
        except ValueError as e:
            print(f"\033[91mError: {e}\033[0m")
            exit()

    def GetParent(Instance: int) -> int:
        return ChaoSpolit.DRP(Instance + parentOffset, True)

    def FindFirstChild(Instance: int, ChildName: str) -> int:
        ChildrenOfInstance = GetChildren(Instance)
        for i in ChildrenOfInstance:
            if GetName(i) == ChildName:
                return i

    def FindFirstChildOfClass(Instance: int, ClassName: str) -> int:
        ChildrenOfInstance = GetChildren(Instance)
        for i in ChildrenOfInstance:
            if GetClassName(i) == ClassName:
                return i
            
    def GetDescendants(Instance: int) -> list:

        descendants = []

        def _get_descendants_recursive(current_instance: int):
            children = GetChildren(current_instance)
            descendants.extend(children)  # Add direct children

            # Recurse into each child
            for child in children:
                _get_descendants_recursive(child)

        _get_descendants_recursive(Instance)
        return descendants
    



    class toInstance:
        def __init__(self, address: int = 0):
            self.Address = address
            self.Self = address
            self.Name = GetName(address)
            self.ClassName = GetClassName(address)
            self.Parent = GetParent(address)

        def getChildren(self):
            return GetChildren(self.Address)

        def findFirstChild(self, ChildName):
            return FindFirstChild(self.Address, ChildName)

        def findFirstClass(self, ChildClass):
            return FindFirstChildOfClass(self.Address, ChildClass)

        def setParent(self, Parent):
            setParent(self.Address, Parent)

        def GetChildren(self):
            return GetChildren(self.Address)

        def GetDescendants(self):
            return GetDescendants(self.Address)

        def FindFirstChild(self, ChildName):
            return FindFirstChild(self.Address, ChildName)

        def FindFirstClass(self, ChildClass):
            return FindFirstChildOfClass(self.Address, ChildClass)

        def SetParent(self, Parent):
            setParent(self.Address, Parent, parentOffset, childrenOffset)

    game = toInstance(dataModel)
    players = toInstance(game.FindFirstClass("Players"))
    localPlayer = toInstance(players.GetChildren()[0])
    workspace = toInstance(game.GetChildren()[0])
    character_found = False

    for obj in workspace.GetDescendants():
        obj_name = GetName(obj)
        if obj_name == localPlayer.Name:
            character = toInstance(obj)
            print("Found Character")
            character_found = True
            break

    if not character_found:
        print("No Character")
        return None

    animateScript = character.findFirstClass("LocalScript")
    if animateScript is None:
        print("No Animate")
        return None
    print("Injecting...")
    targetScript = toInstance(animateScript)
    injectScript = None
    results = ChaoSpolit.AOBSCANALL("496E6A656374????????????????????06", True)
    if results == []:
        print("\033[35mPlease find another teleporter! Line: Rsp11\033[0m")
        return None
    for rn in results:
        result = rn
        bres = ChaoSpolit.d2h(result)
        aobs = "".join(bres[i - 1: i] for i in range(1, 17))
        aobs = ChaoSpolit.hex2le(aobs)
        first = False
        res = ChaoSpolit.AOBSCANALL(aobs, True)
        if res:
            valid = False
            for i in res:
                result = i
                offset_result = result - nameOffset
                try:
                    if ChaoSpolit.Pymem.read_longlong(offset_result + 8) == offset_result:
                        injectScript = offset_result
                        break
                except:
                    pass
        if valid:
            break
    injectScript = toInstance(injectScript)
    print("Attached to :", ChaoSpolit.d2h(injectScript.Self))
    ChaoSpolit.Pymem.process_handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, ChaoSpolit.Pymem.process_id)
    b = ChaoSpolit.Pymem.read_bytes(injectScript.Self + 0x100, 0x150)
    ChaoSpolit.Pymem.write_bytes(targetScript.Self + 0x100, b, len(b))
    coreGui = toInstance(game.GetChildren()[31])
    targetScript.SetParent(coreGui.Self)
    return True

import threading
import os

if __name__ == "__main__":
    global name
    name = threading.Thread(target=undetectname)
    name.daemon = True # idk what it does but docs say its to be running external
    name.start()
    input("Press Enter to inject!")
    if inject():
        Roblox = ChaoSpolit.YieldForProgram("RobloxPlayerBeta.exe")
        print("Reset your character to load the executor")
        stop_thread = True  # Stop the thread
        name.join()  # Wait for the thread to finish
        os._exit(1)
    else:
        Roblox = ChaoSpolit.YieldForProgram("RobloxPlayerBeta.exe")
        print("\033[35mError during injection! Line: Rsp12\033[0m")
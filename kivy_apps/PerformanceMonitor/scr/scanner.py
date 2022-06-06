import cpuinfo
import psutil
import GPUtil

class PCScanner:
    
    def get_cpu_name(self) -> str:
        ''' Returns the name of the CPU. '''
        return cpuinfo.get_cpu_info()['brand_raw']
    
    def get_cpu_load(self) -> float:
        ''' Returns the CPU load. '''
        return psutil.cpu_percent()
    
    def get_cpu_freq(self) -> float:
        ''' Returns the CPU frequency in MHz. '''
        return psutil.cpu_freq().current

    def get_total_ram(self) -> int:
        ''' Returns the total RAM in GB. '''
        return round(psutil.virtual_memory()[0] / 1024.**3, 1)
    
    def get_ram_usage(self) -> float:
        ''' Returns the RAM usage in GB. '''
        return round(psutil.virtual_memory()[3] / 1024.**3, 1)
    
    def get_gpu_name(self) -> str:
        ''' Returns the name of the GPU. '''
        return GPUtil.getGPUs()[0].name
    
    def get_gpu_memory(self) -> int:
        ''' Returns the memory of the GPU in MB. '''
        return round(GPUtil.getGPUs()[0].memoryTotal / 1024)
    
    def get_gpu_load(self) -> float:
        '''
        Returns the GPU load. 
        Return times 100 as GPUtil reports load in scale 0 to 1.
        '''
        return GPUtil.getGPUs()[0].load * 100
    
    def get_gpu_temp(self) -> int:
        ''' Returns the GPU temperature in C. '''
        return GPUtil.getGPUs()[0].temperature
    
    def get_storage_data(self) -> tuple[int, int]:
        ''' Returns the total and used storage in GB. All drives included.'''
        total = 0
        used = 0
        for part in psutil.disk_partitions():
            if part.fstype:
                total += psutil.disk_usage(part.mountpoint).total
                used += psutil.disk_usage(part.mountpoint).used
        return (round(total / 1024.**3, 1), round(used / 1024.**3, 1))  # type: ignore
        
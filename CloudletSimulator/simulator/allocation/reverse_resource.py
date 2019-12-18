from CloudletSimulator.simulator.model.device import Devices

# リソース順序
def reverse_resource_sort(devices:Devices):
    devices = sorted(devices, key=lambda d:d.use_resource, reverse=True)
    return devices

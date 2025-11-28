DEVICES = [
    {
        "deviceId": "0xA4C1",
        "deviceType": "phone",
        "vendor": "MockVendor",
        "model": "X1",
        "supportedGLayers": ["4G", "5G"],
    },
    {
        "deviceId": "0xB7D2",
        "deviceType": "phone",
        "vendor": "MockVendor",
        "model": "Y2",
        "supportedGLayers": ["4G"],
    },
]

TOWERS = [
    {
        "towerId": "T-01",
        "location": "Mock City",
        "bands": ["mid-band-5G", "4G-LTE"],
    },
    {
        "towerId": "T-02",
        "location": "Mock City",
        "bands": ["mid-band-5G"],
    },
]

ROUTES = [
    {
        "device_from": "0xA4C1",
        "device_to": "0xB7D2",
        "tower_id": "T-01",
        "frequency": "3.42GHz",
        "frequency_band": "mid-band-5G",
        "latency": 18.5,
        "signal_quality": 0.91,
        "pattern": "PulseShift-3",
    },
    {
        "device_from": "0xA4C1",
        "device_to": "0xB7D2",
        "tower_id": "T-02",
        "frequency": "3.60GHz",
        "frequency_band": "mid-band-5G",
        "latency": 26.0,
        "signal_quality": 0.84,
        "pattern": "PulseShift-2",
    },
]

FREQUENCIES = [
    {
        "name": "3.42GHz",
        "band": "mid-band-5G",
        "stability": 0.97,
        "drift": 0.01,
        "harmonics": ["6.84GHz", "10.26GHz"],
    },
    {
        "name": "3.60GHz",
        "band": "mid-band-5G",
        "stability": 0.93,
        "drift": 0.02,
        "harmonics": ["7.20GHz"],
    },
]

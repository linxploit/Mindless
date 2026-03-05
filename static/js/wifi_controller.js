/**
 * MINDLESS-REDOPS :: ESP8266 WIFI CONTROLLER
 * Control ESP8266 attack firmware from web interface
 * Author: ICAT Project | Linxploit.xyz
 */

// ============================================
// ESP8266 CONTROLLER STATE
// ============================================

const ESPController = {
    discoveredDevices: [],
    selectedDevice: null,
    scanInProgress: false,
    currentTab: 'attacks',
    apList: [],
    stationList: [],
    ssidList: [],
    attackStatus: {}
};

// ============================================
// DEVICE DISCOVERY
// ============================================

/**
 * Scan for ESP8266 devices
 */
Mindless.scanForESP = function() {
    const scanMethod = document.getElementById('scan_method').value;
    const interface = document.getElementById('wifi_interface').value;
    
    ESPController.scanInProgress = true;
    document.getElementById('scan_status').innerHTML = '<span class="text-cyan">Scanning...</span>';
    document.getElementById('scan_progress').style.width = '50%';
    
    // Simulate scan progress (actual scanning happens in backend)
    let progress = 50;
    const interval = setInterval(() => {
        progress += 5;
        document.getElementById('scan_progress').style.width = progress + '%';
        if (progress >= 90) clearInterval(interval);
    }, 500);
    
    // Call backend API
    fetch('/api/wifi/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            method: scanMethod,
            interface: interface
        })
    })
    .then(response => response.json())
    .then(data => {
        clearInterval(interval);
        document.getElementById('scan_progress').style.width = '100%';
        
        if (data.devices) {
            ESPController.discoveredDevices = data.devices;
            Mindless.updateDeviceList(data.devices);
            document.getElementById('scan_status').innerHTML = `<span class="text-green">✓ Found ${data.devices.length} devices</span>`;
        }
        
        setTimeout(() => {
            document.getElementById('scan_progress').style.width = '0%';
            document.getElementById('scan_status').innerHTML = '<span class="text-yellow">Ready</span>';
            ESPController.scanInProgress = false;
        }, 1000);
    })
    .catch(error => {
        clearInterval(interval);
        document.getElementById('scan_status').innerHTML = '<span class="text-red">✗ Scan failed</span>';
        ESPController.scanInProgress = false;
    });
};

/**
 * Update device list UI
 */
Mindless.updateDeviceList = function(devices) {
    const deviceList = document.getElementById('device_list');
    const deviceCount = document.getElementById('device_count');
    
    if (!devices || devices.length === 0) {
        deviceList.innerHTML = `
            <div style="text-align: center; color: var(--text-secondary); padding: 30px;">
                <i class="fas fa-wifi" style="font-size: 48px; opacity: 0.3; margin-bottom: 15px;"></i>
                <br>No devices discovered
                <br><span style="font-size: 12px;">Try a different scan method</span>
            </div>
        `;
        deviceCount.textContent = '0';
        return;
    }
    
    deviceCount.textContent = devices.length;
    
    let html = '';
    devices.forEach((device, index) => {
        const confidence = device.confidence || 0;
        let confidenceColor = 'var(--accent-green)';
        let confidenceText = 'High';
        
        if (confidence < 50) {
            confidenceColor = 'var(--accent-red)';
            confidenceText = 'Low';
        } else if (confidence < 80) {
            confidenceColor = 'var(--accent-yellow)';
            confidenceText = 'Medium';
        }
        
        html += `
            <div class="device-item" onclick="Mindless.selectDevice(${index})">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <span style="color: var(--accent-cyan); font-weight: bold;">${device.ssid || 'ESP8266'}</span>
                        <br>
                        <span style="color: var(--text-secondary); font-size: 12px;">${device.bssid || device.ip || 'Unknown'}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="color: ${confidenceColor}; font-size: 12px;">${confidenceText}</span>
                        <br>
                        <span style="color: var(--text-secondary); font-size: 11px;">${device.firmware || 'Unknown'}</span>
                    </div>
                </div>
            </div>
        `;
    });
    
    deviceList.innerHTML = html;
};

/**
 * Select device for control
 */
Mindless.selectDevice = function(index) {
    const device = ESPController.discoveredDevices[index];
    ESPController.selectedDevice = device;
    
    // Update UI
    document.querySelectorAll('.device-item').forEach(el => {
        el.classList.remove('selected');
    });
    event.currentTarget.classList.add('selected');
    
    // Show control panel
    document.getElementById('device_control_panel').style.display = 'block';
    document.getElementById('selected_device_name').textContent = device.ssid || 'ESP8266 Device';
    document.getElementById('selected_device_ip').textContent = device.ip || device.bssid || '192.168.4.1';
    
    // Connect to device
    Mindless.connectToDevice(device);
};

/**
 * Connect to selected ESP8266
 */
Mindless.connectToDevice = function(device) {
    const ip = device.ip || '192.168.4.1';
    
    fetch('/api/wifi/connect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ip: ip })
    })
    .then(response => response.json())
    .then(data => {
        if (data.firmware) {
            Mindless.showSuccess(`Connected to ${data.firmware}`, document.getElementById('results'));
            Mindless.refreshDeviceInfo();
        }
    })
    .catch(error => {
        Mindless.showError('Failed to connect to device', document.getElementById('results'));
    });
};

/**
 * Disconnect from device
 */
Mindless.disconnectDevice = function() {
    ESPController.selectedDevice = null;
    document.getElementById('device_control_panel').style.display = 'none';
};

/**
 * Refresh device info
 */
Mindless.refreshDeviceInfo = function() {
    if (!ESPController.selectedDevice) return;
    
    const ip = ESPController.selectedDevice.ip || '192.168.4.1';
    
    fetch(`/api/wifi/${ip}/info`)
        .then(response => response.json())
        .then(data => {
            if (data.firmware) {
                document.getElementById('selected_device_name').textContent = data.firmware;
            }
        });
};

// ============================================
// ATTACK CONTROLS
// ============================================

/**
 * Start specified attack
 */
Mindless.startAttack = function(attackType) {
    if (!ESPController.selectedDevice) {
        Mindless.showError('No device selected', document.getElementById('results'));
        return;
    }
    
    const ip = ESPController.selectedDevice.ip || '192.168.4.1';
    
    fetch(`/api/wifi/${ip}/attack/${attackType}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'attack_started') {
            Mindless.showSuccess(`${attackType.toUpperCase()} attack started`, document.getElementById('results'));
            ESPController.attackStatus[attackType] = true;
        }
    })
    .catch(error => {
        Mindless.showError(`Failed to start ${attackType}`, document.getElementById('results'));
    });
};

/**
 * Stop current attack
 */
Mindless.stopAttack = function() {
    if (!ESPController.selectedDevice) return;
    
    const ip = ESPController.selectedDevice.ip || '192.168.4.1';
    
    fetch(`/api/wifi/${ip}/stop`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        Mindless.showSuccess('Attack stopped', document.getElementById('results'));
        ESPController.attackStatus = {};
    });
};

// ============================================
// WIFI SCANNING
// ============================================

/**
 * Scan for WiFi networks
 */
Mindless.scanWiFi = function() {
    if (!ESPController.selectedDevice) return;
    
    const ip = ESPController.selectedDevice.ip || '192.168.4.1';
    
    fetch(`/api/wifi/${ip}/scan`)
        .then(response => response.json())
        .then(data => {
            ESPController.apList = data.aps || [];
            Mindless.updateAPList(ESPController.apList);
        });
};

/**
 * Update AP list UI
 */
Mindless.updateAPList = function(aps) {
    const apList = document.getElementById('ap_list');
    
    if (!aps || aps.length === 0) {
        apList.innerHTML = '<div style="text-align: center; color: var(--text-secondary); padding: 20px;">No access points found</div>';
        return;
    }
    
    let html = '';
    aps.forEach((ap, index) => {
        html += `
            <div style="padding: 10px; border-bottom: 1px solid var(--border-color);" onclick="Mindless.selectAP(${index})">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <span style="color: var(--accent-cyan);">${ap.ssid || 'Hidden'}</span>
                        <br>
                        <span style="color: var(--text-secondary); font-size: 11px;">${ap.bssid}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="color: var(--accent-green);">CH ${ap.channel}</span>
                        <br>
                        <span style="color: var(--text-secondary); font-size: 11px;">${ap.rssi} dBm</span>
                    </div>
                </div>
                <div style="margin-top: 5px; font-size: 11px; color: var(--text-secondary);">
                    Encryption: ${ap.encryption || 'Unknown'}
                </div>
            </div>
        `;
    });
    
    apList.innerHTML = html;
};

/**
 * Scan for stations
 */
Mindless.scanStations = function() {
    if (!ESPController.selectedDevice) return;
    
    const ip = ESPController.selectedDevice.ip || '192.168.4.1';
    
    fetch(`/api/wifi/${ip}/stations`)
        .then(response => response.json())
        .then(data => {
            ESPController.stationList = data.stations || [];
            Mindless.updateStationList(ESPController.stationList);
        });
};

/**
 * Update station list UI
 */
Mindless.updateStationList = function(stations) {
    const stationList = document.getElementById('station_list');
    
    if (!stations || stations.length === 0) {
        stationList.innerHTML = '<div style="text-align: center; color: var(--text-secondary); padding: 20px;">No stations found</div>';
        return;
    }
    
    let html = '';
    stations.forEach((station, index) => {
        html += `
            <div style="padding: 10px; border-bottom: 1px solid var(--border-color);" onclick="Mindless.selectStation(${index})">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <span style="color: var(--accent-yellow);">${station.station || 'Unknown'}</span>
                        <br>
                        <span style="color: var(--text-secondary); font-size: 11px;">${station.mac}</span>
                    </div>
                    <div>
                        <span style="color: var(--accent-green);">${station.rssi || '?'} dBm</span>
                    </div>
                </div>
                <div style="margin-top: 5px; font-size: 11px; color: var(--text-secondary);">
                    AP: ${station.ap || 'Unknown'}
                </div>
            </div>
        `;
    });
    
    stationList.innerHTML = html;
};

/**
 * Select AP as target
 */
Mindless.selectAP = function(index) {
    const ap = ESPController.apList[index];
    if (!ap) return;
    
    const ip = ESPController.selectedDevice.ip || '192.168.4.1';
    
    fetch(`/api/wifi/${ip}/select/ap`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: index })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('selected_ap').innerHTML = `
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <span style="color: var(--accent-cyan); font-weight: bold;">${ap.ssid}</span>
                    <br>
                    <span style="color: var(--text-secondary); font-size: 12px;">${ap.bssid}</span>
                </div>
                <div style="text-align: right;">
                    <span style="color: var(--accent-green);">CH ${ap.channel}</span>
                    <br>
                    <span style="color: var(--text-secondary); font-size: 11px;">Selected</span>
                </div>
            </div>
        `;
    });
};

/**
 * Select station as target
 */
Mindless.selectStation = function(index) {
    const station = ESPController.stationList[index];
    if (!station) return;
    
    const ip = ESPController.selectedDevice.ip || '192.168.4.1';
    
    fetch(`/api/wifi/${ip}/select/station`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: index })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('selected_station').innerHTML = `
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <span style="color: var(--accent-yellow);">${station.station || 'Client'}</span>
                    <br>
                    <span style="color: var(--text-secondary); font-size: 12px;">${station.mac}</span>
                </div>
                <div>
                    <span style="color: var(--accent-green);">${station.rssi || '?'} dBm</span>
                </div>
            </div>
        `;
    });
};

// ============================================
// SSID MANAGEMENT
// ============================================

/**
 * Add custom SSID
 */
Mindless.addCustomSSID = function() {
    const ssid = prompt('Enter SSID:');
    if (!ssid) return;
    
    if (!ESPController.selectedDevice) return;
    const ip = ESPController.selectedDevice.ip || '192.168.4.1';
    
    fetch(`/api/wifi/${ip}/ssid/add`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ssid: ssid })
    })
    .then(response => response.json())
    .then(data => {
        Mindless.loadSSIDList();
    });
};

/**
 * Generate random SSIDs
 */
Mindless.generateRandomSSIDs = function() {
    const count = prompt('How many SSIDs to generate?', '10');
    if (!count) return;
    
    if (!ESPController.selectedDevice) return;
    const ip = ESPController.selectedDevice.ip || '192.168.4.1';
    
    fetch(`/api/wifi/${ip}/ssid/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ count: parseInt(count) })
    })
    .then(response => response.json())
    .then(data => {
        Mindless.loadSSIDList();
    });
};

/**
 * Load SSID list
 */
Mindless.loadSSIDList = function() {
    if (!ESPController.selectedDevice) return;
    const ip = ESPController.selectedDevice.ip || '192.168.4.1';
    
    fetch(`/api/wifi/${ip}/ssids`)
        .then(response => response.json())
        .then(data => {
            ESPController.ssidList = data.ssids || [];
            Mindless.updateSSIDList(ESPController.ssidList);
        });
};

/**
 * Update SSID list UI
 */
Mindless.updateSSIDList = function(ssids) {
    const ssidList = document.getElementById('ssid_list');
    
    if (!ssids || ssids.length === 0) {
        ssidList.innerHTML = '<div style="text-align: center; color: var(--text-secondary); padding: 20px;">No SSIDs in list</div>';
        return;
    }
    
    let html = '';
    ssids.forEach((ssid, index) => {
        html += `
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px; border-bottom: 1px solid var(--border-color);">
                <span style="color: var(--accent-cyan);">${ssid}</span>
                <button class="btn" style="padding: 4px 8px; font-size: 11px;" onclick="Mindless.removeSSID(${index})">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
    });
    
    ssidList.innerHTML = html;
};

/**
 * Remove SSID from list
 */
Mindless.removeSSID = function(index) {
    if (!ESPController.selectedDevice) return;
    const ip = ESPController.selectedDevice.ip || '192.168.4.1';
    
    fetch(`/api/wifi/${ip}/ssid/remove`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: index })
    })
    .then(response => response.json())
    .then(data => {
        Mindless.loadSSIDList();
    });
};

/**
 * Clear all SSIDs
 */
Mindless.clearSSIDs = function() {
    if (!confirm('Clear all SSIDs?')) return;
    
    if (!ESPController.selectedDevice) return;
    const ip = ESPController.selectedDevice.ip || '192.168.4.1';
    
    fetch(`/api/wifi/${ip}/ssid/clear`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        ESPController.ssidList = [];
        Mindless.updateSSIDList([]);
    });
};

// ============================================
// TAB SWITCHING
// ============================================

/**
 * Switch between tabs
 */
Mindless.switchTab = function(tabName) {
    ESPController.currentTab = tabName;
    
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.currentTarget.classList.add('active');
    
    // Update tab content
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.getElementById(`tab_${tabName}`).classList.add('active');
    
    // Load tab-specific data
    if (tabName === 'ssids') {
        Mindless.loadSSIDList();
    } else if (tabName === 'scan') {
        Mindless.scanWiFi();
        Mindless.scanStations();
    }
};

// ============================================
// DEVICE SETTINGS
// ============================================

/**
 * Save device settings
 */
Mindless.saveSettings = function() {
    if (!ESPController.selectedDevice) return;
    
    const ip = ESPController.selectedDevice.ip || '192.168.4.1';
    const settings = {
        name: document.getElementById('device_name').value,
        ssid: document.getElementById('ap_ssid').value,
        password: document.getElementById('ap_password').value
    };
    
    fetch(`/api/wifi/${ip}/settings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settings)
    })
    .then(response => response.json())
    .then(data => {
        Mindless.showSuccess('Settings saved', document.getElementById('results'));
    });
};

/**
 * Save attack configuration
 */
Mindless.saveAttackConfig = function() {
    if (!ESPController.selectedDevice) return;
    
    const ip = ESPController.selectedDevice.ip || '192.168.4.1';
    const config = {
        deauth_packets: document.getElementById('deauth_packets').value,
        beacon_interval: document.getElementById('beacon_interval').value,
        probe_delay: document.getElementById('probe_delay').value
    };
    
    fetch(`/api/wifi/${ip}/config`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config)
    })
    .then(response => response.json())
    .then(data => {
        Mindless.showSuccess('Attack config saved', document.getElementById('results'));
    });
};

/**
 * Reboot device
 */
Mindless.rebootDevice = function() {
    if (!confirm('Reboot ESP8266?')) return;
    
    if (!ESPController.selectedDevice) return;
    const ip = ESPController.selectedDevice.ip || '192.168.4.1';
    
    fetch(`/api/wifi/${ip}/reboot`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        Mindless.showSuccess('Reboot command sent', document.getElementById('results'));
        setTimeout(() => {
            Mindless.disconnectDevice();
        }, 2000);
    });
};

/**
 * Reset configuration
 */
Mindless.resetConfig = function() {
    if (!confirm('Reset to default settings?')) return;
    
    document.getElementById('deauth_packets').value = '5';
    document.getElementById('beacon_interval').value = '100';
    document.getElementById('probe_delay').value = '50';
    
    Mindless.saveAttackConfig();
};
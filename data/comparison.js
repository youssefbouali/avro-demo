// Global state
let isRunning = false;
let testInterval;
let totalRecordsSent = 0;

// Metrics storage
let metrics = {
    json: {
        times: [],
        sizes: [],
        totalSize: 0,
        recordCount: 0,
        batches: 0
    },
    avro: {
        times: [],
        sizes: [],
        totalSize: 0,
        recordCount: 0,
        batches: 0
    }
};

// Chart instances
let charts = {
    json: null,
    avro: null
};

// Sample user data generators
function generateSmallUser(id) {
    return {
        id: id,
        nom: `User_${id}`,
        age: Math.floor(Math.random() * 60) + 18
    };
}

function generateMediumUser(id) {
    return {
        id: id,
        nom: `User_${id}`,
        age: Math.floor(Math.random() * 60) + 18,
        email: `user${id}@example.com`,
        actif: Math.random() > 0.5
    };
}

function generateLargeUser(id) {
    return {
        id: id,
        nom: `User_${id}`,
        age: Math.floor(Math.random() * 60) + 18,
        email: `user${id}@example.com`,
        actif: Math.random() > 0.5,
        phone: `+1-${String(Math.random() * 1000000000 | 0).padStart(10, '0')}`,
        address: `${Math.random() * 10000 | 0} Main St`,
        city: ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'][Math.random() * 5 | 0],
        country: 'USA',
        zipcode: String(Math.random() * 100000 | 0).padStart(5, '0')
    };
}

// JSON Serialization
function jsonSerialize(data) {
    return JSON.stringify(data);
}

function jsonDeserialize(str) {
    return JSON.parse(str);
}

// Simple Avro-like binary serialization
class AvroSerializer {
    static encodeString(str) {
        const encoder = new TextEncoder();
        const encoded = encoder.encode(str);
        return this.encodeVarInt(encoded.length).concat(Array.from(encoded));
    }

    static encodeVarInt(value) {
        const bytes = [];
        while ((value & 0xFFFFFF80) !== 0) {
            bytes.push((value & 0x7F) | 0x80);
            value >>>= 7;
        }
        bytes.push(value & 0x7F);
        return bytes;
    }

    static encodeInt(value) {
        // Two's complement for negative numbers
        const zigzag = (value << 1) ^ (value >> 31);
        return this.encodeVarInt(zigzag);
    }

    static encodeBoolean(value) {
        return [value ? 1 : 0];
    }

    static encodeRecord(data, schema) {
        let bytes = [];
        for (const field of schema.fields) {
            const value = data[field.name];
            if (field.type === 'long') {
                bytes = bytes.concat(this.encodeInt(value));
            } else if (field.type === 'string') {
                bytes = bytes.concat(this.encodeString(value));
            } else if (field.type === 'int') {
                bytes = bytes.concat(this.encodeInt(value));
            } else if (field.type === 'boolean') {
                bytes = bytes.concat(this.encodeBoolean(value));
            } else if (Array.isArray(field.type)) {
                // Handle union types (null, type)
                if (value === null) {
                    bytes.push(0); // null index
                } else {
                    bytes.push(1); // type index
                    if (field.type[1] === 'string') {
                        bytes = bytes.concat(this.encodeString(value));
                    } else if (field.type[1] === 'int') {
                        bytes = bytes.concat(this.encodeInt(value));
                    }
                }
            }
        }
        return bytes;
    }

    static serialize(data, schema) {
        const bytes = this.encodeRecord(data, schema);
        return new Uint8Array(bytes);
    }

    static bytesToHex(bytes) {
        return Array.from(bytes).map(b => b.toString(16).padStart(2, '0')).join('');
    }
}

// Schemas
const schemas = {
    small: {
        name: 'User_v1',
        fields: [
            { name: 'id', type: 'long' },
            { name: 'nom', type: 'string' },
            { name: 'age', type: 'int' }
        ]
    },
    medium: {
        name: 'User_v2',
        fields: [
            { name: 'id', type: 'long' },
            { name: 'nom', type: 'string' },
            { name: 'age', type: 'int' },
            { name: 'email', type: ['null', 'string'] },
            { name: 'actif', type: 'boolean' }
        ]
    },
    large: {
        name: 'User_extended',
        fields: [
            { name: 'id', type: 'long' },
            { name: 'nom', type: 'string' },
            { name: 'age', type: 'int' },
            { name: 'email', type: ['null', 'string'] },
            { name: 'actif', type: 'boolean' },
            { name: 'phone', type: 'string' },
            { name: 'address', type: 'string' },
            { name: 'city', type: 'string' },
            { name: 'country', type: 'string' },
            { name: 'zipcode', type: 'string' }
        ]
    }
};

// Get user generator based on size
function getUserGenerator(size) {
    switch(size) {
        case 'small': return generateSmallUser;
        case 'medium': return generateMediumUser;
        case 'large': return generateLargeUser;
        default: return generateMediumUser;
    }
}

// Get schema based on size
function getSchema(size) {
    return schemas[size] || schemas.medium;
}

// Format bytes
function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

// Log messages
function addLog(type, message) {
    const logEl = document.getElementById(`${type}Log`);
    const timestamp = new Date().toLocaleTimeString();
    const entry = document.createElement('div');
    entry.className = 'log-entry';
    entry.innerHTML = `<span class="log-timestamp">[${timestamp}]</span> ${message}`;
    logEl.appendChild(entry);
    logEl.scrollTop = logEl.scrollHeight;
    
    // Keep only last 10 entries
    const entries = logEl.querySelectorAll('.log-entry');
    if (entries.length > 10) {
        entries[0].remove();
    }
}

// Initialize charts
function initializeCharts() {
    const chartConfig = {
        type: 'line',
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Size (bytes)' }
                }
            }
        }
    };

    const jsonCtx = document.getElementById('jsonChart').getContext('2d');
    const avroCtx = document.getElementById('avroChart').getContext('2d');

    charts.json = new Chart(jsonCtx, {
        ...chartConfig,
        data: {
            labels: [],
            datasets: [{
                label: 'Record Size',
                data: [],
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 2,
                tension: 0.3,
                fill: true
            }]
        }
    });

    charts.avro = new Chart(avroCtx, {
        ...chartConfig,
        data: {
            labels: [],
            datasets: [{
                label: 'Record Size',
                data: [],
                borderColor: '#f6ad55',
                backgroundColor: 'rgba(246, 173, 85, 0.1)',
                borderWidth: 2,
                tension: 0.3,
                fill: true
            }]
        }
    });
}

// Update metrics display
function updateMetricsDisplay() {
    // JSON metrics
    const jsonAvgTime = metrics.json.times.length > 0 
        ? (metrics.json.times.reduce((a, b) => a + b, 0) / metrics.json.times.length).toFixed(3)
        : 0;
    const jsonAvgSize = metrics.json.recordCount > 0
        ? (metrics.json.totalSize / metrics.json.recordCount).toFixed(1)
        : 0;
    const jsonThroughput = metrics.json.batches > 0
        ? ((metrics.json.totalSize / metrics.json.batches) / (parseInt(document.getElementById('batchInterval').value) / 1000)).toFixed(0)
        : 0;

    document.getElementById('jsonTime').textContent = jsonAvgTime;
    document.getElementById('jsonRecords').textContent = metrics.json.recordCount;
    document.getElementById('jsonAvgSize').textContent = jsonAvgSize;
    document.getElementById('jsonTotalSize').textContent = formatBytes(metrics.json.totalSize);
    document.getElementById('jsonThroughput').textContent = formatBytes(jsonThroughput) + '/s';

    // Avro metrics
    const avroAvgTime = metrics.avro.times.length > 0
        ? (metrics.avro.times.reduce((a, b) => a + b, 0) / metrics.avro.times.length).toFixed(3)
        : 0;
    const avroAvgSize = metrics.avro.recordCount > 0
        ? (metrics.avro.totalSize / metrics.avro.recordCount).toFixed(1)
        : 0;
    const avroThroughput = metrics.avro.batches > 0
        ? ((metrics.avro.totalSize / metrics.avro.batches) / (parseInt(document.getElementById('batchInterval').value) / 1000)).toFixed(0)
        : 0;

    document.getElementById('avroTime').textContent = avroAvgTime;
    document.getElementById('avroRecords').textContent = metrics.avro.recordCount;
    document.getElementById('avroAvgSize').textContent = avroAvgSize;
    document.getElementById('avroTotalSize').textContent = formatBytes(metrics.avro.totalSize);
    document.getElementById('avroThroughput').textContent = formatBytes(avroThroughput) + '/s';

    // Summary metrics
    document.getElementById('totalRecords').textContent = metrics.json.recordCount;
    document.getElementById('avgJsonSize').textContent = jsonAvgSize + ' bytes';
    document.getElementById('avgAvroSize').textContent = avroAvgSize + ' bytes';
    
    const compressionRatio = jsonAvgSize > 0 
        ? ((1 - (avroAvgSize / jsonAvgSize)) * 100).toFixed(1)
        : 0;
    document.getElementById('compressionRatio').textContent = compressionRatio + '%';
    document.getElementById('avgAvroTime').textContent = avroAvgTime + ' ms';
    document.getElementById('avgJsonTime').textContent = jsonAvgTime + ' ms';

    // Update summary comparison
    updateComparison();
}

// Update comparison result
function updateComparison() {
    const jsonAvgSize = metrics.json.recordCount > 0
        ? metrics.json.totalSize / metrics.json.recordCount
        : 0;
    const avroAvgSize = metrics.avro.recordCount > 0
        ? metrics.avro.totalSize / metrics.avro.recordCount
        : 0;
    const jsonAvgTime = metrics.json.times.length > 0
        ? metrics.json.times.reduce((a, b) => a + b, 0) / metrics.json.times.length
        : 0;
    const avroAvgTime = metrics.avro.times.length > 0
        ? metrics.avro.times.reduce((a, b) => a + b, 0) / metrics.avro.times.length
        : 0;

    if (metrics.json.recordCount > 0) {
        const resultDiv = document.getElementById('comparisonResult');
        const compression = jsonAvgSize > 0 ? ((1 - avroAvgSize / jsonAvgSize) * 100).toFixed(1) : 0;
        const speedup = jsonAvgTime > 0 ? (jsonAvgTime / avroAvgTime).toFixed(2) : 0;
        
        let resultHTML = `
            <div class="comparison-result ${avroAvgSize < jsonAvgSize ? 'avro-faster' : ''}">
                <strong>📊 Comparison Results:</strong><br>
                Data Compression: <strong>${compression}%</strong> smaller with Avro<br>
                Speed Difference: <strong>${speedup}x</strong> ${avroAvgTime < jsonAvgTime ? 'faster' : 'slower'} with Avro<br>
                Total Data Sent: JSON: <strong>${formatBytes(metrics.json.totalSize)}</strong> vs Avro: <strong>${formatBytes(metrics.avro.totalSize)}</strong>
            </div>
        `;
        resultDiv.innerHTML = resultHTML;
    }
}

// Run single batch
async function runBatch() {
    const numRecords = parseInt(document.getElementById('numRecords').value);
    const dataSize = document.getElementById('dataSize').value;
    const userGen = getUserGenerator(dataSize);
    const schema = getSchema(dataSize);

    // Generate users
    const users = [];
    for (let i = 0; i < numRecords; i++) {
        users.push(userGen(totalRecordsSent + i));
    }

    // JSON Serialization
    const jsonStart = performance.now();
    const jsonData = JSON.stringify(users);
    const jsonEnd = performance.now();
    const jsonTime = jsonEnd - jsonStart;
    const jsonSize = new Blob([jsonData]).size;

    metrics.json.times.push(jsonTime);
    metrics.json.sizes.push(jsonSize / numRecords);
    metrics.json.totalSize += jsonSize;
    metrics.json.recordCount += numRecords;
    metrics.json.batches++;

    // Avro Serialization
    const avroStart = performance.now();
    let avroTotalSize = 0;
    for (const user of users) {
        const avroData = AvroSerializer.serialize(user, schema);
        avroTotalSize += avroData.byteLength;
    }
    const avroEnd = performance.now();
    const avroTime = avroEnd - avroStart;

    metrics.avro.times.push(avroTime);
    metrics.avro.sizes.push(avroTotalSize / numRecords);
    metrics.avro.totalSize += avroTotalSize;
    metrics.avro.recordCount += numRecords;
    metrics.avro.batches++;

    totalRecordsSent += numRecords;

    // Update charts
    updateCharts();

    // Update metrics
    updateMetricsDisplay();

    // Add logs
    const avgJsonSize = (jsonSize / numRecords).toFixed(1);
    const avgAvroSize = (avroTotalSize / numRecords).toFixed(1);
    const compression = ((1 - avgAvroSize / avgJsonSize) * 100).toFixed(1);

    addLog('json', `✓ Batch #${metrics.json.batches}: ${numRecords} records, ${formatBytes(jsonSize)} total, ${jsonTime.toFixed(2)}ms (${avgJsonSize}B/rec)`);
    addLog('avro', `✓ Batch #${metrics.avro.batches}: ${numRecords} records, ${formatBytes(avroTotalSize)} total, ${avroTime.toFixed(2)}ms (${avgAvroSize}B/rec, ${compression}% smaller)`);
}

// Update charts
function updateCharts() {
    if (metrics.json.sizes.length > 0) {
        charts.json.data.labels = Array.from({length: metrics.json.sizes.length}, (_, i) => i + 1);
        charts.json.data.datasets[0].data = metrics.json.sizes;
        charts.json.update('none');
    }

    if (metrics.avro.sizes.length > 0) {
        charts.avro.data.labels = Array.from({length: metrics.avro.sizes.length}, (_, i) => i + 1);
        charts.avro.data.datasets[0].data = metrics.avro.sizes;
        charts.avro.update('none');
    }
}

// Start comparison
function startComparison() {
    if (isRunning) return;

    isRunning = true;
    document.getElementById('startBtn').style.display = 'none';
    document.getElementById('stopBtn').style.display = 'inline-block';
    
    // Update status
    document.getElementById('jsonStatus').className = 'status running';
    document.getElementById('jsonStatus').innerHTML = '<span class="status-dot"></span>Running...';
    document.getElementById('avroStatus').className = 'status running';
    document.getElementById('avroStatus').innerHTML = '<span class="status-dot"></span>Running...';

    const interval = parseInt(document.getElementById('batchInterval').value);
    
    // Run first batch immediately
    runBatch();

    // Schedule subsequent batches
    testInterval = setInterval(runBatch, interval);
}

// Stop comparison
function stopComparison() {
    if (!isRunning) return;

    isRunning = false;
    clearInterval(testInterval);
    
    document.getElementById('startBtn').style.display = 'inline-block';
    document.getElementById('stopBtn').style.display = 'none';

    // Update status
    document.getElementById('jsonStatus').className = 'status stopped';
    document.getElementById('jsonStatus').innerHTML = '<span class="status-dot"></span>Stopped';
    document.getElementById('avroStatus').className = 'status stopped';
    document.getElementById('avroStatus').innerHTML = '<span class="status-dot"></span>Stopped';

    addLog('json', '⏹ Test stopped');
    addLog('avro', '⏹ Test stopped');
}

// Reset metrics
function resetMetrics() {
    stopComparison();
    
    metrics = {
        json: {
            times: [],
            sizes: [],
            totalSize: 0,
            recordCount: 0,
            batches: 0
        },
        avro: {
            times: [],
            sizes: [],
            totalSize: 0,
            recordCount: 0,
            batches: 0
        }
    };

    totalRecordsSent = 0;

    // Clear logs
    document.getElementById('jsonLog').innerHTML = '<div class="log-entry"><span class="log-timestamp">[Waiting...]</span></div>';
    document.getElementById('avroLog').innerHTML = '<div class="log-entry"><span class="log-timestamp">[Waiting...]</span></div>';

    // Reset charts
    if (charts.json) {
        charts.json.data.labels = [];
        charts.json.data.datasets[0].data = [];
        charts.json.update();
    }
    if (charts.avro) {
        charts.avro.data.labels = [];
        charts.avro.data.datasets[0].data = [];
        charts.avro.update();
    }

    // Update status
    document.getElementById('jsonStatus').className = 'status idle';
    document.getElementById('jsonStatus').innerHTML = '<span class="status-dot"></span>Idle';
    document.getElementById('avroStatus').className = 'status idle';
    document.getElementById('avroStatus').innerHTML = '<span class="status-dot"></span>Idle';

    updateMetricsDisplay();
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeCharts();
    updateMetricsDisplay();
});

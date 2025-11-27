# Avro vs JSON Performance Comparison Tool

A real-time interactive web-based comparison tool that demonstrates the performance differences between JSON and Avro serialization formats.

## Features

✨ **Real-time Performance Metrics**
- Live encoding time measurements
- Data size tracking and comparison
- Throughput calculation
- Compression ratio analysis

📊 **Visual Comparisons**
- Side-by-side performance panels
- Real-time chart updates showing record sizes
- Color-coded metrics (JSON: Blue, Avro: Orange)
- Live log stream for each format

🔄 **Interactive Testing**
- Configurable batch sizes
- Adjustable batch intervals
- Multiple data sizes (small, medium, large schemas)
- Start/stop/reset controls

📈 **Comprehensive Summary**
- Total records processed
- Average encoding times
- Compression ratios
- Throughput metrics
- Data size comparisons

## Quick Start

### 1. Start the Web Server

```bash
cd data/

# Python 3
python server.py
```

The server will start on `http://localhost:8000`

### 2. Open in Browser

Navigate to: **http://localhost:8000**

### 3. Run Comparison

1. **Configure Test Parameters:**
   - Records per Batch: Number of records to process in each batch (default: 100)
   - Batch Interval: Time between batches in milliseconds (default: 1000ms)
   - Data Size: Select schema size (Small/Medium/Large)

2. **Start the Test:**
   - Click "▶ Start Test" to begin real-time comparison
   - Metrics update in real-time as batches are processed

3. **Monitor Results:**
   - Watch encoding times in the metrics panels
   - See data sizes in the large blue/orange boxes
   - Check compression ratios in the summary section
   - Review batch logs in each panel

4. **Stop and Reset:**
   - Click "⏹ Stop Test" to pause
   - Click "🔄 Reset" to clear all data

## Data Sizes

### Small Schema (v1)
- id (long)
- nom (string)
- age (int)

**Expected:** ~30-50 bytes (JSON), ~8-15 bytes (Avro)

### Medium Schema (v2) - Recommended
- id (long)
- nom (string)
- age (int)
- email (optional string)
- actif (boolean)

**Expected:** ~60-100 bytes (JSON), ~15-25 bytes (Avro)

### Large Schema
- All Medium fields plus:
- phone (string)
- address (string)
- city (string)
- country (string)
- zipcode (string)

**Expected:** ~250-350 bytes (JSON), ~80-120 bytes (Avro)

## Understanding the Metrics

### Left Panel - JSON (REST API)
- **Encoding Time**: Time to serialize data to JSON string
- **Records/Batch**: Total records processed
- **Avg Size/Record**: Average bytes per record
- **Throughput**: Bytes per second

### Right Panel - Avro (Binary)
- **Encoding Time**: Time to serialize data to Avro binary
- **Records/Batch**: Total records processed
- **Avg Size/Record**: Average bytes per record (significantly smaller)
- **Throughput**: Bytes per second

### Summary Section
- **Compression Ratio**: Percentage reduction in size (Avro vs JSON)
- **Data Size Comparison**: Total bytes sent in each format
- **Encoding Time Difference**: Which format is faster
- **Overall Efficiency**: Visual representation of improvements

## Performance Characteristics

### Typical Results

For **Medium Schema** with 1000 records:

| Metric | JSON | Avro | Improvement |
|--------|------|------|-------------|
| Avg Size/Record | ~75 bytes | ~20 bytes | 73% smaller |
| Encoding Time | ~2.5ms | ~1.8ms | 28% faster |
| Total Size (1000 rec) | ~75 KB | ~20 KB | 73% compression |
| Throughput | ~2.5 MB/s | ~3.2 MB/s | 28% faster |

## Test Scenarios

### Scenario 1: Many Small Batches
- Records: 10
- Interval: 500ms
- Data Size: Medium
- **Result**: See impact of serialization overhead

### Scenario 2: Large Batches
- Records: 1000
- Interval: 2000ms
- Data Size: Large
- **Result**: Significant size and time differences

### Scenario 3: High-Frequency Streaming
- Records: 100
- Interval: 100ms
- Data Size: Medium
- **Result**: Throughput comparison under load

### Scenario 4: Large Object Comparison
- Records: 50
- Interval: 1000ms
- Data Size: Large
- **Result**: Maximum compression benefit

## How It Works

### JSON Serialization
1. Converts object to JSON string using `JSON.stringify()`
2. Counts bytes using Blob size
3. Measures elapsed time with `performance.now()`

### Avro Serialization
1. Implements Avro binary encoding in JavaScript
2. Uses VarInt encoding for integers
3. Uses UTF-8 encoding for strings
4. Handles union types (null, type)
5. Counts serialized bytes

### Key Implementation Details

**Avro Encoding Features:**
- Variable-length integer encoding (VarInt)
- UTF-8 string encoding with length prefix
- Two's complement zigzag encoding for signed integers
- Union type handling for optional fields

**Measurements:**
- Encoding time: From start of serialization to completion
- Data size: Actual bytes required for storage
- Throughput: Total bytes ÷ interval time
- Compression: (1 - avro_size / json_size) × 100

## Browser Compatibility

Works in all modern browsers:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

Requires:
- Chart.js library (CDN)
- ES6 JavaScript support
- LocalStorage (for future enhancements)

## API Integration

This tool compares JSON and Avro formats. For real Kafka integration:

1. **Keep JSON Endpoint**: Your REST API
2. **Add Avro Support**: Integrate with the Python API server (`api_server.py`)
3. **Modify JS Client**: Update to make actual HTTP requests instead of local serialization

### Modified Implementation Example

```javascript
// Replace local Avro encoding with API call
async function sendToAvroAPI(users, schema) {
    const response = await fetch('http://localhost:5000/api/users/encode/v2', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(users[0])
    });
    return response.json();
}

// Use both local and API endpoints
async function runBatch() {
    // JSON locally
    const jsonStart = performance.now();
    const jsonData = JSON.stringify(users);
    const jsonEnd = performance.now();
    
    // Avro via API
    const avroStart = performance.now();
    const avroResponse = await sendToAvroAPI(users, schema);
    const avroEnd = performance.now();
    
    // Compare
}
```

## Troubleshooting

### Server won't start
```bash
# Check if port 8000 is in use
# Try a different port: python server.py --port 8080
```

### Charts not rendering
- Ensure Chart.js CDN is accessible
- Check browser console for errors
- Refresh the page

### Metrics not updating
- Check browser DevTools Console for errors
- Verify JavaScript is enabled
- Try resetting with the 🔄 button

## Files Structure

```
data/
├── index.html           # Main UI
├── comparison.js        # All logic and visualizations
├── server.py            # HTTP server
├── api_server.py        # Python REST API (optional)
├── test_api_client.py   # API tests
├── user_v1.avsc         # Schema definitions
└── user_v2.avsc
```

## Future Enhancements

- [ ] Real-time connection to Kafka
- [ ] Persistent storage of results
- [ ] Export metrics as CSV/JSON
- [ ] Add Protobuf comparison
- [ ] Network latency simulation
- [ ] Different compression algorithms comparison
- [ ] Record decompression verification
- [ ] Schema evolution testing

## License

This tool is part of the avro-demo project.

const countDisplay = document.getElementById('count-display');
const emaDisplay = document.getElementById('ema-display');
const statusLight = document.getElementById('status-light');
let ws;

function connect() {
    // Create WebSocket connection
    ws = new WebSocket(`ws://${window.location.host}/ws`);

    ws.onopen = (event) => {
        console.log("Connected to WebSocket");
        statusLight.textContent = "Connected (Real-time)";
        statusLight.className = "status connected";
    };

    // Receive data
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        // update value
        countDisplay.textContent = Math.round(data.ema); // data.count
        emaDisplay.textContent = `(EMA: ${data.ema.toFixed(2)})`;

        // change the color upon the number changing
        countDisplay.style.color = '#1E88E5';
        setTimeout(() => {
            countDisplay.style.color = '#4CAF50';
        }, 200);
    };

    ws.onclose = (event) => {
        console.log("WebSocket disconnected. Reconnecting...");
        statusLight.textContent = "Disconnected. Retrying...";
        statusLight.className = "status";
        setTimeout(connect, 3000); 
    };

    ws.onerror = (error) => {
        console.error("WebSocket Error:", error);
        statusLight.textContent = "Connection Error";
        statusLight.className = "status";
        ws.close();
    };
}

connect();
echo "🛑 Stopping CyberGuard Risk Assessment System..."

# Kill processes by PID if files exist
if [ -f .python.pid ]; then
    kill $(cat .python.pid) 2>/dev/null
    rm .python.pid
fi

if [ -f .java.pid ]; then
    kill $(cat .java.pid) 2>/dev/null
    rm .java.pid
fi

if [ -f .frontend.pid ]; then
    kill $(cat .frontend.pid) 2>/dev/null
    rm .frontend.pid
fi

# Fallback: kill by process name
pkill -f "python app.py"
pkill -f "spring-boot:run"
pkill -f "react-scripts start"

echo "✅ All services stopped!"
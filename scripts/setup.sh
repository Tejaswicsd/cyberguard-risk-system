echo " Setting up CyberGuard Risk Assessment System..."

# Setup Frontend
echo " Installing Frontend Dependencies..."
cd frontend
npm install
cd ..

# Setup Python Backend
echo "🐍 Setting up Python Backend..."
cd backend-python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Setup Java Backend
echo " Setting up Java Backend..."
cd backend-java
mvn clean install
cd ..

echo "✅ Setup completed successfully!"

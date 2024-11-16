To run FE

cd fe

npm install
npm run dev


Frontend
cd frontend
// For NEXT JS
npx create-next-app@latest . 

// TAIL WINDS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p


npm install @reduxjs/toolkit react-redux axios


Finally Docker
docker-compose up --build



For local setup 
python manage.py rabbitmq_consumer
python backend/metrics/publisher.py



brew install redis

# Start Redis
brew services start redis

# Verify Redis is running
redis-cli ping

# Install RabbitMQ
brew install rabbitmq

# Start RabbitMQ
brew services start rabbitmq

# Add RabbitMQ commands to your PATH (add this to your ~/.zshrc or ~/.bash_profile)
export PATH=$PATH:/usr/local/opt/rabbitmq/sbin


Access RabbitMQ Management Interface:


Open http://localhost:15672
Default credentials:

Username: guest
Password: guest



Important Information:

Redis default port: 6379
RabbitMQ default ports:

5672 (AMQP)
15672 (Management Interface)

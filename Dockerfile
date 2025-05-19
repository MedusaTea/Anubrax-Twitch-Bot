FROM python:3.11-slim

# Set environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /bot

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code
COPY rogue-blight-chat.py .
COPY chatters.txt .

# Run the bot
CMD ["python", "rogue-blight-chat.py"]



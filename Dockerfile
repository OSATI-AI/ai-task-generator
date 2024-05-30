FROM zauberzeug/nicegui:1.4.26

# Copy the requirements file first (to leverage Docker cache)
COPY requirements.txt /tmp/

# Install dependencies using pip from the requirements file
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app
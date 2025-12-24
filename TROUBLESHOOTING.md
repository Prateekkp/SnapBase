# SnapBase Troubleshooting Guide

## 🚨 Common Issues & Solutions

### Installation Issues

#### Problem 1: "Python is not installed or not in PATH"

**Windows:**
```powershell
# Download from https://www.python.org/downloads/
# IMPORTANT: Check "Add Python to PATH" during installation

# Verify installation
python --version
```

**macOS:**
```bash
brew install python3
python3 --version
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
python3 --version
```

---

#### Problem 2: "pip is not available"

```bash
# Windows
python -m pip install --upgrade pip

# macOS/Linux
python3 -m pip install --upgrade pip
```

---

#### Problem 3: Installation fails with permission errors

```bash
# Use --user flag to install in user directory
pip install --user -e .

# Or use virtual environment (recommended)
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -e .
```

---

#### Problem 4: MySQL connector compilation fails

```bash
# macOS - Install MySQL client development files
brew install mysql-client

# Ubuntu/Debian
sudo apt-get install libmysqlclient-dev

# Fedora/RHEL
sudo dnf install mysql-devel

# Then try installation again
pip install -e .
```

---

### Runtime Issues

#### Problem 5: "Cannot connect to database"

**Checklist:**
- [ ] Is MySQL/MariaDB server running?
- [ ] Is the host/IP correct?
- [ ] Is the port correct? (default: 3306)
- [ ] Is the username correct?
- [ ] Is the password correct?
- [ ] Is there a firewall blocking the connection?

**Test connection manually:**
```bash
# Windows
mysql -h localhost -u root -p

# macOS/Linux
mysql -h 127.0.0.1 -u root -p
```

**Debug mode:**
```bash
# Add to .env
DEBUG_MODE=true
LOG_LEVEL=DEBUG

# Restart SnapBase for detailed logs
snapbase
```

---

#### Problem 6: "API key not validated"

**Checklist:**
- [ ] Is the API key correct?
- [ ] Is the API key from NVIDIA? (https://build.nvidia.com/)
- [ ] Is your internet connection working?
- [ ] Has the API key expired?

**Test API key:**
```python
from llm.generator import test_api_key

# In Python shell
test_api_key("your_api_key_here")
```

---

#### Problem 7: "Could not extract valid SQL from LLM output"

**Possible causes:**
1. API rate limit exceeded
2. Invalid query description
3. LLM service issue

**Solutions:**
```bash
# Clear config and try again
rm snapbase_config.json

# Or try restarting
snapbase

# Check if service is available
curl https://api.nvidia.com/  # Should respond quickly
```

---

#### Problem 8: "Connection timeout"

```bash
# Increase timeout in code
# Edit: db/connection.py

# Add timeout parameter:
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    timeout=30  # Increase from default 5
)
```

---

### Configuration Issues

#### Problem 9: "Config file not found"

```bash
# SnapBase creates config automatically on first run
# If missing, check:

# Windows
%APPDATA%\snapbase\  # or current directory

# macOS/Linux
~/.config/snapbase/  # or current directory

# Manual creation:
mkdir -p ~/.config/snapbase
touch ~/.config/snapbase/config.json
```

---

#### Problem 10: "Credentials stored insecurely"

**Current:** Passwords stored in plain text (security issue)

**Workaround:**
```bash
# Use .env file instead
cp .env.example .env

# Edit .env with your credentials
# Add to code: from dotenv import load_dotenv
load_dotenv()

# This keeps credentials out of config files
```

---

### Platform-Specific Issues

#### macOS Issues

**Issue:** Command not found after installation
```bash
# Ensure you're using the correct Python
which python3

# Or use:
python3 -m pip install -e .

# Then run:
python3 -m main
```

---

#### Linux Issues

**Issue:** Permission denied on config directory
```bash
# Check permissions
ls -la ~/.config/snapbase/

# Fix permissions
chmod 700 ~/.config/snapbase/
```

---

#### Windows Issues

**Issue:** "Command not recognized" in PowerShell
```powershell
# Refresh environment variables
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Or restart PowerShell

# Test again
snapbase
```

---

### Docker Alternative

If all else fails, use Docker!

```bash
# Install Docker from https://www.docker.com/products/docker-desktop

# Build Docker image
docker build -t snapbase .

# Run SnapBase
docker run -it --rm snapbase

# Or use Docker Compose
docker-compose up
```

---

## 🔍 Debug Checklist

When reporting issues, please gather:

```bash
# System info
python --version
pip --version

# Database connectivity
ping your_db_host

# Network test
curl https://api.nvidia.com/

# Check logs
cat snapbase_config.json
tail -f snapbase.log  # if logging enabled

# Python environment
pip list | grep -E "mysql|requests|python-dotenv|tabulate"

# OS info
uname -a  # Unix/Linux/macOS
systeminfo  # Windows
```

---

## 📞 Getting Help

If issues persist:

1. **Check RISK_ANALYSIS.md** - Known issues and workarounds
2. **Enable debug mode** - Set `DEBUG_MODE=true` in .env
3. **Check logs** - Look for error messages
4. **Try Docker** - Eliminates environment issues
5. **Test components individually** - Isolate the problem

---

## 🚀 Performance Optimization

If SnapBase is slow:

```bash
# 1. Increase API timeout
# Edit: .env
API_TIMEOUT=60

# 2. Enable connection pooling
# TODO: Implement in db/connection.py

# 3. Cache schema information
# TODO: Implement in db/schema.py

# 4. Use indexes on frequently queried tables
# TODO: Add schema optimization guide
```

---

## ✅ Verification Checklist

After installation, verify:

- [ ] `snapbase --version` works
- [ ] `snapbase --help` shows menu
- [ ] Can add API key without errors
- [ ] Can add database profile
- [ ] Can connect to database
- [ ] Can execute simple queries
- [ ] Results display properly
- [ ] `exit` command works

---

**Last Updated:** December 24, 2025  
**SnapBase Version:** 1.0.0

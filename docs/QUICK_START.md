# Quick Start Guide - AI Platform for FinTech Evolution

**Get up and running in under 30 minutes!** This guide will walk you through setting up your local development environment on macOS, Windows, or Linux.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Platform-Specific Setup](#platform-specific-setup)
3. [Clone and Configure](#clone-and-configure)
4. [Environment Setup](#environment-setup)
5. [Start Development Servers](#start-development-servers)
6. [Verify Installation](#verify-installation)
7. [Common Issues](#common-issues)
8. [Next Steps](#next-steps)

---

## ✅ Prerequisites

### Required Software

| **Tool** | **Version** | **Purpose** |
|---------|------------|------------|
| **Git** | 2.40+ | Version control |
| **Node.js** | 18+ LTS | Frontend runtime |
| **npm** | 9+ | Package manager |
| **Java JDK** | 17+ | Backend runtime |
| **Maven** | 3.9+ | Build tool (or use wrapper) |
| **Docker Desktop** | 4.20+ | Containerization |

### Optional Software

| **Tool** | **Purpose** |
|---------|-----------|
| **VS Code** | IDE with extensions |
| **IntelliJ IDEA** | Alternative IDE |
| **Postman** | API testing |
| **Azure CLI** | Cloud deployment |

### Check Existing Installations

```bash
# Check all prerequisites at once
git --version
node --version
npm --version
java --version
mvn --version
docker --version
```

**Expected output:**
```
git version 2.40.0
v18.17.0
9.6.7
openjdk version "17.0.8"
Apache Maven 3.9.3
Docker version 24.0.5
```

---

## 🖥️ Platform-Specific Setup

Choose your operating system:

### macOS Setup

#### **1. Install Homebrew (if not installed)**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### **2. Install Prerequisites**

```bash
# Install Git
brew install git

# Install Node.js (includes npm)
brew install node@18

# Install Java
brew install openjdk@17

# Add Java to PATH (add to ~/.zshrc or ~/.bash_profile)
echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Install Maven
brew install maven

# Install Docker Desktop
brew install --cask docker
```

#### **3. Start Docker Desktop**

```bash
# Open Docker Desktop from Applications folder
open -a Docker

# Wait for Docker to fully start (check menu bar icon)
```

#### **4. Configure Git**

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@company.com"
git config --global init.defaultBranch main
```

---

### Windows Setup

#### **1. Install Package Manager (Chocolatey)**

Open PowerShell as Administrator:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

#### **2. Install Prerequisites**

```powershell
# Install Git
choco install git -y

# Install Node.js
choco install nodejs-lts -y

# Install Java
choco install openjdk17 -y

# Install Maven
choco install maven -y

# Install Docker Desktop
choco install docker-desktop -y
```

#### **3. Restart Your Terminal**

Close and reopen PowerShell to load new PATH variables.

#### **4. Start Docker Desktop**

- Launch Docker Desktop from Start Menu
- Wait for Docker Engine to start (check system tray icon)

#### **5. Configure Git**

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@company.com"
git config --global init.defaultBranch main
git config --global core.autocrlf true
```

---

### Linux Setup (Ubuntu/Debian)

#### **1. Update Package Manager**

```bash
sudo apt update && sudo apt upgrade -y
```

#### **2. Install Prerequisites**

```bash
# Install Git
sudo apt install git -y

# Install Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Install Java 17
sudo apt install openjdk-17-jdk -y

# Verify Java installation
java --version
echo 'export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64' >> ~/.bashrc
source ~/.bashrc

# Install Maven
sudo apt install maven -y

# Install Docker
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io -y

# Add user to docker group (logout/login required)
sudo usermod -aG docker $USER
```

#### **3. Start Docker**

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

#### **4. Configure Git**

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@company.com"
git config --global init.defaultBranch main
```

---

## 📦 Clone and Configure

### 1. Clone Repository

```bash
# Navigate to your workspace directory
cd ~/workspace  # or C:\workspace on Windows

# Clone the repository
git clone https://github.com/calvinlee999/AI-Platform-for-FinTech-Evolution.git
cd AI-Platform-for-FinTech-Evolution
```

### 2. Verify Repository Structure

```bash
# List main directories
ls -la

# Expected output:
# backend/          - Java Spring Boot microservices
# frontend/         - Next.js React application
# infrastructure/   - Azure infrastructure as code
# docs/            - Documentation
# scripts/         - Automation scripts
```

---

## ⚙️ Environment Setup

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (this may take 5-10 minutes)
npm install

# Copy environment template
cp .env.example .env.local

# Edit .env.local with your settings
# For local development, defaults are usually fine
```

**Frontend .env.local Configuration:**

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8080
NEXT_PUBLIC_API_TIMEOUT=30000

# Azure AD (optional for local dev)
NEXT_PUBLIC_AZURE_AD_CLIENT_ID=your-client-id
NEXT_PUBLIC_AZURE_AD_TENANT_ID=your-tenant-id

# Feature Flags
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_CHATBOT=true

# Environment
NEXT_PUBLIC_ENV=development
```

### Backend Setup

```bash
# Navigate to backend directory
cd ../backend

# Install dependencies using Maven wrapper
./mvnw clean install -DskipTests

# On Windows, use:
# mvnw.cmd clean install -DskipTests

# Copy application properties template
cp src/main/resources/application.properties.example src/main/resources/application-local.properties
```

**Backend application-local.properties Configuration:**

```properties
# Server Configuration
server.port=8080
spring.application.name=ai-platform-backend

# Database Configuration (H2 for local dev)
spring.datasource.url=jdbc:h2:mem:testdb
spring.datasource.driverClassName=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
spring.h2.console.enabled=true
spring.h2.console.path=/h2-console

# Redis Configuration (optional for local dev)
spring.redis.host=localhost
spring.redis.port=6379

# Security Configuration
jwt.secret=local-development-secret-key-change-in-production
jwt.expiration=86400000

# Logging
logging.level.root=INFO
logging.level.com.company.banking=DEBUG
```

### Docker Services Setup

```bash
# Start supporting services (Redis, PostgreSQL, etc.)
# From project root directory
docker-compose up -d

# Verify services are running
docker ps

# Expected output:
# CONTAINER ID   IMAGE          STATUS
# abc123def456   redis:7        Up 2 minutes
# ghi789jkl012   postgres:15    Up 2 minutes
```

---

## 🚀 Start Development Servers

### Option 1: Use VS Code Tasks (Recommended)

1. Open VS Code: `code .`
2. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
3. Type "Tasks: Run Task"
4. Select **"Start Full Stack"**

This will start both backend and frontend servers in parallel.

### Option 2: Manual Start (Two Terminals)

#### **Terminal 1: Start Backend**

```bash
cd backend

# Run Spring Boot application
./mvnw spring-boot:run -Dspring-boot.run.profiles=local

# On Windows:
# mvnw.cmd spring-boot:run -Dspring-boot.run.profiles=local

# Expected output:
# Started BankingApplication in X.XXX seconds
# Tomcat started on port(s): 8080 (http)
```

#### **Terminal 2: Start Frontend**

```bash
cd frontend

# Run Next.js development server
npm run dev

# Expected output:
# ▲ Next.js 13.4.19
# - Local:        http://localhost:3000
# - Network:      http://192.168.x.x:3000
# ✓ Ready in X.Xs
```

---

## ✅ Verify Installation

### 1. Check Backend Health

```bash
# Health check endpoint
curl http://localhost:8080/actuator/health

# Expected output:
# {"status":"UP"}

# API docs (Swagger UI)
# Open in browser: http://localhost:8080/swagger-ui.html
```

### 2. Check Frontend

```bash
# Open in browser
open http://localhost:3000  # macOS
start http://localhost:3000  # Windows
xdg-open http://localhost:3000  # Linux

# Expected: AI Platform landing page loads
```

### 3. Run Tests

#### **Backend Tests**

```bash
cd backend
./mvnw test

# Expected output:
# Tests run: XX, Failures: 0, Errors: 0, Skipped: 0
# BUILD SUCCESS
```

#### **Frontend Tests**

```bash
cd frontend
npm test

# Press 'a' to run all tests
# Expected: All tests pass
```

### 4. Check Database

```bash
# H2 Console (for local development)
# Open in browser: http://localhost:8080/h2-console

# Connection settings:
# JDBC URL: jdbc:h2:mem:testdb
# User Name: sa
# Password: (leave empty)
```

### 5. Check Docker Services

```bash
# List running containers
docker ps

# Check Redis
docker exec -it ai-platform-redis redis-cli ping
# Expected: PONG

# Check logs
docker logs ai-platform-redis
docker logs ai-platform-postgres
```

---

## 🐛 Common Issues

### Issue 1: Port Already in Use

**Problem:** `Port 8080 is already in use`

**Solution:**

```bash
# Find process using port 8080
# macOS/Linux:
lsof -i :8080
kill -9 <PID>

# Windows:
netstat -ano | findstr :8080
taskkill /PID <PID> /F

# Or use different port
./mvnw spring-boot:run -Dserver.port=8081
```

### Issue 2: npm Install Fails

**Problem:** `EACCES: permission denied` or `checkPermissions missing write access`

**Solution:**

```bash
# macOS/Linux - Fix npm permissions
sudo chown -R $USER:$GROUP ~/.npm
sudo chown -R $USER:$GROUP ~/.config

# Clear npm cache
npm cache clean --force

# Try install again
npm install
```

### Issue 3: Java Version Mismatch

**Problem:** `Unsupported class file major version`

**Solution:**

```bash
# Check Java version
java --version

# Set JAVA_HOME (macOS)
export JAVA_HOME=$(/usr/libexec/java_home -v 17)

# Set JAVA_HOME (Linux)
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Set JAVA_HOME (Windows - PowerShell)
$env:JAVA_HOME = "C:\Program Files\Java\jdk-17"

# Verify
echo $JAVA_HOME
```

### Issue 4: Docker Not Starting

**Problem:** `Cannot connect to the Docker daemon`

**Solution:**

```bash
# macOS: Start Docker Desktop from Applications
open -a Docker

# Linux: Start Docker service
sudo systemctl start docker
sudo systemctl status docker

# Windows: Start Docker Desktop from Start Menu
# Right-click system tray icon > "Start Docker Desktop"

# Verify Docker is running
docker ps
```

### Issue 5: Maven Wrapper Permission Denied

**Problem:** `Permission denied: ./mvnw`

**Solution:**

```bash
# macOS/Linux - Add execute permission
chmod +x mvnw

# Verify
ls -la mvnw
# Should show: -rwxr-xr-x (executable)
```

### Issue 6: Frontend Build Errors

**Problem:** `Module not found` or `Cannot find module`

**Solution:**

```bash
# Remove node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Clear npm cache
npm cache clean --force

# Reinstall dependencies
npm install

# If still fails, try legacy peer deps
npm install --legacy-peer-deps
```

### Issue 7: Database Connection Failed

**Problem:** `Could not open JDBC Connection for transaction`

**Solution:**

```bash
# Check if PostgreSQL container is running
docker ps | grep postgres

# Restart PostgreSQL container
docker restart ai-platform-postgres

# Check logs
docker logs ai-platform-postgres

# Verify connection settings in application-local.properties
# spring.datasource.url=jdbc:postgresql://localhost:5432/banking
# spring.datasource.username=postgres
# spring.datasource.password=postgres
```

### Issue 8: Hot Reload Not Working

**Problem:** Frontend changes not reflecting

**Solution:**

```bash
# Stop development server (Ctrl+C)
# Clear Next.js cache
rm -rf .next

# Restart server
npm run dev

# For backend hot reload issues:
# Ensure you're using Spring Boot DevTools
# Check pom.xml for:
# <dependency>
#   <groupId>org.springframework.boot</groupId>
#   <artifactId>spring-boot-devtools</artifactId>
# </dependency>
```

---

## 📚 Next Steps

### 1. Explore the Codebase

```bash
# Backend structure
backend/
  src/main/java/com/company/banking/
    accounts/          # Account management service
    transactions/      # Transaction processing
    payments/         # Payment gateway integration
    security/         # Security configuration

# Frontend structure
frontend/
  src/
    app/              # Next.js app directory
    components/       # Reusable React components
    lib/             # Utility functions
    styles/          # Global styles
```

### 2. Review Documentation

- **[Technical Design](TECHNICAL_DESIGN.md)** - Architecture and design patterns
- **[Contributing Guide](../CONTRIBUTING.md)** - Development workflow
- **[API Documentation](http://localhost:8080/swagger-ui.html)** - REST API reference
- **[Debugging Guide](DEBUGGING_GUIDE.md)** - Troubleshooting tips

### 3. Make Your First Contribution

```bash
# Create a feature branch
git checkout -b feature/JIRA-123-my-first-feature

# Make some changes
# Write tests
# Commit changes
git add .
git commit -m "feat: add my first feature"

# Push and create PR
git push origin feature/JIRA-123-my-first-feature
```

### 4. Join the Community

- **Slack:** #ai-platform-dev
- **GitHub Discussions:** Ask questions, share ideas
- **Office Hours:** Tuesdays 2-3pm PT
- **Team Wiki:** Confluence space

### 5. Setup IDE Extensions (Optional)

#### **VS Code Extensions:**

```bash
# Install recommended extensions
code --install-extension dbaeumer.vscode-eslint
code --install-extension esbenp.prettier-vscode
code --install-extension vscjava.vscode-java-pack
code --install-extension ms-azuretools.vscode-docker
code --install-extension github.copilot
```

#### **IntelliJ IDEA Plugins:**

- Lombok Plugin
- Spring Boot Assistant
- Azure Toolkit
- Docker Integration

---

## 🆘 Getting Help

### Support Channels

1. **Quick Questions:** Slack #ai-platform-dev
2. **Bug Reports:** GitHub Issues
3. **Feature Requests:** GitHub Discussions
4. **Onboarding Help:** dev-support@company.com

### Useful Commands Reference

```bash
# Backend
./mvnw clean install          # Full build
./mvnw test                   # Run tests
./mvnw spring-boot:run        # Start server
./mvnw clean                  # Clean build artifacts

# Frontend
npm install                   # Install dependencies
npm run dev                   # Start dev server
npm run build                 # Production build
npm test                      # Run tests
npm run lint                  # Lint code

# Docker
docker-compose up -d          # Start all services
docker-compose down           # Stop all services
docker-compose logs -f        # View logs
docker ps                     # List containers
docker exec -it <container> bash  # Enter container

# Git
git status                    # Check status
git checkout -b <branch>      # Create branch
git add .                     # Stage changes
git commit -m "message"       # Commit changes
git push origin <branch>      # Push to remote
git pull upstream develop     # Pull latest changes
```

---

## ✅ Checklist

Track your setup progress:

- [ ] All prerequisites installed and verified
- [ ] Repository cloned successfully
- [ ] Frontend dependencies installed
- [ ] Backend dependencies installed
- [ ] Environment files configured
- [ ] Docker services running
- [ ] Backend server starts successfully
- [ ] Frontend server starts successfully
- [ ] All tests passing
- [ ] Can access Swagger UI (http://localhost:8080/swagger-ui.html)
- [ ] Can access Frontend (http://localhost:3000)
- [ ] IDE setup complete (optional)
- [ ] Joined Slack channels
- [ ] Read Contributing Guide
- [ ] Created first feature branch

---

**Congratulations!** 🎉 You're ready to start developing on the AI Platform!

**Questions?** Reach out on Slack #ai-platform-dev or email dev-support@company.com

---

**Version:** 1.0.0 | **Last Updated:** October 2, 2025 | **Status:** Active ✅

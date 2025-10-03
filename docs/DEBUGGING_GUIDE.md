# Debugging Guide - AI Platform for FinTech Evolution

**Master debugging techniques for rapid problem resolution.** This guide covers common debugging scenarios, tools, and best practices for both frontend and backend development.

---

## 📋 Table of Contents

1. [General Debugging Approach](#general-debugging-approach)
2. [Backend Debugging (Java/Spring Boot)](#backend-debugging-javaspring-boot)
3. [Frontend Debugging (React/Next.js)](#frontend-debugging-reactnextjs)
4. [Database Debugging](#database-debugging)
5. [API Debugging](#api-debugging)
6. [Docker & Container Debugging](#docker--container-debugging)
7. [Performance Debugging](#performance-debugging)
8. [Common Error Scenarios](#common-error-scenarios)
9. [Debugging Tools Reference](#debugging-tools-reference)

---

## 🔍 General Debugging Approach

### The 5-Step Debugging Process

1. **Reproduce** - Confirm you can consistently reproduce the issue
2. **Isolate** - Narrow down the scope (which component/layer/service)
3. **Investigate** - Use logs, debuggers, and tools to understand root cause
4. **Fix** - Implement the solution
5. **Verify** - Confirm fix works and doesn't introduce regressions

### Debugging Mindset

✅ **DO:**
- Read error messages carefully (they usually tell you what's wrong)
- Check logs systematically (backend → database → external services)
- Use scientific method (hypothesis → test → refine)
- Take breaks if stuck (fresh perspective helps)
- Ask for help after 30 minutes of no progress

❌ **DON'T:**
- Make random changes hoping something works
- Skip reading error messages
- Debug in production (use staging/local environments)
- Change multiple things at once
- Give up without documenting what you tried

---

## 🛠️ Backend Debugging (Java/Spring Boot)

### Enable Debug Logging

#### **application-local.properties**

```properties
# Root logging level
logging.level.root=INFO

# Application-specific logging
logging.level.com.company.banking=DEBUG

# Spring framework logging
logging.level.org.springframework.web=DEBUG
logging.level.org.springframework.security=DEBUG

# SQL logging (see queries)
logging.level.org.hibernate.SQL=DEBUG
logging.level.org.hibernate.type.descriptor.sql.BasicBinder=TRACE

# Transaction logging
logging.level.org.springframework.transaction=DEBUG
logging.level.org.springframework.orm.jpa=DEBUG

# Log file output
logging.file.name=logs/application.log
logging.pattern.console=%d{yyyy-MM-dd HH:mm:ss} - %msg%n
```

### IntelliJ IDEA Remote Debugging

#### **1. Configure IntelliJ for Remote Debug**

1. Run → Edit Configurations → Add New → Remote JVM Debug
2. Name: `AI Platform Backend Debug`
3. Host: `localhost`
4. Port: `5005`
5. Module: `backend`
6. Click Apply

#### **2. Start Backend with Debug Port**

```bash
cd backend

# Start with debug enabled
./mvnw spring-boot:run -Dspring-boot.run.jvmArguments="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005"

# Or use environment variable
export MAVEN_OPTS="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005"
./mvnw spring-boot:run
```

#### **3. Attach Debugger in IntelliJ**

1. Set breakpoints in your code (click in gutter)
2. Run → Debug 'AI Platform Backend Debug'
3. Make API request to trigger breakpoint
4. Inspect variables, step through code

### VS Code Remote Debugging

#### **launch.json Configuration**

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "java",
      "name": "Debug Spring Boot",
      "request": "attach",
      "hostName": "localhost",
      "port": 5005,
      "projectName": "backend"
    }
  ]
}
```

### Common Backend Debugging Scenarios

#### **Scenario 1: NullPointerException**

**Error:**
```
java.lang.NullPointerException: Cannot invoke "String.length()" because "this.customerId" is null
```

**Debug Steps:**

1. **Check stack trace** - Identifies exact line
2. **Inspect object state** - Use debugger to see field values
3. **Trace backwards** - Where should this value come from?
4. **Add null checks** - Defensive programming

**Solution:**

```java
// ❌ BAD: No null check
public void processAccount(Account account) {
    String customerId = account.getCustomerId();
    int length = customerId.length(); // NullPointerException if customerId is null
}

// ✅ GOOD: Defensive null checks
public void processAccount(Account account) {
    if (account == null) {
        throw new IllegalArgumentException("Account cannot be null");
    }
    
    String customerId = account.getCustomerId();
    if (customerId == null || customerId.isEmpty()) {
        throw new ValidationException("Customer ID is required");
    }
    
    int length = customerId.length(); // Safe
}

// ✅ BETTER: Use Optional
public void processAccount(Account account) {
    String customerId = Optional.ofNullable(account)
        .map(Account::getCustomerId)
        .orElseThrow(() -> new ValidationException("Customer ID is required"));
    
    int length = customerId.length();
}
```

#### **Scenario 2: Database Connection Issues**

**Error:**
```
HikariPool-1 - Exception during pool initialization.
java.net.ConnectException: Connection refused
```

**Debug Steps:**

```bash
# 1. Check if database is running
docker ps | grep postgres

# 2. Test connection manually
psql -h localhost -p 5432 -U postgres -d banking

# 3. Verify connection properties
cat backend/src/main/resources/application-local.properties | grep datasource

# 4. Check database logs
docker logs ai-platform-postgres

# 5. Restart database if needed
docker restart ai-platform-postgres
```

**Common Causes:**
- Database container not running
- Wrong port (5432 vs 5433)
- Wrong credentials
- Database not initialized
- Network issues

#### **Scenario 3: Transaction Rollback**

**Error:**
```
Transaction silently rolled back because it has been marked as rollback-only
```

**Debug Steps:**

1. **Enable transaction logging:**
```properties
logging.level.org.springframework.transaction=DEBUG
logging.level.org.springframework.orm.jpa=DEBUG
```

2. **Check for nested @Transactional annotations:**
```java
// ❌ BAD: Inner transaction marked rollback-only
@Transactional
public void outerMethod() {
    try {
        innerMethod(); // Throws exception
    } catch (Exception e) {
        // Outer tries to continue but transaction is marked rollback-only
    }
}

@Transactional
public void innerMethod() {
    // Some code that throws exception
}

// ✅ GOOD: Proper propagation
@Transactional
public void outerMethod() {
    try {
        innerMethod();
    } catch (Exception e) {
        // Handle or rethrow
        throw e;
    }
}

@Transactional(propagation = Propagation.REQUIRES_NEW)
public void innerMethod() {
    // Runs in separate transaction
}
```

#### **Scenario 4: Slow Query Performance**

**Debug Steps:**

```properties
# 1. Enable SQL logging with timing
logging.level.org.hibernate.SQL=DEBUG
logging.level.org.hibernate.stat=DEBUG
spring.jpa.properties.hibernate.generate_statistics=true

# 2. Log slow queries (> 1 second)
spring.jpa.properties.hibernate.session.events.log.LOG_QUERIES_SLOWER_THAN_MS=1000
```

**Use Explain Plan:**

```java
// In your repository test or debugging session
@Query(value = "EXPLAIN ANALYZE SELECT * FROM accounts WHERE customer_id = ?1", nativeQuery = true)
List<Object[]> explainAccountQuery(String customerId);
```

**Common Solutions:**
- Add missing indexes
- Use pagination for large result sets
- Optimize JOIN queries
- Use projections instead of full entities
- Cache frequently accessed data

---

## 🌐 Frontend Debugging (React/Next.js)

### Browser DevTools

#### **Chrome DevTools Shortcuts**

| **Action** | **Mac** | **Windows** |
|-----------|---------|------------|
| Open DevTools | `Cmd+Option+I` | `Ctrl+Shift+I` |
| Console | `Cmd+Option+J` | `Ctrl+Shift+J` |
| Network Tab | `Cmd+Option+N` | `Ctrl+Shift+N` |
| Performance | `Cmd+Shift+E` | `Ctrl+Shift+E` |
| Elements | `Cmd+Shift+C` | `Ctrl+Shift+C` |

#### **Console Debugging Techniques**

```typescript
// 1. Basic console logging
console.log('Account data:', account);

// 2. Structured logging
console.table(accounts); // Display array as table

// 3. Conditional logging
console.assert(account.balance >= 0, 'Balance should not be negative');

// 4. Performance timing
console.time('fetchAccounts');
await fetchAccounts();
console.timeEnd('fetchAccounts'); // Logs: fetchAccounts: 234.56ms

// 5. Stack trace
console.trace('How did we get here?');

// 6. Grouped logs
console.group('Account Processing');
console.log('Step 1: Validate');
console.log('Step 2: Process');
console.groupEnd();
```

### VS Code Debugging for Next.js

#### **.vscode/launch.json**

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "Next.js: Chrome",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}/frontend",
      "sourceMapPathOverrides": {
        "webpack://_N_E/*": "${webRoot}/*"
      }
    },
    {
      "type": "node",
      "request": "launch",
      "name": "Next.js: Node",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "cwd": "${workspaceFolder}/frontend",
      "skipFiles": ["<node_internals>/**"],
      "env": {
        "NODE_OPTIONS": "--inspect"
      }
    }
  ]
}
```

### Common Frontend Debugging Scenarios

#### **Scenario 1: Component Not Re-rendering**

**Problem:** Component doesn't update when state changes

**Debug Steps:**

```typescript
// 1. Check if state is actually changing
useEffect(() => {
  console.log('Account state changed:', account);
}, [account]);

// 2. Verify you're updating state correctly
// ❌ BAD: Mutating state directly
const handleUpdate = () => {
  account.balance = 1000; // Direct mutation
  setAccount(account); // React won't detect change
};

// ✅ GOOD: Creating new state object
const handleUpdate = () => {
  setAccount({ ...account, balance: 1000 });
};

// 3. Check for reference equality issues
// ❌ BAD: Array/object comparison
useEffect(() => {
  // This runs every render if accounts is recreated
}, [accounts]);

// ✅ GOOD: Use deep comparison or primitive dependencies
import { useMemo } from 'react';
const accountIds = useMemo(() => 
  accounts.map(a => a.id).join(','), 
  [accounts]
);
useEffect(() => {
  // Only runs when account IDs actually change
}, [accountIds]);
```

#### **Scenario 2: API Call Failures**

**Debug Steps:**

```typescript
// 1. Check Network tab in DevTools
// - Status code (200, 404, 500, etc.)
// - Request headers (Authorization token present?)
// - Request payload (correct data sent?)
// - Response body (error message?)

// 2. Add comprehensive error logging
const fetchAccount = async (accountId: string) => {
  try {
    console.log('[API] Fetching account:', accountId);
    
    const response = await fetch(`/api/accounts/${accountId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });
    
    console.log('[API] Response status:', response.status);
    console.log('[API] Response headers:', Object.fromEntries(response.headers));
    
    if (!response.ok) {
      const errorBody = await response.text();
      console.error('[API] Error response:', errorBody);
      throw new Error(`API error: ${response.status} - ${errorBody}`);
    }
    
    const data = await response.json();
    console.log('[API] Success:', data);
    return data;
    
  } catch (error) {
    console.error('[API] Exception:', error);
    console.error('[API] Error stack:', (error as Error).stack);
    throw error;
  }
};

// 3. Use React Query for better debugging
import { useQuery } from '@tanstack/react-query';

const { data, error, isLoading } = useQuery({
  queryKey: ['account', accountId],
  queryFn: () => fetchAccount(accountId),
  onSuccess: (data) => console.log('Query success:', data),
  onError: (error) => console.error('Query error:', error),
});

// React Query DevTools shows all query states
```

#### **Scenario 3: Infinite Loop/Too Many Re-renders**

**Error:**
```
Error: Too many re-renders. React limits the number of renders to prevent an infinite loop.
```

**Common Causes & Solutions:**

```typescript
// ❌ CAUSE 1: setState in render
const Component = () => {
  const [count, setCount] = useState(0);
  setCount(count + 1); // Called every render → infinite loop
  return <div>{count}</div>;
};

// ✅ FIX: Use useEffect or event handler
const Component = () => {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    setCount(1); // Only on mount
  }, []);
  
  return <div onClick={() => setCount(c => c + 1)}>{count}</div>;
};

// ❌ CAUSE 2: New object in dependency array
const Component = ({ config }) => {
  useEffect(() => {
    fetchData();
  }, [{ apiUrl: config.url }]); // New object every render
};

// ✅ FIX: Use primitive values or useMemo
const Component = ({ config }) => {
  const apiUrl = config.url;
  
  useEffect(() => {
    fetchData();
  }, [apiUrl]); // Primitive value
};

// ❌ CAUSE 3: Function that calls setState passed as prop
<Button onClick={setCount(count + 1)} /> // Called immediately

// ✅ FIX: Pass function reference
<Button onClick={() => setCount(count + 1)} /> // Function reference
```

#### **Scenario 4: Hydration Mismatch (Next.js)**

**Error:**
```
Warning: Text content did not match. Server: "..." Client: "..."
```

**Common Causes:**

```typescript
// ❌ PROBLEM: Client-only data in initial render
const Component = () => {
  return <div>Current time: {new Date().toLocaleString()}</div>;
  // Server renders time A, client renders time B → mismatch
};

// ✅ SOLUTION 1: Suppress hydration warning for specific content
const Component = () => {
  return (
    <div suppressHydrationWarning>
      Current time: {new Date().toLocaleString()}
    </div>
  );
};

// ✅ SOLUTION 2: Only render on client
const Component = () => {
  const [time, setTime] = useState<string>('');
  
  useEffect(() => {
    setTime(new Date().toLocaleString());
  }, []);
  
  return <div>Current time: {time || 'Loading...'}</div>;
};

// ✅ SOLUTION 3: Use dynamic import with ssr: false
import dynamic from 'next/dynamic';

const ClientOnlyComponent = dynamic(
  () => import('./ClientOnlyComponent'),
  { ssr: false }
);
```

---

## 🗄️ Database Debugging

### PostgreSQL Debugging

#### **Access Database**

```bash
# Connect to PostgreSQL in Docker
docker exec -it ai-platform-postgres psql -U postgres -d banking

# Common commands
\l              # List databases
\c banking      # Connect to database
\dt             # List tables
\d accounts     # Describe table
\q              # Quit
```

#### **Check Active Connections**

```sql
-- View active connections
SELECT pid, usename, application_name, client_addr, state, query
FROM pg_stat_activity
WHERE datname = 'banking';

-- Kill a connection
SELECT pg_terminate_backend(12345);  -- Replace with actual PID
```

#### **Analyze Slow Queries**

```sql
-- Enable query logging
ALTER SYSTEM SET log_min_duration_statement = 1000;  -- Log queries > 1 second
SELECT pg_reload_conf();

-- View slow queries
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Check table statistics
SELECT schemaname, tablename, seq_scan, idx_scan, n_tup_ins, n_tup_upd, n_tup_del
FROM pg_stat_user_tables
WHERE schemaname = 'public';

-- Find missing indexes
SELECT schemaname, tablename, attname, n_distinct, correlation
FROM pg_stats
WHERE schemaname = 'public' AND n_distinct > 100;
```

### H2 Console (Local Development)

**Access:** http://localhost:8080/h2-console

**Connection Settings:**
```
JDBC URL: jdbc:h2:mem:testdb
User Name: sa
Password: (empty)
```

**Common Queries:**

```sql
-- View all tables
SHOW TABLES;

-- Check table structure
SHOW COLUMNS FROM accounts;

-- View recent transactions
SELECT * FROM transactions ORDER BY created_at DESC LIMIT 10;

-- Check for orphaned records
SELECT t.* FROM transactions t
LEFT JOIN accounts a ON t.account_id = a.id
WHERE a.id IS NULL;
```

---

## 🔌 API Debugging

### Postman/Thunder Client

#### **Setup Environment Variables**

```json
{
  "name": "Local Development",
  "values": [
    { "key": "base_url", "value": "http://localhost:8080" },
    { "key": "access_token", "value": "your-jwt-token" }
  ]
}
```

#### **Test API Endpoints**

```bash
# Get access token
POST {{base_url}}/api/auth/login
Content-Type: application/json

{
  "username": "admin@company.com",
  "password": "password"
}

# Use token in subsequent requests
GET {{base_url}}/api/accounts
Authorization: Bearer {{access_token}}
```

### curl Commands

```bash
# Simple GET request
curl -X GET http://localhost:8080/api/accounts \
  -H "Authorization: Bearer <token>"

# POST request with JSON body
curl -X POST http://localhost:8080/api/accounts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "customerId": "customer-123",
    "accountType": "CHECKING",
    "currency": "USD"
  }'

# Verbose output (shows request/response headers)
curl -v -X GET http://localhost:8080/api/accounts

# Save response to file
curl -X GET http://localhost:8080/api/accounts > response.json
```

---

## 🐳 Docker & Container Debugging

### View Container Logs

```bash
# View logs (last 100 lines)
docker logs --tail 100 ai-platform-backend

# Follow logs in real-time
docker logs -f ai-platform-backend

# View logs with timestamps
docker logs -t ai-platform-backend

# View logs for specific time range
docker logs --since 2024-10-02T10:00:00 ai-platform-backend
```

### Access Container Shell

```bash
# Enter running container
docker exec -it ai-platform-backend bash

# Run command in container
docker exec ai-platform-backend cat /app/logs/application.log

# Check environment variables
docker exec ai-platform-backend env
```

### Inspect Container

```bash
# View container details
docker inspect ai-platform-backend

# Check resource usage
docker stats ai-platform-backend

# View container processes
docker top ai-platform-backend
```

### Network Debugging

```bash
# List Docker networks
docker network ls

# Inspect network
docker network inspect ai-platform-network

# Test connectivity between containers
docker exec ai-platform-backend ping ai-platform-postgres

# Check open ports
docker exec ai-platform-backend netstat -tulpn
```

---

## ⚡ Performance Debugging

### Backend Performance Profiling

#### **VisualVM / JProfiler**

```bash
# Enable JMX monitoring
export MAVEN_OPTS="-Dcom.sun.management.jmxremote \
  -Dcom.sun.management.jmxremote.port=9010 \
  -Dcom.sun.management.jmxremote.local.only=false \
  -Dcom.sun.management.jmxremote.authenticate=false \
  -Dcom.sun.management.jmxremote.ssl=false"

./mvnw spring-boot:run

# Connect VisualVM to localhost:9010
```

#### **Spring Boot Actuator Metrics**

```bash
# Enable metrics endpoint (application.properties)
management.endpoints.web.exposure.include=health,metrics,prometheus
management.endpoint.metrics.enabled=true

# View metrics
curl http://localhost:8080/actuator/metrics
curl http://localhost:8080/actuator/metrics/jvm.memory.used
curl http://localhost:8080/actuator/metrics/http.server.requests
```

### Frontend Performance Profiling

#### **React DevTools Profiler**

1. Install React DevTools browser extension
2. Open DevTools → Profiler tab
3. Click "Record" → Interact with app → Stop recording
4. Analyze component render times and frequency

#### **Chrome Performance Tab**

1. Open DevTools → Performance tab
2. Click "Record" → Perform actions → Stop
3. Analyze:
   - Main thread activity
   - JavaScript execution time
   - Rendering/painting time
   - Network requests

#### **Lighthouse Audit**

```bash
# Run Lighthouse audit
npx lighthouse http://localhost:3000 --view

# Focus on performance
npx lighthouse http://localhost:3000 --only-categories=performance --view
```

---

## 🚨 Common Error Scenarios

### Error: CORS Policy Block

**Error:**
```
Access to fetch at 'http://localhost:8080/api/accounts' from origin 'http://localhost:3000' 
has been blocked by CORS policy
```

**Solution:**

```java
// Backend: Configure CORS in SecurityConfig
@Bean
public CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration configuration = new CorsConfiguration();
    configuration.setAllowedOrigins(Arrays.asList("http://localhost:3000"));
    configuration.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE", "OPTIONS"));
    configuration.setAllowedHeaders(Arrays.asList("*"));
    configuration.setAllowCredentials(true);
    
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/**", configuration);
    return source;
}
```

### Error: 401 Unauthorized

**Common Causes:**
1. Missing/invalid JWT token
2. Expired token
3. Incorrect Authorization header format
4. Token not sent from frontend

**Debug:**

```typescript
// Frontend: Check token is being sent
const fetchWithAuth = async (url: string) => {
  const token = localStorage.getItem('access_token');
  console.log('Using token:', token ? 'Present' : 'Missing');
  
  const response = await fetch(url, {
    headers: {
      'Authorization': `Bearer ${token}`  // Ensure "Bearer " prefix
    }
  });
  
  if (response.status === 401) {
    console.error('Unauthorized - token may be invalid or expired');
    // Redirect to login
  }
};

// Backend: Add debug logging to SecurityFilter
logger.debug("Authorization header: {}", authHeader);
logger.debug("Token: {}", token);
logger.debug("Token valid: {}", jwtUtils.validateToken(token));
```

---

## 🧰 Debugging Tools Reference

### Essential Tools

| **Tool** | **Purpose** | **Platform** |
|---------|-----------|------------|
| Chrome DevTools | Browser debugging, network analysis | Web |
| React DevTools | React component inspection, profiler | Web |
| IntelliJ IDEA | Java debugging, profiling | Backend |
| VS Code Debugger | Multi-language debugging | All |
| Postman | API testing | All |
| Docker Desktop | Container management | All |
| pgAdmin | PostgreSQL GUI | Database |
| Redis Commander | Redis GUI | Cache |
| VisualVM | JVM monitoring | Backend |
| Lighthouse | Performance auditing | Web |

### Logging Libraries

**Backend:**
- SLF4J + Logback (default)
- Spring Boot Actuator (metrics)

**Frontend:**
- console.log (basic)
- React Query DevTools (query state)
- Redux DevTools (state management)

---

**Need more help?** Check [QUICK_START.md](QUICK_START.md) or reach out on Slack #ai-platform-dev 🚀

---

**Version:** 1.0.0 | **Last Updated:** October 2, 2025 | **Status:** Active ✅

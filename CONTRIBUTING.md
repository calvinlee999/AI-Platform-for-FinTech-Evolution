# Contributing to AI Platform for FinTech Evolution

**Welcome!** Thank you for considering contributing to the AI Platform project. This guide will help you understand our development workflow, coding standards, and contribution process.

---

## 📋 Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Testing Requirements](#testing-requirements)
6. [Pull Request Process](#pull-request-process)
7. [Review Guidelines](#review-guidelines)
8. [Documentation Standards](#documentation-standards)

---

## 🤝 Code of Conduct

###Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of background or experience level.

### Expected Behavior

- ✅ Be respectful and professional
- ✅ Provide constructive feedback
- ✅ Accept constructive criticism gracefully
- ✅ Focus on what is best for the project
- ✅ Show empathy towards other contributors

### Unacceptable Behavior

- ❌ Harassment or discriminatory language
- ❌ Personal attacks or trolling
- ❌ Publishing others' private information
- ❌ Unprofessional or disruptive conduct

**Violations:** Report to project maintainers at [conduct@company.com]

---

## 🚀 Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Development Environment:**
  - Git 2.40+
  - Node.js 18+ and npm 9+
  - Java 17+ and Maven 3.9+
  - Docker Desktop 4.20+
  - IDE: VS Code with recommended extensions OR IntelliJ IDEA Ultimate

- **Access:**
  - GitHub account with repository access
  - Azure DevOps account (for CI/CD)
  - Company VPN access (if applicable)

### Initial Setup

```bash
# 1. Fork the repository on GitHub
# Click "Fork" button at https://github.com/calvinlee999/AI-Platform-for-FinTech-Evolution

# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/AI-Platform-for-FinTech-Evolution.git
cd AI-Platform-for-FinTech-Evolution

# 3. Add upstream remote
git remote add upstream https://github.com/calvinlee999/AI-Platform-for-FinTech-Evolution.git

# 4. Install frontend dependencies
cd frontend
npm install

# 5. Install backend dependencies
cd ../backend
./mvnw clean install

# 6. Setup environment variables
cp .env.example .env.local
# Edit .env.local with your local configuration

# 7. Start development environment
# See docs/QUICK_START.md for detailed instructions
```

### Verify Setup

```bash
# Run backend tests
cd backend
./mvnw test

# Run frontend tests
cd ../frontend
npm test

# Start development servers
npm run dev  # Frontend (port 3000)
cd ../backend && ./mvnw spring-boot:run  # Backend (port 8080)
```

**Expected:** All tests pass, servers start successfully

---

## 🔄 Development Workflow

### Branch Strategy

We use **Git Flow** with the following branch types:

#### **Main Branches**
- `main` - Production-ready code, protected branch
- `develop` - Integration branch for features, protected branch

#### **Supporting Branches**
- `feature/*` - New features (branch from `develop`)
- `bugfix/*` - Bug fixes (branch from `develop`)
- `hotfix/*` - Critical production fixes (branch from `main`)
- `release/*` - Release preparation (branch from `develop`)

### Branch Naming Convention

```bash
feature/JIRA-123-add-account-service
bugfix/JIRA-456-fix-transaction-validation
hotfix/JIRA-789-security-patch
release/v2.1.0
```

**Format:** `<type>/<ticket>-<short-description>`

### Workflow Steps

#### 1. **Create Feature Branch**

```bash
# Ensure you're on develop and up-to-date
git checkout develop
git pull upstream develop

# Create feature branch
git checkout -b feature/JIRA-123-add-account-service
```

#### 2. **Develop Your Feature**

```bash
# Make your changes
# Write tests FIRST (TDD approach)
# Implement functionality
# Ensure all tests pass

# Commit frequently with meaningful messages
git add .
git commit -m "feat(accounts): add account creation service

- Implement AccountService with create method
- Add validation for account types
- Include unit tests with 90% coverage
- Add integration tests for API endpoint

Closes JIRA-123"
```

#### 3. **Keep Your Branch Updated**

```bash
# Regularly sync with upstream develop
git fetch upstream
git rebase upstream/develop

# Resolve any conflicts
# Run tests after rebase
```

#### 4. **Push to Your Fork**

```bash
git push origin feature/JIRA-123-add-account-service
```

#### 5. **Create Pull Request**

- Go to GitHub repository
- Click "New Pull Request"
- Select your branch
- Fill out PR template (see below)
- Request reviews from team members

---

## 📝 Coding Standards

### General Principles

1. **SOLID Principles** - Write clean, maintainable code
2. **DRY (Don't Repeat Yourself)** - Avoid code duplication
3. **KISS (Keep It Simple, Stupid)** - Prefer simplicity over cleverness
4. **YAGNI (You Aren't Gonna Need It)** - Don't over-engineer
5. **Single Responsibility** - One class/function, one purpose

### Java Backend Standards

#### **Code Style**

```java
// ✅ GOOD: Clear naming, single responsibility
@Service
public class AccountService {
    private final AccountRepository accountRepository;
    private final EventPublisher eventPublisher;
    
    public AccountService(
        AccountRepository accountRepository,
        EventPublisher eventPublisher
    ) {
        this.accountRepository = accountRepository;
        this.eventPublisher = eventPublisher;
    }
    
    @Transactional
    public Account createAccount(CreateAccountRequest request) {
        // Validate request
        validateAccountRequest(request);
        
        // Create account entity
        Account account = Account.builder()
            .customerId(request.getCustomerId())
            .accountType(request.getAccountType())
            .currency(request.getCurrency())
            .build();
        
        // Save to database
        Account savedAccount = accountRepository.save(account);
        
        // Publish event
        eventPublisher.publish(new AccountCreatedEvent(savedAccount));
        
        return savedAccount;
    }
    
    private void validateAccountRequest(CreateAccountRequest request) {
        if (request.getCustomerId() == null) {
            throw new ValidationException("Customer ID is required");
        }
        if (request.getAccountType() == null) {
            throw new ValidationException("Account type is required");
        }
    }
}
```

```java
// ❌ BAD: Poor naming, multiple responsibilities, no validation
@Service
public class AcctSvc {
    @Autowired
    private AccountRepository repo;
    
    @Autowired
    private EventPublisher pub;
    
    public Account create(CreateAccountRequest r) {
        Account a = new Account();
        a.setCustomerId(r.getCustomerId());
        a.setAccountType(r.getAccountType());
        repo.save(a);
        pub.publish(new AccountCreatedEvent(a));
        return a;
    }
}
```

#### **Formatting**
- **Indentation:** 4 spaces (no tabs)
- **Line Length:** Max 120 characters
- **Braces:** K&R style (opening brace on same line)
- **Imports:** Remove unused, organize by package

#### **Naming Conventions**
- **Classes:** PascalCase (`AccountService`, `TransactionController`)
- **Methods:** camelCase (`createAccount`, `validateTransaction`)
- **Constants:** UPPER_SNAKE_CASE (`MAX_RETRY_ATTEMPTS`, `DEFAULT_CURRENCY`)
- **Packages:** lowercase (`com.company.banking.accounts`)

### TypeScript/React Frontend Standards

#### **Code Style**

```typescript
// ✅ GOOD: Typed props, clear component structure
interface AccountListProps {
  accounts: Account[];
  onAccountClick: (accountId: string) => void;
  loading?: boolean;
}

export const AccountList: React.FC<AccountListProps> = ({
  accounts,
  onAccountClick,
  loading = false
}) => {
  if (loading) {
    return <LoadingSpinner />;
  }
  
  if (accounts.length === 0) {
    return <EmptyState message="No accounts found" />;
  }
  
  return (
    <div className="account-list">
      {accounts.map(account => (
        <AccountCard
          key={account.id}
          account={account}
          onClick={() => onAccountClick(account.id)}
        />
      ))}
    </div>
  );
};
```

```typescript
// ❌ BAD: No types, unclear logic, poor structure
export const AccountList = (props: any) => {
  return (
    <div>
      {props.loading ? <div>Loading...</div> : 
        props.accounts.length === 0 ? <div>No accounts</div> :
          props.accounts.map((a: any) => 
            <div key={a.id} onClick={() => props.onClick(a.id)}>
              {a.name}
            </div>
          )
      }
    </div>
  );
};
```

#### **Formatting**
- **Indentation:** 2 spaces
- **Line Length:** Max 100 characters
- **Semicolons:** Always use
- **Quotes:** Single quotes for strings
- **Arrow Functions:** Prefer for callbacks

#### **Naming Conventions**
- **Components:** PascalCase (`AccountList`, `TransactionCard`)
- **Functions:** camelCase (`fetchAccounts`, `handleSubmit`)
- **Constants:** UPPER_SNAKE_CASE (`API_BASE_URL`, `MAX_ITEMS`)
- **Interfaces:** PascalCase with `I` prefix optional (`AccountListProps`)

### Documentation Standards

#### **Required Comments**

```java
/**
 * Creates a new customer account with the specified parameters.
 * 
 * @param request The account creation request containing customer ID, 
 *                account type, and currency
 * @return The created account with generated ID and initial balance
 * @throws ValidationException if request parameters are invalid
 * @throws DuplicateAccountException if account already exists
 */
@Transactional
public Account createAccount(CreateAccountRequest request) {
    // Implementation
}
```

#### **When to Comment**
- ✅ Public API methods and interfaces
- ✅ Complex business logic or algorithms
- ✅ Non-obvious technical decisions
- ✅ Workarounds or temporary solutions
- ❌ Obvious code (let code be self-documenting)
- ❌ Commented-out code (use git history)

---

## 🧪 Testing Requirements

### Test Coverage Requirements

| **Test Type** | **Minimum Coverage** | **Responsibility** |
|--------------|---------------------|-------------------|
| **Unit Tests** | 85% | All developers |
| **Integration Tests** | 80% | Feature developers |
| **E2E Tests** | 90% critical paths | QA + Developers |
| **BDD Scenarios** | 100% user stories | Business analysts + Developers |

### TDD (Test-Driven Development) - MANDATORY

**All new code MUST follow TDD:**

1. **Write failing test first**
2. **Write minimal code to pass**
3. **Refactor while keeping tests green**

#### **Example: TDD Flow**

```java
// Step 1: Write failing test
@Test
void shouldCreateAccountWithValidRequest() {
    // Arrange
    CreateAccountRequest request = CreateAccountRequest.builder()
        .customerId("customer-123")
        .accountType(AccountType.CHECKING)
        .currency("USD")
        .build();
    
    // Act
    Account account = accountService.createAccount(request);
    
    // Assert
    assertThat(account).isNotNull();
    assertThat(account.getId()).isNotNull();
    assertThat(account.getCustomerId()).isEqualTo("customer-123");
    assertThat(account.getAccountType()).isEqualTo(AccountType.CHECKING);
    assertThat(account.getBalance()).isEqualTo(BigDecimal.ZERO);
}

// Step 2: Implement minimal code
public Account createAccount(CreateAccountRequest request) {
    Account account = new Account();
    account.setId(UUID.randomUUID().toString());
    account.setCustomerId(request.getCustomerId());
    account.setAccountType(request.getAccountType());
    account.setBalance(BigDecimal.ZERO);
    return accountRepository.save(account);
}

// Step 3: Refactor (while tests stay green)
public Account createAccount(CreateAccountRequest request) {
    return accountRepository.save(
        Account.builder()
            .id(UUID.randomUUID().toString())
            .customerId(request.getCustomerId())
            .accountType(request.getAccountType())
            .balance(BigDecimal.ZERO)
            .build()
    );
}
```

### Running Tests

```bash
# Backend tests
cd backend
./mvnw test                    # Run all tests
./mvnw test -Dtest=AccountServiceTest  # Run specific test
./mvnw verify                  # Run tests + integration tests

# Frontend tests
cd frontend
npm test                       # Run all tests (watch mode)
npm test -- --coverage         # Run with coverage report
npm test -- AccountList.test   # Run specific test

# E2E tests
npm run test:e2e              # Run Playwright E2E tests
```

### Test Organization

```
backend/
  src/
    test/
      java/
        com/company/banking/
          accounts/
            unit/              # Unit tests
              AccountServiceTest.java
            integration/       # Integration tests
              AccountApiTest.java
            
frontend/
  src/
    components/
      __tests__/              # Component tests
        AccountList.test.tsx
    e2e/                      # End-to-end tests
      accounts.spec.ts
```

---

## 🔍 Pull Request Process

### PR Template

When creating a PR, fill out this template:

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update

## Related Issues
Closes JIRA-123
Relates to JIRA-456

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing Done
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] E2E tests added/updated (if applicable)
- [ ] Manual testing completed
- [ ] All tests passing locally

## Test Coverage
- Unit test coverage: XX%
- Integration test coverage: XX%

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Checklist
- [ ] Code follows project coding standards
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated (if needed)
- [ ] No new warnings or errors
- [ ] Tests added and passing
- [ ] Security implications considered
- [ ] Performance implications considered

## Reviewer Notes
Any specific areas you'd like reviewers to focus on.
```

### PR Requirements

**Before submitting:**
1. ✅ All tests pass locally
2. ✅ Code coverage meets requirements (85%+ unit, 80%+ integration)
3. ✅ No linting errors
4. ✅ Documentation updated
5. ✅ Commits follow conventional commit format
6. ✅ Branch is up-to-date with develop

**PR will be auto-rejected if:**
- ❌ Tests failing in CI/CD
- ❌ Code coverage below thresholds
- ❌ Linting errors present
- ❌ Security vulnerabilities detected
- ❌ Breaking changes without approval

---

## 👀 Review Guidelines

### For Authors

**Preparing for Review:**
- Keep PRs small (< 400 lines changed)
- Provide context in PR description
- Tag specific reviewers for expertise areas
- Respond to comments within 24 hours
- Be open to feedback and suggestions

**Responding to Comments:**
- ✅ "Good catch! Fixed in commit abc123"
- ✅ "I considered that, but chose X because Y"
- ✅ "Let's discuss this offline and update here"
- ❌ "This is fine as is" (without explanation)
- ❌ Ignoring comments

### For Reviewers

**Review Checklist:**
- [ ] Code quality and readability
- [ ] Adherence to coding standards
- [ ] Test coverage and quality
- [ ] Security implications
- [ ] Performance implications
- [ ] Documentation completeness
- [ ] Error handling
- [ ] Edge cases considered

**Providing Feedback:**
- ✅ Be specific and constructive
- ✅ Explain the "why" behind suggestions
- ✅ Distinguish between blocking issues and nits
- ✅ Acknowledge good work
- ❌ Personal criticism
- ❌ Vague comments like "fix this"

**Comment Prefixes:**
- `[BLOCKING]` - Must be fixed before merge
- `[SUGGESTION]` - Consider this improvement
- `[NIT]` - Minor style/formatting issue
- `[QUESTION]` - Seeking clarification

### Approval Process

**Required Approvals:**
- 2+ team members (for features)
- 1+ senior developer (for architecture changes)
- 1+ security team (for security-related changes)
- 1+ compliance team (for compliance-related changes)

**Merge Criteria:**
- ✅ All required approvals received
- ✅ All CI/CD checks passing
- ✅ No unresolved blocking comments
- ✅ Up-to-date with target branch

---

## 📚 Documentation Standards

### Code Documentation

#### **Minimum Requirements**
- All public classes, methods, and APIs
- Complex algorithms or business logic
- Configuration and setup instructions
- API endpoint documentation

#### **Documentation Tools**
- **Backend:** JavaDoc
- **Frontend:** TSDoc
- **API:** OpenAPI/Swagger
- **Architecture:** Markdown + Mermaid diagrams

### README Updates

**When to update README:**
- New features added
- Configuration changes
- Setup process changes
- New dependencies

### Architecture Documentation

**Update docs/ when:**
- Adding new services or components
- Changing integration patterns
- Modifying data schemas
- Updating deployment processes

---

## 🐛 Bug Reports

### Creating Bug Reports

Use GitHub Issues with this template:

```markdown
## Bug Description
Clear description of the bug.

## Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. See error

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Environment
- OS: [e.g., macOS 13.0]
- Browser: [e.g., Chrome 115]
- Version: [e.g., 2.1.0]

## Screenshots
If applicable, add screenshots.

## Additional Context
Any other relevant information.
```

---

## 🎯 Feature Requests

### Proposing Features

Use GitHub Issues with `feature-request` label:

```markdown
## Feature Description
Clear description of the proposed feature.

## Business Value
Why is this feature needed? What problem does it solve?

## Proposed Solution
How would you implement this?

## Alternative Solutions
What other approaches did you consider?

## Additional Context
Any mockups, diagrams, or examples.
```

---

## 📧 Getting Help

### Support Channels

- **Slack:** #ai-platform-dev (for quick questions)
- **GitHub Discussions:** For longer discussions
- **Office Hours:** Tuesdays 2-3pm PT (Zoom link in Slack)
- **Email:** dev-support@company.com

### Escalation Path

1. Ask in Slack #ai-platform-dev
2. Create GitHub Discussion
3. Attend office hours
4. Email dev-support@company.com

---

## 🏆 Recognition

### Contributors

We recognize outstanding contributors through:
- 🌟 Monthly Contributor Awards
- 📝 Release notes mentions
- 🎁 Company swag
- 💰 Performance review recognition

### Hall of Fame

Top contributors are featured in:
- Repository README
- Team meetings
- Company blog posts
- Conference talks

---

## 📝 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to the AI Platform!** Your efforts help build a better future for FinTech development. 🚀

**Questions?** Reach out on Slack #ai-platform-dev or email dev-support@company.com

---

**Version:** 1.0.0 | **Last Updated:** October 2, 2025 | **Status:** Active ✅

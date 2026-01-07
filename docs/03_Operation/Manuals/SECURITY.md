# Security Policy

## 🔒 보안 정책 (Security Policy)

### Reporting Security Vulnerabilities (보안 취약점 보고)

If you discover a security vulnerability, please report it to:
- Email: ioas0316@gmail.com
- **DO NOT** create a public GitHub issue for security vulnerabilities

보안 취약점을 발견하면 다음으로 보고해주세요:
- 이메일: ioas0316@gmail.com
- 보안 취약점에 대해 공개 GitHub 이슈를 생성하지 **마세요**

---

## 🔑 API Key Management (API 키 관리)

### ⚠️ CRITICAL: Never Commit Secrets

**NEVER** commit the following to git:
- API keys
- Passwords
- Access tokens
- Private keys
- Database credentials

**절대** 다음을 git에 커밋하지 마세요:
- API 키
- 비밀번호
- 액세스 토큰
- 개인 키
- 데이터베이스 자격 증명

### ✅ Best Practices (모범 사례)

1. **Use Environment Variables**
   ```bash
   # Good ✅
   GEMINI_API_KEY="your_key_here"
   
   # Bad ❌ - Never hardcode in source files
   api_key = "AIzaSy..."
   ```

2. **Use .env for Local Development**
   - Copy `.env.example` to `.env`
   - Add your actual API keys to `.env`
   - `.env` is already in `.gitignore` and will not be committed

3. **Rotate Exposed Keys Immediately**
   - If you accidentally commit a key, rotate it immediately
   - Revoke the old key in the API provider dashboard
   - Generate a new key
   - Update your `.env` file

4. **Use Different Keys for Development and Production**
   - Development: Use test/sandbox keys with limited permissions
   - Production: Use production keys with strict rate limits

---

## 🛡️ Secure Coding Practices (안전한 코딩 관행)

### Input Validation (입력 검증)

Always validate and sanitize user input:

```python
# Good ✅
def process_input(user_input: str) -> str:
    # Validate input
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string")
    
    # Sanitize
    sanitized = user_input.strip()
    
    # Length check
    if len(sanitized) > 1000:
        raise ValueError("Input too long")
    
    return sanitized
```

### Error Handling (오류 처리)

Never expose sensitive information in error messages:

```python
# Good ✅
try:
    result = api.call(api_key=os.getenv("API_KEY"))
except APIError as e:
    logger.error("API call failed", exc_info=True)
    return {"error": "Service temporarily unavailable"}

# Bad ❌
except APIError as e:
    return {"error": f"API failed with key: {api_key}"}
```

### Dependency Management (의존성 관리)

1. **Keep Dependencies Updated**
   ```bash
   pip list --outdated
   pip install --upgrade package-name
   ```

2. **Use Virtual Environments**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Review Dependencies Regularly**
   - Check for known vulnerabilities
   - Remove unused dependencies
   - Pin versions in `requirements.txt`

---

## 🔍 Code Review Checklist (코드 리뷰 체크리스트)

Before committing code, verify:

- [ ] No hardcoded secrets or API keys
- [ ] No sensitive data in logs
- [ ] Input validation is present
- [ ] Error messages don't leak information
- [ ] Dependencies are up to date
- [ ] `.env` file is not committed
- [ ] SQL queries use parameterized statements (if applicable)
- [ ] File paths are validated against directory traversal

---

## 📦 Dependency Security (의존성 보안)

### Known Security Considerations

1. **AI/ML Libraries**: Some dependencies (torch, transformers) are large and should be reviewed
2. **Network Libraries**: Keep `requests`, `urllib3` updated
3. **Web Frameworks**: Keep `flask`, `fastapi` updated

### Scanning for Vulnerabilities

```bash
# Install safety
pip install safety

# Check for known vulnerabilities
safety check

# Or use pip-audit
pip install pip-audit
pip-audit
```

---

## 🚨 Incident Response (사고 대응)

If a security incident occurs:

1. **Immediate Actions**
   - Rotate all compromised credentials immediately
   - Document what happened
   - Assess the scope of the breach

2. **Notify Affected Parties**
   - Contact users if their data was exposed
   - Report to relevant authorities if required

3. **Post-Incident**
   - Conduct a security review
   - Update security procedures
   - Document lessons learned

---

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- [Google API Security Best Practices](https://cloud.google.com/docs/security)

---

*Last Updated: 2025-12-02*
*Version: 1.0*

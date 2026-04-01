# Authentication System

## How login works
1. User enters email and password
2. System verifies credentials
3. JWT token is generated
4. User gets access to protected routes

## Signup
- New users can create an account
- Password is securely hashed

## Common Issues

### Invalid credentials
- Wrong email or password

### Unauthorized error
- Token missing or expired

## Tips
- Always login again if session expires
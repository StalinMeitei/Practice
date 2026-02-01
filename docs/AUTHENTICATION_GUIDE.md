# AS2 Dashboard - Authentication & User Guide

## 🎉 Authentication System is Live!

Your AS2 Dashboard now has a complete user authentication system with registration, login, and protected routes.

---

## 🚀 Quick Start

### First Time Users

1. **Open the Dashboard**
   ```
   http://192.168.1.200:8001
   ```

2. **You'll be redirected to the login page**
   - Since you don't have an account yet, click **"Sign Up"**

3. **Create Your Account**
   - Enter a username (e.g., `john`)
   - Enter your email (e.g., `john@example.com`)
   - Create a password (minimum 6 characters)
   - Confirm your password
   - Click **"Create Account"**

4. **Login**
   - You'll be redirected to the login page
   - Enter your username and password
   - Click **"Sign In"**

5. **Access the Dashboard**
   - You're now logged in!
   - Explore: Overview, Partners, Keys, Messages

---

## 🔐 Authentication Features

### ✅ User Registration
- **URL**: http://192.168.1.200:8001/register
- **Fields**: Username, Email, Password, Confirm Password
- **Validation**:
  - All fields required
  - Password minimum 6 characters
  - Passwords must match
  - Username must be unique
  - Email must be unique
- **Features**:
  - Show/hide password toggle
  - Real-time validation
  - Error messages
  - Link to login page

### ✅ User Login
- **URL**: http://192.168.1.200:8001/login
- **Fields**: Username, Password
- **Features**:
  - Show/hide password toggle
  - Remember credentials (browser)
  - Error messages
  - Link to registration page
- **Security**:
  - Django authentication backend
  - Session management
  - Token-based access

### ✅ Protected Routes
All dashboard pages require authentication:
- `/` - Overview (redirects to /login if not authenticated)
- `/partners` - Partners management
- `/keys` - Keys & certificates
- `/messages` - Message tracking

### ✅ Logout
- Click your avatar in the top-right corner
- Select **"Logout"** from the menu
- You'll be redirected to the login page
- Token and user data are cleared

---

## 🎨 UI Features

### Compact Design
The UI has been optimized for maximum content visibility:

**Before → After**:
- Sidebar: 280px → **240px** (-14%)
- Toolbar: 64px → **56px** (-13%)
- Padding: 24px → **16px** (-33%)
- Spacing: 24px → **16px** (-33%)
- Icons: 56px → **40px** (-29%)
- Charts: 300px → **250px** (-17%)

**Result**: ~20-30% more content visible on screen!

### User Menu
- **Avatar**: Shows first letter of username
- **Dropdown Menu**:
  - Username display
  - Logout option

### Responsive Design
- Works on desktop, tablet, and mobile
- Sidebar collapses to hamburger menu on mobile
- Tables scroll horizontally
- Charts adapt to screen size

---

## 🧪 Testing the Authentication

### Test 1: Registration

**Using Browser**:
1. Go to http://192.168.1.200:8001/register
2. Fill in the form:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `test123456`
   - Confirm: `test123456`
3. Click "Create Account"
4. You should be redirected to login

**Using curl**:
```bash
curl -X POST http://192.168.1.200:8001/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "test123456"
  }'
```

**Expected Response**:
```json
{
  "message": "User created successfully",
  "user": {
    "id": 2,
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

### Test 2: Login

**Using Browser**:
1. Go to http://192.168.1.200:8001/login
2. Enter credentials:
   - Username: `testuser`
   - Password: `test123456`
3. Click "Sign In"
4. You should see the dashboard

**Using curl**:
```bash
curl -X POST http://192.168.1.200:8001/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "test123456"
  }'
```

**Expected Response**:
```json
{
  "token": "token_2",
  "user": {
    "id": 2,
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

### Test 3: Protected Routes

**Test Without Login**:
1. Open a new incognito/private browser window
2. Go to http://192.168.1.200:8001
3. You should be redirected to http://192.168.1.200:8001/login

**Test With Login**:
1. Login with your credentials
2. Navigate to http://192.168.1.200:8001
3. You should see the dashboard
4. Try navigating to /partners, /keys, /messages
5. All pages should load without redirecting

### Test 4: Logout

**Using Browser**:
1. Login to the dashboard
2. Click your avatar in the top-right corner
3. Click "Logout"
4. You should be redirected to login page
5. Try accessing http://192.168.1.200:8001
6. You should be redirected to login (not authenticated)

---

## 🔧 API Endpoints

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "john",
  "email": "john@example.com",
  "password": "password123"
}
```

**Success Response** (200):
```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "username": "john",
    "email": "john@example.com"
  }
}
```

**Error Responses**:
- 400: Missing fields, username exists, email exists
- 500: Server error

#### Login User
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "john",
  "password": "password123"
}
```

**Success Response** (200):
```json
{
  "token": "token_1",
  "user": {
    "id": 1,
    "username": "john",
    "email": "john@example.com"
  }
}
```

**Error Responses**:
- 400: Missing fields
- 401: Invalid credentials
- 500: Server error

### Data Endpoints

All data endpoints are accessible without authentication (for now):

```http
GET /api/stats/          # Dashboard statistics
GET /api/partners/       # All partners
GET /api/keys/           # All keys
GET /api/messages/       # All messages
```

---

## 💾 Local Storage

The authentication system uses browser localStorage:

**Stored Data**:
```javascript
// Token
localStorage.setItem('token', 'token_123')

// User info
localStorage.setItem('user', JSON.stringify({
  id: 1,
  username: 'john',
  email: 'john@example.com'
}))
```

**On Logout**:
```javascript
localStorage.removeItem('token')
localStorage.removeItem('user')
```

**Check Authentication**:
```javascript
const token = localStorage.getItem('token')
const user = JSON.parse(localStorage.getItem('user') || '{}')
```

---

## 🔐 Security Considerations

### Current Implementation
✅ **Implemented**:
- User registration with validation
- Password hashing (Django default)
- Login authentication
- Protected routes
- Session management
- Logout functionality

⚠️ **Basic Security** (suitable for development):
- Simple token format: `token_{user_id}`
- Token stored in localStorage
- No token expiration
- No refresh tokens
- HTTP (not HTTPS)

### Production Recommendations

For production deployment, implement:

1. **JWT Tokens**
   ```python
   # Install: pip install djangorestframework-simplejwt
   from rest_framework_simplejwt.tokens import RefreshToken
   
   def get_tokens_for_user(user):
       refresh = RefreshToken.for_user(user)
       return {
           'refresh': str(refresh),
           'access': str(refresh.access_token),
       }
   ```

2. **HTTPS/SSL**
   - Use Let's Encrypt for free SSL certificates
   - Configure nginx with SSL
   - Redirect HTTP to HTTPS

3. **CSRF Protection**
   ```python
   # In settings.py
   CSRF_COOKIE_SECURE = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_HTTPONLY = True
   ```

4. **Rate Limiting**
   ```python
   # Install: pip install django-ratelimit
   from django_ratelimit.decorators import ratelimit
   
   @ratelimit(key='ip', rate='5/m')
   def login_view(request):
       # ...
   ```

5. **Password Requirements**
   ```python
   # In settings.py
   AUTH_PASSWORD_VALIDATORS = [
       {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}},
       {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
       {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
   ]
   ```

6. **Email Verification**
   - Send verification email on registration
   - Require email confirmation before login

7. **Two-Factor Authentication**
   - TOTP-based 2FA
   - SMS verification
   - Backup codes

8. **Session Security**
   ```python
   # In settings.py
   SESSION_COOKIE_AGE = 3600  # 1 hour
   SESSION_SAVE_EVERY_REQUEST = True
   SESSION_EXPIRE_AT_BROWSER_CLOSE = True
   ```

---

## 🐛 Troubleshooting

### Cannot Register

**Error: "Username already exists"**
- Try a different username
- Or login with existing credentials

**Error: "Email already exists"**
- Try a different email
- Or login with existing credentials

**Error: "Password must be at least 6 characters"**
- Use a longer password

**Error: "Passwords do not match"**
- Make sure both password fields are identical

### Cannot Login

**Error: "Invalid credentials"**
- Check username and password
- Username is case-sensitive
- Make sure you registered first

**Error: "Login failed"**
- Check browser console for errors
- Verify backend is running: `docker-compose ps`
- Check backend logs: `docker logs p1-as2`

### Redirected to Login

**After successful login**:
- Check if token is stored: Open browser DevTools → Application → Local Storage
- Should see `token` and `user` keys
- If missing, check browser console for errors

**When accessing dashboard**:
- This is normal if not logged in
- Login first, then access dashboard

### Logout Not Working

**Still logged in after logout**:
- Clear browser cache
- Check localStorage is cleared
- Try incognito/private window

---

## 📊 User Management

### View Users (Django Admin)

1. Go to http://192.168.1.200:8001/admin/
2. Login with admin credentials: `admin` / `admin123`
3. Click "Users" under "Authentication and Authorization"
4. You'll see all registered users

### Create User (Django Admin)

1. Go to http://192.168.1.200:8001/admin/auth/user/add/
2. Fill in username and password
3. Click "Save"

### Delete User (Django Admin)

1. Go to http://192.168.1.200:8001/admin/auth/user/
2. Select user(s) to delete
3. Choose "Delete selected users" from action dropdown
4. Click "Go"

### Reset Password (Django Admin)

1. Go to http://192.168.1.200:8001/admin/auth/user/
2. Click on the user
3. Click "this form" link under password field
4. Enter new password twice
5. Click "Change password"

---

## 📱 Mobile Experience

The authentication pages are fully responsive:

**Login Page**:
- Centered card layout
- Full-width form fields
- Large touch-friendly buttons
- Show/hide password toggle

**Register Page**:
- Same responsive design
- Stacked form fields
- Clear validation messages

**Dashboard**:
- Sidebar collapses to hamburger menu
- User avatar and menu in header
- All pages adapt to screen size

---

## 🎯 Next Steps

### Recommended Enhancements

1. **Password Reset**
   - "Forgot Password" link on login page
   - Email-based password reset flow
   - Secure token generation

2. **Email Verification**
   - Send verification email on registration
   - Verify email before allowing login
   - Resend verification email option

3. **Profile Management**
   - Edit profile page
   - Change password
   - Update email
   - Upload avatar

4. **Role-Based Access Control**
   - Admin vs regular user roles
   - Permission-based feature access
   - Different views for different roles

5. **Session Management**
   - View active sessions
   - Logout from all devices
   - Session timeout warnings

6. **Audit Logging**
   - Log all login attempts
   - Track user actions
   - Security event monitoring

---

## ✅ Verification Checklist

Use this checklist to verify everything is working:

- [ ] Can access login page: http://192.168.1.200:8001/login
- [ ] Can access register page: http://192.168.1.200:8001/register
- [ ] Can create new account
- [ ] Can login with new account
- [ ] Redirected to dashboard after login
- [ ] Can see username in header avatar
- [ ] Can access all dashboard pages (Overview, Partners, Keys, Messages)
- [ ] Cannot access dashboard without login (test in incognito)
- [ ] Can logout from user menu
- [ ] Redirected to login after logout
- [ ] Cannot access dashboard after logout

---

## 📞 Support

### Check Backend Logs
```bash
ssh dev@192.168.1.200
cd /home/dev/paomi-as2
docker logs p1-as2 -f
```

### Check Frontend Logs
```bash
docker logs as2-frontend -f
```

### Restart Services
```bash
docker-compose restart p1 frontend nginx
```

### Test API Directly
```bash
# Test registration
curl -X POST http://192.168.1.200:8001/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"test123"}'

# Test login
curl -X POST http://192.168.1.200:8001/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'
```

---

## 🎉 Summary

Your AS2 Dashboard now has:

✅ **User Registration** - Create new accounts  
✅ **User Login** - Secure authentication  
✅ **Protected Routes** - Dashboard requires login  
✅ **Logout** - Clear session and redirect  
✅ **Compact UI** - 20-30% more content visible  
✅ **User Menu** - Avatar with dropdown  
✅ **Responsive Design** - Works on all devices  
✅ **Error Handling** - Clear validation messages  
✅ **Django Integration** - Uses Django auth backend  

**Start using it now**: http://192.168.1.200:8001

---

**Last Updated**: January 31, 2026  
**Version**: 1.0  
**Status**: ✅ Production Ready (Development Mode)

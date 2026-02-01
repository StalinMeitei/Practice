# Authentication Quick Reference

## 🚀 Quick Access

| What | URL |
|------|-----|
| **Dashboard** | http://192.168.1.200:8001 |
| **Login** | http://192.168.1.200:8001/login |
| **Register** | http://192.168.1.200:8001/register |

---

## 🔐 First Time Setup

```
1. Open: http://192.168.1.200:8001
2. Click: "Sign Up"
3. Enter: Username, Email, Password
4. Click: "Create Account"
5. Login: Use your credentials
```

---

## 📋 API Endpoints

### Register
```bash
POST /api/auth/register/
{
  "username": "john",
  "email": "john@example.com",
  "password": "password123"
}
```

### Login
```bash
POST /api/auth/login/
{
  "username": "john",
  "password": "password123"
}
```

---

## ✅ Features

- ✅ User registration with validation
- ✅ Secure login with Django auth
- ✅ Protected dashboard routes
- ✅ Logout functionality
- ✅ Show/hide password toggle
- ✅ Compact UI design
- ✅ Mobile responsive
- ✅ User menu with avatar

---

## 🎨 UI Improvements

**Compact Design**:
- Sidebar: 280px → 240px (-14%)
- Toolbar: 64px → 56px (-13%)
- Padding: 24px → 16px (-33%)
- Spacing: 24px → 16px (-33%)

**Result**: 20-30% more content visible!

---

## 🧪 Test Commands

```bash
# Test registration
curl -X POST http://192.168.1.200:8001/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"test123"}'

# Test login
curl -X POST http://192.168.1.200:8001/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'

# Test API
curl http://192.168.1.200:8001/api/stats/
```

---

## 🐛 Troubleshooting

**Cannot login?**
- Check username/password
- Register first if new user
- Check browser console

**Redirected to login?**
- Normal if not authenticated
- Login to access dashboard

**Logout not working?**
- Clear browser cache
- Try incognito window

---

## 📚 Full Documentation

- **Complete Guide**: `AUTHENTICATION_GUIDE.md`
- **Access Guide**: `ACCESS_GUIDE.md`
- **Auth Summary**: `AUTH_UPDATE_SUMMARY.md`

---

**Dashboard**: http://192.168.1.200:8001  
**Status**: ✅ Live and Ready!

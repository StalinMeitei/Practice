# Private Key Issue - Complete Fix Summary

## The Problem

When uploading a private key in django-pyas2 admin, you're getting:
```
Invalid Private Key or password is not correct.
```

## The Solution (TL;DR)

**LEAVE THE PASSWORD FIELD EMPTY!**

The private keys are NOT password protected. Django-pyas2 asks for a password field, but you must leave it blank.

## Quick Fix Steps

1. Go to: http://localhost:8001/admin/
2. Navigate to: **Organizations** → Click your organization (P1 or P2)
3. In "Private Key" section:
   - Click **Choose File**
   - Select: `P1_private.pem` (or `P2_private.pem`)
   - **Leave "Private Key Password" field EMPTY**
   - Click **Save**

## Files Created to Help You

### 1. Visual Guides

| File | Purpose |
|------|---------|
| `show-key-upload-guide.ps1` | Interactive PowerShell guide (run this!) |
| `upload_private_key_guide.txt` | Text-based visual guide |

**Run this now:**
```powershell
.\show-key-upload-guide.ps1
```

### 2. Troubleshooting Tools

| File | Purpose |
|------|---------|
| `PRIVATE_KEY_TROUBLESHOOTING.md` | Complete troubleshooting guide |
| `fix_private_key_format.py` | Check and fix key format issues |

**Check your keys:**
```bash
python fix_private_key_format.py
```

### 3. Updated Scripts

| File | What Changed |
|------|--------------|
| `init_as2_config.py` | Added private key usage instructions |
| `generate_certificates.py` | Already correct (PKCS#8 format) |

## Why This Happens

Django-pyas2 supports both:
- **Encrypted keys** (require password)
- **Unencrypted keys** (password must be empty)

Our setup uses **unencrypted keys** for Docker simplicity, so the password field must remain empty.

## Common Mistakes

❌ **DON'T DO THIS:**
- Enter "password" in the password field
- Enter "admin" in the password field
- Enter ANY text in the password field
- Use `P1_public.pem` (use `P1_private.pem` instead)

✅ **DO THIS:**
- Use `P1_private.pem` or `P2_private.pem`
- Leave password field **completely empty**
- Click Save

## Verification

After uploading correctly, you should see:
```
✓ The organization was changed successfully
✓ Key file: P1_private.pem
```

No error messages!

## Key Format Details

Your `P1_private.pem` contains:
1. **Private Key** (PKCS#8 format, unencrypted)
2. **Certificate** (X.509 format)

Both in ONE file, which is correct for django-pyas2.

## Testing

After fixing the key upload:

1. **Send a test message**:
   ```bash
   python test_file_transfer.py
   ```

2. **Check message status**:
   - Go to: http://localhost:8001/admin/
   - Click: **Messages**
   - Verify message is signed and encrypted

3. **Check logs**:
   ```bash
   docker-compose logs p1 -f
   ```

## Still Having Issues?

### Option 1: Regenerate Certificates
```bash
python generate_certificates.py
docker-compose restart p1 p2
```

### Option 2: Check Key Format
```bash
python fix_private_key_format.py
```

### Option 3: Read Detailed Guide
```bash
# Windows
notepad PRIVATE_KEY_TROUBLESHOOTING.md

# Or just open the file in your editor
```

### Option 4: View Interactive Guide
```powershell
.\show-key-upload-guide.ps1
```

## Quick Reference

| Scenario | Password Field | File to Use |
|----------|---------------|-------------|
| P1 Organization | **EMPTY** | P1_private.pem |
| P2 Organization | **EMPTY** | P2_private.pem |
| P1 Partner (in P2) | N/A | P1_public.pem |
| P2 Partner (in P1) | N/A | P2_public.pem |

## Summary

The fix is simple:
1. Use the correct file (`P1_private.pem` or `P2_private.pem`)
2. Leave password field **EMPTY**
3. Save

That's it! The most common mistake is entering something in the password field when the key is not encrypted.

## Resources

- **Visual Guide**: Run `.\show-key-upload-guide.ps1`
- **Troubleshooting**: Read `PRIVATE_KEY_TROUBLESHOOTING.md`
- **Format Checker**: Run `python fix_private_key_format.py`
- **Text Guide**: View `upload_private_key_guide.txt`

---

**Remember**: The password field should be **EMPTY**. Not "password", not "admin", not anything - just empty!

# Shazam Telegram Bot

یک ربات تلگرامی قدرتمند برای شناسایی موسیقی با استفاده از کتابخانه ShazamIO

A powerful Telegram bot for music recognition using ShazamIO library

## 🎵 ویژگی‌ها | Features

### قابلیت‌های اصلی | Core Features
- 🔍 **شناسایی آهنگ** - Identify songs from audio files
- 🌐 **جستجوی Inline** - Search songs in groups/channels
- ✏️ **ویرایش اطلاعات** - Edit song metadata
- 🌍 **چند زبانه** - Support for Persian and English
- 🎼 **اطلاعات کامل** - Detailed song information
- 🎵 **یکپارچه‌سازی Spotify** - Spotify integration

### قابلیت‌های پیشرفته | Advanced Features
- 📊 **مدیریت فایل** - Advanced file handling
- 🔧 **تنظیمات قابل سفارشی‌سازی** - Customizable settings
- 📝 **لاگینگ پیشرفته** - Advanced logging
- 🛡️ **امنیت** - Security features
- 🔄 **پشتیبان‌گیری** - Backup functionality
- 📈 **نظارت بر عملکرد** - Performance monitoring

## 🚀 نصب و راه‌اندازی | Installation & Setup

### پیش‌نیازها | Prerequisites
- Python 3.8+
- Telegram Bot Token (از @BotFather)
- دسترسی به اینترنت برای شناسایی آهنگ‌ها

### روش ۱: استفاده از اسکریپت راه‌اندازی | Method 1: Using Setup Script

```bash
# کلون یا دانلود فایل‌ها
git clone <repository-url>
cd shazam-telegram-bot

# اجرای اسکریپت راه‌اندازی
./setup.sh

# یا برای راه‌اندازی سریع
./setup.sh --quick

# یا برای راه‌اندازی با سرویس systemd
./setup.sh --service
```

### روش ۲: نصب دستی | Method 2: Manual Installation

```bash
# نصب پیش‌نیازها
pip3 install -r requirements.txt

# تنظیم توکن ربات
# ویرایش فایل bot_config.py و تنظیم TELEGRAM_BOT_TOKEN

# اجرای ربات
python3 shazam_bot.py
```

## ⚙️ تنظیمات | Configuration

### فایل کانفیگ | Configuration File

فایل `bot_config.py` شامل تمام تنظیمات قابل سفارشی‌سازی است:

```python
# تنظیمات اصلی ربات
TELEGRAM_BOT_TOKEN = "YOUR_TOKEN_HERE"
BOT_USERNAME = "YourBotUsername"
BOT_NAME = "Your Bot Name"

# تنظیمات فایل
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB
TEMP_DOWNLOAD_PATH = "/tmp/shazam_bot"

# تنظیمات زبان
DEFAULT_LANGUAGE = 'fa'  # 'fa' یا 'en'

# تنظیمات عملکرد
RECOGNITION_TIMEOUT = 30
MAX_CONCURRENT_RECOGNITIONS = 5
```

### متغیرهای مهم | Important Variables

| متغیر | توضیحات | پیش‌فرض |
|-------|---------|---------|
| `TELEGRAM_BOT_TOKEN` | توکن ربات تلگرام | REQUIRED |
| `BOT_USERNAME` | نام کاربری ربات | ShazamMusicBot |
| `MAX_FILE_SIZE` | حداکثر حجم فایل | 20MB |
| `DEFAULT_LANGUAGE` | زبان پیش‌فرض | fa |
| `RECOGNITION_TIMEOUT` | زمان انتظار برای شناسایی | 30 ثانیه |

## 📖 راهنمای استفاده | Usage Guide

### شروع کار | Getting Started

1. **ارسال /start** برای شروع و انتخاب زبان
2. **ارسال فایل صوتی** برای شناسایی آهنگ
3. **استفاده از Inline** برای جستجو در گروه‌ها

### دستورات | Commands

| دستور | توضیحات | مثال |
|-------|---------|------|
| `/start` | شروع ربات و انتخاب زبان | `/start` |
| `/help` | نمایش راهنما | `/help` |

### حالت Inline | Inline Mode

در هر گروه یا کانال:
```
@YourBotUsername نام آهنگ
```

مثال:
```
@ShazamMusicBot Blinding Lights
```

### ویرایش اطلاعات آهنگ | Editing Song Information

پس از شناسایی آهنگ:
1. کلیک روی دکمه "✏️ ویرایش اطلاعات آهنگ"
2. انتخاب بخش مورد نظر برای ویرایش
3. وارد کردن اطلاعات جدید
4. ذخیره تغییرات

## 🎯 مثال‌های کاربردی | Practical Examples

### مثال ۱: شناسایی آهنگ
```
کاربر: [ارسال فایل صوتی]
ربات: 🎵 آهنگ شناسایی شد!
      🎼 عنوان: Blinding Lights
      🎤 هنرمند: The Weeknd
      💿 آلبوم: After Hours
```

### مثال ۲: جستجوی Inline
```
کاربر: @ShazamMusicBo Blinding Lights
ربات: [نمایش نتایج جستجو]
```

### مثال ۳: ویرایش اطلاعات
```
کاربر: [کلیک روی دکمه ویرایش]
ربات: کدام اطلاعات را می‌خواهید ویرایش کنید؟
کاربر: [انتخاب عنوان]
ربات: عنوان آهنگ را وارد کنید:
کاربر: Blinding Lights (Remix)
ربات: ✅ اطلاعات آهنگ با موفقیت ویرایش شد!
```

## 🔧 اسکریپت‌های کاربردی | Utility Scripts

### start_bot.sh
```bash
#!/bin/bash
# اجرای ربات
python3 shazam_bot.py
```

### update_bot.sh
```bash
#!/bin/bash
# به‌روزرسانی ربات و وابستگی‌ها
git pull
pip3 install -r requirements.txt --upgrade
```

### backup_bot.sh
```bash
#!/bin/bash
# ایجاد پشتیبان از ربات
tar -czf backup_$(date +%Y%m%d).tar.gz \
    --exclude="backups" \
    --exclude="__pycache__" \
    .
```

## 🛠️ عیب‌یابی | Troubleshooting

### خطاهای رایج | Common Errors

#### 1. خطای توکن نامعتبر | Invalid Token Error
```
Error: Unauthorized
```
**راه‌حل**: بررسی توکن ربات در فایل `bot_config.py`

#### 2. خطای حجم فایل | File Size Error
```
Error: File size exceeds limit
```
**راه‌حل**: افزایش `MAX_FILE_SIZE` در تنظیمات

#### 3. خطای شناسایی | Recognition Error
```
Error: Recognition timeout
```
**راه‌حل**: افزایش `RECOGNITION_TIMEOUT` یا بررسی اتصال اینترنت

#### 4. خطای دسترسی فایل | File Access Error
```
Error: Permission denied
```
**راه‌حل**: بررسی دسترسی به مسیر `TEMP_DOWNLOAD_PATH`

### لاگ‌ها | Logs

برای مشاهده لاگ‌های ربات:
```bash
tail -f shazam_bot.log
```

## 📊 پیکربندی پیشرفته | Advanced Configuration

### تنظیمات امنیتی | Security Settings

```python
# لیست سیاه کاربران
BLACKLISTED_USERS = [123456789, 987654321]

# لیست سفید گروه‌ها
WHITELISTED_GROUPS = [-100123456789]

# محدودیت نرخ درخواست
MAX_REQUESTS_PER_MINUTE = 10
REQUEST_COOLDOWN = 5
```

### تنظیمات عملکرد | Performance Settings

```python
# حداکثر پردازش‌های همزمان
MAX_CONCURRENT_RECOGNITIONS = 5

# سطح لاگ
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR

# حالت توسعه
DEBUG_MODE = False
```

## 🌐 چند زبانه | Multilingual Support

### زبان‌های پشتیبانی شده | Supported Languages
- 🇮🇷 **فارسی (Persian)** - زبان پیش‌فرض
- 🇺🇸 **English** - انگلیسی

### افزودن زبان جدید | Adding New Language

1. افزودن پیام‌ها به دیکشنری‌ها
2. به‌روزرسانی دکمه‌ها
3. افزودن زبان به لیست پشتیبانی شده

## 📱 توسعه و مشارکت | Development & Contribution

### ساختار پروژه | Project Structure
```
shazam-telegram-bot/
├── shazam_bot.py      # فایل اصلی ربات
├── bot_config.py      # تنظیمات ربات
├── requirements.txt   # وابستگی‌ها
├── setup.sh          # اسکریپت راه‌اندازی
├── start_bot.sh      # اسکریپت اجرا
├── update_bot.sh     # اسکریپت به‌روزرسانی
├── backup_bot.sh     # اسکریپت پشتیبان
└── README.md         # مستندات
```

### محیط توسعه | Development Environment

```bash
# نصب وابستگی‌های توسعه
pip3 install -r requirements.txt

# اجرا در حالت توسعه
DEBUG_MODE=True python3 shazam_bot.py
```

## 📄 مجوز | License

این پروژه تحت مجوز MIT منتشر شده است.

## 🤝 پشتیبانی | Support

- 📧 **ایمیل**: support@example.com
- 💬 **تلگرام**: [@YourSupportBot](https://t.me/YourSupportBot)
- 🐛 **گزارش مشکل**: [GitHub Issues](https://github.com/your-repo/issues)

## 🎉 تشکرها | Acknowledgments

- [ShazamIO](https://github.com/shazamio/ShazamIO) برای کتابخانه شناسایی موسیقی
- [python-telegram-bot](https://python-telegram-bot.org/) برای فریمورک ربات تلگرام
- تمام توسعه‌دهندگان و مشارکت‌کنندگان

---

**⚠️ توجه**: این ربات از API معکوس‌ engineered شده Shazam استفاده می‌کند. لطفاً در استفاده از آن قوانین مربوطه را رعایت کنید.

**⚠️ Note**: This bot uses a reverse-engineered Shazam API. Please comply with applicable terms of service when using it.
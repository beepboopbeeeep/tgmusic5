"""
Shazam Telegram Bot Configuration
Edit these variables to customize your bot settings
"""

# ===========================================
# TELEGRAM BOT CONFIGURATION
# ===========================================

# Bot Token - Get this from @BotFather on Telegram
# How to get: 
# 1. Start a chat with @BotFather
# 2. Send /newbot
# 3. Follow the instructions to create your bot
# 4. Copy the token and paste it here
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"

# Bot Username - Without the @ symbol
# Example: "ShazamMusicBot" (not "@ShazamMusicBot")
BOT_USERNAME = "ShazamMusicBot"

# Bot Display Name - This is the name users will see
BOT_NAME = "Shazam Music Bot"

# ===========================================
# ADMINISTRATION SETTINGS
# ===========================================

# Admin User IDs - List of user IDs who can manage the bot
# How to get your user ID:
# 1. Send /start to @userinfobot
# 2. It will show your user ID
# Example: [123456789, 987654321]
ADMIN_USER_IDS = []

# ===========================================
# FILE HANDLING SETTINGS
# ===========================================

# Maximum file size for audio files (in bytes)
# Default: 20MB = 20 * 1024 * 1024
MAX_FILE_SIZE = 20 * 1024 * 1024

# Supported audio file formats
# Add or remove formats as needed
SUPPORTED_AUDIO_FORMATS = ['.mp3', '.m4a', '.ogg', '.flac', '.wav', '.opus', '.aac', '.wma']

# ===========================================
# DOWNLOAD AND STORAGE SETTINGS
# ===========================================

# Temporary file storage path
# This is where audio files are temporarily stored for processing
# Make sure the directory exists and is writable
TEMP_DOWNLOAD_PATH = "/tmp/shazam_bot"

# Enable/disable file downloads
# Set to False if you don't want to download files (recognition from URL only)
ENABLE_DOWNLOAD = True

# ===========================================
# RECOGNITION SETTINGS
# ===========================================

# Timeout for song recognition (in seconds)
# If recognition takes longer than this, it will be cancelled
RECOGNITION_TIMEOUT = 30

# Maximum recognition attempts
# How many times to try recognizing a song before giving up
MAX_RECOGNITION_ATTEMPTS = 3

# ===========================================
# LANGUAGE AND LOCALIZATION
# ===========================================

# Default language for new users
# Options: 'fa' (Persian), 'en' (English)
DEFAULT_LANGUAGE = 'fa'

# Enable/disable automatic language detection based on user's Telegram language
AUTO_DETECT_LANGUAGE = True

# ===========================================
# MESSAGE AND RESPONSE SETTINGS
# ===========================================

# Enable/disable rich formatting (Markdown)
ENABLE_MARKDOWN = True

# Show detailed error messages to users
# Set to False for production to avoid exposing sensitive information
SHOW_DETAILED_ERRORS = False

# Enable/disable bot activity indicators (typing, etc.)
SHOW_ACTIVITY_INDICATORS = True

# ===========================================
# PERFORMANCE AND RATE LIMITING
# ===========================================

# Rate limiting settings
# Maximum requests per user per minute
MAX_REQUESTS_PER_MINUTE = 10

# Cooldown period between requests (in seconds)
REQUEST_COOLDOWN = 5

# Maximum concurrent recognition processes
MAX_CONCURRENT_RECOGNITIONS = 5

# ===========================================
# LOGGING AND DEBUGGING
# ===========================================

# Log level for the bot
# Options: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
LOG_LEVEL = 'INFO'

# Log file path
# Set to None to log to console only
LOG_FILE = 'shazam_bot.log'

# Enable/disable debug mode
# Debug mode provides more detailed logging
DEBUG_MODE = False

# ===========================================
# ADVANCED FEATURES
# ===========================================

# Enable/disable inline mode
# Inline mode allows users to search for songs in groups
ENABLE_INLINE_MODE = True

# Enable/disable song editing features
ENABLE_SONG_EDITING = True

# Enable/disable metadata writing to audio files
# This allows the bot to edit ID3 tags of audio files
ENABLE_METADATA_WRITING = False

# Enable/disable Spotify integration
# This adds Spotify links to song results
ENABLE_SPOTIFY_INTEGRATION = True

# ===========================================
# CUSTOMIZATION OPTIONS
# ===========================================

# Custom welcome message (overrides default)
# Set to None to use default messages
CUSTOM_WELCOME_MESSAGE = None

# Custom help message (overrides default)
# Set to None to use default messages
CUSTOM_HELP_MESSAGE = None

# Custom error messages (overrides default)
# Set to None to use default messages
CUSTOM_ERROR_MESSAGES = None

# ===========================================
# SECURITY SETTINGS
# ===========================================

# Enable/disable user blacklist
# If True, the bot will check against a blacklist of users
ENABLE_USER_BLACKLIST = False

# List of blacklisted user IDs
BLACKLISTED_USERS = []

# Enable/disable group whitelist
# If True, the bot will only work in whitelisted groups
ENABLE_GROUP_WHITELIST = False

# List of whitelisted group IDs
WHITELISTED_GROUPS = []

# ===========================================
# BACKUP AND RECOVERY
# ===========================================

# Enable/disable automatic backup of user preferences
ENABLE_AUTO_BACKUP = True

# Backup interval (in hours)
BACKUP_INTERVAL = 24

# Backup file path
BACKUP_FILE = 'user_preferences_backup.json'

# ===========================================
# NOTIFICATION SETTINGS
# ===========================================

# Enable/disable admin notifications for errors
# If True, admins will be notified when errors occur
ENABLE_ADMIN_NOTIFICATIONS = True

# Enable/disable user notifications for bot updates
# If True, users will be notified about bot updates
ENABLE_USER_NOTIFICATIONS = False

# ===========================================
# DEVELOPER SETTINGS
# ===========================================

# Development mode
# Set to True during development for additional features
DEVELOPMENT_MODE = False

# Test bot token (for development)
# Set to None to use the main bot token
TEST_BOT_TOKEN = None

# Enable/disable test features
ENABLE_TEST_FEATURES = False

# ===========================================
# INSTRUCTIONS FOR USE
# ===========================================

"""
HOW TO USE THIS CONFIGURATION FILE:

1. REQUIRED SETTINGS:
   - TELEGRAM_BOT_TOKEN: Get this from @BotFather
   - BOT_USERNAME: Your bot's username without @
   - BOT_NAME: Your bot's display name

2. RECOMMENDED SETTINGS:
   - ADMIN_USER_IDS: Add your user ID for admin access
   - MAX_FILE_SIZE: Adjust based on your server capacity
   - TEMP_DOWNLOAD_PATH: Ensure this directory exists

3. OPTIONAL SETTINGS:
   - DEFAULT_LANGUAGE: Set preferred default language
   - LOG_LEVEL: Adjust logging verbosity
   - ENABLE_INLINE_MODE: Enable/disable inline search

4. SECURITY SETTINGS:
   - ENABLE_USER_BLACKLIST: Enable if you need to block users
   - ENABLE_GROUP_WHITELIST: Enable if you want to restrict to specific groups

5. PERFORMANCE SETTINGS:
   - MAX_REQUESTS_PER_MINUTE: Adjust based on your server capacity
   - REQUEST_COOLDOWN: Prevent spam
   - MAX_CONCURRENT_RECOGNITIONS: Limit concurrent processes

6. ADVANCED FEATURES:
   - ENABLE_SONG_EDITING: Allow users to edit song metadata
   - ENABLE_METADATA_WRITING: Allow editing ID3 tags
   - ENABLE_SPOTIFY_INTEGRATION: Add Spotify links to results

TO APPLY CHANGES:
1. Save this file
2. Restart the bot
3. Test the new settings

TROUBLESHOOTING:
- If the bot doesn't start, check the token
- If file processing fails, check TEMP_DOWNLOAD_PATH permissions
- If recognition is slow, adjust timeout and concurrent settings
- If you get rate limited, adjust rate limiting settings
"""
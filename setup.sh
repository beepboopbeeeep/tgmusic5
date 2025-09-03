#!/bin/bash

# Shazam Telegram Bot Setup Script
# This script helps you configure and set up the Shazam Telegram Bot

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to get user input with default value
get_input() {
    local prompt="$1"
    local default="$2"
    local var_name="$3"
    
    echo -n "$prompt [$default]: "
    read -r input
    
    if [ -z "$input" ]; then
        input="$default"
    fi
    
    # Export the variable
    export "$var_name"="$input"
}

# Function to check if directory exists and is writable
check_directory() {
    local dir="$1"
    
    if [ ! -d "$dir" ]; then
        print_info "Creating directory: $dir"
        mkdir -p "$dir"
    fi
    
    if [ ! -w "$dir" ]; then
        print_error "Directory $dir is not writable"
        exit 1
    fi
}

# Function to install Python dependencies
install_python_deps() {
    print_info "Installing Python dependencies..."
    
    # Check if pip is installed
    if ! command_exists pip3; then
        print_error "pip3 is not installed. Please install Python 3 and pip first."
        exit 1
    fi
    
    # Install required packages
    pip3 install -r requirements.txt
}

# Function to create requirements.txt
create_requirements_file() {
    print_info "Creating requirements.txt file..."
    
    cat > requirements.txt << 'EOF'
python-telegram-bot>=20.0
shazamio>=0.8.0
mutagen>=1.46.0
aiohttp>=3.8.0
asyncio>=3.4.3
python-dotenv>=0.19.0
EOF
    
    print_success "requirements.txt created successfully"
}

# Function to create systemd service file
create_systemd_service() {
    local service_name="$1"
    local service_file="/etc/systemd/system/${service_name}.service"
    
    print_info "Creating systemd service file..."
    
    # Get current working directory
    local current_dir=$(pwd)
    
    # Create service file
    sudo tee "$service_file" > /dev/null << EOF
[Unit]
Description=Shazam Telegram Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$current_dir
ExecStart=/usr/bin/python3 $current_dir/shazam_bot.py
Restart=always
RestartSec=10
Environment=PYTHONPATH=$current_dir

[Install]
WantedBy=multi-user.target
EOF
    
    print_success "Systemd service file created: $service_file"
    
    # Reload systemd
    sudo systemctl daemon-reload
    
    # Enable service
    sudo systemctl enable "$service_name"
    
    print_success "Service $service_name enabled"
}

# Function to create start script
create_start_script() {
    print_info "Creating start script..."
    
    cat > start_bot.sh << 'EOF'
#!/bin/bash

# Shazam Telegram Bot Start Script

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if Python 3 is available
if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if the bot file exists
if [ ! -f "shazam_bot.py" ]; then
    echo "Error: shazam_bot.py not found"
    exit 1
fi

# Start the bot
echo "Starting Shazam Telegram Bot..."
python3 shazam_bot.py
EOF
    
    chmod +x start_bot.sh
    print_success "Start script created: start_bot.sh"
}

# Function to create update script
create_update_script() {
    print_info "Creating update script..."
    
    cat > update_bot.sh << 'EOF'
#!/bin/bash

# Shazam Telegram Bot Update Script

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if git is available
if command -v git >/dev/null 2>&1; then
    echo "Updating from git repository..."
    git pull
else
    echo "Git not available, skipping repository update"
fi

# Update Python dependencies
if command -v pip3 >/dev/null 2>&1; then
    echo "Updating Python dependencies..."
    pip3 install -r requirements.txt --upgrade
else
    echo "pip3 not available, skipping dependency update"
fi

echo "Update completed!"
EOF
    
    chmod +x update_bot.sh
    print_success "Update script created: update_bot.sh"
}

# Function to create backup script
create_backup_script() {
    print_info "Creating backup script..."
    
    cat > backup_bot.sh << 'EOF'
#!/bin/bash

# Shazam Telegram Bot Backup Script

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the script directory
cd "$SCRIPT_DIR"

# Create backup directory
BACKUP_DIR="backups"
mkdir -p "$BACKUP_DIR"

# Create timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.tar.gz"

# Create backup
echo "Creating backup..."
tar -czf "$BACKUP_FILE" \
    --exclude="backups" \
    --exclude="__pycache__" \
    --exclude="*.pyc" \
    --exclude="*.log" \
    --exclude="tmp" \
    .

echo "Backup created: $BACKUP_FILE"
echo "Backup size: $(du -h "$BACKUP_FILE" | cut -f1)"
EOF
    
    chmod +x backup_bot.sh
    print_success "Backup script created: backup_bot.sh"
}

# Function to create configuration file
create_config_file() {
    print_info "Creating configuration file..."
    
    # Create config file from user input
    cat > bot_config.py << EOF
"""
Shazam Telegram Bot Configuration
Generated by setup script on $(date)
"""

# ===========================================
# TELEGRAM BOT CONFIGURATION
# ===========================================

# Bot Token - Get this from @BotFather on Telegram
TELEGRAM_BOT_TOKEN = "$TELEGRAM_BOT_TOKEN"

# Bot Username - Without the @ symbol
BOT_USERNAME = "$BOT_USERNAME"

# Bot Display Name - This is the name users will see
BOT_NAME = "$BOT_NAME"

# ===========================================
# ADMINISTRATION SETTINGS
# ===========================================

# Admin User IDs - List of user IDs who can manage the bot
ADMIN_USER_IDS = $ADMIN_USER_IDS

# ===========================================
# FILE HANDLING SETTINGS
# ===========================================

# Maximum file size for audio files (in bytes)
MAX_FILE_SIZE = $MAX_FILE_SIZE

# Supported audio file formats
SUPPORTED_AUDIO_FORMATS = ['.mp3', '.m4a', '.ogg', '.flac', '.wav', '.opus', '.aac', '.wma']

# ===========================================
# DOWNLOAD AND STORAGE SETTINGS
# ===========================================

# Temporary file storage path
TEMP_DOWNLOAD_PATH = "$TEMP_DOWNLOAD_PATH"

# Enable/disable file downloads
ENABLE_DOWNLOAD = $ENABLE_DOWNLOAD

# ===========================================
# RECOGNITION SETTINGS
# ===========================================

# Timeout for song recognition (in seconds)
RECOGNITION_TIMEOUT = $RECOGNITION_TIMEOUT

# Maximum recognition attempts
MAX_RECOGNITION_ATTEMPTS = $MAX_RECOGNITION_ATTEMPTS

# ===========================================
# LANGUAGE AND LOCALIZATION
# ===========================================

# Default language for new users
DEFAULT_LANGUAGE = '$DEFAULT_LANGUAGE'

# Enable/disable automatic language detection
AUTO_DETECT_LANGUAGE = $AUTO_DETECT_LANGUAGE

# ===========================================
# PERFORMANCE AND RATE LIMITING
# ===========================================

# Maximum requests per user per minute
MAX_REQUESTS_PER_MINUTE = $MAX_REQUESTS_PER_MINUTE

# Cooldown period between requests (in seconds)
REQUEST_COOLDOWN = $REQUEST_COOLDOWN

# Maximum concurrent recognition processes
MAX_CONCURRENT_RECOGNITIONS = $MAX_CONCURRENT_RECOGNITIONS

# ===========================================
# LOGGING AND DEBUGGING
# ===========================================

# Log level
LOG_LEVEL = '$LOG_LEVEL'

# Log file path
LOG_FILE = '$LOG_FILE'

# Debug mode
DEBUG_MODE = $DEBUG_MODE

# ===========================================
# ADVANCED FEATURES
# ===========================================

# Enable/disable inline mode
ENABLE_INLINE_MODE = $ENABLE_INLINE_MODE

# Enable/disable song editing features
ENABLE_SONG_EDITING = $ENABLE_SONG_EDITING

# Enable/disable metadata writing
ENABLE_METADATA_WRITING = $ENABLE_METADATA_WRITING

# Enable/disable Spotify integration
ENABLE_SPOTIFY_INTEGRATION = $ENABLE_SPOTIFY_INTEGRATION

# ===========================================
# SECURITY SETTINGS
# ===========================================

# Enable/disable user blacklist
ENABLE_USER_BLACKLIST = $ENABLE_USER_BLACKLIST

# Enable/disable group whitelist
ENABLE_GROUP_WHITELIST = $ENABLE_GROUP_WHITELIST

# ===========================================
# NOTIFICATION SETTINGS
# ===========================================

# Enable/disable admin notifications
ENABLE_ADMIN_NOTIFICATIONS = $ENABLE_ADMIN_NOTIFICATIONS

# ===========================================
# DEVELOPER SETTINGS
# ===========================================

# Development mode
DEVELOPMENT_MODE = $DEVELOPMENT_MODE
EOF
    
    print_success "Configuration file created: bot_config.py"
}

# Function to display help
show_help() {
    echo "Shazam Telegram Bot Setup Script"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help          Show this help message"
    echo "  -i, --interactive   Interactive setup (default)"
    echo "  -q, --quick         Quick setup with default values"
    echo "  -c, --config FILE   Use configuration file"
    echo "  -s, --service       Create systemd service"
    echo "  --skip-deps         Skip dependency installation"
    echo ""
    echo "Examples:"
    echo "  $0                  Interactive setup"
    echo "  $0 -q               Quick setup"
    echo "  $0 -s               Setup with systemd service"
    echo ""
}

# Main setup function
main() {
    echo "=========================================="
    echo "  Shazam Telegram Bot Setup Script"
    echo "=========================================="
    echo ""
    
    # Parse command line arguments
    INTERACTIVE=true
    CREATE_SERVICE=false
    SKIP_DEPS=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -i|--interactive)
                INTERACTIVE=true
                shift
                ;;
            -q|--quick)
                INTERACTIVE=false
                shift
                ;;
            -s|--service)
                CREATE_SERVICE=true
                shift
                ;;
            --skip-deps)
                SKIP_DEPS=true
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Check if Python 3 is installed
    if ! command_exists python3; then
        print_error "Python 3 is not installed. Please install Python 3.8 or higher."
        exit 1
    fi
    
    print_success "Python 3 is installed: $(python3 --version)"
    
    # Create requirements file
    create_requirements_file
    
    # Install dependencies if not skipped
    if [ "$SKIP_DEPS" = false ]; then
        install_python_deps
    else
        print_warning "Skipping dependency installation"
    fi
    
    if [ "$INTERACTIVE" = true ]; then
        echo ""
        echo "=== Interactive Configuration ==="
        echo ""
        
        # Get user input
        get_input "Enter your Telegram Bot Token" "YOUR_TELEGRAM_BOT_TOKEN_HERE" "TELEGRAM_BOT_TOKEN"
        get_input "Enter your Bot Username (without @)" "ShazamMusicBot" "BOT_USERNAME"
        get_input "Enter your Bot Display Name" "Shazam Music Bot" "BOT_NAME"
        get_input "Enter your User ID (for admin access)" "" "USER_ID"
        get_input "Enter temporary download path" "/tmp/shazam_bot" "TEMP_DOWNLOAD_PATH"
        get_input "Enter default language (fa/en)" "fa" "DEFAULT_LANGUAGE"
        get_input "Enter max file size in MB" "20" "MAX_FILE_SIZE_MB"
        get_input "Enter recognition timeout in seconds" "30" "RECOGNITION_TIMEOUT"
        
        # Convert numeric values
        MAX_FILE_SIZE=$((MAX_FILE_SIZE_MB * 1024 * 1024))
        
        # Create admin user IDs list
        if [ -n "$USER_ID" ]; then
            ADMIN_USER_IDS="[$USER_ID]"
        else
            ADMIN_USER_IDS="[]"
        fi
        
        # Set boolean values
        ENABLE_DOWNLOAD="true"
        AUTO_DETECT_LANGUAGE="true"
        MAX_REQUESTS_PER_MINUTE="10"
        REQUEST_COOLDOWN="5"
        MAX_CONCURRENT_RECOGNITIONS="5"
        LOG_LEVEL="'INFO'"
        LOG_FILE="'shazam_bot.log'"
        DEBUG_MODE="false"
        ENABLE_INLINE_MODE="true"
        ENABLE_SONG_EDITING="true"
        ENABLE_METADATA_WRITING="false"
        ENABLE_SPOTIFY_INTEGRATION="true"
        ENABLE_USER_BLACKLIST="false"
        ENABLE_GROUP_WHITELIST="false"
        ENABLE_ADMIN_NOTIFICATIONS="true"
        DEVELOPMENT_MODE="false"
        
    else
        echo ""
        echo "=== Quick Setup with Default Values ==="
        echo ""
        
        # Use default values
        TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN_HERE"
        BOT_USERNAME="ShazamMusicBot"
        BOT_NAME="Shazam Music Bot"
        ADMIN_USER_IDS="[]"
        TEMP_DOWNLOAD_PATH="/tmp/shazam_bot"
        DEFAULT_LANGUAGE="fa"
        MAX_FILE_SIZE=$((20 * 1024 * 1024))
        ENABLE_DOWNLOAD="true"
        RECOGNITION_TIMEOUT="30"
        MAX_RECOGNITION_ATTEMPTS="3"
        AUTO_DETECT_LANGUAGE="true"
        MAX_REQUESTS_PER_MINUTE="10"
        REQUEST_COOLDOWN="5"
        MAX_CONCURRENT_RECOGNITIONS="5"
        LOG_LEVEL="'INFO'"
        LOG_FILE="'shazam_bot.log'"
        DEBUG_MODE="false"
        ENABLE_INLINE_MODE="true"
        ENABLE_SONG_EDITING="true"
        ENABLE_METADATA_WRITING="false"
        ENABLE_SPOTIFY_INTEGRATION="true"
        ENABLE_USER_BLACKLIST="false"
        ENABLE_GROUP_WHITELIST="false"
        ENABLE_ADMIN_NOTIFICATIONS="true"
        DEVELOPMENT_MODE="false"
    fi
    
    # Create temporary directory
    check_directory "$TEMP_DOWNLOAD_PATH"
    
    # Create configuration file
    create_config_file
    
    # Create utility scripts
    create_start_script
    create_update_script
    create_backup_script
    
    # Create systemd service if requested
    if [ "$CREATE_SERVICE" = true ]; then
        if command_exists systemctl; then
            create_systemd_service "shazam-bot"
        else
            print_warning "systemctl not found. Skipping systemd service creation."
        fi
    fi
    
    echo ""
    echo "=========================================="
    echo "  Setup Complete!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo ""
    echo "1. Edit bot_config.py and set your TELEGRAM_BOT_TOKEN"
    echo "   You can get this from @BotFather on Telegram"
    echo ""
    echo "2. Start the bot:"
    echo "   ./start_bot.sh"
    echo ""
    echo "3. Or if you created a systemd service:"
    echo "   sudo systemctl start shazam-bot"
    echo "   sudo systemctl status shazam-bot"
    echo ""
    echo "4. Check the logs:"
    echo "   tail -f shazam_bot.log"
    echo ""
    echo "5. Useful scripts:"
    echo "   ./update_bot.sh    - Update the bot"
    echo "   ./backup_bot.sh    - Create backup"
    echo ""
    echo "Configuration files created:"
    echo "  - bot_config.py    - Bot configuration"
    echo "  - requirements.txt - Python dependencies"
    echo ""
    echo "Utility scripts created:"
    echo "  - start_bot.sh     - Start the bot"
    echo "  - update_bot.sh    - Update the bot"
    echo "  - backup_bot.sh    - Create backup"
    echo ""
    
    if [ "$CREATE_SERVICE" = true ] && command_exists systemctl; then
        echo "Systemd service created:"
        echo "  - /etc/systemd/system/shazam-bot.service"
        echo ""
    fi
    
    print_success "Setup completed successfully!"
}

# Run main function
main "$@"
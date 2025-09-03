#!/usr/bin/env python3
"""
Shazam Telegram Bot
A Telegram bot for music recognition using ShazamIO library
Features: Music identification, language selection, inline search, song editing
"""

import asyncio
import logging
import os
import tempfile
from typing import Dict, Optional, List
from datetime import datetime

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultAudio,
    InlineQueryResultArticle,
    InputTextMessageContent,
    BotCommand,
    Message,
    Audio,
    Voice,
    Document,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    InlineQueryHandler,
    ContextTypes,
    filters,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
)
from telegram.constants import ParseMode

from shazamio import Shazam, Serialize
import mutagen
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.flac import FLAC

# Configuration - EDIT THESE VALUES
# =================================
# Telegram Bot Token - Get from @BotFather
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"  # <-- EDIT THIS: Your Telegram bot token

# Bot Settings
BOT_USERNAME = "ShazamMusicBot"  # <-- EDIT THIS: Your bot username without @
BOT_NAME = "Shazam Music Bot"   # <-- EDIT THIS: Your bot display name

# Admin Settings (Optional)
ADMIN_USER_IDS = []  # <-- EDIT THIS: List of admin user IDs for bot management (e.g., [123456789, 987654321])

# Message Settings
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB max file size
SUPPORTED_AUDIO_FORMATS = ['.mp3', '.m4a', '.ogg', '.flac', '.wav', '.opus']

# Language Settings
DEFAULT_LANGUAGE = 'fa'  # <-- EDIT THIS: Default language ('fa' for Persian, 'en' for English)

# Download Settings
TEMP_DOWNLOAD_PATH = "/tmp/shazam_bot"  # <-- EDIT THIS: Temporary file storage path
ENABLE_DOWNLOAD = True  # <-- EDIT THIS: Enable/disable file downloads

# Recognition Settings
RECOGNITION_TIMEOUT = 30  # <-- EDIT THIS: Timeout for song recognition in seconds
MAX_RECOGNITION_ATTEMPTS = 3  # <-- EDIT THIS: Maximum recognition attempts

# Message Templates
WELCOME_MESSAGE = {
    'fa': """🎵 **به ربات شناسایی موسیقی خوش آمدید!**

من می‌توانم آهنگ‌ها را از طریق فایل‌های صوتی شناسایی کنم.

**قابلیت‌های من:**
🔍 شناسایی آهنگ از فایل صوتی
🌐 جستجوی آهنگ در گروه‌ها (Inline Mode)
✏️ ویرایش اطلاعات آهنگ
🌍 پشتیبانی از دو زبان فارسی و انگلیسی

**نحوه استفاده:**
1. یک فایل صوتی برایم بفرستید
2. در گروه‌ها از @{} استفاده کنید
3. از دکمه‌های شیشه‌ای برای ویرایش اطلاعات استفاده کنید

برای شروع، زبان خود را انتخاب کنید:""",
    
    'en': """🎵 **Welcome to Music Recognition Bot!**

I can identify songs from audio files.

**My Features:**
🔍 Identify songs from audio files
🌐 Search songs in groups (Inline Mode)
✏️ Edit song information
🌍 Support for Persian and English languages

**How to use:**
1. Send me an audio file
2. Use @{} in groups
3. Use inline buttons to edit information

To get started, select your language:"""
}

LANGUAGE_MESSAGE = {
    'fa': "لطفاً زبان خود را انتخاب کنید:",
    'en': "Please select your language:"
}

BUTTONS = {
    'fa': {
        'persian': "🇮🇷 فارسی",
        'english': "🇺🇸 English",
        'edit_info': "✏️ ویرایش اطلاعات آهنگ",
        'back': "🔙 بازگشت",
        'cancel': "❌ لغو",
        'save': "💾 ذخیره",
        'search_again': "🔍 جستجوی مجدد",
    },
    'en': {
        'persian': "🇮🇷 Persian",
        'english': "🇺🇸 English",
        'edit_info': "✏️ Edit Song Info",
        'back': "🔙 Back",
        'cancel': "❌ Cancel",
        'save': "💾 Save",
        'search_again': "🔍 Search Again",
    }
}

RECOGNITION_MESSAGES = {
    'fa': {
        'processing': "⏳ در حال پردازش فایل صوتی...",
        'recognizing': "🔍 در حال شناسایی آهنگ...",
        'success': "✅ آهنگ با موفقیت شناسایی شد!",
        'failed': "❌ متأسفانه نتوانستم آهنگ را شناسایی کنم.",
        'no_file': "❌ لطفاً یک فایل صوتی معتبر ارسال کنید.",
        'file_too_large': f"❌ حجم فایل بیش از حد مجاز است (حداکثر {MAX_FILE_SIZE//1024//1024}MB).",
        'unsupported_format': "❌ فرمت فایل پشتیبانی نمی‌شود.",
        'timeout': "❌ زمان شناسایی به پایان رسید. لطفاً دوباره تلاش کنید.",
    },
    'en': {
        'processing': "⏳ Processing audio file...",
        'recognizing': "🔍 Recognizing song...",
        'success': "✅ Song successfully identified!",
        'failed': "❌ Sorry, I couldn't identify the song.",
        'no_file': "❌ Please send a valid audio file.",
        'file_too_large': f"❌ File size exceeds limit (max {MAX_FILE_SIZE//1024//1024}MB).",
        'unsupported_format': "❌ File format not supported.",
        'timeout': "❌ Recognition timeout. Please try again.",
    }
}

EDIT_MESSAGES = {
    'fa': {
        'title': "عنوان آهنگ را وارد کنید:",
        'artist': "نام هنرمند را وارد کنید:",
        'album': "نام آلبوم را وارد کنید:",
        'genre': "ژانر موسیقی را وارد کنید:",
        'year': "سال انتشار را وارد کنید:",
        'success': "✅ اطلاعات آهنگ با موفقیت ویرایش شد!",
        'cancel': "❌ ویرایش لغو شد.",
    },
    'en': {
        'title': "Enter song title:",
        'artist': "Enter artist name:",
        'album': "Enter album name:",
        'genre': "Enter music genre:",
        'year': "Enter release year:",
        'success': "✅ Song information successfully edited!",
        'cancel': "❌ Editing cancelled.",
    }
}

# Conversation states for editing
EDIT_TITLE, EDIT_ARTIST, EDIT_ALBUM, EDIT_GENRE, EDIT_YEAR = range(5)

class ShazamBot:
    def __init__(self):
        self.shazam = Shazam()
        self.user_languages: Dict[int, str] = {}
        self.user_sessions: Dict[int, Dict] = {}
        
        # Create temp directory if it doesn't exist
        os.makedirs(TEMP_DOWNLOAD_PATH, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)

    def get_user_language(self, user_id: int) -> str:
        """Get user's preferred language"""
        return self.user_languages.get(user_id, DEFAULT_LANGUAGE)

    def get_message(self, user_id: int, message_dict: Dict) -> str:
        """Get localized message for user"""
        lang = self.get_user_language(user_id)
        return message_dict.get(lang, message_dict.get('en', ''))

    def get_buttons(self, user_id: int) -> Dict[str, str]:
        """Get localized buttons for user"""
        lang = self.get_user_language(user_id)
        return BUTTONS.get(lang, BUTTONS.get('en', {}))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        
        # Create language selection keyboard
        keyboard = [
            [
                InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa"),
                InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_text = WELCOME_MESSAGE.get(self.get_user_language(user_id), WELCOME_MESSAGE['en'])
        welcome_text = welcome_text.format(BOT_USERNAME)
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        user_id = update.effective_user.id
        lang = self.get_user_language(user_id)
        
        help_text = {
            'fa': """**راهنمای استفاده از ربات:**

🎵 **شناسایی آهنگ:**
- یک فایل صوتی ارسال کنید
- ربات به صورت خودکار آهنگ را شناسایی می‌کند

🌐 **جستجوی در گروه‌ها:**
- در هر گروهی تایپ کنید: `@{} نام آهنگ`
- نتایج جستجو به صورت inline نمایش داده می‌شود

✏️ **ویرایش اطلاعات:**
- پس از شناسایی آهنگ، دکمه "ویرایش اطلاعات" را بزنید
- اطلاعات آهنگ را ویرایش کنید

🌍 **تغییر زبان:**
- دستور `/start` را ارسال کنید
- زبان مورد نظر را انتخاب کنید""",
            
            'en': """**Bot Usage Guide:**

🎵 **Song Recognition:**
- Send an audio file
- Bot will automatically identify the song

🌐 **Search in Groups:**
- Type in any group: `@{} song name`
- Search results will be shown inline

✏️ **Edit Information:**
- After song identification, click "Edit Song Info"
- Edit the song information

🌍 **Change Language:**
- Send `/start` command
- Select your preferred language"""
        }
        
        help_text = help_text.get(lang, help_text['en'])
        help_text = help_text.format(BOT_USERNAME)
        
        await update.message.reply_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN
        )

    async def language_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle language selection callback"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        lang_code = query.data.split('_')[1]
        
        # Save user language preference
        self.user_languages[user_id] = lang_code
        
        # Send confirmation message
        confirm_text = {
            'fa': "✅ زبان شما با موفقیت تنظیم شد!",
            'en': "✅ Your language has been set successfully!"
        }
        
        await query.edit_message_text(
            text=confirm_text.get(lang_code, confirm_text['en'])
        )

    async def handle_audio_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming audio files"""
        user_id = update.effective_user.id
        lang = self.get_user_language(user_id)
        
        # Check if message has audio
        audio = update.message.audio or update.message.voice or update.message.document
        
        if not audio:
            msg_text = self.get_message(user_id, RECOGNITION_MESSAGES)['no_file']
            await update.message.reply_text(msg_text)
            return
        
        # Check file size
        if audio.file_size > MAX_FILE_SIZE:
            msg_text = self.get_message(user_id, RECOGNITION_MESSAGES)['file_too_large']
            await update.message.reply_text(msg_text)
            return
        
        # Check file format
        file_name = getattr(audio, 'file_name', '') or audio.file_path or ''
        if not any(file_name.lower().endswith(ext) for ext in SUPPORTED_AUDIO_FORMATS):
            msg_text = self.get_message(user_id, RECOGNITION_MESSAGES)['unsupported_format']
            await update.message.reply_text(msg_text)
            return
        
        # Send processing message
        processing_msg = await update.message.reply_text(
            self.get_message(user_id, RECOGNITION_MESSAGES)['processing']
        )
        
        try:
            # Download file
            file = await context.bot.get_file(audio.file_id)
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(
                delete=False, 
                suffix=os.path.splitext(file_name)[1] or '.mp3',
                dir=TEMP_DOWNLOAD_PATH
            ) as temp_file:
                await file.download_to_drive(temp_file.name)
                temp_file_path = temp_file.name
            
            # Update message to recognizing
            await processing_msg.edit_text(
                self.get_message(user_id, RECOGNITION_MESSAGES)['recognizing']
            )
            
            # Recognize song
            result = await self.recognize_song_with_timeout(temp_file_path)
            
            # Clean up temp file
            os.unlink(temp_file_path)
            
            if result:
                await self.send_song_result(update, result, user_id)
            else:
                await processing_msg.edit_text(
                    self.get_message(user_id, RECOGNITION_MESSAGES)['failed']
                )
                
        except Exception as e:
            self.logger.error(f"Error processing audio file: {e}")
            await processing_msg.edit_text(
                self.get_message(user_id, RECOGNITION_MESSAGES)['failed']
            )

    async def recognize_song_with_timeout(self, file_path: str) -> Optional[Dict]:
        """Recognize song with timeout"""
        try:
            # Use asyncio.wait_for to add timeout
            result = await asyncio.wait_for(
                self.shazam.recognize(file_path),
                timeout=RECOGNITION_TIMEOUT
            )
            return result
        except asyncio.TimeoutError:
            return None
        except Exception as e:
            self.logger.error(f"Recognition error: {e}")
            return None

    async def send_song_result(self, update: Update, result: Dict, user_id: int):
        """Send song recognition result"""
        try:
            # Serialize the result
            track_data = result.get('track', {})
            if not track_data:
                await update.message.reply_text(
                    self.get_message(user_id, RECOGNITION_MESSAGES)['failed']
                )
                return
            
            # Extract song information
            title = track_data.get('title', 'Unknown')
            artist = track_data.get('subtitle', 'Unknown Artist')
            album = track_data.get('sections', [{}])[0].get('metadata', [{}])[0].get('text', 'Unknown Album')
            year = track_data.get('sections', [{}])[0].get('metadata', [{}])[1].get('text', 'Unknown Year')
            genre = track_data.get('genres', {}).get('primary', 'Unknown Genre')
            
            # Get Spotify URL if available
            spotify_url = None
            for hub in track_data.get('hub', {}).get('actions', []):
                if hub.get('type') == 'spotify' and hub.get('uri'):
                    spotify_url = hub.get('uri')
                    break
            
            # Create result message
            result_text = {
                'fa': f"""🎵 **آهنگ شناسایی شد!**

🎼 **عنوان:** {title}
🎤 **هنرمند:** {artist}
💿 **آلبوم:** {album}
📅 **سال:** {year}
🎭 **ژانر:** {genre}""",
                
                'en': f"""🎵 **Song Identified!**

🎼 **Title:** {title}
🎤 **Artist:** {artist}
💿 **Album:** {album}
📅 **Year:** {year}
🎭 **Genre:** {genre}"""
            }
            
            lang = self.get_user_language(user_id)
            message = result_text.get(lang, result_text['en'])
            
            # Create keyboard with edit button
            buttons = self.get_buttons(user_id)
            keyboard = [
                [
                    InlineKeyboardButton(buttons['edit_info'], callback_data=f"edit_{update.message.message_id}")
                ]
            ]
            
            if spotify_url:
                keyboard.append([
                    InlineKeyboardButton("🎵 Spotify", url=spotify_url)
                ])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Store song data for editing
            self.user_sessions[user_id] = {
                'message_id': update.message.message_id,
                'song_data': {
                    'title': title,
                    'artist': artist,
                    'album': album,
                    'year': year,
                    'genre': genre,
                    'file_id': update.message.audio.file_id if update.message.audio else None,
                    'file_path': update.message.audio.file_path if update.message.audio else None
                }
            }
            
            await update.message.reply_text(
                message,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
            
        except Exception as e:
            self.logger.error(f"Error sending song result: {e}")
            await update.message.reply_text(
                self.get_message(user_id, RECOGNITION_MESSAGES)['failed']
            )

    async def edit_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle edit song info callback"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        message_id = int(query.data.split('_')[1])
        
        # Get song data from session
        session = self.user_sessions.get(user_id, {})
        if session.get('message_id') != message_id:
            await query.edit_message_text("❌ Session expired. Please send the audio file again.")
            return
        
        # Create edit menu
        lang = self.get_user_language(user_id)
        buttons = self.get_buttons(user_id)
        
        keyboard = [
            [InlineKeyboardButton("🎼 Title", callback_data="edit_field_title")],
            [InlineKeyboardButton("🎤 Artist", callback_data="edit_field_artist")],
            [InlineKeyboardButton("💿 Album", callback_data="edit_field_album")],
            [InlineKeyboardButton("🎭 Genre", callback_data="edit_field_genre")],
            [InlineKeyboardButton("📅 Year", callback_data="edit_field_year")],
            [InlineKeyboardButton(buttons['back'], callback_data="edit_back")],
            [InlineKeyboardButton(buttons['cancel'], callback_data="edit_cancel")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        edit_text = {
            'fa': "✏️ **ویرایش اطلاعات آهنگ**\n\nکدام اطلاعات را می‌خواهید ویرایش کنید؟",
            'en': "✏️ **Edit Song Information**\n\nWhich information would you like to edit?"
        }
        
        await query.edit_message_text(
            text=edit_text.get(lang, edit_text['en']),
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

    async def edit_field_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle edit field selection callback"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        field = query.data.split('_')[2]
        
        # Store the field being edited
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {}
        self.user_sessions[user_id]['editing_field'] = field
        
        # Send prompt for the field
        lang = self.get_user_language(user_id)
        prompt_text = EDIT_MESSAGES.get(lang, EDIT_MESSAGES['en']).get(field, "Enter value:")
        
        await query.edit_message_text(text=prompt_text)
        
        # Set conversation state
        context.user_data['edit_state'] = field
        
        return field

    async def handle_edit_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text input for editing"""
        user_id = update.effective_user.id
        lang = self.get_user_language(user_id)
        
        # Get the field being edited
        field = context.user_data.get('edit_state')
        if not field:
            return
        
        # Get the new value
        new_value = update.message.text.strip()
        
        # Update the song data
        session = self.user_sessions.get(user_id, {})
        if 'song_data' in session:
            session['song_data'][field] = new_value
        
        # Send confirmation
        success_text = self.get_message(user_id, EDIT_MESSAGES)['success']
        await update.message.reply_text(success_text)
        
        # Clear conversation state
        context.user_data['edit_state'] = None
        
        # Show updated song info
        await self.show_updated_song_info(update, user_id)

    async def show_updated_song_info(self, update: Update, user_id: int):
        """Show updated song information"""
        session = self.user_sessions.get(user_id, {})
        song_data = session.get('song_data', {})
        
        lang = self.get_user_language(user_id)
        
        info_text = {
            'fa': f"""🎵 **اطلاعات به‌روزرسانی شده آهنگ:**

🎼 **عنوان:** {song_data.get('title', 'Unknown')}
🎤 **هنرمند:** {song_data.get('artist', 'Unknown Artist')}
💿 **آلبوم:** {song_data.get('album', 'Unknown Album')}
📅 **سال:** {song_data.get('year', 'Unknown Year')}
🎭 **ژانر:** {song_data.get('genre', 'Unknown Genre')}""",
            
            'en': f"""🎵 **Updated Song Information:**

🎼 **Title:** {song_data.get('title', 'Unknown')}
🎤 **Artist:** {song_data.get('artist', 'Unknown Artist')}
💿 **Album:** {song_data.get('album', 'Unknown Album')}
📅 **Year:** {song_data.get('year', 'Unknown Year')}
🎭 **Genre:** {song_data.get('genre', 'Unknown Genre')}"""
        }
        
        buttons = self.get_buttons(user_id)
        keyboard = [
            [InlineKeyboardButton(buttons['edit_info'], callback_data="edit_again")],
            [InlineKeyboardButton(buttons['search_again'], callback_data="search_again")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            info_text.get(lang, info_text['en']),
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

    async def inline_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline queries"""
        query = update.inline_query
        if not query or not query.query:
            return
        
        user_id = query.from_user.id
        lang = self.get_user_language(user_id)
        
        search_query = query.query.strip()
        
        try:
            # Search for tracks
            results = await self.shazam.search_track(query=search_query, limit=10)
            
            inline_results = []
            
            for track in results.get('tracks', {}).get('hits', [])[:5]:
                track_data = track.get('track', {})
                title = track_data.get('title', 'Unknown')
                artist = track_data.get('subtitle', 'Unknown Artist')
                
                # Create inline result
                result = InlineQueryResultArticle(
                    id=track_data.get('id', str(hash(title + artist))),
                    title=f"{title} - {artist}",
                    description=f"🎵 {title} by {artist}",
                    input_message_content=InputTextMessageContent(
                        message_text=f"🎵 **{title}**\n🎤 {artist}\n\nFound via @{BOT_USERNAME}",
                        parse_mode=ParseMode.MARKDOWN
                    ),
                    thumb_url=track_data.get('images', {}).get('coverart', ''),
                    thumb_width=100,
                    thumb_height=100
                )
                inline_results.append(result)
            
            if inline_results:
                await query.answer(inline_results, cache_time=300)
            else:
                # Send no results message
                no_results_text = {
                    'fa': "❌ هیچ آهنگی یافت نشد.",
                    'en': "❌ No songs found."
                }
                
                result = InlineQueryResultArticle(
                    id="no_results",
                    title=no_results_text.get(lang, no_results_text['en']),
                    input_message_content=InputTextMessageContent(
                        message_text=no_results_text.get(lang, no_results_text['en'])
                    )
                )
                await query.answer([result], cache_time=300)
                
        except Exception as e:
            self.logger.error(f"Inline query error: {e}")
            
            error_text = {
                'fa': "❌ خطا در جستجو. لطفاً دوباره تلاش کنید.",
                'en': "❌ Search error. Please try again."
            }
            
            result = InlineQueryResultArticle(
                id="error",
                title=error_text.get(lang, error_text['en']),
                input_message_content=InputTextMessageContent(
                    message_text=error_text.get(lang, error_text['en'])
                )
            )
            await query.answer([result], cache_time=300)

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        self.logger.error(f"Update {update} caused error {context.error}")
        
        if update and update.effective_message:
            try:
                await update.effective_message.reply_text(
                    "❌ An error occurred. Please try again later."
                )
            except Exception:
                pass

    def setup_handlers(self, application: Application):
        """Setup all handlers"""
        # Command handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        
        # Callback handlers
        application.add_handler(CallbackQueryHandler(self.language_callback, pattern="^lang_"))
        application.add_handler(CallbackQueryHandler(self.edit_callback, pattern="^edit_"))
        application.add_handler(CallbackQueryHandler(self.edit_field_callback, pattern="^edit_field_"))
        
        # Message handlers
        application.add_handler(MessageHandler(filters.AUDIO | filters.VOICE | filters.Document.AUDIO, self.handle_audio_file))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_edit_input))
        
        # Inline query handler
        application.add_handler(InlineQueryHandler(self.inline_query))
        
        # Error handler
        application.add_error_handler(self.error_handler)

    def run(self):
        """Run the bot"""
        # Create application
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        # Setup handlers
        self.setup_handlers(application)
        
        # Set bot commands
        commands = [
            BotCommand("start", "Start the bot / انتخاب زبان"),
            BotCommand("help", "Show help / نمایش راهنما")
        ]
        
        # Start the bot
        self.logger.info("Starting Shazam Telegram Bot...")
        application.run_polling(drop_pending_updates=True)

def main():
    """Main function"""
    bot = ShazamBot()
    bot.run()

if __name__ == "__main__":
    main()
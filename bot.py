#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║              ██████╗ ███████╗██╗   ██╗██╗██╗     ██╗   ██╗██╗███████╗        ║
║              ██╔══██╗██╔════╝╚██╗ ██╔╝██║██║     ██║   ██║██║██╔════╝        ║
║              ██║  ██║█████╗   ╚████╔╝ ██║██║     ██║   ██║██║███████╗        ║
║              ██║  ██║██╔══╝    ╚██╔╝  ██║██║     ██║   ██║██║╚════██║        ║
║              ██████╔╝███████╗   ██║   ██║███████╗╚██████╔╝██║███████║        ║
║              ╚═════╝ ╚══════╝   ╚═╝   ╚═╝╚══════╝ ╚═════╝ ╚═╝╚══════╝        ║
║                                                                               ║
║         SUPER BOT – 100+ TOOLS • AI • MEDIA • UTILITIES • AUTOMATION          ║
║                    with Gift Code Permission System                           ║
║                         Enterprise Telegram Platform                          ║
║                                                                               ║
║         Developer: DK Sharma 🚀                                               ║
║         Admin: @OfficalEarningZone                                            ║
║         Version: 15.0 – "Gift & Permission"                                  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import aiohttp
from aiohttp import ClientTimeout, TCPConnector, web
import aiosqlite
import logging
from logging.handlers import RotatingFileHandler
import sys
import os
import json
import csv
import io
import re
import random
import string
import time
import smtplib
import shutil
import hashlib
import base64
import hmac
import uuid
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from collections import deque, defaultdict
from typing import Optional, List, Dict, Any, Tuple, Union
from functools import wraps
from queue import Queue
from urllib.parse import urlparse
import traceback
import zipfile
import tempfile
from pathlib import Path

# ---------- Third-party libraries ----------
try:
    from PIL import Image, ImageEnhance, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import PyPDF2
    from PyPDF2 import PdfReader, PdfWriter
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    import moviepy.editor as mp
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False

try:
    import qrcode
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = False
except ImportError:
    OPENAI_AVAILABLE = False

# ---------- Telegram & Scheduler ----------
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

# ---------- Optional high-performance modules ----------
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

# ---------- Selenium (optional) ----------
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# ---------- croniter ----------
try:
    from croniter import croniter
except ImportError:
    croniter = None

# ---------- dotenv ----------
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ---------- Environment / Config ----------
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS", "6318083968").split(",")]
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "megabot.log")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY
    OPENAI_AVAILABLE = True
PORT = int(os.getenv("PORT", 8080))

# ---------- Setup Logging ----------
logger = logging.getLogger("SuperBot")
logger.setLevel(getattr(logging, LOG_LEVEL))
console = logging.StreamHandler()
console.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
logger.addHandler(console)
if LOG_FILE:
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(file_handler)

# ---------- Constants ----------
DEFAULT_REFERRAL = os.getenv("DEFAULT_REFERRAL", "1816")
DEFAULT_PASSWORD = "Test@123"
VERIFY_CODE = os.getenv("VERIFY_CODE", "7777")
TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Calcutta")
EM_API_URL = "https://api.earnmigo.com/api/app/user/login/email"
EM_VERIFY_URL = "https://api.earnmigo.com/api/app/user/info"
EM_DB_PATH = "em_registrations.db"
EM_CONCURRENCY = 250
EM_DELAY = 0.002
EM_TURBO_CONCURRENCY = 600
EM_TURBO_DELAY = 0.0

HOLWIN_INVITE = "WLRPSY"
REX_INVITE = "O6NVYX"
HOLWIN_BASE = "https://www.holwin123.top"
HOLWIN_DI = "88dd52c70e7b377527be01c39f5a0a4f"
HOLWIN_VTOKEN = "18667bd921478af5fe5f6506865e4f8a"
REX_BASE = "https://rcapi.rexproearn.com"
REX_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://rch5.rexproearn.com",
    "Referer": "https://rch5.rexproearn.com/",
}
HW_DB_PATH = "holwin_rex.db"

WB_DB_PATH = "whatsapp_unban.db"
WB_DEFAULT_DELAY = 1.0
WB_MAX_RETRIES = 3
WB_BACKUP_INTERVAL = 24
WB_MAX_CONCURRENT_SENDS = 5

# ---------- Utility Functions ----------
def boxed(text: str, title: str = "") -> str:
    lines = text.splitlines()
    max_len = max(len(line) for line in lines) if lines else 0
    top = "┌" + "─" * (max_len + 4) + "┐"
    bottom = "└" + "─" * (max_len + 4) + "┘"
    if title:
        title_line = f"┌─ {title} " + "─" * (max_len - len(title) - 2) + "┐"
        return title_line + "\n" + "\n".join(f"│ {line:<{max_len}} │" for line in lines) + "\n" + bottom
    else:
        return top + "\n" + "\n".join(f"│ {line:<{max_len}} │" for line in lines) + "\n" + bottom

def generate_random_email(domain="mailinator.com"):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + "@" + domain

def generate_random_password(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%", k=length))

def safe_str(obj):
    return str(obj) if obj else ""

def format_timestamp(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else "Never"

# ---------- Database Initialisation ----------
async def init_em_db():
    async with aiosqlite.connect(EM_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        await db.execute('''
            CREATE TABLE IF NOT EXISTS em_registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                password TEXT,
                referral TEXT,
                authorized_key TEXT,
                user_id TEXT,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS em_proxies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proxy TEXT UNIQUE,
                alive INTEGER DEFAULT 1,
                last_used TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS em_schedules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cron_expr TEXT,
                count INTEGER,
                referral TEXT,
                next_run TIMESTAMP,
                active INTEGER DEFAULT 1
            )
        ''')
        await db.commit()

async def init_hw_db():
    async with aiosqlite.connect(HW_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        await db.execute('''
            CREATE TABLE IF NOT EXISTS hw_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                platform TEXT,
                mobile TEXT,
                password TEXT,
                invite_code TEXT,
                registered BOOLEAN DEFAULT 0,
                balance REAL DEFAULT 1000.0,
                email TEXT,
                address TEXT,
                last_daily TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS hw_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                type TEXT,
                amount REAL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS hw_games_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                game TEXT,
                played INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                total_won REAL DEFAULT 0
            )
        ''')
        await db.commit()

async def init_wb_db():
    async with aiosqlite.connect(WB_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        await db.execute('''
            CREATE TABLE IF NOT EXISTS wb_users (
                tid INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                password TEXT,
                reason TEXT DEFAULT 'personal communication',
                delay REAL DEFAULT 1.0,
                approved INTEGER DEFAULT 0,
                email_valid INTEGER DEFAULT 1,
                banned INTEGER DEFAULT 0,
                language TEXT DEFAULT 'en',
                requested_at TIMESTAMP,
                last_active TIMESTAMP,
                total_appeals INTEGER DEFAULT 0,
                success_appeals INTEGER DEFAULT 0,
                failed_appeals INTEGER DEFAULT 0
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS wb_numbers (
                phone TEXT PRIMARY KEY,
                tid INTEGER,
                last_appeal TIMESTAMP,
                appeal_count INTEGER DEFAULT 0,
                blacklisted INTEGER DEFAULT 0,
                custom_reason TEXT,
                FOREIGN KEY(tid) REFERENCES wb_users(tid)
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS wb_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tid INTEGER,
                template TEXT,
                is_default INTEGER DEFAULT 0
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS wb_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tid INTEGER,
                phone TEXT,
                success INTEGER,
                error TEXT,
                sent_at TIMESTAMP,
                template_used TEXT,
                method TEXT
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS wb_scheduler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tid INTEGER,
                cron_expr TEXT,
                interval_minutes INTEGER,
                next_run TIMESTAMP,
                active INTEGER DEFAULT 1,
                last_run TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS wb_proxies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proxy TEXT UNIQUE,
                last_used TIMESTAMP,
                success_count INTEGER DEFAULT 0,
                fail_count INTEGER DEFAULT 0
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS wb_whitelist (
                user_id INTEGER PRIMARY KEY,
                approved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS wb_pending (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS wb_settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        cur = await db.execute("SELECT COUNT(*) FROM wb_templates WHERE is_default=1")
        if (await cur.fetchone())[0] == 0:
            defaults = [
                "Dear WhatsApp Team, my number {number} has been banned. I use it for {reason}. Please unban. Regards, {name}",
                "Hello, I appeal for {number}. It is used for {reason}. Kindly restore. {name}",
                "Respectful request: unban {number}. I am a genuine {reason} user. Thanks, {name}",
                "Urgent: {number} is banned. I follow all rules. Please review. {name}",
                "My account {number} was disabled. I need it for {reason}. Help me. {name}",
            ]
            for t in defaults:
                await db.execute("INSERT INTO wb_templates (tid, template, is_default) VALUES (0, ?, 1)", (t,))
        await db.commit()

async def init_permission_db():
    async with aiosqlite.connect(WB_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        await db.execute('''
            CREATE TABLE IF NOT EXISTS gift_codes (
                code TEXT PRIMARY KEY,
                duration_minutes INTEGER,
                created_by INTEGER,
                used_by INTEGER,
                used_at TIMESTAMP,
                expires_at TIMESTAMP,
                is_used INTEGER DEFAULT 0
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS user_permissions (
                tid INTEGER PRIMARY KEY,
                expires_at TIMESTAMP
            )
        ''')
        await db.commit()

async def init_notes_db():
    async with aiosqlite.connect(WB_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        await db.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tid INTEGER,
                note TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tid INTEGER,
                task TEXT,
                done INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tid INTEGER,
                message TEXT,
                remind_at TIMESTAMP,
                done INTEGER DEFAULT 0
            )
        ''')
        await db.commit()

async def init_all_dbs():
    await init_em_db()
    await init_hw_db()
    await init_wb_db()
    await init_permission_db()
    await init_notes_db()

# ---------- Global State ----------
class GlobalState:
    def __init__(self):
        self.user_modes = {}
        self.em_state = {}
        self.hw_state = {}
        self.wb_state = {}
        self.scheduler = AsyncIOScheduler(timezone="UTC")
        self.em_batch_writer = None
        self.em_proxy_manager = None
        self.wb_proxy_manager = None
        self.wb_auto_engine = None
        self.running_tasks = {}
        self.maintenance_mode = False
        self.config = {
            "auto_backup": True,
            "backup_interval": 24,
            "rate_limit": 5,
            "flood_limit": 10,
        }

global_state = GlobalState()

# ---------- Engine: EarnMigo (EM) ----------
class EMProxyManager:
    def __init__(self):
        self.proxies = []
        self.alive = set()
        self.lock = asyncio.Lock()
        self.check_task = None

    def add_proxy(self, proxy_str: str) -> bool:
        proxy_str = proxy_str.strip()
        if not proxy_str:
            return False
        if "://" not in proxy_str and "@" not in proxy_str and ":" not in proxy_str:
            return False
        self.proxies.append(proxy_str)
        self.alive.add(proxy_str)
        return True

    async def get_proxy(self):
        async with self.lock:
            alive = [p for p in self.proxies if p in self.alive]
            if not alive:
                return None
            return random.choice(alive)

    async def mark_dead(self, proxy_url):
        async with self.lock:
            self.alive.discard(proxy_url)

    async def check_proxy(self, proxy_url: str) -> bool:
        try:
            timeout = ClientTimeout(total=5)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get("https://www.google.com", proxy=proxy_url, timeout=5) as resp:
                    return resp.status == 200
        except:
            return False

    async def check_all_proxies(self):
        while True:
            await asyncio.sleep(300)
            async with self.lock:
                proxies_to_check = self.proxies.copy()
            for p in proxies_to_check:
                ok = await self.check_proxy(p)
                if not ok:
                    await self.mark_dead(p)
                    logger.warning(f"EM Proxy {p} marked dead")

    def start_checker(self):
        if not self.check_task or self.check_task.done():
            self.check_task = asyncio.create_task(self.check_all_proxies())

class EMBatchWriter:
    def __init__(self):
        self.queue = deque()
        self.lock = asyncio.Lock()
        self.running = True
        self.task = None

    async def start(self):
        self.task = asyncio.create_task(self._worker())

    async def _worker(self):
        while self.running:
            await asyncio.sleep(2.0)
            async with self.lock:
                if not self.queue:
                    continue
                batch = list(self.queue)
                self.queue.clear()
            async with aiosqlite.connect(EM_DB_PATH) as db:
                db.row_factory = aiosqlite.Row
                for item in batch:
                    if item[0] == "success":
                        await db.execute(
                            "INSERT OR IGNORE INTO em_registrations (email, password, referral, authorized_key, user_id, status) VALUES (?,?,?,?,?,?)",
                            (item[1], item[2], item[3], item[4], item[5], "success")
                        )
                    else:
                        await db.execute(
                            "INSERT OR IGNORE INTO em_registrations (email, password, referral, status) VALUES (?,?,?,?)",
                            (item[1], item[2], item[3], "fail")
                        )
                await db.commit()

    async def add_success(self, email, password, referral, auth_key, user_id):
        async with self.lock:
            self.queue.append(("success", email, password, referral, auth_key, user_id))

    async def add_fail(self, email, password, referral, error):
        async with self.lock:
            self.queue.append(("fail", email, password, referral, error))

    async def stop(self):
        self.running = False
        if self.task:
            await self.task

class EMEngine:
    def __init__(self):
        self.running = False
        self.paused = False
        self.cancel = False
        self.total = 0
        self.success = 0
        self.fail = 0
        self.processed = 0
        self.referral = DEFAULT_REFERRAL
        self.referral_list = [DEFAULT_REFERRAL]
        self.referral_index = 0
        self.turbo_mode = False
        self.concurrent = EM_CONCURRENCY
        self.delay = EM_DELAY
        self.start_time = None
        self.results = []
        self.proxy_manager = EMProxyManager()
        self.batch_writer = EMBatchWriter()
        self.user_agents = [
            "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.7827.114 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.7827.98 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.7827.91 Mobile Safari/537.36",
        ]
        self._ua_index = 0

    def get_user_agent(self):
        ua = self.user_agents[self._ua_index % len(self.user_agents)]
        self._ua_index += 1
        return ua

    async def register_one(self, session, email, password, referral, proxy=None):
        payload = {
            "email": email,
            "passwd": password,
            "inviter_id": referral,
            "verify_code": VERIFY_CODE,
            "is_h5": True,
            "time_zone": TIME_ZONE,
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": self.get_user_agent(),
            "Origin": "https://www.earnmigo.com",
            "Referer": "https://www.earnmigo.com/"
        }
        for attempt in range(3):
            try:
                async with session.post(EM_API_URL, json=payload, headers=headers, proxy=proxy, timeout=10) as resp:
                    data = await resp.json()
                    if data.get("code") == 0:
                        user = data.get("data", {})
                        return True, email, {
                            "authorized_key": user.get("authorized_key"),
                            "user_id": user.get("id")
                        }
                    else:
                        if resp.status == 429:
                            return False, email, "Rate limit"
                        return False, email, data.get("message", "Unknown error")
            except Exception as e:
                if attempt == 2:
                    return False, email, str(e)
                await asyncio.sleep(0.5 * (attempt + 1))
        return False, email, "Max retries"

    async def run_registration(self, count, referral, progress_callback, email_list=None):
        self.running = True
        self.paused = False
        self.cancel = False
        self.total = count
        self.success = 0
        self.fail = 0
        self.processed = 0
        self.start_time = time.time()
        self.results = []

        connector = TCPConnector(
            limit=self.concurrent,
            limit_per_host=self.concurrent,
            ttl_dns_cache=300,
            enable_cleanup_closed=True,
            force_close=False,
        )
        timeout = ClientTimeout(total=10, connect=3)
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            tasks = []
            for i in range(count):
                if email_list and i < len(email_list):
                    email = email_list[i]
                else:
                    email = generate_random_email()
                if len(self.referral_list) > 1:
                    ref = self.referral_list[self.referral_index % len(self.referral_list)]
                    self.referral_index += 1
                else:
                    ref = referral
                proxy = await self.proxy_manager.get_proxy()
                tasks.append(asyncio.create_task(self.register_one(session, email, DEFAULT_PASSWORD, ref, proxy)))

            for future in asyncio.as_completed(tasks):
                while self.paused and not self.cancel:
                    await asyncio.sleep(0.05)
                if self.cancel:
                    for t in tasks:
                        if not t.done():
                            t.cancel()
                    break

                ok, em, info = await future
                self.processed += 1
                if ok:
                    self.success += 1
                    self.results.append((em, info))
                    await self.batch_writer.add_success(em, DEFAULT_PASSWORD, ref, info.get("authorized_key"), info.get("user_id"))
                else:
                    self.fail += 1
                    await self.batch_writer.add_fail(em, DEFAULT_PASSWORD, ref, info)
                    if "Rate limit" in str(info):
                        await asyncio.sleep(1)
                if self.processed % 100 == 0 or self.processed == count:
                    if progress_callback:
                        await progress_callback(self.processed, self.success, self.fail, count)

        self.running = False

    def em_main_menu(self):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Register", callback_data="em_register")],
            [InlineKeyboardButton("📊 Dashboard", callback_data="em_dashboard")],
            [InlineKeyboardButton("📜 History", callback_data="em_history")],
            [InlineKeyboardButton("⚙️ Settings", callback_data="em_settings"), InlineKeyboardButton("📤 Export", callback_data="em_export")],
            [InlineKeyboardButton("⏸️ Pause", callback_data="em_pause"), InlineKeyboardButton("▶️ Resume", callback_data="em_resume")],
            [InlineKeyboardButton("⏹️ Cancel", callback_data="em_cancel")],
            [InlineKeyboardButton("🎯 Quick Register", callback_data="em_quick")],
            [InlineKeyboardButton("🚀 Turbo Mode", callback_data="em_turbo")],
            [InlineKeyboardButton("🌐 Proxy Manager", callback_data="em_proxy")],
            [InlineKeyboardButton("🔁 Referral List", callback_data="em_referrals")],
            [InlineKeyboardButton("📤 Upload Emails", callback_data="em_upload")],
            [InlineKeyboardButton("⏰ Schedule", callback_data="em_schedule")],
            [InlineKeyboardButton("⬅ Back", callback_data="em_back"), InlineKeyboardButton("🏠 Home", callback_data="home")]
        ])

    def em_settings_menu(self):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("📌 Set Referral", callback_data="em_set_ref")],
            [InlineKeyboardButton("⚡ Concurrency +10", callback_data="em_con_inc"), InlineKeyboardButton("⚡ Concurrency -10", callback_data="em_con_dec")],
            [InlineKeyboardButton("⏱️ Delay +0.01", callback_data="em_delay_inc"), InlineKeyboardButton("⏱️ Delay -0.01", callback_data="em_delay_dec")],
            [InlineKeyboardButton("⬅ Back", callback_data="em_back")]
        ])

    def em_quick_menu(self):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("100", callback_data="em_q_100"), InlineKeyboardButton("500", callback_data="em_q_500")],
            [InlineKeyboardButton("1000", callback_data="em_q_1000"), InlineKeyboardButton("5000", callback_data="em_q_5000")],
            [InlineKeyboardButton("🎛️ Custom", callback_data="em_custom")],
            [InlineKeyboardButton("⬅ Back", callback_data="em_back")]
        ])

    def em_export_menu(self):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("📄 CSV", callback_data="em_export_csv"), InlineKeyboardButton("📄 TXT", callback_data="em_export_txt")],
            [InlineKeyboardButton("📄 JSON", callback_data="em_export_json")],
            [InlineKeyboardButton("⬅ Back", callback_data="em_back")]
        ])

    def em_proxy_menu(self):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Proxy", callback_data="em_add_proxy")],
            [InlineKeyboardButton("🗑️ Clear Proxies", callback_data="em_clear_proxies")],
            [InlineKeyboardButton("👁️ Show Proxies", callback_data="em_show_proxies")],
            [InlineKeyboardButton("⬅ Back", callback_data="em_back")]
        ])

    def em_referral_menu(self):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Referral", callback_data="em_add_ref")],
            [InlineKeyboardButton("🗑️ Clear Referrals", callback_data="em_clear_refs")],
            [InlineKeyboardButton("👁️ Show Referrals", callback_data="em_show_refs")],
            [InlineKeyboardButton("⬅ Back", callback_data="em_back")]
        ])

    async def em_dashboard_text(self, tid):
        total, success, fail = await self.em_stats()
        if self.running and self.total > 0:
            elapsed = time.time() - self.start_time if self.start_time else 0
            rate = self.processed / elapsed if elapsed > 0 else 0
            remaining = (self.total - self.processed) / rate if rate > 0 else 0
            progress = self.processed / self.total * 100
            bar = "█" * int(progress/5) + "░" * (20 - int(progress/5))
            return boxed(
                f"Progress: [{bar}] {progress:.1f}%\n"
                f"✅ Success: {self.success}   ❌ Fail: {self.fail}\n"
                f"⚡ Speed: {rate:.1f}/s\n"
                f"⏳ ETA: {remaining:.0f}s\n"
                f"🕒 Elapsed: {elapsed:.0f}s",
                "EM Dashboard"
            )
        else:
            return boxed(
                f"Status: ⏹️ Idle\n"
                f"Total accounts: {total}\n"
                f"✅ Success: {success}   ❌ Fail: {fail}",
                "EM Dashboard"
            )

    async def em_stats(self):
        async with aiosqlite.connect(EM_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT COUNT(*) FROM em_registrations WHERE status='success'")
            success = (await cur.fetchone())[0]
            cur = await db.execute("SELECT COUNT(*) FROM em_registrations WHERE status='fail'")
            fail = (await cur.fetchone())[0]
            cur = await db.execute("SELECT COUNT(*) FROM em_registrations")
            total = (await cur.fetchone())[0]
            return total, success, fail

    async def em_get_all_success(self):
        async with aiosqlite.connect(EM_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT email, authorized_key, created_at FROM em_registrations WHERE status='success'")
            return await cur.fetchall()

    async def em_get_recent(self, limit=10):
        async with aiosqlite.connect(EM_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT email, authorized_key, created_at FROM em_registrations WHERE status='success' ORDER BY id DESC LIMIT ?", (limit,))
            return await cur.fetchall()

    async def em_clear_db(self):
        async with aiosqlite.connect(EM_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("DELETE FROM em_registrations")
            await db.commit()

    async def em_verify_accounts(self):
        rows = await self.em_get_all_success()
        valid = 0
        invalid = 0
        async with aiohttp.ClientSession() as session:
            for row in rows:
                email = row["email"]
                key = row["authorized_key"]
                headers = {"Authorization": f"Bearer {key}"}
                try:
                    async with session.get(EM_VERIFY_URL, headers=headers, timeout=5) as resp:
                        if resp.status == 200:
                            valid += 1
                        else:
                            invalid += 1
                except:
                    invalid += 1
                await asyncio.sleep(0.1)
        return valid, invalid

# ---------- Engine: Holwin/Rex (HW) ----------
class HWClient:
    def __init__(self, platform):
        self.platform = platform
        self.session = None

    async def __aenter__(self):
        if self.platform == 'holwin':
            headers = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json",
                "Origin": "https://www.holwin123.top",
                "Referer": "https://www.holwin123.top/userRegister",
                "di": HOLWIN_DI,
                "vtoken": HOLWIN_VTOKEN,
            }
        else:
            headers = REX_HEADERS
        self.session = aiohttp.ClientSession(headers=headers)
        return self

    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()

    async def post(self, path, json):
        if self.platform == 'holwin':
            url = f"{HOLWIN_BASE}{path}"
        else:
            url = f"{REX_BASE}{path}"
        async with self.session.post(url, json=json) as resp:
            return await resp.json()

class HWEngine:
    def __init__(self):
        self.invite_codes = {"holwin": HOLWIN_INVITE, "rex": REX_INVITE}

    async def send_sms(self, platform, mobile):
        async with HWClient(platform) as client:
            if platform == 'holwin':
                resp = await client.post("/api/system/sms/send", {"mobile": mobile, "type": "reg_code"})
            else:
                resp = await client.post("/app/user/sendSmsCode", {"mobileNo": mobile})
            return resp

    async def register(self, platform, mobile, otp, password, invite):
        async with HWClient(platform) as client:
            if platform == 'holwin':
                payload = {
                    "mobile": mobile,
                    "authCode": otp,
                    "password": password,
                    "inviteCode": invite,
                    "sourceAppType": "lobby",
                    "registerHost": "www.holwin123.top",
                    "sourceUrl": "https://www.hlowin.link/",
                }
                resp = await client.post("/api/user/register", payload)
                success = resp.get("code") == 0
            else:
                payload = {
                    "mobileNo": mobile,
                    "password": password,
                    "smsCode": otp,
                    "inviteCode": invite,
                }
                resp = await client.post("/app/user/register", payload)
                success = resp.get("code") == 200
            return success, resp

    def hw_main_menu(self, platform=None):
        keyboard = [
            [InlineKeyboardButton("📱 Register", callback_data="hw_register")],
            [InlineKeyboardButton("📊 Balance", callback_data="hw_balance")],
            [InlineKeyboardButton("📜 History", callback_data="hw_history")],
            [InlineKeyboardButton("🔗 Referral", callback_data="hw_referral")],
            [InlineKeyboardButton("🎁 Daily Bonus", callback_data="hw_daily")],
            [InlineKeyboardButton("🎮 Games", callback_data="hw_games")],
            [InlineKeyboardButton("🏆 Leaderboard", callback_data="hw_leaderboard")],
            [InlineKeyboardButton("⚙️ Settings", callback_data="hw_settings")],
            [InlineKeyboardButton("⬅ Back", callback_data="hw_back"), InlineKeyboardButton("🏠 Home", callback_data="home")]
        ]
        return InlineKeyboardMarkup(keyboard)

    def hw_games_menu(self):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Crash", callback_data="hw_game_crash"), InlineKeyboardButton("🎲 Dice", callback_data="hw_game_dice")],
            [InlineKeyboardButton("🎡 Wheel", callback_data="hw_game_wheel"), InlineKeyboardButton("💣 Mine", callback_data="hw_game_mine")],
            [InlineKeyboardButton("🃏 Andar Bahar", callback_data="hw_game_andar"), InlineKeyboardButton("⚖️ Parity", callback_data="hw_game_parity")],
            [InlineKeyboardButton("⬅ Back", callback_data="hw_back")]
        ])

    async def hw_get_user(self, tid):
        async with aiosqlite.connect(HW_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT * FROM hw_users WHERE telegram_id = ?", (tid,))
            return await cur.fetchone()

    async def hw_create_user(self, tid):
        async with aiosqlite.connect(HW_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("INSERT OR IGNORE INTO hw_users (telegram_id) VALUES (?)", (tid,))
            await db.commit()

    async def hw_update_user(self, tid, platform, mobile, password, invite):
        async with aiosqlite.connect(HW_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            await db.execute(
                "UPDATE hw_users SET platform=?, mobile=?, password=?, invite_code=?, registered=1 WHERE telegram_id=?",
                (platform, mobile, password, invite, tid)
            )
            await db.commit()

    async def hw_get_balance(self, tid):
        user = await self.hw_get_user(tid)
        if user:
            return user["balance"]
        return 0.0

    async def hw_add_transaction(self, tid, type, amount, description):
        async with aiosqlite.connect(HW_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            await db.execute(
                "INSERT INTO hw_transactions (user_id, type, amount, description) VALUES (?, ?, ?, ?)",
                (tid, type, amount, description)
            )
            await db.commit()

    async def hw_daily_bonus(self, tid):
        user = await self.hw_get_user(tid)
        if not user:
            return False, "User not found"
        if not user["registered"]:
            return False, "Not registered"
        last = user["last_daily"]
        if last:
            last_dt = datetime.fromisoformat(last)
            if datetime.utcnow() - last_dt < timedelta(days=1):
                return False, "Already claimed today"
        bonus = random.randint(10, 50)
        new_balance = user["balance"] + bonus
        async with aiosqlite.connect(HW_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            await db.execute(
                "UPDATE hw_users SET balance=?, last_daily=? WHERE telegram_id=?",
                (new_balance, datetime.utcnow().isoformat(), tid)
            )
            await db.commit()
        await self.hw_add_transaction(tid, "daily_bonus", bonus, "Daily bonus")
        return True, f"₹{bonus} credited"

    async def hw_leaderboard(self):
        async with aiosqlite.connect(HW_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT mobile, balance FROM hw_users WHERE registered=1 ORDER BY balance DESC LIMIT 10")
            return await cur.fetchall()

    async def hw_play_game(self, tid, game, amount):
        user = await self.hw_get_user(tid)
        if not user or not user["registered"]:
            return None, "Not registered"
        if amount > user["balance"]:
            return None, "Insufficient balance"
        win = 0
        multiplier = 0
        if game == "crash":
            multiplier = random.uniform(1.0, 5.0)
            if random.random() > 0.4:
                win = amount * multiplier
            else:
                win = 0
            result = f"Multiplier: {multiplier:.2f}"
        elif game == "dice":
            dice = random.randint(1, 6)
            win = amount * (dice / 3.5) if dice > 3 else 0
            result = f"Dice: {dice}"
        elif game == "wheel":
            segments = ["red", "black", "green"]
            res = random.choice(segments)
            win = amount * 2 if res == "green" else amount * 0.5
            result = f"Result: {res}"
        elif game == "mine":
            safe = random.random() > 0.3
            win = amount * 3 if safe else 0
            result = "Safe!" if safe else "Boom!"
        elif game == "andar":
            res = random.choice(["Andar", "Bahar"])
            win = amount * 2 if res == "Andar" else 0
            result = f"Result: {res}"
        elif game == "parity":
            num = random.randint(1, 100)
            win = amount * 2 if num % 2 == 0 else 0
            result = f"Number: {num}"
        else:
            return None, "Unknown game"
        new_balance = user["balance"] - amount + win
        async with aiosqlite.connect(HW_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("UPDATE hw_users SET balance = ? WHERE telegram_id = ?", (new_balance, tid))
            await db.commit()
        await self.hw_add_transaction(tid, "game", -amount + win, f"Game {game}")
        await db.execute(
            "INSERT INTO hw_games_stats (user_id, game, played, wins, total_won) VALUES (?, ?, 1, ?, ?) "
            "ON CONFLICT(user_id, game) DO UPDATE SET played=played+1, wins=wins+?, total_won=total_won+?",
            (tid, game, 1 if win > amount else 0, win, 1 if win > amount else 0, win)
        )
        await db.commit()
        return new_balance, f"{result}\nWin: ₹{win:.2f}"

    async def hw_clear_all(self):
        async with aiosqlite.connect(HW_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("DELETE FROM hw_users")
            await db.execute("DELETE FROM hw_transactions")
            await db.execute("DELETE FROM hw_games_stats")
            await db.commit()

# ---------- Engine: WhatsApp Unban (WB) ----------
class WBProxyManager:
    def __init__(self):
        self.proxies = []
        self.lock = asyncio.Lock()
        self.check_task = None

    def add_proxy(self, proxy):
        if proxy not in self.proxies:
            self.proxies.append(proxy)
            return True
        return False

    async def get_proxy(self):
        async with self.lock:
            if self.proxies:
                return random.choice(self.proxies)
            return None

    def mark_dead(self, proxy):
        if proxy in self.proxies:
            self.proxies.remove(proxy)

    async def check_proxy(self, proxy):
        return True

    async def check_all_proxies(self):
        while True:
            await asyncio.sleep(300)

    def start_checker(self):
        if not self.check_task or self.check_task.done():
            self.check_task = asyncio.create_task(self.check_all_proxies())

class WBAutoEngine:
    def __init__(self):
        self.running = {}
        self.lock = asyncio.Lock()

    async def start(self, tid):
        async with self.lock:
            if tid in self.running and self.running[tid]:
                return "Already running"
            self.running[tid] = True
            asyncio.create_task(self._worker(tid))
            return "Auto-send started"

    async def stop(self, tid):
        async with self.lock:
            if tid not in self.running or not self.running[tid]:
                return "Not running"
            self.running[tid] = False
            return "Stopped"

    async def _worker(self, tid):
        user = await self.wb_get_user(tid)
        if not user or user["banned"] or not user["approved"] or not user["email"] or not user["password"]:
            await self.wb_send_message(tid, "❌ Cannot start: missing config or banned/not approved.")
            self.running[tid] = False
            return
        numbers = await self.wb_get_numbers(tid)
        if not numbers:
            await self.wb_send_message(tid, "📭 No numbers.")
            self.running[tid] = False
            return
        while self.running.get(tid, False):
            for num in numbers:
                if not self.running.get(tid, False):
                    break
                if num["blacklisted"]:
                    continue
                phone = num["phone"]
                ok, msg = await self.wb_send_email(tid, phone, user["name"] or "User", user["reason"] or "personal communication", custom_reason=num["custom_reason"])
                if ok:
                    await self.wb_update_last_appeal(phone)
                await self.wb_send_message(tid, f"{'✅' if ok else '❌'} {phone}: {msg}")
                await asyncio.sleep(user["delay"] if user else WB_DEFAULT_DELAY)
        self.running[tid] = False

    async def wb_get_user(self, tid):
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT * FROM wb_users WHERE tid = ?", (tid,))
            return await cur.fetchone()

    async def wb_get_numbers(self, tid):
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT * FROM wb_numbers WHERE tid = ?", (tid,))
            return await cur.fetchall()

    async def wb_update_last_appeal(self, phone):
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("UPDATE wb_numbers SET last_appeal = ?, appeal_count = appeal_count + 1 WHERE phone = ?",
                             (datetime.utcnow().isoformat(), phone))
            await db.commit()

    async def wb_send_email(self, tid, phone, name, reason, custom_reason=None):
        user = await self.wb_get_user(tid)
        if not user or not user["email"] or not user["password"]:
            return False, "Email/password not set"
        if user["banned"] or not user["approved"]:
            return False, "User banned or not approved"
        final_reason = custom_reason if custom_reason else reason
        templates = await self.wb_get_templates(tid, include_default=True)
        if templates:
            template = random.choice(templates)["template"]
        else:
            template = "Dear WhatsApp Team, my number {number} has been banned. I use it for {reason}. Please unban. Regards, {name}"
        body = template.format(number=phone, name=name or "User", reason=final_reason or "personal communication")
        msg = MIMEMultipart()
        msg["From"] = user["email"]
        msg["To"] = "support@whatsapp.com"
        msg["Subject"] = f"Appeal for {phone}"
        msg.attach(MIMEText(body, "plain"))
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(user["email"], user["password"])
            server.send_message(msg)
            server.quit()
            await self.wb_log_appeal(tid, phone, True, "", template, "email")
            return True, "Email sent"
        except Exception as e:
            await self.wb_log_appeal(tid, phone, False, str(e), template, "email")
            return False, str(e)[:40]

    async def wb_get_templates(self, tid, include_default=True):
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            if include_default:
                cur = await db.execute("SELECT id, template FROM wb_templates WHERE tid = ? OR is_default = 1", (tid,))
            else:
                cur = await db.execute("SELECT id, template FROM wb_templates WHERE tid = ?", (tid,))
            return await cur.fetchall()

    async def wb_log_appeal(self, tid, phone, success, error, template, method):
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            await db.execute(
                "INSERT INTO wb_logs (tid, phone, success, error, sent_at, template_used, method) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (tid, phone, 1 if success else 0, error, datetime.utcnow().isoformat(), template, method)
            )
            await db.commit()
            await db.execute("UPDATE wb_users SET total_appeals = total_appeals + 1 WHERE tid = ?", (tid,))
            if success:
                await db.execute("UPDATE wb_users SET success_appeals = success_appeals + 1 WHERE tid = ?", (tid,))
            else:
                await db.execute("UPDATE wb_users SET failed_appeals = failed_appeals + 1 WHERE tid = ?", (tid,))
            await db.commit()

    async def wb_send_message(self, tid, text):
        global bot_app
        if bot_app:
            try:
                await bot_app.bot.send_message(tid, text)
            except:
                pass

    async def wb_submit_webform(self, tid, phone):
        if not SELENIUM_AVAILABLE:
            return False, "Selenium not installed"
        user = await self.wb_get_user(tid)
        if not user or not user["email"]:
            return False, "Email not set"
        name = user["name"] or "User"
        reason = user["reason"] or "personal communication"
        try:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Chrome(options=options)
            driver.get("https://www.whatsapp.com/contact")
            wait = WebDriverWait(driver, 10)
            try:
                dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='combobox']")))
                dropdown.click()
                india = driver.find_element(By.XPATH, "//div[contains(text(), 'India +91')]")
                india.click()
            except:
                pass
            phone_input = driver.find_element(By.NAME, "phoneNumber")
            phone_input.send_keys(phone.replace("+91", ""))
            email_input = driver.find_element(By.NAME, "email")
            email_input.send_keys(user["email"])
            confirm_input = driver.find_element(By.NAME, "confirmEmail")
            confirm_input.send_keys(user["email"])
            android_radio = driver.find_element(By.XPATH, "//input[@value='Android']/..")
            android_radio.click()
            next_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Next Step')]")
            next_btn.click()
            time.sleep(2)
            try:
                textarea = wait.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
                textarea.send_keys(f"My number {phone} is banned. I use it for {reason}. Please review. Thanks, {name}.")
            except:
                pass
            driver.quit()
            await self.wb_log_appeal(tid, phone, True, "", "webform", "webform")
            return True, "Web form submitted (CAPTCHA may appear)"
        except Exception as e:
            return False, str(e)[:50]

    async def wb_clear_all(self):
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("DELETE FROM wb_users")
            await db.execute("DELETE FROM wb_numbers")
            await db.execute("DELETE FROM wb_templates WHERE is_default=0")
            await db.execute("DELETE FROM wb_logs")
            await db.execute("DELETE FROM wb_scheduler")
            await db.execute("DELETE FROM wb_pending")
            await db.execute("DELETE FROM wb_whitelist")
            await db.commit()

    async def wb_export_logs(self, tid):
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT * FROM wb_logs WHERE tid = ? ORDER BY sent_at DESC", (tid,))
            rows = await cur.fetchall()
            if not rows:
                return None
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["ID", "Phone", "Success", "Error", "Sent At", "Template", "Method"])
            for r in rows:
                writer.writerow([r["id"], r["phone"], r["success"], r["error"], r["sent_at"], r["template_used"], r["method"]])
            return output.getvalue()

    async def wb_delete_scheduler(self, job_id):
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("DELETE FROM wb_scheduler WHERE id = ?", (job_id,))
            await db.commit()

    async def wb_get_scheduler_jobs(self, tid):
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT * FROM wb_scheduler WHERE tid = ? AND active = 1", (tid,))
            return await cur.fetchall()

    async def wb_test_email(self, tid):
        user = await self.wb_get_user(tid)
        if not user or not user["email"] or not user["password"]:
            return False, "Email/password not set"
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(user["email"], user["password"])
            server.quit()
            return True, "Login successful"
        except Exception as e:
            return False, str(e)

    async def wb_set_language(self, tid, lang):
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("UPDATE wb_users SET language = ? WHERE tid = ?", (lang, tid))
            await db.commit()

    async def wb_request_approval(self, tid, username):
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("INSERT OR REPLACE INTO wb_pending (user_id, username) VALUES (?, ?)", (tid, username))
            await db.commit()

    async def wb_get_pending(self):
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT * FROM wb_pending ORDER BY requested_at")
            return await cur.fetchall()

    async def wb_approve_user(self, tid):
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("UPDATE wb_users SET approved = 1 WHERE tid = ?", (tid,))
            await db.execute("INSERT OR IGNORE INTO wb_whitelist (user_id) VALUES (?)", (tid,))
            await db.execute("DELETE FROM wb_pending WHERE user_id = ?", (tid,))
            await db.commit()

    async def wb_reject_user(self, tid):
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("DELETE FROM wb_pending WHERE user_id = ?", (tid,))
            await db.commit()

    async def wb_update_user(self, tid, field, value):
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            await db.execute(f"UPDATE wb_users SET {field} = ? WHERE tid = ?", (value, tid))
            await db.commit()

# ---------- Permission Manager ----------
class PermissionManager:
    @staticmethod
    async def has_permission(tid: int) -> bool:
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT expires_at FROM user_permissions WHERE tid = ?", (tid,))
            row = await cur.fetchone()
            if not row:
                return False
            expires_at = datetime.fromisoformat(row["expires_at"])
            return expires_at > datetime.utcnow()

    @staticmethod
    async def get_expiry(tid: int) -> Optional[datetime]:
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT expires_at FROM user_permissions WHERE tid = ?", (tid,))
            row = await cur.fetchone()
            if row:
                return datetime.fromisoformat(row["expires_at"])
            return None

    @staticmethod
    async def grant_permission(tid: int, duration_minutes: int):
        expires_at = datetime.utcnow() + timedelta(minutes=duration_minutes)
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            await db.execute(
                "INSERT OR REPLACE INTO user_permissions (tid, expires_at) VALUES (?, ?)",
                (tid, expires_at.isoformat())
            )
            await db.commit()

    @staticmethod
    async def generate_gift_code(duration_minutes: int, created_by: int) -> str:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        expires_at = datetime.utcnow() + timedelta(minutes=duration_minutes)
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            await db.execute(
                "INSERT INTO gift_codes (code, duration_minutes, created_by, expires_at) VALUES (?, ?, ?, ?)",
                (code, duration_minutes, created_by, expires_at.isoformat())
            )
            await db.commit()
        return code

    @staticmethod
    async def redeem_gift_code(code: str, user_id: int) -> Tuple[bool, str]:
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT * FROM gift_codes WHERE code = ?", (code,))
            row = await cur.fetchone()
            if not row:
                return False, "❌ Invalid gift code."
            if row["is_used"]:
                return False, "❌ This code has already been used."
            expires_at = datetime.fromisoformat(row["expires_at"])
            if expires_at < datetime.utcnow():
                return False, "❌ This code has expired."
            await PermissionManager.grant_permission(user_id, row["duration_minutes"])
            await db.execute(
                "UPDATE gift_codes SET is_used = 1, used_by = ?, used_at = ? WHERE code = ?",
                (user_id, datetime.utcnow().isoformat(), code)
            )
            await db.commit()
            return True, f"✅ Access granted for {row['duration_minutes']} minutes."

# ---------- New Tools (AI, Image, PDF, Text, File) ----------
class AITools:
    @staticmethod
    async def chat(message: str) -> str:
        if not OPENAI_AVAILABLE:
            return "❌ OpenAI not configured."
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": message}],
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"❌ AI error: {e}"

    @staticmethod
    async def summarize(text: str) -> str:
        return await AITools.chat(f"Summarize this in 3 sentences:\n{text}")

    @staticmethod
    async def grammar_fix(text: str) -> str:
        return await AITools.chat(f"Fix grammar and spelling:\n{text}")

class ImageTools:
    @staticmethod
    async def resize(image_bytes, width, height):
        if not PIL_AVAILABLE:
            return None, "PIL not installed."
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img.thumbnail((width, height))
            output = io.BytesIO()
            img.save(output, format="PNG")
            return output.getvalue(), None
        except Exception as e:
            return None, str(e)

    @staticmethod
    async def compress(image_bytes, quality=70):
        if not PIL_AVAILABLE:
            return None, "PIL not installed."
        try:
            img = Image.open(io.BytesIO(image_bytes))
            output = io.BytesIO()
            img.save(output, format="JPEG", quality=quality)
            return output.getvalue(), None
        except Exception as e:
            return None, str(e)

    @staticmethod
    async def blur(image_bytes, radius=2):
        if not PIL_AVAILABLE:
            return None, "PIL not installed."
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img = img.filter(ImageFilter.GaussianBlur(radius))
            output = io.BytesIO()
            img.save(output, format="PNG")
            return output.getvalue(), None
        except Exception as e:
            return None, str(e)

    @staticmethod
    async def rotate(image_bytes, angle):
        if not PIL_AVAILABLE:
            return None, "PIL not installed."
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img = img.rotate(angle, expand=True)
            output = io.BytesIO()
            img.save(output, format="PNG")
            return output.getvalue(), None
        except Exception as e:
            return None, str(e)

class PDFTools:
    @staticmethod
    async def merge(pdfs_data):
        if not PDF_AVAILABLE:
            return None, "PyPDF2 not installed."
        try:
            writer = PdfWriter()
            for data in pdfs_data:
                reader = PdfReader(io.BytesIO(data))
                for page in reader.pages:
                    writer.add_page(page)
            output = io.BytesIO()
            writer.write(output)
            return output.getvalue(), None
        except Exception as e:
            return None, str(e)

    @staticmethod
    async def split(pdf_data, page_numbers):
        if not PDF_AVAILABLE:
            return None, "PyPDF2 not installed."
        try:
            reader = PdfReader(io.BytesIO(pdf_data))
            writer = PdfWriter()
            for i in page_numbers:
                if 0 <= i < len(reader.pages):
                    writer.add_page(reader.pages[i])
            output = io.BytesIO()
            writer.write(output)
            return output.getvalue(), None
        except Exception as e:
            return None, str(e)

class TextTools:
    @staticmethod
    def word_count(text): return len(text.split())
    @staticmethod
    def char_count(text): return len(text)
    @staticmethod
    def reverse(text): return text[::-1]
    @staticmethod
    def upper(text): return text.upper()
    @staticmethod
    def lower(text): return text.lower()
    @staticmethod
    def remove_duplicates(text):
        lines = text.splitlines()
        return "\n".join(dict.fromkeys(lines))
    @staticmethod
    def sort_lines(text):
        lines = text.splitlines()
        return "\n".join(sorted(lines))

class FileTools:
    @staticmethod
    async def zip_files(file_paths, output_path):
        with zipfile.ZipFile(output_path, 'w') as zf:
            for f in file_paths:
                zf.write(f)
        return output_path

    @staticmethod
    async def unzip(zip_path, extract_to):
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(extract_to)
        return extract_to

# ---------- Main Bot ----------
class MegaBot:
    def __init__(self):
        self.app = None
        self.start_time = datetime.now()
        self.em = EMEngine()
        self.hw = HWEngine()
        self.wb_auto = WBAutoEngine()
        self.wb_proxy_manager = WBProxyManager()
        self.wb_engine = self.wb_auto

    async def start(self):
        await init_all_dbs()
        await self.em.batch_writer.start()
        self.em.proxy_manager.start_checker()
        global_state.em_batch_writer = self.em.batch_writer
        global_state.em_proxy_manager = self.em.proxy_manager
        self.wb_proxy_manager.start_checker()
        global_state.wb_proxy_manager = self.wb_proxy_manager
        global_state.wb_auto_engine = self.wb_auto

        self.app = Application.builder().token(BOT_TOKEN) \
            .connect_timeout(10.0).read_timeout(10.0).build()
        global bot_app
        bot_app = self.app

        self._register_handlers()
        global_state.scheduler.start()
        if global_state.config.get("auto_backup"):
            global_state.scheduler.add_job(
                self.auto_backup_job,
                IntervalTrigger(hours=global_state.config.get("backup_interval", 24)),
                id="auto_backup"
            )

        asyncio.create_task(self._run_web_server())

        await self.app.initialize()
        await self.app.start()
        try:
            await asyncio.wait_for(self.app.updater.start_polling(), timeout=60.0)
            logger.info("SuperBot started.")
        except asyncio.TimeoutError:
            logger.error("Polling timeout.")
            return
        while True:
            await asyncio.sleep(1)

    async def _run_web_server(self):
        app = web.Application()
        app.router.add_get("/", self._health_check)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", PORT)
        await site.start()
        logger.info(f"Health check server running on port {PORT}")

    async def _health_check(self, request):
        return web.Response(text="Super Bot is running!", status=200)

    def _register_handlers(self):
        app = self.app
        app.add_handler(CommandHandler("start", self.start_cmd))
        app.add_handler(CommandHandler("help", self.help_cmd))
        app.add_handler(CommandHandler("menu", self.menu_cmd))
        app.add_handler(CommandHandler("cancel", self.cancel_cmd))
        app.add_handler(CommandHandler("request", self.request_cmd))
        app.add_handler(CommandHandler("language", self.language_cmd))
        app.add_handler(CommandHandler("test_email", self.test_email_cmd))
        app.add_handler(CommandHandler("settings", self.settings_cmd))
        app.add_handler(CommandHandler("profile", self.profile_cmd))
        app.add_handler(CommandHandler("feedback", self.feedback_cmd))
        app.add_handler(CommandHandler("admin", self.admin_cmd))
        app.add_handler(CommandHandler("gift", self.gift_cmd))
        app.add_handler(CommandHandler("gen_gift", self.gen_gift_cmd))
        app.add_handler(CommandHandler("approve", self.approve_cmd))
        app.add_handler(CommandHandler("reject", self.reject_cmd))
        app.add_handler(CommandHandler("whitelist", self.whitelist_cmd))
        app.add_handler(CommandHandler("remove", self.remove_whitelist_cmd))
        app.add_handler(CommandHandler("stats", self.stats_cmd))
        app.add_handler(CommandHandler("backup", self.backup_cmd))
        app.add_handler(CommandHandler("restore", self.restore_cmd))
        app.add_handler(CommandHandler("broadcast", self.broadcast_cmd))
        app.add_handler(CommandHandler("list_users", self.list_users_cmd))
        app.add_handler(CommandHandler("clear_em", self.clear_em_cmd))
        app.add_handler(CommandHandler("clear_hw", self.clear_hw_cmd))
        app.add_handler(CommandHandler("clear_wb", self.clear_wb_cmd))
        app.add_handler(CommandHandler("pending", self.pending_cmd))
        app.add_handler(CommandHandler("export_logs", self.export_logs_cmd))
        app.add_handler(CommandHandler("list_schedules", self.list_schedules_cmd))
        app.add_handler(CommandHandler("delete_schedule", self.delete_schedule_cmd))
        app.add_handler(CommandHandler("ban", self.ban_cmd))
        app.add_handler(CommandHandler("unban", self.unban_cmd))
        app.add_handler(CommandHandler("ai", self.ai_chat_cmd))
        app.add_handler(CommandHandler("summarize", self.summarize_cmd))
        app.add_handler(MessageHandler(filters.PHOTO, self.handle_image))
        app.add_handler(MessageHandler(filters.Document.ALL, self.handle_document))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        app.add_handler(CallbackQueryHandler(self.handle_callback))
        app.add_error_handler(self.error_handler)

    # ---------- Permission Check ----------
    async def check_permission(self, update: Update) -> bool:
        tid = update.effective_user.id
        if tid in ADMIN_IDS:
            return True
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT 1 FROM wb_whitelist WHERE user_id = ?", (tid,))
            if await cur.fetchone():
                return True
        has = await PermissionManager.has_permission(tid)
        if not has:
            msg = (
                "⛔ You don't have permission to use this bot.\n\n"
                "Please request access from the administrator or redeem a gift code.\n"
                "• /request - Request access\n"
                "• /gift <code> - Redeem a gift code"
            )
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📨 Request Access", callback_data="request_access")],
                [InlineKeyboardButton("🏠 Home", callback_data="home")]
            ])
            if update.callback_query:
                await update.callback_query.edit_message_text(msg, reply_markup=keyboard)
            else:
                await update.message.reply_text(msg, reply_markup=keyboard)
        return has

    # ---------- Gift Code Commands ----------
    async def gift_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        args = context.args
        if not args:
            await update.message.reply_text("Usage: /gift <code>")
            return
        code = args[0].strip()
        user_id = update.effective_user.id
        success, msg = await PermissionManager.redeem_gift_code(code, user_id)
        await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Home", callback_data="home")]]))

    async def gen_gift_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.")
            return
        args = context.args
        if not args:
            await update.message.reply_text("Usage: /gen_gift <hours>")
            return
        try:
            hours = int(args[0])
            if hours <= 0:
                raise ValueError
        except:
            await update.message.reply_text("❌ Invalid number of hours.")
            return
        duration_minutes = hours * 60
        code = await PermissionManager.generate_gift_code(duration_minutes, update.effective_user.id)
        await update.message.reply_text(
            f"✅ Gift code generated:\n`{code}`\nDuration: {hours} hour(s)\n"
            "Share this code with users. They can redeem it with /gift <code>",
            parse_mode="Markdown"
        )

    # ---------- Navigation ----------
    async def start_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["mode"] = "home"
        user = update.effective_user
        await self._ensure_user(user.id)
        stats = await self._get_user_stats(user.id)
        expiry = await PermissionManager.get_expiry(user.id)
        expiry_str = format_timestamp(expiry) if expiry else "Never / No permission"
        card = boxed(
            f"🟢 Online\n"
            f"👤 @{user.username or 'User'}\n"
            f"🆔 ID: `{user.id}`\n"
            f"📱 Numbers: {stats['total_nums']}\n"
            f"📨 Appeals: {stats['total_appeals']}\n"
            f"✅ Success: {stats['success_appeals']}\n"
            f"❌ Failed: {stats['failed_appeals']}\n"
            f"⚡ Running Jobs: {len(global_state.running_tasks)}\n"
            f"💎 Permission: {'✅ Active' if await PermissionManager.has_permission(user.id) else '❌ None'}\n"
            f"⏳ Expires: {expiry_str}\n"
            f"🕒 Last Active: {stats['last_active']}\n"
            f"━━━━━━━━━━━━━━\n"
            f"💰 HW Balance: ₹{stats['hw_balance']}\n"
            f"📊 EM Accounts: {stats['em_total']} (✅ {stats['em_success']} | ❌ {stats['em_fail']})",
            "🚀 SUPER DASHBOARD"
        )
        await update.message.reply_text(card, parse_mode="Markdown", reply_markup=self.home_keyboard())

    async def _ensure_user(self, tid):
        async with aiosqlite.connect(WB_DB_PATH) as db:
            await db.execute("INSERT OR IGNORE INTO wb_users (tid) VALUES (?)", (tid,))
            await db.commit()

    async def _get_user_stats(self, tid):
        wb_user = await self.wb_auto.wb_get_user(tid)
        nums = await self.wb_auto.wb_get_numbers(tid) if wb_user else []
        hw_user = await self.hw.hw_get_user(tid)
        em_total, em_success, em_fail = await self.em.em_stats()
        return {
            'total_nums': len(nums),
            'total_appeals': wb_user['total_appeals'] if wb_user else 0,
            'success_appeals': wb_user['success_appeals'] if wb_user else 0,
            'failed_appeals': wb_user['failed_appeals'] if wb_user else 0,
            'approved': wb_user['approved'] if wb_user else 0,
            'last_active': wb_user['last_active'] if wb_user else "Never",
            'hw_balance': hw_user['balance'] if hw_user else 0,
            'em_total': em_total,
            'em_success': em_success,
            'em_fail': em_fail,
        }

    def home_keyboard(self):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("🤖 AI Tools", callback_data="menu_ai"),
             InlineKeyboardButton("🖼 Image Tools", callback_data="menu_image")],
            [InlineKeyboardButton("📄 PDF Tools", callback_data="menu_pdf"),
             InlineKeyboardButton("📁 File Tools", callback_data="menu_file")],
            [InlineKeyboardButton("🎥 Video Tools", callback_data="menu_video"),
             InlineKeyboardButton("🎵 Audio Tools", callback_data="menu_audio")],
            [InlineKeyboardButton("📝 Text Tools", callback_data="menu_text"),
             InlineKeyboardButton("🌐 Web Tools", callback_data="menu_web")],
            [InlineKeyboardButton("⚙ Utilities", callback_data="menu_util"),
             InlineKeyboardButton("📊 Dashboard", callback_data="menu_dashboard")],
            [InlineKeyboardButton("👤 Profile", callback_data="profile"),
             InlineKeyboardButton("💎 Premium", callback_data="premium")],
            [InlineKeyboardButton("⚙ Settings", callback_data="settings"),
             InlineKeyboardButton("👑 Admin", callback_data="admin_dashboard")],
            [InlineKeyboardButton("🤖 EarnMigo", callback_data="em_dashboard"),
             InlineKeyboardButton("📈 Holwin/Rex", callback_data="hw_dashboard")],
            [InlineKeyboardButton("📱 WhatsApp Unban", callback_data="wb_dashboard")],
            [InlineKeyboardButton("🔄 Refresh", callback_data="refresh")]
        ])

    # ---------- Tool Menus ----------
    async def show_tool_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE, category: str):
        if not await self.check_permission(update):
            return
        query = update.callback_query
        menus = {
            "ai": ("🤖 AI Tools", [
                ["💬 AI Chat", "ai_chat"],
                ["📝 AI Summarizer", "ai_summarize"],
                ["✍️ Grammar Fix", "ai_grammar"],
            ]),
            "image": ("🖼 Image Tools", [
                ["📐 Resize", "img_resize"],
                ["🗜️ Compress", "img_compress"],
                ["🎨 Blur", "img_blur"],
                ["🔄 Rotate", "img_rotate"],
            ]),
            "pdf": ("📄 PDF Tools", [
                ["📚 Merge", "pdf_merge"],
                ["✂️ Split", "pdf_split"],
            ]),
            "text": ("📝 Text Tools", [
                ["📊 Word Count", "txt_wordcount"],
                ["📊 Character Count", "txt_charcount"],
                ["🔁 Reverse", "txt_reverse"],
                ["🔠 Uppercase", "txt_upper"],
                ["🔡 Lowercase", "txt_lower"],
                ["🧹 Remove Duplicates", "txt_remove_dups"],
                ["🔃 Sort Lines", "txt_sort"],
                ["🔑 Password Generator", "txt_password"],
            ]),
            "file": ("📁 File Tools", [
                ["📦 ZIP", "file_zip"],
                ["📂 Unzip", "file_unzip"],
            ]),
            "util": ("⚙ Utilities", [
                ["📝 Notes", "util_notes"],
                ["✅ Todo", "util_todo"],
                ["⏰ Reminder", "util_reminder"],
                ["🧮 Calculator", "util_calculator"],
            ]),
        }
        if category not in menus:
            await query.edit_message_text("❌ Category not found.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Home", callback_data="home")]]))
            return
        title, buttons = menus[category]
        keyboard = []
        for row in buttons:
            keyboard.append([InlineKeyboardButton(row[0], callback_data=row[1])])
        keyboard.append([InlineKeyboardButton("⬅ Back", callback_data="home")])
        await query.edit_message_text(f"{title}\n\nChoose a tool:", reply_markup=InlineKeyboardMarkup(keyboard))

    # ---------- Tool Actions ----------
    async def ai_tool_action(self, update: Update, context: ContextTypes.DEFAULT_TYPE, action: str):
        if not await self.check_permission(update):
            return
        query = update.callback_query
        if action == "ai_chat":
            await query.edit_message_text("💬 Send a message to chat with AI.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["ai_mode"] = "chat"
        elif action == "ai_summarize":
            await query.edit_message_text("📝 Send text to summarize.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["ai_mode"] = "summarize"
        elif action == "ai_grammar":
            await query.edit_message_text("✍️ Send text to fix grammar.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["ai_mode"] = "grammar"
        else:
            await query.edit_message_text("⏳ Tool coming soon.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="home")]]))

    async def image_tool_action(self, update: Update, context: ContextTypes.DEFAULT_TYPE, action: str):
        if not await self.check_permission(update):
            return
        query = update.callback_query
        if action == "img_resize":
            await query.edit_message_text("📐 Send a photo and specify width,height in caption (e.g., 300,400)", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["img_mode"] = "resize"
        elif action == "img_compress":
            await query.edit_message_text("🗜️ Send a photo to compress.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["img_mode"] = "compress"
        elif action == "img_blur":
            await query.edit_message_text("🎨 Send a photo to blur.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["img_mode"] = "blur"
        elif action == "img_rotate":
            await query.edit_message_text("🔄 Send a photo and angle in caption (e.g., 90)", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["img_mode"] = "rotate"
        else:
            await query.edit_message_text("⏳ Tool coming soon.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="home")]]))

    async def pdf_tool_action(self, update: Update, context: ContextTypes.DEFAULT_TYPE, action: str):
        if not await self.check_permission(update):
            return
        query = update.callback_query
        if action == "pdf_merge":
            await query.edit_message_text("📚 Send multiple PDF files (as documents) to merge. Type /done when finished.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Done", callback_data="pdf_merge_done"), InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["pdf_mode"] = "merge"
            context.user_data["pdf_files"] = []
        elif action == "pdf_split":
            await query.edit_message_text("✂️ Send a PDF file and specify page numbers in caption (e.g., 1,3,5)", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["pdf_mode"] = "split"
        else:
            await query.edit_message_text("⏳ Tool coming soon.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="home")]]))

    async def text_tool_action(self, update: Update, context: ContextTypes.DEFAULT_TYPE, action: str):
        if not await self.check_permission(update):
            return
        query = update.callback_query
        context.user_data["txt_mode"] = action
        await query.edit_message_text("📝 Send the text to process.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))

    # ---------- Message Handlers ----------
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        text = update.message.text
        mode = context.user_data.get("mode", "home")

        if context.user_data.get("ai_mode"):
            if not await self.check_permission(update):
                return
            ai_mode = context.user_data.pop("ai_mode", None)
            if ai_mode == "chat":
                result = await AITools.chat(text)
                await update.message.reply_text(result, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="home")]]))
            elif ai_mode == "summarize":
                result = await AITools.summarize(text)
                await update.message.reply_text(result, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="home")]]))
            elif ai_mode == "grammar":
                result = await AITools.grammar_fix(text)
                await update.message.reply_text(result, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="home")]]))
            else:
                await update.message.reply_text("❌ Unknown AI mode.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Home", callback_data="home")]]))
            return

        if context.user_data.get("txt_mode"):
            if not await self.check_permission(update):
                return
            txt_mode = context.user_data.pop("txt_mode", None)
            if txt_mode == "txt_wordcount":
                wc = TextTools.word_count(text)
                await update.message.reply_text(f"📊 Word count: {wc}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="home")]]))
            elif txt_mode == "txt_charcount":
                cc = TextTools.char_count(text)
                await update.message.reply_text(f"📊 Character count: {cc}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="home")]]))
            elif txt_mode == "txt_reverse":
                await update.message.reply_text(f"🔁 Reversed:\n{TextTools.reverse(text)}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="home")]]))
            elif txt_mode == "txt_upper":
                await update.message.reply_text(f"🔠 Uppercase:\n{TextTools.upper(text)}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="home")]]))
            elif txt_mode == "txt_lower":
                await update.message.reply_text(f"🔡 Lowercase:\n{TextTools.lower(text)}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="home")]]))
            elif txt_mode == "txt_remove_dups":
                await update.message.reply_text(f"🧹 Without duplicates:\n{TextTools.remove_duplicates(text)}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="home")]]))
            elif txt_mode == "txt_sort":
                await update.message.reply_text(f"🔃 Sorted:\n{TextTools.sort_lines(text)}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="home")]]))
            elif txt_mode == "txt_password":
                length = 12
                try:
                    length = int(text.strip())
                except:
                    pass
                pwd = generate_random_password(length)
                await update.message.reply_text(f"🔑 Password:\n`{pwd}`", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="home")]]))
            else:
                await update.message.reply_text("❌ Unknown text tool.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Home", callback_data="home")]]))
            return

        if mode == "em":
            await self.em_handle_text(update, context)
        elif mode == "hw":
            await self.hw_handle_text(update, context)
        elif mode == "wb":
            await self.wb_handle_text(update, context)
        else:
            await update.message.reply_text("Use the buttons.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Home", callback_data="home")]]))

    async def handle_image(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_permission(update):
            return
        if context.user_data.get("img_mode"):
            img_mode = context.user_data.pop("img_mode", None)
            photo = update.message.photo[-1]
            file = await photo.get_file()
            img_bytes = await file.download_as_bytearray()
            if img_mode == "resize":
                try:
                    cap = update.message.caption or ""
                    parts = cap.split(",")
                    width, height = int(parts[0].strip()), int(parts[1].strip())
                    result, err = await ImageTools.resize(img_bytes, width, height)
                    if err:
                        await update.message.reply_text(f"❌ {err}")
                    else:
                        await update.message.reply_document(document=io.BytesIO(result), filename="resized.png", caption="✅ Resized")
                except:
                    await update.message.reply_text("❌ Invalid dimensions. Use: width,height (e.g., 300,400)")
            elif img_mode == "compress":
                result, err = await ImageTools.compress(img_bytes)
                if err:
                    await update.message.reply_text(f"❌ {err}")
                else:
                    await update.message.reply_document(document=io.BytesIO(result), filename="compressed.jpg", caption="✅ Compressed")
            elif img_mode == "blur":
                result, err = await ImageTools.blur(img_bytes)
                if err:
                    await update.message.reply_text(f"❌ {err}")
                else:
                    await update.message.reply_document(document=io.BytesIO(result), filename="blurred.png", caption="✅ Blurred")
            elif img_mode == "rotate":
                try:
                    angle = int(update.message.caption or "90")
                    result, err = await ImageTools.rotate(img_bytes, angle)
                    if err:
                        await update.message.reply_text(f"❌ {err}")
                    else:
                        await update.message.reply_document(document=io.BytesIO(result), filename="rotated.png", caption=f"✅ Rotated {angle}°")
                except:
                    await update.message.reply_text("❌ Invalid angle.")
            else:
                await update.message.reply_text("❌ Unknown image mode.")
            await update.message.reply_text("Done.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="home")]]))
            return
        await update.message.reply_text("Image received. Use image tools.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="home")]]))

    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_permission(update):
            return
        doc = update.message.document
        file = await doc.get_file()
        file_bytes = await file.download_as_bytearray()
        file_name = doc.file_name or "file"

        if context.user_data.get("pdf_mode") == "merge":
            context.user_data["pdf_files"].append(file_bytes)
            await update.message.reply_text(f"📄 Added {file_name}. Send more or click Done.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Done", callback_data="pdf_merge_done"), InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            return
        if context.user_data.get("pdf_mode") == "split":
            cap = update.message.caption or ""
            pages = [int(x.strip()) for x in cap.split(",") if x.strip().isdigit()]
            if not pages:
                await update.message.reply_text("❌ Specify page numbers in caption (e.g., 1,3,5)")
                return
            result, err = await PDFTools.split(file_bytes, pages)
            if err:
                await update.message.reply_text(f"❌ {err}")
            else:
                await update.message.reply_document(document=io.BytesIO(result), filename="split.pdf", caption="✅ Split PDF")
            context.user_data.pop("pdf_mode", None)
            return

        await update.message.reply_text("📎 File received. Use file tools.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="home")]]))

    # ---------- Callback Router ----------
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        data = query.data
        user_id = update.effective_user.id

        if data == "request_access":
            username = update.effective_user.username or "Unknown"
            await self.wb_auto.wb_request_approval(user_id, username)
            await query.edit_message_text("✅ Request sent to admin. You will be notified when approved.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Home", callback_data="home")]]))
            for admin in ADMIN_IDS:
                try:
                    await self.app.bot.send_message(admin, f"📨 *New Access Request*\nUser: @{username} (ID: {user_id})\nUse /pending to view.", parse_mode="Markdown")
                except:
                    pass
            return

        if data.startswith("em_"):
            await self.em_callback(update, context)
            return
        if data.startswith("hw_"):
            await self.hw_callback(update, context)
            return
        if data.startswith("wb_"):
            await self.wb_callback(update, context)
            return
        if data.startswith("admin_"):
            await self.admin_callback(update, context)
            return

        if data == "home":
            await self.start_cmd(update, context)
            return
        if data == "refresh":
            await self.start_cmd(update, context)
            return
        if data == "profile":
            await self.profile_cmd(update, context)
            return
        if data == "settings":
            await self.settings_cmd(update, context)
            return
        if data == "premium":
            await query.edit_message_text("💎 Premium features – coming soon.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="home")]]))
            return
        if data == "admin_dashboard":
            await self.admin_cmd(update, context)
            return
        if data == "em_dashboard":
            await self.show_em(update, context)
            return
        if data == "hw_dashboard":
            await self.show_hw(update, context)
            return
        if data == "wb_dashboard":
            await self.show_wb(update, context)
            return
        if data == "menu_dashboard":
            await self.start_cmd(update, context)
            return
        if data == "cancel":
            context.user_data.pop("ai_mode", None)
            context.user_data.pop("img_mode", None)
            context.user_data.pop("pdf_mode", None)
            context.user_data.pop("txt_mode", None)
            await query.edit_message_text("✅ Cancelled.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Home", callback_data="home")]]))
            return

        if data.startswith("menu_"):
            category = data.split("_")[1]
            await self.show_tool_menu(update, context, category)
            return

        if data.startswith("ai_"):
            await self.ai_tool_action(update, context, data)
            return
        if data.startswith("img_"):
            await self.image_tool_action(update, context, data)
            return
        if data.startswith("pdf_"):
            await self.pdf_tool_action(update, context, data)
            return
        if data.startswith("txt_"):
            await self.text_tool_action(update, context, data)
            return

        if data == "pdf_merge_done":
            pdf_files = context.user_data.get("pdf_files", [])
            if len(pdf_files) < 2:
                await query.edit_message_text("❌ Need at least 2 PDF files to merge.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="home")]]))
                return
            result, err = await PDFTools.merge(pdf_files)
            if err:
                await query.edit_message_text(f"❌ {err}")
            else:
                await query.edit_message_text("✅ Merged PDF ready.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📄 Download", callback_data="pdf_download_merge")]]))
                context.user_data["pdf_merge_result"] = result
            context.user_data.pop("pdf_files", None)
            context.user_data.pop("pdf_mode", None)
            return

        await query.edit_message_text("❌ Unknown action.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Home", callback_data="home")]]))

    # ---------- Engine Callbacks (FULL IMPLEMENTATION) ----------
    async def show_em(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_permission(update):
            return
        query = update.callback_query
        text = boxed(
            "🤖 *EarnMigo Registration Engine*\n\n"
            "Bulk register accounts with referral codes.\n"
            "Configure settings and start.",
            "EarnMigo"
        )
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=self.em.em_main_menu())

    async def show_hw(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_permission(update):
            return
        query = update.callback_query
        user_id = update.effective_user.id
        await self.hw.hw_create_user(user_id)
        text = boxed(
            "📈 *Holwin / Rexproearn Engine*\n\n"
            "Register on these platforms using your invite codes.\n"
            "Earn rewards and play games.",
            "Holwin/Rex"
        )
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=self.hw.hw_main_menu())

    async def show_wb(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_permission(update):
            return
        query = update.callback_query
        user_id = update.effective_user.id
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("INSERT OR IGNORE INTO wb_users (tid) VALUES (?)", (user_id,))
            await db.commit()
        text = boxed(
            "📱 *WhatsApp Unban Engine*\n\n"
            "Automate ban appeals via email and web forms.\n"
            "Add numbers, set templates, and start sending.",
            "WhatsApp Unban"
        )
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=self.wb_main_menu())

    def wb_main_menu(self):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Number", callback_data="wb_add")],
            [InlineKeyboardButton("📋 My Numbers", callback_data="wb_list")],
            [InlineKeyboardButton("📤 Appeal All", callback_data="wb_appeal_all")],
            [InlineKeyboardButton("📤 Appeal One", callback_data="wb_appeal_one")],
            [InlineKeyboardButton("🚀 Mass Appeal", callback_data="wb_mass")],
            [InlineKeyboardButton("🔁 Auto-Send", callback_data="wb_auto")],
            [InlineKeyboardButton("🛑 Stop Auto", callback_data="wb_stop_auto")],
            [InlineKeyboardButton("🌐 Web Form", callback_data="wb_webform")],
            [InlineKeyboardButton("📝 Templates", callback_data="wb_templates")],
            [InlineKeyboardButton("⏰ Scheduler", callback_data="wb_scheduler")],
            [InlineKeyboardButton("📊 Dashboard", callback_data="wb_stats")],
            [InlineKeyboardButton("⚙️ Settings", callback_data="wb_settings")],
            [InlineKeyboardButton("⬅ Back", callback_data="wb_back"), InlineKeyboardButton("🏠 Home", callback_data="home")]
        ])

    # ---------- EM Callbacks ----------
    async def em_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_permission(update):
            return
        query = update.callback_query
        data = query.data
        user_id = update.effective_user.id

        if data == "em_register":
            await query.edit_message_text("📧 Send the number of accounts to register (e.g., 10) or upload a CSV of emails (optional).", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["em_state"] = "awaiting_count"
            return

        elif data == "em_dashboard":
            text = await self.em.em_dashboard_text(user_id)
            await query.edit_message_text(text, parse_mode="Markdown", reply_markup=self.em.em_main_menu())
            return

        elif data == "em_history":
            recent = await self.em.em_get_recent(10)
            if not recent:
                await query.edit_message_text("📭 No history yet.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="em_dashboard")]]))
                return
            lines = ["📜 *Recent Registrations*"]
            for r in recent:
                lines.append(f"📧 {r['email']} | Key: `{r['authorized_key'][:8]}...` | {r['created_at']}")
            await query.edit_message_text("\n".join(lines), parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="em_dashboard")]]))
            return

        elif data == "em_settings":
            await query.edit_message_text("⚙️ *EM Settings*", parse_mode="Markdown", reply_markup=self.em.em_settings_menu())
            return

        elif data == "em_export":
            await query.edit_message_text("📤 *Export Options*", parse_mode="Markdown", reply_markup=self.em.em_export_menu())
            return

        elif data == "em_pause":
            if self.em.running:
                self.em.paused = True
                await query.edit_message_text("⏸️ Paused.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("▶️ Resume", callback_data="em_resume")]]))
            else:
                await query.edit_message_text("No active registration.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="em_dashboard")]]))
            return

        elif data == "em_resume":
            if self.em.running:
                self.em.paused = False
                await query.edit_message_text("▶️ Resumed.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⏸️ Pause", callback_data="em_pause")]]))
            else:
                await query.edit_message_text("No active registration.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="em_dashboard")]]))
            return

        elif data == "em_cancel":
            if self.em.running:
                self.em.cancel = True
                await query.edit_message_text("⏹️ Cancelled.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="em_dashboard")]]))
            else:
                await query.edit_message_text("No active registration.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="em_dashboard")]]))
            return

        elif data == "em_quick":
            await query.edit_message_text("🎯 *Quick Register*", parse_mode="Markdown", reply_markup=self.em.em_quick_menu())
            return

        elif data.startswith("em_q_"):
            count = int(data.split("_")[2])
            context.user_data["em_count"] = count
            context.user_data["em_referral"] = self.em.referral
            await query.edit_message_text(f"🚀 Starting registration for {count} accounts...\nReferral: {self.em.referral}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⏹️ Cancel", callback_data="em_cancel")]]))
            asyncio.create_task(self.em.run_registration(count, self.em.referral, self.em_progress_callback, None))
            return

        elif data == "em_custom":
            await query.edit_message_text("📧 Send the number of accounts to register.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["em_state"] = "awaiting_custom_count"
            return

        elif data == "em_turbo":
            self.em.turbo_mode = not self.em.turbo_mode
            self.em.concurrent = EM_TURBO_CONCURRENCY if self.em.turbo_mode else EM_CONCURRENCY
            self.em.delay = EM_TURBO_DELAY if self.em.turbo_mode else EM_DELAY
            status = "✅ Turbo ON" if self.em.turbo_mode else "✅ Turbo OFF"
            await query.edit_message_text(f"{status}\nConcurrency: {self.em.concurrent}\nDelay: {self.em.delay}s", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="em_dashboard")]]))
            return

        elif data == "em_proxy":
            await query.edit_message_text("🌐 *Proxy Manager*", parse_mode="Markdown", reply_markup=self.em.em_proxy_menu())
            return

        elif data == "em_referrals":
            await query.edit_message_text("🔁 *Referral List*\nCurrent: " + ", ".join(self.em.referral_list), parse_mode="Markdown", reply_markup=self.em.em_referral_menu())
            return

        elif data == "em_upload":
            await query.edit_message_text("📤 Upload a CSV or TXT file with emails (one per line).", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["em_state"] = "awaiting_upload"
            return

        elif data == "em_schedule":
            await query.edit_message_text("⏰ *Schedule Registration*\nSend cron expression (e.g., '0 0 * * *') and count.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["em_state"] = "awaiting_schedule"
            return

        elif data == "em_back":
            await self.show_em(update, context)
            return

        elif data == "em_set_ref":
            await query.edit_message_text("📌 Send new referral code.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["em_state"] = "set_ref"
            return

        elif data == "em_con_inc":
            self.em.concurrent = min(1000, self.em.concurrent + 10)
            await query.edit_message_text(f"⚡ Concurrency: {self.em.concurrent}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="em_settings")]]))
            return

        elif data == "em_con_dec":
            self.em.concurrent = max(10, self.em.concurrent - 10)
            await query.edit_message_text(f"⚡ Concurrency: {self.em.concurrent}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="em_settings")]]))
            return

        elif data == "em_delay_inc":
            self.em.delay = round(self.em.delay + 0.01, 3)
            await query.edit_message_text(f"⏱️ Delay: {self.em.delay}s", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="em_settings")]]))
            return

        elif data == "em_delay_dec":
            self.em.delay = max(0, round(self.em.delay - 0.01, 3))
            await query.edit_message_text(f"⏱️ Delay: {self.em.delay}s", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="em_settings")]]))
            return

        elif data == "em_export_csv":
            rows = await self.em.em_get_all_success()
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["Email", "Authorized Key", "Created At"])
            for r in rows:
                writer.writerow([r["email"], r["authorized_key"], r["created_at"]])
            await query.edit_message_text("✅ CSV ready.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📄 Download", callback_data="em_download_csv")]]))
            context.user_data["em_export_csv"] = output.getvalue()
            return

        elif data == "em_export_txt":
            rows = await self.em.em_get_all_success()
            lines = [f"{r['email']}:{r['authorized_key']}" for r in rows]
            await query.edit_message_text("✅ TXT ready.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📄 Download", callback_data="em_download_txt")]]))
            context.user_data["em_export_txt"] = "\n".join(lines)
            return

        elif data == "em_export_json":
            rows = await self.em.em_get_all_success()
            await query.edit_message_text("✅ JSON ready.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📄 Download", callback_data="em_download_json")]]))
            context.user_data["em_export_json"] = json.dumps([dict(r) for r in rows], indent=2)
            return

        elif data == "em_add_proxy":
            await query.edit_message_text("🌐 Send proxy in format: http://user:pass@host:port", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["em_state"] = "add_proxy"
            return

        elif data == "em_clear_proxies":
            self.em.proxy_manager.proxies.clear()
            self.em.proxy_manager.alive.clear()
            await query.edit_message_text("🗑️ Proxies cleared.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="em_proxy")]]))
            return

        elif data == "em_show_proxies":
            proxies = self.em.proxy_manager.proxies
            if not proxies:
                await query.edit_message_text("📭 No proxies.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="em_proxy")]]))
                return
            await query.edit_message_text("🌐 Proxies:\n" + "\n".join(proxies), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="em_proxy")]]))
            return

        elif data == "em_add_ref":
            await query.edit_message_text("🔁 Send new referral code.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["em_state"] = "add_ref"
            return

        elif data == "em_clear_refs":
            self.em.referral_list = [DEFAULT_REFERRAL]
            await query.edit_message_text("🗑️ Referrals cleared. Reset to default.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="em_referrals")]]))
            return

        elif data == "em_show_refs":
            await query.edit_message_text("🔁 Referrals:\n" + "\n".join(self.em.referral_list), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="em_referrals")]]))
            return

        elif data == "em_download_csv":
            csv_data = context.user_data.get("em_export_csv", "")
            if not csv_data:
                await query.edit_message_text("❌ No data.")
                return
            await query.message.reply_document(document=io.BytesIO(csv_data.encode()), filename="em_accounts.csv", caption="✅ Export")
            context.user_data.pop("em_export_csv", None)
            return

        elif data == "em_download_txt":
            txt_data = context.user_data.get("em_export_txt", "")
            if not txt_data:
                await query.edit_message_text("❌ No data.")
                return
            await query.message.reply_document(document=io.BytesIO(txt_data.encode()), filename="em_accounts.txt", caption="✅ Export")
            context.user_data.pop("em_export_txt", None)
            return

        elif data == "em_download_json":
            json_data = context.user_data.get("em_export_json", "")
            if not json_data:
                await query.edit_message_text("❌ No data.")
                return
            await query.message.reply_document(document=io.BytesIO(json_data.encode()), filename="em_accounts.json", caption="✅ Export")
            context.user_data.pop("em_export_json", None)
            return

        else:
            await query.edit_message_text("❌ Unknown EM action.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="em_dashboard")]]))

    async def em_progress_callback(self, processed, success, fail, total):
        pass

    async def em_handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_permission(update):
            return
        text = update.message.text.strip()
        state = context.user_data.get("em_state")
        if state == "awaiting_count":
            try:
                count = int(text)
                if count <= 0:
                    raise ValueError
                context.user_data["em_count"] = count
                context.user_data["em_referral"] = self.em.referral
                await update.message.reply_text(f"🚀 Starting registration for {count} accounts...\nReferral: {self.em.referral}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⏹️ Cancel", callback_data="em_cancel")]]))
                asyncio.create_task(self.em.run_registration(count, self.em.referral, self.em_progress_callback, None))
                context.user_data.pop("em_state", None)
            except:
                await update.message.reply_text("❌ Please enter a valid number.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            return
        elif state == "awaiting_custom_count":
            try:
                count = int(text)
                if count <= 0:
                    raise ValueError
                context.user_data["em_count"] = count
                context.user_data["em_referral"] = self.em.referral
                await update.message.reply_text(f"🚀 Starting registration for {count} accounts...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⏹️ Cancel", callback_data="em_cancel")]]))
                asyncio.create_task(self.em.run_registration(count, self.em.referral, self.em_progress_callback, None))
                context.user_data.pop("em_state", None)
            except:
                await update.message.reply_text("❌ Please enter a valid number.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            return
        elif state == "set_ref":
            if text.isalnum():
                self.em.referral = text
                await update.message.reply_text(f"✅ Referral set to {text}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="em_settings")]]))
            else:
                await update.message.reply_text("❌ Invalid referral code.")
            context.user_data.pop("em_state", None)
            return
        elif state == "add_ref":
            if text.isalnum():
                self.em.referral_list.append(text)
                await update.message.reply_text(f"✅ Added {text}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="em_referrals")]]))
            else:
                await update.message.reply_text("❌ Invalid referral code.")
            context.user_data.pop("em_state", None)
            return
        elif state == "add_proxy":
            if self.em.proxy_manager.add_proxy(text):
                await update.message.reply_text("✅ Proxy added.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="em_proxy")]]))
            else:
                await update.message.reply_text("❌ Invalid proxy format.")
            context.user_data.pop("em_state", None)
            return
        elif state == "awaiting_upload":
            await update.message.reply_text("Please upload a file.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data.pop("em_state", None)
            return
        elif state == "awaiting_schedule":
            parts = text.split()
            if len(parts) != 2:
                await update.message.reply_text("❌ Usage: <cron> <count>\nExample: '0 0 * * * 100'")
                return
            cron_expr, count_str = parts[0], parts[1]
            try:
                count = int(count_str)
                if not croniter.is_valid(cron_expr):
                    raise ValueError
                async with aiosqlite.connect(EM_DB_PATH) as db:
                    db.row_factory = aiosqlite.Row
                    await db.execute("INSERT INTO em_schedules (cron_expr, count, referral, next_run, active) VALUES (?, ?, ?, ?, 1)",
                                     (cron_expr, count, self.em.referral, datetime.utcnow().isoformat()))
                    await db.commit()
                await update.message.reply_text(f"✅ Schedule added: {cron_expr} with {count} accounts.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="em_dashboard")]]))
            except:
                await update.message.reply_text("❌ Invalid cron or count.")
            context.user_data.pop("em_state", None)
            return
        else:
            await update.message.reply_text("❌ Unknown state. Use the buttons.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="em_dashboard")]]))

    # ---------- HW Callbacks ----------
    async def hw_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_permission(update):
            return
        query = update.callback_query
        data = query.data
        user_id = update.effective_user.id

        if data == "hw_register":
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📱 Holwin", callback_data="hw_reg_holwin")],
                [InlineKeyboardButton("📱 Rexproearn", callback_data="hw_reg_rex")],
                [InlineKeyboardButton("⬅ Back", callback_data="hw_dashboard")]
            ])
            await query.edit_message_text("Select platform:", reply_markup=keyboard)
            return

        elif data.startswith("hw_reg_"):
            platform = data.split("_")[2]
            await query.edit_message_text(f"📱 Enter your mobile number for {platform} (with country code, e.g., 91XXXXXXXXXX):", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["hw_platform"] = platform
            context.user_data["hw_state"] = "awaiting_mobile"
            return

        elif data == "hw_balance":
            user = await self.hw.hw_get_user(user_id)
            if not user or not user["registered"]:
                await query.edit_message_text("❌ You are not registered.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="hw_dashboard")]]))
                return
            bal = await self.hw.hw_get_balance(user_id)
            await query.edit_message_text(f"💰 Your balance: ₹{bal:.2f}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="hw_dashboard")]]))
            return

        elif data == "hw_history":
            user = await self.hw.hw_get_user(user_id)
            if not user or not user["registered"]:
                await query.edit_message_text("❌ Not registered.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="hw_dashboard")]]))
                return
            async with aiosqlite.connect(HW_DB_PATH) as db:
                db.row_factory = aiosqlite.Row
                cur = await db.execute("SELECT * FROM hw_transactions WHERE user_id = ? ORDER BY created_at DESC LIMIT 10", (user_id,))
                rows = await cur.fetchall()
            if not rows:
                await query.edit_message_text("📭 No transactions.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="hw_dashboard")]]))
                return
            lines = ["📜 *Recent Transactions*"]
            for r in rows:
                lines.append(f"{r['type']}: {r['amount']:.2f} | {r['description']} | {r['created_at']}")
            await query.edit_message_text("\n".join(lines), parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="hw_dashboard")]]))
            return

        elif data == "hw_referral":
            user = await self.hw.hw_get_user(user_id)
            if not user or not user["registered"]:
                await query.edit_message_text("❌ Not registered.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="hw_dashboard")]]))
                return
            await query.edit_message_text(f"🔗 Your invite code: {user['invite_code']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="hw_dashboard")]]))
            return

        elif data == "hw_daily":
            ok, msg = await self.hw.hw_daily_bonus(user_id)
            await query.edit_message_text(f"{'✅' if ok else '❌'} {msg}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="hw_dashboard")]]))
            return

        elif data == "hw_games":
            await query.edit_message_text("🎮 *Games*", parse_mode="Markdown", reply_markup=self.hw.hw_games_menu())
            return

        elif data.startswith("hw_game_"):
            game = data.split("_")[2]
            await query.edit_message_text(f"🎮 {game.capitalize()} - Enter bet amount:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["hw_game"] = game
            context.user_data["hw_state"] = "awaiting_bet"
            return

        elif data == "hw_leaderboard":
            leaderboard = await self.hw.hw_leaderboard()
            if not leaderboard:
                await query.edit_message_text("📭 No users.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="hw_dashboard")]]))
                return
            lines = ["🏆 *Leaderboard*"]
            for i, row in enumerate(leaderboard, 1):
                lines.append(f"{i}. {row['mobile']} - ₹{row['balance']:.2f}")
            await query.edit_message_text("\n".join(lines), parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="hw_dashboard")]]))
            return

        elif data == "hw_settings":
            await query.edit_message_text("⚙️ *HW Settings* - coming soon.", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="hw_dashboard")]]))
            return

        elif data == "hw_back":
            await self.show_hw(update, context)
            return

        else:
            await query.edit_message_text("❌ Unknown HW action.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="hw_dashboard")]]))

    async def hw_handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_permission(update):
            return
        text = update.message.text.strip()
        state = context.user_data.get("hw_state")
        if state == "awaiting_mobile":
            mobile = text
            platform = context.user_data.get("hw_platform")
            try:
                resp = await self.hw.send_sms(platform, mobile)
                if platform == 'holwin' and resp.get("code") == 0:
                    await update.message.reply_text(f"✅ OTP sent to {mobile}. Please enter OTP:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
                    context.user_data["hw_mobile"] = mobile
                    context.user_data["hw_state"] = "awaiting_otp"
                elif platform == 'rex' and resp.get("code") == 200:
                    await update.message.reply_text(f"✅ OTP sent to {mobile}. Please enter OTP:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
                    context.user_data["hw_mobile"] = mobile
                    context.user_data["hw_state"] = "awaiting_otp"
                else:
                    await update.message.reply_text(f"❌ Failed to send OTP: {resp}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="hw_dashboard")]]))
                    context.user_data.pop("hw_state", None)
            except Exception as e:
                await update.message.reply_text(f"❌ Error: {e}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="hw_dashboard")]]))
                context.user_data.pop("hw_state", None)
            return

        elif state == "awaiting_otp":
            otp = text
            mobile = context.user_data.get("hw_mobile")
            platform = context.user_data.get("hw_platform")
            password = generate_random_password(8)
            invite = self.hw.invite_codes.get(platform, "")
            success, resp = await self.hw.register(platform, mobile, otp, password, invite)
            if success:
                await self.hw.hw_update_user(update.effective_user.id, platform, mobile, password, invite)
                await update.message.reply_text(f"✅ Registration successful!\nPlatform: {platform}\nMobile: {mobile}\nPassword: `{password}`\nInvite: {invite}", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="hw_dashboard")]]))
            else:
                await update.message.reply_text(f"❌ Registration failed: {resp}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="hw_dashboard")]]))
            context.user_data.pop("hw_state", None)
            context.user_data.pop("hw_mobile", None)
            context.user_data.pop("hw_platform", None)
            return

        elif state == "awaiting_bet":
            try:
                amount = float(text)
                if amount <= 0:
                    raise ValueError
                game = context.user_data.get("hw_game")
                new_balance, result = await self.hw.hw_play_game(update.effective_user.id, game, amount)
                if new_balance is None:
                    await update.message.reply_text(f"❌ {result}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="hw_games")]]))
                else:
                    await update.message.reply_text(f"✅ {result}\nNew balance: ₹{new_balance:.2f}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="hw_games")]]))
            except:
                await update.message.reply_text("❌ Invalid amount.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="hw_games")]]))
            context.user_data.pop("hw_state", None)
            context.user_data.pop("hw_game", None)
            return

        else:
            await update.message.reply_text("❌ Unknown state. Use the buttons.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="hw_dashboard")]]))

    # ---------- WB Callbacks ----------
    async def wb_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_permission(update):
            return
        query = update.callback_query
        data = query.data
        user_id = update.effective_user.id

        if data == "wb_add":
            await query.edit_message_text("📞 Enter phone number (with country code, e.g., +919876543210):", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["wb_state"] = "add_number"
            return

        elif data == "wb_list":
            numbers = await self.wb_auto.wb_get_numbers(user_id)
            if not numbers:
                await query.edit_message_text("📭 No numbers added.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_dashboard")]]))
                return
            lines = ["📋 *Your Numbers*"]
            for n in numbers:
                lines.append(f"📞 {n['phone']} | Appeals: {n['appeal_count']} | {'🚫 Blacklisted' if n['blacklisted'] else '✅ Active'}")
            await query.edit_message_text("\n".join(lines), parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_dashboard")]]))
            return

        elif data == "wb_appeal_all":
            numbers = await self.wb_auto.wb_get_numbers(user_id)
            if not numbers:
                await query.edit_message_text("📭 No numbers.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_dashboard")]]))
                return
            user = await self.wb_auto.wb_get_user(user_id)
            if not user or not user["approved"] or not user["email"]:
                await query.edit_message_text("❌ You are not approved or email not set.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_dashboard")]]))
                return
            await query.edit_message_text("🔄 Sending appeals...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⏹️ Stop", callback_data="wb_stop_auto")]]))
            for n in numbers:
                phone = n["phone"]
                ok, msg = await self.wb_auto.wb_send_email(user_id, phone, user["name"] or "User", user["reason"] or "personal communication", n["custom_reason"])
                await self.wb_auto.wb_update_last_appeal(phone)
                await self.app.bot.send_message(user_id, f"{'✅' if ok else '❌'} {phone}: {msg}")
                await asyncio.sleep(user["delay"] if user else WB_DEFAULT_DELAY)
            await query.edit_message_text("✅ Done.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_dashboard")]]))
            return

        elif data == "wb_appeal_one":
            await query.edit_message_text("📞 Enter phone number to appeal:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["wb_state"] = "appeal_one"
            return

        elif data == "wb_mass":
            await query.edit_message_text("📤 Upload CSV with 'phone' column.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["wb_state"] = "mass_upload"
            return

        elif data == "wb_auto":
            result = await self.wb_auto.start(user_id)
            await query.edit_message_text(f"🔁 {result}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_dashboard")]]))
            return

        elif data == "wb_stop_auto":
            result = await self.wb_auto.stop(user_id)
            await query.edit_message_text(f"🛑 {result}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_dashboard")]]))
            return

        elif data == "wb_webform":
            await query.edit_message_text("🌐 Enter phone number for web form appeal:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["wb_state"] = "webform"
            return

        elif data == "wb_templates":
            templates = await self.wb_auto.wb_get_templates(user_id, include_default=True)
            if not templates:
                await query.edit_message_text("📭 No templates.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_dashboard")]]))
                return
            lines = ["📝 *Templates*"]
            for t in templates:
                lines.append(f"{t['id']}: {t['template'][:50]}...")
            await query.edit_message_text("\n".join(lines), parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➕ Add Template", callback_data="wb_add_template"), InlineKeyboardButton("⬅ Back", callback_data="wb_dashboard")]]))
            return

        elif data == "wb_add_template":
            await query.edit_message_text("📝 Send new template (use {number}, {name}, {reason}):", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["wb_state"] = "add_template"
            return

        elif data == "wb_scheduler":
            await query.edit_message_text("⏰ *Scheduler*\nSend cron expression (e.g., '0 9 * * *') or interval in minutes (e.g., '60').", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["wb_state"] = "scheduler"
            return

        elif data == "wb_stats":
            user = await self.wb_auto.wb_get_user(user_id)
            if not user:
                await query.edit_message_text("❌ No stats.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_dashboard")]]))
                return
            text = boxed(
                f"📊 *Your Stats*\n"
                f"Total Appeals: {user['total_appeals']}\n"
                f"✅ Success: {user['success_appeals']}\n"
                f"❌ Failed: {user['failed_appeals']}\n"
                f"📱 Numbers: {len(await self.wb_auto.wb_get_numbers(user_id))}",
                "WB Stats"
            )
            await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_dashboard")]]))
            return

        elif data == "wb_settings":
            user = await self.wb_auto.wb_get_user(user_id)
            if not user:
                await query.edit_message_text("❌ User not found.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_dashboard")]]))
                return
            text = boxed(
                f"📧 Email: {user['email'] or 'Not set'}\n"
                f"🔑 Password: {'***' if user['password'] else 'Not set'}\n"
                f"⏱️ Delay: {user['delay']}s\n"
                f"📝 Reason: {user['reason']}\n"
                f"✅ Approved: {'Yes' if user['approved'] else 'No'}",
                "WB Settings"
            )
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📧 Set Email", callback_data="wb_set_email")],
                [InlineKeyboardButton("🔑 Set Password", callback_data="wb_set_pass")],
                [InlineKeyboardButton("⏱️ Set Delay", callback_data="wb_set_delay")],
                [InlineKeyboardButton("📝 Set Reason", callback_data="wb_set_reason")],
                [InlineKeyboardButton("⬅ Back", callback_data="wb_dashboard")]
            ])
            await query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)
            return

        elif data == "wb_back":
            await self.show_wb(update, context)
            return

        elif data == "wb_set_email":
            await query.edit_message_text("📧 Send your email (Gmail):", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["wb_state"] = "set_email"
            return

        elif data == "wb_set_pass":
            await query.edit_message_text("🔑 Send your email password:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["wb_state"] = "set_pass"
            return

        elif data == "wb_set_delay":
            await query.edit_message_text("⏱️ Send delay in seconds (e.g., 2):", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["wb_state"] = "set_delay"
            return

        elif data == "wb_set_reason":
            await query.edit_message_text("📝 Send reason for appeal (e.g., 'personal communication'):", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data["wb_state"] = "set_reason"
            return

        else:
            await query.edit_message_text("❌ Unknown WB action.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_dashboard")]]))

    async def wb_handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_permission(update):
            return
        text = update.message.text.strip()
        state = context.user_data.get("wb_state")
        user_id = update.effective_user.id

        if state == "add_number":
            phone = text
            async with aiosqlite.connect(WB_DB_PATH) as db:
                db.row_factory = aiosqlite.Row
                await db.execute("INSERT OR IGNORE INTO wb_numbers (phone, tid) VALUES (?, ?)", (phone, user_id))
                await db.commit()
            await update.message.reply_text(f"✅ Added {phone}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_dashboard")]]))
            context.user_data.pop("wb_state", None)
            return

        elif state == "appeal_one":
            phone = text
            user = await self.wb_auto.wb_get_user(user_id)
            if not user or not user["approved"] or not user["email"]:
                await update.message.reply_text("❌ You are not approved or email not set.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_dashboard")]]))
                context.user_data.pop("wb_state", None)
                return
            ok, msg = await self.wb_auto.wb_send_email(user_id, phone, user["name"] or "User", user["reason"] or "personal communication")
            await self.wb_auto.wb_update_last_appeal(phone)
            await update.message.reply_text(f"{'✅' if ok else '❌'} {phone}: {msg}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_dashboard")]]))
            context.user_data.pop("wb_state", None)
            return

        elif state == "mass_upload":
            await update.message.reply_text("Please upload a CSV file.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]))
            context.user_data.pop("wb_state", None)
            return

        elif state == "webform":
            phone = text
            ok, msg = await self.wb_auto.wb_submit_webform(user_id, phone)
            await update.message.reply_text(f"{'✅' if ok else '❌'} {phone}: {msg}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_dashboard")]]))
            context.user_data.pop("wb_state", None)
            return

        elif state == "add_template":
            if "{number}" in text and "{name}" in text and "{reason}" in text:
                async with aiosqlite.connect(WB_DB_PATH) as db:
                    db.row_factory = aiosqlite.Row
                    await db.execute("INSERT INTO wb_templates (tid, template) VALUES (?, ?)", (user_id, text))
                    await db.commit()
                await update.message.reply_text("✅ Template added.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_templates")]]))
            else:
                await update.message.reply_text("❌ Template must include {number}, {name}, {reason}.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_templates")]]))
            context.user_data.pop("wb_state", None)
            return

        elif state == "scheduler":
            try:
                if croniter.is_valid(text):
                    cron_expr = text
                    interval = None
                else:
                    interval = int(text)
                    cron_expr = None
                async with aiosqlite.connect(WB_DB_PATH) as db:
                    db.row_factory = aiosqlite.Row
                    await db.execute(
                        "INSERT INTO wb_scheduler (tid, cron_expr, interval_minutes, next_run, active) VALUES (?, ?, ?, ?, 1)",
                        (user_id, cron_expr, interval, datetime.utcnow().isoformat())
                    )
                    await db.commit()
                await update.message.reply_text("✅ Scheduler added.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_dashboard")]]))
            except:
                await update.message.reply_text("❌ Invalid cron or interval.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_dashboard")]]))
            context.user_data.pop("wb_state", None)
            return

        elif state == "set_email":
            if "@" in text:
                await self.wb_auto.wb_update_user(user_id, "email", text)
                await update.message.reply_text("✅ Email set.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_settings")]]))
            else:
                await update.message.reply_text("❌ Invalid email.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_settings")]]))
            context.user_data.pop("wb_state", None)
            return

        elif state == "set_pass":
            await self.wb_auto.wb_update_user(user_id, "password", text)
            await update.message.reply_text("✅ Password set.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_settings")]]))
            context.user_data.pop("wb_state", None)
            return

        elif state == "set_delay":
            try:
                delay = float(text)
                if delay < 0:
                    raise ValueError
                await self.wb_auto.wb_update_user(user_id, "delay", delay)
                await update.message.reply_text(f"✅ Delay set to {delay}s.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_settings")]]))
            except:
                await update.message.reply_text("❌ Invalid number.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_settings")]]))
            context.user_data.pop("wb_state", None)
            return

        elif state == "set_reason":
            await self.wb_auto.wb_update_user(user_id, "reason", text)
            await update.message.reply_text(f"✅ Reason set to '{text}'.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_settings")]]))
            context.user_data.pop("wb_state", None)
            return

        else:
            await update.message.reply_text("❌ Unknown state. Use the buttons.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wb_dashboard")]]))

    # ---------- Admin Commands ----------
    async def admin_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Home", callback_data="home")]]))
            return
        await self.admin_dashboard(update, context)

    async def admin_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        em_total, em_success, em_fail = await self.em.em_stats()
        async with aiosqlite.connect(HW_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT COUNT(*) FROM hw_users")
            hw_total = (await cur.fetchone())[0]
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT COUNT(*) FROM wb_users")
            wb_total = (await cur.fetchone())[0]
            cur = await db.execute("SELECT COUNT(*) FROM wb_users WHERE approved=1")
            wb_approved = (await cur.fetchone())[0]
            cur = await db.execute("SELECT COUNT(*) FROM wb_pending")
            pending = (await cur.fetchone())[0]
        uptime = datetime.now() - self.start_time
        text = boxed(
            f"📊 *Global Stats*\n"
            f"👥 Total Users: {wb_total}\n"
            f"✅ Approved: {wb_approved}\n"
            f"⏳ Pending: {pending}\n"
            f"📈 EarnMigo: {em_total} (✅ {em_success} | ❌ {em_fail})\n"
            f"📈 Holwin/Rex: {hw_total}\n"
            f"🕒 Uptime: {str(uptime).split('.')[0]}\n"
            f"🟢 System: {'🟢 Online' if not global_state.maintenance_mode else '🔴 Maintenance'}",
            "👑 ADMIN"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📊 Stats", callback_data="stats"), InlineKeyboardButton("👥 Users", callback_data="list_users")],
            [InlineKeyboardButton("📢 Broadcast", callback_data="broadcast")],
            [InlineKeyboardButton("🚫 Ban", callback_data="admin_ban"), InlineKeyboardButton("✅ Unban", callback_data="admin_unban")],
            [InlineKeyboardButton("📋 Whitelist", callback_data="whitelist")],
            [InlineKeyboardButton("🔧 Maintenance", callback_data="admin_maintenance"), InlineKeyboardButton("🔄 Restart", callback_data="admin_restart")],
            [InlineKeyboardButton("💾 Backup", callback_data="backup")],
            [InlineKeyboardButton("⬅ Back", callback_data="home")]
        ])
        if update.callback_query:
            await update.callback_query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)
        else:
            await update.message.reply_text(text, parse_mode="Markdown", reply_markup=keyboard)

    async def admin_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        data = query.data
        if not data.startswith("admin_"):
            return
        if update.effective_user.id not in ADMIN_IDS:
            await query.edit_message_text("⛔ Admin only.")
            return
        if data == "admin_ban" or data == "admin_unban":
            await query.edit_message_text("Send /ban <user_id> or /unban <user_id>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="admin_dashboard")]]))
            return
        elif data == "admin_maintenance":
            global_state.maintenance_mode = not global_state.maintenance_mode
            await query.edit_message_text(f"🔧 Maintenance mode: {'ON' if global_state.maintenance_mode else 'OFF'}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="admin_dashboard")]]))
            return
        elif data == "admin_restart":
            await query.edit_message_text("🔄 Restarting... (not implemented)", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="admin_dashboard")]]))
            return
        else:
            if data.startswith("admin_approve_"):
                tid = int(data.split("_")[2])
                await self.wb_auto.wb_approve_user(tid)
                await query.edit_message_text(f"✅ User {tid} approved.")
                try:
                    await context.bot.send_message(tid, "🎉 You have been approved to use the bot.")
                except:
                    pass
                return
            await query.edit_message_text("Unknown admin action.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="admin_dashboard")]]))

    # ---------- Other Admin Commands ----------
    async def approve_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.")
            return
        args = context.args
        if not args:
            await update.message.reply_text("Usage: /approve <user_id>")
            return
        try:
            tid = int(args[0])
        except:
            await update.message.reply_text("Invalid user ID.")
            return
        await self.wb_auto.wb_approve_user(tid)
        await update.message.reply_text(f"✅ User {tid} approved.")
        try:
            await context.bot.send_message(tid, "🎉 You have been approved to use the bot.")
        except:
            pass

    async def reject_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.")
            return
        args = context.args
        if not args:
            await update.message.reply_text("Usage: /reject <user_id>")
            return
        try:
            tid = int(args[0])
        except:
            await update.message.reply_text("Invalid user ID.")
            return
        await self.wb_auto.wb_reject_user(tid)
        await update.message.reply_text(f"❌ User {tid} rejected.")

    async def whitelist_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.")
            return
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT user_id FROM wb_whitelist")
            rows = await cur.fetchall()
        if not rows:
            await update.message.reply_text("Whitelist empty.")
            return
        text = "📋 Whitelisted users:\n" + "\n".join([str(r["user_id"]) for r in rows])
        await update.message.reply_text(text)

    async def remove_whitelist_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.")
            return
        args = context.args
        if not args:
            await update.message.reply_text("Usage: /remove <user_id>")
            return
        try:
            tid = int(args[0])
        except:
            await update.message.reply_text("Invalid user ID.")
            return
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("DELETE FROM wb_whitelist WHERE user_id = ?", (tid,))
            await db.commit()
        await update.message.reply_text(f"🗑️ User {tid} removed from whitelist.")

    async def stats_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.")
            return
        em_total, em_success, em_fail = await self.em.em_stats()
        async with aiosqlite.connect(HW_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT COUNT(*) FROM hw_users")
            hw_total = (await cur.fetchone())[0]
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT COUNT(*) FROM wb_users")
            wb_total = (await cur.fetchone())[0]
        text = boxed(
            f"📊 *Global Stats*\n\n"
            f"EarnMigo: Total {em_total}, Success {em_success}, Fail {em_fail}\n"
            f"Holwin/Rex: {hw_total} users\n"
            f"WhatsApp Unban: {wb_total} users",
            "Stats"
        )
        await update.message.reply_text(text, parse_mode="Markdown")

    async def backup_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.")
            return
        backup_path = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        with zipfile.ZipFile(backup_path, 'w') as zf:
            for db in [EM_DB_PATH, HW_DB_PATH, WB_DB_PATH]:
                if os.path.exists(db):
                    zf.write(db)
        with open(backup_path, 'rb') as f:
            await update.message.reply_document(document=f, filename=backup_path, caption="✅ Backup created.")
        os.remove(backup_path)

    async def restore_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.")
            return
        if not update.message.reply_to_message or not update.message.reply_to_message.document:
            await update.message.reply_text("Please reply to a backup zip file with /restore")
            return
        file = await update.message.reply_to_message.document.get_file()
        content = await file.download_as_bytearray()
        backup_path = f"restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        with open(backup_path, 'wb') as f:
            f.write(content)
        try:
            with zipfile.ZipFile(backup_path, 'r') as zf:
                zf.extractall(".")
            await update.message.reply_text("✅ Restore successful.")
        except Exception as e:
            await update.message.reply_text(f"❌ Restore failed: {e}")
        os.remove(backup_path)

    async def broadcast_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.")
            return
        msg_text = update.message.text.replace("/broadcast", "").strip()
        if not msg_text:
            await update.message.reply_text("Usage: /broadcast <message>")
            return
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            users = await db.execute("SELECT tid FROM wb_users").fetchall()
        count = 0
        for row in users:
            try:
                await context.bot.send_message(row["tid"], f"📢 *Broadcast*\n\n{msg_text}", parse_mode="Markdown")
                count += 1
                await asyncio.sleep(0.05)
            except:
                pass
        await update.message.reply_text(f"✅ Broadcast sent to {count} users.")

    async def list_users_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.")
            return
        async with aiosqlite.connect(WB_DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT tid, name, approved, banned FROM wb_users")
            rows = await cur.fetchall()
        text = "👥 *Users*\n"
        for r in rows:
            text += f"ID: {r['tid']} | Name: {r['name'] or 'N/A'} | Approved: {'✅' if r['approved'] else '❌'} | Banned: {'🚫' if r['banned'] else '✔️'}\n"
        await update.message.reply_text(text, parse_mode="Markdown")

    async def clear_em_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.")
            return
        await self.em.em_clear_db()
        await update.message.reply_text("🗑️ EarnMigo data cleared.")

    async def clear_hw_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.")
            return
        await self.hw.hw_clear_all()
        await update.message.reply_text("🗑️ Holwin/Rex data cleared.")

    async def clear_wb_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.")
            return
        await self.wb_auto.wb_clear_all()
        await update.message.reply_text("🗑️ WhatsApp Unban data cleared.")

    async def pending_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.")
            return
        pending = await self.wb_auto.wb_get_pending()
        if not pending:
            await update.message.reply_text("No pending requests.")
            return
        keyboard = []
        for p in pending:
            keyboard.append([InlineKeyboardButton(f"{p['username']} (ID: {p['user_id']})", callback_data=f"admin_approve_{p['user_id']}")])
        keyboard.append([InlineKeyboardButton("🔙 Home", callback_data="home")])
        await update.message.reply_text("Select user to approve:", reply_markup=InlineKeyboardMarkup(keyboard))

    async def export_logs_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.")
            return
        args = context.args
        if not args:
            await update.message.reply_text("Usage: /export_logs <user_id>")
            return
        try:
            tid = int(args[0])
        except:
            await update.message.reply_text("Invalid user ID.")
            return
        csv_data = await self.wb_auto.wb_export_logs(tid)
        if csv_data is None:
            await update.message.reply_text("No logs for this user.")
            return
        await update.message.reply_document(document=io.BytesIO(csv_data.encode()), filename=f"logs_{tid}.csv", caption="✅ Logs exported.")

    async def list_schedules_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.")
            return
        args = context.args
        if not args:
            await update.message.reply_text("Usage: /list_schedules <user_id>")
            return
        try:
            tid = int(args[0])
        except:
            await update.message.reply_text("Invalid user ID.")
            return
        jobs = await self.wb_auto.wb_get_scheduler_jobs(tid)
        if not jobs:
            await update.message.reply_text("No active schedules for this user.")
            return
        text = "⏰ *Scheduler Jobs*\n"
        for j in jobs:
            # FIX: avoid nested f-string to prevent syntax error
            cron_or_interval = j['cron_expr'] if j['cron_expr'] else f"every {j['interval_minutes']} min"
            text += f"ID: {j['id']} | {cron_or_interval} | Next: {j['next_run']}\n"
        await update.message.reply_text(text, parse_mode="Markdown")

    async def delete_schedule_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.")
            return
        args = context.args
        if not args:
            await update.message.reply_text("Usage: /delete_schedule <job_id>")
            return
        try:
            job_id = int(args[0])
        except:
            await update.message.reply_text("Invalid job ID.")
            return
        await self.wb_auto.wb_delete_scheduler(job_id)
        await update.message.reply_text("✅ Schedule deleted.")

    async def ban_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.")
            return
        args = context.args
        if not args:
            await update.message.reply_text("Usage: /ban <user_id>")
            return
        try:
            tid = int(args[0])
        except:
            await update.message.reply_text("Invalid user ID.")
            return
        async with aiosqlite.connect(WB_DB_PATH) as db:
            await db.execute("UPDATE wb_users SET banned = 1 WHERE tid = ?", (tid,))
            await db.commit()
        await update.message.reply_text(f"✅ User {tid} banned.")

    async def unban_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.")
            return
        args = context.args
        if not args:
            await update.message.reply_text("Usage: /unban <user_id>")
            return
        try:
            tid = int(args[0])
        except:
            await update.message.reply_text("Invalid user ID.")
            return
        async with aiosqlite.connect(WB_DB_PATH) as db:
            await db.execute("UPDATE wb_users SET banned = 0 WHERE tid = ?", (tid,))
            await db.commit()
        await update.message.reply_text(f"✅ User {tid} unbanned.")

    # ---------- Other Navigation Commands ----------
    async def help_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = boxed(
            "📖 *Help*\n\n"
            "Welcome to Super Bot!\n"
            "Use inline buttons to navigate.\n"
            "You need a gift code to use premium features.\n"
            "Commands:\n"
            "/start – Home\n"
            "/gift <code> – Redeem a gift code\n"
            "/profile – Your profile\n"
            "/settings – Settings\n"
            "/feedback – Send feedback\n"
            "/admin – Admin panel (admin only)",
            "Help"
        )
        await update.message.reply_text(help_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Home", callback_data="home")]]))

    async def menu_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.start_cmd(update, context)

    async def cancel_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data.pop("em_state", None)
        context.user_data.pop("hw_state", None)
        context.user_data.pop("wb_state", None)
        await update.message.reply_text("✅ Operation cancelled.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Home", callback_data="home")]]))

    async def request_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        username = update.effective_user.username or "Unknown"
        await self.wb_auto.wb_request_approval(user_id, username)
        await update.message.reply_text("✅ Request sent to admin. You will be notified when approved.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Home", callback_data="home")]]))
        for admin in ADMIN_IDS:
            try:
                await self.app.bot.send_message(admin, f"📨 *New Access Request*\nUser: @{username} (ID: {user_id})\nUse /pending to view.", parse_mode="Markdown")
            except:
                pass

    async def language_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        args = context.args
        if not args:
            await update.message.reply_text("Usage: /language <en|hi>\nExample: /language hi")
            return
        lang = args[0].lower()
        if lang not in ["en", "hi"]:
            await update.message.reply_text("❌ Supported languages: en, hi")
            return
        await self.wb_auto.wb_set_language(user_id, lang)
        await update.message.reply_text(f"✅ Language set to {lang}.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Home", callback_data="home")]]))

    async def test_email_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        ok, msg = await self.wb_auto.wb_test_email(user_id)
        await update.message.reply_text(f"{'✅' if ok else '❌'} Email test: {msg}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Home", callback_data="home")]]))

    # ---------- Profile & Settings ----------
    async def profile_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        stats = await self._get_user_stats(user.id)
        expiry = await PermissionManager.get_expiry(user.id)
        expiry_str = format_timestamp(expiry) if expiry else "Never"
        text = boxed(
            f"👤 @{user.username or 'User'}\n"
            f"🆔 ID: `{user.id}`\n"
            f"📱 Numbers: {stats['total_nums']}\n"
            f"📨 Appeals: {stats['total_appeals']}\n"
            f"✅ Success: {stats['success_appeals']}\n"
            f"❌ Failed: {stats['failed_appeals']}\n"
            f"💎 Permission: {'✅' if await PermissionManager.has_permission(user.id) else '❌'}\n"
            f"⏳ Expires: {expiry_str}",
            "PROFILE"
        )
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="home")]]))

    async def settings_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        wb_user = await self.wb_auto.wb_get_user(user_id)
        lang = wb_user["language"] if wb_user else "en"
        delay = wb_user["delay"] if wb_user else WB_DEFAULT_DELAY
        text = boxed(
            f"🌐 Language: {lang}\n"
            f"⏱️ Delay: {delay}s\n"
            f"📧 Email: {wb_user['email'] if wb_user else 'Not set'}\n"
            f"⚡ Concurrency: {self.em.concurrent}",
            "⚙ SETTINGS"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌐 Change Language", callback_data="settings_lang")],
            [InlineKeyboardButton("⏱️ Set Delay", callback_data="settings_delay")],
            [InlineKeyboardButton("📧 Set Email", callback_data="wb_set_email")],
            [InlineKeyboardButton("🔑 Set Password", callback_data="wb_set_pass")],
            [InlineKeyboardButton("⬅ Back", callback_data="home")]
        ])
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=keyboard)

    # ---------- Feedback ----------
    async def feedback_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        feedback = " ".join(context.args) if context.args else None
        if not feedback:
            await update.message.reply_text("📝 Send feedback: /feedback <message>")
            return
        for admin in ADMIN_IDS:
            try:
                await self.app.bot.send_message(admin, f"📩 *Feedback from @{update.effective_user.username}*\n\n{feedback}", parse_mode="Markdown")
            except:
                pass
        await update.message.reply_text("✅ Thanks for your feedback!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Home", callback_data="home")]]))

    # ---------- AI Commands ----------
    async def ai_chat_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_permission(update):
            return
        text = " ".join(context.args) if context.args else None
        if not text:
            await update.message.reply_text("Usage: /ai <your question>")
            return
        result = await AITools.chat(text)
        await update.message.reply_text(result, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="home")]]))

    async def summarize_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_permission(update):
            return
        text = " ".join(context.args) if context.args else None
        if not text:
            await update.message.reply_text("Usage: /summarize <text>")
            return
        result = await AITools.summarize(text)
        await update.message.reply_text(result, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="home")]]))

    # ---------- Auto Backup ----------
    async def auto_backup_job(self):
        try:
            backup_path = f"auto_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            with zipfile.ZipFile(backup_path, 'w') as zf:
                for db in [EM_DB_PATH, HW_DB_PATH, WB_DB_PATH]:
                    if os.path.exists(db):
                        zf.write(db)
            logger.info(f"Auto backup: {backup_path}")
            backups = sorted([f for f in os.listdir('.') if f.startswith('auto_backup_') and f.endswith('.zip')])
            for old in backups[:-5]:
                os.remove(old)
        except Exception as e:
            logger.error(f"Auto backup failed: {e}")

    # ---------- Global Error Handler ----------
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.error(msg="Exception while handling an update:", exc_info=context.error)
        try:
            for admin in ADMIN_IDS:
                await context.bot.send_message(admin, f"⚠️ *Error*\n{str(context.error)[:200]}")
        except:
            pass

# ---------- Global bot_app ----------
bot_app = None

# ---------- Main ----------
if __name__ == "__main__":
    import asyncio
    bot = MegaBot()
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    except Exception as e:
        logger.error(f"Fatal error: {e}\n{traceback.format_exc()}")

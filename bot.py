#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║              ██████╗ ███████╗██╗   ██╗██╗██╗     ██╗   ██╗██╗███████╗    ║
║              ██╔══██╗██╔════╝╚██╗ ██╔╝██║██║     ██║   ██║██║██╔════╝    ║
║              ██║  ██║█████╗   ╚████╔╝ ██║██║     ██║   ██║██║███████╗    ║
║              ██║  ██║██╔══╝    ╚██╔╝  ██║██║     ██║   ██║██║╚════██║    ║
║              ██████╔╝███████╗   ██║   ██║███████╗╚██████╔╝██║███████║    ║
║              ╚═════╝ ╚══════╝   ╚═╝   ╚═╝╚══════╝ ╚═════╝ ╚═╝╚══════╝    ║
║                                                                           ║
║               MEGA APP DASHBOARD BOT – ULTIMATE PREMIUM EDITION           ║
║                   Unified Multi‑Engine Automation System                   ║
║                                                                           ║
║         Developer: DK Sharma 🚀                                           ║
║         Admin: @OfficalEarningZone                                        ║
║         Version: 10.1 – "The Titan"                                      ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import aiohttp
from aiohttp import ClientTimeout, TCPConnector
import aiosqlite
import logging
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
import threading
import shutil
import hashlib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from collections import deque
from typing import Optional, List, Dict, Any, Tuple, Union
from functools import wraps
from queue import Queue

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
from croniter import croniter

# ---------- Optional high-performance modules ----------
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

# ---------- Optional Selenium for Web Form ----------
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# ---------- Optional 2captcha ----------
try:
    from twocaptcha import TwoCaptcha
    TWOCAPTCHA_AVAILABLE = True
except ImportError:
    TWOCAPTCHA_AVAILABLE = False

# ---------- Logging ----------
logging.basicConfig(
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("MegaBot")

# ---------- Environment Variables ----------
BOT_TOKEN = os.getenv("BOT_TOKEN", "8693119356:AAHCuPtu29sYh1P2hK-DkRb0UBt5rmnrfvQ")
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "5888777479").split(",") if x.strip().isdigit()]
DEVELOPER_NAME = "DK Sharma"
ADMIN_USERNAME = "@OfficalEarningZone"

# ----- Engine-specific defaults -----
DEFAULT_REFERRAL = os.getenv("DEFAULT_REFERRAL", "1816")
DEFAULT_PASSWORD = os.getenv("DEFAULT_PASSWORD", "Test@123")
VERIFY_CODE = os.getenv("VERIFY_CODE", "7777")
TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Calcutta")
EM_API_URL = os.getenv("EM_API_URL", "https://api.earnmigo.com/api/app/user/login/email")
EM_VERIFY_URL = os.getenv("EM_VERIFY_URL", "https://api.earnmigo.com/api/app/user/info")
EM_DB_PATH = os.getenv("EM_DB_PATH", "em_registrations.db")
EM_CONCURRENCY = int(os.getenv("EM_CONCURRENCY", "250"))
EM_DELAY = float(os.getenv("EM_DELAY", "0.002"))
EM_TURBO_CONCURRENCY = int(os.getenv("EM_TURBO_CONCURRENCY", "600"))
EM_TURBO_DELAY = float(os.getenv("EM_TURBO_DELAY", "0.0"))

HOLWIN_INVITE = os.getenv("HOLWIN_INVITE", "WLRPSY")
REX_INVITE = os.getenv("REX_INVITE", "O6NVYX")
HOLWIN_BASE = os.getenv("HOLWIN_BASE", "https://www.holwin123.top")
HOLWIN_DI = os.getenv("HOLWIN_DI", "88dd52c70e7b377527be01c39f5a0a4f")
HOLWIN_VTOKEN = os.getenv("HOLWIN_VTOKEN", "18667bd921478af5fe5f6506865e4f8a")
REX_BASE = os.getenv("REX_BASE", "https://rcapi.rexproearn.com")
REX_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://rch5.rexproearn.com",
    "Referer": "https://rch5.rexproearn.com/",
}
HW_DB_PATH = os.getenv("HW_DB_PATH", "holwin_rex.db")

WB_DB_PATH = os.getenv("WB_DB_PATH", "whatsapp_unban.db")
WB_DEFAULT_DELAY = float(os.getenv("WB_DEFAULT_DELAY", "1.0"))
WB_MAX_RETRIES = int(os.getenv("WB_MAX_RETRIES", "3"))
WB_MAX_CONCURRENT_SENDS = int(os.getenv("WB_MAX_CONCURRENT_SENDS", "5"))
RATE_LIMIT_CALLS = int(os.getenv("RATE_LIMIT_CALLS", "20"))
RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD", "60"))

SELENIUM_ENABLED = os.getenv("SELENIUM_ENABLED", "false").lower() == "true"
TWOCAPTCHA_ENABLED = os.getenv("TWOCAPTCHA_ENABLED", "false").lower() == "true"

# ---------- Utility Functions ----------
def boxed(text: str, title: str = "") -> str:
    """Wrap text in a nice box with borders."""
    lines = text.splitlines()
    max_len = max(len(line) for line in lines) if lines else 0
    if title:
        title_line = f"┌─ {title} " + "─" * (max_len - len(title) - 2) + "┐"
        return title_line + "\n" + "\n".join(f"│ {line:<{max_len}} │" for line in lines) + "\n" + "└" + "─" * (max_len + 4) + "┘"
    else:
        return "┌" + "─" * (max_len + 4) + "┐" + "\n" + "\n".join(f"│ {line:<{max_len}} │" for line in lines) + "\n" + "└" + "─" * (max_len + 4) + "┘"

def format_em_dashboard(crud, em_engine) -> str:
    """Return the EarnMigo dashboard text."""
    total, success, fail = asyncio.run(crud.em_stats())  # We'll call from async context, so this is a sync helper
    if em_engine.running and em_engine.total > 0:
        elapsed = time.time() - em_engine.start_time if em_engine.start_time else 0
        rate = em_engine.processed / elapsed if elapsed > 0 else 0
        remaining = (em_engine.total - em_engine.processed) / rate if rate > 0 else 0
        progress = em_engine.processed / em_engine.total * 100
        bar = "█" * int(progress/5) + "░" * (20 - int(progress/5))
        return boxed(
            f"Progress: [{bar}] {progress:.1f}%\n"
            f"✅ Success: {em_engine.success}   ❌ Fail: {em_engine.fail}\n"
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

# ---------- Database ----------
class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def execute(self, query: str, params: tuple = ()):
        async with aiosqlite.connect(self.db_path) as db:
            cur = await db.execute(query, params)
            await db.commit()
            return cur

    async def fetch_one(self, query: str, params: tuple = ()):
        async with aiosqlite.connect(self.db_path) as db:
            cur = await db.execute(query, params)
            return await cur.fetchone()

    async def fetch_all(self, query: str, params: tuple = ()):
        async with aiosqlite.connect(self.db_path) as db:
            cur = await db.execute(query, params)
            return await cur.fetchall()

    async def init_tables(self):
        # EM registrations
        await self.execute("""
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
        """)
        # HW users
        await self.execute("""
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
        """)
        await self.execute("""
            CREATE TABLE IF NOT EXISTS hw_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                type TEXT,
                amount REAL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # WB tables
        await self.execute("""
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
                failed_appeals INTEGER DEFAULT 0,
                smtp_host TEXT DEFAULT 'smtp.gmail.com',
                smtp_port INTEGER DEFAULT 587,
                support_email TEXT DEFAULT 'support@whatsapp.com'
            )
        """)
        await self.execute("""
            CREATE TABLE IF NOT EXISTS wb_numbers (
                phone TEXT PRIMARY KEY,
                tid INTEGER,
                last_appeal TIMESTAMP,
                appeal_count INTEGER DEFAULT 0,
                blacklisted INTEGER DEFAULT 0,
                custom_reason TEXT,
                FOREIGN KEY(tid) REFERENCES wb_users(tid)
            )
        """)
        await self.execute("""
            CREATE TABLE IF NOT EXISTS wb_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tid INTEGER,
                template TEXT,
                is_default INTEGER DEFAULT 0
            )
        """)
        await self.execute("""
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
        """)
        await self.execute("""
            CREATE TABLE IF NOT EXISTS wb_scheduler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tid INTEGER,
                cron_expr TEXT,
                interval_minutes INTEGER,
                next_run TIMESTAMP,
                active INTEGER DEFAULT 1,
                last_run TIMESTAMP
            )
        """)
        await self.execute("""
            CREATE TABLE IF NOT EXISTS wb_proxies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proxy TEXT UNIQUE,
                last_used TIMESTAMP,
                success_count INTEGER DEFAULT 0,
                fail_count INTEGER DEFAULT 0
            )
        """)
        await self.execute("""
            CREATE TABLE IF NOT EXISTS wb_whitelist (
                user_id INTEGER PRIMARY KEY,
                approved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await self.execute("""
            CREATE TABLE IF NOT EXISTS wb_pending (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Default templates for WB
        cur = await self.fetch_one("SELECT COUNT(*) FROM wb_templates WHERE is_default=1")
        if cur and cur[0] == 0:
            defaults = [
                "Dear WhatsApp Team, my number {number} has been banned. I use it for {reason}. Please unban. Regards, {name}",
                "Hello, I appeal for {number}. It is used for {reason}. Kindly restore. {name}",
                "Respectful request: unban {number}. I am a genuine {reason} user. Thanks, {name}",
                "Urgent: {number} is banned. I follow all rules. Please review. {name}",
                "My account {number} was disabled. I need it for {reason}. Help me. {name}",
            ]
            for t in defaults:
                await self.execute("INSERT INTO wb_templates (tid, template, is_default) VALUES (0, ?, 1)", (t,))
        logger.info("All database tables initialized.")

# ---------- CRUD ----------
class CRUD:
    def __init__(self, db: Database):
        self.db = db

    # ---- EM ----
    async def em_add_success(self, email: str, password: str, referral: str, auth_key: str, user_id: str):
        await self.db.execute(
            "INSERT OR IGNORE INTO em_registrations (email, password, referral, authorized_key, user_id, status) VALUES (?,?,?,?,?,?)",
            (email, password, referral, auth_key, user_id, "success")
        )

    async def em_add_fail(self, email: str, password: str, referral: str, error: str):
        await self.db.execute(
            "INSERT OR IGNORE INTO em_registrations (email, password, referral, status) VALUES (?,?,?,?)",
            (email, password, referral, "fail")
        )

    async def em_stats(self):
        total = (await self.db.fetch_one("SELECT COUNT(*) FROM em_registrations"))[0]
        success = (await self.db.fetch_one("SELECT COUNT(*) FROM em_registrations WHERE status='success'"))[0]
        fail = (await self.db.fetch_one("SELECT COUNT(*) FROM em_registrations WHERE status='fail'"))[0]
        return total, success, fail

    async def em_get_all_success(self):
        return await self.db.fetch_all("SELECT email, authorized_key, created_at FROM em_registrations WHERE status='success'")

    async def em_get_recent(self, limit=10):
        return await self.db.fetch_all(
            "SELECT email, authorized_key, created_at FROM em_registrations WHERE status='success' ORDER BY id DESC LIMIT ?",
            (limit,)
        )

    async def em_clear(self):
        await self.db.execute("DELETE FROM em_registrations")

    # ---- HW ----
    async def hw_get_user(self, telegram_id: int):
        return await self.db.fetch_one("SELECT * FROM hw_users WHERE telegram_id = ?", (telegram_id,))

    async def hw_create_user(self, telegram_id: int):
        await self.db.execute("INSERT OR IGNORE INTO hw_users (telegram_id) VALUES (?)", (telegram_id,))

    async def hw_update_user(self, telegram_id: int, platform: str, mobile: str, password: str, invite: str):
        await self.db.execute(
            "UPDATE hw_users SET platform=?, mobile=?, password=?, invite_code=?, registered=1 WHERE telegram_id=?",
            (platform, mobile, password, invite, telegram_id)
        )

    async def hw_update_balance(self, telegram_id: int, amount: float):
        await self.db.execute("UPDATE hw_users SET balance = balance + ? WHERE telegram_id = ?", (amount, telegram_id))

    async def hw_add_transaction(self, user_id: int, type: str, amount: float, description: str):
        await self.db.execute(
            "INSERT INTO hw_transactions (user_id, type, amount, description) VALUES (?,?,?,?)",
            (user_id, type, amount, description)
        )

    async def hw_leaderboard(self):
        return await self.db.fetch_all("SELECT mobile, balance FROM hw_users WHERE registered=1 ORDER BY balance DESC LIMIT 10")

    # ---- WB ----
    async def wb_get_user(self, tid: int):
        return await self.db.fetch_one("SELECT * FROM wb_users WHERE tid = ?", (tid,))

    async def wb_create_user(self, tid: int, name: str = None):
        await self.db.execute(
            "INSERT OR IGNORE INTO wb_users (tid, name, requested_at, last_active) VALUES (?, ?, ?, ?)",
            (tid, name, datetime.utcnow().isoformat(), datetime.utcnow().isoformat())
        )

    async def wb_update_user(self, tid: int, **kwargs):
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key}=?")
            values.append(value)
        values.append(tid)
        await self.db.execute(f"UPDATE wb_users SET {', '.join(fields)} WHERE tid=?", tuple(values))

    async def wb_add_number(self, tid: int, phone: str, custom_reason: str = None):
        try:
            await self.db.execute(
                "INSERT INTO wb_numbers (phone, tid, custom_reason) VALUES (?, ?, ?)",
                (phone, tid, custom_reason)
            )
            return True, "Number added"
        except:
            return False, "Number already exists"

    async def wb_get_numbers(self, tid: int):
        return await self.db.fetch_all("SELECT * FROM wb_numbers WHERE tid = ?", (tid,))

    async def wb_get_number(self, phone: str):
        return await self.db.fetch_one("SELECT * FROM wb_numbers WHERE phone = ?", (phone,))

    async def wb_update_last_appeal(self, phone: str):
        await self.db.execute(
            "UPDATE wb_numbers SET last_appeal = ?, appeal_count = appeal_count + 1 WHERE phone = ?",
            (datetime.utcnow().isoformat(), phone)
        )

    async def wb_toggle_blacklist(self, phone: str):
        await self.db.execute("UPDATE wb_numbers SET blacklisted = 1 - blacklisted WHERE phone = ?", (phone,))

    async def wb_remove_number(self, tid: int, phone: str) -> bool:
        cur = await self.db.execute("DELETE FROM wb_numbers WHERE phone = ? AND tid = ?", (phone, tid))
        return cur.rowcount > 0

    async def wb_get_templates(self, tid: int, include_default=True):
        if include_default:
            return await self.db.fetch_all(
                "SELECT id, template FROM wb_templates WHERE tid = ? OR is_default = 1", (tid,)
            )
        else:
            return await self.db.fetch_all("SELECT id, template FROM wb_templates WHERE tid = ?", (tid,))

    async def wb_add_template(self, tid: int, template: str):
        await self.db.execute("INSERT INTO wb_templates (tid, template, is_default) VALUES (?, ?, 0)", (tid, template))

    async def wb_delete_template(self, tid: int, template_id: int):
        cur = await self.db.execute(
            "DELETE FROM wb_templates WHERE id = ? AND tid = ? AND is_default = 0",
            (template_id, tid)
        )
        return cur.rowcount > 0

    async def wb_log_appeal(self, tid: int, phone: str, success: bool, error: str = "", template: str = "", method: str = "email"):
        await self.db.execute(
            "INSERT INTO wb_logs (tid, phone, success, error, sent_at, template_used, method) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (tid, phone, 1 if success else 0, error, datetime.utcnow().isoformat(), template, method)
        )
        await self.db.execute("UPDATE wb_users SET total_appeals = total_appeals + 1 WHERE tid = ?", (tid,))
        if success:
            await self.db.execute("UPDATE wb_users SET success_appeals = success_appeals + 1 WHERE tid = ?", (tid,))
        else:
            await self.db.execute("UPDATE wb_users SET failed_appeals = failed_appeals + 1 WHERE tid = ?", (tid,))

    async def wb_get_stats(self, tid: int):
        user = await self.wb_get_user(tid)
        if not user:
            return None
        numbers = await self.wb_get_numbers(tid)
        total_logs = (await self.db.fetch_one("SELECT COUNT(*) FROM wb_logs WHERE tid = ?", (tid,)))[0]
        success_logs = (await self.db.fetch_one("SELECT COUNT(*) FROM wb_logs WHERE tid = ? AND success=1", (tid,)))[0]
        return {
            "user": user,
            "total_numbers": len(numbers),
            "appealed": sum(1 for n in numbers if n[3] > 0),
            "total_logs": total_logs,
            "success_logs": success_logs,
            "failed_logs": total_logs - success_logs,
        }

    async def wb_get_scheduler_jobs(self, tid: int):
        return await self.db.fetch_all("SELECT * FROM wb_scheduler WHERE tid = ? AND active = 1", (tid,))

    async def wb_create_scheduler_job(self, tid: int, cron_expr: str = None, interval_minutes: int = None, next_run: datetime = None):
        if next_run is None:
            if cron_expr:
                next_run = croniter(cron_expr, datetime.utcnow()).get_next(datetime)
            elif interval_minutes:
                next_run = datetime.utcnow() + timedelta(minutes=interval_minutes)
            else:
                return None
        cur = await self.db.execute(
            "INSERT INTO wb_scheduler (tid, cron_expr, interval_minutes, next_run, active) VALUES (?, ?, ?, ?, 1)",
            (tid, cron_expr, interval_minutes, next_run.isoformat())
        )
        return cur.lastrowid

    async def wb_delete_scheduler_job(self, job_id: int):
        await self.db.execute("DELETE FROM wb_scheduler WHERE id = ?", (job_id,))

    async def wb_update_scheduler_job(self, job_id: int, next_run: datetime):
        await self.db.execute(
            "UPDATE wb_scheduler SET next_run = ?, last_run = ? WHERE id = ?",
            (next_run.isoformat(), datetime.utcnow().isoformat(), job_id)
        )

    async def is_whitelisted(self, user_id: int) -> bool:
        row = await self.db.fetch_one("SELECT 1 FROM wb_whitelist WHERE user_id = ?", (user_id,))
        return row is not None

    async def add_whitelist(self, user_id: int):
        await self.db.execute("INSERT OR IGNORE INTO wb_whitelist (user_id) VALUES (?)", (user_id,))

    async def remove_whitelist(self, user_id: int):
        await self.db.execute("DELETE FROM wb_whitelist WHERE user_id = ?", (user_id,))

    async def add_pending(self, user_id: int, username: str):
        await self.db.execute("INSERT OR REPLACE INTO wb_pending (user_id, username) VALUES (?, ?)", (user_id, username))

    async def remove_pending(self, user_id: int):
        await self.db.execute("DELETE FROM wb_pending WHERE user_id = ?", (user_id,))

    async def get_pending(self):
        return await self.db.fetch_all("SELECT user_id, username FROM wb_pending ORDER BY requested_at")

    async def get_whitelist(self):
        rows = await self.db.fetch_all("SELECT user_id FROM wb_whitelist")
        return [row[0] for row in rows]

    async def wb_get_proxies(self):
        rows = await self.db.fetch_all("SELECT proxy FROM wb_proxies")
        return [row[0] for row in rows]

    async def wb_add_proxy(self, proxy: str):
        try:
            await self.db.execute("INSERT INTO wb_proxies (proxy) VALUES (?)", (proxy,))
            return True
        except:
            return False

    async def wb_remove_proxy(self, proxy: str):
        await self.db.execute("DELETE FROM wb_proxies WHERE proxy = ?", (proxy,))

    async def wb_update_proxy_stats(self, proxy: str, success: bool):
        if success:
            await self.db.execute(
                "UPDATE wb_proxies SET success_count = success_count + 1, last_used = ? WHERE proxy = ?",
                (datetime.utcnow().isoformat(), proxy)
            )
        else:
            await self.db.execute(
                "UPDATE wb_proxies SET fail_count = fail_count + 1, last_used = ? WHERE proxy = ?",
                (datetime.utcnow().isoformat(), proxy)
            )

# ---------- EarnMigo Engine ----------
class EMEngine:
    def __init__(self, crud: CRUD):
        self.crud = crud
        self.running = False
        self.paused = False
        self.cancel = False
        self.total = 0
        self.success = 0
        self.fail = 0
        self.processed = 0
        self.referral = DEFAULT_REFERRAL
        self.concurrent = EM_CONCURRENCY
        self.delay = EM_DELAY
        self.start_time = None
        self.referral_list = [DEFAULT_REFERRAL]
        self.referral_index = 0
        self.turbo_mode = False
        self.proxies = []
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

    async def run_registration(self, count: int, referral: str, progress_callback=None, email_list: List[str] = None):
        self.running = True
        self.paused = False
        self.cancel = False
        self.total = count
        self.success = 0
        self.fail = 0
        self.processed = 0
        self.start_time = time.time()

        connector = TCPConnector(
            limit=self.concurrent,
            limit_per_host=self.concurrent,
            ttl_dns_cache=300,
            enable_cleanup_closed=True,
        )
        timeout = ClientTimeout(total=10, connect=3)
        sem = asyncio.Semaphore(self.concurrent)

        async def worker(session, email):
            async with sem:
                if len(self.referral_list) > 1:
                    ref = self.referral_list[self.referral_index % len(self.referral_list)]
                    self.referral_index += 1
                else:
                    ref = referral
                proxy = random.choice(self.proxies) if self.proxies else None
                ok, em, info = await self.register_one(session, email, DEFAULT_PASSWORD, ref, proxy)
                self.processed += 1
                if ok:
                    self.success += 1
                    await self.crud.em_add_success(em, DEFAULT_PASSWORD, ref, info.get("authorized_key"), info.get("user_id"))
                else:
                    self.fail += 1
                    await self.crud.em_add_fail(em, DEFAULT_PASSWORD, ref, info)
                # Delay to respect rate limits
                await asyncio.sleep(self.delay)
                if progress_callback and (self.processed % 100 == 0 or self.processed == count):
                    await progress_callback(self.processed, self.success, self.fail, count)

        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            tasks = []
            for i in range(count):
                while self.paused and not self.cancel:
                    await asyncio.sleep(0.05)
                if self.cancel:
                    break
                email = email_list[i] if email_list and i < len(email_list) else ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + "@mailinator.com"
                tasks.append(asyncio.create_task(worker(session, email)))
            await asyncio.gather(*tasks, return_exceptions=True)

        self.running = False

# ---------- Holwin/Rex Engine ----------
class HolwinClient:
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://www.holwin123.top",
            "Referer": "https://www.holwin123.top/userRegister",
            "di": HOLWIN_DI,
            "vtoken": HOLWIN_VTOKEN,
        }
        self.session = aiohttp.ClientSession(headers=headers)
        return self

    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()

    async def post(self, path, json):
        url = f"{HOLWIN_BASE}{path}"
        async with self.session.post(url, json=json) as resp:
            return await resp.json()

class RexClient:
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=REX_HEADERS)
        return self

    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()

    async def post(self, path, json):
        url = f"{REX_BASE}{path}"
        async with self.session.post(url, json=json) as resp:
            return await resp.json()

class HWEngine:
    def __init__(self, crud: CRUD):
        self.crud = crud
        self.invite_codes = {"holwin": HOLWIN_INVITE, "rex": REX_INVITE}

    async def send_sms(self, platform: str, mobile: str):
        if platform == "holwin":
            async with HolwinClient() as client:
                return await client.post("/api/system/sms/send", {"mobile": mobile, "type": "reg_code"})
        else:
            async with RexClient() as client:
                return await client.post("/app/user/sendSmsCode", {"mobileNo": mobile})

    async def register(self, platform: str, mobile: str, otp: str, password: str, invite: str):
        if platform == "holwin":
            async with HolwinClient() as client:
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
            async with RexClient() as client:
                payload = {
                    "mobileNo": mobile,
                    "password": password,
                    "smsCode": otp,
                    "inviteCode": invite,
                }
                resp = await client.post("/app/user/register", payload)
                success = resp.get("code") == 200
        return success, resp

    def play_game(self, game: str, amount: float, balance: float):
        if amount > balance:
            return None, "Insufficient balance"
        win = 0
        result = ""
        if game == "crash":
            multiplier = random.uniform(1.0, 5.0)
            win = amount * multiplier if random.random() > 0.4 else 0
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
        new_balance = balance - amount + win
        return new_balance, f"{result}\nWin: ₹{win:.2f}"

# ---------- WhatsApp Unban Engine ----------
class WBEngine:
    def __init__(self, crud: CRUD):
        self.crud = crud
        self.running = {}
        self.stop_flags = {}
        self.semaphore = threading.Semaphore(WB_MAX_CONCURRENT_SENDS)

    async def send_appeal_email(self, tid: int, phone: str, name: str, reason: str, custom_reason: Optional[str] = None) -> Tuple[bool, str]:
        user = await self.crud.wb_get_user(tid)
        if not user:
            return False, "User not found"
        if not user[2] or not user[3]:
            return False, "Email/password not set"
        if user[6] == 0:
            return False, "Email invalid"
        if user[7] == 1:
            return False, "User banned"

        final_reason = custom_reason if custom_reason else reason
        templates = await self.crud.wb_get_templates(tid)
        if templates:
            template = random.choice(templates)[1]
        else:
            template = "Dear WhatsApp Team, my number {number} has been banned. I use it for {reason}. Please unban. Regards, {name}"
        body = template.format(number=phone, name=name or "User", reason=final_reason or "personal communication")

        smtp_host = user[9] if user[9] else "smtp.gmail.com"
        smtp_port = user[10] if user[10] else 587
        support_email = user[11] if user[11] else "support@whatsapp.com"

        msg = MIMEMultipart()
        msg["From"] = user[2]
        msg["To"] = support_email
        msg["Subject"] = f"Appeal for {phone}"
        msg.attach(MIMEText(body, "plain"))

        def send_sync():
            if smtp_port == 465:
                server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30)
            else:
                server = smtplib.SMTP(smtp_host, smtp_port, timeout=30)
                server.starttls()
            server.login(user[2], user[3])
            server.send_message(msg)
            server.quit()

        try:
            await asyncio.to_thread(send_sync)
            await self.crud.wb_log_appeal(tid, phone, True, "", template, "email")
            await self.crud.wb_update_last_appeal(phone)
            return True, "Email sent"
        except Exception as e:
            await self.crud.wb_log_appeal(tid, phone, False, str(e), template, "email")
            return False, f"Error: {str(e)[:40]}"

    async def start_auto(self, tid: int) -> str:
        if tid in self.running and self.running[tid]:
            return "Already running"
        user = await self.crud.wb_get_user(tid)
        if not user or user[7] == 1:
            return "User not found or banned"
        if user[6] == 0:
            return "Email invalid"
        if not user[2] or not user[3]:
            return "Email/password not set"
        numbers = await self.crud.wb_get_numbers(tid)
        if not numbers:
            return "No numbers to appeal"
        self.running[tid] = True
        self.stop_flags[tid] = False
        asyncio.create_task(self._auto_worker(tid, user, numbers))
        return "Auto-send started"

    async def stop_auto(self, tid: int) -> str:
        if tid not in self.running or not self.running[tid]:
            return "Not running"
        self.stop_flags[tid] = True
        self.running[tid] = False
        return "Auto-send stopped"

    async def _auto_worker(self, tid: int, user, numbers):
        name = user[1] or "User"
        reason = user[4] or "personal communication"
        delay = user[5] if user[5] else WB_DEFAULT_DELAY
        bot_instance = bot  # global

        while not self.stop_flags.get(tid, False):
            for num in numbers:
                if self.stop_flags.get(tid, False):
                    break
                phone = num[0]
                if num[4] == 1:
                    continue
                custom_reason = num[5]
                ok, msg = await self.send_appeal_email(tid, phone, name, reason, custom_reason)
                try:
                    if bot_instance:
                        await bot_instance.send_message(tid, f"{'✅' if ok else '❌'} {phone}: {msg}")
                except:
                    pass
                await asyncio.sleep(delay)
            await asyncio.sleep(1)
        self.running[tid] = False

    async def submit_web_form(self, tid: int, phone: str, custom_reason: Optional[str] = None) -> Tuple[bool, str]:
        if not SELENIUM_AVAILABLE:
            return False, "Selenium not enabled"
        user = await self.crud.wb_get_user(tid)
        if not user or user[7] == 1:
            return False, "User not found or banned"
        name = user[1] or "User"
        reason = custom_reason if custom_reason else (user[4] or "personal communication")
        email = user[2] or "user@example.com"

        proxies = await self.crud.wb_get_proxies()
        proxy = random.choice(proxies) if proxies else None

        def web_driver_task():
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            if proxy:
                options.add_argument(f'--proxy-server={proxy}')
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
            try:
                phone_input = driver.find_element(By.NAME, "phoneNumber")
                phone_input.send_keys(phone.replace("+91", ""))
            except:
                pass
            try:
                email_input = driver.find_element(By.NAME, "email")
                email_input.send_keys(email)
                confirm_input = driver.find_element(By.NAME, "confirmEmail")
                confirm_input.send_keys(email)
            except:
                pass
            try:
                android_radio = driver.find_element(By.XPATH, "//input[@value='Android']/..")
                android_radio.click()
            except:
                pass
            try:
                next_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Next Step')]")
                next_btn.click()
                time.sleep(2)
            except:
                pass

            if TWOCAPTCHA_AVAILABLE and TWOCAPTCHA_ENABLED:
                captcha_api_key = os.getenv("TWOCAPTCHA_API_KEY")
                if captcha_api_key:
                    try:
                        solver = TwoCaptcha(captcha_api_key)
                        captcha_element = driver.find_element(By.XPATH, "//div[@class='captcha']//img")
                        captcha_src = captcha_element.get_attribute('src')
                        import requests
                        img_data = requests.get(captcha_src, timeout=10).content
                        result = solver.normal(img_data)
                        if result:
                            captcha_input = driver.find_element(By.NAME, "captcha")
                            captcha_input.send_keys(result['code'])
                            driver.find_element(By.XPATH, "//button[@type='submit']").click()
                    except Exception as e:
                        logger.error(f"CAPTCHA solving failed: {e}")

            try:
                textarea = wait.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
                templates = asyncio.run(self.crud.wb_get_templates(tid))
                template = random.choice(templates)[1] if templates else "Dear WhatsApp Team, my number {number} has been banned. I use it for {reason}. Please unban. Regards, {name}"
                textarea.send_keys(template.format(number=phone, name=name, reason=reason))
            except:
                pass
            try:
                submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
                submit_btn.click()
            except:
                pass

            driver.quit()
            return True

        try:
            success = await asyncio.to_thread(web_driver_task)
            if success:
                await self.crud.wb_log_appeal(tid, phone, True, "", "webform", "webform")
                if proxy:
                    await self.crud.wb_update_proxy_stats(proxy, True)
                return True, "Web form submitted"
            else:
                return False, "Web form failed"
        except Exception as e:
            if proxy:
                await self.crud.wb_update_proxy_stats(proxy, False)
            return False, f"Web form error: {str(e)[:50]}"

# ---------- Global bot reference ----------
bot = None

# ---------- Inline Keyboards ----------
def main_menu(tid: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 EarnMigo", callback_data="em_menu")],
        [InlineKeyboardButton("📈 Holwin/Rex", callback_data="hw_menu")],
        [InlineKeyboardButton("📱 WhatsApp Unban", callback_data="wb_menu")],
        [InlineKeyboardButton("👤 Profile", callback_data="profile"), InlineKeyboardButton("❓ Help", callback_data="help")],
    ])

def em_main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Register", callback_data="em_register")],
        [InlineKeyboardButton("📊 Dashboard", callback_data="em_dashboard")],
        [InlineKeyboardButton("📜 History", callback_data="em_history")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="em_settings"), InlineKeyboardButton("📤 Export", callback_data="em_export")],
        [InlineKeyboardButton("⏸️ Pause", callback_data="em_pause"), InlineKeyboardButton("▶️ Resume", callback_data="em_resume"), InlineKeyboardButton("⏹️ Cancel", callback_data="em_cancel")],
        [InlineKeyboardButton("🎯 Quick Register", callback_data="em_quick")],
        [InlineKeyboardButton("🚀 Turbo Mode", callback_data="em_turbo")],
        [InlineKeyboardButton("🌐 Proxy Manager", callback_data="em_proxy")],
        [InlineKeyboardButton("🔁 Referral List", callback_data="em_referrals")],
        [InlineKeyboardButton("📤 Upload Emails", callback_data="em_upload")],
        [InlineKeyboardButton("⏰ Schedule", callback_data="em_schedule")],
        [InlineKeyboardButton("🔙 Home", callback_data="home")]
    ])

def em_settings_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📌 Set Referral", callback_data="em_set_ref")],
        [InlineKeyboardButton("⚡ Concurrency +10", callback_data="em_con_inc"), InlineKeyboardButton("⚡ Concurrency -10", callback_data="em_con_dec")],
        [InlineKeyboardButton("⏱️ Delay +0.01", callback_data="em_delay_inc"), InlineKeyboardButton("⏱️ Delay -0.01", callback_data="em_delay_dec")],
        [InlineKeyboardButton("🔙 Back", callback_data="em_back")]
    ])

def em_quick_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("100", callback_data="em_q_100"), InlineKeyboardButton("500", callback_data="em_q_500")],
        [InlineKeyboardButton("1000", callback_data="em_q_1000"), InlineKeyboardButton("5000", callback_data="em_q_5000")],
        [InlineKeyboardButton("🎛️ Custom", callback_data="em_custom")],
        [InlineKeyboardButton("🔙 Back", callback_data="em_back")]
    ])

def em_export_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📄 CSV", callback_data="em_export_csv"), InlineKeyboardButton("📄 TXT", callback_data="em_export_txt")],
        [InlineKeyboardButton("📄 JSON", callback_data="em_export_json")],
        [InlineKeyboardButton("🔙 Back", callback_data="em_back")]
    ])

def em_proxy_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Proxy", callback_data="em_add_proxy")],
        [InlineKeyboardButton("🗑️ Clear Proxies", callback_data="em_clear_proxies")],
        [InlineKeyboardButton("👁️ Show Proxies", callback_data="em_show_proxies")],
        [InlineKeyboardButton("🔙 Back", callback_data="em_back")]
    ])

def em_referral_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Referral", callback_data="em_add_ref")],
        [InlineKeyboardButton("🗑️ Clear Referrals", callback_data="em_clear_refs")],
        [InlineKeyboardButton("👁️ Show Referrals", callback_data="em_show_refs")],
        [InlineKeyboardButton("🔙 Back", callback_data="em_back")]
    ])

def hw_main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📱 Register", callback_data="hw_register")],
        [InlineKeyboardButton("📊 Balance", callback_data="hw_balance")],
        [InlineKeyboardButton("📜 History", callback_data="hw_history")],
        [InlineKeyboardButton("🔗 Referral", callback_data="hw_referral")],
        [InlineKeyboardButton("🎁 Daily Bonus", callback_data="hw_daily")],
        [InlineKeyboardButton("🎮 Games", callback_data="hw_games")],
        [InlineKeyboardButton("🏆 Leaderboard", callback_data="hw_leaderboard")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="hw_settings")],
        [InlineKeyboardButton("🔙 Home", callback_data="home")]
    ])

def hw_games_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Crash", callback_data="hw_game_crash")],
        [InlineKeyboardButton("🎲 Dice", callback_data="hw_game_dice")],
        [InlineKeyboardButton("🎡 Wheel", callback_data="hw_game_wheel")],
        [InlineKeyboardButton("💣 Mine", callback_data="hw_game_mine")],
        [InlineKeyboardButton("🃏 Andar Bahar", callback_data="hw_game_andar")],
        [InlineKeyboardButton("⚖️ Parity", callback_data="hw_game_parity")],
        [InlineKeyboardButton("🔙 Back", callback_data="hw_back")]
    ])

def wb_main_menu() -> InlineKeyboardMarkup:
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
        [InlineKeyboardButton("🔙 Home", callback_data="home")]
    ])

def wb_settings_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📧 Set Email", callback_data="wb_set_email")],
        [InlineKeyboardButton("🔑 Set Password", callback_data="wb_set_pass")],
        [InlineKeyboardButton("📝 Set Reason", callback_data="wb_set_reason")],
        [InlineKeyboardButton("⏱ Set Delay", callback_data="wb_set_delay")],
        [InlineKeyboardButton("🌐 Set Language", callback_data="wb_set_lang")],
        [InlineKeyboardButton("🔙 Back", callback_data="wb_back")]
    ])

def number_actions(phone: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📤 Appeal Now", callback_data=f"wb_appeal_single_{phone}")],
        [InlineKeyboardButton("🚫 Toggle Blacklist", callback_data=f"wb_blacklist_{phone}")],
        [InlineKeyboardButton("✏️ Set Reason", callback_data=f"wb_reason_{phone}")],
        [InlineKeyboardButton("❌ Remove", callback_data=f"wb_remove_{phone}")],
        [InlineKeyboardButton("🔙 Back", callback_data="wb_back")]
    ])

def language_selector() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇬🇧 English", callback_data="wb_lang_en")],
        [InlineKeyboardButton("🇮🇳 हिंदी", callback_data="wb_lang_hi")],
        [InlineKeyboardButton("🇪🇸 Español", callback_data="wb_lang_es")],
        [InlineKeyboardButton("🇫🇷 Français", callback_data="wb_lang_fr")],
    ])

# ---------- Handlers ----------
class CommandHandlers:
    def __init__(self, crud: CRUD, em: EMEngine, hw: HWEngine, wb: WBEngine):
        self.crud = crud
        self.em = em
        self.hw = hw
        self.wb = wb

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        tid = user.id
        await self.crud.wb_create_user(tid, user.first_name)

        if not await self.crud.is_whitelisted(tid) and tid not in ADMIN_IDS:
            await update.message.reply_text(
                "🔒 *Welcome!*\n\nYou need admin approval to use this bot.\n"
                "Click the button below to request access.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📩 Request Access", callback_data="request_access")]
                ]),
                parse_mode="Markdown"
            )
            return

        welcome = boxed(
            f"🚀 *Mega Bot Ultimate*\n\n"
            f"👨‍💻 Developer: {DEVELOPER_NAME}\n"
            f"📌 Admin: {ADMIN_USERNAME}\n\n"
            "Choose an engine from the buttons below.\n"
            "Each engine provides specialized automation.\n\n"
            "🤖 *EarnMigo* – Bulk account registration\n"
            "📈 *Holwin/Rex* – Referral & gaming platform\n"
            "📱 *WhatsApp Unban* – Automated ban appeals",
            "MegaBot v10.1"
        )
        await update.message.reply_text(welcome, parse_mode="Markdown", reply_markup=main_menu(tid))

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = boxed(
            "📖 *Help*\n\n"
            "Use the main menu buttons to navigate.\n"
            "Each engine has its own features.\n"
            "For admin commands, use /admin.\n"
            f"Contact {ADMIN_USERNAME} for support.",
            "Help"
        )
        await update.message.reply_text(help_text, parse_mode="Markdown")

    async def admin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.")
            return
        text = boxed(
            "👑 *Admin Panel*\n\n"
            "/approve <user_id> – approve user\n"
            "/reject <user_id> – reject user\n"
            "/whitelist – list whitelisted users\n"
            "/remove <user_id> – remove from whitelist\n"
            "/stats – global stats\n"
            "/backup – backup databases",
            "Admin"
        )
        await update.message.reply_text(text, parse_mode="Markdown")

    async def stats_global(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.")
            return
        em_total, em_success, em_fail = await self.crud.em_stats()
        hw_users = await self.crud.db.fetch_one("SELECT COUNT(*) FROM hw_users")
        wb_users = await self.crud.db.fetch_one("SELECT COUNT(*) FROM wb_users")
        text = boxed(
            f"📊 *Global Stats*\n\n"
            f"EarnMigo: Total {em_total}, Success {em_success}, Fail {em_fail}\n"
            f"Holwin/Rex: {hw_users[0] if hw_users else 0} users\n"
            f"WhatsApp Unban: {wb_users[0] if wb_users else 0} users",
            "Stats"
        )
        await update.message.reply_text(text, parse_mode="Markdown")

    async def approve(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        user = await self.crud.wb_get_user(tid)
        if not user:
            await update.message.reply_text("User not found.")
            return
        if user[6] == 1:
            await update.message.reply_text("Already approved.")
            return
        await self.crud.wb_update_user(tid, approved=1)
        await self.crud.add_whitelist(tid)
        await update.message.reply_text(f"✅ User {tid} approved.")
        try:
            await context.bot.send_message(tid, "🎉 You have been approved to use the bot. Use /start.")
        except:
            pass

    async def reject(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        await self.crud.wb_update_user(tid, approved=0)
        await self.crud.remove_whitelist(tid)
        await self.crud.remove_pending(tid)
        await update.message.reply_text(f"❌ User {tid} rejected.")
        try:
            await context.bot.send_message(tid, "⛔ Your access request has been rejected.")
        except:
            pass

    async def whitelist(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.")
            return
        whitelist = await self.crud.get_whitelist()
        if not whitelist:
            await update.message.reply_text("Whitelist is empty.")
            return
        text = "📋 Whitelisted users:\n" + "\n".join([str(uid) for uid in whitelist])
        await update.message.reply_text(text)

    async def remove_whitelist(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        await self.crud.remove_whitelist(tid)
        await self.crud.wb_update_user(tid, approved=0)
        await update.message.reply_text(f"🗑️ User {tid} removed from whitelist.")

    async def backup(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only.")
            return
        try:
            backup_path = f"backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.db"
            shutil.copyfile("mega_bot.db", backup_path)
            await update.message.reply_text(f"✅ Backup created: {backup_path}")
        except Exception as e:
            await update.message.reply_text(f"❌ Backup failed: {e}")

# ---------- Callback Handler ----------
class CallbackHandlers:
    def __init__(self, crud: CRUD, em: EMEngine, hw: HWEngine, wb: WBEngine):
        self.crud = crud
        self.em = em
        self.hw = hw
        self.wb = wb
        self.temp_data = {}

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        data = query.data
        user_id = update.effective_user.id

        if data == "home":
            await query.edit_message_text(
                "🏠 *Main Menu*", parse_mode="Markdown", reply_markup=main_menu(user_id)
            )
            return

        if data == "request_access":
            await self.crud.add_pending(user_id, update.effective_user.username or str(user_id))
            await query.edit_message_text("✅ Request sent to admin. Please wait.")
            for admin in ADMIN_IDS:
                try:
                    await context.bot.send_message(
                        admin,
                        f"📩 New permission request from @{update.effective_user.username or user_id} (ID: {user_id}).\n"
                        f"Use /approve {user_id} or /reject {user_id}."
                    )
                except:
                    pass
            return

        if data.startswith("em_"):
            await self._handle_em(query, context, user_id)
        elif data.startswith("hw_"):
            await self._handle_hw(query, context, user_id)
        elif data.startswith("wb_"):
            await self._handle_wb(query, context, user_id)
        else:
            await query.edit_message_text("❌ Unknown action.")

    # ---- EM ----
    async def _handle_em(self, query, context, user_id):
        data = query.data
        if data == "em_menu":
            await query.edit_message_text(
                "🤖 *EarnMigo Engine*\n\n"
                "Bulk register accounts with referral codes.",
                parse_mode="Markdown",
                reply_markup=em_main_menu()
            )
        elif data == "em_register":
            await query.edit_message_text(
                "📌 Enter count and optional referral:\n"
                "Format: `count referral`\n"
                "Example: `100 1816`",
                parse_mode="Markdown"
            )
            context.user_data["em_state"] = {"waiting_for_register": True}
        elif data == "em_dashboard":
            await query.edit_message_text(format_em_dashboard(self.crud, self.em), parse_mode="Markdown", reply_markup=em_main_menu())
        elif data == "em_history":
            total, success, fail = await self.crud.em_stats()
            recent = await self.crud.em_get_recent(10)
            text = f"📜 *History*\nTotal: `{total}` | ✅ Success: `{success}` | ❌ Fail: `{fail}`\n\n**Latest 10:**\n" + "\n".join([f"• `{r[0]}` (key: `{r[1][:15]}...`)" for r in recent]) if recent else "No data."
            await query.edit_message_text(text, reply_markup=em_main_menu(), parse_mode="Markdown")
        elif data == "em_settings":
            await query.edit_message_text("⚙️ *EM Settings*", reply_markup=em_settings_menu(), parse_mode="Markdown")
        elif data == "em_back":
            await query.edit_message_text("🤖 *EarnMigo*", reply_markup=em_main_menu())
        elif data == "em_set_ref":
            await query.edit_message_text("📌 Enter main referral code:")
            context.user_data["em_state"] = {"waiting_for_referral": True}
        elif data == "em_con_inc":
            self.em.concurrent = min(self.em.concurrent + 10, 1000)
            await query.edit_message_text(f"⚡ Concurrency set to `{self.em.concurrent}`", reply_markup=em_settings_menu(), parse_mode="Markdown")
        elif data == "em_con_dec":
            self.em.concurrent = max(self.em.concurrent - 10, 1)
            await query.edit_message_text(f"⚡ Concurrency set to `{self.em.concurrent}`", reply_markup=em_settings_menu(), parse_mode="Markdown")
        elif data == "em_delay_inc":
            self.em.delay = min(self.em.delay + 0.01, 1.0)
            await query.edit_message_text(f"⏱️ Delay set to `{self.em.delay:.3f}s`", reply_markup=em_settings_menu(), parse_mode="Markdown")
        elif data == "em_delay_dec":
            self.em.delay = max(self.em.delay - 0.01, 0.0)
            await query.edit_message_text(f"⏱️ Delay set to `{self.em.delay:.3f}s`", reply_markup=em_settings_menu(), parse_mode="Markdown")
        elif data == "em_quick":
            await query.edit_message_text("🎯 Choose count:", reply_markup=em_quick_menu())
        elif data.startswith("em_q_"):
            count = int(data.split("_")[2])
            if self.em.running:
                await query.edit_message_text("⏳ Already running. Cancel first.")
                return
            await query.edit_message_text(f"🚀 Starting {count} accounts...")
            async def progress_callback(processed, success, fail, total):
                await query.edit_message_text(format_em_dashboard(self.crud, self.em), reply_markup=em_main_menu(), parse_mode="Markdown")
            asyncio.create_task(self.em.run_registration(count, self.em.referral, progress_callback))
        elif data == "em_custom":
            await query.edit_message_text("🎛️ Enter count (1-50000):")
            context.user_data["em_state"] = {"waiting_for_custom_count": True}
        elif data == "em_turbo":
            self.em.turbo_mode = not self.em.turbo_mode
            if self.em.turbo_mode:
                self.em.concurrent = EM_TURBO_CONCURRENCY
                self.em.delay = EM_TURBO_DELAY
                await query.edit_message_text("🚀 Turbo Mode **ON**\nConcurrency: 600 | Delay: 0.000s", reply_markup=em_main_menu(), parse_mode="Markdown")
            else:
                self.em.concurrent = EM_CONCURRENCY
                self.em.delay = EM_DELAY
                await query.edit_message_text("🚀 Turbo Mode **OFF**", reply_markup=em_main_menu(), parse_mode="Markdown")
        elif data == "em_pause":
            if self.em.running:
                self.em.paused = True
                await query.edit_message_text("⏸️ Paused.", reply_markup=em_main_menu())
            else:
                await query.edit_message_text("Not running.", reply_markup=em_main_menu())
        elif data == "em_resume":
            if self.em.running and self.em.paused:
                self.em.paused = False
                await query.edit_message_text("▶️ Resumed.", reply_markup=em_main_menu())
            else:
                await query.edit_message_text("Not paused.", reply_markup=em_main_menu())
        elif data == "em_cancel":
            if self.em.running:
                self.em.cancel = True
                await query.edit_message_text("⏹️ Cancelling...", reply_markup=em_main_menu())
            else:
                await query.edit_message_text("Not running.", reply_markup=em_main_menu())
        elif data == "em_proxy":
            await query.edit_message_text("🌐 *Proxy Manager*", reply_markup=em_proxy_menu(), parse_mode="Markdown")
        elif data == "em_add_proxy":
            await query.edit_message_text("🌐 Send proxy line by line:\nExample:\n`http://user:pass@1.2.3.4:8080`", parse_mode="Markdown")
            context.user_data["em_state"] = {"waiting_for_proxies": True}
        elif data == "em_clear_proxies":
            self.em.proxies.clear()
            await query.edit_message_text("🗑️ Proxies cleared.", reply_markup=em_main_menu())
        elif data == "em_show_proxies":
            if self.em.proxies:
                text = "🌐 *Proxies:*\n" + "\n".join([f"{i+1}. `{p}`" for i, p in enumerate(self.em.proxies)])
            else:
                text = "No proxies loaded."
            await query.edit_message_text(text, reply_markup=em_proxy_menu(), parse_mode="Markdown")
        elif data == "em_referrals":
            await query.edit_message_text("🔁 *Referral Manager*", reply_markup=em_referral_menu(), parse_mode="Markdown")
        elif data == "em_add_ref":
            await query.edit_message_text("📌 Send referral codes (one per line):")
            context.user_data["em_state"] = {"waiting_for_referrals": True}
        elif data == "em_clear_refs":
            self.em.referral_list = [self.em.referral]
            await query.edit_message_text("🗑️ Referrals reset to main only.", reply_markup=em_main_menu())
        elif data == "em_show_refs":
            text = "🔁 *Referrals:*\n" + "\n".join([f"{i+1}. `{r}`" for i, r in enumerate(self.em.referral_list)])
            await query.edit_message_text(text, reply_markup=em_referral_menu(), parse_mode="Markdown")
        elif data == "em_export":
            await query.edit_message_text("📤 Choose format:", reply_markup=em_export_menu())
        elif data in ["em_export_csv", "em_export_txt", "em_export_json"]:
            rows = await self.crud.em_get_all_success()
            if not rows:
                await query.edit_message_text("❌ No data.", reply_markup=em_main_menu())
                return
            if data == "em_export_csv":
                output = io.StringIO()
                writer = csv.writer(output)
                writer.writerow(["Email", "Authorized_Key", "Created_At"])
                writer.writerows(rows)
                content = output.getvalue()
                fname = "em_registrations.csv"
            elif data == "em_export_txt":
                content = "Email, Authorized_Key\n" + "\n".join([f"{r[0]}, {r[1]}" for r in rows])
                fname = "em_accounts.txt"
            else:
                content = json.dumps([{"email": r[0], "key": r[1], "created": r[2]} for r in rows], indent=2)
                fname = "em_accounts.json"
            await query.edit_message_text("📤 Exporting...", reply_markup=em_main_menu())
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=io.BytesIO(content.encode()),
                filename=fname,
                caption="✅ Done."
            )
        elif data == "em_schedule":
            await query.edit_message_text(
                "⏰ *Schedule Registration*\n"
                "Send time, count, and referral (optional).\n"
                "Examples:\n"
                "`10:30 500` – run at 10:30 AM today\n"
                "`in 5m 100 1816` – run in 5 minutes\n"
                "`in 2h 1000` – run in 2 hours\n"
                "`every 30m 200` – repeat every 30 minutes\n"
                "`daily 09:00 300` – run daily at 9 AM",
                parse_mode="Markdown"
            )
            context.user_data["em_state"] = {"waiting_for_schedule": True}
        elif data == "em_upload":
            await query.edit_message_text("📤 Send a text file with one email per line.")
            context.user_data["em_state"] = {"waiting_for_email_file": True}
        else:
            await query.edit_message_text("Unknown EM action.")

    # ---- HW ----
    async def _handle_hw(self, query, context, user_id):
        data = query.data
        if data == "hw_menu":
            await query.edit_message_text(
                "📈 *Holwin/Rex Engine*\n\n"
                "Register on these platforms using your invite codes.",
                parse_mode="Markdown",
                reply_markup=hw_main_menu()
            )
        elif data == "hw_register":
            await query.edit_message_text(
                "📱 Choose platform:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🏠 Holwin", callback_data="hw_platform_holwin")],
                    [InlineKeyboardButton("📈 Rexproearn", callback_data="hw_platform_rex")],
                    [InlineKeyboardButton("🔙 Back", callback_data="hw_back")]
                ])
            )
        elif data.startswith("hw_platform_"):
            platform = data.split("_")[2]
            context.user_data["hw_state"] = {"step": "mobile", "platform": platform}
            invite = HOLWIN_INVITE if platform == "holwin" else REX_INVITE
            await query.edit_message_text(
                f"✅ Selected: *{platform.upper()}*\nInvite code: `{invite}`\n\n📱 Enter mobile number (10-15 digits):",
                parse_mode="Markdown"
            )
        elif data == "hw_back":
            await query.edit_message_text("📈 *Holwin/Rex*", reply_markup=hw_main_menu())
        elif data == "hw_balance":
            user = await self.crud.hw_get_user(user_id)
            if user and user[5]:
                await query.edit_message_text(f"💰 Balance: ₹{user[6]:.2f}", reply_markup=hw_main_menu())
            else:
                await query.edit_message_text("⚠️ Not registered. Please register first.", reply_markup=hw_main_menu())
        elif data == "hw_history":
            await query.edit_message_text("📜 *Transaction History*\n(coming soon)", reply_markup=hw_main_menu(), parse_mode="Markdown")
        elif data == "hw_referral":
            user = await self.crud.hw_get_user(user_id)
            if user and user[5]:
                invite = user[7] or (HOLWIN_INVITE if user[1] == "holwin" else REX_INVITE)
                bot_username = (await context.bot.get_me()).username
                link = f"https://t.me/{bot_username}?start=ref_{invite}"
                await query.edit_message_text(f"🔗 *Referral Link*\n`{link}`\n\nInvite code: `{invite}`", reply_markup=hw_main_menu(), parse_mode="Markdown")
            else:
                await query.edit_message_text("⚠️ Register first.", reply_markup=hw_main_menu())
        elif data == "hw_daily":
            user = await self.crud.hw_get_user(user_id)
            if not user or not user[5]:
                await query.edit_message_text("⚠️ Register first.", reply_markup=hw_main_menu())
                return
            last = user[8]
            if last:
                last_dt = datetime.fromisoformat(last)
                if datetime.utcnow() - last_dt < timedelta(days=1):
                    await query.edit_message_text("❌ Already claimed today.", reply_markup=hw_main_menu())
                    return
            bonus = random.randint(10, 50)
            new_balance = user[6] + bonus
            await self.crud.hw_update_balance(user_id, bonus)
            await self.crud.db.execute(
                "UPDATE hw_users SET last_daily = ? WHERE telegram_id = ?",
                (datetime.utcnow().isoformat(), user_id)
            )
            await self.crud.hw_add_transaction(user_id, "daily_bonus", bonus, "Daily bonus")
            await query.edit_message_text(f"✅ ₹{bonus} credited. New balance: ₹{new_balance:.2f}", reply_markup=hw_main_menu())
        elif data == "hw_games":
            await query.edit_message_text("🎮 *Games*", reply_markup=hw_games_menu(), parse_mode="Markdown")
        elif data.startswith("hw_game_"):
            game = data.split("_")[2]
            user = await self.crud.hw_get_user(user_id)
            if not user or not user[5]:
                await query.edit_message_text("⚠️ Register first.", reply_markup=hw_main_menu())
                return
            await query.edit_message_text(f"🎮 *{game.capitalize()}*\nEnter bet amount (₹):", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="hw_back")]]))
            context.user_data["hw_state"] = {"game": game, "step": "bet"}
        elif data == "hw_leaderboard":
            rows = await self.crud.hw_leaderboard()
            if rows:
                text = "🏆 *Leaderboard*\n" + "\n".join([f"{i+1}. {r[0] or 'Anonymous'} – ₹{r[1]:.2f}" for i, r in enumerate(rows)])
            else:
                text = "No data."
            await query.edit_message_text(text, reply_markup=hw_main_menu(), parse_mode="Markdown")
        elif data == "hw_settings":
            await query.edit_message_text("⚙️ *Settings*\nUse /setemail, /setpass for this engine.", reply_markup=hw_main_menu())
        else:
            await query.edit_message_text("Unknown HW action.")

    # ---- WB ----
    async def _handle_wb(self, query, context, user_id):
        data = query.data
        if data == "wb_menu":
            await query.edit_message_text(
                "📱 *WhatsApp Unban Engine*\n\n"
                "Automate ban appeals via email and web forms.",
                parse_mode="Markdown",
                reply_markup=wb_main_menu()
            )
        elif data == "wb_add":
            await query.edit_message_text("📞 Enter phone number (with or without +91):")
            context.user_data["wb_state"] = {"waiting_for_number": True}
        elif data == "wb_list":
            numbers = await self.crud.wb_get_numbers(user_id)
            if not numbers:
                await query.edit_message_text("📭 No numbers.")
                return
            for n in numbers:
                status = "🚫 Blacklisted" if n[4] else "✅ Active"
                appeals = n[3]
                last = n[2][:10] if n[2] else "Never"
                custom = f"📝 Reason: {n[5]}" if n[5] else ""
                text = f"📞 *{n[0]}*\n{status}\n📤 Appeals: {appeals}\n🕒 Last: {last}\n{custom}"
                await query.message.reply_text(text, reply_markup=number_actions(n[0]))
            await query.edit_message_text("📋 End of list.", reply_markup=wb_main_menu())
        elif data == "wb_appeal_all":
            await self._appeal_all(query, user_id)
        elif data == "wb_appeal_one":
            numbers = await self.crud.wb_get_numbers(user_id)
            if not numbers:
                await query.edit_message_text("📭 No numbers.")
                return
            keyboard = []
            for n in numbers:
                keyboard.append([InlineKeyboardButton(n[0], callback_data=f"wb_appeal_single_{n[0]}")])
            keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="wb_back")])
            await query.edit_message_text("🔢 Select a number:", reply_markup=InlineKeyboardMarkup(keyboard))
        elif data.startswith("wb_appeal_single_"):
            phone = data.replace("wb_appeal_single_", "")
            await self._appeal_one(query, user_id, phone)
        elif data == "wb_mass":
            await query.edit_message_text("🔢 Enter number of appeals per number:")
            context.user_data["wb_state"] = {"waiting_for_mass_count": True}
        elif data == "wb_auto":
            res = await self.wb.start_auto(user_id)
            await query.edit_message_text(f"🔁 {res}", reply_markup=wb_main_menu())
        elif data == "wb_stop_auto":
            res = await self.wb.stop_auto(user_id)
            await query.edit_message_text(f"🛑 {res}", reply_markup=wb_main_menu())
        elif data == "wb_webform":
            numbers = await self.crud.wb_get_numbers(user_id)
            if not numbers:
                await query.edit_message_text("📭 No numbers.")
                return
            keyboard = []
            for n in numbers:
                keyboard.append([InlineKeyboardButton(n[0], callback_data=f"wb_form_{n[0]}")])
            keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="wb_back")])
            await query.edit_message_text("🌐 Select number for web form:", reply_markup=InlineKeyboardMarkup(keyboard))
        elif data.startswith("wb_form_"):
            phone = data.replace("wb_form_", "")
            ok, msg = await self.wb.submit_web_form(user_id, phone)
            await query.edit_message_text(f"{'✅' if ok else '❌'} {msg}", reply_markup=wb_main_menu())
        elif data == "wb_templates":
            templates = await self.crud.wb_get_templates(user_id, include_default=True)
            if not templates:
                await query.edit_message_text("📭 No templates.")
                return
            text = "📝 *Templates*\n"
            for t in templates:
                text += f"ID: {t[0]} | {t[1][:40]}...\n"
            keyboard = []
            for t in templates:
                if not t[0]: continue  # skip default? Actually we want delete only custom
                if t[0] != 0:  # custom templates have tid = user_id, but we don't have tid stored; we need to check if is_default=0
                    # We'll use db to check, but we don't have is_default in result. We'll query again.
                    pass
            # We'll just add a delete button for each template (only if not default)
            # Simplification: we can ask user to send template id to delete.
            keyboard.append([InlineKeyboardButton("➕ Add Template", callback_data="wb_add_template")])
            keyboard.append([InlineKeyboardButton("🗑️ Delete Template (send ID)", callback_data="wb_del_template_prompt")])
            keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="wb_back")])
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        elif data == "wb_del_template_prompt":
            await query.edit_message_text("📝 Send the template ID to delete:")
            context.user_data["wb_state"] = {"waiting_for_del_template": True}
        elif data == "wb_add_template":
            await query.edit_message_text("📝 Send your template (use {number}, {name}, {reason}):")
            context.user_data["wb_state"] = {"waiting_for_template": True}
        elif data.startswith("wb_del_template_"):
            template_id = int(data.split("_")[3])
            if await self.crud.wb_delete_template(user_id, template_id):
                await query.edit_message_text("✅ Template deleted.")
            else:
                await query.edit_message_text("❌ Failed to delete.")
            await self._handle_wb(query, context, user_id)
        elif data == "wb_scheduler":
            jobs = await self.crud.wb_get_scheduler_jobs(user_id)
            if not jobs:
                await query.edit_message_text("⏰ No active scheduler jobs.")
            else:
                text = "⏰ *Scheduler Jobs*\n"
                keyboard = []
                for j in jobs:
                    cron = j[2] if j[2] else f"every {j[3]} min"
                    next_run = j[4][:16] if j[4] else "N/A"
                    text += f"ID: {j[0]} | {cron} | Next: {next_run}\n"
                    keyboard.append([InlineKeyboardButton(f"🗑️ Delete {j[0]}", callback_data=f"wb_del_scheduler_{j[0]}")])
                keyboard.append([InlineKeyboardButton("➕ Add Scheduler", callback_data="wb_add_scheduler")])
                keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="wb_back")])
                await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        elif data == "wb_add_scheduler":
            await query.edit_message_text("⏰ Enter cron expression (e.g., '0 9 * * *') or minutes interval (e.g., '60'):")
            context.user_data["wb_state"] = {"waiting_for_scheduler": True}
        elif data.startswith("wb_del_scheduler_"):
            job_id = int(data.split("_")[3])
            await self.crud.wb_delete_scheduler_job(job_id)
            if scheduler:
                try:
                    scheduler.remove_job(f"wb_job_{job_id}")
                except:
                    pass
            await query.edit_message_text("✅ Scheduler job deleted.")
            await self._handle_wb(query, context, user_id)  # refresh
        elif data == "wb_stats":
            stats = await self.crud.wb_get_stats(user_id)
            if not stats:
                await query.edit_message_text("User not found.")
                return
            user = stats["user"]
            text = boxed(
                f"📊 *Dashboard*\n\n"
                f"Total numbers: {stats['total_numbers']}\n"
                f"Appealed: {stats['appealed']}\n"
                f"Pending: {stats['total_numbers'] - stats['appealed']}\n"
                f"Email: {user[2] or 'Not set'}\n"
                f"Delay: {user[5] or WB_DEFAULT_DELAY}s\n"
                f"Reason: {user[4] or 'Not set'}\n"
                f"Total Appeals: {stats['total_logs']} (✅ {stats['success_logs']} | ❌ {stats['failed_logs']})\n"
                f"Language: {user[8].upper()}",
                "WB Stats"
            )
            await query.edit_message_text(text, reply_markup=wb_main_menu(), parse_mode="Markdown")
        elif data == "wb_settings":
            await query.edit_message_text("⚙️ *Settings*", reply_markup=wb_settings_menu(), parse_mode="Markdown")
        elif data == "wb_back":
            await query.edit_message_text("📱 *WhatsApp Unban*", reply_markup=wb_main_menu())
        elif data == "wb_set_email":
            await query.edit_message_text("📧 Enter your Gmail address:")
            context.user_data["wb_state"] = {"waiting_for_email": True}
        elif data == "wb_set_pass":
            await query.edit_message_text("🔑 Enter your Gmail App Password:")
            context.user_data["wb_state"] = {"waiting_for_password": True}
        elif data == "wb_set_reason":
            await query.edit_message_text("📝 Enter your reason:")
            context.user_data["wb_state"] = {"waiting_for_reason": True}
        elif data == "wb_set_delay":
            await query.edit_message_text("⏱ Enter delay (seconds, min 0.5):")
            context.user_data["wb_state"] = {"waiting_for_delay": True}
        elif data == "wb_set_lang":
            await query.edit_message_text("🌐 Select language:", reply_markup=language_selector())
        elif data.startswith("wb_lang_"):
            lang = data.split("_")[2]
            await self.crud.wb_update_user(user_id, language=lang)
            await query.edit_message_text(f"✅ Language set to {lang.upper()}", reply_markup=wb_settings_menu())
        elif data.startswith("wb_blacklist_"):
            phone = data.replace("wb_blacklist_", "")
            await self.crud.wb_toggle_blacklist(phone)
            await query.edit_message_text(f"🚫 Blacklist toggled for {phone}")
            await self._handle_wb(query, context, user_id)
        elif data.startswith("wb_remove_"):
            phone = data.replace("wb_remove_", "")
            if await self.crud.wb_remove_number(user_id, phone):
                await query.edit_message_text(f"✅ Removed {phone}")
            else:
                await query.edit_message_text("❌ Not found")
            await self._handle_wb(query, context, user_id)
        elif data.startswith("wb_reason_"):
            phone = data.replace("wb_reason_", "")
            await query.edit_message_text("📝 Enter custom reason for this number (or '-' for default):")
            context.user_data["wb_state"] = {"waiting_for_number_reason": phone}
        else:
            await query.edit_message_text("Unknown WB action.")

    async def _appeal_all(self, query, user_id):
        user = await self.crud.wb_get_user(user_id)
        if not user or user[7] == 1:
            await query.edit_message_text("⛔ Banned or not found.")
            return
        if user[6] == 0:
            await query.edit_message_text("❌ Email invalid.")
            return
        if not user[2] or not user[3]:
            await query.edit_message_text("❌ Email/password not set.")
            return
        numbers = await self.crud.wb_get_numbers(user_id)
        if not numbers:
            await query.edit_message_text("📭 No numbers.")
            return
        await query.edit_message_text("⏳ Sending appeals...")
        name = user[1] or "User"
        reason = user[4] or "personal communication"
        for n in numbers:
            if n[4] == 1:
                continue
            phone = n[0]
            custom = n[5]
            ok, msg = await self.wb.send_appeal_email(user_id, phone, name, reason, custom)
            if ok:
                await self.crud.wb_update_last_appeal(phone)
            await query.message.reply_text(f"{'✅' if ok else '❌'} {phone}: {msg}")
            await asyncio.sleep(0.5)
        await query.edit_message_text("✅ Appeal All completed.", reply_markup=wb_main_menu())

    async def _appeal_one(self, query, user_id, phone):
        user = await self.crud.wb_get_user(user_id)
        if not user or user[7] == 1:
            await query.edit_message_text("⛔ Banned or not found.")
            return
        if user[6] == 0:
            await query.edit_message_text("❌ Email invalid.")
            return
        if not user[2] or not user[3]:
            await query.edit_message_text("❌ Email/password not set.")
            return
        num = await self.crud.wb_get_number(phone)
        if not num or num[1] != user_id:
            await query.edit_message_text("❌ Number not yours.")
            return
        if num[4] == 1:
            await query.edit_message_text("🚫 Number blacklisted.")
            return
        name = user[1] or "User"
        reason = user[4] or "personal communication"
        custom = num[5]
        ok, msg = await self.wb.send_appeal_email(user_id, phone, name, reason, custom)
        if ok:
            await self.crud.wb_update_last_appeal(phone)
        await query.edit_message_text(f"{'✅' if ok else '❌'} {phone}: {msg}", reply_markup=wb_main_menu())

# ---------- Message Handlers ----------
class MessageHandlers:
    def __init__(self, crud: CRUD, em: EMEngine, hw: HWEngine, wb: WBEngine):
        self.crud = crud
        self.em = em
        self.hw = hw
        self.wb = wb

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        text = update.message.text.strip()

        if "em_state" in context.user_data:
            await self._handle_em_text(update, context)
        elif "hw_state" in context.user_data:
            await self._handle_hw_text(update, context)
        elif "wb_state" in context.user_data:
            await self._handle_wb_text(update, context)
        else:
            await update.message.reply_text("Use the buttons or /start.")

    async def _handle_em_text(self, update, context):
        state = context.user_data["em_state"]
        text = update.message.text
        user_id = update.effective_user.id

        if state.get("waiting_for_register"):
            parts = text.split()
            try:
                count = int(parts[0])
                referral = parts[1] if len(parts) > 1 else self.em.referral
                if self.em.running:
                    await update.message.reply_text("⏳ Already running.")
                    return
                context.user_data.pop("em_state")
                await update.message.reply_text(f"🚀 Starting {count} accounts...")
                async def progress_callback(processed, success, fail, total):
                    await update.message.reply_text(format_em_dashboard(self.crud, self.em), reply_markup=em_main_menu(), parse_mode="Markdown")
                asyncio.create_task(self.em.run_registration(count, referral, progress_callback))
            except ValueError:
                await update.message.reply_text("❌ Invalid format. Send: `count referral`")
        elif state.get("waiting_for_custom_count"):
            try:
                count = int(text)
                if count < 1 or count > 50000:
                    await update.message.reply_text("❌ 1-50000 only.")
                    return
                context.user_data.pop("em_state")
                if self.em.running:
                    await update.message.reply_text("⏳ Already running.")
                    return
                await update.message.reply_text(f"🚀 Starting {count} accounts...")
                async def progress_callback(processed, success, fail, total):
                    await update.message.reply_text(format_em_dashboard(self.crud, self.em), reply_markup=em_main_menu(), parse_mode="Markdown")
                asyncio.create_task(self.em.run_registration(count, self.em.referral, progress_callback))
            except ValueError:
                await update.message.reply_text("❌ Invalid number.")
        elif state.get("waiting_for_referral"):
            self.em.referral = text
            context.user_data.pop("em_state")
            await update.message.reply_text(f"✅ Main referral set to `{self.em.referral}`", parse_mode="Markdown")
        elif state.get("waiting_for_proxies"):
            lines = text.splitlines()
            added = 0
            for line in lines:
                if line.strip():
                    self.em.proxies.append(line.strip())
                    added += 1
            await update.message.reply_text(f"✅ Added {added} proxies. Total: {len(self.em.proxies)}")
            context.user_data.pop("em_state")
        elif state.get("waiting_for_referrals"):
            refs = [r.strip() for r in text.splitlines() if r.strip()]
            if refs:
                self.em.referral_list.extend(refs)
                await update.message.reply_text(f"✅ Added {len(refs)} referrals. Total: {len(self.em.referral_list)}")
            else:
                await update.message.reply_text("❌ No valid codes.")
            context.user_data.pop("em_state")
        elif state.get("waiting_for_schedule"):
            parts = text.split()
            if len(parts) < 2:
                await update.message.reply_text("❌ Need time and count. Example: `10:30 500`")
                return
            time_str = parts[0]
            try:
                count = int(parts[1])
                referral = parts[2] if len(parts) > 2 else self.em.referral
            except:
                await update.message.reply_text("❌ Invalid count.")
                return
            run_time = self._em_schedule(time_str, count, referral)
            if run_time:
                context.user_data.pop("em_state")
                await update.message.reply_text(f"⏰ Scheduled for {run_time.strftime('%Y-%m-%d %H:%M')} with {count} accounts.")
            else:
                await update.message.reply_text("❌ Invalid time format.")
        elif state.get("waiting_for_email_file"):
            if update.message.document:
                file = await update.message.get_file()
                content = await file.download_as_bytearray()
                emails = content.decode().splitlines()
                emails = [e.strip() for e in emails if e.strip()]
                if not emails:
                    await update.message.reply_text("❌ No emails found.")
                    return
                if self.em.running:
                    await update.message.reply_text("⏳ Already running.")
                    return
                context.user_data.pop("em_state")
                await update.message.reply_text(f"📤 Starting registration for {len(emails)} emails...")
                async def progress_callback(processed, success, fail, total):
                    await update.message.reply_text(format_em_dashboard(self.crud, self.em), reply_markup=em_main_menu(), parse_mode="Markdown")
                asyncio.create_task(self.em.run_registration(len(emails), self.em.referral, progress_callback, email_list=emails))
            else:
                await update.message.reply_text("📤 Please send a text file.")
        else:
            await update.message.reply_text("Unknown state.")

    def _em_schedule(self, time_str: str, count: int, referral: str):
        now = datetime.now()
        if time_str.startswith("in "):
            parts = time_str.split()
            if len(parts) == 2:
                val = int(parts[1][:-1])
                unit = parts[1][-1]
                if unit == 'm':
                    delta = timedelta(minutes=val)
                elif unit == 'h':
                    delta = timedelta(hours=val)
                else:
                    delta = timedelta(seconds=val)
                run_time = now + delta
                trigger = DateTrigger(run_time=run_time)
        elif time_str.startswith("every "):
            parts = time_str.split()
            if len(parts) == 2:
                val = int(parts[1][:-1])
                unit = parts[1][-1]
                if unit == 'm':
                    seconds = val * 60
                elif unit == 'h':
                    seconds = val * 3600
                else:
                    seconds = val
                trigger = IntervalTrigger(seconds=seconds)
                run_time = now + timedelta(seconds=seconds)
            else:
                return None
        elif time_str.startswith("daily "):
            parts = time_str.split()
            if len(parts) == 2:
                hour, minute = map(int, parts[1].split(':'))
                trigger = CronTrigger(hour=hour, minute=minute)
                run_time = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
                if run_time < now:
                    run_time += timedelta(days=1)
            else:
                return None
        else:
            try:
                hour, minute = map(int, time_str.split(':'))
                trigger = DateTrigger(run_time=datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0))
                run_time = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
                if run_time < now:
                    run_time += timedelta(days=1)
            except:
                return None

        async def job_func():
            await self.em.run_registration(count, referral, None)

        scheduler.add_job(job_func, trigger=trigger, id=f"em_sched_{int(time.time())}")
        return run_time

    async def _handle_hw_text(self, update, context):
        state = context.user_data["hw_state"]
        text = update.message.text
        user_id = update.effective_user.id

        if state.get("step") == "mobile":
            mobile = text.strip()
            if not re.match(r"^\d{10,15}$", mobile):
                await update.message.reply_text("❌ Invalid. Enter 10-15 digits:")
                return
            context.user_data["hw_state"]["mobile"] = mobile
            platform = state.get("platform")
            resp = await self.hw.send_sms(platform, mobile)
            if (platform == "holwin" and resp.get("code") != 0) or (platform == "rex" and resp.get("code") != 200):
                await update.message.reply_text(f"❌ OTP request failed: {resp.get('msg', 'Unknown')}")
                context.user_data.pop("hw_state")
                return
            context.user_data["hw_state"]["step"] = "otp"
            await update.message.reply_text("✅ OTP sent! Enter OTP:")
        elif state.get("step") == "otp":
            otp = text.strip()
            if not otp.isdigit():
                await update.message.reply_text("❌ OTP must be numeric. Try again:")
                return
            context.user_data["hw_state"]["otp"] = otp
            context.user_data["hw_state"]["step"] = "password"
            await update.message.reply_text("🔑 Set a password (min 6 chars, or type 'skip' for default):")
        elif state.get("step") == "password":
            pwd = text.strip()
            if pwd.lower() == "skip":
                pwd = "Dk12345dk" if state.get("platform") == "rex" else "Password@123"
            elif len(pwd) < 6:
                await update.message.reply_text("❌ Min 6 characters. Try again or type 'skip':")
                return
            context.user_data["hw_state"]["password"] = pwd
            context.user_data["hw_state"]["step"] = "confirm"
            platform = state.get("platform")
            invite = HOLWIN_INVITE if platform == "holwin" else REX_INVITE
            await update.message.reply_text(
                f"📋 *Summary*\n"
                f"📱 Mobile: `{state['mobile']}`\n"
                f"🔑 Password: `{'*'*len(pwd)}`\n"
                f"🎫 Platform: `{platform.upper()}`\n"
                f"🎫 Invite Code: `{invite}`\n\n"
                f"Confirm? (reply 'yes' or 'no')",
                parse_mode="Markdown"
            )
        elif state.get("step") == "confirm":
            if text.lower() in ["yes", "y"]:
                platform = state.get("platform")
                mobile = state["mobile"]
                otp = state["otp"]
                password = state["password"]
                invite = HOLWIN_INVITE if platform == "holwin" else REX_INVITE
                success, resp = await self.hw.register(platform, mobile, otp, password, invite)
                if success:
                    await self.crud.hw_update_user(user_id, platform, mobile, password, invite)
                    await update.message.reply_text("✅ *Registration successful!*", parse_mode="Markdown")
                else:
                    await update.message.reply_text(f"❌ Registration failed: {resp.get('msg', 'Unknown error')}")
                context.user_data.pop("hw_state")
            else:
                await update.message.reply_text("❌ Cancelled.")
                context.user_data.pop("hw_state")
        elif state.get("step") == "bet":
            try:
                amount = float(text)
                if amount <= 0:
                    raise ValueError
            except:
                await update.message.reply_text("❌ Invalid amount.")
                return
            game = state.get("game")
            user = await self.crud.hw_get_user(user_id)
            if not user:
                await update.message.reply_text("User not found.")
                return
            balance = user[6]
            new_balance, result = self.hw.play_game(game, amount, balance)
            if new_balance is None:
                await update.message.reply_text(f"❌ {result}")
                return
            await self.crud.hw_update_balance(user_id, new_balance - balance)
            await self.crud.hw_add_transaction(user_id, game, new_balance - balance, f"Game: {game}")
            await update.message.reply_text(f"🎮 *{game.capitalize()}*\n{result}\nNew balance: ₹{new_balance:.2f}", parse_mode="Markdown")
            context.user_data.pop("hw_state")
        else:
            await update.message.reply_text("Unknown HW state.")

    async def _handle_wb_text(self, update, context):
        state = context.user_data["wb_state"]
        text = update.message.text
        user_id = update.effective_user.id

        if state.get("waiting_for_number"):
            ok, msg = await self.crud.wb_add_number(user_id, text)
            await update.message.reply_text(f"{'✅' if ok else '❌'} {msg}")
            context.user_data.pop("wb_state")
        elif state.get("waiting_for_mass_count"):
            try:
                count = int(text)
                if count < 1:
                    raise ValueError
            except:
                await update.message.reply_text("❌ Invalid number.")
                return
            user = await self.crud.wb_get_user(user_id)
            if not user or user[7] == 1:
                await update.message.reply_text("⛔ Banned or not found.")
                return
            if user[6] == 0:
                await update.message.reply_text("❌ Email invalid.")
                return
            if not user[2] or not user[3]:
                await update.message.reply_text("❌ Email/password not set.")
                return
            numbers = await self.crud.wb_get_numbers(user_id)
            if not numbers:
                await update.message.reply_text("📭 No numbers.")
                return
            name = user[1] or "User"
            reason = user[4] or "personal communication"
            total = 0
            for n in numbers:
                if n[4] == 1:
                    continue
                custom = n[5]
                for _ in range(count):
                    ok, msg = await self.wb.send_appeal_email(user_id, n[0], name, reason, custom)
                    if ok:
                        await self.crud.wb_update_last_appeal(n[0])
                    await update.message.reply_text(f"{'✅' if ok else '❌'} {n[0]}: {msg}")
                    await asyncio.sleep(user[5] if user[5] else WB_DEFAULT_DELAY)
                    total += 1
            await update.message.reply_text(f"✅ Mass appeal complete: {total} emails sent.")
            context.user_data.pop("wb_state")
        elif state.get("waiting_for_email"):
            if not re.match(r"^[^@]+@[^@]+\.[^@]+$", text):
                await update.message.reply_text("❌ Invalid email format.")
                return
            await self.crud.wb_update_user(user_id, email=text, email_valid=1)
            await update.message.reply_text(f"✅ Email set to {text}")
            context.user_data.pop("wb_state")
        elif state.get("waiting_for_password"):
            if len(text) < 8:
                await update.message.reply_text("❌ Min 8 characters.")
                return
            await self.crud.wb_update_user(user_id, password=text, email_valid=1)
            await update.message.reply_text("✅ Password set.")
            context.user_data.pop("wb_state")
        elif state.get("waiting_for_reason"):
            await self.crud.wb_update_user(user_id, reason=text)
            await update.message.reply_text(f"✅ Reason set: {text}")
            context.user_data.pop("wb_state")
        elif state.get("waiting_for_delay"):
            try:
                delay = float(text)
                if delay < 0.5:
                    await update.message.reply_text("❌ Minimum 0.5 seconds.")
                    return
                await self.crud.wb_update_user(user_id, delay=delay)
                await update.message.reply_text(f"✅ Delay set to {delay}s")
            except:
                await update.message.reply_text("❌ Invalid number.")
            context.user_data.pop("wb_state")
        elif state.get("waiting_for_template"):
            template = text.strip()
            if not template:
                await update.message.reply_text("❌ Template cannot be empty.")
                return
            await self.crud.wb_add_template(user_id, template)
            await update.message.reply_text("✅ Template added.")
            context.user_data.pop("wb_state")
        elif state.get("waiting_for_del_template"):
            try:
                template_id = int(text)
                if await self.crud.wb_delete_template(user_id, template_id):
                    await update.message.reply_text("✅ Template deleted.")
                else:
                    await update.message.reply_text("❌ Not found or default.")
            except:
                await update.message.reply_text("❌ Invalid ID.")
            context.user_data.pop("wb_state")
        elif state.get("waiting_for_scheduler"):
            expr = text.strip()
            try:
                if croniter.is_valid(expr):
                    cron_expr = expr
                    interval = None
                else:
                    interval = int(expr)
                    cron_expr = None
                    if interval < 1:
                        raise ValueError
            except:
                await update.message.reply_text("❌ Invalid cron expression or minutes.")
                return
            job_id = await self.crud.wb_create_scheduler_job(user_id, cron_expr, interval)
            if job_id:
                if cron_expr:
                    trigger = CronTrigger.from_crontab(cron_expr)
                else:
                    trigger = IntervalTrigger(minutes=interval)
                async def job_func():
                    await self.wb.start_auto(user_id)
                    next_run = croniter(cron_expr, datetime.utcnow()).get_next(datetime) if cron_expr else datetime.utcnow() + timedelta(minutes=interval)
                    await self.crud.wb_update_scheduler_job(job_id, next_run)
                scheduler.add_job(job_func, trigger=trigger, id=f"wb_job_{job_id}", replace_existing=True)
                await update.message.reply_text("✅ Scheduler job created.")
            else:
                await update.message.reply_text("❌ Failed to create scheduler job.")
            context.user_data.pop("wb_state")
        elif state.get("waiting_for_number_reason"):
            phone = state["waiting_for_number_reason"]
            reason = text.strip()
            if reason == "-":
                reason = None
            await self.crud.db.execute("UPDATE wb_numbers SET custom_reason = ? WHERE phone = ?", (reason, phone))
            await update.message.reply_text(f"✅ Custom reason set for {phone}")
            context.user_data.pop("wb_state")
        else:
            await update.message.reply_text("Unknown WB state.")

# ---------- Scheduler ----------
scheduler = AsyncIOScheduler()

# ---------- Main ----------
async def main():
    db = Database("mega_bot.db")
    await db.init_tables()
    crud = CRUD(db)

    em = EMEngine(crud)
    hw = HWEngine(crud)
    wb = WBEngine(crud)

    cmd_handlers = CommandHandlers(crud, em, hw, wb)
    cb_handlers = CallbackHandlers(crud, em, hw, wb)
    msg_handlers = MessageHandlers(crud, em, hw, wb)

    app = Application.builder().token(BOT_TOKEN).build()

    global bot
    bot = app.bot

    app.add_handler(CommandHandler("start", cmd_handlers.start))
    app.add_handler(CommandHandler("help", cmd_handlers.help))
    app.add_handler(CommandHandler("admin", cmd_handlers.admin))
    app.add_handler(CommandHandler("stats", cmd_handlers.stats_global))
    app.add_handler(CommandHandler("approve", cmd_handlers.approve))
    app.add_handler(CommandHandler("reject", cmd_handlers.reject))
    app.add_handler(CommandHandler("whitelist", cmd_handlers.whitelist))
    app.add_handler(CommandHandler("remove", cmd_handlers.remove_whitelist))
    app.add_handler(CommandHandler("backup", cmd_handlers.backup))

    app.add_handler(CallbackQueryHandler(cb_handlers.handle))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msg_handlers.handle_text))
    app.add_handler(MessageHandler(filters.Document.ALL, msg_handlers.handle_text))

    scheduler.start()

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    logger.info("Bot started.")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await app.stop()
        await app.shutdown()

if __name__ == "__main__":
    asyncio.run(main())

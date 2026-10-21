"""
Asset generation script for Python Practical Lab
Generates publication-grade light-theme SVG vector graphics and renders PNGs via Chrome headless.
"""
import os
import subprocess
import time
from pathlib import Path

BASE_DIR = Path(r"d:\intership\python\vj")
ASSETS_DIR = BASE_DIR / "docs" / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# ==============================================================================
# 1. HERO BANNER (1200 x 500)
# ==============================================================================
hero_banner_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 500" width="1200" height="500">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FAF9F6"/>
      <stop offset="100%" stop-color="#F3F0E6"/>
    </linearGradient>
    <pattern id="dotPattern" x="0" y="0" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="3" cy="3" r="1.5" fill="#D8D5CC" opacity="0.45"/>
    </pattern>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#1E1B4B" flood-opacity="0.06"/>
      <feDropShadow dx="0" dy="1" stdDeviation="2" flood-color="#1E1B4B" flood-opacity="0.04"/>
    </filter>
  </defs>

  <rect width="1200" height="500" fill="url(#bgGrad)"/>
  <rect width="1200" height="500" fill="url(#dotPattern)"/>
  <rect x="1" y="1" width="1198" height="498" rx="16" fill="none" stroke="#D8D5CC" stroke-width="2"/>

  <!-- Top Badge -->
  <g transform="translate(60, 42)">
    <rect width="370" height="34" rx="17" fill="#FDF1EE" stroke="#F5C4BA" stroke-width="1"/>
    <circle cx="18" cy="17" r="5" fill="#E05C43"/>
    <text x="32" y="22" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#E05C43" letter-spacing="1.2">PYTHON PRACTICAL LAB • 4 STANDALONE APPS</text>
  </g>

  <!-- Title & Subtitle -->
  <text x="60" y="125" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="44" font-weight="800" fill="#1E1B4B" letter-spacing="-0.5">Python Practical Lab</text>
  <text x="60" y="158" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="400" fill="#475569">Engineering Suite Exploring Game Logic, Portfolio Analysis, Filesystem Automation, and Chatbots</text>

  <!-- 4 Application Cards Grid -->
  <!-- Card 1 -->
  <g transform="translate(60, 195)" filter="url(#cardShadow)">
    <rect width="252" height="180" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="0" y="0" width="252" height="6" rx="3" fill="#E05C43"/>
    <circle cx="36" cy="40" r="18" fill="#FDF1EE"/>
    <text x="36" y="46" font-size="18" text-anchor="middle">🎯</text>
    <text x="64" y="38" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#E05C43" letter-spacing="0.5">TASK 01</text>
    <text x="64" y="54" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="700" fill="#1E1B4B">Hangman Challenge</text>
    <text x="20" y="88" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">7-stage ASCII gallows engine,</text>
    <text x="20" y="106" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">9,894-word Google dataset &amp;</text>
    <text x="20" y="124" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">stateful replay loop.</text>
    <rect x="20" y="142" width="60" height="22" rx="4" fill="#F1F5F9"/>
    <text x="50" y="157" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="600" fill="#475569" text-anchor="middle">random</text>
    <rect x="88" y="142" width="60" height="22" rx="4" fill="#F1F5F9"/>
    <text x="118" y="157" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="600" fill="#475569" text-anchor="middle">pathlib</text>
  </g>

  <!-- Card 2 -->
  <g transform="translate(336, 195)" filter="url(#cardShadow)">
    <rect width="252" height="180" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="0" y="0" width="252" height="6" rx="3" fill="#10B981"/>
    <circle cx="36" cy="40" r="18" fill="#ECFDF5"/>
    <text x="36" y="46" font-size="18" text-anchor="middle">📈</text>
    <text x="64" y="38" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#10B981" letter-spacing="0.5">TASK 02</text>
    <text x="64" y="54" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="700" fill="#1E1B4B">Portfolio Journal</text>
    <text x="20" y="88" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">S&amp;P 500 stock tracker with</text>
    <text x="20" y="106" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">real-time P&amp;L analysis, ticker</text>
    <text x="20" y="124" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">validation &amp; CSV export.</text>
    <rect x="20" y="142" width="50" height="22" rx="4" fill="#F1F5F9"/>
    <text x="45" y="157" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="600" fill="#475569" text-anchor="middle">csv</text>
    <rect x="78" y="142" width="55" height="22" rx="4" fill="#F1F5F9"/>
    <text x="105" y="157" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="600" fill="#475569" text-anchor="middle">math</text>
  </g>

  <!-- Card 3 -->
  <g transform="translate(612, 195)" filter="url(#cardShadow)">
    <rect width="252" height="180" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="0" y="0" width="252" height="6" rx="3" fill="#2563EB"/>
    <circle cx="36" cy="40" r="18" fill="#EFF6FF"/>
    <text x="36" y="46" font-size="18" text-anchor="middle">🗂️</text>
    <text x="64" y="38" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#2563EB" letter-spacing="0.5">TASK 03</text>
    <text x="64" y="54" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="700" fill="#1E1B4B">Desktop File Sorter</text>
    <text x="20" y="88" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Safe file organizer with</text>
    <text x="20" y="106" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">dry-run preview, collision-free</text>
    <text x="20" y="124" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">renaming &amp; audit logging.</text>
    <rect x="20" y="142" width="50" height="22" rx="4" fill="#F1F5F9"/>
    <text x="45" y="157" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="600" fill="#475569" text-anchor="middle">shutil</text>
    <rect x="78" y="142" width="60" height="22" rx="4" fill="#F1F5F9"/>
    <text x="108" y="157" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="600" fill="#475569" text-anchor="middle">logging</text>
  </g>

  <!-- Card 4 -->
  <g transform="translate(888, 195)" filter="url(#cardShadow)">
    <rect width="252" height="180" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="0" y="0" width="252" height="6" rx="3" fill="#8B5CF6"/>
    <circle cx="36" cy="40" r="18" fill="#F5F3FF"/>
    <text x="36" y="46" font-size="18" text-anchor="middle">🤖</text>
    <text x="64" y="38" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#8B5CF6" letter-spacing="0.5">TASK 04</text>
    <text x="64" y="54" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="700" fill="#1E1B4B">FAQ Assistant</text>
    <text x="20" y="88" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Rule-based chatbot with</text>
    <text x="20" y="106" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">intent detection, keyword</text>
    <text x="20" y="124" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">scoring &amp; fallback handling.</text>
    <rect x="20" y="142" width="50" height="22" rx="4" fill="#F1F5F9"/>
    <text x="45" y="157" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="600" fill="#475569" text-anchor="middle">json</text>
    <rect x="78" y="142" width="40" height="22" rx="4" fill="#F1F5F9"/>
    <text x="98" y="157" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="600" fill="#475569" text-anchor="middle">re</text>
  </g>

  <!-- Bottom Metric Bar -->
  <g transform="translate(60, 410)">
    <rect width="1080" height="52" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
    
    <g transform="translate(35, 16)">
      <circle cx="8" cy="10" r="4" fill="#10B981"/>
      <text x="22" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="600" fill="#1E1B4B">100% Python Standard Library</text>
    </g>

    <line x1="285" y1="12" x2="285" y2="40" stroke="#E2E8F0" stroke-width="1"/>

    <g transform="translate(315, 16)">
      <circle cx="8" cy="10" r="4" fill="#2563EB"/>
      <text x="22" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="600" fill="#1E1B4B">100+ Automated Unit Tests</text>
    </g>

    <line x1="565" y1="12" x2="565" y2="40" stroke="#E2E8F0" stroke-width="1"/>

    <g transform="translate(595, 16)">
      <circle cx="8" cy="10" r="4" fill="#E05C43"/>
      <text x="22" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="600" fill="#1E1B4B">Terminal CLI + Web Showcase</text>
    </g>

    <line x1="865" y1="12" x2="865" y2="40" stroke="#E2E8F0" stroke-width="1"/>

    <g transform="translate(895, 16)">
      <circle cx="8" cy="10" r="4" fill="#8B5CF6"/>
      <text x="22" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="600" fill="#1E1B4B">Validated Real Datasets</text>
    </g>
  </g>
</svg>
"""

# ==============================================================================
# 2. ARCHITECTURE DIAGRAM (1200 x 480)
# ==============================================================================
architecture_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 480" width="1200" height="480">
  <defs>
    <linearGradient id="archBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FAF9F6"/>
      <stop offset="100%" stop-color="#F2EFE8"/>
    </linearGradient>
    <filter id="boxShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#1E1B4B" flood-opacity="0.05"/>
    </filter>
  </defs>

  <rect width="1200" height="480" fill="url(#archBg)"/>
  <rect x="1" y="1" width="1198" height="478" rx="16" fill="none" stroke="#D8D5CC" stroke-width="2"/>

  <!-- Header -->
  <g transform="translate(60, 36)">
    <rect width="270" height="28" rx="14" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="1"/>
    <text x="20" y="18" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#2563EB" letter-spacing="1">SYSTEM ARCHITECTURE &amp; DATA FLOW</text>
    <text x="0" y="58" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="28" font-weight="800" fill="#1E1B4B">Multi-Tier Modular Engineering Pipeline</text>
    <text x="0" y="82" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#64748B">Decoupled execution engines, defensive runtime protections, and automated test verification</text>
  </g>

  <!-- Flow Columns (4 Layers) -->

  <!-- Layer 1: Presentation Layer -->
  <g transform="translate(60, 145)" filter="url(#boxShadow)">
    <rect width="245" height="290" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="0" y="0" width="245" height="40" rx="12" fill="#F8FAFC"/>
    <rect x="0" y="30" width="245" height="10" fill="#F8FAFC"/>
    <text x="20" y="26" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#1E1B4B">1. PRESENTATION LAYER</text>

    <!-- Sub-blocks -->
    <rect x="16" y="55" width="213" height="75" rx="8" fill="#FDF1EE" stroke="#F5C4BA" stroke-width="1"/>
    <text x="30" y="78" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#E05C43">🖥️ Terminal CLI Engines</text>
    <text x="30" y="98" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" fill="#64748B">Pure Python standard I/O</text>
    <text x="30" y="114" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" fill="#64748B">ASCII art, flags (--dry-run)</text>

    <rect x="16" y="145" width="213" height="75" rx="8" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
    <text x="30" y="168" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#16A34A">🌐 Web Portal &amp; Showcases</text>
    <text x="30" y="188" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" fill="#64748B">index.html + vanilla JS widgets</text>
    <text x="30" y="204" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" fill="#64748B">Editorial light theme styling</text>

    <rect x="16" y="235" width="213" height="40" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
    <text x="30" y="260" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="600" fill="#475569">0 ms compilation runtime</text>
  </g>

  <!-- Arrow 1 to 2 -->
  <g transform="translate(315, 280)">
    <line x1="0" y1="0" x2="20" y2="0" stroke="#CBD5E1" stroke-width="2" stroke-dasharray="4"/>
    <polygon points="20,-4 28,0 20,4" fill="#94A3B8"/>
  </g>

  <!-- Layer 2: Core Applications -->
  <g transform="translate(350, 145)" filter="url(#boxShadow)">
    <rect width="255" height="290" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="0" y="0" width="255" height="40" rx="12" fill="#F8FAFC"/>
    <rect x="0" y="30" width="255" height="10" fill="#F8FAFC"/>
    <text x="20" y="26" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#1E1B4B">2. CORE APPLICATION LOGIC</text>

    <g transform="translate(16, 55)">
      <rect width="223" height="48" rx="6" fill="#FAF9F6" stroke="#E2E8F0" stroke-width="1"/>
      <text x="14" y="22" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#1E1B4B">🎯 word_challenge/game.py</text>
      <text x="14" y="38" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" fill="#64748B">Gallows state machine &amp; word guessing</text>
    </g>

    <g transform="translate(16, 112)">
      <rect width="223" height="48" rx="6" fill="#FAF9F6" stroke="#E2E8F0" stroke-width="1"/>
      <text x="14" y="22" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#1E1B4B">📈 market_journal/tracker.py</text>
      <text x="14" y="38" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" fill="#64748B">S&amp;P 500 lookup, P&amp;L math, ledger logic</text>
    </g>

    <g transform="translate(16, 169)">
      <rect width="223" height="48" rx="6" fill="#FAF9F6" stroke="#E2E8F0" stroke-width="1"/>
      <text x="14" y="22" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#1E1B4B">🗂️ desktop_sorter/sorter.py</text>
      <text x="14" y="38" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" fill="#64748B">Classifier engine &amp; collision resolver</text>
    </g>

    <g transform="translate(16, 226)">
      <rect width="223" height="48" rx="6" fill="#FAF9F6" stroke="#E2E8F0" stroke-width="1"/>
      <text x="14" y="22" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#1E1B4B">🤖 faq_assistant/assistant.py</text>
      <text x="14" y="38" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" fill="#64748B">Tokenization &amp; intent scoring</text>
    </g>
  </g>

  <!-- Arrow 2 to 3 -->
  <g transform="translate(615, 280)">
    <line x1="0" y1="0" x2="20" y2="0" stroke="#CBD5E1" stroke-width="2" stroke-dasharray="4"/>
    <polygon points="20,-4 28,0 20,4" fill="#94A3B8"/>
  </g>

  <!-- Layer 3: Defensive Safety & Runtime -->
  <g transform="translate(645, 145)" filter="url(#boxShadow)">
    <rect width="245" height="290" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="0" y="0" width="245" height="40" rx="12" fill="#F8FAFC"/>
    <rect x="0" y="30" width="245" height="10" fill="#F8FAFC"/>
    <text x="20" y="26" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#1E1B4B">3. DEFENSIVE SAFETY</text>

    <rect x="16" y="55" width="213" height="45" rx="6" fill="#FFFBEB" stroke="#FDE68A" stroke-width="1"/>
    <text x="26" y="74" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#B45309">🛡️ Dry-Run Simulation</text>
    <text x="26" y="90" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" fill="#78350F">Pre-validates moves before touching disk</text>

    <rect x="16" y="110" width="213" height="45" rx="6" fill="#FFFBEB" stroke="#FDE68A" stroke-width="1"/>
    <text x="26" y="129" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#B45309">🔄 Zero Overwrite Resolver</text>
    <text x="26" y="145" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" fill="#78350F">Automatic duplicate renaming pattern</text>

    <rect x="16" y="165" width="213" height="45" rx="6" fill="#FFFBEB" stroke="#FDE68A" stroke-width="1"/>
    <text x="26" y="184" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#B45309">🚫 Path &amp; Input Guardrails</text>
    <text x="26" y="200" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" fill="#78350F">Blocks root, OS files, invalid inputs</text>

    <rect x="16" y="220" width="213" height="45" rx="6" fill="#FFFBEB" stroke="#FDE68A" stroke-width="1"/>
    <text x="26" y="239" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#B45309">💬 NLP Fallback Engine</text>
    <text x="26" y="255" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" fill="#78350F">Graceful recovery for unknown queries</text>

    <rect x="16" y="272" width="213" height="50" rx="6" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
    <text x="26" y="292" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" font-weight="600" fill="#475569">Audit Logs: desktop_sorter/logs/</text>
    <text x="26" y="308" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" fill="#64748B">Timestamped tracking for every action</text>
  </g>

  <!-- Arrow 3 to 4 -->
  <g transform="translate(900, 280)">
    <line x1="0" y1="0" x2="20" y2="0" stroke="#CBD5E1" stroke-width="2" stroke-dasharray="4"/>
    <polygon points="20,-4 28,0 20,4" fill="#94A3B8"/>
  </g>

  <!-- Layer 4: Data & Verification -->
  <g transform="translate(930, 145)" filter="url(#boxShadow)">
    <rect width="210" height="290" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="0" y="0" width="210" height="40" rx="12" fill="#F8FAFC"/>
    <rect x="0" y="30" width="210" height="10" fill="#F8FAFC"/>
    <text x="18" y="26" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#1E1B4B">4. DATA &amp; TESTS</text>

    <g transform="translate(14, 55)">
      <rect width="182" height="60" rx="6" fill="#F5F3FF" stroke="#DDD6FE" stroke-width="1"/>
      <text x="12" y="20" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#7C3AED">📂 Verified Datasets</text>
      <text x="12" y="36" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" fill="#64748B">• Google 10k English Words</text>
      <text x="12" y="50" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" fill="#64748B">• S&amp;P 500 Constituents CSV</text>
    </g>

    <g transform="translate(14, 125)">
      <rect width="182" height="45" rx="6" fill="#F5F3FF" stroke="#DDD6FE" stroke-width="1"/>
      <text x="12" y="20" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#7C3AED">📄 JSON Knowledge Base</text>
      <text x="12" y="36" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" fill="#64748B">• sample_faq.json (Datheon)</text>
    </g>

    <g transform="translate(14, 180)">
      <rect width="182" height="95" rx="6" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1"/>
      <text x="12" y="22" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#047857">🧪 unittest Test Suite</text>
      <text x="12" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" fill="#065F46">• 100+ tests passing</text>
      <text x="12" y="56" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" fill="#065F46">• Edge-case coverage</text>
      <text x="12" y="72" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" fill="#065F46">• Boundary condition tests</text>
      <text x="12" y="88" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" font-weight="700" fill="#047857">STATUS: ALL PASSING</text>
    </g>
  </g>
</svg>
"""

# ==============================================================================
# 3. APP 1 SHOWCASE: HANGMAN (1100 x 420)
# ==============================================================================
app1_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 420" width="1100" height="420">
  <defs>
    <filter id="shadow1" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="5" stdDeviation="8" flood-color="#1E1B4B" flood-opacity="0.06"/>
    </filter>
  </defs>

  <rect width="1100" height="420" rx="14" fill="#FAF9F6" stroke="#D8D5CC" stroke-width="1.5"/>

  <!-- Left: Monospace Terminal Window -->
  <g transform="translate(45, 40)" filter="url(#shadow1)">
    <rect width="470" height="340" rx="10" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
    <rect width="470" height="36" rx="10" fill="#F1F5F9"/>
    <rect y="26" width="470" height="10" fill="#F1F5F9"/>
    <circle cx="20" cy="18" r="5" fill="#EF4444"/>
    <circle cx="36" cy="18" r="5" fill="#F59E0B"/>
    <circle cx="52" cy="18" r="5" fill="#10B981"/>
    <text x="235" y="22" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" fill="#64748B" text-anchor="middle">terminal — word_challenge/game.py</text>

    <!-- Terminal Content -->
    <g transform="translate(30, 60)" font-family="'JetBrains Mono', Consolas, monospace" font-size="13" fill="#1E1B4B">
      <text x="0" y="20" fill="#94A3B8">  +---+</text>
      <text x="0" y="40" fill="#94A3B8">  |   |</text>
      <text x="0" y="60" fill="#E05C43" font-weight="700">  O   |</text>
      <text x="0" y="80" fill="#E05C43" font-weight="700"> /|\  |</text>
      <text x="0" y="100" fill="#E05C43" font-weight="700"> /    |</text>
      <text x="0" y="120" fill="#94A3B8">========</text>

      <g transform="translate(170, 20)">
        <text x="0" y="10" font-size="11" fill="#64748B">WORD CATEGORY: GENERAL</text>
        <text x="0" y="40" font-size="18" font-weight="700" fill="#1E1B4B" letter-spacing="4">P Y T H _ N</text>
        <text x="0" y="70" font-size="12" fill="#64748B">Guessed letters:</text>
        <text x="0" y="90" font-size="13" font-weight="700" fill="#E05C43">[A, E, I, S, T]</text>
        <text x="0" y="115" font-size="12" fill="#64748B">Lives Remaining: <tspan fill="#E05C43" font-weight="700">2 / 6</tspan></text>
      </g>

      <line x1="0" y1="150" x2="410" y2="150" stroke="#E2E8F0" stroke-width="1"/>

      <text x="0" y="180" fill="#047857" font-weight="700">&gt; Guess a letter: o</text>
      <text x="0" y="205" fill="#2563EB">Good job! 'O' is in the word.</text>
      <text x="0" y="235" font-size="16" font-weight="800" fill="#16A34A" letter-spacing="4">P Y T H O N</text>
      <text x="0" y="258" fill="#10B981" font-weight="700">🎉 VICTORY! You guessed the word!</text>
    </g>
  </g>

  <!-- Right: Feature Breakdown -->
  <g transform="translate(560, 45)">
    <rect width="180" height="26" rx="13" fill="#FDF1EE" stroke="#F5C4BA" stroke-width="1"/>
    <text x="14" y="17" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#E05C43" letter-spacing="1">TASK 01 SHOWCASE</text>

    <text x="0" y="60" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="26" font-weight="800" fill="#1E1B4B">Hangman Word Challenge</text>
    <text x="0" y="85" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#475569">A robust terminal word-guessing game with dynamic ASCII gallows art</text>

    <!-- Key Capabilities List -->
    <g transform="translate(0, 115)">
      <!-- Item 1 -->
      <circle cx="12" cy="12" r="10" fill="#FDF1EE"/>
      <text x="12" y="16" font-size="12" text-anchor="middle" fill="#E05C43">✓</text>
      <text x="32" y="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#1E1B4B">9,894-Word Curated Dataset</text>
      <text x="32" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Sourced from Google 10k English with length filtering &amp; normalization</text>

      <!-- Item 2 -->
      <g transform="translate(0, 48)">
        <circle cx="12" cy="12" r="10" fill="#FDF1EE"/>
        <text x="12" y="16" font-size="12" text-anchor="middle" fill="#E05C43">✓</text>
        <text x="32" y="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#1E1B4B">Defensive Input Validation</text>
        <text x="32" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Rejects multi-character strings, digits, symbols &amp; duplicate attempts</text>
      </g>

      <!-- Item 3 -->
      <g transform="translate(0, 96)">
        <circle cx="12" cy="12" r="10" fill="#FDF1EE"/>
        <text x="12" y="16" font-size="12" text-anchor="middle" fill="#E05C43">✓</text>
        <text x="32" y="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#1E1B4B">Dual CLI &amp; In-Browser Web Showcase</text>
        <text x="32" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Run via python in terminal or test live in browser with virtual keyboard</text>
      </g>

      <!-- Item 4 -->
      <g transform="translate(0, 144)">
        <circle cx="12" cy="12" r="10" fill="#FDF1EE"/>
        <text x="12" y="16" font-size="12" text-anchor="middle" fill="#E05C43">✓</text>
        <text x="32" y="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#1E1B4B">Full Test Suite Verification</text>
        <text x="32" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Exhaustive unittest coverage for state transitions, gallows progression &amp; win/loss</text>
      </g>
    </g>

    <!-- Tech tags -->
    <g transform="translate(0, 305)">
      <rect width="65" height="24" rx="4" fill="#F1F5F9"/>
      <text x="32" y="16" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="#475569" text-anchor="middle">random</text>

      <rect x="75" width="65" height="24" rx="4" fill="#F1F5F9"/>
      <text x="107" y="16" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="#475569" text-anchor="middle">pathlib</text>

      <rect x="150" width="75" height="24" rx="4" fill="#F1F5F9"/>
      <text x="187" y="16" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="#475569" text-anchor="middle">unittest</text>

      <rect x="235" width="130" height="24" rx="4" fill="#FDF1EE" stroke="#F5C4BA" stroke-width="1"/>
      <text x="300" y="16" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#E05C43" text-anchor="middle">Standard Library Only</text>
    </g>
  </g>
</svg>
"""

# ==============================================================================
# 4. APP 2 SHOWCASE: PORTFOLIO JOURNAL (1100 x 420)
# ==============================================================================
app2_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 420" width="1100" height="420">
  <defs>
    <filter id="shadow2" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="5" stdDeviation="8" flood-color="#1E1B4B" flood-opacity="0.06"/>
    </filter>
  </defs>

  <rect width="1100" height="420" rx="14" fill="#FAF9F6" stroke="#D8D5CC" stroke-width="1.5"/>

  <!-- Left: Financial Dashboard Card -->
  <g transform="translate(45, 40)" filter="url(#shadow2)">
    <rect width="470" height="340" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
    <rect width="470" height="42" rx="12" fill="#F8FAFC"/>
    <rect y="32" width="470" height="10" fill="#F8FAFC"/>
    <text x="24" y="26" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#1E1B4B">PORTFOLIO MARKET JOURNAL</text>
    <rect x="360" y="10" width="90" height="22" rx="11" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1"/>
    <text x="405" y="25" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">S&amp;P 500 VERIFIED</text>

    <!-- Balance Row -->
    <g transform="translate(24, 60)">
      <rect width="200" height="65" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
      <text x="14" y="24" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" fill="#64748B">TOTAL PORTFOLIO VALUE</text>
      <text x="14" y="50" font-family="'JetBrains Mono', Consolas, monospace" font-size="20" font-weight="800" fill="#1E1B4B">$14,340.50</text>

      <rect x="220" width="200" height="65" rx="8" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1"/>
      <text x="234" y="24" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" fill="#065F46">TOTAL UNREALIZED GAIN</text>
      <text x="234" y="50" font-family="'JetBrains Mono', Consolas, monospace" font-size="20" font-weight="800" fill="#047857">+$1,890.50 (+15.2%)</text>
    </g>

    <!-- Table Header -->
    <g transform="translate(24, 145)" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#64748B">
      <rect width="422" height="26" fill="#F1F5F9" rx="4"/>
      <text x="12" y="17">TICKER</text>
      <text x="100" y="17">SHARES</text>
      <text x="180" y="17">BUY PRICE</text>
      <text x="270" y="17">CURRENT</text>
      <text x="360" y="17">RETURN</text>
    </g>

    <!-- Row 1: AAPL -->
    <g transform="translate(24, 180)" font-family="'JetBrains Mono', Consolas, monospace" font-size="12">
      <text x="12" y="16" font-weight="700" fill="#1E1B4B">AAPL</text>
      <text x="100" y="16" fill="#475569">20</text>
      <text x="180" y="16" fill="#475569">$150.00</text>
      <text x="270" y="16" fill="#475569">$182.50</text>
      <text x="360" y="16" font-weight="700" fill="#047857">+21.67%</text>
      <line x1="0" y1="26" x2="422" y2="26" stroke="#F1F5F9" stroke-width="1"/>
    </g>

    <!-- Row 2: NVDA -->
    <g transform="translate(24, 215)" font-family="'JetBrains Mono', Consolas, monospace" font-size="12">
      <text x="12" y="16" font-weight="700" fill="#1E1B4B">NVDA</text>
      <text x="100" y="16" fill="#475569">15</text>
      <text x="180" y="16" fill="#475569">$420.00</text>
      <text x="270" y="16" fill="#475569">$495.00</text>
      <text x="360" y="16" font-weight="700" fill="#047857">+17.86%</text>
      <line x1="0" y1="26" x2="422" y2="26" stroke="#F1F5F9" stroke-width="1"/>
    </g>

    <!-- Row 3: MSFT -->
    <g transform="translate(24, 250)" font-family="'JetBrains Mono', Consolas, monospace" font-size="12">
      <text x="12" y="16" font-weight="700" fill="#1E1B4B">MSFT</text>
      <text x="100" y="16" fill="#475569">10</text>
      <text x="180" y="16" fill="#475569">$310.00</text>
      <text x="270" y="16" fill="#475569">$335.00</text>
      <text x="360" y="16" font-weight="700" fill="#047857">+8.06%</text>
    </g>

    <!-- Bottom Actions -->
    <g transform="translate(24, 290)">
      <rect width="130" height="28" rx="6" fill="#F1F5F9"/>
      <text x="65" y="18" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="600" fill="#475569" text-anchor="middle">📄 Export to CSV</text>

      <rect x="140" width="130" height="28" rx="6" fill="#F1F5F9"/>
      <text x="205" y="18" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="600" fill="#475569" text-anchor="middle">➕ Add Position</text>
    </g>
  </g>

  <!-- Right: Feature Breakdown -->
  <g transform="translate(560, 45)">
    <rect width="180" height="26" rx="13" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1"/>
    <text x="14" y="17" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#047857" letter-spacing="1">TASK 02 SHOWCASE</text>

    <text x="0" y="60" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="26" font-weight="800" fill="#1E1B4B">Portfolio Market Journal</text>
    <text x="0" y="85" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#475569">Stock tracking &amp; gain/loss analysis engine backed by S&amp;P 500 records</text>

    <!-- Key Capabilities List -->
    <g transform="translate(0, 115)">
      <!-- Item 1 -->
      <circle cx="12" cy="12" r="10" fill="#ECFDF5"/>
      <text x="12" y="16" font-size="12" text-anchor="middle" fill="#047857">✓</text>
      <text x="32" y="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#1E1B4B">S&amp;P 500 Constituent Validation</text>
      <text x="32" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Validates tickers against 503 official constituent companies from CSV</text>

      <!-- Item 2 -->
      <g transform="translate(0, 48)">
        <circle cx="12" cy="12" r="10" fill="#ECFDF5"/>
        <text x="12" y="16" font-size="12" text-anchor="middle" fill="#047857">✓</text>
        <text x="32" y="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#1E1B4B">Defensive Financial Math</text>
        <text x="32" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Guards against division-by-zero, negative prices, and invalid quantities</text>
      </g>

      <!-- Item 3 -->
      <g transform="translate(0, 96)">
        <circle cx="12" cy="12" r="10" fill="#ECFDF5"/>
        <text x="12" y="16" font-size="12" text-anchor="middle" fill="#047857">✓</text>
        <text x="32" y="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#1E1B4B">Dual Valuation Architecture</text>
        <text x="32" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Supports offline manual entry with extensible hooks for live web quotes</text>
      </g>

      <!-- Item 4 -->
      <g transform="translate(0, 144)">
        <circle cx="12" cy="12" r="10" fill="#ECFDF5"/>
        <text x="12" y="16" font-size="12" text-anchor="middle" fill="#047857">✓</text>
        <text x="32" y="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#1E1B4B">Automated CSV Reports</text>
        <text x="32" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Exports complete timestamped portfolio snapshots ready for spreadsheet analysis</text>
      </g>
    </g>

    <!-- Tech tags -->
    <g transform="translate(0, 305)">
      <rect width="45" height="24" rx="4" fill="#F1F5F9"/>
      <text x="22" y="16" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="#475569" text-anchor="middle">csv</text>

      <rect x="55" width="55" height="24" rx="4" fill="#F1F5F9"/>
      <text x="82" y="16" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="#475569" text-anchor="middle">math</text>

      <rect x="120" width="75" height="24" rx="4" fill="#F1F5F9"/>
      <text x="157" y="16" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="#475569" text-anchor="middle">datetime</text>

      <rect x="205" width="75" height="24" rx="4" fill="#F1F5F9"/>
      <text x="242" y="16" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="#475569" text-anchor="middle">unittest</text>

      <rect x="290" width="130" height="24" rx="4" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1"/>
      <text x="355" y="16" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#047857" text-anchor="middle">Standard Library Only</text>
    </g>
  </g>
</svg>
"""

# ==============================================================================
# 5. APP 3 SHOWCASE: DESKTOP SORTER (1100 x 420)
# ==============================================================================
app3_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 420" width="1100" height="420">
  <defs>
    <filter id="shadow3" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="5" stdDeviation="8" flood-color="#1E1B4B" flood-opacity="0.06"/>
    </filter>
  </defs>

  <rect width="1100" height="420" rx="14" fill="#FAF9F6" stroke="#D8D5CC" stroke-width="1.5"/>

  <!-- Left: Sorter Pipeline Simulation -->
  <g transform="translate(45, 40)" filter="url(#shadow3)">
    <rect width="470" height="340" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
    <rect width="470" height="42" rx="12" fill="#F8FAFC"/>
    <rect y="32" width="470" height="10" fill="#F8FAFC"/>
    <text x="24" y="26" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#1E1B4B">DESKTOP FILE SORTER PIPELINE</text>
    <rect x="340" y="10" width="110" height="22" rx="11" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="1"/>
    <text x="395" y="25" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" font-weight="700" fill="#2563EB" text-anchor="middle">DRY-RUN SAFE</text>

    <!-- Source Bucket -->
    <g transform="translate(24, 60)">
      <rect width="180" height="90" rx="8" fill="#FFFBEB" stroke="#FDE68A" stroke-width="1"/>
      <text x="14" y="22" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#B45309">📁 TARGET DIRECTORY</text>
      <text x="14" y="44" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" fill="#475569">annual_report.pdf</text>
      <text x="14" y="62" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" fill="#475569">app_icon.png</text>
      <text x="14" y="80" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" fill="#475569">dataset_2026.csv</text>
    </g>

    <!-- Arrow Classifier -->
    <g transform="translate(215, 105)">
      <circle cx="15" cy="0" r="14" fill="#2563EB"/>
      <text x="15" y="4" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF" text-anchor="middle">→</text>
    </g>

    <!-- Categorized Output Buckets -->
    <g transform="translate(255, 60)">
      <rect width="190" height="90" rx="8" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
      <text x="14" y="22" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#16A34A">🗂️ ORGANIZED CATEGORIES</text>
      <text x="14" y="44" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" fill="#166534">📂 Documents/ (.pdf)</text>
      <text x="14" y="62" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" fill="#166534">📂 Images/ (.png, .jpg)</text>
      <text x="14" y="80" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" fill="#166534">📂 Spreadsheets/ (.csv)</text>
    </g>

    <!-- Console Log Window -->
    <g transform="translate(24, 165)">
      <rect width="422" height="150" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
      <rect width="422" height="24" rx="8" fill="#F1F5F9"/>
      <rect y="16" width="422" height="8" fill="#F1F5F9"/>
      <text x="14" y="16" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="600" fill="#64748B">Audit Log Output — safe dry-run preview</text>

      <g transform="translate(14, 40)" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" fill="#1E1B4B">
        <text x="0" y="14" fill="#2563EB">[INFO] Scanning directory: ~/Downloads</text>
        <text x="0" y="32" fill="#475569">[PLAN] annual_report.pdf → Documents/</text>
        <text x="0" y="50" fill="#475569">[PLAN] app_icon.png → Images/</text>
        <text x="0" y="68" fill="#D97706">[COLLISION] report.pdf exists → renaming to report (1).pdf</text>
        <text x="0" y="86" fill="#16A34A" font-weight="700">[SAFE] 0 files moved. Run with --confirm to apply.</text>
      </g>
    </g>
  </g>

  <!-- Right: Feature Breakdown -->
  <g transform="translate(560, 45)">
    <rect width="180" height="26" rx="13" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="1"/>
    <text x="14" y="17" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#2563EB" letter-spacing="1">TASK 03 SHOWCASE</text>

    <text x="0" y="60" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="26" font-weight="800" fill="#1E1B4B">Desktop File Sorter</text>
    <text x="0" y="85" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#475569">Production-grade directory organizer engineered with strict safety guarantees</text>

    <!-- Key Capabilities List -->
    <g transform="translate(0, 115)">
      <!-- Item 1 -->
      <circle cx="12" cy="12" r="10" fill="#EFF6FF"/>
      <text x="12" y="16" font-size="12" text-anchor="middle" fill="#2563EB">✓</text>
      <text x="32" y="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#1E1B4B">Safe Dry-Run by Default</text>
      <text x="32" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Always previews proposed file relocations; requires explicit --confirm to execute</text>

      <!-- Item 2 -->
      <g transform="translate(0, 48)">
        <circle cx="12" cy="12" r="10" fill="#EFF6FF"/>
        <text x="12" y="16" font-size="12" text-anchor="middle" fill="#2563EB">✓</text>
        <text x="32" y="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#1E1B4B">Zero Overwrite Collision Resolution</text>
        <text x="32" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Never overwrites identical file names — automatically resolves to 'name (1).ext'</text>
      </g>

      <!-- Item 3 -->
      <g transform="translate(0, 96)">
        <circle cx="12" cy="12" r="10" fill="#EFF6FF"/>
        <text x="12" y="16" font-size="12" text-anchor="middle" fill="#2563EB">✓</text>
        <text x="32" y="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#1E1B4B">Filesystem Safety Boundaries</text>
        <text x="32" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Refuses root paths, system locations, symlinks, and self-script directories</text>
      </g>

      <!-- Item 4 -->
      <g transform="translate(0, 144)">
        <circle cx="12" cy="12" r="10" fill="#EFF6FF"/>
        <text x="12" y="16" font-size="12" text-anchor="middle" fill="#2563EB">✓</text>
        <text x="32" y="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#1E1B4B">Structured Audit Logging</text>
        <text x="32" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Generates permanent timestamped activity journals in desktop_sorter/logs/</text>
      </g>
    </g>

    <!-- Tech tags -->
    <g transform="translate(0, 305)">
      <rect width="40" height="24" rx="4" fill="#F1F5F9"/>
      <text x="20" y="16" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="#475569" text-anchor="middle">os</text>

      <rect x="50" width="55" height="24" rx="4" fill="#F1F5F9"/>
      <text x="77" y="16" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="#475569" text-anchor="middle">shutil</text>

      <rect x="115" width="65" height="24" rx="4" fill="#F1F5F9"/>
      <text x="147" y="16" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="#475569" text-anchor="middle">pathlib</text>

      <rect x="190" width="65" height="24" rx="4" fill="#F1F5F9"/>
      <text x="222" y="16" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="#475569" text-anchor="middle">logging</text>

      <rect x="265" width="130" height="24" rx="4" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="1"/>
      <text x="330" y="16" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#2563EB" text-anchor="middle">Standard Library Only</text>
    </g>
  </g>
</svg>
"""

# ==============================================================================
# 6. APP 4 SHOWCASE: FAQ ASSISTANT (1100 x 420)
# ==============================================================================
app4_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 420" width="1100" height="420">
  <defs>
    <filter id="shadow4" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="5" stdDeviation="8" flood-color="#1E1B4B" flood-opacity="0.06"/>
    </filter>
  </defs>

  <rect width="1100" height="420" rx="14" fill="#FAF9F6" stroke="#D8D5CC" stroke-width="1.5"/>

  <!-- Left: Conversational Chat UI -->
  <g transform="translate(45, 40)" filter="url(#shadow4)">
    <rect width="470" height="340" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
    <rect width="470" height="42" rx="12" fill="#F8FAFC"/>
    <rect y="32" width="470" height="10" fill="#F8FAFC"/>
    <circle cx="28" cy="21" r="7" fill="#10B981"/>
    <text x="44" y="26" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#1E1B4B">FAQ CONVERSATION ASSISTANT</text>
    <rect x="350" y="10" width="100" height="22" rx="11" fill="#F5F3FF" stroke="#DDD6FE" stroke-width="1"/>
    <text x="400" y="25" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" font-weight="700" fill="#7C3AED" text-anchor="middle">NLP PIPELINE</text>

    <!-- Chat Messages -->
    <g transform="translate(20, 58)">
      <!-- User Bubble 1 -->
      <g transform="translate(110, 0)">
        <rect width="320" height="44" rx="12" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="1"/>
        <text x="16" y="20" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="600" fill="#1E40AF">How do I submit my project assignment?</text>
        <text x="16" y="34" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" fill="#64748B">User Query • Intent: faq_submit</text>
      </g>

      <!-- Bot Bubble 1 -->
      <g transform="translate(0, 56)">
        <rect width="390" height="85" rx="12" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
        <!-- Intent badge -->
        <rect x="14" y="12" width="160" height="18" rx="4" fill="#F5F3FF" stroke="#DDD6FE" stroke-width="1"/>
        <text x="20" y="25" font-family="'JetBrains Mono', Consolas, monospace" font-size="9" font-weight="700" fill="#7C3AED">MATCH: SUBMIT_ASSIGNMENT (96%)</text>
        
        <text x="14" y="48" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" fill="#1E1B4B">Assignments must be submitted via the student portal before</text>
        <text x="14" y="64" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" fill="#1E1B4B">the deadline. Include all tests, source files, and report docs.</text>
        <text x="14" y="78" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="9" fill="#059669">✓ Sourced from Datheon sample_faq.json</text>
      </g>

      <!-- User Bubble 2 -->
      <g transform="translate(180, 153)">
        <rect width="250" height="34" rx="12" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="1"/>
        <text x="14" y="21" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="600" fill="#1E40AF">When will I get my certificate?</text>
      </g>

      <!-- Bot Bubble 2 -->
      <g transform="translate(0, 198)">
        <rect width="390" height="65" rx="12" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
        <rect x="14" y="10" width="150" height="18" rx="4" fill="#F5F3FF" stroke="#DDD6FE" stroke-width="1"/>
        <text x="20" y="23" font-family="'JetBrains Mono', Consolas, monospace" font-size="9" font-weight="700" fill="#7C3AED">MATCH: CERTIFICATE (92%)</text>
        <text x="14" y="44" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" fill="#1E1B4B">Certificates are dispatched within 5 to 7 business days</text>
        <text x="14" y="58" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" fill="#1E1B4B">following successful completion and mentor verification.</text>
      </g>
    </g>
  </g>

  <!-- Right: Feature Breakdown -->
  <g transform="translate(560, 45)">
    <rect width="180" height="26" rx="13" fill="#F5F3FF" stroke="#DDD6FE" stroke-width="1"/>
    <text x="14" y="17" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#7C3AED" letter-spacing="1">TASK 04 SHOWCASE</text>

    <text x="0" y="60" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="26" font-weight="800" fill="#1E1B4B">FAQ Conversation Assistant</text>
    <text x="0" y="85" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" fill="#475569">Rule-based conversational agent with multi-stage intent classification</text>

    <!-- Key Capabilities List -->
    <g transform="translate(0, 115)">
      <!-- Item 1 -->
      <circle cx="12" cy="12" r="10" fill="#F5F3FF"/>
      <text x="12" y="16" font-size="12" text-anchor="middle" fill="#7C3AED">✓</text>
      <text x="32" y="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#1E1B4B">NLP Preprocessing Pipeline</text>
      <text x="32" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">String normalization, punctuation cleansing, and English stopword extraction</text>

      <!-- Item 2 -->
      <g transform="translate(0, 48)">
        <circle cx="12" cy="12" r="10" fill="#F5F3FF"/>
        <text x="12" y="16" font-size="12" text-anchor="middle" fill="#7C3AED">✓</text>
        <text x="32" y="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#1E1B4B">Jaccard Keyword Scoring Engine</text>
        <text x="32" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Computes overlap token similarity against questions in sample_faq.json</text>
      </g>

      <!-- Item 3 -->
      <g transform="translate(0, 96)">
        <circle cx="12" cy="12" r="10" fill="#F5F3FF"/>
        <text x="12" y="16" font-size="12" text-anchor="middle" fill="#7C3AED">✓</text>
        <text x="32" y="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#1E1B4B">Graceful Ambiguity Fallback</text>
        <text x="32" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Never breaks on unrecognised input — offers clarifying suggestion topics</text>
      </g>

      <!-- Item 4 -->
      <g transform="translate(0, 144)">
        <circle cx="12" cy="12" r="10" fill="#F5F3FF"/>
        <text x="12" y="16" font-size="12" text-anchor="middle" fill="#7C3AED">✓</text>
        <text x="32" y="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#1E1B4B">Web Chat Simulator Included</text>
        <text x="32" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Interactive HTML interface in faq_assistant/index.html with clickable queries</text>
      </g>
    </g>

    <!-- Tech tags -->
    <g transform="translate(0, 305)">
      <rect width="45" height="24" rx="4" fill="#F1F5F9"/>
      <text x="22" y="16" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="#475569" text-anchor="middle">json</text>

      <rect x="55" width="35" height="24" rx="4" fill="#F1F5F9"/>
      <text x="72" y="16" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="#475569" text-anchor="middle">re</text>

      <rect x="100" width="85" height="24" rx="4" fill="#F1F5F9"/>
      <text x="142" y="16" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="#475569" text-anchor="middle">collections</text>

      <rect x="195" width="75" height="24" rx="4" fill="#F1F5F9"/>
      <text x="232" y="16" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="#475569" text-anchor="middle">unittest</text>

      <rect x="280" width="130" height="24" rx="4" fill="#F5F3FF" stroke="#DDD6FE" stroke-width="1"/>
      <text x="345" y="16" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#7C3AED" text-anchor="middle">Standard Library Only</text>
    </g>
  </g>
</svg>
"""

# ==============================================================================
# 7. LINKEDIN SHOWCASE & IMAGE.PNG (1200 x 675 — 16:9 Aspect Ratio)
# ==============================================================================
linkedin_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" width="1200" height="675">
  <defs>
    <linearGradient id="liBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FAF9F6"/>
      <stop offset="100%" stop-color="#F2EFE8"/>
    </linearGradient>
    <pattern id="liDots" x="0" y="0" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="3" cy="3" r="1.5" fill="#D8D5CC" opacity="0.45"/>
    </pattern>
    <filter id="liShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#1E1B4B" flood-opacity="0.07"/>
      <feDropShadow dx="0" dy="1" stdDeviation="2" flood-color="#1E1B4B" flood-opacity="0.04"/>
    </filter>
  </defs>

  <rect width="1200" height="675" fill="url(#liBg)"/>
  <rect width="1200" height="675" fill="url(#liDots)"/>
  <rect x="2" y="2" width="1196" height="671" rx="16" fill="none" stroke="#D8D5CC" stroke-width="2"/>

  <!-- Top Pill -->
  <g transform="translate(60, 36)">
    <rect width="390" height="32" rx="16" fill="#FDF1EE" stroke="#F5C4BA" stroke-width="1"/>
    <circle cx="16" cy="16" r="5" fill="#E05C43"/>
    <text x="30" y="21" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#E05C43" letter-spacing="1.2">PYTHON PROGRAMMING INTERNSHIP • DATHEON</text>
  </g>

  <!-- Title & Subtitle -->
  <g transform="translate(60, 88)">
    <text x="0" y="32" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="34" font-weight="800" fill="#1E1B4B" letter-spacing="-0.5">Python Practical Lab: 4 Modular Applications</text>
    <text x="0" y="58" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="400" fill="#475569">Engineered with 100% Python Standard Library • Zero 3rd-Party Dependencies • 100+ Tests Passing</text>
  </g>

  <!-- 4 Bento Grid Cards (2x2) -->
  
  <!-- Row 1, Col 1: Hangman -->
  <g transform="translate(60, 168)" filter="url(#liShadow)">
    <rect width="525" height="195" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="0" y="0" width="525" height="5" rx="2.5" fill="#E05C43"/>

    <!-- Header -->
    <circle cx="36" cy="38" r="16" fill="#FDF1EE"/>
    <text x="36" y="44" font-size="16" text-anchor="middle">🎯</text>
    <text x="64" y="34" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#E05C43">TASK 01</text>
    <text x="64" y="50" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="700" fill="#1E1B4B">Hangman Word Challenge</text>

    <!-- Mini visual -->
    <g transform="translate(24, 72)">
      <rect width="180" height="75" rx="6" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
      <text x="14" y="24" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" fill="#64748B">GALLOWS STATE: 4/6</text>
      <text x="14" y="46" font-family="'JetBrains Mono', Consolas, monospace" font-size="15" font-weight="700" fill="#E05C43" letter-spacing="3">P Y T H _ N</text>
      <text x="14" y="64" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" fill="#047857">GUESSES: [A, E, I, S]</text>
    </g>

    <!-- Details -->
    <g transform="translate(220, 75)" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#475569">
      <text x="0" y="14">• 9,894-word Google 10k English dataset</text>
      <text x="0" y="34">• 7-stage progressive ASCII gallows</text>
      <text x="0" y="54">• Defensive single-character input parser</text>
      <text x="0" y="74">• Stateful win/loss detection &amp; replay</text>
    </g>

    <!-- Tags -->
    <g transform="translate(24, 160)">
      <rect width="55" height="20" rx="4" fill="#F1F5F9"/>
      <text x="27" y="14" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="600" fill="#475569" text-anchor="middle">random</text>
      <rect x="62" width="55" height="20" rx="4" fill="#F1F5F9"/>
      <text x="89" y="14" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="600" fill="#475569" text-anchor="middle">pathlib</text>
      <rect x="124" width="105" height="20" rx="4" fill="#FDF1EE"/>
      <text x="176" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" font-weight="700" fill="#E05C43" text-anchor="middle">CLI + Web Portal</text>
    </g>
  </g>

  <!-- Row 1, Col 2: Portfolio Journal -->
  <g transform="translate(615, 168)" filter="url(#liShadow)">
    <rect width="525" height="195" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="0" y="0" width="525" height="5" rx="2.5" fill="#10B981"/>

    <!-- Header -->
    <circle cx="36" cy="38" r="16" fill="#ECFDF5"/>
    <text x="36" y="44" font-size="16" text-anchor="middle">📈</text>
    <text x="64" y="34" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#10B981">TASK 02</text>
    <text x="64" y="50" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="700" fill="#1E1B4B">Portfolio Market Journal</text>

    <!-- Mini visual -->
    <g transform="translate(24, 72)">
      <rect width="180" height="75" rx="6" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1"/>
      <text x="14" y="22" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" fill="#065F46">S&amp;P 500 CONSTITUENTS</text>
      <text x="14" y="44" font-family="'JetBrains Mono', Consolas, monospace" font-size="16" font-weight="800" fill="#047857">+$1,890.50</text>
      <text x="14" y="62" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="700" fill="#047857">+15.18% TOTAL GAIN</text>
    </g>

    <!-- Details -->
    <g transform="translate(220, 75)" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#475569">
      <text x="0" y="14">• Validated against 503 S&amp;P 500 tickers</text>
      <text x="0" y="34">• Accurate P&amp;L gain/loss calculations</text>
      <text x="0" y="54">• Defensive division-by-zero checks</text>
      <text x="0" y="74">• Automated timestamped CSV export</text>
    </g>

    <!-- Tags -->
    <g transform="translate(24, 160)">
      <rect width="45" height="20" rx="4" fill="#F1F5F9"/>
      <text x="22" y="14" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="600" fill="#475569" text-anchor="middle">csv</text>
      <rect x="52" width="45" height="20" rx="4" fill="#F1F5F9"/>
      <text x="74" y="14" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="600" fill="#475569" text-anchor="middle">math</text>
      <rect x="104" width="115" height="20" rx="4" fill="#ECFDF5"/>
      <text x="161" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">Financial Analytics</text>
    </g>
  </g>

  <!-- Row 2, Col 1: Desktop Sorter -->
  <g transform="translate(60, 385)" filter="url(#liShadow)">
    <rect width="525" height="195" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="0" y="0" width="525" height="5" rx="2.5" fill="#2563EB"/>

    <!-- Header -->
    <circle cx="36" cy="38" r="16" fill="#EFF6FF"/>
    <text x="36" y="44" font-size="16" text-anchor="middle">🗂️</text>
    <text x="64" y="34" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#2563EB">TASK 03</text>
    <text x="64" y="50" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="700" fill="#1E1B4B">Desktop File Sorter</text>

    <!-- Mini visual -->
    <g transform="translate(24, 72)">
      <rect width="180" height="75" rx="6" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="1"/>
      <text x="14" y="24" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="700" fill="#1E40AF">SAFE DRY-RUN SIMULATOR</text>
      <text x="14" y="44" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" fill="#1E40AF">→ Documents/ (PDF)</text>
      <text x="14" y="62" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" fill="#1E40AF">→ Images/ (PNG, JPG)</text>
    </g>

    <!-- Details -->
    <g transform="translate(220, 75)" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#475569">
      <text x="0" y="14">• Safe dry-run preview before execution</text>
      <text x="0" y="34">• Zero-overwrite collision resolution</text>
      <text x="0" y="54">• Filesystem root &amp; OS guardrails</text>
      <text x="0" y="74">• Timestamped audit logging trail</text>
    </g>

    <!-- Tags -->
    <g transform="translate(24, 160)">
      <rect width="45" height="20" rx="4" fill="#F1F5F9"/>
      <text x="22" y="14" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="600" fill="#475569" text-anchor="middle">shutil</text>
      <rect x="52" width="55" height="20" rx="4" fill="#F1F5F9"/>
      <text x="79" y="14" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="600" fill="#475569" text-anchor="middle">logging</text>
      <rect x="114" width="115" height="20" rx="4" fill="#EFF6FF"/>
      <text x="171" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" font-weight="700" fill="#2563EB" text-anchor="middle">Filesystem Automation</text>
    </g>
  </g>

  <!-- Row 2, Col 2: FAQ Assistant -->
  <g transform="translate(615, 385)" filter="url(#liShadow)">
    <rect width="525" height="195" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="0" y="0" width="525" height="5" rx="2.5" fill="#8B5CF6"/>

    <!-- Header -->
    <circle cx="36" cy="38" r="16" fill="#F5F3FF"/>
    <text x="36" y="44" font-size="16" text-anchor="middle">🤖</text>
    <text x="64" y="34" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#8B5CF6">TASK 04</text>
    <text x="64" y="50" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="700" fill="#1E1B4B">FAQ Conversation Assistant</text>

    <!-- Mini visual -->
    <g transform="translate(24, 72)">
      <rect width="180" height="75" rx="6" fill="#F5F3FF" stroke="#DDD6FE" stroke-width="1"/>
      <text x="14" y="24" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="700" fill="#6D28D9">INTENT: FAQ_MATCH</text>
      <text x="14" y="44" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" fill="#475569">Similarity: 0.96</text>
      <text x="14" y="62" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" fill="#047857">"Assignment submission..."</text>
    </g>

    <!-- Details -->
    <g transform="translate(220, 75)" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#475569">
      <text x="0" y="14">• Rule-based intent detection engine</text>
      <text x="0" y="34">• Text normalization &amp; stopword filter</text>
      <text x="0" y="54">• Jaccard multi-token keyword scoring</text>
      <text x="0" y="74">• Graceful ambiguous fallback questions</text>
    </g>

    <!-- Tags -->
    <g transform="translate(24, 160)">
      <rect width="45" height="20" rx="4" fill="#F1F5F9"/>
      <text x="22" y="14" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="600" fill="#475569" text-anchor="middle">json</text>
      <rect x="52" width="35" height="20" rx="4" fill="#F1F5F9"/>
      <text x="69" y="14" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="600" fill="#475569" text-anchor="middle">re</text>
      <rect x="94" width="115" height="20" rx="4" fill="#F5F3FF"/>
      <text x="151" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" font-weight="700" fill="#7C3AED" text-anchor="middle">NLP &amp; Conversational</text>
    </g>
  </g>

  <!-- Bottom Metric Strip & Author -->
  <g transform="translate(60, 600)">
    <rect width="1080" height="52" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>

    <g transform="translate(30, 16)">
      <circle cx="8" cy="10" r="4" fill="#10B981"/>
      <text x="20" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#1E1B4B">100% Python Standard Library</text>
    </g>

    <line x1="260" y1="12" x2="260" y2="40" stroke="#E2E8F0" stroke-width="1"/>

    <g transform="translate(285, 16)">
      <circle cx="8" cy="10" r="4" fill="#2563EB"/>
      <text x="20" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#1E1B4B">100+ Automated Unit Tests</text>
    </g>

    <line x1="515" y1="12" x2="515" y2="40" stroke="#E2E8F0" stroke-width="1"/>

    <g transform="translate(540, 16)">
      <circle cx="8" cy="10" r="4" fill="#E05C43"/>
      <text x="20" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#1E1B4B">Dual CLI &amp; Web Interfaces</text>
    </g>

    <line x1="770" y1="12" x2="770" y2="40" stroke="#E2E8F0" stroke-width="1"/>

    <g transform="translate(795, 16)">
      <text x="10" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#1E1B4B">By Vijay <tspan fill="#64748B" font-weight="500">(@vijaymahes9080)</tspan></text>
    </g>
  </g>
</svg>
"""

# Dictionary of SVGs and dimensions
SVG_FILES = {
    "hero_banner_light": (hero_banner_svg, 1200, 500),
    "architecture_light": (architecture_svg, 1200, 480),
    "app1_hangman_light": (app1_svg, 1100, 420),
    "app2_portfolio_light": (app2_svg, 1100, 420),
    "app3_sorter_light": (app3_svg, 1100, 420),
    "app4_faq_light": (app4_svg, 1100, 420),
    "linkedin_showcase": (linkedin_svg, 1200, 675),
}

def render_svg_to_png(svg_path: Path, png_path: Path, width: int, height: int):
    # Wrap SVG in a bare-bones HTML page with no margins for exact pixel rendering
    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: {width}px;
    height: {height}px;
    overflow: hidden;
    background: #FAF9F6;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  svg {{
    width: {width}px;
    height: {height}px;
    display: block;
  }}
</style>
</head>
<body>
{svg_path.read_text(encoding='utf-8')}
</body>
</html>"""
    temp_html = svg_path.with_suffix(".temp.html")
    temp_html.write_text(html_content, encoding="utf-8")

    file_url = "file:///" + str(temp_html).replace("\\", "/")
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        f"--window-size={width},{height}",
        f"--screenshot={png_path}",
        file_url
    ]
    subprocess.run(cmd, check=True)
    temp_html.unlink(missing_ok=True)
    print(f"Rendered: {png_path.name} ({png_path.stat().st_size} bytes)")

def main():
    print("Generating SVGs and rendering PNGs...")
    for name, (svg_code, width, height) in SVG_FILES.items():
        svg_file = ASSETS_DIR / f"{name}.svg"
        png_file = ASSETS_DIR / f"{name}.png"
        svg_file.write_text(svg_code, encoding="utf-8")
        print(f"Saved SVG: {svg_file.name}")
        render_svg_to_png(svg_file, png_file, width, height)

    # Copy LinkedIn showcase assets to root
    # 1. image.png in root
    import shutil
    shutil.copy2(ASSETS_DIR / "linkedin_showcase.png", BASE_DIR / "image.png")
    print(f"Copied {ASSETS_DIR / 'linkedin_showcase.png'} -> {BASE_DIR / 'image.png'}")

    # 2. linkedin_showcase.svg in root
    shutil.copy2(ASSETS_DIR / "linkedin_showcase.svg", BASE_DIR / "linkedin_showcase.svg")
    print(f"Copied {ASSETS_DIR / 'linkedin_showcase.svg'} -> {BASE_DIR / 'linkedin_showcase.svg'}")

    print("\nAll assets generated successfully!")

if __name__ == "__main__":
    main()

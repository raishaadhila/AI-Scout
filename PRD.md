# PRD: AI-Scout (Blockchain & AI Intelligence Agent)

## 1. Project Overview
**AI-Scout** adalah agen AI otonom yang berfungsi sebagai peneliti (researcher) intelijen untuk memantau perkembangan terbaru dari perusahaan AI besar (Anthropic, Google, xAI, dll.) serta tren AI di ekosistem Solana. Agen ini melakukan scraping, merangkum berita menggunakan AI, dan mengirimkan laporan rutin ke Telegram.

- **Primary Platform**: Telegram Bot (DMs/Channel).
- **Intelligence Engine**: Gemini API (Pro/Flash).
- **Data Source**: X/Twitter (via `twscrape`).
- **Host Hardware**: ThinkPad L460 (Linux Mint).

## 2. Technical Stack
- **Framework**: ElizaOS (Modular AI Agent Framework).
- **Scraper**: `twscrape` (Python-based scraper menggunakan akun X cadangan).
- **LLM Provider**: Google Gemini API.
- **Interface**: `@elizaos/plugin-telegram`.
- **Database**: SQLite (Local) untuk menyimpan *tweet history* dan mencegah duplikasi berita.

## 3. Core Features & Requirements

### R1: The Hybrid Collector Strategy (Efficiency)
- **Background Research**: Bot melakukan scraping dan riset secara otomatis 30 menit sebelum jadwal pengiriman.
- **Data Persistence**: Hasil riset disimpan di SQLite. Bot tidak melakukan scraping ulang setiap kali user chat untuk menghemat CPU ThinkPad L460.
- **Fast Reply**: Jika user bertanya di luar jadwal, bot akan menjawab menggunakan data terbaru yang sudah ada di database.

### R2: Ordered Content Formatting
Setiap laporan di Telegram harus memiliki format yang konsisten dan akurat:
- **Numbered Summary**: Setiap poin berita wajib memiliki nomor urut.
- **Strict Link Mapping**: Link postingan X asli harus diletakkan tepat di bawah rangkuman berita yang relevan (korespondensi 1-ke-1).
- **Format Contoh**:
  1. [Rangkuman Berita A dari Gemini]
     - Link: [URL Postingan X Berita A]
  2. [Rangkuman Berita B dari Gemini]
     - Link: [URL Postingan X Berita B]

### R3: Automation & Scheduling
- **Jadwal Pengiriman**: Pesan otomatis dikirim 2x sehari pada pukul **08:00 AM** dan **04:00 PM**.
- **Content Scope**: Mencakup update dari Google AI, Anthropic, Perplexity, DeepSeek, ChatGPT, Kimi, Qwen, xAI, ElizaOS, x402, dan Solana updates.

## 4. Milestone Plan

### Phase 1: Environment & Scraper Setup
- [ ] Konfigurasi `twscrape` dengan akun X cadangan.
- [ ] Integrasi Gemini API Key ke dalam environment.
- [ ] Setup Telegram Bot via BotFather & ID mapping.

### Phase 2: Intelligence & Formatting Logic
- [ ] Implementasi script "Collector" untuk mengambil tweet dan menyimpannya di SQLite.
- [ ] Pembuatan Prompt System untuk Gemini agar output rangkuman selalu berurutan sesuai data input.
- [ ] Testing integrasi antara `twscrape` -> Gemini -> Telegram Formatting.

### Phase 3: Deployment & Optimization
- [ ] Setup Internal Scheduler ElizaOS untuk jam 08:00 & 16:00.
- [ ] Monitoring suhu dan penggunaan RAM pada ThinkPad L460 saat proses build/run.
- [ ] Finalisasi fitur "Fast Reply" menggunakan data dari SQLite.

## 5. Constraints & Security
- **Hardware Limit**: Proses `pnpm build` dilakukan secara bertahap untuk menghindari *overheat*.
- **API Safety**: Menggunakan *Rate Limiting* pada `twscrape` agar akun X tidak terkena ban.
- **Privacy**: File `.env` yang berisi API Keys dan Bot Token wajib masuk ke `.gitignore`.

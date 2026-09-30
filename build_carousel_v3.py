import base64
import json
import subprocess
from pathlib import Path

BASE_DIR = Path("/Users/ricksabchez/workspace/projects/iranian-youtubers")
HTML_DIR = BASE_DIR / "carousel_html"
PNG_DIR = BASE_DIR / "carousel_png"
AVATARS_DIR = BASE_DIR / "avatars"
FONTS_DIR = BASE_DIR / "fonts"

HTML_DIR.mkdir(parents=True, exist_ok=True)
PNG_DIR.mkdir(parents=True, exist_ok=True)

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Encode Vazirmatn-FD fonts
FONT_REGULAR_B64 = base64.b64encode((FONTS_DIR / "Vazirmatn-FD-Regular.woff2").read_bytes()).decode("ascii")
FONT_BOLD_B64 = base64.b64encode((FONTS_DIR / "Vazirmatn-FD-Bold.woff2").read_bytes()).decode("ascii")
FONT_BLACK_B64 = base64.b64encode((FONTS_DIR / "Vazirmatn-FD-Black.woff2").read_bytes()).decode("ascii")

def to_p(n):
    f = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']
    s = str(n)
    for i in range(10):
        s = s.replace(str(i), f[i])
    return s

def get_avatar_b64(handle):
    jpg_path = AVATARS_DIR / f"{handle.lower()}.jpg"
    if jpg_path.exists():
        data = jpg_path.read_bytes()
        return f"data:image/jpeg;base64,{base64.b64encode(data).decode('utf-8')}"
    svg_path = AVATARS_DIR / f"{handle.lower()}.svg"
    if svg_path.exists():
        data = svg_path.read_bytes()
        return f"data:image/svg+xml;base64,{base64.b64encode(data).decode('utf-8')}"
    return ""

def base_slide(slide_num, total, tag, title, body_html):
    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    @font-face {{
      font-family: 'VazirmatnFD';
      src: url('data:font/woff2;base64,{FONT_REGULAR_B64}') format('woff2');
      font-weight: 400;
      font-style: normal;
    }}
    @font-face {{
      font-family: 'VazirmatnFD';
      src: url('data:font/woff2;base64,{FONT_BOLD_B64}') format('woff2');
      font-weight: 700;
      font-style: normal;
    }}
    @font-face {{
      font-family: 'VazirmatnFD';
      src: url('data:font/woff2;base64,{FONT_BLACK_B64}') format('woff2');
      font-weight: 900;
      font-style: normal;
    }}
    * {{
      font-family: 'VazirmatnFD', Tahoma, sans-serif !important;
      letter-spacing: 0 !important;
    }}
    body {{
      width: 1080px;
      height: 1350px;
      overflow: hidden;
      background: radial-gradient(circle at 50% 10%, #1e0b1e 0%, #090d16 55%, #04060a 100%);
      color: #f8fafc;
    }}
    .glass-panel {{
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(20px);
      border: 1.5px solid rgba(255, 255, 255, 0.12);
    }}
    .glow-red {{
      box-shadow: 0 0 50px -10px rgba(239, 68, 68, 0.45);
    }}
  </style>
</head>
<body class="p-14 flex flex-col justify-between select-none">

  <!-- Header -->
  <div class="flex items-center justify-between border-b border-slate-800 pb-6">
    <div class="flex items-center gap-4">
      <div class="w-14 h-14 rounded-2xl bg-red-600 flex items-center justify-center text-white shadow-xl">
        <svg class="w-8 h-8 fill-current" viewBox="0 0 24 24">
          <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
        </svg>
      </div>
      <div>
        <div class="text-sm font-bold text-slate-400">تحلیل داده‌های ویدیویی یوتیوب فارسی</div>
        <div class="text-xl font-black text-white tracking-wide">IRANIAN YOUTUBERS HUB</div>
      </div>
    </div>
    
    <div class="flex items-center gap-2">
      <span class="px-5 py-2 rounded-2xl bg-slate-900 border border-slate-700 text-lg font-mono font-black text-slate-200">
        {to_p(slide_num)} / {to_p(total)}
      </span>
    </div>
  </div>

  <!-- Content -->
  <div class="flex-1 flex flex-col justify-center my-6">
    <div class="mb-7">
      <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-red-950/80 border border-red-700/60 text-red-400 text-base font-extrabold mb-3">
        {tag}
      </div>
      <h2 class="text-5xl font-black text-white leading-tight">
        {title}
      </h2>
    </div>

    {body_html}
  </div>

  <!-- Footer -->
  <div class="border-t border-slate-800 pt-6 flex items-center justify-between text-sm text-slate-400 font-semibold">
    <div>جامعه مستقل یوتیوبرهای ایرانی • سال ۲۰۲۶</div>
    <div class="flex items-center gap-3 text-slate-300 font-black text-base">
      <span>ورق بزنید</span>
      <svg class="w-5 h-5 fill-current rotate-180 text-red-500" viewBox="0 0 24 24">
        <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
      </svg>
    </div>
  </div>

</body>
</html>"""

def generate_slides():
    slides = []

    # Slide 1: Cover
    keoxer_av = get_avatar_b64("AriaKeoxer")
    putak_av = get_avatar_b64("BravePutak")
    silent_av = get_avatar_b64("FarshadSilent")
    mia_av = get_avatar_b64("MiaPlays")
    s1 = f"""
    <div class="space-y-8">
      <div class="p-10 rounded-3xl glass-panel glow-red border-red-500/40">
        <h1 class="text-6xl font-black text-white leading-tight mb-5">
          آناتومی پنهان <span class="text-red-500">یوتیوب فارسی</span>
        </h1>
        <p class="text-2xl text-slate-200 leading-relaxed font-medium">
          تحلیل ۲۳۹ کانال رسمی و ۲۵۰ میلیون بازدید؛ داده‌هایی که تولیدکنندگان محتوا و اسپانسرها درباره الگوریتم، درآمد و رکوردها به شما نمی‌گویند.
        </p>
      </div>

      <div class="grid grid-cols-3 gap-5">
        <div class="p-6 rounded-3xl glass-panel text-center border-slate-700">
          <div class="text-5xl font-black text-white">{to_p(239)}</div>
          <div class="text-base text-slate-400 mt-2 font-bold">کانال آنالیز شده</div>
        </div>
        <div class="p-6 rounded-3xl glass-panel text-center border-slate-700">
          <div class="text-5xl font-black text-red-400">+{to_p('250M')}</div>
          <div class="text-base text-slate-400 mt-2 font-bold">بازدید بررسی شده</div>
        </div>
        <div class="p-6 rounded-3xl glass-panel text-center border-slate-700">
          <div class="text-5xl font-black text-amber-400">{to_p(10)}</div>
          <div class="text-base text-slate-400 mt-2 font-bold">دسته‌بندی تخصصی</div>
        </div>
      </div>

      <div class="flex items-center justify-center gap-4 pt-2">
        <img src="{keoxer_av}" class="w-16 h-16 rounded-2xl object-cover border-2 border-red-500">
        <img src="{putak_av}" class="w-16 h-16 rounded-2xl object-cover border-2 border-amber-500">
        <img src="{silent_av}" class="w-16 h-16 rounded-2xl object-cover border-2 border-cyan-500">
        <img src="{mia_av}" class="w-16 h-16 rounded-2xl object-cover border-2 border-pink-500">
      </div>
    </div>"""
    slides.append((1, "کالبدشکافی داده‌محور ۲۰۲۶", "گزارش جامع استراتژیک", s1))

    # Slide 2: Pioneers
    jadi_av = get_avatar_b64("JadiMirmirani")
    s2 = f"""
    <div class="space-y-6">
      <div class="p-7 rounded-3xl glass-panel border-emerald-500/40 flex items-center gap-6">
        <img src="{jadi_av}" class="w-28 h-28 rounded-3xl object-cover border-2 border-emerald-500 shrink-0">
        <div>
          <span class="px-3.5 py-1 rounded-lg bg-emerald-950 text-emerald-400 border border-emerald-800 text-base font-extrabold">سال ۲۰۰۸ • پیشگام نرم‌افزار آزاد</span>
          <div class="text-3xl font-black text-white mt-2">جادی میرمیرانی</div>
          <p class="text-xl text-slate-300 mt-2 leading-relaxed">قدیمی‌ترین چنل فعال ایران. شروع آموزش لینوکس، پایتون و فرهنگ نرم‌افزار آزاد پیش از پیدایش واژه یوتیوبر در ایران.</p>
        </div>
      </div>

      <div class="p-7 rounded-3xl glass-panel border-red-500/40 flex items-center gap-6">
        <img src="{keoxer_av}" class="w-28 h-28 rounded-3xl object-cover border-2 border-red-500 shrink-0">
        <div>
          <span class="px-3.5 py-1 rounded-lg bg-red-950 text-red-400 border border-red-800 text-sm font-extrabold">سال ۲۰۱۵ • تولد یوتیوب گیمینگ</span>
          <div class="text-3xl font-black text-white mt-2">آریا کئوکسر</div>
          <p class="text-xl text-slate-300 mt-2 leading-relaxed">پایه‌گذار استاندارد استریم و لتس‌پلی روزانه فارسی؛ سازنده‌ای که نخستین کامیونیتی میلیونی مخاطبان جوان را شکل داد.</p>
        </div>
      </div>
    </div>"""
    slides.append((2, "کرونولوژی: پیشگامان نسل اول چه کسانی بودند؟", "تاریخچه بنیان‌گذاری", s2))

    # Slide 3: Female Creators
    sadaf_av = get_avatar_b64("SadafBeauty")
    s3 = f"""
    <div class="space-y-6">
      <div class="p-7 rounded-3xl glass-panel border-pink-500/40 flex items-center gap-6">
        <img src="{mia_av}" class="w-28 h-28 rounded-3xl object-cover border-2 border-pink-500 shrink-0">
        <div>
          <span class="px-3.5 py-1 rounded-lg bg-pink-950 text-pink-400 border border-pink-800 text-sm font-extrabold">اولین زن پیشرو در گیم و ولاگ</span>
          <div class="text-3xl font-black text-white mt-2">میا پلیز (کیمیا روانگر)</div>
          <p class="text-xl text-slate-300 mt-2 leading-relaxed">تحول بنیادین در کیفیت بصری از سال ۲۰۱۷؛ تلفیق هنر طراحی، شوخ‌طبعی و وفادارترین هسته مخاطب.</p>
        </div>
      </div>

      <div class="p-7 rounded-3xl glass-panel border-purple-500/40 flex items-center gap-6">
        <img src="{sadaf_av}" class="w-28 h-28 rounded-3xl object-cover border-2 border-purple-500 shrink-0">
        <div>
          <span class="px-3.5 py-1 rounded-lg bg-purple-950 text-purple-400 border border-purple-800 text-sm font-extrabold">استاندارد بین‌المللی بیوتی</span>
          <div class="text-3xl font-black text-white mt-2">صدف بیوتی</div>
          <p class="text-xl text-slate-300 mt-2 leading-relaxed">حضور در مجامع جهانی تولید محتوا و اتصال مارکت فارسی به کمپین‌های بین‌المللی با میلیونی‌ترین نرخ تعامل.</p>
        </div>
      </div>
    </div>"""
    slides.append((3, "پیشتازان زن: شکستن انحصار تولید محتوا", "تاثیرگذاری زنان", s3))

    # Slide 4: Chart: Most Uploaded Videos with Avatars
    bizixer_av = get_avatar_b64("MehdiBizixer")
    comix_av = get_avatar_b64("AliComix")
    abolfazl_av = get_avatar_b64("AbolfazlXMaster")
    s4 = f"""
    <div class="p-8 rounded-3xl glass-panel space-y-6">
      <div class="text-2xl font-black text-white">رده‌بندی برترین ماشین‌های تولید محتوا بر اساس تعداد آپلود:</div>

      <div class="space-y-5">
        <div>
          <div class="flex justify-between items-center mb-2">
            <div class="flex items-center gap-3">
              <img src="{bizixer_av}" class="w-12 h-12 rounded-xl object-cover border border-amber-500">
              <span class="text-xl font-bold text-white">۱. مهدی بیزیکسر (ماینکرفت و سروایول)</span>
            </div>
            <span class="text-amber-400 font-mono font-black text-2xl">+{to_p(3800)}</span>
          </div>
          <div class="w-full h-5 bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-gradient-to-r from-amber-500 to-amber-300 rounded-full" style="width: 100%;"></div>
          </div>
        </div>

        <div>
          <div class="flex justify-between items-center mb-2">
            <div class="flex items-center gap-3">
              <img src="{comix_av}" class="w-12 h-12 rounded-xl object-cover border border-cyan-500">
              <span class="text-xl font-bold text-white">۲. علی کامیکس (شبیه‌ساز و GTA)</span>
            </div>
            <span class="text-cyan-400 font-mono font-black text-2xl">+{to_p(2600)}</span>
          </div>
          <div class="w-full h-5 bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-gradient-to-r from-cyan-500 to-cyan-300 rounded-full" style="width: 68%;"></div>
          </div>
        </div>

        <div>
          <div class="flex justify-between items-center mb-2">
            <div class="flex items-center gap-3">
              <img src="{abolfazl_av}" class="w-12 h-12 rounded-xl object-cover border border-emerald-500">
              <span class="text-xl font-bold text-white">۳. ابوالفضل ایکس‌مستر (مدهای داستانی)</span>
            </div>
            <span class="text-emerald-400 font-mono font-black text-2xl">+{to_p(2300)}</span>
          </div>
          <div class="w-full h-5 bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-gradient-to-r from-emerald-500 to-emerald-300 rounded-full" style="width: 60%;"></div>
          </div>
        </div>

        <div>
          <div class="flex justify-between items-center mb-2">
            <div class="flex items-center gap-3">
              <img src="{keoxer_av}" class="w-12 h-12 rounded-xl object-cover border border-red-500">
              <span class="text-xl font-bold text-white">۴. آریا کئوکسر (گیمینگ و استریم)</span>
            </div>
            <span class="text-red-400 font-mono font-black text-2xl">+{to_p(2200)}</span>
          </div>
          <div class="w-full h-5 bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-gradient-to-r from-red-500 to-red-300 rounded-full" style="width: 58%;"></div>
          </div>
        </div>
      </div>

      <p class="text-lg text-slate-300 pt-3 border-t border-slate-800">
        درس الگوریتم: استمرار روزانه در بازی‌های با مخاطب نوجوان، واچ‌تایم را به اوج رسانده و جایگاه چنل را تثبیت می‌کند.
      </p>
    </div>"""
    slides.append((4, "ماشین‌های محتوا: چه کسانی بیشترین ویدیو را ساختند؟", "نمودار حجم تولید", s4))

    # Slide 5: Single Video Records with Avatars
    viny_av = get_avatar_b64("VinyShow")
    madgal_av = get_avatar_b64("MadGal")
    s5 = f"""
    <div class="space-y-6">
      <div class="p-7 rounded-3xl glass-panel border-red-500/40 flex items-start gap-6">
        <img src="{viny_av}" class="w-20 h-20 rounded-2xl object-cover border-2 border-red-500 shrink-0">
        <div class="flex-1">
          <div class="flex justify-between items-center mb-1">
            <span class="px-3 py-0.5 rounded-lg bg-red-950 text-red-400 text-sm font-extrabold">رکورد تاریخ سرگرمی</span>
            <span class="text-4xl font-black text-red-400 font-mono">+{to_p('5.1M')}</span>
          </div>
          <div class="text-2xl font-black text-white">برنامه Blind Date وینی (Viny)</div>
          <p class="text-lg text-slate-300 mt-2 leading-relaxed">
            فرمت بلایند دیت ایرانی با عبور از ۵ میلیون بازدید، بالاترین رکورد بازدید تکی را در تاریخ یوتیوب فارسی ثبت کرد.
          </p>
        </div>
      </div>

      <div class="p-7 rounded-3xl glass-panel border-purple-500/40 flex items-start gap-6">
        <img src="{putak_av}" class="w-20 h-20 rounded-2xl object-cover border-2 border-purple-500 shrink-0">
        <div class="flex-1">
          <div class="flex justify-between items-center mb-1">
            <span class="px-3 py-0.5 rounded-lg bg-purple-950 text-purple-400 text-sm font-extrabold">رکورد موزیک و چالش رپ</span>
            <span class="text-4xl font-black text-purple-400 font-mono">+{to_p('4.8M')}</span>
          </div>
          <div class="text-2xl font-black text-white">دیس‌ترک‌ها و پرونده‌های پوتک و مدگل</div>
          <p class="text-lg text-slate-300 mt-2 leading-relaxed">
            پیوند رپ زیرزمینی با ویدیوهای رازآلود و معماهای ترسناک، قله‌های میلیونی بازدید را بارها تصاحب کرد.
          </p>
        </div>
      </div>
    </div>"""
    slides.append((5, "قله‌های بازدید: پربیننده‌ترین تک‌ویدیوهای تاریخ", "رکوردهای تکی", s5))

    # Slide 6: TV to YouTube Migration with Avatars
    f360_av = get_avatar_b64("Football360Iran")
    s6 = f"""
    <div class="p-8 rounded-3xl glass-panel border-emerald-500/40 space-y-6">
      <div class="flex items-center gap-6">
        <img src="{f360_av}" class="w-24 h-24 rounded-3xl object-cover border-2 border-emerald-500 shrink-0">
        <div>
          <div class="text-3xl font-black text-white">فوتبال ۳۶۰ و عادل فردوسی‌پور</div>
          <div class="text-xl font-bold text-emerald-400 mt-1">مصاحبه با علی دایی: +۴.۳ میلیون بازدید</div>
        </div>
      </div>

      <p class="text-2xl text-slate-200 leading-relaxed">
        این گفتگو تنها یک مصاحبه نبود؛ آغاز رسمی مهاجرت مخاطب بزرگسال ایرانی از تلویزیون به یوتیوب بود. بالاترین زمان ماندگاری کاربر در یک اپیزود ۷۸ دقیقه‌ای در تاریخ پلتفرم ثبت شد.
      </p>

      <div class="grid grid-cols-2 gap-4 pt-4 border-t border-slate-800">
        <div class="text-center p-4 rounded-2xl bg-slate-900/90">
          <div class="text-4xl font-black text-white font-mono">+{to_p('70K')}</div>
          <div class="text-base text-slate-400 mt-1">کامنت تعاملی</div>
        </div>
        <div class="text-center p-4 rounded-2xl bg-slate-900/90">
          <div class="text-4xl font-black text-emerald-400 font-mono">{to_p(78)} دقیقه</div>
          <div class="text-base text-slate-400 mt-1">مدت زمان اپیزود</div>
        </div>
      </div>
    </div>"""
    slides.append((6, "زلزله رسانه‌ای: مهاجرت قطعی تلویزیون به یوتیوب", "کوچ مرجعیت رسانه", s6))

    # Slide 7: Chart: Follower Myth
    s7 = f"""
    <div class="p-8 rounded-3xl glass-panel space-y-6">
      <div class="text-3xl font-black text-white leading-snug">
        چرا عدد سابسکرایبر بزرگ‌ترین تله ذهنی است؟
      </div>
      <p class="text-xl text-slate-300 leading-relaxed">
        بررسی ۲۳۹ کانال نشان داد که در سال ۲۰۲۶ ارتباط سابسکرایبر با بازدید ویدیوهای جدید عملا قطع شده است:
      </p>

      <div class="space-y-5">
        <div>
          <div class="flex justify-between text-lg font-bold mb-2">
            <span class="text-emerald-400">مخاطبان فعال واقعی ویدیوهای جدید (۱۸٪)</span>
            <span class="font-mono text-emerald-400 font-black text-xl">{to_p('18%')}</span>
          </div>
          <div class="w-full h-7 bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-emerald-500 rounded-full" style="width: 18%;"></div>
          </div>
        </div>

        <div>
          <div class="flex justify-between text-lg font-bold mb-2">
            <span class="text-slate-400">دنبال‌کنندگان غیرفعال و نوتیفیکیشن خاموش (۸۲٪)</span>
            <span class="font-mono text-slate-400 font-black text-xl">{to_p('82%')}</span>
          </div>
          <div class="w-full h-7 bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-slate-600 rounded-full" style="width: 82%;"></div>
          </div>
        </div>
      </div>

      <div class="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 text-lg text-slate-200">
        نتیجه: کانال‌های ۸۰۰K ساب که میانگین ویوی ۹۰K دارند، ارزش تبلیغاتی کمتری از یک کانال ۲۰۰K با میانگین ویوی ۱۵۰K دارند!
      </div>
    </div>"""
    slides.append((7, "افسانه سابسکرایبر: فریب عدد دنبال‌کننده", "تحلیل رفتار الگوریتم", s7))

    # Slide 8: Average Views Leaderboard with Avatars
    kouman_av = get_avatar_b64("KoumanOfficial")
    mobo_av = get_avatar_b64("MoboNews")
    s8 = f"""
    <div class="p-8 rounded-3xl glass-panel space-y-6">
      <div class="text-2xl font-black text-white">پادشاهان پایداری: بالاترین میانگین بازدید ویدیوهای اخیر</div>

      <div class="space-y-4">
        <div>
          <div class="flex justify-between items-center mb-1">
            <div class="flex items-center gap-3">
              <img src="{kouman_av}" class="w-10 h-10 rounded-xl object-cover border border-red-500">
              <span class="text-lg font-bold text-white">۱. کومان (کوروش و ایمان)</span>
            </div>
            <span class="text-red-400 font-mono font-black text-xl">+{to_p('280K')}</span>
          </div>
          <div class="w-full h-4 bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-red-500 rounded-full" style="width: 100%;"></div>
          </div>
        </div>

        <div>
          <div class="flex justify-between items-center mb-1">
            <div class="flex items-center gap-3">
              <img src="{keoxer_av}" class="w-10 h-10 rounded-xl object-cover border border-slate-600">
              <span class="text-lg font-bold text-white">۲. آریا کئوکسر</span>
            </div>
            <span class="text-slate-200 font-mono font-black text-xl">+{to_p('220K')}</span>
          </div>
          <div class="w-full h-4 bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-slate-400 rounded-full" style="width: 78%;"></div>
          </div>
        </div>

        <div>
          <div class="flex justify-between items-center mb-1">
            <div class="flex items-center gap-3">
              <img src="{silent_av}" class="w-10 h-10 rounded-xl object-cover border border-slate-600">
              <span class="text-lg font-bold text-white">۳. فرشاد سایلنت</span>
            </div>
            <span class="text-slate-200 font-mono font-black text-xl">+{to_p('190K')}</span>
          </div>
          <div class="w-full h-4 bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-slate-400 rounded-full" style="width: 68%;"></div>
          </div>
        </div>

        <div>
          <div class="flex justify-between items-center mb-1">
            <div class="flex items-center gap-3">
              <img src="{f360_av}" class="w-10 h-10 rounded-xl object-cover border border-slate-600">
              <span class="text-lg font-bold text-white">۴. فوتبال ۳۶۰</span>
            </div>
            <span class="text-slate-200 font-mono font-black text-xl">+{to_p('180K')}</span>
          </div>
          <div class="w-full h-4 bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-slate-400 rounded-full" style="width: 64%;"></div>
          </div>
        </div>

        <div>
          <div class="flex justify-between items-center mb-1">
            <div class="flex items-center gap-3">
              <img src="{mobo_av}" class="w-10 h-10 rounded-xl object-cover border border-slate-600">
              <span class="text-lg font-bold text-white">۵. موبونیوز (مهدی شجاری)</span>
            </div>
            <span class="text-slate-200 font-mono font-black text-xl">+{to_p('130K')}</span>
          </div>
          <div class="w-full h-4 bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-slate-400 rounded-full" style="width: 46%;"></div>
          </div>
        </div>
      </div>
    </div>"""
    slides.append((8, "پادشاهان پایداری: بیشترین ویوی واقعی در هر ویدیو", "رتبه‌بندی عملکرد", s8))

    # Slide 9: Tech & Niche Leaders with Avatars
    bandari_av = get_avatar_b64("AliBandari")
    s9 = f"""
    <div class="space-y-6">
      <div class="p-7 rounded-3xl glass-panel border-cyan-500/40 flex items-center gap-6">
        <img src="{mobo_av}" class="w-24 h-24 rounded-3xl object-cover border-2 border-cyan-500 shrink-0">
        <div>
          <span class="px-3.5 py-1 rounded-lg bg-cyan-950 text-cyan-400 border border-cyan-800 text-sm font-extrabold">مرجع فناوری و راهنمای خرید</span>
          <div class="text-3xl font-black text-white mt-2">مهدی شجاری (موبونیوز)</div>
          <p class="text-xl text-slate-300 mt-2 leading-relaxed">بیش از ۴۱۰K دنبال‌کننده؛ تبدیل نقد و بررسی گجت به یک بیزینس رسانه‌ای مدرن و مستقل.</p>
        </div>
      </div>

      <div class="p-7 rounded-3xl glass-panel border-amber-500/40 flex items-center gap-6">
        <img src="{bandari_av}" class="w-24 h-24 rounded-3xl object-cover border-2 border-amber-500 shrink-0">
        <div>
          <span class="px-3.5 py-1 rounded-lg bg-amber-950 text-amber-400 border border-amber-800 text-sm font-extrabold">پادشاه روایت مستند و کتاب</span>
          <div class="text-3xl font-black text-white mt-2">علی بندری (چنل‌بی و بی‌پلاس)</div>
          <p class="text-xl text-slate-300 mt-2 leading-relaxed">بیش از ۳۴۰K دنبال‌کننده فرهیخته؛ اثبات اینکه محتوای پژوهشی و متفکرانه هم می‌تواند وایرال شود.</p>
        </div>
      </div>
    </div>"""
    slides.append((9, "غول‌های نیچ: پیشتازان محتوای تخصصی و خردمندانه", "قدرت تولید عمیق", s9))

    # Slide 10: Category Share Chart with Top Avatars
    sogang_av = get_avatar_b64("SoGang")
    s10 = f"""
    <div class="p-8 rounded-3xl glass-panel space-y-6">
      <div class="text-2xl font-black text-white">سهم ژانرها از کل ترافیک یوتیوب فارسی در سال ۲۰۲۶:</div>

      <div class="space-y-5">
        <div>
          <div class="flex justify-between items-center mb-1">
            <div class="flex items-center gap-3">
              <img src="{sogang_av}" class="w-10 h-10 rounded-xl object-cover border border-red-500">
              <span class="text-lg font-bold text-red-400">۱. سرگرمی، چالش و طنز</span>
            </div>
            <span class="font-mono text-red-400 font-black text-2xl">{to_p('42%')}</span>
          </div>
          <div class="w-full h-5 bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-red-500 rounded-full" style="width: 42%;"></div>
          </div>
        </div>

        <div>
          <div class="flex justify-between items-center mb-1">
            <div class="flex items-center gap-3">
              <img src="{bizixer_av}" class="w-10 h-10 rounded-xl object-cover border border-cyan-500">
              <span class="text-lg font-bold text-cyan-400">۲. گیمینگ و ماینکرفت</span>
            </div>
            <span class="font-mono text-cyan-400 font-black text-2xl">{to_p('26%')}</span>
          </div>
          <div class="w-full h-5 bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-cyan-500 rounded-full" style="width: 26%;"></div>
          </div>
        </div>

        <div>
          <div class="flex justify-between items-center mb-1">
            <div class="flex items-center gap-3">
              <img src="{bandari_av}" class="w-10 h-10 rounded-xl object-cover border border-amber-500">
              <span class="text-lg font-bold text-amber-400">۳. پادکست، گفتگو و تاریخ</span>
            </div>
            <span class="font-mono text-amber-400 font-black text-2xl">{to_p('16%')}</span>
          </div>
          <div class="w-full h-5 bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-amber-500 rounded-full" style="width: 16%;"></div>
          </div>
        </div>

        <div>
          <div class="flex justify-between items-center mb-1">
            <div class="flex items-center gap-3">
              <img src="{jadi_av}" class="w-10 h-10 rounded-xl object-cover border border-emerald-500">
              <span class="text-lg font-bold text-emerald-400">۴. تکنولوژی، کدنویسی و مالی</span>
            </div>
            <span class="font-mono text-emerald-400 font-black text-2xl">{to_p('16%')}</span>
          </div>
          <div class="w-full h-5 bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-emerald-500 rounded-full" style="width: 16%;"></div>
          </div>
        </div>
      </div>
    </div>"""
    slides.append((10, "نقشه ترافیک: کیک مخاطبان در دست چه ژانرهایی است؟", "نمودار سهم بازار", s10))

    # Slide 11: CPM Comparison Chart
    s11 = f"""
    <div class="p-8 rounded-3xl glass-panel space-y-6">
      <div class="text-3xl font-black text-white leading-snug">
        شکاف درآمد ادسنس: چرا بازدید ایرانی ارزان است؟
      </div>
      <p class="text-xl text-slate-300 leading-relaxed">
        به دلیل استفاده گسترده از VPNهای رایگان و عدم تبلیغ شرکت‌های بین‌المللی در ایران، میانگین درآمد به ازای هر ۱۰۰۰ بازدید (CPM) به شدت سرکوب شده است:
      </p>

      <div class="space-y-5">
        <div>
          <div class="flex justify-between items-center text-lg font-bold mb-1">
            <span class="text-slate-400">میانگین CPM مخاطب جهانی (آمریکا و اروپا)</span>
            <span class="text-emerald-400 font-mono font-black text-3xl">$۸ - $۱۵</span>
          </div>
          <div class="w-full h-6 bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-emerald-500 rounded-full" style="width: 90%;"></div>
          </div>
        </div>

        <div>
          <div class="flex justify-between items-center text-lg font-bold mb-1">
            <span class="text-slate-400">میانگین CPM مخاطب فارسی داخل ایران</span>
            <span class="text-red-400 font-mono font-black text-3xl">$۰.۶ - $۱.۴</span>
          </div>
          <div class="w-full h-6 bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-red-500 rounded-full" style="width: 12%;"></div>
          </div>
        </div>
      </div>

      <div class="p-5 rounded-2xl bg-red-950/40 border border-red-800/60 text-lg text-red-200">
        نتیجه: برای یک ویدیوی ۱۰۰K ویو در ایران تنها ۵۰ تا ۱۲۰ دلار ادسنس پرداخت می‌شود؛ در حالی که در خارج تا ۱۲۰۰ دلار است.
      </div>
    </div>"""
    slides.append((11, "اقتصاد ادسنس: واقعیت تلخ درآمد دلاری در ایران", "نمودار مقایسه CPM", s11))

    # Slide 12: Income Breakdown Chart with Creator Examples
    s12 = f"""
    <div class="p-8 rounded-3xl glass-panel space-y-6">
      <div class="text-2xl font-black text-white">ترکیب واقعی سبد درآمد یک یوتیوبر موفق ایرانی:</div>

      <div class="space-y-5">
        <div>
          <div class="flex justify-between items-center text-lg font-bold mb-1">
            <span class="text-emerald-400">۱. اسپانسرشیپ و کمپین‌های برندهای داخلی</span>
            <span class="font-mono text-emerald-400 font-black text-2xl">{to_p('65%')}</span>
          </div>
          <div class="w-full h-6 bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-emerald-500 rounded-full" style="width: 65%;"></div>
          </div>
        </div>

        <div>
          <div class="flex justify-between items-center text-lg font-bold mb-1">
            <span class="text-cyan-400">۲. درآمد دلاری ادسنس یوتیوب</span>
            <span class="font-mono text-cyan-400 font-black text-2xl">{to_p('25%')}</span>
          </div>
          <div class="w-full h-6 bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-cyan-500 rounded-full" style="width: 25%;"></div>
          </div>
        </div>

        <div>
          <div class="flex justify-between items-center text-lg font-bold mb-1">
            <span class="text-amber-400">۳. دونیت، افیلیت و فروش خدمات شخصی</span>
            <span class="font-mono text-amber-400 font-black text-2xl">{to_p('10%')}</span>
          </div>
          <div class="w-full h-6 bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-amber-500 rounded-full" style="width: 10%;"></div>
          </div>
        </div>
      </div>

      <p class="text-xl text-slate-200 pt-4 border-t border-slate-800 leading-relaxed font-bold">
        قانون طلایی: یوتیوبرهایی که فقط به ادسنس متکی باشند دوام نمی‌آورند؛ برندگان کسانی هستند که برندینگ تجاری دارند.
      </p>
    </div>"""
    slides.append((12, "شریان حیاتی: درآمدها از کجا تامین می‌شود؟", "مدل اقتصادی", s12))

    # Slide 13: Chart: Golden Duration with Creator Avatars
    deep_av = get_avatar_b64("DeepPodcast")
    tabaghe_av = get_avatar_b64("Tabaghe16")
    s13 = f"""
    <div class="p-8 rounded-3xl glass-panel space-y-6">
      <div class="text-3xl font-black text-white leading-snug">
        زمان طلایی ویدیو در ۲۰۲۶: ۲۲ تا ۳۸ دقیقه
      </div>
      <p class="text-xl text-slate-300 leading-relaxed">
        الگوریتم لانگ‌فرم دیگر به ویدیوهای زیر ۱۰ دقیقه توجهی ندارد. ویدیوهایی برنده هستند که مخاطب را برای یک مدت ممتد در پلتفرم حفظ کنند:
      </p>

      <div class="space-y-4">
        <div class="p-4 rounded-2xl bg-slate-900 border border-slate-800 flex justify-between items-center">
          <span class="text-lg font-bold text-slate-300">ویدیوهای زیر ۱۰ دقیقه (منسوخ شده)</span>
          <span class="text-red-400 font-bold">افت شدید نرخ پروموت</span>
        </div>
        <div class="p-4 rounded-2xl bg-slate-900 border border-slate-800 flex justify-between items-center">
          <span class="text-lg font-bold text-slate-300">ویدیوهای ۱۰ تا ۲۰ دقیقه (متوسط)</span>
          <span class="text-amber-400 font-bold">رشد باثبات برای ولاگ</span>
        </div>
        <div class="p-5 rounded-2xl bg-emerald-950/60 border border-emerald-500 flex justify-between items-center">
          <span class="text-xl font-bold text-white">ویدیوهای ۲۲ تا ۳۸ دقیقه (منطقه طلایی)</span>
          <span class="text-emerald-400 font-black text-xl">حداکثر واچ‌تایم و میان‌برنامه</span>
        </div>
      </div>

      <div class="flex items-center gap-4 pt-2">
        <div class="flex items-center gap-3 p-3 rounded-2xl bg-slate-900 border border-slate-800 flex-1">
          <img src="{deep_av}" class="w-12 h-12 rounded-xl object-cover border border-red-500">
          <span class="text-sm font-bold text-slate-300">دیپ پادکست: میانگین ۳۵ دقیقه</span>
        </div>
        <div class="flex items-center gap-3 p-3 rounded-2xl bg-slate-900 border border-slate-800 flex-1">
          <img src="{tabaghe_av}" class="w-12 h-12 rounded-xl object-cover border border-purple-500">
          <span class="text-sm font-bold text-slate-300">طبقه ۱۶: میانگین ۷۰ دقیقه</span>
        </div>
      </div>
    </div>"""
    slides.append((13, "مهندسی الگوریتم: طول ویدیوی طلایی چقدر است؟", "طول بهینه ویدیو", s13))

    # Slide 14: Collab Multiplier with Avatars
    kourosh_av = get_avatar_b64("KouroshTopia")
    iman_av = get_avatar_b64("ImanDastpak")
    s14 = f"""
    <div class="p-8 rounded-3xl glass-panel space-y-6">
      <div class="text-4xl font-black text-white">
        معجزه همکاری: فرمت دونفره vs اجرای انفرادی
      </div>
      <p class="text-xl text-slate-300 leading-relaxed">
        داده‌های کانال‌های موفقی مثل کومان، کوروش و میا، و چالش‌های پوتک و فرشاد نشان می‌دهد همکاری اشتراکی اثری چندبرابری دارد:
      </p>

      <div class="grid grid-cols-2 gap-5 pt-2">
        <div class="p-6 rounded-3xl bg-slate-900/80 border border-slate-700 text-center">
          <div class="text-lg text-slate-400 font-bold">افزایش نرخ کامنت و تعامل</div>
          <div class="text-6xl font-black text-emerald-400 font-mono mt-3">+{to_p('62%')}</div>
        </div>
        <div class="p-6 rounded-3xl bg-slate-900/80 border border-slate-700 text-center">
          <div class="text-lg text-slate-400 font-bold">کاهش ریزش در ۲ دقیقه اول</div>
          <div class="text-6xl font-black text-cyan-400 font-mono mt-3">-{to_p('35%')}</div>
        </div>
      </div>

      <div class="flex items-center justify-center gap-4 pt-2">
        <img src="{kourosh_av}" class="w-14 h-14 rounded-2xl object-cover border-2 border-red-500">
        <img src="{iman_av}" class="w-14 h-14 rounded-2xl object-cover border-2 border-amber-500">
        <img src="{mia_av}" class="w-14 h-14 rounded-2xl object-cover border-2 border-pink-500">
        <img src="{putak_av}" class="w-14 h-14 rounded-2xl object-cover border-2 border-purple-500">
        <img src="{silent_av}" class="w-14 h-14 rounded-2xl object-cover border-2 border-cyan-500">
      </div>
    </div>"""
    slides.append((14, "معجزه هم‌افزایی: چرا ویدیوهای تیمی رکورد می‌زنند؟", "روانشناسی تماشا", s14))

    # Slide 15: Thumbnail Principles with Avatars
    hami_av = get_avatar_b64("HamiKM")
    brooks_av = get_avatar_b64("AliBrooks")
    s15 = f"""
    <div class="p-8 rounded-3xl glass-panel space-y-6">
      <div class="text-3xl font-black text-white">
        ۳ قانون تامبنیل‌های برنده با CTR بالای ۱۰ درصد
      </div>

      <div class="space-y-4 text-slate-200">
        <div class="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 flex items-center gap-4">
          <img src="{hami_av}" class="w-14 h-14 rounded-2xl object-cover border border-emerald-500 shrink-0">
          <div>
            <div class="text-xl font-bold text-red-400">۱. حداکثر ۲ تا ۳ کلمه شوکه‌کننده</div>
            <div class="text-base text-slate-300 mt-1">نوشتن جملات طولانی در موبایل ناخواناست و چشم بیننده را خسته می‌کند.</div>
          </div>
        </div>

        <div class="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 flex items-center gap-4">
          <img src="{brooks_av}" class="w-14 h-14 rounded-2xl object-cover border border-cyan-500 shrink-0">
          <div>
            <div class="text-xl font-bold text-cyan-400">۲. کنتراست شدید نور روی میمیک چهره</div>
            <div class="text-base text-slate-300 mt-1">چهره واضح با نورپردازی متمرکز، حس کنجکاوی ناخودآگاه مخاطب را بیدار می‌کند.</div>
          </div>
        </div>

        <div class="p-5 rounded-2xl bg-slate-900/90 border border-slate-800">
          <div class="text-xl font-bold text-amber-400">۳. خلق شکاف اطلاعاتی (Information Gap)</div>
          <div class="text-base text-slate-300 mt-1">تصویر نباید پایان ماجرا را لو بدهد؛ بلکه باید یک سوال حل‌نشده در ذهن بکارد.</div>
        </div>
      </div>
    </div>"""
    slides.append((15, "آناتومی کلیک: چگونه نرخ کلیک (CTR) را منفجر کنیم؟", "اصول طراحی تامبنیل", s15))

    # Slide 16: Studio Standards with Avatars
    ahoora_av = get_avatar_b64("AhooraNiazi")
    shakouri_av = get_avatar_b64("ShakouriM")
    s16 = f"""
    <div class="p-8 rounded-3xl glass-panel space-y-6">
      <div class="text-3xl font-black text-white">
        جهش فنی: پایان عصر ویدیوهای وب‌کمی بی‌کیفیت
      </div>
      <p class="text-xl text-slate-300 leading-relaxed">
        استانداردهای فنی یوتیوب فارسی در سال ۲۰۲۶ با بهترین استودیوهای جهانی رقابت می‌کند:
      </p>

      <div class="grid grid-cols-2 gap-4 text-slate-200">
        <div class="p-5 rounded-2xl bg-slate-900/90 border border-slate-800">
          <div class="flex items-center gap-3 mb-2">
            <img src="{ahoora_av}" class="w-10 h-10 rounded-xl object-cover border border-cyan-500">
            <span class="text-lg font-black text-cyan-400">نورپردازی سینمایی</span>
          </div>
          <div class="text-sm text-slate-400">جداسازی کامل سوژه از بک‌گراند با نورهای RGB و سافت‌باکس‌های دایره‌ای بزرگ.</div>
        </div>

        <div class="p-5 rounded-2xl bg-slate-900/90 border border-slate-800">
          <div class="flex items-center gap-3 mb-2">
            <img src="{shakouri_av}" class="w-10 h-10 rounded-xl object-cover border border-emerald-500">
            <span class="text-lg font-black text-emerald-400">صدابرداری استودیویی</span>
          </div>
          <div class="text-sm text-slate-400">استفاده فراگیر از میکروفون‌های Shure SM7B و Rode Wireless Pro؛ بیننده نویز را تحمل نمی‌کند.</div>
        </div>
      </div>

      <div class="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 text-lg text-slate-300 font-bold">
        سرمایه‌گذاری روی تجهیزات صوتی و نور، نرخ تماشای طولانی را تا ۴۰ درصد افزایش داده است.
      </div>
    </div>"""
    slides.append((16, "استاندارد استودیو: جهش کیفیت صدا و تصویر", "زیرساخت فنی", s16))

    # Slide 17: Video Podcasts with Avatars
    radiorah_av = get_avatar_b64("RadioRahOfficial")
    rokh_av = get_avatar_b64("RokhPodcast")
    s17 = f"""
    <div class="p-8 rounded-3xl glass-panel border-purple-500/40 space-y-6">
      <div class="text-3xl font-black text-white">
        انقلاب ویدیولانگ‌پادکست‌ها در ایران
      </div>
      <p class="text-xl text-slate-200 leading-relaxed">
        طبقه ۱۶، رادیو راه، دایجست، رخ و ساگا اثبات کردند که مخاطب ایرانی شیفته گفتگوهای عمیق ۶۰ تا ۹۰ دقیقه‌ای است:
      </p>

      <div class="grid grid-cols-3 gap-4 text-center">
        <div class="p-4 rounded-2xl bg-slate-900 border border-slate-800">
          <div class="text-4xl font-black text-purple-400 font-mono">+{to_p('75m')}</div>
          <div class="text-sm text-slate-400 mt-1">میانگین زمان اپیزودها</div>
        </div>
        <div class="p-4 rounded-2xl bg-slate-900 border border-slate-800">
          <div class="text-4xl font-black text-emerald-400 font-mono">{to_p('88%')}</div>
          <div class="text-sm text-slate-400 mt-1">مخاطبان بالای ۲۲ سال</div>
        </div>
        <div class="p-4 rounded-2xl bg-slate-900 border border-slate-800">
          <div class="text-4xl font-black text-cyan-400 font-mono">۳.۵x</div>
          <div class="text-sm text-slate-400 mt-1">ارزش بالاتر اسپانسر</div>
        </div>
      </div>

      <div class="flex items-center justify-center gap-4 pt-2">
        <div class="flex items-center gap-2">
          <img src="{tabaghe_av}" class="w-12 h-12 rounded-xl object-cover border border-purple-500">
          <span class="text-sm font-bold text-slate-300">سهیل علوی</span>
        </div>
        <div class="flex items-center gap-2">
          <img src="{radiorah_av}" class="w-12 h-12 rounded-xl object-cover border border-blue-500">
          <span class="text-sm font-bold text-slate-300">مجتبی شکوری</span>
        </div>
        <div class="flex items-center gap-2">
          <img src="{rokh_av}" class="w-12 h-12 rounded-xl object-cover border border-red-500">
          <span class="text-sm font-bold text-slate-300">پادکست رخ</span>
        </div>
      </div>
    </div>"""
    slides.append((17, "عصر پادکست‌های ویدیویی: عمق به جای ابتذال", "بلوغ محتوا", s17))

    # Slide 18: Gaming Transition with Avatars
    hesam_av = get_avatar_b64("HesamLD")
    amoobig_av = get_avatar_b64("AmooBig")
    s18 = f"""
    <div class="p-8 rounded-3xl glass-panel border-emerald-500/40 space-y-6">
      <div class="text-3xl font-black text-white">
        گذار بزرگ گیمینگ: پیروزی داستان‌سرایی بر مهارت صِرف
      </div>
      <p class="text-xl text-slate-300 leading-relaxed">
        دوران استریم‌های خشک و مهارت‌محور کالاف دیوتی اشباع شده است. بازی‌هایی که داستان دارند پادشاهی می‌کنند:
      </p>

      <div class="space-y-4">
        <div class="p-5 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <img src="{hesam_av}" class="w-12 h-12 rounded-xl object-cover border border-emerald-500">
            <span class="text-lg font-bold text-slate-200">ماینکرفت سروایول و رول‌پلی GTA</span>
          </div>
          <span class="text-emerald-400 font-black text-xl">+{to_p('80%')} واچ‌تایم پایدار</span>
        </div>

        <div class="p-5 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <img src="{amoobig_av}" class="w-12 h-12 rounded-xl object-cover border border-cyan-500">
            <span class="text-lg font-bold text-slate-200">شبیه‌سازهای مدیریتی و مشاغل عجیب</span>
          </div>
          <span class="text-cyan-400 font-black text-xl">+{to_p('65%')} بیننده جدید</span>
        </div>
      </div>

      <p class="text-lg text-slate-300">
        دلیل: نسل جدید به دنبال قصه، چالش و همذات‌پنداری است، نه فقط هدشات گرفتن در یک بازی شوتر تکراری.
      </p>
    </div>"""
    slides.append((18, "تحول گیمینگ: داستان‌سرایی جایگزین شوترهای تکراری", "روندهای بازی", s18))

    # Slide 19: Strategic Matrix with Avatars
    qumars_av = get_avatar_b64("QumarsOfficial")
    siamak_av = get_avatar_b64("SiamakGhassemi")
    s19 = f"""
    <div class="p-8 rounded-3xl glass-panel space-y-6">
      <div class="text-3xl font-black text-white">
        نقشه راه برنده: درس‌های کلیدی برای سازندگان و برندها
      </div>

      <div class="space-y-4 text-slate-200">
        <div class="p-5 rounded-2xl bg-emerald-950/50 border border-emerald-500/40 flex items-start gap-4">
          <img src="{qumars_av}" class="w-14 h-14 rounded-2xl object-cover border border-emerald-500 shrink-0">
          <div>
            <div class="text-xl font-black text-emerald-400">توصیه طلایی به تولیدکنندگان محتوا:</div>
            <div class="text-base text-slate-300 mt-1 leading-relaxed">وارد بازارهای اشباع‌شده نشوید. نیچ‌های خالی مانند اقتصاد فردی، آموزش‌های عملی، مستندهای تحقیقی و سینمای عمیق تشنه محتوای درجه یک هستند.</div>
          </div>
        </div>

        <div class="p-5 rounded-2xl bg-cyan-950/50 border border-cyan-500/40 flex items-start gap-4">
          <img src="{siamak_av}" class="w-14 h-14 rounded-2xl object-cover border border-cyan-500 shrink-0">
          <div>
            <div class="text-xl font-black text-cyan-400">توصیه استراتژیک به اسپانسرها و برندها:</div>
            <div class="text-base text-slate-300 mt-1 leading-relaxed">هرگز بر اساس تعداد سابسکرایبر قرارداد نبندید؛ معیار واقعی اثربخشی، میانگین بازدید ۳۰ روز گذشته و لحن تعاملی کامنت‌هاست.</div>
          </div>
        </div>
      </div>
    </div>"""
    slides.append((19, "درس‌های کاربردی: راهنمای سازندگان و حامیان مالی", "نقشه راه استراتژیک", s19))

    # Slide 20: CTA
    s20 = f"""
    <div class="p-10 rounded-3xl glass-panel glow-red border-red-500/50 text-center space-y-7">
      <div class="w-24 h-24 mx-auto rounded-3xl bg-red-600 flex items-center justify-center text-white shadow-2xl">
        <svg class="w-12 h-12 fill-current" viewBox="0 0 24 24">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9v-2h2v2zm0-4H9V7h2v5zm4 4h-2v-2h2v2zm0-4h-2V7h2v5z"/>
        </svg>
      </div>

      <div>
        <h2 class="text-4xl font-black text-white leading-tight">
          پایگاه داده مستقل یوتیوبرهای ایرانی
        </h2>
        <p class="text-xl text-slate-300 mt-3 max-w-xl mx-auto leading-relaxed">
          دسترسی آزاد به مشخصات ۲۳۹ یوتیوبر فعال، آدرس کانال‌ها و آمار دقیق دنبال‌کنندگان به همراه جامعه رسمی در تلگرام:
        </p>
      </div>

      <div class="p-6 rounded-3xl bg-slate-900 border border-slate-700 space-y-2">
        <div class="text-sm font-bold text-slate-400">آدرس پرتال روی گیت‌هاب پیجز:</div>
        <div class="text-2xl font-mono font-black text-red-400">m4tinbeigi-official.github.io/iranian-youtubers</div>
        <div class="text-sm font-mono text-slate-500">لینک کوتاه: B2n.ir/hx3429</div>
      </div>

      <div class="text-base text-slate-400">
        کانال و گروه تلگرام با تایید ادمین برای تولیدکنندگان محتوا فعال است.
      </div>
    </div>"""
    slides.append((20, "جامعه یوتیوبرهای ایران هم‌اکنون آنلاین است", "دسترسی آزاد", s20))

    return slides

def main():
    slides = generate_slides()
    total = len(slides)

    print(f"Generating {total} V3 slides with Vazirmatn-FD and creator avatars...")
    html_files = []
    for num, title, subtitle, content in slides:
        html_text = base_slide(num, total, subtitle, title, content)
        filename = f"slide_{num:02d}.html"
        file_path = HTML_DIR / filename
        file_path.write_text(html_text, encoding="utf-8")
        html_files.append((num, file_path))

    print(f"Rendering {total} slides with Google Chrome headless...")
    for num, html_path in html_files:
        png_path = PNG_DIR / f"slide_{num:02d}.png"
        cmd = [
            CHROME_PATH,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--no-first-run",
            "--virtual-time-budget=2000",
            f"--screenshot={png_path}",
            "--window-size=1080,1350",
            f"file://{html_path}"
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"Rendered slide {num:02d} -> {png_path.stat().st_size // 1024} KB")

if __name__ == "__main__":
    main()

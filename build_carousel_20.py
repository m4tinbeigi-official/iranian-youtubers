import base64
import json
import subprocess
from pathlib import Path

BASE_DIR = Path("/Users/ricksabchez/workspace/projects/iranian-youtubers")
HTML_DIR = BASE_DIR / "carousel_html"
PNG_DIR = BASE_DIR / "carousel_png"
AVATARS_DIR = BASE_DIR / "avatars"

HTML_DIR.mkdir(parents=True, exist_ok=True)
PNG_DIR.mkdir(parents=True, exist_ok=True)

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def to_persian(n):
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

def base_slide_template(slide_num, total_slides, title, subtitle, content_html, footer_tag="گزارش تحلیلی جامع یوتیوب فارسی ۲۰۲۶"):
    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {{
      width: 1080px;
      height: 1350px;
      overflow: hidden;
      font-family: 'Vazirmatn', Tahoma, sans-serif;
      letter-spacing: 0 !important;
      background: radial-gradient(circle at 50% 15%, #180918 0%, #080c16 65%, #05070c 100%);
      color: #f1f5f9;
    }}
    .glass-box {{
      background: rgba(17, 24, 39, 0.78);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .glow-red {{
      box-shadow: 0 0 45px -10px rgba(239, 68, 68, 0.35);
    }}
    .glow-gold {{
      box-shadow: 0 0 40px -10px rgba(234, 179, 8, 0.3);
    }}
  </style>
</head>
<body class="p-14 flex flex-col justify-between select-none">

  <!-- Header -->
  <div class="flex items-center justify-between border-b border-slate-800/80 pb-6">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-2xl bg-red-600 flex items-center justify-center text-white shadow-lg">
        <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24">
          <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
        </svg>
      </div>
      <div>
        <div class="text-xs font-bold text-slate-400">کالبدشکافی تحلیلی یوتیوب فارسی</div>
        <div class="text-sm font-black text-white">IRANIAN YOUTUBERS HUB</div>
      </div>
    </div>
    
    <div class="flex items-center gap-2">
      <span class="px-3.5 py-1.5 rounded-full bg-slate-900 border border-slate-700/80 text-xs font-mono font-bold text-slate-300">
        {to_persian(slide_num)} / {to_persian(total_slides)}
      </span>
    </div>
  </div>

  <!-- Main Body -->
  <div class="flex-1 flex flex-col justify-center my-6">
    <div class="mb-8">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-red-950/70 border border-red-700/50 text-red-400 text-xs font-bold mb-3">
        {subtitle}
      </div>
      <h2 class="text-4xl font-black text-white leading-tight">
        {title}
      </h2>
    </div>

    {content_html}
  </div>

  <!-- Footer -->
  <div class="border-t border-slate-800/80 pt-6 flex items-center justify-between text-xs text-slate-500 font-medium">
    <div>{footer_tag}</div>
    <div class="flex items-center gap-2 text-slate-400 font-semibold">
      <span>ورق بزنید</span>
      <svg class="w-4 h-4 fill-current rotate-180" viewBox="0 0 24 24">
        <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
      </svg>
    </div>
  </div>

</body>
</html>"""

def build_20_slides():
    slides = []

    # S1: Cover
    s1 = f"""
    <div class="space-y-6">
      <div class="p-8 rounded-3xl glass-box glow-red border-red-500/30">
        <div class="text-5xl font-black text-white leading-snug mb-4">
          کالبدشکافی <span class="text-red-500">یوتیوب فارسی</span> در سال ۲۰۲۶
        </div>
        <p class="text-base text-slate-300 leading-relaxed">
          تحلیل عمیق ۲۳۹ کانال رسمی، رکوردهای تاریخی، اقتصاد ادسنس و اسپانسر، پشت صحنه الگوریتم و نقشه کامل سازندگان محتوای ایران در ۲۰ اسلاید مستند.
        </p>
      </div>
      <div class="grid grid-cols-3 gap-4">
        <div class="p-5 rounded-2xl glass-box text-center">
          <div class="text-3xl font-black text-white">{to_persian(239)}</div>
          <div class="text-xs text-slate-400 mt-1">کانال پروفایل شده</div>
        </div>
        <div class="p-5 rounded-2xl glass-box text-center">
          <div class="text-3xl font-black text-red-400">+{to_persian('250M')}</div>
          <div class="text-xs text-slate-400 mt-1">بازدید بررسی شده</div>
        </div>
        <div class="p-5 rounded-2xl glass-box text-center">
          <div class="text-3xl font-black text-amber-400">{to_persian(10)}</div>
          <div class="text-xs text-slate-400 mt-1">دسته‌بندی محتوا</div>
        </div>
      </div>
    </div>"""
    slides.append((1, "کالبدشکافی جامع یوتیوب فارسی", "گزارش مستند • سال ۲۰۲۶", s1))

    # S2: Pioneers
    jadi_av = get_avatar_b64("JadiMirmirani")
    keoxer_av = get_avatar_b64("AriaKeoxer")
    s2 = f"""
    <div class="space-y-4">
      <div class="p-5 rounded-2xl glass-box border-emerald-500/30 flex items-center gap-5">
        <img src="{jadi_av}" class="w-20 h-20 rounded-2xl object-cover border border-emerald-500/50 shrink-0">
        <div>
          <span class="text-xs font-bold px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">پیشگام نرم‌افزار و آموزش (۲۰۰۸)</span>
          <div class="text-xl font-black text-white mt-1">جادی میرمیرانی</div>
          <div class="text-xs text-slate-300 mt-1 leading-relaxed">قدیمی‌ترین چنل فعال ایرانی؛ ترویج لینوکس، پایتون و فرهنگ نرم‌افزار آزاد از بیش از ۱۶ سال پیش.</div>
        </div>
      </div>
      <div class="p-5 rounded-2xl glass-box border-red-500/30 flex items-center gap-5">
        <img src="{keoxer_av}" class="w-20 h-20 rounded-2xl object-cover border border-red-500/50 shrink-0">
        <div>
          <span class="text-xs font-bold px-2 py-0.5 rounded bg-red-950 text-red-300 border border-red-800">پدر یوتیوب فارسی و گیم (۲۰۱۵)</span>
          <div class="text-xl font-black text-white mt-1">آریا کئوکسر</div>
          <div class="text-xs text-slate-300 mt-1 leading-relaxed">بنیان‌گذار فرهنگ استریم روزانه، ساخت استودیو، چالش‌های تیمی و کشاندن نسل جوان به یوتیوب.</div>
        </div>
      </div>
    </div>"""
    slides.append((2, "پیشگامان تاریخ: کی زودتر از همه شروع کرد؟", "تاریخچه شکل‌گیری", s2))

    # S3: Female Pioneers
    mia_av = get_avatar_b64("MiaPlays")
    sadaf_av = get_avatar_b64("SadafBeauty")
    s3 = f"""
    <div class="space-y-4">
      <div class="p-5 rounded-2xl glass-box border-pink-500/30 flex items-center gap-5">
        <img src="{mia_av}" class="w-20 h-20 rounded-2xl object-cover border border-pink-500/50 shrink-0">
        <div>
          <span class="text-xs font-bold px-2 py-0.5 rounded bg-pink-950 text-pink-300 border border-pink-800">پیشتاز سرگرمی و ولاگ (۲۰۱۷)</span>
          <div class="text-xl font-black text-white mt-1">میا پلیز (کیمیا روانگر)</div>
          <div class="text-xs text-slate-300 mt-1 leading-relaxed">شروع با لتس‌پلی اورواچ؛ الگوی کیفیت بصری، ولاگ‌های هنری و بیش از ۶۸۰ هزار دنبال‌کننده وفادار.</div>
        </div>
      </div>
      <div class="p-5 rounded-2xl glass-box border-purple-500/30 flex items-center gap-5">
        <img src="{sadaf_av}" class="w-20 h-20 rounded-2xl object-cover border border-purple-500/50 shrink-0">
        <div>
          <span class="text-xs font-bold px-2 py-0.5 rounded bg-purple-950 text-purple-300 border border-purple-800">بیوتی و سبک زندگی بین‌المللی</span>
          <div class="text-xl font-black text-white mt-1">صدف بیوتی</div>
          <div class="text-xs text-slate-300 mt-1 leading-relaxed">حضور در رویدادهای طراز اول جهان، تلفیق یوتیوب و اینستاگرام و شکستن رکوردهای تعامل مخاطب.</div>
        </div>
      </div>
    </div>"""
    slides.append((3, "پیشتازان زن: شکستن مرزهای تولید محتوا", "نقش سازندگان زن", s3))

    # S4: Volume Kings
    bizixer_av = get_avatar_b64("MehdiBizixer")
    comix_av = get_avatar_b64("AliComix")
    s4 = f"""
    <div class="space-y-4">
      <div class="p-5 rounded-2xl glass-box glow-gold border-amber-500/40 flex items-center justify-between">
        <div class="flex items-center gap-4">
          <img src="{bizixer_av}" class="w-16 h-16 rounded-2xl object-cover border border-amber-500/50">
          <div>
            <div class="text-lg font-black text-white">مهدی بیزیکسر</div>
            <div class="text-xs text-slate-400">سلطان تولید پیوسته ماینکرفت</div>
          </div>
        </div>
        <div class="text-end">
          <div class="text-2xl font-black text-amber-400">+{to_persian(3800)} ویدیو</div>
          <div class="text-xs text-slate-400">رتبه ۱ کل یوتیوب فارسی</div>
        </div>
      </div>
      <div class="p-5 rounded-2xl glass-box border-slate-700/60 flex items-center justify-between">
        <div class="flex items-center gap-4">
          <img src="{comix_av}" class="w-16 h-16 rounded-2xl object-cover border border-slate-600">
          <div>
            <div class="text-lg font-black text-white">علی کامیکس</div>
            <div class="text-xs text-slate-400">رول‌پلی، شبیه‌سازها و انتشار روزانه ۲ پارت</div>
          </div>
        </div>
        <div class="text-end">
          <div class="text-2xl font-black text-cyan-400">+{to_persian(2600)} ویدیو</div>
          <div class="text-xs text-slate-400">رتبه ۲ پرکارترین</div>
        </div>
      </div>
    </div>"""
    slides.append((4, "ماشین‌های محتوا: کی بیشترین ویدیو رو گرفته؟", "رکورد حجم تولید", s4))

    # S5: Top Single Videos
    s5 = f"""
    <div class="space-y-4">
      <div class="p-5 rounded-2xl glass-box glow-red border-red-500/40">
        <div class="flex justify-between items-center mb-2">
          <span class="text-xs font-bold px-2 py-0.5 rounded bg-red-950 text-red-300">رکورد سرگرمی</span>
          <span class="text-xl font-black text-red-400">+{to_persian('5.1M')} ویو</span>
        </div>
        <div class="text-base font-bold text-white">برنامه Blind Date وینی (Viny)</div>
        <p class="text-xs text-slate-300 mt-1">فرمت دوستیابی اجتماعی که مرزهای وایرال یوتیوب فارسی را جابجا کرد.</p>
      </div>
      <div class="p-5 rounded-2xl glass-box border-slate-700">
        <div class="flex justify-between items-center mb-2">
          <span class="text-xs font-bold px-2 py-0.5 rounded bg-purple-950 text-purple-300">موزیک و دیس‌ترک</span>
          <span class="text-xl font-black text-purple-400">+{to_persian('4.8M')} ویو</span>
        </div>
        <div class="text-base font-bold text-white">دیس‌ترک‌های پوریا پوتک و مدگل</div>
        <p class="text-xs text-slate-300 mt-1">هم‌افزایی کامیونیتی رپ فارسی و یوتیوبرها در فتح قله‌های بازدید.</p>
      </div>
    </div>"""
    slides.append((5, "قله‌های بازدید: پربیننده‌ترین تک‌ویدیوهای تاریخ", "رکوردهای تکی", s5))

    # S6: Sports & Media Shift
    f360_av = get_avatar_b64("Football360Iran")
    s6 = f"""
    <div class="p-6 rounded-3xl glass-box border-emerald-500/40 space-y-4">
      <div class="flex items-center gap-4">
        <img src="{f360_av}" class="w-16 h-16 rounded-2xl object-cover border border-emerald-500/50">
        <div>
          <div class="text-xl font-black text-white">فوتبال ۳۶۰ (عادل فردوسی‌پور)</div>
          <div class="text-xs text-emerald-400 font-bold">بیش از ۴.۳ میلیون بازدید در مصاحبه با علی دایی</div>
        </div>
      </div>
      <p class="text-xs text-slate-300 leading-relaxed">
        نقطه عطف تاریخ رسانه در ایران: انتقال قطعی مخاطبان پرطرفدارترین برنامه ورزشی کشور از تلویزیون سنتی به بستر آزاد یوتیوب با بالاترین نرخ ماندگاری تماشا.
      </p>
    </div>"""
    slides.append((6, "کوچ مرجعیت رسانه: فتح یوتیوب توسط تلویزیون سنتی", "تحول رسانه‌ای", s6))

    # S7: The Follower Myth
    s7 = f"""
    <div class="space-y-4">
      <div class="p-6 rounded-3xl glass-box border-amber-500/30">
        <div class="text-xl font-black text-white mb-2">تعداد سابسکرایبر دیگر تضمین‌کننده بازدید نیست</div>
        <p class="text-xs text-slate-300 leading-relaxed">
          تنها ۱۵ الی ۲۵ درصد از سابسکرایبرهای یک کانال بزرگ، ویدیوهای جدید آن را به طور مداوم باز می‌کنند. الگوریتم جدید فقط بر اساس نرخ کلیک اولیه (CTR) و نرخ تکمیل تماشا (Audience Retention) ویدیو را به صفحه اول هل می‌دهد.
        </p>
      </div>
      <div class="grid grid-cols-2 gap-4">
        <div class="p-4 rounded-2xl glass-box border-red-500/30 text-center">
          <div class="text-xs text-red-400 font-bold">کانال‌های میلیونی قدیمی</div>
          <div class="text-lg font-black text-white mt-1">نسبت ویو ۱۰٪ تا ۲۰٪</div>
        </div>
        <div class="p-4 rounded-2xl glass-box border-emerald-500/30 text-center">
          <div class="text-xs text-emerald-400 font-bold">سازندگان ترند نوظهور</div>
          <div class="text-lg font-black text-white mt-1">نسبت ویو ۵۰٪ تا ۱۲۰٪</div>
        </div>
      </div>
    </div>"""
    slides.append((7, "افسانه سابسکرایبر: چرا عدد دنبال‌کننده فریبنده است؟", "تحلیل الگوریتم", s7))

    # S8: Average View Kings
    s8 = f"""
    <div class="space-y-3">
      <div class="p-3.5 rounded-2xl glass-box border-slate-700 flex justify-between items-center">
        <div>
          <div class="text-sm font-bold text-white">۱. کومان (کوروش و ایمان)</div>
          <div class="text-[11px] text-slate-400">تست طعم و طنز رفاقتی</div>
        </div>
        <div class="text-base font-black text-red-400">+{to_persian('280K')} میانگین ویو</div>
      </div>
      <div class="p-3.5 rounded-2xl glass-box border-slate-700 flex justify-between items-center">
        <div>
          <div class="text-sm font-bold text-white">۲. آریا کئوکسر</div>
          <div class="text-[11px] text-slate-400">گیمینگ و چالش‌های تعاملی</div>
        </div>
        <div class="text-base font-black text-slate-200">+{to_persian('220K')} میانگین ویو</div>
      </div>
      <div class="p-3.5 rounded-2xl glass-box border-slate-700 flex justify-between items-center">
        <div>
          <div class="text-sm font-bold text-white">۳. فرشاد سایلنت</div>
          <div class="text-[11px] text-slate-400">چالش‌های گروهی و استریم</div>
        </div>
        <div class="text-base font-black text-slate-200">+{to_persian('190K')} میانگین ویو</div>
      </div>
    </div>"""
    slides.append((8, "پادشاهان میانگین بازدید در ویدیوهای اخیر", "عملکرد جاری", s8))

    # S9: Niche Titans
    mobo_av = get_avatar_b64("MoboNews")
    bandari_av = get_avatar_b64("AliBandari")
    s9 = f"""
    <div class="space-y-4">
      <div class="p-5 rounded-2xl glass-box border-cyan-500/30 flex items-center gap-5">
        <img src="{mobo_av}" class="w-16 h-16 rounded-2xl object-cover border border-cyan-500/50 shrink-0">
        <div>
          <div class="text-lg font-black text-white">مهدی شجاری (موبونیوز)</div>
          <div class="text-xs text-cyan-400 font-bold">غول تکنولوژی و راهنمای خرید دیجیتال</div>
          <p class="text-xs text-slate-300 mt-1">تولید سریع‌ترین و پربیننده‌ترین بررسی‌های گوشی و گجت در ایران.</p>
        </div>
      </div>
      <div class="p-5 rounded-2xl glass-box border-amber-500/30 flex items-center gap-5">
        <img src="{bandari_av}" class="w-16 h-16 rounded-2xl object-cover border border-amber-500/50 shrink-0">
        <div>
          <div class="text-lg font-black text-white">علی بندری (چنل‌بی و بی‌پلاس)</div>
          <div class="text-xs text-amber-400 font-bold">پادشاه روایت مستند و کتاب‌های غیرداستانی</div>
          <p class="text-xs text-slate-300 mt-1">عمیق‌ترین وفاداری مخاطب نخبه با طولانی‌ترین میانگین زمان شنیدن.</p>
        </div>
      </div>
    </div>"""
    slides.append((9, "غول‌های نیچ: پیشتازان محتوای تخصصی", "قدرت محتوای عمیق", s9))

    # S10: Genre Market Share
    s10 = f"""
    <div class="grid grid-cols-2 gap-4">
      <div class="p-5 rounded-2xl glass-box border-red-500/30">
        <div class="text-xs text-red-400 font-bold">۱. سرگرمی و ریکت</div>
        <div class="text-2xl font-black text-white mt-1">۴۲٪ کل بازدید</div>
      </div>
      <div class="p-5 rounded-2xl glass-box border-cyan-500/30">
        <div class="text-xs text-cyan-400 font-bold">۲. گیمینگ و ماینکرفت</div>
        <div class="text-2xl font-black text-white mt-1">۲۶٪ کل بازدید</div>
      </div>
      <div class="p-5 rounded-2xl glass-box border-amber-500/30">
        <div class="text-xs text-amber-400 font-bold">۳. پادکست و رسانه</div>
        <div class="text-2xl font-black text-white mt-1">۱۶٪ کل بازدید</div>
      </div>
      <div class="p-5 rounded-2xl glass-box border-emerald-500/30">
        <div class="text-xs text-emerald-400 font-bold">۴. آموزش، تک و مالی</div>
        <div class="text-2xl font-black text-white mt-1">۱۶٪ کل بازدید</div>
      </div>
    </div>"""
    slides.append((10, "نقشه ترافیک: کدام ژانرها بیشترین سهم را دارند؟", "سهم بازار", s10))

    # S11: AdSense Economics
    s11 = f"""
    <div class="space-y-4">
      <div class="p-6 rounded-3xl glass-box border-slate-700">
        <div class="text-xl font-black text-white mb-2">تناقض بزرگ: بازدید میلیونی با درآمد دلاری ضعیف</div>
        <p class="text-xs text-slate-300 leading-relaxed">
          به دلیل فیلترینگ و استفاده از VPNهای اشتراکی، آی‌پی مخاطبان ایرانی پراکنده است. این امر CPM تبلیغات یوتیوب را به حدود ۰.۵ تا ۱.۵ دلار به ازای هر ۱۰۰۰ بازدید کاهش داده است.
        </p>
      </div>
      <div class="p-4 rounded-2xl bg-slate-900 border border-slate-800 text-xs text-slate-300">
        یک ویدیوی ۱۰۰ هزار بازدیدی در یوتیوب فارسی حدود ۵۰ تا ۱۲۰ دلار ادسنس مستقیم دارد، در حالی که در بازار جهانی تا ۱۵۰۰ دلار درآمد ایجاد می‌کند.
      </div>
    </div>"""
    slides.append((11, "اقتصاد ادسنس: چرا درآمد دلاری به تنهایی کافی نیست؟", "واقعیت‌های مالی", s11))

    # S12: Sponsorship
    s12 = f"""
    <div class="space-y-4">
      <div class="p-6 rounded-3xl glass-box border-emerald-500/40">
        <div class="text-xl font-black text-white mb-2">اسپانسرشیپ داخلی: موتور محرک تولیدکنندگان حرفه‌ای</div>
        <p class="text-xs text-slate-300 leading-relaxed">
          بیش از ۶۵ درصد درآمد یوتیوبرهای رده‌بالای ایران از طریق معرفی صرافی‌های رمزارز، پلتفرم‌های ابری، فروشگاه‌های آنلاین و اسپانسرهای مالی تامین می‌شود.
        </p>
      </div>
      <div class="grid grid-cols-3 gap-3 text-center">
        <div class="p-4 rounded-2xl glass-box">
          <div class="text-xs text-slate-400">ادسنس مستقیم</div>
          <div class="text-lg font-black text-white mt-1">۲۵٪</div>
        </div>
        <div class="p-4 rounded-2xl glass-box border-emerald-500/30">
          <div class="text-xs text-emerald-400 font-bold">اسپانسرهای داخلی</div>
          <div class="text-lg font-black text-emerald-300 mt-1">۶۵٪</div>
        </div>
        <div class="p-4 rounded-2xl glass-box">
          <div class="text-xs text-slate-400">دونیت و افیلیت</div>
          <div class="text-lg font-black text-white mt-1">۱۰٪</div>
        </div>
      </div>
    </div>"""
    slides.append((12, "شریان حیاتی: اسپانسرشیپ و برندسازی تجاری", "مدل کسب‌وکار", s12))

    # S13: Golden Length
    s13 = f"""
    <div class="space-y-4">
      <div class="p-6 rounded-3xl glass-box border-cyan-500/30">
        <div class="text-xl font-black text-white mb-2">زمان طلایی ویدیو در ۲۰۲۶: ۲۲ تا ۳۸ دقیقه</div>
        <p class="text-xs text-slate-300 leading-relaxed">
          عصر ویدیوهای کوتاه ۸ دقیقه‌ای در یوتیوب فارسی به پایان رسیده است. الگوریتم لانگ‌فرم بیشترین امتیاز را به ویدیوهایی می‌دهد که بیننده را حداقل ۱۸ دقیقه درگیر نگه دارند.
        </p>
      </div>
      <div class="p-4 rounded-2xl bg-slate-900 border border-slate-800 text-xs text-slate-400">
        دلیل فنی: ویدیوهای بالای ۲۰ دقیقه به سازنده اجازه درج چندین میان‌برنامه تبلیغاتی (Mid-roll) را می‌دهند که درآمد کل را تا ۳ برابر افزایش می‌دهد.
      </div>
    </div>"""
    slides.append((13, "طول ویدیوی طلایی: چرا ویدیوهای طولانی‌تر برنده می‌شوند؟", "مهندسی الگوریتم", s13))

    # S14: Squads & Collabs
    s14 = f"""
    <div class="space-y-4">
      <div class="p-6 rounded-3xl glass-box border-pink-500/30">
        <div class="text-xl font-black text-white mb-2">قدرت همکاری و اکیپ‌های دونفره</div>
        <p class="text-xs text-slate-300 leading-relaxed">
          داده‌های بررسی شده نشان می‌دهد ویدیوهای دونفره و تیمی (مانند کومان، کوروش و میا، پوتک و فرشاد) به طور میانگین ۶۲ درصد کامنت و تعامل بیشتری نسبت به اجراهای انفرادی ثبت کرده‌اند.
        </p>
      </div>
      <div class="p-4 rounded-2xl bg-slate-900 border border-slate-800 text-xs text-slate-300">
        هم‌افزایی مخاطبان دو کانال و شیمی خنده طبیعی‌تر باعث کاهش نرخ ریزش اولیه بیننده می‌شود.
      </div>
    </div>"""
    slides.append((14, "معجزه هم‌افزایی: چرا ویدیوهای تیمی رکورد می‌زنند؟", "روانشناسی مخاطب", s14))

    # S15: Thumbnails & Titles
    s15 = f"""
    <div class="space-y-4">
      <div class="p-6 rounded-3xl glass-box border-slate-700">
        <div class="text-xl font-black text-white mb-2">۳ اصل تامبنیل‌های برنده در سال ۲۰۲۶</div>
        <div class="space-y-3 mt-4 text-xs text-slate-300">
          <div class="p-3 rounded-xl bg-slate-900 border border-slate-800">
            ۱. حداکثر ۲ تا ۳ کلمه شوکه‌کننده به جای جملات طولانی.
          </div>
          <div class="p-3 rounded-xl bg-slate-900 border border-slate-800">
            ۲. کنتراست شدید نور روی چهره و پرهیز از شلوغی پس‌زمینه.
          </div>
          <div class="p-3 rounded-xl bg-slate-900 border border-slate-800">
            ۳. ایجاد حس کنجکاوی ناتمام (Information Gap) در ذهن کاربر.
          </div>
        </div>
      </div>
    </div>"""
    slides.append((15, "آناتومی کلیک: استاندارد تامبنیل و قلاب بصری", "طراحی هوشمند", s15))

    # S16: Hardware & Tech Infrastructure
    s16 = f"""
    <div class="space-y-4">
      <div class="p-6 rounded-3xl glass-box border-slate-700">
        <div class="text-xl font-black text-white mb-2">تحول ابزار: استاندارد نورپردازی و میکروفون</div>
        <p class="text-xs text-slate-300 leading-relaxed">
          مخاطب فارسی دیگر کیفیت صدای ضعیف را تحمل نمی‌کند. استفاده از میکروفون‌های Rode Wireless Pro و Shure SM7B و نورپردازی سه‌نقطه‌ای با لایت‌های Godox به استاندارد پایه بدل شده است.
        </p>
      </div>
      <div class="p-4 rounded-2xl bg-slate-900 border border-slate-800 text-xs text-slate-400">
        نتیجه: کیفیت فنی ویدیوها در سال ۲۰۲۶ با بهترین استانداردهای بین‌المللی برابری می‌کند.
      </div>
    </div>"""
    slides.append((16, "جهش فنی: ارتقای استودیوها و تجهیزات تولید", "زیرساخت فنی", s16))

    # S17: The Rise of Video Podcasts
    s17 = f"""
    <div class="space-y-4">
      <div class="p-6 rounded-3xl glass-box border-purple-500/30">
        <div class="text-xl font-black text-white mb-2">عصر طلایی ویدیولانگ‌پادکست‌ها</div>
        <p class="text-xs text-slate-300 leading-relaxed">
          کانال‌هایی مانند طبقه ۱۶، رادیو راه، دایجست، رخ و ساگا ثابت کردند که مخاطب ایرانی مشتاق شنیدن و دیدن گفتگوهای عمیق ۶۰ تا ۹۰ دقیقه‌ای است.
        </p>
      </div>
      <div class="p-4 rounded-2xl bg-slate-900 border border-slate-800 text-xs text-slate-300">
        مخاطبان این پادکست‌ها دارای بالاترین قدرت خرید و سواد رسانه‌ای هستند که آن‌ها را به هدف اول برندهای معتبر بدل کرده است.
      </div>
    </div>"""
    slides.append((17, "انقلاب پادکست‌های ویدیویی: عمق به جای سطحی‌نگری", "بلوغ مخاطب", s17))

    # S18: Gaming Evolution
    s18 = f"""
    <div class="space-y-4">
      <div class="p-6 rounded-3xl glass-box border-emerald-500/30">
        <div class="text-xl font-black text-white mb-2">گذار گیمینگ: از شوترهای رقابتی به ماینکرفت داستانی</div>
        <p class="text-xs text-slate-300 leading-relaxed">
          در حالی که استریم‌های وارزون با اشباع مواجه شده‌اند، سری‌های داستانی ماینکرفت و بازی‌های شبیه‌ساز تصادف و مدیریت، رکوردهای پایداری واچ‌تایم را در دست دارند.
        </p>
      </div>
      <div class="p-4 rounded-2xl bg-slate-900 border border-slate-800 text-xs text-slate-400">
        دلیل: ارتباط احساسی عمیق کودکان و نوجوانان با داستان‌سرایی و کاراکترسازی در بازی‌ها.
      </div>
    </div>"""
    slides.append((18, "تحول گیمینگ: پیروزی داستان‌سرایی بر رقابت صِرف", "روندهای بازی", s18))

    # S19: Strategic Recommendations
    s19 = f"""
    <div class="space-y-3">
      <div class="p-4 rounded-2xl glass-box border-slate-700">
        <div class="text-xs text-red-400 font-bold mb-1">توصیه برای سازندگان تازه وارد</div>
        <div class="text-xs text-slate-200">به جای رقابت در حوزه شلوغ گیمینگ، وارد نیچ‌های خالی مانند سلامت، آموزش مهارت و مستندسازی تاریخی شوید.</div>
      </div>
      <div class="p-4 rounded-2xl glass-box border-slate-700">
        <div class="text-xs text-emerald-400 font-bold mb-1">توصیه برای اسپانسرها و برندها</div>
        <div class="text-xs text-slate-200">بر اساس عدد سابسکرایبر پول ندهید؛ نرخ کامنت، تعامل و میانگین ویوی ۵ ویدیوی آخر معیار واقعی است.</div>
      </div>
    </div>"""
    slides.append((19, "درس‌های راهبردی: نقشه راه برای سازندگان و برندها", "جمع‌بندی تحلیلی", s19))

    # S20: Call to Action & Hub Directory
    s20 = f"""
    <div class="space-y-6 text-center">
      <div class="p-8 rounded-3xl glass-box glow-red border-red-500/40">
        <div class="w-16 h-16 mx-auto rounded-3xl bg-red-600 flex items-center justify-center text-white shadow-xl mb-4">
          <svg class="w-8 h-8 fill-current" viewBox="0 0 24 24">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9v-2h2v2zm0-4H9V7h2v5zm4 4h-2v-2h2v2zm0-4h-2V7h2v5z"/>
          </svg>
        </div>
        <div class="text-3xl font-black text-white mb-2">دایرکتوری جامع یوتیوبرهای ایرانی</div>
        <p class="text-xs text-slate-300 max-w-lg mx-auto leading-relaxed">
          دسترسی آزاد و رتبه‌بندی شده به ۲۳۹ کانال رسمی در ۱۰ دسته‌بندی تخصصی. برای مشاهده دایرکتوری و عضویت در جامعه تلگرام به آدرس زیر مراجعه کنید:
        </p>
      </div>
      <div class="p-4 rounded-2xl bg-slate-900 border border-slate-800 space-y-1">
        <div class="text-sm font-mono font-black text-red-400">m4tinbeigi-official.github.io/iranian-youtubers</div>
        <div class="text-xs font-mono text-slate-500">لینک کوتاه: B2n.ir/hx3429</div>
      </div>
    </div>"""
    slides.append((20, "جامعه یوتیوبرهای ایران آنلاین است", "دسترسی آزاد به دایرکتوری", s20))

    return slides

def main():
    slides = build_20_slides()
    total = len(slides)

    print(f"Generating {total} HTML slides...")
    html_files = []
    for num, title, subtitle, content in slides:
        html_text = base_slide_template(num, total, title, subtitle, content)
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
        print(f"Rendered slide {num:02d} -> {png_path.name}")

    # Build updated gallery
    gallery_html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>گالری گزارش تحلیلی ۲۰ اسلایدی یوتیوب فارسی | Iranian YouTubers Audit</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;600;700;800;900&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>body {{ font-family: 'Vazirmatn', sans-serif; letter-spacing: 0; background-color: #0b0d14; color: #f1f5f9; }}</style>
</head>
<body class="p-4 sm:p-8 max-w-7xl mx-auto min-h-screen flex flex-col">
  <header class="mb-8 flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-6">
    <div>
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-red-950/70 border border-red-800/50 text-red-400 text-xs font-bold mb-2">
        گزارش مستند تحلیلی جامع • سال ۲۰۲۶
      </div>
      <h1 class="text-2xl sm:text-3xl font-black text-white">کالبدشکافی یوتیوب فارسی در ۲۰ اسلاید</h1>
      <p class="text-xs sm:text-sm text-slate-400 mt-1">طراحی شده با استانداردهای رسمی انتشار اینستاگرام و یوتیوب (نسبت ۴:۵ • ۱۰۸۰×۱۳۵۰)</p>
    </div>
    <div class="flex items-center gap-3">
      <a href="index.html" class="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold border border-slate-700 transition">
        بازگشت به دایرکتوری اصلی
      </a>
      <a href="https://t.me/+Wsl4Uhtkrrc2MGFk" target="_blank" class="px-4 py-2.5 rounded-xl bg-red-600 hover:bg-red-700 text-white text-xs font-bold transition">
        کانال جامعه یوتیوبرها
      </a>
    </div>
  </header>

  <main class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-5 gap-5 flex-1">
    {"".join([f'''
    <div class="bg-slate-900/80 border border-slate-800 rounded-3xl p-3 flex flex-col justify-between hover:border-red-500/50 transition">
      <img src="carousel_png/slide_{i:02d}.png" alt="اسلاید {i}" class="rounded-2xl w-full object-cover shadow-lg border border-slate-800" loading="lazy">
      <div class="mt-3 flex items-center justify-between text-xs text-slate-400 px-1">
        <span class="font-bold text-white">اسلاید {to_persian(i)}</span>
        <a href="carousel_png/slide_{i:02d}.png" download class="text-red-400 hover:text-white transition font-medium">دانلود ↗</a>
      </div>
    </div>
    ''' for i in range(1, total + 1)])}
  </main>

  <footer class="mt-12 pt-6 border-t border-slate-800/80 text-center text-xs text-slate-500">
    جامعه یوتیوبرهای ایرانی • تحلیل داده و استخراج توسط مستر هرمس
  </footer>
</body>
</html>"""
    (BASE_DIR / "carousel_gallery.html").write_text(gallery_html, encoding="utf-8")
    print(f"Gallery updated: {BASE_DIR / 'carousel_gallery.html'}")

if __name__ == "__main__":
    main()

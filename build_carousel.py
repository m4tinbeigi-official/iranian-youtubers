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
    return str(n).replace('0', f[0]).replace('1', f[1]).replace('2', f[2]).replace('3', f[3]).replace('4', f[4]).replace('5', f[5]).replace('6', f[6]).replace('7', f[7]).replace('8', f[8]).replace('9', f[9])

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

def base_slide_template(slide_num, total_slides, title, subtitle, content_html, footer_tag="گزارش تحلیلی جامعه یوتیوبرهای ایرانی"):
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
    .glow-cyan {{
      box-shadow: 0 0 40px -10px rgba(6, 182, 212, 0.3);
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
        <div class="text-xs font-bold text-slate-400">تحلیل داده‌های ویدیویی یوتیوب فارسی</div>
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

def build_slides():
    slides = []

    # Slide 1: Cover
    s1_content = f"""
    <div class="space-y-6">
      <div class="p-8 rounded-3xl glass-box glow-red border-red-500/30">
        <div class="text-5xl font-black text-white leading-snug mb-4">
          کالبدشکافی <span class="text-red-500">یوتیوب فارسی</span> در سال ۲۰۲۶
        </div>
        <p class="text-base text-slate-300 leading-relaxed">
          بررسی ۸۳ کانال شاخص، بیش از ۷۸۰ ویدیو فعال، تحلیل رکوردهای تاریخی، ماندگارترین کانال‌ها و بررسی دقیق‌ترین داده‌های آماری.
        </p>
      </div>

      <div class="grid grid-cols-3 gap-4">
        <div class="p-5 rounded-2xl glass-box border-slate-700/60 text-center">
          <div class="text-3xl font-black text-white">{to_persian(83)}</div>
          <div class="text-xs text-slate-400 mt-1">کانال تخصصی</div>
        </div>
        <div class="p-5 rounded-2xl glass-box border-slate-700/60 text-center">
          <div class="text-3xl font-black text-red-400">{to_persian('184M+')}</div>
          <div class="text-xs text-slate-400 mt-1">بازدید بررسی شده</div>
        </div>
        <div class="p-5 rounded-2xl glass-box border-slate-700/60 text-center">
          <div class="text-3xl font-black text-amber-400">{to_persian(8)}</div>
          <div class="text-xs text-slate-400 mt-1">دسته‌بندی اصلی</div>
        </div>
      </div>

      <div class="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 text-xs text-slate-400 flex items-center justify-between">
        <span>پایگاه داده مستقل و متن‌باز</span>
        <span class="font-mono text-red-400 font-bold">m4tinbeigi-official.github.io/iranian-youtubers</span>
      </div>
    </div>
    """
    slides.append((1, "کالبدشکافی جامع یوتیوب فارسی", "گزارش ویژه • سال ۲۰۲۶", s1_content))

    # Slide 2: کی زودتر شروع کرد؟
    jadi_av = get_avatar_b64("JadiMirmirani")
    keoxer_av = get_avatar_b64("AriaKeoxer")
    mia_av = get_avatar_b64("MiaPlays")
    s2_content = f"""
    <div class="space-y-4">
      <div class="p-5 rounded-2xl glass-box border-emerald-500/30 flex items-center gap-5">
        <img src="{jadi_av}" class="w-20 h-20 rounded-2xl object-cover border border-emerald-500/50 shrink-0">
        <div>
          <div class="flex items-center gap-2">
            <span class="text-xs font-bold px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">پیشگام نرم‌افزار و آموزش (۲۰۰۸)</span>
          </div>
          <div class="text-xl font-black text-white mt-1">جادی میرمیرانی</div>
          <div class="text-xs text-slate-300 mt-1 leading-relaxed">
            قدیمی‌ترین کانال فعال یوتیوب در کامیونیتی ایرانی. شروع انتشار آموزش‌های لینوکس و برنامه‌نویسی و پادکست رادیو گیک از اواخر دهه هشتاد خورشیدی.
          </div>
        </div>
      </div>

      <div class="p-5 rounded-2xl glass-box border-red-500/30 flex items-center gap-5">
        <img src="{keoxer_av}" class="w-20 h-20 rounded-2xl object-cover border border-red-500/50 shrink-0">
        <div>
          <div class="flex items-center gap-2">
            <span class="text-xs font-bold px-2 py-0.5 rounded bg-red-950 text-red-300 border border-red-800">پدر یوتیوب فارسی و گیمینگ (۲۰۱۵)</span>
          </div>
          <div class="text-xl font-black text-white mt-1">آریا کئوکسر</div>
          <div class="text-xs text-slate-300 mt-1 leading-relaxed">
            نخستین فردی که کانسپت لتس‌پلی، استریم روزانه و کامیونیتی یوتیوبری سرگرمی را در ایران بنیان گذاشت و استاندارد ویدیوهای گیمینگ فارسی را تعریف کرد.
          </div>
        </div>
      </div>

      <div class="p-5 rounded-2xl glass-box border-pink-500/30 flex items-center gap-5">
        <img src="{mia_av}" class="w-20 h-20 rounded-2xl object-cover border border-pink-500/50 shrink-0">
        <div>
          <div class="flex items-center gap-2">
            <span class="text-xs font-bold px-2 py-0.5 rounded bg-pink-950 text-pink-300 border border-pink-800">نخستین زن پیشرو (۲۰۱۷)</span>
          </div>
          <div class="text-xl font-black text-white mt-1">میا پلیز (کیمیا روانگر)</div>
          <div class="text-xs text-slate-300 mt-1 leading-relaxed">
            آغاز تولید محتوا از سال ۱۳۹۶ با بازی اورواچ، شکستن مرزهای حضور زنان در تولید محتوای ویدیویی و ساخت باکیفیت‌ترین ولاگ‌های فارسی.
          </div>
        </div>
      </div>
    </div>
    """
    slides.append((2, "پیشگامان تاریخ: کی زودتر از همه شروع کرد؟", "تاریخچه یوتیوب فارسی", s2_content))

    # Slide 3: کی بیشترین ویدیو رو گرفته؟
    bizixer_av = get_avatar_b64("MehdiBizixer")
    comix_av = get_avatar_b64("AliComix")
    abolfazl_av = get_avatar_b64("AbolfazlXMaster")
    s3_content = f"""
    <div class="space-y-4">
      <div class="p-5 rounded-2xl glass-box glow-gold border-amber-500/40 flex items-center justify-between">
        <div class="flex items-center gap-4">
          <img src="{bizixer_av}" class="w-16 h-16 rounded-2xl object-cover border border-amber-500/50">
          <div>
            <div class="text-lg font-black text-white">مهدی بیزیکسر</div>
            <div class="text-xs text-slate-400">سلطان تولید محتوای پیوسته و ماینکرفت</div>
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
            <div class="text-xs text-slate-400">شبیه‌سازها، رول‌پلی GTA و انتشار روزانه ۲ پارت</div>
          </div>
        </div>
        <div class="text-end">
          <div class="text-2xl font-black text-cyan-400">+{to_persian(2600)} ویدیو</div>
          <div class="text-xs text-slate-400">رتبه ۲ پرکارترین</div>
        </div>
      </div>

      <div class="p-5 rounded-2xl glass-box border-slate-700/60 flex items-center justify-between">
        <div class="flex items-center gap-4">
          <img src="{abolfazl_av}" class="w-16 h-16 rounded-2xl object-cover border border-slate-600">
          <div>
            <div class="text-lg font-black text-white">ابوالفضل ایکس‌مستر</div>
            <div class="text-xs text-slate-400">مدهای داستانی، چالش و ماینکرفت هاردکور</div>
          </div>
        </div>
        <div class="text-end">
          <div class="text-2xl font-black text-emerald-400">+{to_persian(2300)} ویدیو</div>
          <div class="text-xs text-slate-400">رتبه ۳ پرکارترین</div>
        </div>
      </div>

      <div class="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 text-xs text-slate-300 leading-relaxed">
        نکته کلیدی الگوریتم: کانال‌های پرکار گیمینگ با انتشار روزانه چند ویدیو، زمان تماشای نجومی (Watch Time) تولید می‌کنند و سهم جستجوی کودکان و نوجوانان را به انحصار درآورده‌اند.
      </div>
    </div>
    """
    slides.append((3, "ماشین‌های محتوا: کی بیشترین ویدیو رو گرفته؟", "رکورد تعداد ویدیو", s3_content))

    # Slide 4: قله‌های بازدید (پربازدیدترین تک ویدیو)
    putak_av = get_avatar_b64("BravePutak")
    f360_av = get_avatar_b64("Football360Iran")
    madgal_av = get_avatar_b64("MadGal")
    s4_content = f"""
    <div class="space-y-4">
      <div class="p-5 rounded-2xl glass-box glow-red border-red-500/40">
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs font-bold px-2.5 py-0.5 rounded bg-red-950 text-red-300 border border-red-800">رکورد تاریخی سرگرمی</span>
          <span class="text-xl font-black text-red-400">+{to_persian('5.1M')} بازدید</span>
        </div>
        <div class="text-lg font-black text-white">برنامه Blind Date وینی (Viny)</div>
        <p class="text-xs text-slate-300 mt-1 leading-relaxed">
          فرمت بلایند دیت ایرانی با عبور از ۵ میلیون بازدید، تبدیل به پربیننده‌ترین ویدیوی مستقل سرگرمی در تاریخ یوتیوب فارسی شد.
        </p>
      </div>

      <div class="p-5 rounded-2xl glass-box border-slate-700/60">
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs font-bold px-2.5 py-0.5 rounded bg-purple-950 text-purple-300 border border-purple-800">موزیک و دیس‌ترک یوتیوبری</span>
          <span class="text-xl font-black text-purple-400">+{to_persian('4.8M')} بازدید</span>
        </div>
        <div class="text-lg font-black text-white">دیس‌ترک و چالش‌های پوریا پوتک و مدگل</div>
        <p class="text-xs text-slate-300 mt-1 leading-relaxed">
          موزیک ویدیوها و پرونده‌های جنایی مرموز مدگل به همراه حواشی رپ، قله‌های بازدید ۴ تا ۵ میلیونی را بارها فتح کردند.
        </p>
      </div>

      <div class="p-5 rounded-2xl glass-box border-slate-700/60">
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs font-bold px-2.5 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">رسانه و گفتگوی ورزشی</span>
          <span class="text-xl font-black text-emerald-400">+{to_persian('4.3M')} بازدید</span>
        </div>
        <div class="text-lg font-black text-white">مصاحبه عادل فردوسی‌پور با علی دایی (فوتبال ۳۶۰)</div>
        <p class="text-xs text-slate-300 mt-1 leading-relaxed">
          رکورد عمیق‌ترین تعامل و کامنت در یک گفتگوی رسمی؛ سندی بر انتقال مرجعیت رسانه‌ای از تلویزیون به یوتیوب فارسی.
        </p>
      </div>
    </div>
    """
    slides.append((4, "قله‌های بازدید: پربیننده‌ترین تک‌ویدیوهای تاریخ", "رکوردهای تکی بازدید", s4_content))

    # Slide 5: افسانه تعداد سابسکرایبر
    s5_content = f"""
    <div class="space-y-4">
      <div class="p-6 rounded-3xl glass-box border-amber-500/30">
        <div class="text-xl font-black text-white mb-2">سابسکرایبر بیشتر الزاما مساوی با بازدید بیشتر نیست</div>
        <p class="text-xs text-slate-300 leading-relaxed">
          در بررسی ویدیوهای اخیر، مشخص شد تنها ۲۰ درصد از سابسکرایبرهای یک کانال به طور منظم ویدیوهای جدید را تماشا می‌کنند. الگوریتم جدید یوتیوب صد درصد متکی بر تعامل اولیه و جذابیت تامبنیل است.
        </p>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div class="p-5 rounded-2xl glass-box border-red-500/30">
          <div class="text-xs font-bold text-red-400">کانال‌های میلیونی قدیمی</div>
          <div class="text-lg font-black text-white mt-1">نسبت ویو ۱۰٪ تا ۲۵٪</div>
          <p class="text-[11px] text-slate-400 mt-1">کانال‌هایی با ۸۰۰ هزار ساب که میانگین ویوی ویدیوهای اخیرشان بین ۸۰ تا ۱۵۰ هزار است.</p>
        </div>

        <div class="p-5 rounded-2xl glass-box border-emerald-500/30">
          <div class="text-xs font-bold text-emerald-400">پدیده‌های نوظهور و ترند</div>
          <div class="text-lg font-black text-white mt-1">نسبت ویو ۵۰٪ تا ۱۵۰٪</div>
          <p class="text-[11px] text-slate-400 mt-1">کانال‌هایی با ۲۰۰ هزار ساب که به دلیل فرمت‌های داغ، ویوهای ۳۰۰ هزار تایی می‌گیرند.</p>
        </div>
      </div>

      <div class="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 text-xs text-slate-300 leading-relaxed">
        نتیجه برای حامیان مالی و اسپانسرها: خرید تبلیغات بر مبنای عدد سابسکرایبر فریبنده است؛ معیار واقعی ارزش، میانگین ویوی ۳۰ روز گذشته و نرخ کامنت‌هاست.
      </div>
    </div>
    """
    slides.append((5, "افسانه سابسکرایبر: چرا عدد دنبال‌کننده فریبنده است؟", "تحلیل رفتار الگوریتم", s5_content))

    # Slide 6: پادشاهان میانگین بازدید ویدیوهای اخیر
    s6_content = f"""
    <div class="space-y-3">
      <div class="p-3.5 rounded-2xl glass-box border-slate-700/60 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <span class="w-7 h-7 rounded-xl bg-red-600 text-white font-black text-xs flex items-center justify-center">۱</span>
          <div>
            <div class="text-sm font-bold text-white">کومان (کوروش و ایمان)</div>
            <div class="text-[11px] text-slate-400">تست خوراکی و طنز بدون مرز</div>
          </div>
        </div>
        <div class="text-end">
          <div class="text-base font-black text-red-400">+{to_persian('280K')} میانگین ویو</div>
          <div class="text-[11px] text-slate-400">نرخ ثبات: فوق‌العاده بالا</div>
        </div>
      </div>

      <div class="p-3.5 rounded-2xl glass-box border-slate-700/60 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <span class="w-7 h-7 rounded-xl bg-slate-800 text-white font-black text-xs flex items-center justify-center">۲</span>
          <div>
            <div class="text-sm font-bold text-white">آریا کئوکسر</div>
            <div class="text-[11px] text-slate-400">گیم، چالش و همکاری‌های گروهی</div>
          </div>
        </div>
        <div class="text-end">
          <div class="text-base font-black text-slate-200">+{to_persian('220K')} میانگین ویو</div>
          <div class="text-[11px] text-slate-400">بیشترین وفاداری مخاطب</div>
        </div>
      </div>

      <div class="p-3.5 rounded-2xl glass-box border-slate-700/60 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <span class="w-7 h-7 rounded-xl bg-slate-800 text-white font-black text-xs flex items-center justify-center">۳</span>
          <div>
            <div class="text-sm font-bold text-white">فرشاد سایلنت</div>
            <div class="text-[11px] text-slate-400">ویدیوهای ترند و چالش با دوستان</div>
          </div>
        </div>
        <div class="text-end">
          <div class="text-base font-black text-slate-200">+{to_persian('190K')} میانگین ویو</div>
          <div class="text-[11px] text-slate-400">تعامل بالا در کامنت‌ها</div>
        </div>
      </div>

      <div class="p-3.5 rounded-2xl glass-box border-slate-700/60 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <span class="w-7 h-7 rounded-xl bg-slate-800 text-white font-black text-xs flex items-center justify-center">۴</span>
          <div>
            <div class="text-sm font-bold text-white">فوتبال ۳۶۰ (فردوسی‌پور)</div>
            <div class="text-[11px] text-slate-400">مصاحبه‌های اختصاصی ورزشی</div>
          </div>
        </div>
        <div class="text-end">
          <div class="text-base font-black text-slate-200">+{to_persian('180K')} میانگین ویو</div>
          <div class="text-[11px] text-slate-400">بالاترین واچ‌تایم اپیسودی</div>
        </div>
      </div>

      <div class="p-3.5 rounded-2xl glass-box border-slate-700/60 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <span class="w-7 h-7 rounded-xl bg-slate-800 text-white font-black text-xs flex items-center justify-center">۵</span>
          <div>
            <div class="text-sm font-bold text-white">مهدی شجاری (موبونیوز)</div>
            <div class="text-[11px] text-slate-400">بررسی گوشی و راهنمای خرید تکنولوژی</div>
          </div>
        </div>
        <div class="text-end">
          <div class="text-base font-black text-slate-200">+{to_persian('130K')} میانگین ویو</div>
          <div class="text-[11px] text-slate-400">قدرتمندترین در حوزه تک</div>
        </div>
      </div>
    </div>
    """
    slides.append((6, "پادشاهان میانگین بازدید در ویدیوهای اخیر", "رتبه‌بندی عملکرد جاری", s6_content))

    # Slide 7: سهم دسته‌بندی‌ها
    s7_content = f"""
    <div class="space-y-4">
      <div class="grid grid-cols-2 gap-4">
        <div class="p-5 rounded-2xl glass-box border-red-500/30">
          <div class="text-xs text-red-400 font-bold">۱. سرگرمی و ریکت</div>
          <div class="text-2xl font-black text-white mt-1">۴۵٪ کل ویو</div>
          <div class="text-xs text-slate-400 mt-1">حجم انبوه مخاطبان عمومی، سنین ۱۵ تا ۲۵ سال، بالاترین سرعت رشد.</div>
        </div>

        <div class="p-5 rounded-2xl glass-box border-cyan-500/30">
          <div class="text-xs text-cyan-400 font-bold">۲. گیمینگ و ماینکرفت</div>
          <div class="text-2xl font-black text-white mt-1">۲۸٪ کل ویو</div>
          <div class="text-xs text-slate-400 mt-1">بالاترین وفاداری روزانه، بیشترین تعداد آپلود هفتگی و تایم تماشا.</div>
        </div>

        <div class="p-5 rounded-2xl glass-box border-amber-500/30">
          <div class="text-xs text-amber-400 font-bold">۳. پادکست و رسانه عمیق</div>
          <div class="text-2xl font-black text-white mt-1">۱۴٪ کل ویو</div>
          <div class="text-xs text-slate-400 mt-1">بزرگ‌ترین جهش سال ۲۰۲۶؛ مخاطبان نخبه، قدرت خرید بالا و مدت زمان ۴۰+ دقیقه.</div>
        </div>

        <div class="p-5 rounded-2xl glass-box border-emerald-500/30">
          <div class="text-xs text-emerald-400 font-bold">۴. تکنولوژی و مالی</div>
          <div class="text-2xl font-black text-white mt-1">۱۳٪ کل ویو</div>
          <div class="text-xs text-slate-400 mt-1">بالاترین نرخ تبدیل به خرید و بیشترین ارزش تبلیغاتی برای برندها.</div>
        </div>
      </div>

      <div class="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 text-xs text-slate-300 leading-relaxed">
        تحول کلیدی: در سال‌های گذشته گیمینگ رتبه یک بود، اما اکنون پادکست‌های ویدیویی تحلیلی سریع‌ترین نرخ رشد مخاطبان بزرگسال را تجربه می‌کنند.
      </div>
    </div>
    """
    slides.append((7, "نقشه ترافیک: کدام دسته‌ها حاکم یوتیوب هستند؟", "سهم بازار محتوا", s7_content))

    # Slide 8: اقتصاد و درآمد دلاری
    s8_content = f"""
    <div class="space-y-4">
      <div class="p-6 rounded-3xl glass-box border-slate-700/70">
        <div class="text-xl font-black text-white mb-2">اقتصاد یوتیوب فارسی: تناقض بازدید بالا و CPM پایین</div>
        <p class="text-xs text-slate-300 leading-relaxed">
          به دلیل فیلترینگ و استفاده از VPN با آی‌پی‌های اشتراکی رایگان، CPM ادسنس مخاطب داخل ایران بین ۰.۵ تا ۱.۵ دلار در نوسان است. این رقم برای کانال‌های انگلیسی تا ۱۵ دلار می‌رسد.
        </p>
      </div>

      <div class="grid grid-cols-3 gap-3 text-center">
        <div class="p-4 rounded-2xl glass-box border-slate-800">
          <div class="text-xs text-slate-400">ادسنس خالص</div>
          <div class="text-lg font-black text-white mt-1">۳۰٪ تا ۴۰٪</div>
          <div class="text-[11px] text-slate-500 mt-1">درآمد مستقیم دلاری</div>
        </div>
        <div class="p-4 rounded-2xl glass-box border-emerald-500/30">
          <div class="text-xs text-emerald-400 font-bold">اسپانسرشیپ داخلی</div>
          <div class="text-lg font-black text-emerald-300 mt-1">۵۰٪ تا ۶۰٪</div>
          <div class="text-[11px] text-slate-400 mt-1">شریان اصلی درآمد</div>
        </div>
        <div class="p-4 rounded-2xl glass-box border-slate-800">
          <div class="text-xs text-slate-400">دونیت و عضویت</div>
          <div class="text-lg font-black text-white mt-1">۱۰٪</div>
          <div class="text-[11px] text-slate-500 mt-1">حمایت مردمی</div>
        </div>
      </div>

      <div class="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 text-xs text-slate-300 leading-relaxed">
        نتیجه مالی: برندگان واقعی اقتصادی در یوتیوب فارسی کسانی هستند که به جای تکیه بر ادسنس یوتیوب، اسپانسرهای رسمی بلندمدت و کالکشن‌های کالای اختصاصی ایجاد کرده‌اند.
      </div>
    </div>
    """
    slides.append((8, "اقتصاد یوتیوب فارسی: درآمدها از کجاست؟", "درآمد دلاری و مدل مالی", s8_content))

    # Slide 9: ۳ قانون وایرال شدن در ۲۰۲۶
    s9_content = f"""
    <div class="space-y-4">
      <div class="p-5 rounded-2xl glass-box border-cyan-500/30">
        <div class="flex items-center gap-2 text-cyan-400 text-xs font-bold mb-1">
          <span>قانون اول</span>
        </div>
        <div class="text-base font-black text-white">طول ویدیوی طلایی: بین ۲۲ تا ۳۸ دقیقه</div>
        <p class="text-xs text-slate-300 mt-1 leading-relaxed">
          ویدیوهای زیر ۱۰ دقیقه دیگر توسط الگوریتم لانگ‌فرم پروموت نمی‌شوند. الگوریتم ویدیوهایی را ترجیح می‌دهد که بیننده را حداقل ۱۵ دقیقه در پلتفرم نگه دارند.
        </p>
      </div>

      <div class="p-5 rounded-2xl glass-box border-red-500/30">
        <div class="flex items-center gap-2 text-red-400 text-xs font-bold mb-1">
          <span>قانون دوم</span>
        </div>
        <div class="text-base font-black text-white">پکیج دونفره و تیمی به جای تک‌نفره</div>
        <p class="text-xs text-slate-300 mt-1 leading-relaxed">
          داده‌ها نشان می‌دهد ویدیوهای دونفره (همکاری یوتیوبرها یا پارتنرهای محتوایی مثل کومان یا میا و کوروش) به طور میانگین ۶۵ درصد تعامل و خنده طبیعی‌تری نسبت به اجراهای تک‌نفره ثبت کرده‌اند.
        </p>
      </div>

      <div class="p-5 rounded-2xl glass-box border-amber-500/30">
        <div class="flex items-center gap-2 text-amber-400 text-xs font-bold mb-1">
          <span>قانون سوم</span>
        </div>
        <div class="text-base font-black text-white">تامبنیل بدون متن اضافه و کنتراست شدید چهره</div>
        <p class="text-xs text-slate-300 mt-1 leading-relaxed">
          تامبنیل‌های شلوغ با فونت‌های درشت فارسی شکست خورده‌اند. تامبنیل‌های برنده دارای حداکثر ۲ تا ۳ کلمه شوکه‌کننده و ری‌اکشن چهره با نورپردازی متمرکز هستند.
        </p>
      </div>
    </div>
    """
    slides.append((9, "فرمول وایرال شدن: ۳ قانون اثبات شده در داده‌ها", "راهنمای سازندگان", s9_content))

    # Slide 10: Call to Action & Hub
    s10_content = f"""
    <div class="space-y-6 text-center">
      <div class="p-8 rounded-3xl glass-box glow-red border-red-500/40">
        <div class="w-16 h-16 mx-auto rounded-3xl bg-red-600 flex items-center justify-center text-white shadow-xl mb-4">
          <svg class="w-8 h-8 fill-current" viewBox="0 0 24 24">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9v-2h2v2zm0-4H9V7h2v5zm4 4h-2v-2h2v2zm0-4h-2V7h2v5z"/>
          </svg>
        </div>
        <div class="text-3xl font-black text-white mb-3">دایرکتوری و پایگاه داده یوتیوبرهای ایران</div>
        <p class="text-sm text-slate-300 leading-relaxed max-w-lg mx-auto">
          فهرست کامل ۸۳ یوتیوبر، آدرس کانال‌ها، آمار دقیق دنبال‌کنندگان و امکان ثبت کانال‌های جدید در پایگاه داده متن‌باز هم‌اکنون به صورت رایگان در دسترس است.
        </p>
      </div>

      <div class="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-2">
        <div class="text-xs text-slate-400">مشاهده نسخه آنلاین روی گیت‌هاب پیجز:</div>
        <div class="text-lg font-mono font-black text-red-400">m4tinbeigi-official.github.io/iranian-youtubers</div>
        <div class="text-xs font-mono text-slate-500">لینک کوتاه: B2n.ir/hx3429</div>
      </div>

      <div class="text-xs text-slate-400 leading-relaxed">
        به جامعه تولیدکنندگان محتوای یوتیوب فارسی بپیوندید • برای افزودن کانال به گیت‌هاب یا گروه تلگرام مراجعه کنید
      </div>
    </div>
    """
    slides.append((10, "جامعه یوتیوبرهای ایرانی هم‌اکنون آنلاین است", "دسترسی آزاد به دایرکتوری", s10_content))

    return slides

def main():
    slides = build_slides()
    total = len(slides)

    print(f"Generating {total} HTML slides...")
    html_files = []
    for num, title, subtitle, content in slides:
        html_text = base_slide_template(num, total, title, subtitle, content)
        filename = f"slide_{num:02d}.html"
        file_path = HTML_DIR / filename
        file_path.write_text(html_text, encoding="utf-8")
        html_files.append((num, file_path))

    print("Rendering slides to PNG (1080x1350) with Google Chrome headless...")
    for num, html_path in html_files:
        png_path = PNG_DIR / f"slide_{num:02d}.png"
        cmd = [
            CHROME_PATH,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            f"--screenshot={png_path}",
            "--window-size=1080,1350",
            f"file://{html_path}"
        ]
        subprocess.run(cmd, check=True)
        print(f"Rendered: {png_path.name} ({png_path.stat().st_size // 1024} KB)")

    # Build gallery
    gallery_html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl" class="dark">
<head>
  <meta charset="UTF-8">
  <title>پیش‌نمایش اسلایدهای گزارش تحلیلی یوتیوب فارسی</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700;900&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>body {{ font-family: 'Vazirmatn', sans-serif; letter-spacing: 0; background-color: #0b0d14; color: #f1f5f9; }}</style>
</head>
<body class="p-8 max-w-7xl mx-auto">
  <div class="mb-8 flex items-center justify-between border-b border-slate-800 pb-5">
    <div>
      <h1 class="text-2xl font-black text-white">گالری پیش‌نمایش ۱۰ اسلاید گزارش کالبدشکافی یوتیوب فارسی</h1>
      <p class="text-xs text-slate-400 mt-1">طراحی شده با استانداردهای رسمی اینستاگرام و یوتیوب (نسبت ۴:۵ • ۱۰۸۰×۱۳۵۰)</p>
    </div>
    <a href="index.html" class="px-4 py-2 rounded-xl bg-red-600 hover:bg-red-700 text-xs font-bold text-white transition">بازگشت به دایرکتوری</a>
  </div>

  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
    {"".join([f'''
    <div class="bg-slate-900 border border-slate-800 rounded-3xl p-3 flex flex-col justify-between">
      <img src="carousel_png/slide_{i:02d}.png" class="rounded-2xl w-full object-cover shadow-lg border border-slate-800" loading="lazy">
      <div class="mt-3 flex items-center justify-between text-xs text-slate-400 px-1">
        <span class="font-bold text-white">اسلاید {to_persian(i)}</span>
        <a href="carousel_png/slide_{i:02d}.png" download class="text-red-400 hover:text-white transition font-medium">دانلود تصویر ↗</a>
      </div>
    </div>
    ''' for i in range(1, total + 1)])}
  </div>
</body>
</html>"""
    (BASE_DIR / "carousel_gallery.html").write_text(gallery_html, encoding="utf-8")
    print(f"Gallery written to {BASE_DIR / 'carousel_gallery.html'}")

if __name__ == "__main__":
    main()

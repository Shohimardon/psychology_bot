<!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>FOTIHA — O'zingizga qaytish kursi</title>
<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '1303889688600316');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=1303889688600316&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
<style>
  :root {
    --primary: #7C3AED;
    --primary-light: #A78BFA;
    --primary-dark: #5B21B6;
    --accent: #F59E0B;
    --accent-dark: #D97706;
    --bg: #FAF8FF;
    --card: #FFFFFF;
    --text: #1E1B2E;
    --muted: #6B7280;
    --danger: #EF4444;
    --green: #10B981;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    overflow-x: hidden;
  }

  /* ─── TOP BAR ─── */
  .topbar {
    background: var(--primary-dark);
    color: white;
    text-align: center;
    padding: 10px 16px;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.3px;
  }
  .topbar span { color: var(--accent); }

  /* ─── HERO ─── */
  .hero {
    background: linear-gradient(145deg, #1E1B2E 0%, #3B1F6B 55%, #6D28D9 100%);
    padding: 40px 20px 48px;
    position: relative;
    overflow: hidden;
  }
  .hero::before {
    content: '';
    position: absolute;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(167,139,250,0.15) 0%, transparent 70%);
    top: -80px; right: -80px;
    border-radius: 50%;
  }

  .hero-inner {
    display: flex;
    align-items: center;
    gap: 16px;
    position: relative;
    z-index: 1;
  }

  .hero-left { flex: 1; }

  .hero-tag {
    display: inline-block;
    background: rgba(245,158,11,0.2);
    border: 1px solid var(--accent);
    color: var(--accent);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 4px 10px;
    border-radius: 20px;
    margin-bottom: 14px;
  }

  .hero-question {
    color: white;
    font-size: 18px;
    font-weight: 800;
    line-height: 1.35;
    margin-bottom: 18px;
  }
  .hero-question em {
    font-style: normal;
    color: var(--primary-light);
  }

  .hero-pains {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 0;
  }
  .hero-pains li {
    color: rgba(255,255,255,0.88);
    font-size: 14px;
    display: flex;
    align-items: flex-start;
    gap: 8px;
    line-height: 1.4;
  }
  .hero-pains li::before {
    content: '•';
    color: var(--accent);
    font-size: 18px;
    line-height: 1;
    flex-shrink: 0;
  }

  .hero-photo {
    width: 150px;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
  }
  .hero-photo img {
    width: 145px;
    height: 185px;
    object-fit: cover;
    object-position: top;
    border-radius: 20px;
    border: 3px solid var(--accent);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
  }
  .photo-placeholder {
    width: 120px;
    height: 155px;
    border-radius: 18px;
    border: 3px solid var(--accent);
    background: linear-gradient(160deg, #4C1D95, #7C3AED);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
  }
  .photo-placeholder svg { opacity: 0.6; }
  .photo-placeholder span {
    color: rgba(255,255,255,0.5);
    font-size: 10px;
    margin-top: 6px;
    text-align: center;
  }
  .psych-name {
    color: white;
    font-size: 12px;
    font-weight: 700;
    text-align: center;
  }
  .psych-title {
    color: var(--primary-light);
    font-size: 10px;
    text-align: center;
  }

  /* ─── HERO BOTTOM ─── */
  .hero-bottom {
    background: linear-gradient(145deg, #3B1F6B, #6D28D9);
    padding: 8px 20px 32px;
    position: relative;
    overflow: hidden;
  }
  .hero-bottom::after {
    content: '';
    position: absolute;
    inset: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Ccircle cx='30' cy='30' r='20'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    pointer-events: none;
  }
  .course-title {
    text-align: center;
    color: white;
    font-size: 32px;
    font-weight: 900;
    letter-spacing: 2px;
    margin-bottom: 1em;
    text-shadow: 0 0 40px rgba(167,139,250,0.5);
    position: relative; z-index:1;
  }
  .course-subtitle {
    text-align: center;
    color: var(--accent);
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 16px;
    position: relative; z-index:1;
  }
  .course-desc {
    text-align: center;
    color: rgba(255,255,255,0.85);
    font-size: 15px;
    line-height: 1.6;
    margin-bottom: 24px;
    position: relative; z-index:1;
  }
  .course-desc strong { color: var(--primary-light); }

  /* ─── CTA BUTTON ─── */
  .cta-wrap { padding: 0 20px 8px; text-align: center; position: relative; z-index:1; }
  .btn-cta {
    display: block;
    width: 100%;
    background: linear-gradient(135deg, var(--accent) 0%, #F97316 100%);
    color: white;
    font-size: 17px;
    font-weight: 800;
    padding: 17px 24px;
    border-radius: 16px;
    border: none;
    cursor: pointer;
    text-decoration: none;
    box-shadow: 0 8px 24px rgba(245,158,11,0.4);
    transition: transform 0.15s, box-shadow 0.15s;
    letter-spacing: 0.3px;
    animation: pulse-btn 2.5s infinite;
  }
  @keyframes pulse-btn {
    0%, 100% { box-shadow: 0 8px 24px rgba(245,158,11,0.4); }
    50% { box-shadow: 0 8px 36px rgba(245,158,11,0.7); }
  }
  .btn-cta:active { transform: scale(0.97); }
  .btn-cta .sub { font-size: 12px; font-weight: 500; opacity: 0.88; display: block; margin-top: 2px; }

  /* ─── TIMER ─── */
  .timer-section {
    background: #1E1B2E;
    padding: 20px;
    text-align: center;
    border-top: 1px solid rgba(167,139,250,0.2);
    border-bottom: 1px solid rgba(167,139,250,0.2);
  }
  .timer-label {
    color: var(--danger);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
  }
  .timer-label::before, .timer-label::after { content: '🔥'; }
  .timer-boxes {
    display: flex;
    justify-content: center;
    gap: 10px;
  }
  .timer-box {
    background: linear-gradient(145deg, #2D2450, #3B1F6B);
    border: 1px solid rgba(167,139,250,0.3);
    border-radius: 12px;
    padding: 10px 14px;
    min-width: 62px;
  }
  .timer-num {
    color: white;
    font-size: 28px;
    font-weight: 900;
    line-height: 1;
    font-variant-numeric: tabular-nums;
  }
  .timer-unit {
    color: var(--primary-light);
    font-size: 10px;
    margin-top: 3px;
    font-weight: 600;
    letter-spacing: 0.5px;
  }
  .timer-sep {
    color: var(--accent);
    font-size: 24px;
    font-weight: 900;
    align-self: center;
    padding-bottom: 8px;
  }
  .spots-left {
    margin-top: 12px;
    color: var(--danger);
    font-size: 13px;
    font-weight: 700;
  }
  .spots-left span { color: white; }

  /* ─── SECTION TITLE ─── */
  .section { padding: 36px 20px; }
  .section-tag {
    display: inline-block;
    background: linear-gradient(135deg, var(--primary), var(--primary-light));
    color: white;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 10px;
  }
  .section-title {
    font-size: 22px;
    font-weight: 800;
    line-height: 1.3;
    margin-bottom: 20px;
  }
  .section-title em {
    font-style: normal;
    color: var(--primary);
  }

  /* ─── WHAT YOU GET ─── */
  .modules { display: flex; flex-direction: column; gap: 12px; }
  .module-card {
    background: var(--card);
    border-radius: 16px;
    padding: 16px;
    display: flex;
    gap: 14px;
    align-items: flex-start;
    box-shadow: 0 2px 12px rgba(124,58,237,0.08);
    border: 1px solid rgba(124,58,237,0.1);
  }
  .module-num {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, var(--primary), var(--primary-light));
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    color: white;
    font-size: 16px;
    font-weight: 900;
    flex-shrink: 0;
  }
  .module-info h4 { font-size: 14px; font-weight: 700; margin-bottom: 3px; }
  .module-info p { font-size: 13px; color: var(--muted); line-height: 1.4; }

  /* ─── WHO IS IT FOR ─── */
  .for-section { background: #F3F0FF; padding: 36px 20px; }
  .for-items { display: flex; flex-direction: column; gap: 10px; }
  .for-item {
    background: white;
    border-radius: 14px;
    padding: 14px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 1px 8px rgba(124,58,237,0.07);
  }
  .for-icon { font-size: 22px; }
  .for-text { font-size: 14px; font-weight: 600; line-height: 1.4; }

  /* ─── PSYCHOLOGIST ─── */
  .psych-section { padding: 36px 20px; }
  .psych-card {
    background: linear-gradient(145deg, #1E1B2E, #3B1F6B);
    border-radius: 24px;
    padding: 28px 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
  }
  .psych-card::before {
    content: '';
    position: absolute;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(167,139,250,0.15), transparent 70%);
    bottom: -60px; right: -60px;
    border-radius: 50%;
  }
  .psych-avatar {
    width: 220px; height: 220px;
    border-radius: 50%;
    border: 5px solid var(--accent);
    margin: 0 auto 18px;
    object-fit: cover;
    object-position: top;
    display: block;
    box-shadow: 0 12px 48px rgba(245,158,11,0.35);
  }
  .psych-avatar-ph {
    width: 150px; height: 150px;
    border-radius: 50%;
    border: 4px solid var(--accent);
    margin: 0 auto 16px;
    background: linear-gradient(145deg, #4C1D95, #7C3AED);
    display: flex; align-items: center; justify-content: center;
  }
  .psych-card-name { color: white; font-size: 24px; font-weight: 800; margin-bottom: 6px; }
  .psych-card-role { color: var(--primary-light); font-size: 14px; margin-bottom: 20px; letter-spacing: 0.3px; }
  .psych-stats {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-bottom: 16px;
    flex-wrap: wrap;
  }
  .psych-stat {
    background: rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 12px 18px;
    text-align: center;
  }
  .psych-stat-num { color: var(--accent); font-size: 26px; font-weight: 900; }
  .psych-stat-label { color: rgba(255,255,255,0.7); font-size: 12px; margin-top: 2px; }
  .psych-bio { color: rgba(255,255,255,0.8); font-size: 15px; line-height: 1.7; }

  /* ─── REVIEWS ─── */
  .reviews-section { background: #F3F0FF; padding: 36px 20px; }
  .reviews { display: flex; flex-direction: column; gap: 14px; }
  .review-card {
    background: white;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 2px 10px rgba(124,58,237,0.07);
  }
  .review-top {
    display: flex; align-items: center; gap: 10px; margin-bottom: 10px;
  }
  .review-ava {
    width: 40px; height: 40px; border-radius: 50%;
    background: linear-gradient(135deg, var(--primary), var(--primary-light));
    display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 700; font-size: 15px;
    flex-shrink: 0;
  }
  .review-name { font-weight: 700; font-size: 14px; }
  .review-stars { color: var(--accent); font-size: 13px; }
  .review-text { font-size: 14px; color: #374151; line-height: 1.55; }

  /* ─── PRICE ─── */
  .price-section { padding: 36px 20px; }
  .price-card {
    background: linear-gradient(145deg, #1E1B2E, #3B1F6B);
    border-radius: 24px;
    padding: 28px 20px;
    text-align: center;
    border: 2px solid var(--accent);
    box-shadow: 0 0 40px rgba(245,158,11,0.15);
    position: relative;
    overflow: hidden;
  }
  .price-badge {
    position: absolute;
    top: -1px; right: 20px;
    background: var(--danger);
    color: white;
    font-size: 11px;
    font-weight: 800;
    padding: 6px 14px;
    border-radius: 0 0 12px 12px;
    letter-spacing: 0.5px;
  }
  .price-name { color: white; font-size: 22px; font-weight: 800; margin-bottom: 6px; }
  .price-old {
    color: rgba(255,255,255,0.4);
    font-size: 18px;
    text-decoration: line-through;
    margin-bottom: 2px;
  }
  .price-new {
    color: var(--accent);
    font-size: 42px;
    font-weight: 900;
    line-height: 1;
    margin-bottom: 4px;
  }
  .price-currency { font-size: 20px; }
  .price-note { color: rgba(255,255,255,0.5); font-size: 12px; margin-bottom: 20px; }
  .includes { list-style: none; text-align: left; margin-bottom: 24px; display: flex; flex-direction: column; gap: 10px; }
  .includes li {
    color: rgba(255,255,255,0.88);
    font-size: 14px;
    display: flex; gap: 10px; align-items: flex-start;
  }
  .includes li::before {
    content: '✓';
    color: var(--green);
    font-weight: 900;
    flex-shrink: 0;
  }
  .guarantee {
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 12px;
    padding: 12px 16px;
    color: var(--green);
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 20px;
    display: flex; gap: 8px; align-items: center;
  }

  /* ─── BUNDLE ─── */
  .bundle-box {
    background: rgba(245,158,11,0.1);
    border: 1.5px solid rgba(245,158,11,0.4);
    border-radius: 14px;
    padding: 14px 16px;
    margin-bottom: 4px;
  }
  .bundle-title {
    color: var(--accent);
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 10px;
    text-align: center;
  }
  .bundle-items { display: flex; flex-direction: column; gap: 6px; }
  .bundle-item {
    color: rgba(255,255,255,0.9);
    font-size: 14px;
    font-weight: 600;
    padding: 6px 10px;
    background: rgba(255,255,255,0.06);
    border-radius: 8px;
    text-align: center;
  }

  /* ─── BONUS ─── */
  .bonus-header {
    background: linear-gradient(135deg, #F59E0B, #F97316);
    color: white;
    font-size: 15px;
    font-weight: 800;
    padding: 14px 16px;
    border-radius: 14px 14px 0 0;
    text-align: center;
    line-height: 1.4;
  }
  .bonus-sub {
    background: rgba(245,158,11,0.15);
    color: var(--accent);
    font-size: 12px;
    font-weight: 700;
    text-align: center;
    padding: 8px 16px;
    letter-spacing: 0.3px;
  }
  .bonus-list {
    display: flex;
    flex-direction: column;
    gap: 0;
    border: 1.5px solid rgba(245,158,11,0.25);
    border-top: none;
    border-radius: 0 0 14px 14px;
    overflow: hidden;
    margin-bottom: 12px;
  }
  .bonus-item {
    display: flex;
    gap: 12px;
    align-items: flex-start;
    padding: 12px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    background: rgba(255,255,255,0.03);
  }
  .bonus-item:last-child { border-bottom: none; }
  .bonus-num {
    color: var(--green);
    font-size: 13px;
    font-weight: 800;
    flex-shrink: 0;
    padding-top: 1px;
  }
  .bonus-text {
    color: rgba(255,255,255,0.85);
    font-size: 13px;
    line-height: 1.5;
  }
  .bonus-text strong { color: white; }
  .bonus-total {
    background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(16,185,129,0.05));
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 12px;
    padding: 12px 16px;
    color: rgba(255,255,255,0.8);
    font-size: 14px;
    font-weight: 600;
    text-align: center;
  }
  .bonus-total span { color: var(--green); font-size: 18px; font-weight: 900; }

  /* ─── FAQ ─── */
  .faq-section { padding: 36px 20px; background: #FAF8FF; }
  .faq-items { display: flex; flex-direction: column; gap: 10px; }
  .faq-item {
    background: white;
    border-radius: 14px;
    border: 1px solid rgba(124,58,237,0.1);
    overflow: hidden;
  }
  .faq-q {
    padding: 16px;
    font-size: 14px;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    user-select: none;
  }
  .faq-q .arr { color: var(--primary); font-size: 18px; transition: transform 0.3s; flex-shrink: 0; }
  .faq-a {
    padding: 0 16px;
    font-size: 14px;
    color: var(--muted);
    line-height: 1.6;
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.35s ease, padding 0.35s;
  }
  .faq-item.open .faq-a { max-height: 200px; padding: 0 16px 16px; }
  .faq-item.open .arr { transform: rotate(180deg); }

  /* ─── FOOTER CTA ─── */
  .footer-cta {
    background: linear-gradient(145deg, #1E1B2E, #3B1F6B);
    padding: 40px 20px 50px;
    text-align: center;
  }
  .footer-cta h2 { color: white; font-size: 22px; font-weight: 800; margin-bottom: 8px; line-height: 1.35; }
  .footer-cta p { color: rgba(255,255,255,0.7); font-size: 14px; margin-bottom: 24px; }
  .footer-copy {
    background: #111827;
    padding: 16px;
    text-align: center;
    color: rgba(255,255,255,0.3);
    font-size: 11px;
  }

  /* ─── STICKY CTA ─── */
  .sticky-cta {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    z-index: 999;
    padding: 12px 16px 20px;
    background: linear-gradient(to top, rgba(30,27,46,0.98) 0%, rgba(30,27,46,0) 100%);
    pointer-events: none;
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.4s, transform 0.4s;
  }
  .sticky-cta.show { opacity: 1; transform: translateY(0); pointer-events: all; }
  .sticky-cta .btn-cta { max-width: 420px; margin: 0 auto; }

</style>
</head>
<body>

<!-- TOP BAR -->
<div class="topbar">
  ⏳ Narx ko'tarilguncha: <span id="topbar-spots">7 ta o'rin qoldi!</span>
</div>

<!-- ════ HERO ════ -->
<section class="hero">
  <div class="hero-inner">
    <div class="hero-left">
      <div class="hero-tag">Psixologiya kursi</div>
      <h1 class="hero-question">
        O'zingizga nima <em>yetishmayotganini</em> bilmayabsizmi?
      </h1>
      <ul class="hero-pains">
        <li>Charchoq ketmaydimi?</li>
        <li>Ko'p yig'lagingiz keladimi?</li>
        <li>Ichingizda bo'shliq bormi?</li>
        <li>O'zingizni qadrlash qiyinmi?</li>
        <li>Qalbingiz tinchlik izlayaptimi?</li>
        <li>Xiyonat yarasi bormı?</li>
        <li>Qarzdorlikdan charchadizmi?</li>
      </ul>
    </div>
    <div class="hero-photo">
      <img src="foto.jpg" alt="Psixolog">
      <div class="psych-name"><!-- ISM --></div>
      <div class="psych-title">Psixolog</div>
    </div>
  </div>
</section>

<!-- ════ HERO BOTTOM ════ -->
<section class="hero-bottom">
  <div class="course-title">✦ FOTIHA ✦</div>
  <p class="course-desc" style="margin-top:-8px">
    Bu oddiy kurs emas.<br>
    Bu — <strong>o'zingizga qaytish yo'li.</strong><br>
    Ichki yaralarni tuzatib, o'z qadringizni topasiz.
  </p>
</section>

<!-- CTA BUTTON -->
<div class="cta-wrap" style="background:linear-gradient(145deg,#3B1F6B,#6D28D9); padding:0 20px 28px;">
  <a href="https://t.me/OybarchinObidova" class="btn-cta">
    📲 Kursga yozilish
    <span class="sub">Hozir yoziling — narx ko'tariladi</span>
  </a>
</div>

<!-- ════ TIMER ════ -->
<div class="timer-section">
  <div class="timer-label">Chegirma tugashiga qoldi</div>
  <div class="timer-boxes">
    <div class="timer-box">
      <div class="timer-num" id="t-h">00</div>
      <div class="timer-unit">soat</div>
    </div>
    <div class="timer-sep">:</div>
    <div class="timer-box">
      <div class="timer-num" id="t-m">00</div>
      <div class="timer-unit">daqiqa</div>
    </div>
    <div class="timer-sep">:</div>
    <div class="timer-box">
      <div class="timer-num" id="t-s">00</div>
      <div class="timer-unit">soniya</div>
    </div>
  </div>
  <div class="spots-left">🔴 Faqat <span id="spots-num">7</span> ta o'rin qoldi!</div>
</div>

<!-- ════ WHAT YOU GET ════ -->
<section class="section">
  <div class="section-tag">Kurs tarkibi</div>
  <h2 class="section-title">Kursda nima <em>olasiz?</em></h2>
  <div class="modules">
    <div class="module-card">
      <div class="module-num">1</div>
      <div class="module-info">
        <h4>O'zingizni tushunish</h4>
        <p>Nima sababdan charchayotganingiz va bo'shliq his etayotganingizni aniqlaymiz.</p>
      </div>
    </div>
    <div class="module-card">
      <div class="module-num">2</div>
      <div class="module-info">
        <h4>Ichki yaralarni tuzatish</h4>
        <p>Xiyonat, yo'qotish, rad etilish — bularni qayta ishlash va ozod bo'lish.</p>
      </div>
    </div>
    <div class="module-card">
      <div class="module-num">3</div>
      <div class="module-info">
        <h4>O'z-o'zini qadrlash</h4>
        <p>O'zingizga "yo'q" deyishni, chegaralar o'rnatishni va sevishni o'rganasiz.</p>
      </div>
    </div>
    <div class="module-card">
      <div class="module-num">4</div>
      <div class="module-info">
        <h4>Xotirjamlik va tinchlik</h4>
        <p>Har kuni ishlaydigan amaliy texnikalar — stress, xavotir, qo'rquvga qarshi.</p>
      </div>
    </div>
    <div class="module-card">
      <div class="module-num">5</div>
      <div class="module-info">
        <h4>Yangi hayot boshlanishi</h4>
        <p>Kurs tugagach siz boshqa odam bo'lasiz — ichdan erkin, kuchli va tinch.</p>
      </div>
    </div>
  </div>
</section>

<!-- ════ WHO IS IT FOR ════ -->
<section class="for-section">
  <div class="section-tag">Kim uchun?</div>
  <h2 class="section-title" style="margin-bottom:18px">Bu kurs <em>siz uchun</em> agar...</h2>
  <div class="for-items">
    <div class="for-item"><div class="for-icon">💔</div><div class="for-text">Xiyonat yoki ajralishdan keyin o'zingizni yo'qotgan bo'lsangiz</div></div>
    <div class="for-item"><div class="for-icon">😮‍💨</div><div class="for-text">Doim charchagan, uyqusiz yoki hissiy bo'shliqda bo'lsangiz</div></div>
    <div class="for-item"><div class="for-icon">🪞</div><div class="for-text">O'zingizni yoqtirmay, past baholasangiz</div></div>
    <div class="for-item"><div class="for-icon">😰</div><div class="for-text">Xavotir va qo'rquv hayotingizga xalaqit berayotgan bo'lsa</div></div>
    <div class="for-item"><div class="for-icon">🌸</div><div class="for-text">Yangi boshlanish istasangiz, lekin qayerdan boshlashni bilmasangiz</div></div>
  </div>
</section>

<!-- ════ PSYCHOLOGIST ════ -->
<section class="psych-section">
  <div class="section-tag">Murabbiy</div>
  <div class="psych-card">
    <img class="psych-avatar" src="foto.jpg" alt="Psixolog">
    <div class="psych-card-name"><!-- Psixolog ismi --></div>
    <div class="psych-card-role">Psixolog • Trener • FOTIHA muallifi</div>
    <div class="psych-stats">
      <div class="psych-stat">
        <div class="psych-stat-num">8+</div>
        <div class="psych-stat-label">yil tajriba</div>
      </div>
      <div class="psych-stat">
        <div class="psych-stat-num">5000+</div>
        <div class="psych-stat-label">mijoz</div>
      </div>
      <div class="psych-stat">
        <div class="psych-stat-num">98%</div>
        <div class="psych-stat-label">natija</div>
      </div>
    </div>
    <p class="psych-bio"><!-- Psixolog haqida qisqacha: 2-3 jumla. Masalan: "Men 5 yil davomida 200+ insonlarga o'z-o'zini tiklashda yordam berdim..." --></p>
  </div>
</section>

<!-- ════ REVIEWS ════ -->
<section class="reviews-section">
  <div class="section-tag">Fikrlar</div>
  <h2 class="section-title" style="margin-bottom:18px">Ular allaqachon <em>o'zgardi</em></h2>
  <div class="reviews">
    <div class="review-card">
      <div class="review-top">
        <div class="review-ava">Z</div>
        <div>
          <div class="review-name">Zulfiya, 28 yosh</div>
          <div class="review-stars">★★★★★</div>
        </div>
      </div>
      <p class="review-text">"Ajralishdan keyin o'zimni yo'qotgandim. Bu kurs menga o'zim bilan qayta tanishishga yordam berdi. Endi o'zimni sevishni boshladim 🌸"</p>
    </div>
    <div class="review-card">
      <div class="review-top">
        <div class="review-ava" style="background:linear-gradient(135deg,#EC4899,#8B5CF6)">N</div>
        <div>
          <div class="review-name">Nilufar, 34 yosh</div>
          <div class="review-stars">★★★★★</div>
        </div>
      </div>
      <p class="review-text">"Doim xavotirda yashadim. Kurs texnikaları darhol ishladi — 2-hafta ichida uyqu yaxshilandi, xotirjam bo'ldim. Rahmat!"</p>
    </div>
    <div class="review-card">
      <div class="review-top">
        <div class="review-ava" style="background:linear-gradient(135deg,#10B981,#3B82F6)">M</div>
        <div>
          <div class="review-name">Malika, 25 yosh</div>
          <div class="review-stars">★★★★★</div>
        </div>
      </div>
      <p class="review-text">"Kurs boshlanishida yig'ladim — chunki hamma og'riqlarim ko'rsatildi. Oxirida — kuldim. Bu mo'jiza! Haqiqiy o'zgarish."</p>
    </div>
  </div>
</section>

<!-- ════ PRICE ════ -->
<section class="price-section" id="price">
  <div class="section-tag">Narx</div>
  <h2 class="section-title" style="margin-bottom:18px">Bugun <em>maxsus narx</em> — ertaga ko'tariladi</h2>
  <div class="price-card">
    <div class="price-badge">-96% CHEGIRMA</div>
    <div class="price-name">FOTIHA kursi</div>
    <div class="price-old">Odatiy narx: 2 400 000 so'm</div>
    <div class="price-new"><span class="price-currency">💰</span> 99 000 <span style="font-size:22px">so'm</span></div>
    <div class="price-note">Bir martalik to'lov • 6 oylik kirish</div>

    <!-- KURS ICHIDA -->
    <ul class="includes">
      <li>8 ta jonli darslik</li>
      <li>Keyingi kursga 30% chegirma vaucher</li>
      <li>Kursga 6 oylik dostup</li>
    </ul>

    <!-- 3 TA KURS 1 NARXDA -->
    <div class="bundle-box">
      <div class="bundle-title">🎁 3 ta kurs — 1 narxda!</div>
      <div class="bundle-items">
        <div class="bundle-item">✦ Minnatdorchilik kursi</div>
        <div class="bundle-item">✦ Barakalai ayol kursi</div>
        <div class="bundle-item">✦ Fotiha kursi</div>
      </div>
    </div>

    <!-- NARX -->
    <div class="price-old" style="margin-top:16px;display:none">x</div>
    <div class="price-new">99 000 <span style="font-size:22px">so'm</span></div>
    <div class="price-note" style="margin-bottom:20px">Bir martalik to'lov • 6 oylik kirish • Boshlanish: 15-iyun</div>

    <a href="https://t.me/OybarchinObidova" class="btn-cta" style="margin-bottom:24px">
      📲 Hozir yozilish — 99 000 so'm
      <span class="sub">Faqat <span id="spots-btn">7</span> ta o'rin qoldi!</span>
    </a>

    <!-- BONUSLAR -->
    <div class="bonus-header">
      🥳 Hozir to'lagan o'quvchilarga chegirma joylari ochildi!
    </div>
    <div class="bonus-sub">Faqatgina hozir to'lov qilganlarga:</div>

    <div class="bonus-list">
      <div class="bonus-item">
        <div class="bonus-num">✅ 1</div>
        <div class="bonus-text">
          <strong>189 $ lik "Minnatdorchilik va o'zini sevish"</strong> darsi sovg'a sifatida qo'shib beriladi + <strong>233 $ lik "XIYONATGA MOYILLIK"</strong> darsiga umrbod dostup
        </div>
      </div>
      <div class="bonus-item">
        <div class="bonus-num">✅ 2</div>
        <div class="bonus-text"><strong>6 ta bonus sovg'a</strong> — maxsus materiallar va amaliyotlar</div>
      </div>
      <div class="bonus-item">
        <div class="bonus-num">✅ 3</div>
        <div class="bonus-text"><strong>3 kunlik to'liq darslar</strong> audio formatda — istalgan vaqt tinglaysiz</div>
      </div>
      <div class="bonus-item">
        <div class="bonus-num">✅ 4</div>
        <div class="bonus-text"><strong>190 $ lik "PULLARGA OCHILISH"</strong> amaliyoti sovg'a!</div>
      </div>
    </div>

    <div class="bonus-total">
      Jami bonuslar qiymati: <span>612 $+</span> — bepul!
    </div>
  </div>
</section>

<!-- ════ FAQ ════ -->
<section class="faq-section">
  <div class="section-tag">Savollar</div>
  <h2 class="section-title" style="margin-bottom:18px">Ko'p beriladigan <em>savollar</em></h2>
  <div class="faq-items">
    <div class="faq-item">
      <div class="faq-q">Kurs qachon boshlanadi? <span class="arr">▼</span></div>
      <div class="faq-a">Kurs 15-iyun da boshlanadi. Yozilganingizdan so'ng guruhga qo'shilasiz va barcha ma'lumotlar yuboriladi.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q">Kurs qancha davom etadi? <span class="arr">▼</span></div>
      <div class="faq-a">Kurs 1 oy davom etadi — 15-iyundan 15-iyulgacha. Har hafta yangi modul ochiladi. Siz o'z sur'atingizda ishlaysiz.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q">Onlayn yoki offline? <span class="arr">▼</span></div>
      <div class="faq-a">100% onlayn. Telegram va video-platform orqali. Vaqtingizga qarab, istalgan joydan kirishingiz mumkin.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q">Psixologga borishga vaqtim yo'q, bu kurs yordam beradimi? <span class="arr">▼</span></div>
      <div class="faq-a">Ha! Bu kurs ayniqsa band odamlar uchun. 15-20 daqiqa kuniga — shu kifoya. Hamma narsa mobil telefon orqali.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q">Natija ko'rmasam nima bo'ladi? <span class="arr">▼</span></div>
      <div class="faq-a">Kurs tugagandan so'ng siz o'zingizda haqiqiy o'zgarish his etasiz. Ko'plab o'quvchilarimiz allaqachon natija ko'rishdi — endi navbat sizda! 🌸</div>
    </div>
  </div>
</section>

<!-- ════ FOOTER CTA ════ -->
<section class="footer-cta">
  <h2>O'zingizga qaytishni boshlang — <em style="color:var(--accent)">bugun</em></h2>
  <p>Ertaga emas, hozir. Chegirma tugaydi, o'rinlar tugaydi.</p>
  <a href="https://t.me/OybarchinObidova" class="btn-cta" style="max-width:400px;margin:0 auto;display:block;">
    📲 Kursga yozilish
    <span class="sub">Faqat <span id="spots-footer">7</span> ta o'rin qoldi</span>
  </a>
</section>

<div class="footer-copy">
  © 2025 FOTIHA kursi. Barcha huquqlar himoyalangan.
</div>

<!-- STICKY CTA -->
<div class="sticky-cta" id="sticky">
  <a href="https://t.me/OybarchinObidova" class="btn-cta">
    📲 Kursga yozilish
    <span class="sub">Chegirma tugaydi — hozir yoziling!</span>
  </a>
</div>

<script>
// ─── COUNTDOWN TIMER ───
(function() {
  // Chegirma muddati: localStorage'da saqlanadi (har odam uchun alohida, ammo doimiy)
  var key = 'fotiha_deadline';
  var stored = localStorage.getItem(key);
  var deadline;
  if (stored) {
    deadline = parseInt(stored);
  } else {
    // 23 soat 47 daqiqa countdown
    deadline = Date.now() + (1 * 3600 + 47 * 60) * 1000;
    localStorage.setItem(key, deadline);
  }

  function pad(n) { return n < 10 ? '0' + n : '' + n; }

  function tick() {
    var diff = Math.max(0, deadline - Date.now());
    var h = Math.floor(diff / 3600000);
    var m = Math.floor((diff % 3600000) / 60000);
    var s = Math.floor((diff % 60000) / 1000);
    document.getElementById('t-h').textContent = pad(h);
    document.getElementById('t-m').textContent = pad(m);
    document.getElementById('t-s').textContent = pad(s);
    if (diff <= 0) {
      // Yangi 24 soat qayta boshlanadi
      deadline = Date.now() + (1 * 3600 + 47 * 60) * 1000;
      localStorage.setItem(key, deadline);
    }
  }
  tick();
  setInterval(tick, 1000);
})();

// ─── FAKE SPOTS COUNTER ───
(function() {
  var key2 = 'fotiha_spots';
  var stored = localStorage.getItem(key2);
  var spots;
  if (stored) {
    spots = parseInt(stored);
  } else {
    spots = 7; // Boshlang'ich soni
    localStorage.setItem(key2, spots);
  }

  // Har 4-8 daqiqada 1 ta kamayadi (sahifa ochiq bo'lsa)
  function dec() {
    if (spots > 2) {
      spots--;
      localStorage.setItem(key2, spots);
      updateSpots();
    }
  }

  function updateSpots() {
    ['spots-num','spots-btn','spots-footer'].forEach(function(id) {
      var el = document.getElementById(id);
      if (el) el.textContent = spots;
    });
    var tb = document.getElementById('topbar-spots');
    if (tb) tb.textContent = spots + " ta o'rin qoldi!";
  }

  updateSpots();
  // Random interval: 4-8 daqiqa
  function schedDec() {
    var delay = (4 + Math.random() * 4) * 60 * 1000;
    setTimeout(function() { dec(); schedDec(); }, delay);
  }
  schedDec();
})();

// ─── STICKY CTA: show after hero ───
(function() {
  var sticky = document.getElementById('sticky');
  var shown = false;
  window.addEventListener('scroll', function() {
    if (window.scrollY > 420 && !shown) {
      shown = true;
      sticky.classList.add('show');
    } else if (window.scrollY <= 420 && shown) {
      shown = false;
      sticky.classList.remove('show');
    }
  });
})();

// ─── FAQ ACCORDION ───
document.querySelectorAll('.faq-q').forEach(function(q) {
  q.addEventListener('click', function() {
    var item = q.parentElement;
    item.classList.toggle('open');
  });
});

// ─── CTA CLICK TRACKING ───
document.querySelectorAll('.btn-cta').forEach(function(a) {
  a.addEventListener('click', function() {
    if(typeof fbq !== 'undefined') fbq('track', 'Lead');
  });
});
</script>
</body>
</html>

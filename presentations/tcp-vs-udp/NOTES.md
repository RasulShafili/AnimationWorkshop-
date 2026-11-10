# TCP vs UDP – təqdimat videosu (Şəfili Rəsul, 24A, tapşırıq 19)

1920x1080, 90 s, 2D pixel, musiqisiz (yalnız səs effektləri). Render: `npx remotion render src/index.ts Video out.mp4 --browser-executable=/usr/bin/google-chrome --concurrency=4`
Font: VT323 (OFL) – ə/ş/ğ/İ latin-ext faylından, ç/ı/ö/ü latin faylından bişirilib.

| Vaxt | Səhnə | Tapşırıq sualı |
|---|---|---|
| 0:00-0:06 | Gecə küçəsi: TCP furqonu, UDP motosikleti | Başlıq |
| 0:06-0:14 | Evdən serverə paketlər | Giriş |
| 0:14-0:26 | Kuryer: SYN -> SYN-ACK -> ACK, əl sıxma | 1. TCP əlaqə yönümlüdürmü? |
| 0:26-0:44 | Nömrəli qutular, ACK imzası, itən 3-cü qutu, taymer, təkrar göndərmə | 3. ACK nədir? 4. Etibarlılıq |
| 0:44-0:58 | Stadiondan TV-yə canlı yayım, itən kadr | 2. UDP necə işləyir? |
| 0:58-1:10 | Oyun: TCP ilişir, UDP axıcı | 5. UDP nə zaman üstündür? |
| 1:10-1:20 | Veb, e-poçt, FTP / oyun, video zəng, canlı yayım, DNS | 6. Tətbiq nümunələri |
| 1:20-1:30 | Müqayisə cədvəli, Təşəkkürlər | Cədvəl |

Fakt yoxlaması: TCP başlığı minimum 20 bayt, UDP başlığı 8 bayt; DNS əsasən UDP (port 53) istifadə edir.

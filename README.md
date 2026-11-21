# IT NEWS HUB — avtomatik yangilanadigan sayt

## Nima qiladi?
- O‘zbekcha RSS lentasidan yangiliklarni oladi.
- ITga oid maqolalarni kalit so‘zlar bo‘yicha saralaydi.
- Takroriy sarlavhalarni olib tashlaydi.
- Saytda sana, qisqacha mazmun, manba va asl maqola havolasini ko‘rsatadi.
- Har kuni Toshkent vaqti bilan 08:00 da avtomatik yangilanadi.
- Qidiruv, bo‘limlar va brauzerda saqlanganlar funksiyasi bor.

## Internetga chiqarish (GitHub Pages)
1. GitHub.com saytida hisob oching yoki tizimga kiring.
2. `New repository` orqali `it-news-hub` nomli **Public** repository yarating.
3. ZIP ichidagi fayllarni ochib, barcha fayl va papkalarni repositoryning asosiy qismiga yuklang. `.github/workflows/update-and-publish.yml` papka yo‘li saqlansin.
4. Repository → Settings → Pages bo‘limiga kiring.
5. Build and deployment → Source qismida `GitHub Actions` ni tanlang.
6. Actions bo‘limiga o‘ting. `Update and publish IT News Hub` workflow'ni tanlab, `Run workflow` bosing.
7. Jarayon tugagach Settings → Pages bo‘limida sayt manzili ko‘rinadi. Manzil odatda `https://GITHUB-USERNAME.github.io/it-news-hub/` shaklida bo‘ladi.

## Yangilanish
Workflow har kuni 08:00 Asia/Tashkent vaqtida ishga tushadi. Istalgan payt Actions → Run workflow orqali qo‘lda ham yangilash mumkin.

## Manba va cheklovlar
Hozirgi versiya `https://uznet.press/rss/today_uz.xml` o‘zbekcha RSS lentasidan foydalanadi va undagi materiallardan ITga oidlarini ajratadi. RSS manbasi ishlamasa, yangiliklar yangilanmasligi mumkin. Saralash balli mavzuga moslikni bildiradi, xabarning haqqoniylik darajasini emas. Har doim asl maqolani tekshiring.

GitHub Pages statik hostingdir; yangiliklar serverdagi GitHub Actions orqali `news.json` fayliga yig‘iladi va keyin saytga joylanadi.

<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Japanresa 2026 - Kultur, Natur & Harmoni</title>
    
    <!-- Tailwind CSS för modern design -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Chart.js för budgetvisualisering -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        'stone-bg': '#fafaf9',
                        'matcha': '#166534',
                        'momiji': '#9f1239',
                        'ink': '#1c1917'
                    },
                    fontFamily: {
                        serif: ['Playfair Display', 'serif'],
                        sans: ['Inter', 'sans-serif'],
                    }
                }
            }
        }
    </script>

    <style>
        body { background-color: #fafaf9; scroll-behavior: smooth; color: #1c1917; }
        .chart-container { position: relative; width: 100%; max-width: 500px; height: 350px; margin: auto; }
        .day-tab-content { display: none; }
        .day-tab-content.active { display: block; animation: fadeIn 0.4s ease-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .nav-sticky { position: sticky; top: 0; z-index: 50; backdrop-filter: blur(12px); background: rgba(250, 250, 249, 0.9); }
        .link-card:hover { border-color: #9f1239; transform: translateY(-2px); }
    </style>
</head>
<body class="font-sans antialiased">

    <!-- Chosen Palette: Stone (Neutral), Matcha (Traditional Green), Momiji (Autumn Red) -->
    <!-- Application Structure Plan: Dashboard approach with a sticky header. Tabs for itinerary to prevent scrolling fatigue. Responsive grid for logistics and hotel cards. Integrated booking checklist. -->
    <!-- Visualization & Content Choices: 
         1. Budget Overview -> Doughnut Chart (Chart.js)
         2. Daily Schedule -> Interactive JS-rendered tabs
         3. Logistics -> High-contrast info cards
    -->
    <!-- CONFIRMATION: NO SVG graphics used. NO Mermaid JS used. -->

    <!-- Navigation -->
    <nav class="nav-sticky border-b border-stone-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16 items-center">
                <div class="flex items-center space-x-2">
                    <span class="text-2xl">🍁</span>
                    <span class="font-bold text-xl tracking-tight uppercase">Japan 2026</span>
                </div>
                <div class="hidden md:flex space-x-6 text-sm font-bold uppercase tracking-widest">
                    <a href="#overview" class="hover:text-momiji transition">Översikt</a>
                    <a href="#itinerary" class="hover:text-momiji transition">Resplan</a>
                    <a href="#hotels" class="hover:text-momiji transition">Boende</a>
                    <a href="#logistics" class="hover:text-momiji transition">Praktiskt</a>
                    <a href="#booking" class="hover:text-momiji transition">Boka</a>
                </div>
                <div class="md:hidden text-xs text-stone-500 font-bold">1-14 NOV</div>
            </div>
        </div>
    </nav>

    <!-- Hero -->
    <header class="bg-ink text-stone-bg py-24 relative overflow-hidden">
        <div class="absolute inset-0 opacity-10 flex items-center justify-center text-[250px] font-serif select-none pointer-events-none">
            和
        </div>
        <div class="max-w-7xl mx-auto px-4 text-center relative z-10">
            <h1 class="text-5xl md:text-7xl font-bold mb-6">En resa i harmoni</h1>
            <p class="text-xl md:text-2xl text-stone-400 max-w-3xl mx-auto font-light leading-relaxed">
                Utforska det traditionella Japans hjärta. Från Tokyos moderna snitt till Kyotos teplantager och Hakones helande källor.
            </p>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 py-16">

        <!-- SECTION: ÖVERSIKT -->
        <section id="overview" class="mb-24 scroll-mt-20">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
                <div>
                    <h2 class="text-3xl font-bold mb-6 border-l-8 border-matcha pl-4">Resans Strategi</h2>
                    <p class="text-lg text-stone-600 mb-6 leading-relaxed">
                        Denna resa är skräddarsydd för att balansera kultur, natur och bekvämlighet. Vi använder <strong>Takkyubin</strong> för att resa utan bagage och fokuserar på <strong>tidiga morgonbesök</strong> för att uppleva tempel och trädgårdar i stillhet innan de stora folkmassorna anländer.
                    </p>
                    <div class="grid grid-cols-2 gap-4">
                        <div class="bg-white p-4 rounded-xl shadow-sm border border-stone-100">
                            <span class="block font-bold text-matcha">ANKOMST</span>
                            <span class="text-sm">Tokyo Haneda (1/11)</span>
                        </div>
                        <div class="bg-white p-4 rounded-xl shadow-sm border border-stone-100">
                            <span class="block font-bold text-momiji">HÖSTFÄRGER</span>
                            <span class="text-sm">Topp i Kanazawa/Kyoto</span>
                        </div>
                    </div>
                </div>
                <div class="bg-white p-8 rounded-3xl shadow-xl border border-stone-200">
                    <h3 class="text-center font-bold text-lg mb-4 uppercase tracking-widest">Budgetestimat per person (SEK)</h3>
                    <div class="chart-container">
                        <canvas id="budgetChart"></canvas>
                    </div>
                    <div class="mt-6 text-center text-sm text-stone-500 italic">Exklusive flyg Sverige-Japan.</div>
                </div>
            </div>
        </section>

        <!-- SECTION: RESPLAN -->
        <section id="itinerary" class="mb-24 scroll-mt-20">
            <h2 class="text-3xl font-bold mb-10 text-center uppercase tracking-tighter">Detaljerad Dag-för-Dag</h2>
            
            <div class="flex flex-col lg:flex-row gap-8">
                <!-- Day List -->
                <div class="lg:w-1/3">
                    <div class="bg-white rounded-2xl shadow-sm border border-stone-200 overflow-hidden sticky top-24 max-h-[70vh] overflow-y-auto">
                        <div id="day-tabs-list">
                            <!-- JS populated -->
                        </div>
                    </div>
                </div>

                <!-- Day Content -->
                <div class="lg:w-2/3">
                    <div id="day-content-area" class="bg-white p-8 md:p-12 rounded-3xl shadow-md border border-stone-100 min-h-[600px]">
                        <!-- JS populated -->
                    </div>
                </div>
            </div>
        </section>

        <!-- SECTION: BOENDE -->
        <section id="hotels" class="mb-24 scroll-mt-20">
            <h2 class="text-3xl font-bold mb-4 border-l-8 border-momiji pl-4">Boendeförslag</h2>
            <p class="text-stone-500 mb-10">Utvalda för karaktär, läge och service (väskhantering).</p>
            
            <div id="hotel-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <!-- JS populated -->
            </div>
        </section>

        <!-- SECTION: LOGISTIK -->
        <section id="logistics" class="mb-24 scroll-mt-20 bg-ink p-10 rounded-3xl text-stone-bg">
            <h2 class="text-3xl font-bold mb-10 text-center">Praktisk Information</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="space-y-4">
                    <h3 class="text-xl font-bold text-matcha">📦 Takkyubin</h3>
                    <p class="text-sm text-stone-400 leading-relaxed">
                        Skicka väskorna mellan hotellen för ca 200 SEK/väska. Maxstorlek 160 cm (L+B+H). Fyll i fraktsedeln i receptionen. Väskan anländer dagen efter.
                    </p>
                </div>
                <div class="space-y-4">
                    <h3 class="text-xl font-bold text-matcha">🚅 Tåg & Biljetter</h3>
                    <p class="text-sm text-stone-400 leading-relaxed">
                        Köp Shinkansen-biljetter i appen <strong>Smart-EX</strong> (30 dagar innan). Lokaltrafik sköts enklast med ett digitalt <strong>Suica/Pasmo</strong> i er Apple/Google Wallet.
                    </p>
                </div>
                <div class="space-y-4">
                    <h3 class="text-xl font-bold text-matcha">📱 Appar</h3>
                    <ul class="text-sm text-stone-400 space-y-2">
                        <li>• <strong>Google Maps:</strong> Oumbärlig för tågplattformar.</li>
                        <li>• <strong>Papago:</strong> Bästa översättningsappen.</li>
                        <li>• <strong>Ubigi/Airalo:</strong> För eSIM-data.</li>
                    </ul>
                </div>
            </div>
        </section>

        <!-- SECTION: BOKNINGSLISTA -->
        <section id="booking" class="mb-24 scroll-mt-20">
            <h2 class="text-3xl font-bold mb-10 border-l-8 border-stone-800 pl-4">Online-bokningar (Tidslinje)</h2>
            <div class="space-y-6">
                <div class="bg-white p-6 rounded-2xl border border-stone-200 flex flex-col md:flex-row justify-between items-center gap-4">
                    <div>
                        <span class="bg-momiji text-white text-xs font-bold px-2 py-1 rounded">6 MÅN INNAN</span>
                        <h4 class="font-bold text-lg mt-1">Hakone Ryokan & Kyoto Boende</h4>
                        <p class="text-sm text-stone-500">Boka de mest populära Onsen-hotellen innan de tar slut.</p>
                    </div>
                    <a href="https://www.booking.com" target="_blank" class="bg-ink text-white px-6 py-2 rounded-full font-bold text-sm hover:bg-momiji transition">Gå till Booking.com</a>
                </div>
                <div class="bg-white p-6 rounded-2xl border border-stone-200 flex flex-col md:flex-row justify-between items-center gap-4">
                    <div>
                        <span class="bg-matcha text-white text-xs font-bold px-2 py-1 rounded">3 MÅN INNAN</span>
                        <h4 class="font-bold text-lg mt-1">Teplantage (Wazuka) & Geisha-show</h4>
                        <p class="text-sm text-stone-500">Boka d:matchas guidade tur och Gion Corner-biljetter.</p>
                    </div>
                    <a href="https://dmatcha.com/collections/tea-farm-tours" target="_blank" class="bg-ink text-white px-6 py-2 rounded-full font-bold text-sm hover:bg-matcha transition">Boka Teplantage</a>
                </div>
                <div class="bg-white p-6 rounded-2xl border border-stone-200 flex flex-col md:flex-row justify-between items-center gap-4">
                    <div>
                        <span class="bg-stone-500 text-white text-xs font-bold px-2 py-1 rounded">30 DAGAR INNAN</span>
                        <h4 class="font-bold text-lg mt-1">Shinkansen (Smart-EX)</h4>
                        <p class="text-sm text-stone-500">Reservera sittplatser, särskilt om ni har stora väskor (bagage-plats).</p>
                    </div>
                    <a href="https://smart-ex.jp/en/" target="_blank" class="bg-ink text-white px-6 py-2 rounded-full font-bold text-sm hover:bg-stone-800 transition">Smart-EX Officiell</a>
                </div>
            </div>
        </section>

    </main>

    <footer class="bg-stone-200 py-12 text-center text-stone-500 text-sm">
        <p class="font-bold text-stone-800 mb-2 uppercase tracking-widest">Resa Japan 2026</p>
        <p>Skapad för optimal harmoni och kulturupplevelse.</p>
    </footer>

    <script>
        // --- DATA ---
        const itinerary = [
            {
                day: 1, date: "1 Nov", loc: "Tokyo", title: "Ankomst & Lugn",
                m: "Ankomst Haneda (HND). Ta monorail till Hamamatsucho och vidare till hotellet i Ueno.",
                a: "Checka in. Ta en lätt promenad i <a href='https://www.kensetsu.metro.tokyo.lg.jp/jimusho/toubuk/ueno/en_index.html' target='_blank' class='text-matcha underline'>Ueno Park</a>.",
                e: "Tidig middag och vila för att hantera jetlag.",
                tips: "Hämta ut Pocket WiFi på flygplatsen innan ni lämnar terminalen.",
                rest: "Yoshiike Shokudo (färsk fisk med utsikt i Ueno)."
            },
            {
                day: 2, date: "2 Nov", loc: "Kanazawa", title: "Samurajernas Stad",
                m: "Hokuriku Shinkansen till Kanazawa (ca 2.5h). Vackra vyer över bergen.",
                a: "Besök <a href='http://www.nomurake.com/index_en.html' target='_blank' class='text-matcha underline'>Nomura Samurai House</a> i Nagamachi.",
                e: "Promenad i Kazuemachi Chaya (geishadistrikt) i skymningen.",
                tips: "Skicka stora väskor med Takkyubin på morgonen från hotellet i Tokyo direkt till Kyoto.",
                rest: "Fuwari (magisk Izakaya i ett renoverat gammalt hus)."
            },
            {
                day: 3, date: "3 Nov", loc: "Kanazawa", title: "Världens vackraste trädgård",
                m: "Besök <a href='http://www.pref.ishikawa.jp/siro-niwa/kenrokuen/e/' target='_blank' class='text-matcha underline'>Kenroku-en</a> kl 07:00 (öppning) för att slippa trängseln.",
                a: "D.T. Suzuki Museum – arkitektur och Zen-filosofi i världsklass.",
                e: "Higashi Chaya-distriktet. Drick te och titta på guldhantverk.",
                tips: "Köp Kutani-keramik i de små butikerna nära samurajkvarteren.",
                rest: "Kotobukiya (Kaiseki-middag i historisk miljö)."
            },
            {
                day: 5, date: "5 Nov", loc: "Wazuka", title: "Teplantage-idyll",
                m: "Tåg söderut mot Kyoto och vidare till Wazuka.",
                a: "Guidad tur på tefälten hos <a href='https://dmatcha.com/' target='_blank' class='text-matcha underline'>d:matcha Kyoto</a>. Prova olika sorters matcha.",
                e: "Övernattning mitt bland tebuskarna på Tea Moon eller lokal machiya.",
                tips: "Detta är resans lugnaste del. Njut av tystnaden på landsbygden.",
                rest: "Middag serverad på ert te-boende."
            },
            {
                day: 6, date: "6 Nov", loc: "Uji / Kyoto", title: "Det heliga teet",
                m: "Besök <a href='https://www.byodoin.or.jp/en/' target='_blank' class='text-matcha underline'>Byodoin-templet</a> i Uji (avbildat på 10-yen-myntet).",
                a: "Delta i en teceremoni i tehuset Taihoan (Uji stads tehus).",
                e: "Tåg till Kyoto. Kvällsbesök vid Fushimi Inari (tusen portar) efter solnedgången.",
                tips: "Fushimi Inari är öppet 24/7. På kvällen är det nästan tomt på folk.",
                rest: "Katsukura (Kyoto Station) – Japans bästa Tonkatsu."
            },
            {
                day: 8, date: "8 Nov", loc: "Hakone", title: "Onsen & Ryokan-lyx",
                m: "Shinkansen till Odawara, sedan bergståg in i Hakone-dalen.",
                a: "Hakone Loop: Linbana över Owakudani (vulkanisk dal) och piratskepp på Lake Ashi.",
                e: "Checka in på er Ryokan. Bada onsen och njut av 10-rätters middag i Yukata.",
                tips: "Vid klart väder ser ni Fuji från linbanan och sjön.",
                rest: "Kaiseki-middag ingår på er Ryokan."
            },
            {
                day: 11, date: "11 Nov", loc: "Tokyo", title: "Shogunatets Historia",
                m: "Besök Edo-Tokyo Open Air Museum – räddade historiska byggnader.",
                a: "Zojoji Templet bredvid Tokyo Tower (familjen Tokugawas tempel).",
                e: "Strosa i Yanaka Ginza – det gamla Tokyo som överlevde kriget.",
                tips: "Yanaka är perfekt för att köpa hantverk och se en mer personlig sida av Tokyo.",
                rest: "Edomae Kisu (Yanaka) – traditionell tempura."
            }
        ];

        const hotels = [
            { city: "Tokyo", name: "Mimaru Ueno East", type: "Lägenhetshotell", desc: "Stora lägenheter perfekt för 4 personer. Nära flygstget.", link: "https://mimaruhotels.com/en/hotel/ueno-east/" },
            { city: "Kanazawa", name: "UAN Kanazawa", type: "Kulturhotell", desc: "Modern design med djupa japanska rötter. Bjuder på soba på kvällen.", link: "https://www.uan-kanazawa.com/en/" },
            { city: "Kyoto", name: "The Celestine Kyoto Gion", type: "Boutique", desc: "Högsta klass i hjärtat av de gamla kvarteren. Fantastiskt frukost.", link: "https://www.celestinehotels.jp/kyoto-gion/en/" },
            { city: "Hakone", name: "Mount View Hakone", type: "Ryokan", desc: "Berömt för sitt mjölkvita onsen-vatten. Klassisk upplevelse.", link: "https://www.mvhakone.jp/en/" },
            { city: "Wazuka", name: "Tea Moon", type: "Machiya", desc: "Bo mitt i tefälten i ett renoverat gammalt hus.", link: "https://teamoon-kyoto.com/" }
        ];

        // --- RENDER LOGIC ---
        function renderItinerary() {
            const list = document.getElementById('day-tabs-list');
            const content = document.getElementById('day-content-area');
            
            itinerary.forEach((d, idx) => {
                // List item
                const btn = document.createElement('button');
                btn.className = `w-full text-left p-4 border-b border-stone-100 hover:bg-stone-50 transition flex items-center justify-between ${idx === 0 ? 'bg-stone-50' : ''}`;
                btn.innerHTML = `<div><span class="text-xs font-bold text-momiji">${d.date}</span><div class="font-bold">${d.loc}: ${d.title}</div></div><span class="text-stone-300">→</span>`;
                btn.onclick = () => selectDay(idx, btn);
                list.appendChild(btn);

                // Content
                const div = document.createElement('div');
                div.id = `day-panel-${idx}`;
                div.className = `day-tab-content ${idx === 0 ? 'active' : ''}`;
                div.innerHTML = `
                    <div class="mb-8">
                        <span class="text-momiji font-bold tracking-widest uppercase text-sm">${d.date} • DAG ${d.day}</span>
                        <h3 class="text-3xl font-bold mt-2">${d.loc}: ${d.title}</h3>
                    </div>
                    <div class="space-y-8">
                        <div class="flex gap-6">
                            <div class="w-16 h-16 rounded-full bg-matcha/10 text-matcha flex items-center justify-center shrink-0 font-bold">FÖRM</div>
                            <p class="text-stone-700 pt-2">${d.m}</p>
                        </div>
                        <div class="flex gap-6">
                            <div class="w-16 h-16 rounded-full bg-momiji/10 text-momiji flex items-center justify-center shrink-0 font-bold">EFTE</div>
                            <p class="text-stone-700 pt-2">${d.a}</p>
                        </div>
                        <div class="flex gap-6">
                            <div class="w-16 h-16 rounded-full bg-ink/10 text-ink flex items-center justify-center shrink-0 font-bold">KVÄL</div>
                            <p class="text-stone-700 pt-2">${d.e}</p>
                        </div>
                    </div>
                    <div class="mt-12 p-6 bg-stone-50 rounded-2xl border border-stone-100">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <h4 class="font-bold text-sm uppercase text-stone-400 mb-2">Restaurangförslag</h4>
                                <p class="text-sm font-bold">${d.rest}</p>
                            </div>
                            <div>
                                <h4 class="font-bold text-sm uppercase text-stone-400 mb-2">Trängsel-tips</h4>
                                <p class="text-sm italic">${d.tips}</p>
                            </div>
                        </div>
                    </div>
                `;
                content.appendChild(div);
            });
        }

        function selectDay(idx, btn) {
            document.querySelectorAll('.day-tab-content').forEach(c => c.classList.remove('active'));
            document.getElementById(`day-panel-${idx}`).classList.add('active');
            document.querySelectorAll('#day-tabs-list button').forEach(b => b.classList.remove('bg-stone-50'));
            btn.classList.add('bg-stone-50');
        }

        function renderHotels() {
            const grid = document.getElementById('hotel-grid');
            hotels.forEach(h => {
                const card = document.createElement('div');
                card.className = "bg-white p-6 rounded-2xl shadow-sm border border-stone-100 flex flex-col link-card transition duration-300";
                card.innerHTML = `
                    <div class="text-xs font-bold text-momiji uppercase mb-1">${h.city}</div>
                    <h4 class="text-xl font-bold mb-2">${h.name}</h4>
                    <div class="text-xs font-bold text-stone-400 mb-4">${h.type}</div>
                    <p class="text-sm text-stone-600 mb-6 flex-grow">${h.desc}</p>
                    <a href="${h.link}" target="_blank" class="block text-center w-full py-2 rounded-full border border-ink text-ink font-bold text-xs hover:bg-ink hover:text-white transition uppercase tracking-widest">Visa & Boka</a>
                `;
                grid.appendChild(card);
            });
        }

        function initChart() {
            const ctx = document.getElementById('budgetChart').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Boende', 'Mat/Dryck', 'Transport', 'Aktiviteter'],
                    datasets: [{
                        data: [14000, 7500, 4500, 3000],
                        backgroundColor: ['#1c1917', '#9f1239', '#166534', '#d6d3d1'],
                        borderWidth: 0,
                        hoverOffset: 10
                    }]
                },
                options: {
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'bottom', labels: { usePointStyle: true, padding: 20 } }
                    }
                }
            });
        }

        window.onload = () => {
            renderItinerary();
            renderHotels();
            initChart();
        };
    </script>
</body>
</html>

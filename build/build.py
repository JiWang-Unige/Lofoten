"""Generate site/index.html from the itinerary data below.

Usage:
  python3 build/build.py            # page only
  python3 build/build.py --maps     # also re-render static day maps (needs `staticmap`, uses OSM tiles)
"""
import json, os, sys, html, math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, 'build')
SITE = os.path.join(ROOT, 'site')
NOK = 0.088  # CHF per NOK, ECB 2026-10-21

def nok(x):
    return round(x * NOK, 1)

# ---------------------------------------------------------------- places
POIS = {
  'tromso':          dict(name='特罗姆瑟市中心', local='Tromsø sentrum', ll=(69.6492, 18.9553), desc='北极圈内最大的城市，港口、木屋老街和大教堂都在步行范围内。'),
  'arctic-cathedral':dict(name='北极教堂', local='Ishavskatedralen', ll=(69.6481, 18.9877), desc='三角形白色教堂，从大桥上或对岸拍最好看；外景免费。'),
  'fjellheisen':     dict(name='Fjellheisen 缆车', local='Fjellheisen / Storsteinen', ll=(69.6430, 18.9970), desc='缆车上到海拔 421 m 的观景台，俯瞰全城、大桥和峡湾；傍晚看蓝调，天黑后看极光。'),
  'sommaroy':        dict(name='Sommarøy 海岛', local='Sommarøy', ll=(69.6346, 18.0080), desc='特罗姆瑟西边的小渔岛，白沙滩、浅蓝海水和雪山，坐 422 路 71 分钟。'),
  'ersfjordbotn':    dict(name='Ersfjordbotn 峡湾', local='Ersfjordbotn', ll=(69.6939, 18.6630), desc='峡湾尽头的小村，四周雪山倒映在水里；远离城市灯光，适合日落后等极光。'),
  'telegrafbukta':   dict(name='Telegrafbukta 海湾', local='Telegrafbukta', ll=(69.6293, 18.9175), desc='岛南端的海边石滩，市区最方便的免费看极光点。'),
  'prestvannet':     dict(name='Prestvannet 湖', local='Prestvannet', ll=(69.6611, 18.9330), desc='岛中央的湖，冬天结冰，灯光少，步行可到的看极光点。'),
  'havila':          dict(name='Havila 海岸游轮', local='Havila Capella', ll=(69.6468, 18.9592), desc='挪威海岸航线的游轮，夜里从特罗姆瑟开出，第二天傍晚到斯沃尔韦尔。'),
  'raftsundet':      dict(name='Raftsundet 海峡', local='Raftsundet', ll=(68.43, 14.86), desc='罗弗敦和韦斯特罗伦之间的狭长海峡，两侧雪山贴着船过，下午 15:00 后经过。'),
  'svolvaer':        dict(name='斯沃尔韦尔', local='Svolvær', ll=(68.2343, 14.5683), desc='罗弗敦的主镇和港口，红色渔屋和背后的尖峰山。'),
  'henningsvaer':    dict(name='亨宁斯韦尔渔村', local='Henningsvær', ll=(68.1530, 14.2040), desc='建在一串小岛上的渔村，晾鱼架、海上足球场和咖啡馆。'),
  'stockfish':       dict(name='鳕鱼干架', local='Hjeller (stockfish racks)', ll=(68.1530, 14.2040), desc='3 月正是鳕鱼季，木架上挂满风干的鳕鱼，是罗弗敦冬天的标志画面。'),
  'leknes':          dict(name='莱克内斯', local='Leknes', ll=(68.1470, 13.6110), desc='罗弗敦中部的交通枢纽和购物镇，适合补给。'),
  'ramberg':         dict(name='Ramberg 海滩', local='Rambergstranda', ll=(68.0890, 13.2310), desc='长长的白沙滩，背后是雪山和红色木屋。'),
  'hamnoy':          dict(name='Hamnøy', local='Hamnøy', ll=(67.9473, 13.1310), desc='桥上就能拍到红屋、雪山和海的经典机位。'),
  'reine':           dict(name='雷讷', local='Reine', ll=(67.9330, 13.0890), desc='罗弗敦最有名的渔村；Reinehalsen 观景点看全景，早上光线最好。'),
  'sakrisoy':        dict(name='Sakrisøy 黄房子', local='Sakrisøy', ll=(67.9428, 13.1167), desc='一排黄色渔屋配尖峰 Olstinden，离 Olenilsøya 车站约 400 m。'),
  'a-lofoten':       dict(name='Å 渔村', local='Å i Lofoten', ll=(67.8790, 12.9790), desc='E10 公路的尽头，整村就是一座活的渔村博物馆。'),
  'fiskevaer-museum':dict(name='挪威渔村博物馆', local='Norsk Fiskeværsmuseum', ll=(67.8795, 12.9800), desc='老渔屋、鱼肝油作坊和面包房组成的露天博物馆。'),
  'sorvagen':        dict(name='Sørvågen', local='Sørvågen', ll=(67.8920, 13.0280), desc='安静的小渔村，Tind 海湾一带适合散步。'),
  'moskenes-ferry':  dict(name='Moskenes 渡轮码头', local='Moskenes ferjekai', ll=(67.8999, 13.0447), desc='去博德的渡轮从这里开，步行旅客免费，开船前 45 分钟登记。'),
  'bodo':            dict(name='博德', local='Bodø', ll=(67.2804, 14.4049), desc='北挪威的港口城市，2024 年欧洲文化之都。'),
  'luftfartsmuseum': dict(name='挪威航空博物馆', local='Norsk Luftfartsmuseum', ll=(67.2763, 14.4180), desc='螺旋桨造型的大馆，民航和军用飞机，包括 U-2 和喷火式。'),
  'saltstraumen':    dict(name='Saltstraumen 潮流', local='Saltstraumen', ll=(67.2310, 14.6220), desc='世界最强的潮汐流之一，入流最强时海面出现漩涡；看潮汐表决定时间。'),
  'oslo-opera':      dict(name='奥斯陆歌剧院', local='Operahuset', ll=(59.9075, 10.7531), desc='斜屋顶可以走上去看峡湾和城市，免费；冬季可能因冰雪部分封闭。'),
  'akershus':        dict(name='阿克什胡斯城堡', local='Akershus festning', ll=(59.9076, 10.7363), desc='中世纪城堡，城墙上看奥斯陆峡湾，免费进入。'),
}


# official / tourist-board pages: linked, never copied (their photos are copyrighted)
OFFICIAL = {
  'tromso': ('Visit Tromsø', 'https://www.visittromso.no/'),
  'arctic-cathedral': ('Visit Tromsø', 'https://www.visittromso.no/travel/getting-around/sights'),
  'fjellheisen': ('Fjellheisen 官网', 'https://www.fjellheisen.no/engelsk/fjellheisen-home'),
  'havila': ('Havila 官网', 'https://www.havilavoyages.com/en/sailing-schedule'),
  'raftsundet': ('Visit Norway', 'https://www.visitnorway.no/listings/trollfjord/227089/'),
  'svolvaer': ('Visit Lofoten', 'https://visitlofoten.com/en/'),
  'henningsvaer': ('Visit Lofoten', 'https://visitlofoten.com/en/'),
  'reine': ('Visit Lofoten', 'https://visitlofoten.com/en/place/reine/'),
  'a-lofoten': ('Visit Lofoten', 'https://visitlofoten.com/en/place/a/'),
  'fiskevaer-museum': ('Nordnorge 官方旅游', 'https://nordnorge.com/en/aktivitet/the-norwegian-fishing-village-museum-in-a-brings-the-past-to-life/'),
  'sorvagen': ('Visit Lofoten', 'https://visitlofoten.com/en/place/sorvagen/'),
  'moskenes-ferry': ('Torghatten 官网', 'https://www.torghatten.no/en/our-routes/18-782'),
  'bodo': ('Visit Bodø', 'https://visitbodo.com/en/'),
  'luftfartsmuseum': ('航空博物馆官网', 'https://www.luftfartsmuseum.no/billetter-og-booking'),
  'saltstraumen': ('Visit Bodø', 'https://visitbodo.com/en/saltstraumen'),
  'oslo-opera': ('Visit Norway', 'https://www.visitnorway.com/places-to-go/eastern-norway/oslo/oslo-opera-house'),
  'akershus': ('Forsvarsbygg 官网', 'https://www.forsvarsbygg.no/en/festningene/akershus-fortress'),
}

def maps_url(k):
    p = POIS[k]
    return 'https://www.google.com/maps/search/?api=1&query=' + f"{p['ll'][0]},{p['ll'][1]}"

# ---------------------------------------------------------------- days
# item: t, what, cost (CHF, None = no cost), opt (optional), note, v (verification tag)
DAYS = [
 dict(id='0305', date='03.05', wd='周五', where='日内瓦 → 特罗姆瑟', title='直飞进北极圈', legs=['airport'], pois=['tromso'],
  items=[
   dict(t='19:25–23:20', what='Norwegian DY1613 日内瓦 → 特罗姆瑟直飞', cost=77, note='只带座位下小包；官网加登机箱后 99', v='plan'),
   dict(t='23:34–23:55', what='40 路（或 26/24/42 路）机场 → 市区，买 24 小时票', cost=nok(140), note='24 小时 1 区票 NOK 140，在机场激活，可一直用到周六晚', v='b'),
   dict(t='—', what='Clarion The Edge（积分约 16,000 分）', cost=0, note='订不到时 Airbnb 约 115', v='x'),
   dict(t='—', what='餐饮（机上自备）', cost=10, note='', v=''),
  ], sleep='Clarion The Edge，码头旁，24 小时前台，含早餐'),
 dict(id='0306', date='03.06', wd='周六', where='特罗姆瑟 → 船上', title='Sommarøy、Ersfjordbotn、夜里登船', legs=['sommaroy-out','sommaroy-back','ersfjord-out','ersfjord-back'],
  pois=['sommaroy','ersfjordbotn','fjellheisen','arctic-cathedral','telegrafbukta','prestvannet','havila'],
  items=[
   dict(t='09:00 → 10:11', what='422 路 Prostneset → Sommarøy', cost=0, note='24 小时票已含', v='b'),
   dict(t='12:34 → 14:07', what='422 路回城；退房，行李寄存', cost=nok(100), note='Tromsø Luggage Storage 24 小时 NOK 100；或请酒店前台代存（待确认）', v=''),
   dict(t='14:50 → 15:39', what='42 路 Bankgata → Eidkjosen 换 425 → Ersfjordbotn', cost=0, note='24 小时票已含', v='b'),
   dict(t='15:39–18:48', what='峡湾日落（约 16:50）、蓝调，天黑后等极光', cost=None, note='', v=''),
   dict(t='18:48 → 19:43', what='回城（周六末班）', cost=0, note='', v='b'),
   dict(t='20:00–23:00', what='Fjellheisen 缆车看夜景和极光', cost=nok(645), note='往返 NOK 645；正在建设"Fjellheisen 2.0"，冬季营业待确认；不坐就去 Telegrafbukta / Prestvannet 免费看', v='c'),
   dict(t='23:45–01:15', what='Havila Capella 靠港办理登船，01:15 截止', cost=None, note='', v='a'),
   dict(t='—', what='餐饮', cost=22, note='超市为主（约 NOK 250/天）', v=''),
  ], sleep='Havila 船上（座位票）'),
 dict(id='0307', date='03.07', wd='周日', where='海岸航行 → 斯沃尔韦尔', title='Havila 南下，下午过 Raftsundet', legs=['coastal'], pois=['havila','raftsundet','svolvaer'],
  items=[
   dict(t='01:30 → 18:30', what='Havila 特罗姆瑟 → 斯沃尔韦尔（Harstad 08:00、Sortland 12:30、Stokmarknes 14:15–15:15）', cost=85, note='港到港座位票，价格未核实（参考 NOK 900–1,050）', v='x'),
   dict(t='15:00–18:30', what='待在甲板：Raftsundet 海峡', cost=None, note='', v=''),
   dict(t='晚上', what='港口看极光', cost=None, note='', v=''),
   dict(t='—', what='Fast Hotel Svolvær', cost=66, note='Trip.com 66 / Booking 88，不含早餐', v='plan'),
   dict(t='—', what='餐饮（船上自带补给）', cost=22, note='', v=''),
  ], sleep='Fast Hotel Svolvær'),
 dict(id='0308', date='03.08', wd='周一', where='斯沃尔韦尔 → 莱克内斯', title='亨宁斯韦尔渔村，傍晚跨岛', legs=['henningsvaer-out','henningsvaer-back','leknes'], pois=['svolvaer','henningsvaer','stockfish','leknes'],
  items=[
   dict(t='08:30–10:20', what='港口、Svinøya 红木屋，退房', cost=None, note='', v=''),
   dict(t='10:30 → 11:11', what='743 路 → 亨宁斯韦尔', cost=nok(66), note='2 区 NOK 66；有 ISIC 卡学生半价', v='b'),
   dict(t='14:21 → 14:57', what='743 路返回斯沃尔韦尔', cost=nok(66), note='', v='b'),
   dict(t='15:45 → 17:10', what='741 路 → 莱克内斯', cost=nok(155), note='4 区 NOK 155；错过就坐 300 路 20:10', v='b'),
   dict(t='—', what='Lofoten Overnatting', cost=88, note='3/5 前可免费取消', v='plan'),
   dict(t='—', what='餐饮', cost=25, note='罗弗敦超市少、略贵', v=''),
  ], sleep='Lofoten Overnatting，莱克内斯'),
 dict(id='0309', date='03.09', wd='周二', where='莱克内斯 → 雷讷', title='Ramberg 海滩、Hamnøy、雷讷', legs=['ramberg','hamnoy','reine'], pois=['ramberg','hamnoy','reine'],
  items=[
   dict(t='08:40 → 09:22', what='742 路 → Ramberg 海滩', cost=nok(66), note='2 区', v='b'),
   dict(t='13:20 → 13:45', what='742 路 → Hamnøy，桥上拍红屋', cost=nok(66), note='2 区', v='b'),
   dict(t='14:45 → 14:55', what='772 路 → 雷讷 / 住处', cost=nok(45), note='上学日线路；不开就坐 300 路 16:50', v='c'),
   dict(t='—', what='Moskenes 码头旁 Airbnb（第 1 晚）', cost=57.5, note='2 晚 115，3/8 前可免费取消', v='plan'),
   dict(t='—', what='餐饮', cost=25, note='', v=''),
  ], sleep='Moskenes 码头旁 Airbnb 单间'),
 dict(id='0310', date='03.10', wd='周三', where='雷讷', title='雷讷群岛摄影', legs=['olenilsoy-out','olenilsoy-back'], pois=['reine','sakrisoy'],
  items=[
   dict(t='07:00–11:30', what='Reinehalsen 晨光（日出约 06:50）、港口、晾鱼架', cost=None, note='', v=''),
   dict(t='13:35 → 13:41', what='772 路 → Olenilsøya，走 400 m 到 Sakrisøy', cost=nok(45), note='上学日线路', v='c'),
   dict(t='14:47 → 14:55', what='772 路返回（742 路 13:48、16:53 也可以）', cost=nok(45), note='', v='c'),
   dict(t='晚上', what='雷讷周边看极光', cost=None, note='', v=''),
   dict(t='—', what='Airbnb（第 2 晚）', cost=57.5, note='', v='plan'),
   dict(t='—', what='餐饮', cost=25, note='', v=''),
  ], sleep='Moskenes 码头旁 Airbnb 单间'),
 dict(id='0311', date='03.11', wd='周四', where='Å → 夜渡博德', title='奥镇、索尔沃根，晚上的船', legs=['aa','sorvagen','ferry'], pois=['a-lofoten','fiskevaer-museum','sorvagen','moskenes-ferry'],
  items=[
   dict(t='09:57 → 10:27', what='742 路雷讷 → Å', cost=nok(45), note='', v='b'),
   dict(t='10:30–12:15', what='挪威渔村博物馆', cost=nok(125), opt=True, note='成人 NOK 125 / 学生 95；冬季开放时间待确认', v='c'),
   dict(t='12:20 → 12:26', what='772 路 → Sørvågen，Tind 海湾', cost=nok(45), note='或步行 2.9 km', v='b'),
   dict(t='19:00 → 19:30', what='步行 2.2 km 到 Moskenes 码头', cost=0, note='唯一的晚班车 20:10 才到，赶不上 19:45 登记截止', v=''),
   dict(t='20:30 → 23:45', what='Torghatten 渡轮 → 博德（步行旅客免费）', cost=0, note='座位保证 NOK 65 可选，前一天 20:00 前订', v='a'),
   dict(t='—', what='Smarthotel Bodø（含早餐）', cost=84, note='步行约 1 km', v='plan'),
   dict(t='—', what='餐饮', cost=25, note='', v=''),
  ], sleep='Smarthotel Bodø'),
 dict(id='0312', date='03.12', wd='周五', where='博德 → 奥斯陆', title='按潮汐排的 Saltstraumen', legs=['saltstraumen-out','saltstraumen-back','bodo-airport'], pois=['bodo','luftfartsmuseum','saltstraumen'],
  items=[
   dict(t='上午', what='挪威航空博物馆', cost=nok(195), opt=True, note='成人 NOK 195 / 学生 160；或港口散步（免费）', v=''),
   dict(t='12:32 → 13:10', what='200 路 → Saltstraumen', cost=nok(66), note='2 区', v='a'),
   dict(t='13:10–14:10', what='看入流最强的漩涡（约 13:00–13:45）', cost=None, note='3/10 后用 BarentsWatch 48 小时预报复核', v='c'),
   dict(t='14:10 / 14:53', what='回博德，酒店取行李', cost=nok(66), note='', v='a'),
   dict(t='约 18:00', what='1/2 路去机场（约 6 分钟）', cost=nok(45), note='或步行 1.3 km', v='b'),
   dict(t='19:45 → 21:20', what='SAS SK4123 博德 → 奥斯陆（与次日同一张联程票）', cost=54, note='只带小包；带登机箱约 79', v='plan'),
   dict(t='—', what='奥斯陆机场过夜', cost=0, note='Avinor：24 小时开放', v=''),
   dict(t='—', what='餐饮', cost=22, note='', v=''),
  ], sleep='奥斯陆机场（备选 Comfort Grand Central，现金 118–150）'),
 dict(id='0313', date='03.13', wd='周六', where='奥斯陆 → 日内瓦', title='奥斯陆半天', legs=['oslo-in','oslo-out'], pois=['oslo-opera','akershus'],
  items=[
   dict(t='08:03 → 08:26', what='Vy 火车 机场 → Oslo S', cost=nok(134), note='无学生折扣；Flytoget 学生价 138 也可以', v='b'),
   dict(t='08:30–11:30', what='歌剧院、阿克什胡斯城堡（免费）', cost=None, note='冬季歌剧院屋顶可能因冰雪部分封闭，待确认；城堡冬季 06:00–21:00 开放', v='c'),
   dict(t='11:34 → 11:57', what='Vy 火车回机场', cost=nok(134), note='', v='b'),
   dict(t='13:25 → 16:00', what='SAS SK4631 奥斯陆 → 日内瓦（联程第二段）', cost=0, note='已含在前一天的 54 里', v='plan'),
   dict(t='—', what='餐饮', cost=22, note='', v=''),
  ], sleep='到家'),
]

VTAG = {'a': ('v-a', '官方 2027'), 'b': ('v-b', 'Entur 2027'), 'c': ('v-c', '参考'), 'x': ('v-x', '未核实'), 'plan': ('c-plan', '暂定'), '': None}

# ---------------------------------------------------------------- legs geometry
def rdp(pts, eps):
    if len(pts) < 3:
        return pts
    (y1, x1), (y2, x2) = pts[0], pts[-1]
    dmax, idx = 0, 0
    for i in range(1, len(pts) - 1):
        y0, x0 = pts[i]
        num = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        den = math.hypot(y2 - y1, x2 - x1) or 1e-9
        d = num / den
        if d > dmax:
            dmax, idx = d, i
    if dmax > eps:
        return rdp(pts[:idx + 1], eps)[:-1] + rdp(pts[idx:], eps)
    return [pts[0], pts[-1]]

raw = json.load(open(os.path.join(B, 'legs_raw.json')))
LEGS = {}
for lid, v in raw.items():
    out = []
    for l in v['legs']:
        pts = rdp(l['pts'], 0.0004)
        if l['mode'] == 'foot' and len(pts) < 2:
            continue
        out.append(dict(m=l['mode'], c=l.get('code'), p=pts))
    LEGS[lid] = out
# legs not available from Entur: walking to the ferry (straight line)
LEGS['sorvagen-walk'] = [dict(m='foot', c=None, p=[[67.8915, 13.0267], [67.8999, 13.0447]])]
for d in DAYS:
    if d['id'] == '0311':
        d['legs'].insert(2, 'sorvagen-walk')

credits = json.load(open(os.path.join(B, 'photo_credits.json')))

def has_photo(k):
    return os.path.exists(os.path.join(SITE, 'img', 'poi', k + '.jpg'))

# ---------------------------------------------------------------- render
E = html.escape

def money(x):
    return '—' if x is None else ('0' if x == 0 else f'{x:,.0f}' if x >= 10 else f'{x:.1f}')

def render_day(d):
    rows = []
    sub = opt = 0.0
    for it in d['items']:
        tag = VTAG.get(it.get('v', ''))
        chip = f' <span class="chip {tag[0]}">{tag[1]}</span>' if tag else ''
        c = it.get('cost')
        if c:
            if it.get('opt'):
                opt += c
            else:
                sub += c
        cls = ' class="opt"' if it.get('opt') else ''
        note = f'<small>{E(it["note"])}</small>' if it.get('note') else ''
        price = money(c) + (' <i>可选</i>' if it.get('opt') else '')
        rows.append(f'<tr{cls}><td class="t">{E(it["t"])}</td><td>{E(it["what"])}{chip}{note}</td><td class="num">{price}</td></tr>')
    d['_sub'], d['_opt'] = sub, opt
    tiles = []
    for k in d['pois']:
        p = POIS[k]
        if has_photo(k):
            img = f'<img src="img/poi/{k}.jpg" alt="{E(p["name"])}" loading="lazy">'
        else:
            img = '<span class="ph"><span>点开看官网照片</span></span>'
        tiles.append(f'<button class="tile" type="button" data-poi="{k}">{img}<span class="cap">{E(p["name"])}</span></button>')
    optline = f'；可选另计 {opt:,.0f}' if opt else ''
    return f'''
  <section class="day" id="d{d['id']}">
    <header class="day-h"><span class="date">{d['date']}</span><span class="wd">{d['wd']}</span><span class="where">{E(d['where'])}</span><h3>{E(d['title'])}</h3></header>
    <div class="day-grid">
      <div class="sched">
        <div class="tbl"><table class="plan"><thead><tr><th>时间</th><th>安排</th><th>CHF</th></tr></thead><tbody>{''.join(rows)}</tbody>
        <tfoot><tr><td></td><td>当天小计{optline}</td><td class="num">{sub:,.0f}</td></tr></tfoot></table></div>
        <p class="sleep">{E(d['sleep'])}</p>
      </div>
      <div class="mapbox"><div class="map" data-day="{d['id']}" role="img" aria-label="{d['date']} 路线地图"></div>
        <img class="mapstatic" src="img/maps/day-{d['id']}.jpg" alt="{d['date']} 路线地图" loading="lazy" hidden>
        <p class="maplegend"><span><span class="lg bus"></span>巴士/火车</span><span><span class="lg water"></span>船</span><span><span class="lg foot"></span>步行</span><span><span class="lg poi"></span>景点（可点）</span></p></div>
    </div>
    <div class="tiles">{''.join(tiles)}</div>
  </section>'''

def main():
    base = open(os.path.join(B, 'base_v6.html')).read()
    head = base[:base.find('<div class="wrap">')]
    css_extra = open(os.path.join(B, 'leaflet.css')).read()
    s_book = base[base.find('<h2 id="book">'):base.find('<h2 id="days">')]
    s_rest = base[base.find('<h2 id="stay">'):base.find('<p class="foot">')]
    days_html = ''.join(render_day(d) for d in DAYS)
    total = sum(d['_sub'] for d in DAYS)
    total_opt = sum(d['_opt'] for d in DAYS)
    cat = {'机票': 77 + 54, '住宿': 66 + 88 + 115 + 84, 'Havila 船票': 85}
    food = sum(it['cost'] for d in DAYS for it in d['items'] if it['what'].startswith('餐饮'))
    cat['餐饮'] = food
    cat['缆车'] = nok(645)
    cat['交通（公交、火车）与寄存'] = round(total - sum(cat.values()), 1)
    cat_rows = ''.join(f'<tr><td>{k}</td><td class="num">{v:,.0f}</td></tr>' for k, v in cat.items())
    day_rows = ''.join(f'<tr><td><a href="#d{d["id"]}">{d["date"]} {d["wd"]}</a></td><td>{E(d["where"])}</td><td class="num">{d["_sub"]:,.0f}</td></tr>' for d in DAYS)
    poi_js = {k: dict(n=v['name'], l=v['local'], ll=v['ll'], d=v['desc'], m=maps_url(k), ph=has_photo(k),
                      cr=credits.get(k), of=OFFICIAL.get(k)) for k, v in POIS.items()}
    day_js = {d['id']: dict(legs=[LEGS[l] for l in d['legs'] if l in LEGS], pois=d['pois']) for d in DAYS}

    page = head.replace('<title>北极圈冬季行程 2027</title>', '<title>北极圈冬季行程 2027</title>')
    page = page.replace('</style>', EXTRA_CSS + '\n/* Leaflet 1.9.4 (BSD-2) */\n' + css_extra + '\n</style>')
    page += f'''<div class="wrap">
  <p class="eyebrow">特罗姆瑟 · 罗弗敦 · 博德 · 奥斯陆 · 2027 年 3 月</p>
  <h1>北极圈冬季行程：最终方案</h1>
  <p class="lede">方案 C：<b>03.05 周五 – 03.13 周六，9 天</b>。每天一张路线图、一张带价格的行程表，点照片看景点介绍。截至 2026-10-21 没有任何预订或付款，所有条目均为「暂定」。</p>
  <div class="stats">
    <div class="stat"><b>9 天</b><span>周五晚出发，周六 16:00 到家</span></div>
    <div class="stat"><b>≈ CHF {total:,.0f}</b><span>全程必要花费，含餐饮（只带小包）</span></div>
    <div class="stat"><b>+ CHF {total_opt:,.0f}</b><span>可选门票（两个博物馆）</span></div>
    <div class="stat"><b>16,000 分</b><span>Choice 积分，特罗姆瑟 1 晚</span></div>
  </div>
  <nav class="nav" aria-label="页面目录">
    <a href="#overview">总览地图</a><a href="#book">预订顺序</a><a href="#days">逐日行程</a><a href="#cost">费用</a><a href="#stay">住宿</a><a href="#risks">风险</a><a href="#diff">与原计划差异</a><a href="#log">决策记录</a>
  </nav>

  <h2 id="overview">总览地图</h2>
  <div class="mapbox wide"><div class="map" data-day="all" role="img" aria-label="全程路线地图"></div>
    <img class="mapstatic" src="img/maps/route-map.jpg" alt="全程路线示意图" loading="lazy" hidden></div>
  <p class="note" style="margin-top:10px">巴士、游轮、渡轮和火车线路来自 Entur 的实际走向（游轮只有停靠港之间的连线）。在 claude.ai 上打开时，在线地图无法加载，会自动换成静态图。</p>

  {s_book}
  <h2 id="days">逐日行程</h2>
  <div class="legend">
    <span><span class="chip v-a">官方 2027</span> 运营方已公布 2027 年 3 月时刻</span>
    <span><span class="chip v-b">Entur 2027</span> Entur 已有当天数据，2 月复核</span>
    <span><span class="chip v-c">参考</span> 待官方确认</span>
    <span><span class="chip v-x">未核实</span> 被拦截或缺数据</span>
    <span><span class="chip c-plan">暂定</span> 计划采用，未预订</span>
  </div>
  <p class="note" style="margin-top:10px">价格单位 CHF（1 NOK = 0.088）。罗弗敦和博德的巴士按成人价；有 ISIC 国际学生证可半价（UNIGE 学生卡单独不被 Reis Nordland 接受）。特罗姆瑟 18–29 岁按"青年"票价，24 小时票更划算。</p>
  {days_html}

  <h2 id="cost">费用汇总（CHF，单人）</h2>
  <div class="cost-grid">
    <div class="tbl"><table><thead><tr><th>类别</th><th>CHF</th></tr></thead><tbody>{cat_rows}</tbody>
      <tfoot><tr><td>合计</td><td class="num">{total:,.0f}</td></tr></tfoot></table></div>
    <div class="tbl"><table><thead><tr><th>日期</th><th>行程</th><th>CHF</th></tr></thead><tbody>{day_rows}</tbody>
      <tfoot><tr><td></td><td>合计</td><td class="num">{total:,.0f}</td></tr></tfoot></table></div>
  </div>
  <ul class="risks">
    <li>带 1 件登机箱：+约 CHF 47（Norwegian 官网加购约 20；SAS 经 Flysmarter +25）。</li>
    <li>积分房订不到：特罗姆瑟改 Airbnb 约 +115。</li>
    <li>餐饮按超市为主约 NOK 250/天估算；每天吃一顿便宜餐馆约 NOK 450/天，全程约 +CHF 150。</li>
    <li>有 ISIC 学生证：罗弗敦和博德巴士减半，全程约 -CHF 30。</li>
    <li>有条件的追光团另计约 CHF 96–140。</li>
  </ul>

  {s_rest}
  <p class="foot">查于 2026-10-21。没有任何预订或付款。照片来自 Wikimedia Commons，作者和许可证见每张照片说明；地图 © OpenStreetMap 贡献者。</p>
</div>

<dialog id="lb" aria-labelledby="lb-title">
  <form method="dialog"><button class="lb-close" aria-label="关闭">×</button></form>
  <div class="lb-img"></div>
  <div class="lb-body">
    <h3 id="lb-title"></h3><p class="lb-local"></p><p class="lb-desc"></p>
    <p class="lb-links"><a class="lb-off" target="_blank" rel="noopener"></a><a class="lb-map" target="_blank" rel="noopener">Google 地图（含游客照片）</a></p>
    <p class="lb-credit"></p>
  </div>
</dialog>

<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script>
const POIS = {json.dumps(poi_js, ensure_ascii=False)};
const DAYS = {json.dumps(day_js, ensure_ascii=False)};
{JS}
</script>
'''
    open(os.path.join(SITE, 'index.html'), 'w').write(page)
    json.dump(day_js, open(os.path.join(SITE, 'img', 'maps', 'days.json'), 'w'), ensure_ascii=False)
    print('total', round(total), 'optional', round(total_opt), 'bytes', len(page))
    if '--maps' in sys.argv:
        static_maps(day_js)

COLORS = {'bus': '#2f5d73', 'rail': '#6b4fa0', 'water': '#a63a2b', 'foot': '#7d8a94', 'coach': '#2f5d73'}

def static_maps(day_js):
    from staticmap import StaticMap, Line, CircleMarker
    for did, v in day_js.items():
        m = StaticMap(900, 560, padding_x=40, padding_y=40, url_template='https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                      headers={'User-Agent': 'TripPlannerStaticMap/1.0 (personal, low volume)'})
        for legs in v['legs']:
            for l in legs:
                m.add_line(Line([(p[1], p[0]) for p in l['p']], COLORS.get(l['m'], '#2f5d73'), 3 if l['m'] == 'foot' else 5))
        for k in v['pois']:
            lat, lon = POIS[k]['ll']
            m.add_marker(CircleMarker((lon, lat), '#ffffff', 14))
            m.add_marker(CircleMarker((lon, lat), '#a63a2b', 9))
        m.render().convert('RGB').save(os.path.join(SITE, 'img', 'maps', f'day-{did}.jpg'), quality=78, optimize=True)
        print('map', did)

EXTRA_CSS = '''
.day{display:block;padding:22px 0;border-bottom:1px solid var(--line)}
.day-h{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 12px;margin-bottom:12px}
.day-h .date{font-family:var(--display);font-size:24px;font-weight:800;color:var(--ink)}
.day-h .wd{font-family:var(--mono);font-size:13px;color:var(--muted)}
.day-h .where{color:var(--accent);font-weight:700;font-size:14px}
.day-h h3{flex-basis:100%;font-size:17px}
.day-grid{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:16px;align-items:start}
.sched{min-width:0}
table.plan{min-width:0}
table.plan td.t{font-family:var(--mono);font-size:12.5px;color:var(--fjord);white-space:nowrap}
table.plan td small{display:block;color:var(--muted);font-size:12.5px}
table.plan tr.opt td{color:var(--muted)}
table.plan i{font-style:normal;font-size:11px;color:var(--muted)}
tfoot td{font-weight:700;background:var(--bg)}
.mapbox{min-width:0}
.map{height:340px;border:1px solid var(--line);background:var(--fjord-soft)}
.mapbox.wide .map{height:440px}
.mapstatic{width:100%;border:1px solid var(--line);display:block}
.mapstatic[hidden],.map[hidden]{display:none}
.maplegend{font-size:12px;color:var(--muted);margin-top:6px;display:flex;flex-wrap:wrap;gap:4px 14px;align-items:center}
.maplegend>span{white-space:nowrap}
.lg{display:inline-block;width:18px;height:4px;vertical-align:middle;margin-right:2px}
.lg.bus{background:#2f5d73}.lg.water{background:#a63a2b}.lg.foot{background:none;height:0;border-top:3px dashed #7d8a94}
.lg.poi{width:10px;height:10px;border-radius:50%;background:#a63a2b;border:2px solid #fff;box-shadow:0 0 0 1px #a63a2b}
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin-top:14px}
.tile{all:unset;cursor:pointer;display:grid;background:var(--surface);border:1px solid var(--line)}
.tile:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.tile img,.tile .ph{width:100%;aspect-ratio:3/2;object-fit:cover;display:block;max-width:100%}
.tile .ph{background:linear-gradient(135deg,var(--fjord-soft),var(--accent-soft));display:grid;place-items:center;font-size:12.5px;color:var(--fjord)}
.tile .cap{font-size:13px;padding:6px 8px;font-weight:500}
.tile:hover .cap{color:var(--accent)}
.cost-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.cost-grid table{min-width:0}
dialog#lb{max-width:min(880px,94vw);width:100%;padding:0;border:none;background:var(--surface);color:var(--ink)}
dialog#lb::backdrop{background:rgba(10,16,22,.72)}
.lb-img img{width:100%;max-height:62vh;object-fit:cover;display:block}
.lb-img .ph{display:block;height:160px;background:linear-gradient(135deg,var(--fjord-soft),var(--accent-soft))}
.lb-body{padding:14px 18px 18px;display:grid;gap:6px}
.lb-local{font-family:var(--mono);font-size:12.5px;color:var(--muted)}
.lb-credit{font-size:12px;color:var(--muted)}
.lb-links{display:flex;flex-wrap:wrap;gap:6px 16px}
.lb-links a[hidden]{display:none}
.lb-close{position:absolute;right:10px;top:8px;width:36px;height:36px;border-radius:50%;border:none;background:rgba(0,0,0,.55);color:#fff;font-size:22px;cursor:pointer;z-index:2}
dialog#lb{position:fixed}
.leaflet-container{font-family:var(--body)}
@media (max-width:760px){.day-grid{grid-template-columns:1fr}.map{height:280px}}
'''

JS = r'''
const COL={bus:'#2f5d73',coach:'#2f5d73',rail:'#6b4fa0',water:'#a63a2b',foot:'#7d8a94'};
function esc(s){return String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
const lb=document.getElementById('lb');
function openPoi(k){
  const p=POIS[k]; if(!p) return;
  lb.querySelector('.lb-img').innerHTML=p.ph?`<img src="img/poi/${k}.jpg" alt="${esc(p.n)}">`:'<span class="ph"></span>';
  lb.querySelector('#lb-title').textContent=p.n;
  lb.querySelector('.lb-local').textContent=p.l;
  lb.querySelector('.lb-desc').textContent=p.d;
  lb.querySelector('.lb-map').href=p.m;
  const of=lb.querySelector('.lb-off'); if(p.of){of.hidden=false;of.textContent=p.of[0]+' 介绍与照片';of.href=p.of[1];}else{of.hidden=true;}
  const cr=p.cr; lb.querySelector('.lb-credit').innerHTML=cr?`照片：${esc(cr.artist||'未署名')} · ${esc(cr.license)} · <a href="${esc(cr.page)}" target="_blank" rel="noopener">Wikimedia Commons</a>`:'这里还没有可转载的照片：点上面的官网或 Google 地图链接查看。';
  if(lb.showModal) lb.showModal(); else lb.setAttribute('open','');
}
document.querySelectorAll('.tile').forEach(b=>b.addEventListener('click',()=>openPoi(b.dataset.poi)));
lb.addEventListener('click',e=>{if(e.target===lb) lb.close();});

function fallback(el){el.hidden=true; const img=el.parentElement.querySelector('.mapstatic'); if(img) img.hidden=false;}
function drawMap(el){
  if(typeof L==='undefined'){fallback(el);return;}
  const id=el.dataset.day;
  const sets=id==='all'?Object.entries(DAYS).filter(([k])=>k!=='0313').map(([,v])=>v):[DAYS[id]];
  const map=L.map(el,{scrollWheelZoom:false,attributionControl:true});
  let ok=false;
  const tl=L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:17,attribution:'© OpenStreetMap'});
  tl.on('tileload',()=>{ok=true;}); tl.addTo(map);
  const b=L.latLngBounds([]);
  sets.forEach(s=>{
    s.legs.forEach(legs=>legs.forEach(l=>{
      const pl=L.polyline(l.p,{color:COL[l.m]||'#2f5d73',weight:l.m==='foot'?3:5,opacity:.9,dashArray:l.m==='foot'?'4 6':null}).addTo(map);
      if(l.c) pl.bindTooltip(l.c+' 路',{sticky:true});
      l.p.forEach(p=>b.extend(p));
    }));
    s.pois.forEach(k=>{const p=POIS[k];
      L.circleMarker(p.ll,{radius:7,color:'#ffffff',weight:2,fillColor:'#a63a2b',fillOpacity:1}).addTo(map)
        .bindTooltip(p.n).on('click',()=>openPoi(k));
      b.extend(p.ll);});
  });
  if(b.isValid()) map.fitBounds(b,{padding:[24,24],maxZoom:13});
  setTimeout(()=>{if(!ok){map.remove();fallback(el);}},4000);
}
const io='IntersectionObserver' in window?new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){io.unobserve(e.target);drawMap(e.target);}}),{rootMargin:'300px'}):null;
document.querySelectorAll('.map').forEach(el=>io?io.observe(el):drawMap(el));
'''

if __name__ == '__main__':
    main()

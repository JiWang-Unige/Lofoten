# 北极圈冬季行程 2027（特罗姆瑟 · 罗弗敦 · 博德 · 奥斯陆）

最终方案：**方案 C，2027-03-05（周五）至 03-13（周六），9 天**。
现金估算约 CHF 770（只带座位下小包，不含餐饮），带 1 件登机箱约 CHF 815，另用 16,000 Choice 积分。

截至 2026-10-21：**没有任何预订或付款**。所有条目都是「暂定」。

## 目录结构

| 路径 | 内容 |
|---|---|
| `site/index.html` | 最终行程网页：每日路线地图（可交互，claude.ai 上自动换成静态图）、带价格的行程表、景点照片卡片、预订顺序、费用、住宿、风险、与原计划的差异、A/B/C 决策记录 |
| `site/img/` | 景点照片（Wikimedia Commons，作者和许可证见 `build/photo_credits.json` 和网页说明）与静态地图（© OpenStreetMap 贡献者） |
| `build/build.py` | 生成网页的脚本：行程、价格、景点都写在脚本开头的数据里，改完运行 `python3 build/build.py`（加 `--maps` 重画静态地图，需要 `pip install staticmap`） |
| `docs/decision-log.md` | 决策记录：日期、路线结构、斯瓦尔巴、付费活动、A 对 C 的取舍 |
| `docs/research-notes.md` | 各条调研的结论汇总，附来源和核实等级 |
| `data/original/` | 圆周旅迹原计划 v4（已去除用户 ID、昵称、头像、分享码） |
| `data/evidence/transport/` | Entur API 原始查询结果（JSON）与运营商时刻表 PDF（Svipper、Reis Nordland、Torghatten、Havila） |
| `data/evidence/tide/` | Kartverket 博德潮汐预测（2027-03-11 至 13）与 Saltstraumen 2027 潮汐表 |
| `data/evidence/flights/` | Google Flights 航班详情页的文本记录（第一行是来源 URL） |

## 逐日概要

| 日期 | 行程 | 住宿 |
|---|---|---|
| 03-05 周五 | DY1613 日内瓦 19:25 → 特罗姆瑟 23:20 直飞；26/40/24/42 路进城 | Clarion The Edge（积分） |
| 03-06 周六 | 422 路 Sommarøy（09:00 → 10:11，12:34 → 14:07）；42 路换车去 Ersfjordbotn（14:50 → 15:39，18:48 回）；晚上缆车或免费点看极光；23:45–01:15 登 Havila | 船上 |
| 03-07 周日 | Havila 01:30 → 斯沃尔韦尔 18:30（下午过 Raftsundet） | Fast Hotel Svolvær |
| 03-08 周一 | 743 路 10:30 → 亨宁斯韦尔，14:21 回；741 路 15:45 → 莱克内斯 17:10 | Lofoten Overnatting |
| 03-09 周二 | 742 路 08:40 → Ramberg；13:20 → Hamnøy；772 路 14:45 → 雷讷（上学日线路，备选 300 路 16:50） | Moskenes 码头旁 Airbnb |
| 03-10 周三 | 雷讷晨光；772 路 13:35 → Olenilsøya / Sakrisøy，14:47 回 | 同上 |
| 03-11 周四 | 742 路 09:57 → Å；772 路 12:20 → Sørvågen；步行 2.2 km 到 Moskenes 码头（19:45 前登记）；渡轮 20:30 → 博德 23:45 | Smarthotel Bodø |
| 03-12 周五 | 上午港口或航空博物馆；200 路 12:32 → Saltstraumen（入流最强约 13:00–13:45）；SAS SK4123 19:45 → 奥斯陆 | 奥斯陆机场过夜 |
| 03-13 周六 | 奥斯陆半天；SAS SK4631 13:25 → 日内瓦 16:00 | — |

## 预订顺序

1. **现在**：去程 DY1613（价格在涨；要带登机箱就在 Norwegian 官网订）
2. **现在**：Choice 积分房 Clarion The Edge 03-05（需登录确认积分价）
3. **现在**：回程 SAS 联程 SK4123 + SK4631（先在 flysas.com 对比官网价）
4. **现在**：Havila 03-07 特罗姆瑟 → 斯沃尔韦尔（需人工查票价）
5. **现在**：可免费取消的罗弗敦和博德住宿
6. **2027 年 2 月中**：复核 Reis Nordland 新时刻表、Moskenes 校历（772 路）、缆车冬季营业
7. **出发前 1 周**：装 Svipper 和 Reis App；决定周六追光团（只报能保证 00:30 前回城的团）
8. **03-10 20:00 前**：可选渡轮座位保证 NOK 65
9. **03-10 至 03-11**：BarentsWatch 查 Saltstraumen 48 小时潮流预报

## 核实等级

- **官方 2027**：运营方已公布 2027 年 3 月时刻（Havila、Torghatten、Reis Nordland 200 路）
- **Entur 2027**：Entur 已有当天数据，但运营方 PDF 只到 2027 年 1 月，2 月需复核
- **参考**：参考，待官方确认
- **未核实**：被网站拦截或缺数据（Choice 积分价、Havila 票价、SAS 官网价）

## 隐私

仓库默认私有。这里不放订单号、证件号、登录信息或个人联系方式。原计划数据已去除用户 ID、昵称、头像和分享码。公开仓库前需要先确认。

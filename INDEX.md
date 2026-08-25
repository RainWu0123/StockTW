# 台股研究全庫 Index（法人研究＋LLMwiki 薄入口）

更新日期：2026-08-25
根目錄：`/home/ubuntu/investment/`

> 使用方式：先用本檔按代碼、產業／供應鏈、主題查找，再進入完整研究檔。薄入口只負責定位與聯想，不取代研究報告。

## 研究狀態

- 已掃描股票研究檔：**127 檔**（截至 2026-08-25，含新增 2351 順德、7788 松川精密、3042 晶技、2455 全新、4919 新唐、3105 穩懋、3264 欣銓、2324 仁寶、6488 環球晶、6182 合晶、3532 台勝科）
- 批次 A：15/15 完成。
- 批次 B：19/19 完成。
- 研究唯一落點：`research/{代碼}_{公司}.md`
- 即時資料 `data/live.json` 僅供查價，本 Index 不寫入或修改。

## 依供應鏈／主題定位

- **AI**：[1101 台泥](research/1101_台泥.md)、[1301 台塑](research/1301_台塑.md)、[1303 南亞](research/1303_南亞.md)、[1326 台化](research/1326_台化.md)、[2059 川湖](research/2059_川湖.md)、[2301 光寶科](research/2301_光寶科.md)、[2303 聯電](research/2303_聯電.md)、[2308 台達電](research/2308_台達電.md)、[2313 華通](research/2313_華通.md)、[2317 鴻海](research/2317_鴻海.md)、[2327 國巨](research/2327_國巨.md)、[2330 台積電](research/2330_台積電.md)、[2337 旺宏](research/2337_旺宏.md)、[2344 華邦電](research/2344_華邦電.md)、[2345 智邦](research/2345_智邦.md)、[2356 英業達](research/2356_英業達.md)、[2357 華碩](research/2357_華碩.md)、[2360 致茂](research/2360_致茂.md)、[2363 矽統](research/2363_矽統.md)、[2368 金像電](research/2368_金像電.md)、[2375 凱美](research/2375_凱美.md)、[2376 技嘉](research/2376_技嘉.md)、[2377 微星](research/2377_微星.md)、[2379 瑞昱](research/2379_瑞昱.md)、[2382 廣達](research/2382_廣達.md)、[2383 台光電](research/2383_台光電.md)、[2395 研華](research/2395_研華.md)、[2408 南亞科](research/2408_南亞科.md)、[2412 中華電](research/2412_中華電.md)、[2449 京元電子](research/2449_京元電子.md)、[2454 聯發科](research/2454_聯發科.md)、[2610 華航](research/2610_華航.md)、[2618 長榮航](research/2618_長榮航.md)、[2881 富邦金](research/2881_富邦金.md)、[2885 元大金](research/2885_元大金.md)、[2892 第一金](research/2892_第一金.md)、[3005 神基](research/3005_神基.md)、[3008 大立光](research/3008_大立光.md)、[3017 奇鋐](research/3017_奇鋐.md)、[3026 禾伸堂](research/3026_禾伸堂.md)、[3034 聯詠](research/3034_聯詠.md)、[3037 欣興](research/3037_欣興.md)、[3045 台灣大](research/3045_台灣大.md)、[3081 聯亞](research/3081_聯亞.md)、[3231 緯創](research/3231_緯創.md)、[3324 雙鴻](research/3324_雙鴻.md)、[3443 創意](research/3443_創意.md)、[3449 京元電](research/3449_京元電.md)、[3529 力旺](research/3529_力旺.md)、[3533 嘉澤](research/3533_嘉澤.md)、[3653 健策](research/3653_健策.md)、[3661 世芯-KY](research/3661_世芯-KY.md)、[3665 貿聯-KY](research/3665_貿聯-KY.md)、[3706 神達](research/3706_神達.md)、[3711 日月光](research/3711_日月光.md)、[4904 遠傳](research/4904_遠傳.md)、[4938 和碩](research/4938_和碩.md)、[4953 緯軟](research/4953_緯軟.md)、[4958 臻鼎-KY](research/4958_臻鼎-KY.md)、[4971 IET-KY](research/4971_IET-KY.md)、[4979 華星光](research/4979_華星光.md)、[5243 乙盛-KY](research/5243_乙盛-KY.md)、[5269 祥碩_wrong](research/5269_祥碩_wrong.md)、[5274 信驊](research/5274_信驊.md)、[5880 合庫金](research/5880_合庫金.md)、[6166 凌華](research/6166_凌華.md)、[6196 帆宣](research/6196_帆宣.md)、[6223 旺矽](research/6223_旺矽.md)、[6239 力成](research/6239_力成.md)、[6278 台表科](research/6278_台表科.md)、[6285 啟碁](research/6285_啟碁.md)、[6415 矽力-KY](research/6415_矽力-KY.md)、[6442 光聖](research/6442_光聖.md)、[6515 穎崴](research/6515_穎崴.md)、[6584 南俊國際](research/6584_南俊國際.md)、[6669 緯穎](research/6669_緯穎.md)、[6715 嘉基](research/6715_嘉基.md)、[6770 力積電](research/6770_力積電.md)、[6805 富世達](research/6805_富世達.md)、[6830 汎銓](research/6830_汎銓.md)、[7610 聯友金屬創](research/7610_聯友金屬創.md)、[8046 南電](research/8046_南電.md)、[8210 勤誠](research/8210_勤誠.md)、[8299 群聯](research/8299_群聯.md)
- **CPO**：[2301 光寶科](research/2301_光寶科.md)、[2303 聯電](research/2303_聯電.md)、[2313 華通](research/2313_華通.md)、[2317 鴻海](research/2317_鴻海.md)、[2345 智邦](research/2345_智邦.md)、[2360 致茂](research/2360_致茂.md)、[2449 京元電子](research/2449_京元電子.md)、[2454 聯發科](research/2454_聯發科.md)、[3008 大立光](research/3008_大立光.md)、[3017 奇鋐](research/3017_奇鋐.md)、[3081 聯亞](research/3081_聯亞.md)、[3163 波若威](research/3163_波若威.md)、[3443 創意](research/3443_創意.md)、[3449 京元電](research/3449_京元電.md)、[3533 嘉澤](research/3533_嘉澤.md)、[3711 日月光](research/3711_日月光.md)、[4971 IET-KY](research/4971_IET-KY.md)、[4979 華星光](research/4979_華星光.md)、[6187 萬潤](research/6187_萬潤.md)、[6223 旺矽](research/6223_旺矽.md)、[6239 力成](research/6239_力成.md)、[6442 光聖](research/6442_光聖.md)、[6515 穎崴](research/6515_穎崴.md)、[6715 嘉基](research/6715_嘉基.md)、[6830 汎銓](research/6830_汎銓.md)
- **NPO**：[2313 華通](research/2313_華通.md)、[2345 智邦](research/2345_智邦.md)、[3163 波若威](research/3163_波若威.md)、[3533 嘉澤](research/3533_嘉澤.md)、[6715 嘉基](research/6715_嘉基.md)
- **CoWoS**：[2108 南帝](research/2108_南帝.md)、[2303 聯電](research/2303_聯電.md)、[2330 台積電](research/2330_台積電.md)、[2454 聯發科](research/2454_聯發科.md)、[3443 創意](research/3443_創意.md)、[3673 TPK-KY](research/3673_TPK-KY.md)、[3711 日月光](research/3711_日月光.md)、[6187 萬潤](research/6187_萬潤.md)、[6196 帆宣](research/6196_帆宣.md)、[6239 力成](research/6239_力成.md)、[6770 力積電](research/6770_力積電.md)
- **矽光子**：[2303 聯電](research/2303_聯電.md)、[3163 波若威](research/3163_波若威.md)、[4979 華星光](research/4979_華星光.md)、[6187 萬潤](research/6187_萬潤.md)、[6515 穎崴](research/6515_穎崴.md)、[6830 汎銓](research/6830_汎銓.md)
- **光通訊**：[2301 光寶科](research/2301_光寶科.md)、[2317 鴻海](research/2317_鴻海.md)、[2360 致茂](research/2360_致茂.md)、[2379 瑞昱](research/2379_瑞昱.md)、[3081 聯亞](research/3081_聯亞.md)、[3529 力旺](research/3529_力旺.md)、[4971 IET-KY](research/4971_IET-KY.md)、[4979 華星光](research/4979_華星光.md)、[6278 台表科](research/6278_台表科.md)、[6715 嘉基](research/6715_嘉基.md)
- **光模組**：[2313 華通](research/2313_華通.md)、[3037 欣興](research/3037_欣興.md)、[3081 聯亞](research/3081_聯亞.md)、[3163 波若威](research/3163_波若威.md)、[4958 臻鼎-KY](research/4958_臻鼎-KY.md)、[4971 IET-KY](research/4971_IET-KY.md)、[4979 華星光](research/4979_華星光.md)、[6278 台表科](research/6278_台表科.md)、[6415 矽力-KY](research/6415_矽力-KY.md)、[6715 嘉基](research/6715_嘉基.md)、[6830 汎銓](research/6830_汎銓.md)
- **散熱**：[2301 光寶科](research/2301_光寶科.md)、[2308 台達電](research/2308_台達電.md)、[2375 凱美](research/2375_凱美.md)、[2449 京元電子](research/2449_京元電子.md)、[3017 奇鋐](research/3017_奇鋐.md)、[3026 禾伸堂](research/3026_禾伸堂.md)、[3324 雙鴻](research/3324_雙鴻.md)、[3449 京元電](research/3449_京元電.md)、[3533 嘉澤](research/3533_嘉澤.md)、[3653 健策](research/3653_健策.md)、[6187 萬潤](research/6187_萬潤.md)
- **液冷**：[2301 光寶科](research/2301_光寶科.md)、[2308 台達電](research/2308_台達電.md)、[2317 鴻海](research/2317_鴻海.md)、[2345 智邦](research/2345_智邦.md)、[2375 凱美](research/2375_凱美.md)、[3017 奇鋐](research/3017_奇鋐.md)、[3324 雙鴻](research/3324_雙鴻.md)、[3533 嘉澤](research/3533_嘉澤.md)、[6584 南俊國際](research/6584_南俊國際.md)、[6669 緯穎](research/6669_緯穎.md)、[6805 富世達](research/6805_富世達.md)、[8210 勤誠](research/8210_勤誠.md)
- **電源**：[2301 光寶科](research/2301_光寶科.md)、[2303 聯電](research/2303_聯電.md)、[2308 台達電](research/2308_台達電.md)、[2317 鴻海](research/2317_鴻海.md)、[2345 智邦](research/2345_智邦.md)、[2360 致茂](research/2360_致茂.md)、[2375 凱美](research/2375_凱美.md)、[3529 力旺](research/3529_力旺.md)、[3665 貿聯-KY](research/3665_貿聯-KY.md)、[4938 和碩](research/4938_和碩.md)、[5243 乙盛-KY](research/5243_乙盛-KY.md)、[6415 矽力-KY](research/6415_矽力-KY.md)、[6770 力積電](research/6770_力積電.md)
- **ABF**：[1303 南亞](research/1303_南亞.md)、[2313 華通](research/2313_華通.md)、[3037 欣興](research/3037_欣興.md)、[4958 臻鼎-KY](research/4958_臻鼎-KY.md)、[8046 南電](research/8046_南電.md)
- **BT**：[1303 南亞](research/1303_南亞.md)、[2313 華通](research/2313_華通.md)、[3037 欣興](research/3037_欣興.md)、[8046 南電](research/8046_南電.md)
- **CCL**：[1303 南亞](research/1303_南亞.md)、[2313 華通](research/2313_華通.md)、[2368 金像電](research/2368_金像電.md)、[2383 台光電](research/2383_台光電.md)、[4938 和碩](research/4938_和碩.md)、[6274 台燿](research/6274_台燿.md)
- **PCB**：[1303 南亞](research/1303_南亞.md)、[2301 光寶科](research/2301_光寶科.md)、[2313 華通](research/2313_華通.md)、[2345 智邦](research/2345_智邦.md)、[2368 金像電](research/2368_金像電.md)、[2383 台光電](research/2383_台光電.md)、[2395 研華](research/2395_研華.md)、[3037 欣興](research/3037_欣興.md)、[3533 嘉澤](research/3533_嘉澤.md)、[4938 和碩](research/4938_和碩.md)、[4958 臻鼎-KY](research/4958_臻鼎-KY.md)、[6166 凌華](research/6166_凌華.md)、[6278 台表科](research/6278_台表科.md)、[8046 南電](research/8046_南電.md)
- **HDI**：[2313 華通](research/2313_華通.md)、[2368 金像電](research/2368_金像電.md)、[3037 欣興](research/3037_欣興.md)、[4958 臻鼎-KY](research/4958_臻鼎-KY.md)、[6278 台表科](research/6278_台表科.md)
- **mSAP**：[2313 華通](research/2313_華通.md)、[4958 臻鼎-KY](research/4958_臻鼎-KY.md)
- **DRAM**：[1303 南亞](research/1303_南亞.md)、[2303 聯電](research/2303_聯電.md)、[2344 華邦電](research/2344_華邦電.md)、[2379 瑞昱](research/2379_瑞昱.md)、[2395 研華](research/2395_研華.md)、[2408 南亞科](research/2408_南亞科.md)、[3034 聯詠](research/3034_聯詠.md)、[3324 雙鴻](research/3324_雙鴻.md)、[3711 日月光](research/3711_日月光.md)、[6239 力成](research/6239_力成.md)、[6278 台表科](research/6278_台表科.md)、[6770 力積電](research/6770_力積電.md)
- **NAND**：[2337 旺宏](research/2337_旺宏.md)、[2344 華邦電](research/2344_華邦電.md)、[2408 南亞科](research/2408_南亞科.md)、[6239 力成](research/6239_力成.md)、[8299 群聯](research/8299_群聯.md)
- **HBM**：[2345 智邦](research/2345_智邦.md)、[2408 南亞科](research/2408_南亞科.md)、[3443 創意](research/3443_創意.md)、[3661 世芯-KY](research/3661_世芯-KY.md)、[3711 日月光](research/3711_日月光.md)、[6196 帆宣](research/6196_帆宣.md)、[6239 力成](research/6239_力成.md)
- **記憶體**：[1560 中砂](research/1560_中砂.md)、[2303 聯電](research/2303_聯電.md)、[2317 鴻海](research/2317_鴻海.md)、[2327 國巨](research/2327_國巨.md)、[2337 旺宏](research/2337_旺宏.md)、[2344 華邦電](research/2344_華邦電.md)、[2345 智邦](research/2345_智邦.md)、[2357 華碩](research/2357_華碩.md)、[2379 瑞昱](research/2379_瑞昱.md)、[2382 廣達](research/2382_廣達.md)、[2395 研華](research/2395_研華.md)、[2404 漢唐](research/2404_漢唐.md)、[2408 南亞科](research/2408_南亞科.md)、[2454 聯發科](research/2454_聯發科.md)、[3008 大立光](research/3008_大立光.md)、[3026 禾伸堂](research/3026_禾伸堂.md)、[3034 聯詠](research/3034_聯詠.md)、[3081 聯亞](research/3081_聯亞.md)、[3231 緯創](research/3231_緯創.md)、[3529 力旺](research/3529_力旺.md)、[3533 嘉澤](research/3533_嘉澤.md)、[3711 日月光](research/3711_日月光.md)、[4904 遠傳](research/4904_遠傳.md)、[4938 和碩](research/4938_和碩.md)、[6239 力成](research/6239_力成.md)、[6278 台表科](research/6278_台表科.md)、[6285 啟碁](research/6285_啟碁.md)、[6669 緯穎](research/6669_緯穎.md)、[6770 力積電](research/6770_力積電.md)、[8299 群聯](research/8299_群聯.md)
- **載板**：[1303 南亞](research/1303_南亞.md)、[2313 華通](research/2313_華通.md)、[2454 聯發科](research/2454_聯發科.md)、[3037 欣興](research/3037_欣興.md)、[4958 臻鼎-KY](research/4958_臻鼎-KY.md)、[5274 信驊](research/5274_信驊.md)、[6278 台表科](research/6278_台表科.md)、[8046 南電](research/8046_南電.md)
- **封測**：[2344 華邦電](research/2344_華邦電.md)、[2360 致茂](research/2360_致茂.md)、[2379 瑞昱](research/2379_瑞昱.md)、[2408 南亞科](research/2408_南亞科.md)、[3034 聯詠](research/3034_聯詠.md)、[3449 京元電](research/3449_京元電.md)、[3673 TPK-KY](research/3673_TPK-KY.md)、[3711 日月光](research/3711_日月光.md)、[5274 信驊](research/5274_信驊.md)、[6239 力成](research/6239_力成.md)、[6515 穎崴](research/6515_穎崴.md)
- **晶圓代工**：[2363 矽統](research/2363_矽統.md)、[2404 漢唐](research/2404_漢唐.md)、[3529 力旺](research/3529_力旺.md)、[6415 矽力-KY](research/6415_矽力-KY.md)
- **伺服器**：[1101 台泥](research/1101_台泥.md)、[2059 川湖](research/2059_川湖.md)、[2301 光寶科](research/2301_光寶科.md)、[2308 台達電](research/2308_台達電.md)、[2313 華通](research/2313_華通.md)、[2317 鴻海](research/2317_鴻海.md)、[2327 國巨](research/2327_國巨.md)、[2337 旺宏](research/2337_旺宏.md)、[2345 智邦](research/2345_智邦.md)、[2356 英業達](research/2356_英業達.md)、[2357 華碩](research/2357_華碩.md)、[2360 致茂](research/2360_致茂.md)、[2368 金像電](research/2368_金像電.md)、[2375 凱美](research/2375_凱美.md)、[2376 技嘉](research/2376_技嘉.md)、[2377 微星](research/2377_微星.md)、[2382 廣達](research/2382_廣達.md)、[2383 台光電](research/2383_台光電.md)、[2395 研華](research/2395_研華.md)、[2408 南亞科](research/2408_南亞科.md)、[2618 長榮航](research/2618_長榮航.md)、[3017 奇鋐](research/3017_奇鋐.md)、[3026 禾伸堂](research/3026_禾伸堂.md)、[3037 欣興](research/3037_欣興.md)、[3231 緯創](research/3231_緯創.md)、[3529 力旺](research/3529_力旺.md)、[3533 嘉澤](research/3533_嘉澤.md)、[3665 貿聯-KY](research/3665_貿聯-KY.md)、[3706 神達](research/3706_神達.md)、[4938 和碩](research/4938_和碩.md)、[4958 臻鼎-KY](research/4958_臻鼎-KY.md)、[5243 乙盛-KY](research/5243_乙盛-KY.md)、[5269 祥碩_wrong](research/5269_祥碩_wrong.md)、[5274 信驊](research/5274_信驊.md)、[6278 台表科](research/6278_台表科.md)、[6584 南俊國際](research/6584_南俊國際.md)、[6669 緯穎](research/6669_緯穎.md)、[6715 嘉基](research/6715_嘉基.md)、[6805 富世達](research/6805_富世達.md)、[8210 勤誠](research/8210_勤誠.md)
- **網通**：[2345 智邦](research/2345_智邦.md)、[2368 金像電](research/2368_金像電.md)、[2379 瑞昱](research/2379_瑞昱.md)、[3037 欣興](research/3037_欣興.md)、[3231 緯創](research/3231_緯創.md)、[6278 台表科](research/6278_台表科.md)、[6285 啟碁](research/6285_啟碁.md)、[8046 南電](research/8046_南電.md)
- **低軌衛星**：[2301 光寶科](research/2301_光寶科.md)、[2313 華通](research/2313_華通.md)、[2383 台光電](research/2383_台光電.md)、[3529 力旺](research/3529_力旺.md)、[4904 遠傳](research/4904_遠傳.md)、[5243 乙盛-KY](research/5243_乙盛-KY.md)、[6274 台燿](research/6274_台燿.md)、[6285 啟碁](research/6285_啟碁.md)
- **工業電腦**：[2395 研華](research/2395_研華.md)、[3005 神基](research/3005_神基.md)、[6166 凌華](research/6166_凌華.md)
- **連接器**：[2317 鴻海](research/2317_鴻海.md)、[3533 嘉澤](research/3533_嘉澤.md)、[6715 嘉基](research/6715_嘉基.md)
- **CPU**：[2317 鴻海](research/2317_鴻海.md)、[2330 台積電](research/2330_台積電.md)、[2356 英業達](research/2356_英業達.md)、[2395 研華](research/2395_研華.md)、[2449 京元電子](research/2449_京元電子.md)、[2454 聯發科](research/2454_聯發科.md)、[3037 欣興](research/3037_欣興.md)、[3231 緯創](research/3231_緯創.md)、[3443 創意](research/3443_創意.md)、[3449 京元電](research/3449_京元電.md)、[3529 力旺](research/3529_力旺.md)、[3533 嘉澤](research/3533_嘉澤.md)、[3653 健策](research/3653_健策.md)、[3661 世芯-KY](research/3661_世芯-KY.md)、[3706 神達](research/3706_神達.md)、[4938 和碩](research/4938_和碩.md)、[6223 旺矽](research/6223_旺矽.md)、[6715 嘉基](research/6715_嘉基.md)、[8046 南電](research/8046_南電.md)
- **手機**：[2317 鴻海](research/2317_鴻海.md)、[2454 聯發科](research/2454_聯發科.md)、[3008 大立光](research/3008_大立光.md)、[3034 聯詠](research/3034_聯詠.md)、[3081 聯亞](research/3081_聯亞.md)、[3231 緯創](research/3231_緯創.md)、[4958 臻鼎-KY](research/4958_臻鼎-KY.md)、[6278 台表科](research/6278_台表科.md)、[6515 穎崴](research/6515_穎崴.md)、[6805 富世達](research/6805_富世達.md)、[8299 群聯](research/8299_群聯.md)
- **面板**：[3034 聯詠](research/3034_聯詠.md)、[3680 家登](research/3680_家登.md)、[3711 日月光](research/3711_日月光.md)、[6166 凌華](research/6166_凌華.md)、[6239 力成](research/6239_力成.md)
- **塑化**：[1301 台塑](research/1301_台塑.md)、[1303 南亞](research/1303_南亞.md)、[1326 台化](research/1326_台化.md)、[6505 台塑化](research/6505_台塑化.md)

## 全庫研究清單

| 代碼 | 公司 | 供應鏈／主題 | Base target | 信心 | 驗證日 | 完整研究 |
|---:|---|---|---:|---|---|---|
| 1101 | 台泥 | 海外水泥、低碳建材、能源、和平電力、Molicel與儲能 | 28 | 中高 | 2026-08-25 | [`research/1101_台泥.md`](research/1101_台泥.md) |
| 1102 | 亞泥 | 水泥、電力、裕民與遠東新轉投資、能源成本、減碳 | 45 | 中 | 2026-08-25 | [`research/1102_亞泥.md`](research/1102_亞泥.md) |
| 1216 | 統一 | 食品製造、統一超、統一中控、消費基礎設施、中國消費 | 85 | 中高 | 2026-08-25 | [`research/1216_統一.md`](research/1216_統一.md) |
| 1301 | 台塑 | 石化循環、PVC與PE、台塑美國、台塑化轉投資、半導體化學品 | 62 | 中 | 2026-08-25 | [`research/1301_台塑.md`](research/1301_台塑.md) |
| 1303 | 南亞 | AI、ABF、BT、CCL、PCB、DRAM、載板、塑化 | 240 | 高 | 2026-08-24 | [`research/1303_南亞.md`](research/1303_南亞.md) |
| 1326 | 台化 | AI、塑化 | 68 | 中 | 2026-08-22 | [`research/1326_台化.md`](research/1326_台化.md) |
| 1560 | 中砂 | 記憶體 | 805 | 高 | 2026-08-22 | [`research/1560_中砂.md`](research/1560_中砂.md) |
| 1590 | 亞德客-KY | 待補主題標籤 | 1600 | 中 | 2026-08-23 | [`research/1590_亞德客-KY.md`](research/1590_亞德客-KY.md) |
| 2002 | 中鋼 | 鋼鐵循環、精緻鋼、台灣內需、產線整併、綠色鋼 | 23 | 中 | 2026-08-25 | [`research/2002_中鋼.md`](research/2002_中鋼.md) |
| 2059 | 川湖 | AI、伺服器 | 12000 | 高 | 2026-08-22 | [`research/2059_川湖.md`](research/2059_川湖.md) |
| 2108 | 南帝 | CoWoS | 33 | 中 | 2026-08-22 | [`research/2108_南帝.md`](research/2108_南帝.md) |
| 2301 | 光寶科 | AI、ASIC、CPO、光通訊、散熱、液冷、電源、PCB | 280 | 高 | 2026-08-24 | [`research/2301_光寶科.md`](research/2301_光寶科.md) |
| 2303 | 聯電 | AI、CPO、CoWoS、矽光子、電源、DRAM、記憶體 | 131 | 中高 | 2026-08-24 | [`research/2303_聯電.md`](research/2303_聯電.md) |
| 2308 | 台達電 | AI、散熱、液冷、電源、伺服器 | 2400 | 高 | 2026-08-24 | [`research/2308_台達電.md`](research/2308_台達電.md) |
| 2312 | 金寶 | EMS、儲存設備、網通、印表機、AI伺服器L10、HVDC電源、全球製造 | 38 | 中 | 2026-08-25 | [`research/2312_金寶.md`](research/2312_金寶.md) |
| 2313 | 華通 | AI、CPO、NPO、光模組、ABF、BT、CCL、PCB | 324 | 高 | 2026-08-24 | [`research/2313_華通.md`](research/2313_華通.md) |
| 2317 | 鴻海 | AI、ASIC、CPO、光通訊、液冷、電源、記憶體、伺服器 | 415 | 高 | 2026-08-24 | [`research/2317_鴻海.md`](research/2317_鴻海.md) |
| 2327 | 國巨 | AI、記憶體、伺服器 | 1280 | 高 | 2026-08-24 | [`research/2327_國巨.md`](research/2327_國巨.md) |
| 2330 | 台積電 | AI、ASIC、CoWoS、CPU | 3100 | 高 | 2026-08-24 | [`research/2330_台積電.md`](research/2330_台積電.md) |
| 2337 | 旺宏 | NOR Flash、SLC NAND、eMMC、AI伺服器、車用記憶體、擴產 | 180 | 中高 | 2026-08-25 | [`research/2337_旺宏.md`](research/2337_旺宏.md) |
| 2344 | 華邦電 | AI、DRAM、NAND、記憶體、封測 | 120 | 高 | 2026-08-24 | [`research/2344_華邦電.md`](research/2344_華邦電.md) |
| 2345 | 智邦 | AI、ASIC、CPO、NPO、液冷、電源、PCB、HBM | 3688 | 高 | 2026-08-24 | [`research/2345_智邦.md`](research/2345_智邦.md) |
| 2348 | 海悅 | 房屋代銷、營建投資、建案完工認列、預售推案、房貸管制 | 105 | 中 | 2026-08-25 | [`research/2348_海悅.md`](research/2348_海悅.md) |
| 2356 | 英業達 | AI、ASIC、伺服器、CPU | 75 | 高 | 2026-08-24 | [`research/2356_英業達.md`](research/2356_英業達.md) |
| 2357 | 華碩 | AI、記憶體、伺服器 | 1050 | 高 | 2026-08-22 | [`research/2357_華碩.md`](research/2357_華碩.md) |
| 2360 | 致茂 | AI、ASIC、CPO、光通訊、電源、封測、伺服器 | 2400 | 中 | 2026-08-23 | [`research/2360_致茂.md`](research/2360_致茂.md) |
| 2363 | 矽統 | MCU、BMS、類比IC、紘康整合、聯電集團資源 | 60 | 中 | 2026-08-25 | [`research/2363_矽統.md`](research/2363_矽統.md) |
| 2368 | 金像電 | AI、ASIC、CCL、PCB、HDI、伺服器、網通 | 1800 | 高 | 2026-08-22 | [`research/2368_金像電.md`](research/2368_金像電.md) |
| 2375 | 凱美 | AI、散熱、液冷、電源、伺服器 | 150 | 中 | 2026-08-22 | [`research/2375_凱美.md`](research/2375_凱美.md) |
| 2376 | 技嘉 | AI、伺服器、顯示卡、主機板 | 500 | 中高 | 2026-08-25 | [`research/2376_技嘉.md`](research/2376_技嘉.md) |
| 2377 | 微星 | AI、電競PC、顯示卡、AI PC、AI伺服器、地端AI | 155 | 中 | 2026-08-25 | [`research/2377_微星.md`](research/2377_微星.md) |
| 2378 | 鴻準 | 待補主題標籤 |  | 低 |  | [`research/2378_鴻準.md`](research/2378_鴻準.md) |
| 2379 | 瑞昱 | AI、光通訊、DRAM、記憶體、封測、網通、Wi-Fi 7、車用乙太網路 | 680 | 中高 | 2026-08-25 | [`research/2379_瑞昱.md`](research/2379_瑞昱.md) |
| 2382 | 廣達 | AI、ASIC、記憶體、伺服器 | 450 | 高 | 2026-08-24 | [`research/2382_廣達.md`](research/2382_廣達.md) |
| 2383 | 台光電 | AI、CCL、PCB、伺服器、低軌衛星 | 10200 | 高 | 2026-08-24 | [`research/2383_台光電.md`](research/2383_台光電.md) |
| 2385 | 群光 | 待補主題標籤 |  | 低 |  | [`research/2385_群光.md`](research/2385_群光.md) |
| 2395 | 研華 | AI、PCB、DRAM、記憶體、伺服器、工業電腦、CPU | 700 | 高 | 2026-08-24 | [`research/2395_研華.md`](research/2395_研華.md) |
| 2404 | 漢唐 | 記憶體、晶圓代工 | 1700 | 高 | 2026-08-24 | [`research/2404_漢唐.md`](research/2404_漢唐.md) |
| 2408 | 南亞科 | AI、DRAM、NAND、HBM、記憶體、封測、伺服器 | 580 | 高 | 2026-08-24 | [`research/2408_南亞科.md`](research/2408_南亞科.md) |
| 2412 | 中華電 | 5G行動、高速寬頻、企業ICT、AIDC、IDC與國際業務、股利 | 145 | 中高 | 2026-08-25 | [`research/2412_中華電.md`](research/2412_中華電.md) |
| 2449 | 京元電子 | AI、ASIC、CPO、散熱、封測、CPU、Burn-in、Rubin | 348 | 中高 | 2026-08-25 | [`research/2449_京元電子.md`](research/2449_京元電子.md) |
| 2455 | 全新 | AI、光通訊、矽光子、手機、光模組 | 240 | 中高 | 2026-08-25 | [`research/2455_全新.md`](research/2455_全新.md) |
| 2454 | 聯發科 | AI、ASIC、CPO、CoWoS、記憶體、載板、CPU、手機 | 6800 | 高 | 2026-08-24 | [`research/2454_聯發科.md`](research/2454_聯發科.md) |
| 2603 | 長榮 | 待補主題標籤 | 230 | 中 | 2026-08-23 | [`research/2603_長榮.md`](research/2603_長榮.md) |
| 2609 | 陽明 | 貨櫃航運、歐美航線、SCFI、船隊與聯盟、燃油與地緣政治 | 68 | 中 | 2026-08-25 | [`research/2609_陽明.md`](research/2609_陽明.md) |
| 2610 | 華航 | AI | 27 | 中 | 2026-08-23 | [`research/2610_華航.md`](research/2610_華航.md) |
| 2615 | 萬海 | 待補主題標籤 | 140 | 中 | 2026-08-23 | [`research/2615_萬海.md`](research/2615_萬海.md) |
| 2618 | 長榮航 | AI、伺服器 | 48 | 中 | 2026-08-23 | [`research/2618_長榮航.md`](research/2618_長榮航.md) |
| 2637 | 慧洋-KY | 待補主題標籤 |  | 低 |  | [`research/2637_慧洋-KY.md`](research/2637_慧洋-KY.md) |
| 2880 | 華南金 | 公股金控、華南銀行、證券與創投、財管、股利 | 33 | 中 | 2026-08-25 | [`research/2880_華南金.md`](research/2880_華南金.md) |
| 2881 | 富邦金 | 壽險金控、富邦人壽、台北富邦銀行、FVOCI、CSM、海外金融 | 155 | 中高 | 2026-08-25 | [`research/2881_富邦金.md`](research/2881_富邦金.md) |
| 2882 | 國泰金 | 壽險金控、國泰世華、IFRS17、外匯與利率、資本市場 | 115 | 中 | 2026-08-25 | [`research/2882_國泰金.md`](research/2882_國泰金.md) |
| 2883 | 凱基金 | 待補主題標籤 | 35 | 高 | 2026-08-22 | [`research/2883_凱基金.md`](research/2883_凱基金.md) |
| 2884 | 玉山金 | 銀行金控、玉山銀行、海外布局、三商壽合併、證券與投信 | 36 | 中高 | 2026-08-25 | [`research/2884_玉山金.md`](research/2884_玉山金.md) |
| 2885 | 元大金 | AI | 60 | 中 | 2026-08-23 | [`research/2885_元大金.md`](research/2885_元大金.md) |
| 2886 | 兆豐金 | 公股金控、兆豐銀行、海外金融、外匯與聯貸、證券與非銀 | 42 | 中 | 2026-08-25 | [`research/2886_兆豐金.md`](research/2886_兆豐金.md) |
| 2887 | 台新新光金 | 待補主題標籤 | 32 | 高 | 2026-08-22 | [`research/2887_台新新光金.md`](research/2887_台新新光金.md) |
| 2890 | 永豐金 | 待補主題標籤 | 40 | 中 | 2026-08-23 | [`research/2890_永豐金.md`](research/2890_永豐金.md) |
| 2891 | 中信金 | 待補主題標籤 | 58 | 高 | 2026-08-22 | [`research/2891_中信金.md`](research/2891_中信金.md) |
| 2892 | 第一金 | AI | 34 | 中 | 2026-08-23 | [`research/2892_第一金.md`](research/2892_第一金.md) |
| 3005 | 神基 | AI、工業電腦 | 150 | 中 | 2026-08-22 | [`research/3005_神基.md`](research/3005_神基.md) |
| 3008 | 大立光 | AI、CPO、記憶體、手機 | 5150 | 高 | 2026-08-24 | [`research/3008_大立光.md`](research/3008_大立光.md) |
| 3017 | 奇鋐 | AI、ASIC、CPO、散熱、液冷、伺服器 | 4005 | 高 | 2026-08-24 | [`research/3017_奇鋐.md`](research/3017_奇鋐.md) |
| 3026 | 禾伸堂 | AI、散熱、記憶體、伺服器 | 900 | 中 | 2026-08-22 | [`research/3026_禾伸堂.md`](research/3026_禾伸堂.md) |
| 3034 | 聯詠 | AI、ASIC、DRAM、記憶體、封測、手機、面板 | 530 | 高 | 2026-08-24 | [`research/3034_聯詠.md`](research/3034_聯詠.md) |
| 3037 | 欣興 | AI、ASIC、光模組、ABF、BT、PCB、HDI、載板 | 1400 | 高 | 2026-08-24 | [`research/3037_欣興.md`](research/3037_欣興.md) |
| 3042 | 晶技 | AI、光通訊、車用、手機、網通 | 240 | 中高 | 2026-08-25 | [`research/3042_晶技.md`](research/3042_晶技.md) |
| 3532 | 台勝科 | AI、矽晶圓、8吋、12吋、HBM、先進封裝 | 180 | 中 | 2026-08-25 | [`research/3532_台勝科.md`](research/3532_台勝科.md) |
| 6182 | 合晶 | AI、矽晶圓、8吋、SiC、GaN、HPC | 125 | 中 | 2026-08-25 | [`research/6182_合晶.md`](research/6182_合晶.md) |
| 6488 | 環球晶 | AI、矽晶圓、SOI、SiC、GaN、矽光子 | 620 | 中高 | 2026-08-25 | [`research/6488_環球晶.md`](research/6488_環球晶.md) |
| 2324 | 仁寶 | AI、伺服器、PC、AI PC、液冷、機櫃 | 42 | 中高 | 2026-08-25 | [`research/2324_仁寶.md`](research/2324_仁寶.md) |
| 3264 | 欣銓 | AI、ASIC、矽光子、晶圓測試、車用、工控 | 310 | 高 | 2026-08-25 | [`research/3264_欣銓.md`](research/3264_欣銓.md) |
| 3045 | 台灣大 | AI | 145 | 中 | 2026-08-22 | [`research/3045_台灣大.md`](research/3045_台灣大.md) |
| 3081 | 聯亞 | AI、CPO、光通訊、光模組、記憶體、手機 | 3000 | 中 | 2026-08-24 | [`research/3081_聯亞.md`](research/3081_聯亞.md) |
| 2351 | 順德 | AI、散熱、電源、車用、連接器 | 105 | 中 | 2026-08-25 | [`research/2351_順德.md`](research/2351_順德.md) |
| 3163 | 波若威 | CPO、NPO、矽光子、光模組 |  | 中 | 2026-08-24 | [`research/3163_波若威.md`](research/3163_波若威.md) |
| 3231 | 緯創 | AI、伺服器、機櫃、ODM、交換器、Vera Rubin、MI450 | 270 | 中高 | 2026-08-25 | [`research/3231_緯創.md`](research/3231_緯創.md) |
| 3324 | 雙鴻 | AI、散熱、液冷、水冷板、CDU、QD、DIMM、ASIC、Rubin | 1350 | 中高 | 2026-08-25 | [`research/3324_雙鴻.md`](research/3324_雙鴻.md) |
| 3443 | 創意 | AI、ASIC、CPO、CoWoS、HBM、CPU | 5600 | 中高 | 2026-08-25 | [`research/3443_創意.md`](research/3443_創意.md) |
| 3449 | 京元電 | AI、ASIC、CPO、散熱、封測、CPU | 380 | 高 | 2026-08-22 | [`research/3449_京元電.md`](research/3449_京元電.md) |
| 3529 | 力旺 | IP授權、eNVM、PUF安全IP、3奈米與2奈米、AI資料中心、權利金 | 3330 | 中高 | 2026-08-25 | [`research/3529_力旺.md`](research/3529_力旺.md) |
| 3533 | 嘉澤 | AI、CPO、NPO、散熱、液冷、PCB、記憶體、伺服器 | 2400 | 高 | 2026-08-24 | [`research/3533_嘉澤.md`](research/3533_嘉澤.md) |
| 3653 | 健策 | AI、散熱、GPU、CPU、ASIC、均熱片 | 6100 | 中高 | 2026-08-25 | [`research/3653_健策.md`](research/3653_健策.md) |
| 3661 | 世芯-KY | AI、ASIC、3奈米、2奈米、CSP、車用ADAS、NRE、量產 | 5800 | 中高 | 2026-08-25 | [`research/3661_世芯-KY.md`](research/3661_世芯-KY.md) |
| 3665 | 貿聯-KY | AI資料中心、線束、HPC、AEC、電源互連、半導體設備、Interplex Datacom | 3300 | 中高 | 2026-08-25 | [`research/3665_貿聯-KY.md`](research/3665_貿聯-KY.md) |
| 3673 | TPK-KY | 觸控模組、奕力IC、TGV玻璃基板、先進封裝、泰國產能 | 70 | 中 | 2026-08-25 | [`research/3673_TPK-KY.md`](research/3673_TPK-KY.md) |
| 3680 | 家登 | AI、EUV、FOUP、先進製程、先進封裝、半導體載具 | 650 | 中高 | 2026-08-25 | [`research/3680_家登.md`](research/3680_家登.md) |
| 3706 | 神達 | AI、伺服器、機櫃、AMD、MI355、全球在地化、AIoT | 125 | 中 | 2026-08-25 | [`research/3706_神達.md`](research/3706_神達.md) |
| 3711 | 日月光 | AI、ASIC、CPO、CoWoS、DRAM、HBM、記憶體、封測 | 750 | 高 | 2026-08-24 | [`research/3711_日月光.md`](research/3711_日月光.md) |
| 4904 | 遠傳 | AI、記憶體、低軌衛星 | 105 | 中 | 2026-08-22 | [`research/4904_遠傳.md`](research/4904_遠傳.md) |
| 4938 | 和碩 | AI、電源、CCL、PCB、記憶體、伺服器、CPU | 95 | 中 | 2026-08-23 | [`research/4938_和碩.md`](research/4938_和碩.md) |
| 4919 | 新唐 | AI、MCU、伺服器、車用、手機 | 105 | 中 | 2026-08-25 | [`research/4919_新唐.md`](research/4919_新唐.md) |
| 3105 | 穩懋 | AI、光通訊、矽光子、手機、低軌衛星 | 360 | 中高 | 2026-08-25 | [`research/3105_穩懋.md`](research/3105_穩懋.md) |
| 4953 | 緯軟 | AI | 160 | 中 | 2026-08-22 | [`research/4953_緯軟.md`](research/4953_緯軟.md) |
| 4958 | 臻鼎-KY | AI、ASIC、光模組、ABF、PCB、HDI、mSAP、載板 | 920 | 高 | 2026-08-22 | [`research/4958_臻鼎-KY.md`](research/4958_臻鼎-KY.md) |
| 4971 | IET-KY | AI、CPO、光通訊、光模組 | 550 | 中 | 2026-08-24 | [`research/4971_IET-KY.md`](research/4971_IET-KY.md) |
| 4979 | 華星光 | AI、CPO、矽光子、光通訊、光模組 | 430 | 中 | 2026-08-23 | [`research/4979_華星光.md`](research/4979_華星光.md) |
| 5243 | 乙盛-KY | AI伺服器機構件、低軌衛星、汽車、新能源、Out of China | 90 | 中 | 2026-08-25 | [`research/5243_乙盛-KY.md`](research/5243_乙盛-KY.md) |
| 5269 | 祥碩_wrong | AI、伺服器 | 1500 | 中 | 2026-08-22 | [`research/5269_祥碩_wrong.md`](research/5269_祥碩_wrong.md) |
| 5274 | 信驊 | AI、ASIC、BMC、載板、封測、伺服器、AST2700、遠端管理 | 20000 | 中高 | 2026-08-25 | [`research/5274_信驊.md`](research/5274_信驊.md) |
| 5515 | 建準 | 待補主題標籤 |  | 低 |  | [`research/5515_建準.md`](research/5515_建準.md) |
| 5880 | 合庫金 | AI | 28 | 中 | 2026-08-23 | [`research/5880_合庫金.md`](research/5880_合庫金.md) |
| 6166 | 凌華 | AI、PCB、工業電腦、面板 | 110 | 中 | 2026-08-22 | [`research/6166_凌華.md`](research/6166_凌華.md) |
| 6187 | 萬潤 | CPO、CoWoS、矽光子、散熱 | 1550 | 高 | 2026-08-24 | [`research/6187_萬潤.md`](research/6187_萬潤.md) |
| 6196 | 帆宣 | AI、CoWoS、HBM | 650 | 高 | 2026-08-22 | [`research/6196_帆宣.md`](research/6196_帆宣.md) |
| 6223 | 旺矽 | AI、ASIC、CPO、CPU、探針卡、MEMS、VPC、測試設備 | 7500 | 中高 | 2026-08-25 | [`research/6223_旺矽.md`](research/6223_旺矽.md) |
| 6239 | 力成 | AI、CPO、CoWoS、DRAM、NAND、HBM、記憶體、封測 | 384 | 高 | 2026-08-24 | [`research/6239_力成.md`](research/6239_力成.md) |
| 6269 | 台郡 | 待補主題標籤 |  | 低 |  | [`research/6269_台郡.md`](research/6269_台郡.md) |
| 6274 | 台燿 | 高階CCL、M7、M8、AI伺服器、800G、1.6T、ASIC、泰國產能 | 2200 | 中高 | 2026-08-25 | [`research/6274_台燿.md`](research/6274_台燿.md) |
| 6278 | 台表科 | AI、光通訊、光模組、PCB、HDI、DRAM、記憶體、載板 | 210 | 中高 | 2026-08-24 | [`research/6278_台表科.md`](research/6278_台表科.md) |
| 6285 | 啟碁 | AI、記憶體、網通、低軌衛星 | 340 | 高 | 2026-08-24 | [`research/6285_啟碁.md`](research/6285_啟碁.md) |
| 6415 | 矽力-KY | AI、PMIC、資料中心、車用、VCORE、光模組 | 480 | 中 | 2026-08-25 | [`research/6415_矽力-KY.md`](research/6415_矽力-KY.md) |
| 6442 | 光聖 | AI、光通訊、CPO、高芯數光纖、資料中心、RF | 2200 | 中 | 2026-08-25 | [`research/6442_光聖.md`](research/6442_光聖.md) |
| 6505 | 台塑化 | 塑化 | 105 | 中 | 2026-07-14 | [`research/6505_台塑化.md`](research/6505_台塑化.md) |
| 6515 | 穎崴 | AI測試介面、Coaxial Socket、HyperSocket、MEMS探針卡、高階封裝 | 11000 | 中高 | 2026-08-25 | [`research/6515_穎崴.md`](research/6515_穎崴.md) |
| 6584 | 南俊國際 | AI、伺服器、滑軌、GB300、Vera Rubin、ASIC、液冷 | 760 | 中 | 2026-08-25 | [`research/6584_南俊國際.md`](research/6584_南俊國際.md) |
| 6669 | 緯穎 | AI、ASIC、液冷、記憶體、伺服器 | 7000 | 高 | 2026-08-24 | [`research/6669_緯穎.md`](research/6669_緯穎.md) |
| 6715 | 嘉基 | AI、CPO、NPO、光通訊、光模組、伺服器、連接器、CPU | 180 | 中 | 2026-08-22 | [`research/6715_嘉基.md`](research/6715_嘉基.md) |
| 6770 | 力積電 | AI、CoWoS、電源、DRAM、記憶體 | 85 | 中 | 2026-08-24 | [`research/6770_力積電.md`](research/6770_力積電.md) |
| 6805 | 富世達 | AI、ASIC、液冷、伺服器、手機 | 2615 | 高 | 2026-08-22 | [`research/6805_富世達.md`](research/6805_富世達.md) |
| 6830 | 汎銓 | AI、CPO、矽光子、光模組 | 520 | 中 | 2026-08-23 | [`research/6830_汎銓.md`](research/6830_汎銓.md) |
| 7610 | 聯友金屬創 | AI |  | 中 | 2026-08-22 | [`research/7610_聯友金屬創.md`](research/7610_聯友金屬創.md) |
| 7769 | 鴻勁 | 待補主題標籤 |  | 低 |  | [`research/7769_鴻勁.md`](research/7769_鴻勁.md) |
| 8046 | 南電 | AI、ASIC、ABF、BT、PCB、載板、網通、CPU | 1600 | 高 | 2026-08-24 | [`research/8046_南電.md`](research/8046_南電.md) |
| 7788 | 松川精密 | AI、電源、車用、繼電器 | 320 | 中高 | 2026-08-25 | [`research/7788_松川精密.md`](research/7788_松川精密.md) |
| 8210 | 勤誠 | AI、ASIC、液冷、伺服器 | 1482 | 高 | 2026-08-22 | [`research/8210_勤誠.md`](research/8210_勤誠.md) |
| 8299 | 群聯 | AI、NAND、記憶體、手機 | 2750 | 中 | 2026-08-24 | [`research/8299_群聯.md`](research/8299_群聯.md) |

## 跨標的聯想入口

- **AI 伺服器／組裝**：2317 鴻海、2382 廣達、2356 英業達、6669 緯穎。
- **AI 電源／液冷**：2308 台達電、2301 光寶科、3017 奇鋐、6187 萬潤。
- **ABF／高階載板**：3037 欣興、8046 南電、6239 力成。
- **CCL／高速材料**：2383 台光電、1303 南亞。
- **光通訊／矽光**：3081 聯亞、4971 IET-KY、3163 波若威、2345 智邦、2313 華通。
- **記憶體週期**：2408 南亞科、2344 華邦電、6770 力積電、8299 群聯。
- **成熟製程／特殊製程**：2330 台積電、2303 聯電、2454 聯發科。

## 薄入口規則

- 需要投資判斷時，必須回到完整研究檔，檢查最新來源、估值、風險與賣出條件。
- 目標價、EPS、現價都帶日期，禁止把市場傳言當訂單事實。
- `obsidian-wiki/entities/` 對應頁提供主題、上下游與關聯標的的快速跳轉。

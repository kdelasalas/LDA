# LDA
Training session: Project LDA

Initial code guide: https://towardsdatascience.com/topic-modeling-and-latent-dirichlet-allocation-in-python-9bf156893c24

Sample data from: https://www.kaggle.com/therohk/million-headlines
- Collection of news headlines published over a period of 17 years
- Format: CSV ; Single File
- publish_date: Date of publishing for the article in yyyyMMdd format
- headline_text: Text of the headline in Ascii , English , lowercase
- Start Date: 2003-02-19 ; End Date: 2019-12-31

articles.csv sources:
'https://www.rappler.com/entertainment/celebrities/korean-star-park-seo-joon-philippine-telco-smart-communications-endorser?utm_medium=Social&utm_source=Twitter#Echobox=1603872147',
'https://www.preview.ph//culture/park-seo-joon-smart-communications-newest-endorser-a00268-20201028',
'https://www.gmanetwork.com/news/lifestyle/hobbiesandactivities/761741/park-seo-joon-is-the-newest-brand-ambassador-of-phl-telco/story/',
'https://mb.com.ph/2020/10/28/park-seo-jun-is-smart-communications-newest-endorser/',
'https://news.abs-cbn.com/entertainment/10/28/20/after-hyun-bin-and-son-ye-jin-park-seo-joon-also-joins-smart-family',
'https://outoftownblog.com/park-seo-joon-is-the-newest-smart-brand-ambassador/',
'https://www.google.com.ph/amp/s/www.philstar.com/entertainment/korean-wave/2020/10/28/2052929/k-ilig-park-seo-joon-newest-face-smart/amp/',
'https://www.noypigeeks.com/telecoms/smart-park-seo-joon-endorse-giga-k-video-99-promo/',
'https://www.gizguide.com/2020/10/smart-park-seo-joon-giga-k-video-promo.html?m=1',
'https://www.gmanetwork.com/news/lifestyle/hobbiesandactivities/761758/park-seo-jun-speaks-tagalog-in-new-phl-telco-commercial/story/?amp#click=https://t.co/bOxpEYlVeh',
'https://www.hallyudorama.com/park-seo-joon-is-smart-endorser-for-giga-k-video-with-viu-premium/'s
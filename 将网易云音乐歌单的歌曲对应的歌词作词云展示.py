
'''
（2）将网易云音乐歌单的歌曲对应的歌词作词云展示
'''
import re
import requests
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

headers = {
       'Referer'  :'http://music.163.com',
       'Host'     :'music.163.com',
       'Accept'   :'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
       'User-Agent':'Chrome/10'
    }

#得到指定歌单页面的 全部歌曲的歌曲ID，歌曲名
def get_songs(playlist_id):
    page_url='http://music.163.com/api/playlist/detail?id='+playlist_id
    #获取网页HTML
    res=requests.request('GET',page_url,headers=headers)
    # 输出歌单中歌曲数量
    print(len(res.json()['result']['tracks']))

    # 设置热门歌曲的ID，歌曲名称
    song_ids=[]
    song_names=[]

    for i in range(len(res.json()['result']['tracks'])):
        names=res.json()['result']['tracks'][i]['name']
        ids=res.json()['result']['tracks'][i]['id']
        song_names.append(names)
        song_ids.append(ids)
        print(names,' ',ids)
    return song_names,song_ids
 
# 得到某一首歌的歌词
def get_song_lyric(headers,lyric_url):
    res = requests.request('GET', lyric_url, headers=headers)
    if 'lrc' in res.json():
       lyric = res.json()['lrc']['lyric']
       new_lyric = re.sub(r'[\d:.[\]]','',lyric)
       return new_lyric
    else:
       return ''
       print(res.json())


#去掉停用词
def remove_stop_words(f):
    stop_words=['作词', '作曲', '编曲', 'Arranger', '录音', '混音', '人声', 'Vocal', '弦乐', 'Keyboard', '键盘', '编辑', '助理', 'Assistants', 'Mixing', 'Editing', 'Recording', '音乐', '制作', 'Producer', '发行', 'produced', 'and', 'distributed']
    for stop_word in stop_words:
        f=f.replace(stop_word,'')
    return f

#生成词云
def create_word_cloud(f):
    print('根据词频 生成词云')
    f=remove_stop_words(f)
    cut_text=' '.join(jieba.cut(f,cut_all=False,HMM=True))
    wc = WordCloud(
       font_path="./wc.ttf",
       max_words=100,
       width=2000,
       height=1200,
    )
    print(cut_text)
    wordcloud = wc.generate(cut_text)
    # 写词云图片
    wordcloud.to_file("wordcloud.jpg")
    # 显示词云文件
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    

# 设置歌单ID，【毛不易 | 不善言辞的深情】为753776811
playlist_id='753776811'
[song_names,song_ids]=get_songs(playlist_id)

#所有歌词
all_word=''
# 获取每首歌歌词
for (song_id, song_name) in zip(song_ids, song_names):
    # 歌词 API URL
    lyric_url = 'http://music.163.com/api/song/lyric?os=pc&id=' + str(song_id) + '&lv=-1&kv=-1&tv=-1'
    lyric = get_song_lyric(headers, lyric_url)
    all_word = all_word + ' ' + lyric
    print(song_name)

#根据词频，生成词云
create_word_cloud(all_word)


db_config = {}

daum_crawler = {
    'daum_news_site_info': {'ENTERTAIN': 'https://entertain.daum.net/ranking/popular',
                  'SPORTS': 'https://sports.daum.net/'}
}

nate_crawler = {
    'nate_news_site_info': {
        'NATE_NEWS': 'https://news.nate.com/rank/interest?sc=sisa',
        'NATE_ENTERTAIN': 'https://news.nate.com/rank/interest?sc=ent',
        'NATE_SPORTS': 'https://news.nate.com/rank/interest?sc=spo'
    },
    'nate_pann_site_info': {
        '결혼/시집/친정': 'https://pann.nate.com/talk/c20025',
        '지금은 연애중': 'https://pann.nate.com/talk/c20009',
        '해석 남/여': 'https://pann.nate.com/talk/c20007',
        '사랑과 이별': 'https://pann.nate.com/talk/c20006',
        '회사생활': 'https://pann.nate.com/talk/c20019',
    }
}

naver_crawler = {
    'naver_cate_link_dct': {
        '정치':
            {
                '대통령실': 'https://news.naver.com/main/list.naver?mode=LS2D&sid2=264&sid1=100&mid=shm&',
                '국회': 'https://news.naver.com/main/list.naver?mode=LS2D&sid2=265&sid1=100&mid=shm&',
                '외교/국방': 'https://news.naver.com/main/list.naver?mode=LS2D&sid2=267&sid1=100&mid=shm&',
                '북한': 'https://news.naver.com/main/list.naver?mode=LS2D&sid2=268&sid1=100&mid=shm&',
            },
        '사회':
            {
                '교육': 'https://news.naver.com/main/list.naver?mode=LS2D&sid2=250&sid1=102&mid=shm&',
                '환경': 'https://news.naver.com/main/list.naver?mode=LS2D&sid2=252&sid1=102&mid=shm&',
                '인권/복지': 'https://news.naver.com/main/list.naver?mode=LS2D&sid2=59b&sid1=102&mid=shm&',
                '노동': 'https://news.naver.com/main/list.naver?mode=LS2D&sid2=251&sid1=102&mid=shm&',
            },
        'IT/과학':
            {
                '모바일': 'https://news.naver.com/main/list.naver?mode=LS2D&sid2=731&sid1=105&mid=shm&',
                '컴퓨터': 'https://news.naver.com/main/list.naver?mode=LS2D&sid2=283&sid1=105&mid=shm&'
            },
        '글로벌':
            {
                '아시아/호주': 'https://news.naver.com/main/list.naver?mode=LS2D&sid2=231&sid1=104&mid=shm&',
                '미국/중남미': 'https://news.naver.com/main/list.naver?mode=LS2D&sid2=232&sid1=104&mid=shm&',
                '유럽': 'https://news.naver.com/main/list.naver?mode=LS2D&sid2=233&sid1=104&mid=shm&',
                '중동/아프리카': 'https://news.naver.com/main/list.naver?mode=LS2D&sid2=234&sid1=104&mid=shm&'
            }
    },
    'naver_category_lst': ['대통령실', '국회', '외교_국방', '북한', '교육', '환경', '인권_복지', '노동', '모바일', '컴퓨터',
                           '아시아_호주', '미국_중남미', '유럽', '중동_아프리카']
}

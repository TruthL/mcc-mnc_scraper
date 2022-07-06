import utils.func as func


def bulletin():
    url = "https://www.itu.int/pub/T-SP-OB"
    base = "https://www.itu.int/"
    #print(base)
    check_link = func.bullet_link(url)
    year = func.year_link(url)

    soup = func.get_soup(check_link[1])
    head = soup.find('strong')
    a = head.find_next('a',href = True)
    toc_link = base  + a['href']
    print(toc_link)
    if func.mnc_exist(toc_link):
        print('exists')
        down = a.find_next('a', string = 'DOWNLOAD',href = True)
        pdf = base + down
    else : print("not exist")
    #for link in check_link:
    #    soup = func.get_soup(link)
    #    head = soup.find('strong')
    #    print(head)



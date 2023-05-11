from django.core.paginator import Paginator, EmptyPage


def custom_paginator(request, queryset, per_page=3, page_param='page', current_page_each_side=2):
    # 获取当前页码,默认为1
    page_num = request.GET.get(page_param, '1')
    page_num = int(page_num) if page_num.isdecimal() else 1
    # 实例化Paginator,将数据集进行分页
    paginator = Paginator(queryset, per_page)

    try:
        # 获得当前页的数据集
        page = paginator.get_page(page_num)
    except EmptyPage as e:
        if page_num < paginator.num_pages:
            # 查询的当前页超出了分页后的最大页数,获取末页
            page_num = paginator.num_pages
            page = paginator.get_page(page_num)
        else:
            # 获取首页
            page_num = 1
            page = paginator.get_page(page_num)

    # 页码导航栏的页码列表
    page_list = paginator.get_elided_page_range(
        number=page_num,
        on_each_side=current_page_each_side,
        on_ends=0
    )

    return page, page_list

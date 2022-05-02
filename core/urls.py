"""
define the url routes of core api
"""
from django.urls import path
from core.api.auth import obtain_jwt_token, refresh_jwt_token
from core.api.chat import get_chat_list, delete_chat, message_read, create_chat, get_chat, push_message
from core.api.friend import list_friends, list_full_friends

from core.api.my_post import list_posts
from core.api.profile import get_profile
from core.api.search import search_user_list,search_user_full_list
from core.api.sign_up import change_password, change_email, CREATE_USER_API, FORGET_PASSWORD_API
from core.api.comment import create_comment, delete_comment, get_comment, get_comment_list

from core.api.user import follow, unfollow, list_favorite_recent, change_organization

from core.api.fan import list_fans, list_full_fans
from core.api.follower import list_followers, list_full_followers
from core.api.user_icon import USER_ICON_API,read_img,read_default_img
from core.api.notification import (NOTIFICATION_API, NOTIFICATION_SET_API)
from core.api.image import (IMAGE_API, IMAGE_SET_API)

from core.api.interpretation import createInterpretation, INTERPRETATION_API, \
  collectInterpretation, uncollectInterpretation, likeInterpretation, searchInterpretation, \
    transmitInterpretation, recommendInterpretation, downloadInterpretation, randomWalkInterpretation, \
      getAllInterpretation, queryVisitorNumber, queryKeywordTops, queryTagRatio

from core.api.user import get_all_user_info,delete_user,change_user_info

from core.api.platform.need_api import create_need, get_all_need, get_need_info, get_finished_need, \
  finish_need, get_proceeding_need, edit_need, delete_need, search_need, create_need_contact,\
    get_need_contact, expert_recommend

from core.api.platform.order_api import get_pending_order, get_cooperating_order, get_finished_order, finish_order, accept_order, \
  refuse_order, get_order_info, create_order, get_order_id, get_all_order

from core.api.enterprise import set_info, agree_enterprise, refuse_enterprise, get_enterpriseInfo, get_all_enterprise

from core.api.expert import setinfo, agree_expert, refuse_expert, get_expertInfo, get_all_expert

urlpatterns = [

    #user apis
    path('token-auth', obtain_jwt_token),
    path('token-refresh', refresh_jwt_token),
    path('user/create', CREATE_USER_API),
    path('user/change-password', change_password),
    path('user/change-email', change_email),
    path('user/forget-password', FORGET_PASSWORD_API),
    path('user/profile', get_profile),
    path('user/icon', USER_ICON_API),
    path('user/all',get_all_user_info),
    path('user/delete',delete_user),
    path('user/changeinfo',change_user_info),
    

    # comment apis
    path('comment/create', create_comment),
    path('comment/delete', delete_comment),
    path('comment/<int:id>', get_comment),
    path('comment', get_comment_list),

      # user apis
    path('user/<int:pid>/follow', follow),
    path('user/<int:pid>/unfollow', unfollow),
    path('user/organization', change_organization),
    # collection apis
    path('favorites/page/<int:pindex>', list_favorite_recent),


    # list posts - web PAGE
    path('post/<int:uid>', list_posts),

    #list fans - web PAGE
    path('fan/<int:uid>', list_fans),
    #list fans - app ROLL
    path('fan/roll/<int:uid>', list_full_fans),

    #list follower - web PAGE
    path('follower/<int:uid>', list_followers),
    #list follower - app ROLL
    path('follower/roll/<int:uid>', list_full_followers),


    #list friends - web PAGE
    path('friend/<int:uid>', list_friends),
    #list friends - app ROLL
    path('friend/roll/<int:uid>', list_full_friends),

    # notifications
    path('notification', NOTIFICATION_API),
    path('notification/page/<int:pindex>', NOTIFICATION_SET_API),

    # recommend related
    path('recommend', recommendInterpretation),
    path('Interpretation/popup', randomWalkInterpretation),

    # images
    path('image', IMAGE_API),
    path('image/page/<int:pindex>', IMAGE_SET_API),

    #chat
    path('chat/create',create_chat),
    path('chat/<int:id>', get_chat),
    path('chat/list', get_chat_list),
    path('chat/delete', delete_chat),
    path('chat/read', message_read),
    path('chat/push',push_message),

    #search - web PAGE
    path('user/search/<int:uid>',search_user_list),
    # search - app ROLL
    path('user/search/roll',search_user_full_list),

    # interpretations
    path('Interpretation', createInterpretation),
    path('Interpretation/<int:id>', INTERPRETATION_API),
    path('Interpretation/<int:eid>/favor', collectInterpretation),
    path('Interpretation/<int:eid>/unfavor', uncollectInterpretation),
    path('Interpretation/<int:id>/like', likeInterpretation),
    path('Interpretation/page/<int:pid>', searchInterpretation),
    path('Interpretation/<int:id>/transmit', transmitInterpretation),
    path('Interpretation/getall', getAllInterpretation),
    path('Interpretation/getvis', queryVisitorNumber),
    path('Interpretation/getkeywords', queryKeywordTops),
    path('Interpretation/gettags', queryTagRatio),

    #image
    path('images/<str:year>/<str:day>/icons/<str:file_name>',read_img),
    path('images/default_user_icon.jpg',read_default_img),

    # downloads
    path('download/Interpretation/<int:id>', downloadInterpretation),

    # platform<---需求平台

    ## need
    path('need', create_need), # 发布新的需求
    path('need/all', get_all_need), # 获取全部待解决需求
    path('need/<int:id>', get_need_info), # 获取某个需求的信息
    path('user/<int:uid>/need/<int:id>/edit', edit_need), # 修改需求
    path('user/<int:uid>/need/<int:id>/finish', finish_need), # 企业结束需求
    path('user/<int:uid>/need/finished', get_finished_need), # 获取某个企业正在进行的需求
    path('user/<int:uid>/need/proceeding', get_proceeding_need), # 获取某个企业已结束的需求
    path('user/<int:uid>/need/<int:id>', delete_need), # 企业删除需求
    path('need/search', search_need),
    path('need/contact', create_need_contact),
    path('need/get_contact', get_need_contact),

    path('need/<int:id>/expert_recommend', expert_recommend), # 基于需求的专家推荐

    ## order
    path('order', create_order),  # 企业创建新订单
    path('order/<int:id>', get_order_info), # 获取某个订单的信息
    path('user/<int:uid>/order/<int:id>/refuse', refuse_order), # 专家拒绝订单
    path('user/<int:uid>/order/<int:id>/accept', accept_order), # 专家接受订单
    path('user/<int:uid>/order/<int:id>/finish', finish_order), # 企业结束订单
    path('user/<int:uid>/order/finished', get_finished_order), # 获取某个用户（企业或专家）已完成订单（拒绝和结束）
    path('user/<int:uid>/order/pending', get_pending_order), # 获取某个用户（企业或专家）新请求的订单
    path('user/<int:uid>/order/cooperating', get_cooperating_order), # 获取某个用户（企业或专家）正在合作的订单
    path('user/<int:uid>/order/all', get_all_order),
    path('order/get', get_order_id),

    #enterprise
    path('enterprise/setinfo', set_info),
    path('enterprise/getinfo/<int:id>', get_enterpriseInfo),
    path('enterprise/agree/<int:id>', agree_enterprise),
    path('enterprise/refuse/<int:id>', refuse_enterprise),
    path('enterprise/getall', get_all_enterprise),

    #expert
    path('expert/setinfo', setinfo),
    path('expert/getinfo/<int:id>', get_expertInfo),
    path('expert/agree/<int:id>', agree_expert),
    path('expert/refuse/<int:id>', refuse_expert),
    path('expert/getall', get_all_expert),


]


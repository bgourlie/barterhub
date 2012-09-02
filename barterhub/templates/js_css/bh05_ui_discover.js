//////////ui discover//////////
ui_discover = []
ui_discover['general'] = function(){
    gElm['general'] = [];
    gElm['general']['content'] = elm('content');
    gElm['general']['login_status'] = elm('login_status');
};
ui_discover['browse'] = function(){
    gElm['browse'] = [];
    gElm['browse']['part'] = elm('part_browse');
    gElm['browse']['browse_go'] = elm('browse_go');
    gElm['browse']['browse_gr'] = elm('browse_gr');
    gElm['browse']['browse_so'] = elm('browse_so');
    gElm['browse']['browse_sr'] = elm('browse_sr');
};
ui_discover['category_navigator'] = function(){
    gElm['category_navigator'] = [];
    gElm['category_navigator']['part'] = elm('part_category_navigator');
    gElm['category_navigator']['lineage'] = elm('lineage');
    gElm['category_navigator']['current_category'] = elm('current_category');
    gElm['category_navigator']['child_categories'] = elm('child_categories');
    gElm['category_navigator']['category_navigator_label'] = elm('category_navigator_label');
};
ui_discover['option'] = function(){
    gElm['options'] = [];
    gElm['options']['part'] = elm('part_options');
};
ui_discover['login_or_signup'] = function(){
    gElm['login_or_signup'] = [];
    gElm['login_or_signup']['part'] = elm('part_login_or_signup');
    gElm['login_or_signup']['login_link'] = elm('login_link');
    gElm['login_or_signup']['signup_link'] = elm('signup_link');
};
ui_discover['login'] = function(){
    gElm['login'] = [];
    gElm['login']['part'] = elm('part_login');
    gElm['login']['email'] = elm('email');
    gElm['login']['password'] = elm('password');
    gElm['login']['salt'] = elm('salt');
    gElm['login']['login_button'] = elm('login_button');
};

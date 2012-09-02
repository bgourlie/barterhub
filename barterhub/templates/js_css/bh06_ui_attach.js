////////ui attach////////////
ui_attach = []
ui_attach['login_or_signup'] = function(){
    addEvent(gElm['login_or_signup']['login_link'], 'click', function(){
            updateUIState(STATE_AT_LOGIN);
    });
    addEvent(gElm['login_or_signup']['signup_link'], 'click', function(){
            alert('signup');
    });
};

ui_attach['login'] = function(){
        addEvent(gElm['login']['email'], 'change', function(){
            requestSalt();
        });
        addEvent(gElm['login']['login_button'], 'click', function(){
            doLogin();
        });
};

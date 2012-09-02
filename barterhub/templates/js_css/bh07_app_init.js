////////////async lib////////////
function initComplete(){
    elm('loading').style.display = 'none';
    gElm['general']['content'].style.display = 'block';                    
}

function uiInit(){
    for(var ui_element in ui_discover){
        console.log('Discovering ' + ui_element);
        ui_discover[ui_element]();
        ui_discover[ui_element] = null;
    }
    ui_discover = null;
    for(var ui_element in ui_attach){
        console.log('Attaching ' + ui_element);
        ui_attach[ui_element]();
        ui_attach[ui_element] = null;
    }
    ui_attach = null;
}

function appInit(){
    //init application
    console.log('Requesting Session Cookie...');
        console.log('Calling init async...');
        asyncRequest('/async/app_init', function(success, response){
            if(success){
                console.log('app_init returned: ' + response);
                //Getting session specific initialization data...
                var arr_init_data = response.split(',');
                var uiState = (arr_init_data[0] == String(STATE_LOGGED_IN)) ? STATE_LOGGED_IN : STATE_NOT_LOGGED_IN;
                gEmailAddress = arr_init_data[1];
                updateUIState(uiState);
                //check to make sure we received the cookie
                var cookie_valid = false;
                try{
                    cookie_valid = document.cookie.indexOf(SESSION_COOKIE_NAME + '=') > -1;
                }catch(err){
                    cookie_valid = false;
                }
                
                if(cookie_valid){
                    //if we get here, initialization process is complete
                    initComplete();
                }else{
                    //cookie doesn't exist
                    console.log('Cookie doesn\'t exist');
                    displayError(ERR_COOKIES_NOT_ENABLED);
                }
                
            }else{
                //app_init failed
                console.log('Init async failed');
                displayError(ERR_INIT_FAILED);
            }
        });
}

DOMReady(function(){
    //if javascript is enabled then this block will show,
    //otherwise a <noscript /> tag will show an error
    //saying javascript is disabled
    elm('javascript_enabled').style.display = 'block';
    uiInit();
    appInit();
});
////////ui lib/////////////
function displayError(error){
    elm('loading').innerHTML = '<span class="loading_error"><h2>' + ERR_HEADER + '</h2><h3>' + error + '</h3></span>';
}

function updateUIState(uiState){
    console.log('Updating UI State...');
    var login_status = gElm['general']['login_status'];
    var options_part = gElm['options']['part'];
    var login_or_signup_part = gElm['login_or_signup']['part'];
    var login_part = gElm['login']['part'];
    var email = gElm['login']['email'];
    var password = gElm['login']['password'];
    var login_button = gElm['login']['login_button'];
    
    switch(uiState){
    case STATE_NOT_LOGGED_IN:
        console.log('New state: Not Logged In');
        login_status.innerHTML = LBL_NOT_LOGGED_IN;
        options_part.style.display = 'none';
        login_or_signup_part.style.display = 'block';
        login_part.style.display = 'none';
        break;
    case STATE_LOGGED_IN:
        console.log('New state: Logged In');
        login_status.innerHTML = LBL_LOGGED_IN_AS + gEmailAddress;
        options_part.style.display = 'block';
        login_or_signup_part.style.display = 'none';
        login_part.style.display = 'none';
        break;
        
    case STATE_AT_LOGIN:
        console.log('New state: At Login');
        login_status.innerHTML = LBL_NOT_LOGGED_IN;
        options_part.style.display = 'none';
        login_or_signup_part.style.display = 'none';
        login_part.style.display = 'block';
        email.value = '';
        password.value = '';
        login_button.disabled = false;
        login_button.value = LBL_LOG_IN;
        break;
    case STATE_LOGGING_IN:
        console.log('New state: Logging In');
        login_button.disabled = true;
        login_button.value = LBL_LOGGING_IN;
        break;
    default:
        throw "Invalid Login State";
    }
    
    gUIState = uiState;
}

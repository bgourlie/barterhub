///////////async lib/////////////////
function requestSalt(){
    var email = gElm['login']['email'].value;
    var login_button = gElm['login']['login_button'];
    
    login_button.disabled = true;
    asyncRequest('async/request_salt?' + email, function(success, response){
        if (success){
            gElm['login']['salt'].value = response;
        }else{
            alert('getSalt() failed.');
        }
        login_button.disabled = false;
    });
}

function doLogin(){
    updateUIState(STATE_LOGGING_IN);
    var email = gElm['login']['email'].value;
    var password = gElm['login']['password'];
    var salt = gElm['login']['salt'];
    var password_hash = hex_md5(salt.value + password.value);
    
    asyncRequest('async/do_login?' + email + ',' + password_hash, function(success, response){
        if(success){
            login_success = (response == '1') ? true : false;
            if(login_success){
                updateUIState(STATE_LOGGED_IN);
            }else{
                alert('login failed, wrong email or password');
                updateUIState(STATE_AT_LOGIN);
            }
        }else{
            alert('doLogin() failed');
            updateUIState(STATE_AT_LOGIN);
        }
    });
}



function updateCategoryNavigator(category_key){
    asyncRequest('/async/category?c=' + category_key, function(success, response){
        var arr_category_data = response.split(';');
        var arr_current_category = arr_category_data[0].split(',');
        var arr_lineage = arr_category_data[1].split(',');
        var arr_children = arr_category_data[2].split(',');
        console.log('current category: %o', arr_current_category);
        console.log('lineage: %o', arr_lineage);
        console.log('children: %o', arr_children);
        gElm['category_navigator']['current_category'].innerHTML = arr_current_category[1];
        
        var str_lineage = '';
        for(var i = 0; i < arr_lineage.length - 1; i+=2){
            str_lineage += '<a href="#" class="category_link" name="' + arr_lineage[i] + '">' + arr_lineage[i+1] + '</a>&nbsp;&raquo;';
        }
        gElm['category_navigator']['lineage'].innerHTML = str_lineage;
        
        var str_child_categories = '<ul>';
        for(var i = 0; i < arr_children.length - 1; i+=2){
            str_child_categories += '<li><a href="#" class="category_link" name="' + arr_children[i] + '">' + arr_children[i+1] + '</a></li>';
        }
        str_child_categories += '</ul>';
        gElm['category_navigator']['child_categories'].innerHTML = str_child_categories;
        
        arr_category_links = elmsByClass('category_link');
        
        //add event handlers to all category links
        for(var i in arr_category_links){
            addEvent(arr_category_link[i],'click',function(){
                updateCategoryNavigator(this.name);
            });
        }
    });
}

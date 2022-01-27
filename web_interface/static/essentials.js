//modal stuff
var backdrop = document.getElementById("backdrop");
var modal= document.getElementById("Modal_to_open");
var modal_header = document.getElementById("modal_header");
var modal_status = document.getElementById("modal_status");
var modal_msg = document.getElementById("modal_msg");
var site_alert = document.getElementById("site_alert");
var header = document.getElementById("header_replace");

var api_url = document.getElementById("api_url").innerHTML

function openModal() {
    backdrop.style.display = "block";
    modal.style.display = "block";
    modal.classList.add("show");
}
function closeModal() {
    backdrop.style.display = "none";
    modal.style.display = "none";
    modal.classList.remove("show")
}

function check_status(){
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    console.log(urlParams);
    console.log(urlParams.get("modal_status"))
    console.log(urlParams.get("error"));
    if (urlParams.get("modal_rec_msg")){
        //change Modal
        modal_msg.innerHTML = urlParams.get("modal_rec_msg");
        modal_status.innerHTML = urlParams.get("modal_headline");
        modal_header.classList = "modal-header "+urlParams.get("modal_type");
        //open modal
        openModal();
    }
    if (urlParams.get("alert_msg") && urlParams.get("alert_type")){
        //cahnge Modal
        site_alert.innerHTML = urlParams.get("alert_msg");
        site_alert.classList = "alert "+urlParams.get("alert_type");
        //remove vars from url
        //open alert
        showAlert();
    }

    var newURL = window.location.href.split("?")[0];
    window.history.pushState('object', document.title, newURL);
}

function showAlert(){
    site_alert.style.display ="inline-block";
    site_alert.style.opacity = 1;
    setTimeout(
        function() {
          fade_alert();
        }, 3000);
    
}

function fade_alert(){
    opacity = site_alert.style.opacity
    site_alert.style.opacity -= 0.02
    if (opacity > 0.1){
        setTimeout(function() {fade_alert();}, 50);
    } else {
        hide_alert();
    }
    
}
function hide_alert(){
    site_alert.style.opacity = 0;
    site_alert.style.display ="none";
}

function copy_to_clipboard(obj){
    console.log(obj)
    /* Get the text field */
      
    /* Copy the text inside the text field */
    navigator.clipboard.writeText(obj.innerHTML);

    site_alert.innerHTML = "copied to clipboard!";
    site_alert.classList = "alert alert-success";

    showAlert()

}


// Cookies
function createCookie(name, value, days) {
    if (days) {
        var today = new Date();
        var valid_until = new Date();
        valid_until.setDate(today.getDate()+days);
        var expires = "; expires=" + valid_until.toUTCString();
    } else {
        var expires = "";
    }              

    document.cookie = name + "=" + value + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function deleteCookie(name) {
    createCookie(name, "", -1);
}


function update_header(){
    var header_replace = document.getElementById("header_replace")
    post(type="GET",{},"header",header_replace)
}

update_header()
check_status();

function post(type, input_object = Object(), api_endpoint, object_to_update = null,include_token = true) {

    if(include_token){
        token_cookie = getCookie("token");
        if(token_cookie){
            if (token_cookie.length < 2){
                console.log("did not append cookie to json")
            } else {
                input_object["token"] = getCookie("token");
            }
        } 
    }

    if(type != "GET"){
        //create json from object
        to_send = JSON.stringify(input_object)
    } else {
        to_send = input_object
    }

    
    //console.log(to_send)
    return $.ajax
    ({
        type: type,
        url: api_url+"/"+api_endpoint,
        dataType: "json",
        //processData: false,
        async: true,
        //json object to sent to the authentication url
        data: to_send,
        success: data => process_response(data,object_to_update),
        error: data => process_response(data.responseJSON,object_to_update)
    })
}

function process_response(json_obj,to_change){
    console.log(json_obj)
    console.log(to_change)
    //empty redirect params
    var redirect_params = new URLSearchParams()

    //handle login!
    if(json_obj.Login){
        createCookie("token",json_obj.Login.token,json_obj.Login.valid_days)
    }
    //handle login!
    if(json_obj.Logout){
        deleteCookie("token")
    }
    //handle alerts
    if(json_obj.Alert){
        site_alert.innerHTML = json_obj.Alert.alert_msg;
        site_alert.classList = "alert "+json_obj.Alert.alert_type;
        
        redirect_params.append("alert_type", json_obj.Alert.alert_type);
        redirect_params.append("alert_msg", json_obj.Alert.alert_msg);

        showAlert();
    }
    //handle Modals
    if (json_obj.Modal){
        //change Modal
        modal_msg.innerHTML = json_obj.Modal.modal_rec_msg;
        modal_status.innerHTML = json_obj.Modal.modal_headline;
        modal_header.classList = "modal-header "+json_obj.Modal.modal_type;

        //update redirect params!
        redirect_params.append("modal_type", json_obj.Modal.modal_type);
        redirect_params.append("modal_rec_msg", json_obj.Modal.modal_rec_msg);
        redirect_params.append("modal_headline", json_obj.Modal.modal_headline);

        //open modal
        openModal();
    }
    //handle pre-rendered content!
    if (json_obj.pre_rendered){ 
        to_change.innerHTML = json_obj.pre_rendered.content;
    }
    
    //handle Redirects
    if (json_obj.Redirect){
        console.log(redirect_params)
        console.log(redirect_params.toString())
        //redirect!
        window.location.replace(json_obj.Redirect.redirect_url+"?"+redirect_params)
    }
}

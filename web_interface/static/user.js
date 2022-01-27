var username = document.getElementById("username");

function del_user(){

    if (confirm("are ya sure about that?")){
        alert("reeee")
        post("POST",{},"user/delete/"+username.innerHTML)
    }
    

}

function* entries(obj) {
    for (let key of Object.keys(obj)) {
      yield [key, obj[key]];
    }
 }

async function get_user_data(){

    url = window.location.href.split("/")
    username_url= url.pop().split("?")[0];

    let data = await post("GET",{},"user/"+username_url)
    console.log(data)


    if(data.user){
        document.getElementById("username").innerHTML = data.user.username;
        document.getElementById("useravatar").src=api_url+"/avatars/"+data.user.avatar;
        new_obj = data.user;

        userinfo_list = document.createElement("ul");
        for(iterator in Object.keys(new_obj)){
            key = Object.keys(new_obj)[iterator];
            li_item = document.createElement("li");
            li_item.innerHTML = key+": "+new_obj[key];
            userinfo_list.appendChild(li_item) ;  
        }

        if(data.token.last_login){
            li_item = document.createElement("li");
            li_item.innerHTML = "last_login: "+data.token.last_login;
            userinfo_list.appendChild(li_item);
        }


        document.getElementById("user_info").innerHTML = ""
        document.getElementById("user_info").appendChild(userinfo_list);      

    }
    if(data.token.token && data.Admin){
        document.getElementById("token_info_button").style.display="inline"
        document.getElementById("token_info").innerHTML = "<ul><li>Last_Token_Creation: "+data.token.last_login+"</li><li>valid_for: "+data.token.valid_for+"</li><li>valid_until: "+data.token.valid_until+"</li><li>Token: <code>"+data.token.token+"</code></li></ul>"

    }
    if(data.user.username ==  url.pop().split("?")[0] || data.Admin){
        document.getElementById("token_edit_button").style.display="inline"
        document.getElementById("delete").style.display="inline"
    }
}

get_user_data()


function change(){
    alert("would change stuff if that would be implemented lol")
}
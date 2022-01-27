var user_container = document.getElementById("usercontainer")

async function get_users(){
    console.log("reeee")
    json_ = {}
    let data = await post("GET",{},"users")
    console.log(data.users)

    for (user in data.users){
        console.log(data.users[user])

        let userlink = document.createElement('a')
        userlink.href = "/user/"+data.users[user].username
        
        let userbox = document.createElement('button')
        userbox.classList = "btn btn-primary"

        useravatar = document.createElement('img')
        useravatar.src=api_url+"/avatars/"+data.users[user].avatar
        useravatar.style.height = "50px"
        useravatar.style.borderRadius = "100%"
        useravatar.style.marginRight ="10px"
        useravatar.style.marginLeft ="-5px"

        userlink.append(userbox)
        userbox.appendChild(useravatar)
        userbox.innerHTML = userbox.innerHTML + data.users[user].username

        user_container.appendChild(userlink)
        userlink.style.margin="5px"
    }
}

get_users()